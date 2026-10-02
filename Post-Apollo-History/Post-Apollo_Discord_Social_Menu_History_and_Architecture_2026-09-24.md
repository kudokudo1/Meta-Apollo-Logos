# Post-Apollo Discord / Social Menu
## Complete History, Architecture, Landmark Fixes, and Future Direction

**Documentation date:** 2026-09-24  
**Project:** Taskbars // Post-Apollo — Quickshell Messaging / Discord integration  
**Environment:** Fedora Silverblue 44, Sway/Wayland, Quickshell 0.2.1, Qt 6.11.2, Vesktop + Vencord  
**Primary Quickshell path:** `~/.config/quickshell/widgets/messanger/`  
**Discord client:** Flatpak `dev.vencord.Vesktop`  
**Current model:** Quickshell social shell + separate Vesktop Wayland surface, synchronized strongly enough to behave like one window

---

# 1. Purpose

This document records the evolution of the Post-Apollo Discord menu from the original reusable Quickshell messaging panel to the current Quickshell + Sway + Vesktop + Vencord architecture.

It preserves:

- the architectural pivots that mattered;
- failed approaches that should not be rediscovered;
- tracking, timing, resizing, startup, focus, and geometry fixes;
- the current split between QML, Sway, Python, Vesktop, and Vencord;
- the custom resize-performance and Escape-key bridge work;
- current invariants and regression hazards;
- the next planned architecture, especially animated opening.

The most important lesson is that several problems initially looked like one problem but actually belonged to different layers:

```text
visual layout
!=
native Wayland surface lifecycle
!=
Sway compositor geometry
!=
external Vesktop lifecycle
!=
live move/resize tracking
!=
Discord renderer performance
!=
keyboard ownership / Escape routing
```

Most landmark fixes came from identifying the correct owner for a problem.

---

# 2. Source-of-truth rule

When old notes and live code disagree, use this precedence:

1. **Current working source on the machine**
2. **A change explicitly tested and confirmed as working**
3. **Newest full-file snapshot**
4. **Older project archives**
5. **Historical proposals and experiments**

An older complete file is not automatically safer than a newer partial one. Several major regressions can be reintroduced by restoring old code that looks structurally clean.

The oldest baseline used here is the **2026-09-10 Quickshell Messaging Complete Archive**, when Session was working and Discord was still the next planned messenger.

---

# 3. Executive summary

The current Discord integration is deliberately **not true native embedding**.

Vesktop remains its own Wayland/Sway window. Quickshell cannot simply parent it like a QML child. Instead, Post-Apollo builds a coordinated composite:

```text
┌─────────────────────────────────────────────────────────────────┐
│ Quickshell social FloatingWindow                                │
│                                                                 │
│ ┌────────────┬────────────────────────────────────────────────┐ │
│ │ AppSelector│                                                │ │
│ │ 110 px     │             real Vesktop                      │ │
│ │            │        positioned by Sway on top              │ │
│ │            │                                                │ │
│ └────────────┴────────────────────────────────────────────────┘ │
│  ContactList / ChatFeed shell remains underneath Discord       │
└─────────────────────────────────────────────────────────────────┘
```

The key result is:

> **Two native windows are choreographed as one user-facing object.**

Current responsibility split:

```text
MessagingW.qml
    semantic state
    app selection
    canonical shared geometry
    lifecycle policy
    Quickshell shell visuals
          │
          ▼
DiscordGeometry.py
    persistent Sway IPC
    geometry sampling
    direct leader/follower movement
          │
          ▼
Sway
    actual toplevel positions/sizes
          │
          ├── QS_SOCIAL_MENU
          └── vesktop

Vencord plugin
    resize-performance state
    Escape capture while Vesktop has focus
          │
          ▼
Quickshell IPC
    close social menu
    move Vesktop to scratchpad
    keep Discord process alive
```

---

# 4. Phase Zero — reusable messaging shell before Discord

The project began as a reusable in-shell messaging surface rather than a Discord-specific widget.

Target interaction:

```text
APP SELECTOR
     ↓
CONTACT LIST
     ↓
MESSAGE FEED / COMPOSER
```

Original app indices:

```text
0 = Session
1 = Discord
2 = Telegram
```

Session became the first real backend and defined the first architecture:

```text
modules/Sessions.qml
        │
        ▼
widgets/messanger/MessagingW.qml
        ├── AppSelector.qml
        ├── ContactList.qml
        └── ChatFeed.qml
                 │
                 ▼
services/messaging/SessionAdapter.qml
```

The original long-term idea was adapter reuse:

```text
backend
   ↓
adapter
   ↓
normalized conversations/messages
   ↓
shared Quickshell frontend
```

Discord eventually required a different backend strategy, but the reusable social shell remained the foundation.

---

# 5. Landmark pre-Discord fix — keep the root native PanelWindow alive

The obvious early implementation was:

```qml
PanelWindow {
    visible: menuOpen
}
```

Repeated opening and closing eventually produced a native Qt/Quickshell crash. The captured call path implicated native visibility/window creation/reparenting, not Session data or styling.

A `Qt.callLater()` timing workaround did not solve the underlying lifecycle problem.

The accepted rule became:

> **LANDMARK DECISION — Keep the native controller `PanelWindow` alive. Hide child content and collapse input instead of recreating the native surface on every toggle.**

Conceptually:

```qml
PanelWindow {
    visible: true

    mask: Region {
        width: menuOpen ? width : 0
        height: menuOpen ? height : 0
    }

    Item {
        visible: menuOpen
    }
}
```

This produced a durable lesson:

```text
QML visibility is not always "just styling"
when the object owns a native Wayland surface.
```

---

# 6. Landmark pre-Discord fix — Wayland stacking is not QML z-order

The messaging panel once appeared under another Quickshell window, especially the Power surface.

Child `z` values could not solve it because separate `PanelWindow`s are separate native Wayland surfaces.

The accepted fix was:

```qml
import Quickshell.Wayland

PanelWindow {
    WlrLayershell.layer: WlrLayer.Overlay
}
```

> **LANDMARK DECISION — When independent Quickshell windows cover each other, reason about Wayland/layer-shell stacking, not only QML item z-order.**

That distinction later becomes central to the Discord architecture.

---

# 7. Discord strategy decision — use real Vesktop/Vencord

By 2026-09-13 the project considered several approaches:

```text
1. Real Vesktop styled/positioned by Sway
2. Nested compositor techniques
3. Qt WebEngine
4. Custom Discord adapter + rebuilt QML client
5. Experimental true native embedding
```

The chosen direction was the stable real-client path:

> **LANDMARK DECISION — Use Vesktop/Vencord as the actual Discord client and make it visually belong to the Quickshell social shell.**

Why this direction won:

- real Discord functionality remains intact;
- Vencord enables deep customization;
- no need to rebuild Discord itself;
- Sway already provides mature floating-window controls;
- effort can go into choreography and Post-Apollo presentation.

The choice also matched the desire to experiment with Vencord rather than treat Discord as a static foreign app.

---

# 8. Central realization — external Vesktop is not a QML child

The first Discord experiments exposed the main ownership boundary:

```text
Quickshell QML layout
    does not own
Vesktop's Wayland toplevel.
```

Therefore the mental model:

```text
"put Discord in this Rectangle and anchor.fill it"
```

is wrong.

Vesktop's real position and size must ultimately be controlled through the compositor.

This created two coordinate systems:

```text
Quickshell-local geometry
        vs
Sway-global compositor geometry
```

---

# 9. Failed or rejected geometry approaches

## 9.1 `mapToGlobal()`

A natural attempt was to use QML global mapping to derive Vesktop coordinates.

Under the Wayland/layer-shell arrangement it did not provide a reliable bridge to the Sway coordinates needed for the external surface.

It was reverted.

**Lesson:** do not treat QML global mapping as compositor truth for this external Wayland window.

## 9.2 Arbitrary Discord Y offsets

Hard-coded top offsets were also rejected. They could make one screenshot look correct while tying the system to one specific panel arrangement.

**Lesson:** derive from workspace/compositor geometry, not magic numbers.

## 9.3 `floating enable` at the wrong lifecycle point

Early commands tried to force `floating enable` while Vesktop was hidden in scratchpad state. Sway could reject or mishandle that transition.

The architecture learned to respect scratchpad/mapping lifecycle rather than inject unnecessary state changes.

---

# 10. First useful Vesktop lifecycle — scratchpad show, then snap

The first stable-enough lifecycle became:

```text
ensure Vesktop exists
        ↓
move Vesktop to scratchpad
        ↓
scratchpad show
        ↓
allow Sway to map it visibly
        ↓
resize/move/focus it
```

Representative concept:

```bash
if Vesktop does not exist:
    launch Flatpak
    wait for app_id=vesktop

move Vesktop to scratchpad
scratchpad show

later:
    resize
    move absolute
    focus
```

This is where timing became a first-class architectural concern rather than an incidental bug.

---

# 11. Sway workspace geometry becomes global placement authority

Instead of trusting QML global mapping, `MessagingW.qml` began asking Sway for visible workspace geometry:

```bash
swaymsg -r -t get_workspaces
```

The selected workspace populates:

```qml
swayAreaX
swayAreaY
swayAreaWidth
swayAreaHeight
swayGeometryReady
```

Default positions can then be derived from the actual compositor workspace.

> **LANDMARK DECISION — Global placement derives from Sway workspace geometry.**

This removed fragile assumptions about absolute origin and panel offsets.

---

# 12. Requirement change — Discord and the shell must move as one unit

The target interaction evolved from:

```text
Quickshell = static shell
Discord = independently positioned guest
```

into:

```text
AppSelector
ContactList shell
ChatFeed shell
Discord
        ↓
one logical movable/resizable object
```

The user explicitly wanted Sway `$mod` move/resize behavior to act as though the whole social receiver were one window.

This requirement drove the largest structural refactor.

---

# 13. Landmark architecture — controller PanelWindow + visible FloatingWindow

The original root was a layer-shell `PanelWindow`. That preserved shell anchoring but was not the right visible object for normal Sway floating-window manipulation.

The solution split the roles:

```text
MessagingW root PanelWindow
    = permanent controller
    = shell.qml contract
    = click-through
    = semantic owner

socialWindow FloatingWindow
    = actual visible social body
    = normal Sway toplevel
    = Mod-movable / Mod-resizable
```

> **LANDMARK ARCHITECTURE — Preserve the controller `PanelWindow`, but move the visible social menu into a normal `FloatingWindow`.**

Conceptually:

```qml
PanelWindow {
    id: messagingWindow
    visible: true
    focusable: false

    mask: Region {
        width: 0
        height: 0
    }

    FloatingWindow {
        id: socialWindow
        title: "QS_SOCIAL_MENU"
        visible: messagingWindow.menuOpen
    }
}
```

This gave the project both shell compatibility and normal Sway floating controls.

`shell.qml` was deliberately kept out of the geometry churn.

---

# 14. `DiscordBackingW.qml` becomes obsolete

Earlier designs considered or used a separate Discord backing surface.

Once `socialWindow` became the visible shared body, that extra geometry owner stopped being useful.

The real underlay already exists:

```text
socialWindow
    ├── AppSelector
    ├── ContactList
    └── ChatFeed
```

> **LANDMARK CLEANUP — `DiscordBackingW.qml` is obsolete in the current architecture and should not be reintroduced as a competing geometry surface.**

---

# 15. Discord mode preserves the physical Quickshell shell

When Discord is active, Quickshell does not simply destroy ContactList and ChatFeed.

Instead:

- their inner Session-specific contents disappear;
- the dark backing remains;
- the cyan perimeter remains;
- Vesktop sits on top of the content region.

A small inset leaves the receiver border visible around Vesktop.

Current known value:

```qml
property int discordInset: 1
```

Conceptually:

```qml
discordX =
    sharedPanelX
    + appSelectorWidth
    + discordGap
    + discordInset

discordY = sharedPanelY + discordInset
```

The result is not merely "Discord next to Quickshell." It is Discord visually mounted into the Post-Apollo social receiver.

---

# 16. Canonical shared geometry

The next major abstraction was one logical rectangle:

```qml
sharedPanelX
sharedPanelY
sharedPanelWidth
sharedPanelHeight
```

Known current default dimensions:

```qml
defaultPanelWidth: 1210
defaultPanelHeight: 1355
```

Important width values:

```qml
appSelectorWidth: 110
contactListWidth: 200
discordGap: 0
discordInset: 1
```

The whole social `FloatingWindow` uses the shared rectangle.

Discord gets a derived rectangle inside it.

```text
shared rectangle
     │
     ├── socialWindow = full rectangle
     │
     └── Vesktop = content rectangle after AppSelector/inset
```

---

# 17. Bidirectional geometry adoption

The user wanted either visible window to be a usable manipulation handle.

Therefore tracking became bidirectional.

When social leads:

```text
social moved/resized
        ↓
adoptSocialGeometry()
        ↓
shared geometry changes
        ↓
Discord follows
```

When Discord leads:

```text
Discord moved/resized
        ↓
adoptDiscordGeometry()
        ↓
reconstruct full shared rectangle
        ↓
social follows
```

Discord-to-shared conversion restores the hidden AppSelector portion:

```qml
sharedPanelX =
    discordRect.x
    - appSelectorWidth
    - discordGap
    - discordInset

sharedPanelWidth =
    appSelectorWidth
    + discordGap
    + discordRect.width
    + discordInset * 2
```

This is what turns two windows into one logical geometry system.

---

# 18. Landmark startup fix — Vesktop splash is a guest, never geometry authority

Vesktop can briefly present a smaller startup/splash-like surface.

If that temporary surface is adopted as real geometry, the entire social unit collapses around it.

The fix established a critical startup rule:

> **LANDMARK FIX — The small Vesktop startup surface is a guest inside the existing Discord slot. It does not define shared geometry.**

Known thresholds:

```qml
discordStartupMaxWidth: 760
discordStartupMaxHeight: 760
```

Behavior:

```text
small startup surface
        ↓
recognize as startup-like
        ↓
leave shared geometry untouched
        ↓
center startup surface inside Discord slot
        ↓
wait for real Discord surface
```

When the real surface appears:

```text
existing shared social geometry wins
        ↓
Discord snaps into slot
        ↓
normal bidirectional tracking begins
```

The project intentionally avoided letting a first-launch quirk become the architecture's geometry authority.

---

# 19. Early tracking — Timer → bash → swaymsg → jq

The first live tracker used a repeated process chain roughly like:

```text
QML Timer
   ↓
bash
   ↓
swaymsg
   ↓
jq
   ↓
QML receives geometry
   ↓
QML calculates correction
   ↓
another swaymsg
```

It worked functionally, but every sample paid process-spawn and parsing overhead.

For interactive move/resize, especially on a high-refresh display, that latency became visible.

---

# 20. Geometry ping-pong bug

Once both social and Discord could update shared geometry, a new failure mode appeared:

```text
Discord moves
   ↓
social differs
   ↓
social adopted too early
   ↓
Discord corrected back
   ↓
Discord now differs
   ↓
repeat
```

This was a **leader ambiguity** bug.

The fix was not "poll faster." It was to decide which window is the user's active leader before adopting geometry.

Accepted pattern:

```qml
if (discordChanged) {
    adoptDiscordGeometry(discordRect);
    syncSocialGeometry(false);
    return;
}

if (socialChanged) {
    adoptSocialGeometry(socialRect);
    syncDiscordGeometry(false);
    discordRaiseDelay.restart();
}
```

When both differ in one compositor snapshot, focus helps identify the active leader.

Another tuning change was:

```qml
geometryTolerance: 0
```

> **LANDMARK FIX — Decide leader first, adopt only the leader, move only the follower.**

---

# 21. Landmark performance architecture — persistent `DiscordGeometry.py`

The shell-process polling model was replaced by a persistent Python helper:

```text
~/.config/quickshell/widgets/messanger/DiscordGeometry.py
```

`MessagingW.qml` keeps it alive:

```qml
Process {
    id: groupGeometryHelper
    command: [
        "python3",
        Quickshell.shellPath("widgets/messanger/DiscordGeometry.py"),
        "--interval-ms",
        String(messagingWindow.geometryPollIntervalMs)
    ]

    running: true
    stdinEnabled: true
}
```

Communication is simple and persistent:

```text
Python → QML
    newline-delimited JSON geometry snapshots

QML → Python
    newline-delimited JSON commands over stdin
```

Representative operations:

```text
config
mode
watch
sample
sync
centerDiscord
focusDiscord
```

Known sample interval:

```qml
geometryPollIntervalMs: 8
```

> **LANDMARK ARCHITECTURE — Geometry synchronization became a persistent IPC service instead of a repeated shell command pipeline.**

---

# 22. Fast path v2 — Python moves the follower directly

Persistent Python removed process-spawn overhead, but a live drag could still take this route:

```text
Python sees movement
    ↓
QML receives movement
    ↓
QML decides follower position
    ↓
QML sends command back to Python
    ↓
Python tells Sway
```

For the interactive hot path that was still unnecessary latency.

The next version moved immediate follower motion into Python itself.

Discord leads:

```text
Discord focused + moving/resizing
        ↓
Python reads Discord geometry
        ↓
Python directly moves socialWindow
        ↓
QML receives canonical shared geometry afterward
```

Social leads:

```text
socialWindow focused + moving/resizing
        ↓
Python reads social geometry
        ↓
Python directly moves Discord
        ↓
QML catches up semantically afterward
```

QML recognizes fast-path state such as:

```text
payload.fastLeader
payload.shared
```

and updates canonical state without sending another follower correction.

> **LANDMARK FIX — The live manipulation path bypasses the Python → QML → Python round trip. QML stays semantic authority; Python performs immediate compositor choreography.**

This is the change after which the unit began to feel like a normal window.

---

# 23. Delayed Discord raise after social drag

When Discord is active, Vesktop needs to sit above its Quickshell shell.

But focusing it during an active Sway Mod-move/resize can cancel the user's compositor operation.

The solution is a delayed raise after the drag settles.

Known timer:

```qml
interval: 260
```

Flow:

```text
social being moved/resized
        ↓
do not focus Discord mid-drag
        ↓
drag settles
        ↓
short delay
        ↓
raise/focus Discord
```

This is another example of treating timing as explicit lifecycle policy instead of adding random focus calls.

---

# 24. Remaining resize lag was inside Discord, not geometry

After the Python fast path, outer geometry was largely correct.

The remaining lag mainly appeared while Vesktop reflowed and repainted Discord contents during resize.

That separated two problems:

```text
compositor geometry latency
!=
Electron/Discord renderer cost
```

The correct fix therefore moved into Vencord.

---

# 25. `RiceResizePerf` — custom Vencord resize-performance plugin

Custom plugin path:

```text
~/.config/vencord/src/userplugins/riceResizePerf/
    ├── index.ts
    └── native.ts
```

The original resize behavior adds a temporary root class during resize:

```text
rice-resizing
```

Representative logic:

```ts
function onResize() {
    document.documentElement.classList.add("rice-resizing");

    clearTimeout(resizeTimer);

    resizeTimer = setTimeout(() => {
        document.documentElement.classList.remove("rice-resizing");
    }, 120);
}
```

Theme CSS disables expensive effects during live resize:

```css
html.rice-resizing *,
html.rice-resizing *::before,
html.rice-resizing *::after {
    animation: none !important;
    transition: none !important;
    text-shadow: none !important;
    box-shadow: none !important;
    filter: none !important;
    backdrop-filter: none !important;
}
```

The effect was visibly confirmed:

```text
actively resize
    → glows/effects off

pause/stop
    → glows/effects return
```

> **LANDMARK PERFORMANCE FIX — Fix Discord renderer cost inside Discord instead of adding more compositor hacks.**

---

# 26. Custom Vencord build architecture

Custom Vencord source lives at:

```text
~/.config/vencord/
```

Build command:

```bash
cd ~/.config/vencord
pnpm build --disable-updater
```

A key diagnostic was verifying that the plugin actually appears in the Vesktop-target renderer artifact:

```bash
rg -l "RiceResizePerf" dist/renderer.js
rg -l "RiceResizePerf" dist/vencordDesktopRenderer.js
```

Both eventually contained the plugin.

This mattered because a successful build does not automatically mean Vesktop is loading that build.

---

# 27. Landmark deployment fix — separate Vencord source/build from runtime

At one point DevTools still returned:

```js
Vencord.Plugins.plugins.RiceResizePerf
```

as:

```text
undefined
```

even though the source existed.

The real issue became:
```text
custom source/build tree
!=
files Vesktop currently loads
```

The clean architecture became:

```text
~/.config/vencord/
    source + build workspace

~/.config/Vesktop/custom-vencord/
    exact runtime files Vesktop should load
```

Vesktop state points to:

```json
"vencordDir": "/var/home/mapple/.config/Vesktop/custom-vencord"
```

After a build, copy:

```bash
cp dist/vencordDesktopMain.js \
   dist/vencordDesktopPreload.js \
   dist/vencordDesktopRenderer.js \
   dist/vencordDesktopRenderer.css \
   ~/.config/Vesktop/custom-vencord/
```

> **LANDMARK DEPLOYMENT FIX — Development output and runtime authority are separate concepts.**

---

# 28. Vesktop configuration layout

Vesktop configuration was moved to a normal user-facing location:

```text
~/.config/Vesktop/
```

with the Flatpak config path linked to it.

The useful conceptual split is now:

```text
Vesktop application/config state
    ~/.config/Vesktop/

Vencord source
    ~/.config/vencord/

custom Vencord runtime
    ~/.config/Vesktop/custom-vencord/
```

---

# 29. Escape revealed another ownership boundary

When Vesktop owns keyboard focus, Quickshell does not receive its keys.

Therefore this kind of QML handler:

```qml
Keys.onPressed: function(event) {
    if (event.key === Qt.Key_Escape) {
        ...
    }
}
```

cannot close the composite while Discord itself has focus.

This is not a broken QML handler. It is a focus/ownership fact:

```text
Quickshell focus → Quickshell gets keys
Vesktop focus    → Vesktop gets keys
```

---

# 30. Landmark close semantics — hide Discord, do not kill it

The requested Escape behavior was explicitly:

```text
Escape
    ↓
social menu disappears
Vesktop disappears
Discord process stays alive
```

not:

```text
Escape
    ↓
kill Vesktop
```

Vesktop is hidden with Sway scratchpad:

```bash
swaymsg '[app_id="vesktop"] move scratchpad'
```

This preserves session state and gives fast reopen behavior.

> **LANDMARK DECISION — Closing the social UI means hiding the composite, not terminating Discord.**

---

# 31. Quickshell IPC becomes the semantic close endpoint

`MessagingW.qml` gained:

```qml
IpcHandler {
    target: "messaging"

    function closeMenu(): void {
        messagingWindow.menuOpen = false;
    }
}
```

Host test:

```bash
qs ipc call messaging closeMenu
```

This proved that the Quickshell lifecycle could be triggered externally.

The important architectural idea is:

> **There should be one semantic close action, not duplicated close logic in every layer.**

---

# 32. Vencord → host → Quickshell Escape bridge

The working sandbox bridge became:

```bash
flatpak-spawn --host qs ipc call messaging closeMenu
```

Vesktop needed permission to talk to the Flatpak service:

```bash
flatpak override --user \
  --talk-name=org.freedesktop.Flatpak \
  dev.vencord.Vesktop
```

The Vencord plugin was extended with a native Node helper.

Current conceptual flow:

```text
Escape inside Discord
        ↓
Vencord renderer catches keydown
        ↓
plugin native.ts
        ↓
flatpak-spawn --host
        ↓
qs ipc call messaging closeMenu
        ↓
MessagingW closes
        ↓
Vesktop → scratchpad
        ↓
Discord process remains alive
```

> **LANDMARK ARCHITECTURE — Quickshell owns close semantics; Vencord only forwards Escape into that semantic action.**

---

# 33. `discordHideProcess` versus `discordLeaveProcess`

Two operations can currently execute similar scratchpad commands while representing different events:

```text
discordHideProcess
    = switch away from Discord inside an otherwise open social UI

discordLeaveProcess
    = leave/close the entire social UI
```

Keeping them semantically separate is valuable even if their current shell commands look similar.

> Same immediate command does not mean same architectural event.

---

# 34. Explicit default geometry

Reopen behavior occasionally produced an unwanted half-size menu.

The intended clean opening size was separated from mutable live state:

```qml
property int defaultPanelWidth: 1210
property int defaultPanelHeight: 1355

property int sharedPanelWidth: defaultPanelWidth
property int sharedPanelHeight: defaultPanelHeight
```

Default X derives from the workspace and **default** width:

```qml
readonly property int defaultPanelX:
    swayAreaX
    + swayAreaWidth
    - margins.right
    - defaultPanelWidth
```

This creates an important distinction:

```text
defaultPanel*
    desired clean opening geometry

sharedPanel*
    live mutable geometry
```

---

# 35. `width` / `height` versus only implicit size

The visible `FloatingWindow` also moved toward binding actual size:

```qml
width: messagingWindow.sharedPanelWidth
height: messagingWindow.sharedPanelHeight
```

rather than relying only on:

```qml
implicitWidth
implicitHeight
```

The goal was to make current shared geometry explicit at the window level while still allowing legitimate Sway resizes to update shared state through the adoption path.

---

# 36. The half-size reopening race

Even with correct numbers, repeated open/close stress testing could occasionally produce a half-size window.

The key diagnosis was:

```text
default size is correct
```

but temporary compositor geometry could be observed at the wrong moment.

Failure pattern:

```text
menu opens
    ↓
FloatingWindow maps
    ↓
Sway briefly reports transitional geometry
    ↓
geometry watcher sees it
    ↓
adoptSocialGeometry() treats it as user intent
    ↓
temporary half-size becomes canonical shared size
```

Changing one-shot timer values such as 160 ms, 40 ms, or 20 ms could change how often the race was won, but did not eliminate the underlying authority problem.

The better rule became:

> **LANDMARK TIMING FIX — During controlled opening/restoration, transitional compositor geometry is not allowed to become authoritative shared geometry.**

Conceptually:

```text
geometry watch OFF
    ↓
restore intended default width/height/X/Y
    ↓
protect geometry for the map/open interval
    ↓
map/sync
    ↓
geometry watch ON
    ↓
normal user-resize adoption resumes
```

`ignoreSocialGeometryUntil` is part of this protection.

The user later reported that the system was winning the race consistently enough for normal use and chose not to destabilize working code merely to eliminate a theoretical edge case.

That decision is worth preserving:

> **Engineering stability beats chasing a race that only appears under artificial stress testing.**

---

# 37. Current known geometry values

Known important values at this documentation point:

```text
default shared width:         1210
default shared height:        1355

AppSelector width:             110
ContactList width:             200
Discord gap:                     0
Discord inset:                   1

minimum shared width:
    appSelectorWidth + contactListWidth + 1

minimum shared height:         260

Discord startup max width:     760
Discord startup max height:    760

geometry tolerance:              0
geometry helper interval:        8 ms
```

Opening timer constants changed repeatedly during race testing and should be verified in the live tree rather than treated as architectural constants.

---

# 38. Current `MessagingW.qml` responsibilities

`MessagingW.qml` is now the semantic controller for the whole social unit.

It owns:

```text
menuOpen
focusZone
activeAppIndex
discordSelected

default geometry
shared geometry
startup state
socialReady
discordReady
discordConfigured

geometry-watch policy
startup classification
show/hide semantics
app activation
Quickshell IPC close endpoint
```

It is the correct place for questions like:

```text
"what does this menu mean?"
"which app is selected?"
"what should opening/closing do?"
```

It is not the ideal place for every per-frame compositor follower command.

---

# 39. Current `DiscordGeometry.py` responsibilities

The Python helper exists because compositor choreography has different performance needs from QML UI state.

It handles:

```text
persistent Sway IPC
high-frequency geometry sampling
finding social and Vesktop nodes
leader/follower fast path
direct Sway move/resize
focus operations
startup centering
canonical geometry snapshots back to QML
```

It should not become the semantic owner of app selection or social UI meaning.

This division is intentional:

```text
QML = semantic authority
Python = compositor hot path
```

---

# 40. Current Vencord plugin responsibilities

`RiceResizePerf` now has two jobs.

## Resize performance

```text
resize events
    ↓
add rice-resizing class
    ↓
disable expensive effects
    ↓
debounce
    ↓
restore full theme
```

## Escape forwarding

```text
Escape while Vesktop focused
    ↓
native helper
    ↓
flatpak-spawn --host
    ↓
qs ipc call messaging closeMenu
```

These jobs belong inside Vesktop because they depend on Vesktop renderer/runtime context.

The plugin is a bridge, not the canonical owner of social-menu state.

---

# 41. Current architecture diagram

```text
                            POST-APOLLO SOCIAL UNIT
┌───────────────────────────────────────────────────────────────────────────┐
│                                                                           │
│ shell.qml                                                                 │
│    │                                                                      │
│    ▼                                                                      │
│ MessagingW.qml                                                            │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ permanent controller PanelWindow                                    │ │
│ │ - Overlay layer                                                     │ │
│ │ - click-through                                                     │ │
│ │ - semantic state                                                    │ │
│ │ - shared geometry                                                   │ │
│ │ - IPC close endpoint                                                │ │
│ │                                                                      │ │
│ │ socialWindow : FloatingWindow                                       │ │
│ │ ┌────────────┬────────────────────┬────────────────────────────────┐ │ │
│ │ │AppSelector │ ContactList shell  │ ChatFeed shell                 │ │ │
│ │ │            │                    │                                │ │ │
│ │ │            │ Discord mode: inner content hidden                 │ │ │
│ │ │            │ shell/backing remains                              │ │ │
│ │ └────────────┴────────────────────┴────────────────────────────────┘ │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
│             │                                                             │
│             │ JSON stdin/stdout                                            │
│             ▼                                                             │
│ DiscordGeometry.py                                                        │
│             │ persistent Sway IPC                                          │
│             ▼                                                             │
│ Sway compositor                                                           │
│      ├── title="QS_SOCIAL_MENU"                                           │
│      └── app_id="vesktop"                                                 │
│                         │                                                  │
│                         ▼                                                  │
│                  Vesktop / Vencord                                         │
│                  ┌───────────────────────┐                                 │
│                  │ RiceResizePerf        │                                 │
│                  │ - resize CSS state    │                                 │
│                  │ - Escape bridge       │                                 │
│                  └───────────┬───────────┘                                 │
│                              │ flatpak-spawn --host                        │
│                              ▼                                             │
│                    qs ipc call messaging closeMenu                         │
│                              │                                             │
│                              └──────────────► MessagingW                   │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

---

# 42. Current open flow

Normal social-menu opening is conceptually:

```text
bar button toggles menuOpen
        ↓
MessagingW begins open lifecycle
        ↓
Discord hidden to scratchpad unless selected
        ↓
default width/height restored
        ↓
default X/Y derived from Sway workspace
        ↓
socialWindow becomes visible
        ↓
controlled geometry sync
        ↓
normal geometry authority enabled after opening protection
```

When Discord is selected:

```text
activeAppIndex = Discord
        ↓
showDiscord()
        ↓
ensure Vesktop exists
        ↓
move scratchpad / scratchpad show
        ↓
startup-sized?
   yes → center guest, do not adopt
   no  → snap real Discord into slot
        ↓
normal leader/follower tracking
```

---

# 43. Current close flow

```text
menuOpen = false
        ↓
geometry watch off
        ↓
relevant timers/helpers stop
        ↓
Vesktop moves to scratchpad
        ↓
socialWindow hides
        ↓
app/focus state returns to baseline
```

Discord remains running.

---

# 44. Current move/resize flow — social leads

```text
user Mod-moves/resizes QS_SOCIAL_MENU
        ↓
DiscordGeometry.py sees focused social window
        ↓
Python derives Discord follower rectangle
        ↓
Python immediately moves/resizes Vesktop
        ↓
QML receives canonical shared geometry
        ↓
MessagingW updates sharedPanel*
        ↓
after drag settles, Discord may be raised
```

The hot path avoids a redundant QML round trip.

---

# 45. Current move/resize flow — Discord leads

```text
user moves/resizes Vesktop
        ↓
DiscordGeometry.py sees focused Discord window
        ↓
Python reconstructs full shared rectangle
        ↓
Python immediately moves/resizes socialWindow
        ↓
QML receives canonical shared state
        ↓
MessagingW updates sharedPanel*
```

The reconstruction preserves AppSelector width, gap, and inset.

---

# 46. Core architectural invariants

## 46.1 Do not mentally turn Vesktop into a QML child

It is a separate Wayland surface. Ignoring that eventually fails at geometry, focus, stacking, or lifecycle.

## 46.2 Keep `shell.qml` out of local geometry experiments

The successful refactor preserved the shell contract and moved complexity into `MessagingW` and `DiscordGeometry.py`.

## 46.3 `DiscordBackingW.qml` is not part of the current model

The shared `FloatingWindow` is the underlay/shell.

## 46.4 Startup Vesktop is not geometry authority

Temporary splash geometry is not user intent.

## 46.5 The focused active window is leader during ambiguous geometry changes

Do not let both windows repeatedly correct each other.

## 46.6 QML owns semantics; Python owns the live compositor hot path

Do not blur this without a deliberate reason.

## 46.7 Vencord performance problems belong in Vencord

Do not keep adding compositor fixes for expensive CSS and Electron reflow.

## 46.8 Escape closes the logical social unit, not the Discord process

Scratchpad hiding is the current lifecycle contract.

## 46.9 Built Vencord and loaded Vencord are separate facts

Always distinguish source/build output from runtime files.

## 46.10 Transitional map geometry is not user-resize intent

Do not adopt opening geometry simply because Sway reports it first.

---

# 47. Landmark decisions at a glance

| Stage | Problem | Landmark decision / fix | Why it mattered |
|---|---|---|---|
| Messaging baseline | Repeated PanelWindow toggle crash | Keep root native controller alive; hide content/input | Removed create/reparent churn |
| Messaging baseline | Power overlapped menu | `WlrLayer.Overlay` | Fixed actual Wayland stacking layer |
| Discord selection | How to integrate Discord | Real Vesktop/Vencord | Preserved real client + deep customization |
| Early geometry | External window not owned by QML | Sway controls Vesktop geometry | Respected Wayland boundary |
| Geometry source | `mapToGlobal` / magic offsets unreliable | Sway workspace geometry | Removed fragile coordinate guesses |
| Lifecycle | Hidden scratchpad timing inconsistent | Show/map first, then snap | Made surface lifecycle explicit |
| Shared behavior | Social and Discord moved separately | One canonical shared rectangle | Created one logical unit |
| Window type | Layer-shell body lacked normal floating behavior | Controller PanelWindow + visible FloatingWindow | Enabled normal Sway `$mod` controls |
| Visual integration | Discord needed to feel embedded | Keep ContactList/ChatFeed shell underneath | Preserved physical receiver look |
| Cold start | Splash could shrink whole unit | Startup surface is centered guest | Protected canonical geometry |
| Tracking | Both windows fought | Leader/follower model | Removed ping-pong |
| Tracking performance | shell polling too slow | Persistent `DiscordGeometry.py` | Removed process-spawn overhead |
| Live resize | QML round trip still visible | Python direct fast follower | Made movement feel native |
| Discord repaint lag | Geometry fixed but content lagged | `RiceResizePerf` | Fixed renderer cost at renderer layer |
| Vencord deployment | Plugin built but runtime missed it | Separate build and `custom-vencord` runtime | Made runtime authority explicit |
| Escape | QML cannot see Vesktop keys | Vencord native bridge → `qs ipc` | Unified close behavior |
| Close semantics | Do not kill Discord | Scratchpad hide | Fast reopen, process survives |
| Reopen sizing | Occasional half-size | Explicit defaults + opening protection | Blocked transitional geometry adoption |
| Next direction | Popup feels abrupt | Controlled edge-slide animation | Turns timing into deliberate choreography |

---

# 48. Historical approaches not to casually restore

- Root `visible: menuOpen` on the old controller `PanelWindow`
- `mapToGlobal()` as Sway coordinate truth
- arbitrary Discord Y/top offsets
- repeated bash + swaymsg + jq polling
- adopting both sides without deciding a leader
- treating startup Vesktop as real shared geometry
- killing Vesktop when the social menu closes
- assuming a successful Vencord build is the runtime Vesktop loads
- reintroducing `DiscordBackingW` as a competing geometry owner

---

# 49. Current file map

## Quickshell

```text
~/.config/quickshell/
└── widgets/
    └── messanger/
        ├── MessagingW.qml
        ├── DiscordGeometry.py
        ├── AppSelector.qml
        ├── ContactList.qml
        └── ChatFeed.qml
```

The directory is currently spelled `messanger`, not `messenger`.

## Vencord source

```text
~/.config/vencord/
└── src/
    └── userplugins/
        └── riceResizePerf/
            ├── index.ts
            └── native.ts
```

## Vesktop runtime/config

```text
~/.config/Vesktop/
├── custom-vencord/
├── sessionData/
├── settings/
├── settings.json
├── state.json
└── themes/
```

---

# 50. Custom Vencord operational notes

After editing the plugin:

```bash
cd ~/.config/vencord
pnpm build --disable-updater
```

Copy the Vesktop-target runtime files:

```bash
cp dist/vencordDesktopMain.js \
   dist/vencordDesktopPreload.js \
   dist/vencordDesktopRenderer.js \
   dist/vencordDesktopRenderer.css \
   ~/.config/Vesktop/custom-vencord/
```

Useful DevTools check:

```js
Vencord.Plugins.plugins.RiceResizePerf
```

Expected: a plugin object, not `undefined`.

---

# 51. Current IPC checks

Inspect Quickshell IPC:

```bash
qs ipc show
```

Expected social endpoint:

```text
target messaging
  function closeMenu(): void
```

Direct host test:

```bash
qs ipc call messaging closeMenu
```

Flatpak-to-host route:

```bash
flatpak-spawn --host qs ipc call messaging closeMenu
```

The latter depends on Vesktop's permission to talk to `org.freedesktop.Flatpak`.

---

# 52. Why this is a good fit for Post-Apollo despite not being true embedding

The current model keeps useful boundaries:

- Vesktop remains replaceable;
- Discord updates do not require rebuilding the entire social UI;
- Vencord remains available;
- Sway retains mature move/resize behavior;
- Quickshell remains the shell authority;
- visuals can evolve independently;
- each layer can be debugged independently.

The cost is choreography complexity, but that cost is now structured rather than hidden.

---

# 53. Future plan — controlled slide-in opening animation

The next planned architectural change is to replace the abrupt popup with a deliberate edge-slide.

First-pass flow:

```text
menu requested open
        ↓
map socialWindow
        ↓
temporarily disable geometry adoption
        ↓
place full-size social window almost offscreen to the right
        ↓
animate X toward target
        ↓
snap exactly to final X/Y
        ↓
reenable normal geometry tracking
```

Proposed QML animation state:

```text
socialSlidePending
socialSlideActive
socialSlideDuration
socialSlidePeek
socialSlideStartX
socialSlideTargetX
socialSlideTargetY
socialSlideStartedAt
```

The critical rule is:

> **Animate temporary compositor position, not canonical shared geometry.**

Conceptually:

```text
sharedPanelX/Y
    = real destination / remembered geometry

animated temporary X
    = presentation only
```

This should also make the old opening race less important because opening becomes an explicitly controlled state rather than a scramble to make the first mapped rectangle immediately become the final one.

---

# 54. Future plan — nearest-edge animation

The first version should slide from the right because the social unit currently lives near the right edge.

A generalized version can calculate:

```text
distance to left
distance to right
distance to top
distance to bottom
        ↓
choose smallest
        ↓
animate from nearest edge
```

Then the animation remains correct even if the default social position changes later.

---

# 55. Future plan — closing animation

Once open animation is stable, close can become the inverse:

```text
normal active geometry
        ↓
geometry adoption off
        ↓
slide to chosen edge
        ↓
hide socialWindow
        ↓
move Vesktop to scratchpad
        ↓
stop animation timer
```

The timer should only run during the brief transition, so the closed state remains essentially idle.

---

# 56. Future plan — possibly move animation execution into Python later

The first pass should remain in `MessagingW.qml` because visual iteration is easier there.

If per-frame Sway animation proves timing-sensitive, a later split could mirror the successful resize fast path:

```text
QML
    owns animation intent
    start / target / duration / easing

Python
    executes high-frequency Sway movement
```

This should be an optimization only if needed, not the starting point.

---

# 57. Future plan — generalized Post-Apollo window choreography

The social menu is becoming a prototype for a broader Post-Apollo window language.

Potential reusable concepts:

```text
controlled mapping state
edge-aware slide-in/out
temporary geometry-authority lock
shared geometry across multiple native surfaces
focus restoration after animation
leader/follower compositor relationships
```

If several modules adopt this behavior, a reusable choreography helper may eventually be cleaner than duplicating timers and geometry state.

---

# 58. Future plan — automate custom Vencord deployment

The current plugin workflow is manual:

```text
edit source
    ↓
pnpm build --disable-updater
    ↓
copy four vencordDesktop* files
    ↓
restart Vesktop
```

A helper script or `just` task could reduce this to one command while preserving the important source/build/runtime separation.

---

# 59. Future plan — make resize-performance mode more selective

The current CSS intentionally disables many expensive effects for reliability.

Later tuning can selectively target the most expensive operations:

```text
backdrop-filter
filter
large box-shadow
large text-shadow
selected animations/transitions
```

while retaining cheaper visual identity during live resize.

This is a Vencord/theme optimization, not a geometry fix.

---

# 60. Future plan — reuse the external-app shell pattern

The Discord work demonstrates a broader Post-Apollo pattern:

```text
Quickshell shell
    +
external app window
    +
compositor geometry bridge
    +
optional app-side plugin/IPC bridge
```

This can be useful whenever an external native application is more capable than rebuilding that application inside QML.
The reusable lesson is:

> **Make ownership boundaries explicit, then synchronize across them intentionally.**

---

# 61. Architectural lessons learned

## 61.1 Timing bugs often reveal authority bugs

Many early fixes looked like:

```text
wait 160 ms
wait 180 ms
try again
```

The stronger question became:

```text
Who is allowed to define geometry at this moment?
```

Examples:

- startup splash: not authority;
- actively manipulated window: authority;
- follower: not authority;
- transitional map geometry: not authority.

That is more robust than simply increasing delays.

## 61.2 One logical object can span multiple processes and surfaces

The social receiver feels like one thing even though it spans:

```text
Quickshell
Python
Sway
Flatpak
Vesktop
Vencord
```

It works because each layer owns a narrow responsibility.

## 61.3 Performance requires layer-specific fixes

Three separate lag classes had separate fixes:

```text
process-spawn geometry lag
    → persistent Python Sway IPC

QML/Python round-trip drag lag
    → Python fast follower

Discord content repaint lag
    → Vencord resize-performance mode
```

Trying to fix all three with one mechanism would have made the architecture worse.

## 61.4 Stable semantics matter even when commands match

`discordHideProcess` and `discordLeaveProcess` may issue similar scratchpad commands today, but they represent different semantic events and should remain distinguishable.

## 61.5 Hidden is not the same as destroyed

The project repeatedly benefits from keeping stateful objects alive and hiding them:

- controller PanelWindow stays alive;
- Vesktop stays running;
- Python helper stays running;
- animation timers stop rather than forcing architecture teardown.

This is a recurring Post-Apollo design pattern.

---

# 62. Architecture generations

```text
GEN 0
Reusable Quickshell messaging UI
Session is first backend

        ↓

GEN 1
Real Vesktop shown with Quickshell
scratchpad + delayed snap

        ↓

GEN 2
Sway workspace geometry
Discord slot
startup guest handling

        ↓

GEN 3
Controller PanelWindow + visible FloatingWindow
one shared geometry
normal Sway Mod move/resize

        ↓

GEN 4
Bidirectional leader/follower tracking
persistent DiscordGeometry.py

        ↓

GEN 5
Python fast path
movement/resizing feels native

        ↓

GEN 6
Vencord resize-performance mode
renderer cost reduced during resize

        ↓

GEN 7
Quickshell IPC + Vencord native Escape bridge
composite closes as one object without killing Discord

        ↓

GEN 8
Explicit default opening geometry
map/race protection

        ↓

NEXT
controlled edge-slide animation
```

The current result is increasingly a **compositor-aware multi-surface application shell**, not a collection of unrelated hacks.

---

# 63. Recovery checklist

If the Discord social unit breaks after a future edit, check these in order:

1. Does `MessagingW.qml` still create `socialWindow` as a `FloatingWindow`?
2. Is the root controller `PanelWindow` still only the permanent shell/controller rather than the movable visual body?
3. Does Sway contain `title="QS_SOCIAL_MENU"`?
4. Does Sway contain `app_id="vesktop"`?
5. Is `DiscordGeometry.py` running?
6. Is geometry watch enabled only when it should be?
7. Is a startup-sized Vesktop being incorrectly adopted?
8. Is the focused window being treated as leader?
9. Is Vencord actually loading `~/.config/Vesktop/custom-vencord`?
10. Does DevTools return a `RiceResizePerf` plugin object?
11. Does `qs ipc show` expose `messaging.closeMenu()`?
12. Can `qs ipc call messaging closeMenu` close the shell?
13. Can Vesktop run `flatpak-spawn --host qs ipc call messaging closeMenu`?
14. Are default dimensions separate from mutable shared dimensions?
15. During opening, can transitional geometry still reach `adoptSocialGeometry()`?

Do not immediately change several timers at once. First identify which ownership layer failed.

---

# 64. Final project principle

The most important idea behind the current Discord integration is:

> **Post-Apollo does not need to literally own every application surface in order to make the desktop behave like one designed machine.**

Quickshell, Sway, Vesktop, Python, and Vencord remain distinct layers.

The architecture succeeds by giving each one a narrow authority and explicit bridges to the others.

That is why the current result can:

- look like one social receiver;
- move like one window;
- resize like one window;
- use a real Discord client;
- preserve Post-Apollo visuals;
- hide without killing Discord;
- catch Escape from either side;
- reduce Discord rendering cost while resizing;
- and evolve toward animated, physical-feeling window behavior.

---

# 65. One-page handoff

```text
WHAT IT IS
---------
A Quickshell social receiver visually containing real Vesktop Discord.

NOT TRUE EMBEDDING
------------------
Vesktop remains a separate Sway/Wayland window.

SEMANTIC OWNER
--------------
MessagingW.qml

VISIBLE QUICKSHELL WINDOW
-------------------------
FloatingWindow title="QS_SOCIAL_MENU"

COMPOSITOR HOT PATH
-------------------
DiscordGeometry.py
persistent direct Sway IPC
~8 ms sampling
direct leader/follower movement

CANONICAL GEOMETRY
------------------
sharedPanelX/Y/Width/Height

KNOWN DEFAULT SIZE
------------------
1210 × 1355

DISCORD SLOT
------------
full shared rectangle
minus 110 px AppSelector
minus 1 px inset perimeter

STARTUP RULE
------------
small Vesktop startup window is a guest
never geometry authority

CLOSE RULE
----------
hide to scratchpad
do not kill Vesktop

ESCAPE
------
Vencord keydown
→ native.ts
→ flatpak-spawn --host
→ qs ipc call messaging closeMenu

RESIZE PERFORMANCE
------------------
RiceResizePerf adds rice-resizing class
theme disables expensive effects temporarily

VENCORD SOURCE
--------------
~/.config/vencord/

VENCORD RUNTIME
---------------
~/.config/Vesktop/custom-vencord/

BIGGEST REGRESSION RISKS
------------------------
- treating QML coordinates as Sway truth
- adopting splash/transitional geometry
- removing leader/follower distinction
- returning to shell-process polling
- reintroducing DiscordBackingW as competing owner
- killing Vesktop on social-menu close
- assuming built Vencord == loaded Vencord

NEXT MAJOR PLAN
---------------
controlled slide from nearest screen edge
with geometry adoption disabled during animation
```