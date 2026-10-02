✦︎✦︎✦︎ Meta Apollo Logos //

# ✮˙๋࣭⭑ MODEL // REPOSITORY DESIGN LANGUAGE

![](../BUILD/assets/design/chassis/focus-rail.svg)


> **STATE //** active \~\~ **HEALTH //** ࣪˖ദ്ദി๋࣭⭑ VERIFIED \~\~ **VIEW //** repository design grammar


> This design language derives from the canonical **[META APOLLO LOGOS // PRINCIPLES](./Meta-Apollo-Logos-Principles.md)**. It does not define a second principles system.

> **Readable operator manuals for living systems.**

Meta Apollo repositories should be usable, legible, and aesthetically coherent while they are still being built.

Polish is not a final pass.

It is part of the architecture.

---

# 1. The Seven Canonical Rooms


Every Meta Apollo repository uses the same seven top-level rooms:

| Room | Reader question | Typical contents |
| --- | --- | --- |
| **ATLAS** | What is this whole repository? | Purpose, status, roadmap, repo-wide navigation, major pieces |
| **MODEL** | How does it work? | Architecture, concepts, contracts, diagrams, specifications, design decisions |
| **BUILD** | What becomes the thing? | Source code, modules, assets, shipped config, vendored code, packaging |
| **DEV** | How do I work on the thing? | Tests, scripts, developer tools, fixtures, mocks, debug and release tooling |
| **OPERATE** | How do I use or run it? | Installation, examples, workflows, configuration, runbooks, troubleshooting |
| **EVIDENCE** | What shows that it works or supports the claim? | Test results, benchmark results, reports, experiments, screenshots, demonstrations |
| **ARCHIVE** | How did we get here? | Legacy work, superseded designs, history, provenance |

Canonical order:

```
ATLAS
MODEL
BUILD
DEV
OPERATE
EVIDENCE
ARCHIVE
```

All seven rooms exist in every Meta Apollo repository, even when one is mostly empty.

Consistency is intentional.

---

# 2. Every Room Gets a Map


GitHub automatically renders a folder's `README.md` when the folder is opened.

Meta Apollo uses that behavior deliberately.

Every canonical room contains:

```
README.md
```

and the visible heading inside follows:

```
# MAP // ATLAS


# MAP // MODEL


# MAP // BUILD


# MAP // DEV


# MAP // OPERATE


# MAP // EVIDENCE


# MAP // ARCHIVE


```

**ATLAS** is the map of the whole territory.

A room's **README** is the map taped to the wall when you enter that room.

The filename remains `README.md` because GitHub gives it useful native behavior.

---

# 3. Shared Room-Map Chassis


Every room map uses the same basic shape:

```
# MAP // <ROOM>


WHAT THIS ROOM IS

WHAT BELONGS HERE

CURRENT CONTENTS

WHERE TO GO NEXT
```

The wording can adapt to the room, but the navigation grammar stays recognizable.

---

# 4. Standard Repository Skeleton


```text
repo/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
├── .gitignore
├── .github/
│
├── ATLAS/
│   └── README.md
│
├── MODEL/
│   └── README.md
│
├── BUILD/
│   ├── README.md
│   ├── src/
│   ├── assets/
│   ├── config/
│   ├── vendor/
│   └── packaging/
│
├── DEV/
│   ├── README.md
│   ├── tests/
│   ├── scripts/
│   ├── tools/
│   └── debug/
│
├── OPERATE/
│   ├── README.md
│   ├── install/
│   ├── examples/
│   └── troubleshooting/
│
├── EVIDENCE/
│   ├── README.md
│   ├── test-results/
│   ├── benchmark-results/
│   ├── reports/
│   ├── experiments/
│   └── screenshots/
│
└── ARCHIVE/
    ├── README.md
    ├── legacy/
    ├── superseded/
    └── history/
```

The standard subfolders are starting points, not requirements for every project.

The seven canonical rooms are the fixed part.

---

# 5. Root Exceptions


Do not fight GitHub or build tooling merely to make the filesystem visually pure.

Files that GitHub or common tooling expects at the repository root should remain there when appropriate.

Common examples:

- `README.md`
- `LICENSE`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `CHANGELOG.md`
- `.gitignore`
- `.github/`
- language/package manifests that tooling expects at root

Use GitHub's conventions for behavior.

Use Meta Apollo's conventions for meaning and presentation.

---

# 6. BUILD


> **BUILD = the thing.**

BUILD contains what becomes the product or directly defines the product.

Typical contents:

- `src/`
- modules
- components
- services
- models
- `assets/`
- shipped/default `config/`
- `vendor/`
- packaging
- build/distribution definitions

A common source shape is:

```text
BUILD/
└── src/
    ├── modules/
    ├── components/
    ├── services/
    ├── models/
    └── ...
```

Do not move something into DEV merely because a developer touches it.

If it ships as part of the product or directly defines the product, it belongs in BUILD.

---

# 7. DEV


> **DEV = the workshop.**

DEV contains the machinery contributors use to create, inspect, verify, debug, generate, and release the product.

Typical contents:

- `tests/`
- `scripts/`
- `tools/`
- fixtures
- mocks
- test helpers
- debug/probe utilities
- release tooling

The test code lives here because it is developer machinery.

The results produced by those tests do not.

---

# 8. OPERATE


> **OPERATE = use the thing.**

Typical contents:

- installation
- quick start
- examples
- user-facing configuration
- common workflows
- runbooks
- diagnostics
- troubleshooting
- recovery

Examples normally belong here because they usually answer:

> **How do I use this?**

---

# 9. EVIDENCE


> **EVIDENCE = show what happened.**

Typical contents:

- test results
- benchmark results
- coverage reports
- experiment records
- screenshots
- demonstrations
- comparison reports
- supporting references

The distinction is:

> **DEV/tests = the machinery used to test.**  
> **EVIDENCE = what the testing showed.**

Evidence should support claims without taking over the main interface.

---

# 10. MODEL


MODEL explains the structure underneath the product.

Typical contents:

- architecture
- concepts
- data flow
- ownership
- contracts/interfaces
- specifications
- design decisions
- diagrams

MODEL answers:

> **How does this thing work, and why is it shaped this way?**

---

# 11. ATLAS


ATLAS orients the reader to the repository as a whole.

Typical contents:

- purpose
- current status
- roadmap
- major subsystems
- repository-wide navigation
- project relationships
- fast paths for different readers

ATLAS is not a generic dumping ground for documentation.

It is the map of the territory.

---

# 12. ARCHIVE


ARCHIVE preserves material that is intentionally historical.

Typical contents:

- legacy implementations
- superseded designs
- old architecture
- historical notes
- migration records
- provenance

Git already preserves revision history.

ARCHIVE is for material a human should still be able to deliberately browse.

A clean interface does not require historical amnesia.

---

# 13. Documentation Is Distributed by Purpose


Meta Apollo does not use one giant generic `docs/` bucket by default.

Documentation goes where its job belongs:

```text
ATLAS      → roadmap, orientation, status
MODEL      → architecture, concepts, specifications
OPERATE    → installation, examples, troubleshooting
EVIDENCE   → reports, results, experiment records
ARCHIVE    → historical and superseded documentation
```

The filesystem itself should help explain what a document is doing.

---

# 14. Visual Identity


Primary palette inherited from Post-Apollo:

| Role | Color |
| --- | --- |
| Background | `#1B0623` |
| Cyan | `#55CFCA` |
| Orange | `#F2BE4E` |
| Red | `#D16041` |
| Blue | `#5B5FD4` |
| Magenta | `#C74EC7` |
| Offwhite | `#DCF3FA` |

Mood:

- operator console
- serious but alive
- technical / philosophical
- retro-futurist
- tactile
- modular
- human
- not sterile
- not generic SaaS

Long-form text remains readable first.

---

# 15. Symbol Language


The symbol system is semantic first and decorative second.

The **meaning** of a symbol is canonical. Its surrounding ornament may be tightened later as long as the symbol remains recognizable and keeps the same role.

## Rooms


| Symbol | Room |
| --- | --- |
| 🧭 | **ATLAS** |
| ✮˙๋࣭⭑ | **MODEL** |
| 🖨 | **BUILD** |
| ⚒ | **DEV** |
| 🖳 | **OPERATE** |
| ⊹ ࣪ℼ˖ | **EVIDENCE** |
| ࣪⋅˚🕮‧₊˚ | **ARCHIVE** |

## Content / State


| Symbol | Meaning |
| --- | --- |
| ★⋆˙ | **CORE / IMPORTANT** |
| ✮˙๋࣭⭑ | **MODEL / STRUCTURE** |
| ⌯✦ | **PROCESS / FLOW** |
| ˖ ࣪♻๋࣭⭑ | **RELATIONSHIP / TRANSFORMATION** |
| ˖⚠ ๋࣭⭑ | **WARNING** |
| ࣪˖ദ്ദി๋࣭⭑ | **VERIFIED** |
| ⊹⚡ ๋࣭⭑ | **PROVISIONAL** |
| ⁴⁰⁴ | **DEPRECATED** |
| ↺ | **REVERSION / REVISION** |

## Rule


> **Same symbol = same meaning everywhere.**

Do not reuse a canonical symbol for an unrelated state merely because it looks good.

Ornament may evolve.

Meaning should remain stable.

---

# 16. Current-State Notation


Meta Apollo uses **c** to mark the current working state of a project.

Examples:

```text
c0.1
c0.7
c1
c2.3
```

The number is project-specific.

**c** does not mean "final release."

It means:

> **This is the current working state of the thing.**

Use it when a project benefits from a compact visible state marker without implying that the work is finished or formally released.

A header may combine it with a plain-language state:

```text
ACTIVE · c0.7
EXPERIMENTAL · c1
STABLE · c2.3
```

Do not invent a state number merely to fill the field.

---

# 17. Content-Block Grammar


Meta Apollo documents use the canonical pattern:

```text
SYMBOL + TYPE // SUBJECT
```

The symbol identifies the semantic role.

The type names the kind of block.

The subject tells the reader what this specific block is about.

Examples:

```md
## ✮˙๋࣭⭑ MODEL // SYSTEM ARCHITECTURE


## ⌯✦ PROCESS // STARTUP FLOW


## ⊹ ࣪ℼ˖ EVIDENCE // TEST RESULTS


## ˖⚠ ๋࣭⭑ WARNING // DESTRUCTIVE ACTION


```

Use the same grammar for smaller in-section blocks when appropriate.

## Canonical block types


### ★⋆˙ CORE


Use for a load-bearing claim or rule that the surrounding section depends on.

### ✮˙๋࣭⭑ MODEL


Use for structural explanations, architecture, or conceptual machinery.

### ⌯✦ PROCESS


Use for sequences, flows, lifecycles, or ordered transformations.

### ˖ ࣪♻๋࣭⭑ RELATIONSHIP


Use when the important information is the relationship between two or more things.

### ˖⚠ ๋࣭⭑ WARNING


Use for failure modes, destructive actions, dangerous assumptions, or important constraints.

### ࣪˖ദ്ദി๋࣭⭑ VERIFIED


Use for states, facts, or behavior that have actually been checked.

### ⊹⚡ ๋࣭⭑ PROVISIONAL


Use for working models, hypotheses, incomplete architecture, or decisions that are not yet frozen.

### ⁴⁰⁴ DEPRECATED


Use for old paths, behaviors, APIs, or structures that remain visible for history or compatibility but should not be used for new work.

### ↺ REVISION


Use when the change itself matters: previous state, current state, and why the transition happened.

## Rule


The block should still be readable without knowing the symbol language.

Symbols provide scanning and semantic reinforcement.

They do not replace plain language.

---

# 18. Navigation Grammar


Meta Apollo uses Ghost String connectors for navigation.

## Permanent room map


Use:

```text
// ROOM ~~ // ROOM ~~ // ROOM
```

Meaning:

> **These rooms are connected.**

The canonical room strip is:

```text
// 🧭 ATLAS ~~ // ✮˙๋࣭⭑ MODEL ~~ // 🖨 BUILD ~~ // ⚒ DEV ~~ // 🖳 OPERATE ~~ // ⊹ ࣪ℼ˖ EVIDENCE ~~ // ࣪⋅˚🕮‧₊˚ ARCHIVE
```

In Markdown, escape the tildes so GitHub does not interpret them as strikethrough:

```md
// [🧭 ATLAS](../ATLAS/) \~\~ // [✮˙๋࣭⭑ MODEL](../MODEL/) \~\~ // [🖨 BUILD](../BUILD/) \~\~ // **⚒ DEV** \~\~ // [🖳 OPERATE](../OPERATE/) \~\~ // [⊹ ࣪ℼ˖ EVIDENCE](../EVIDENCE/) \~\~ // [࣪⋅˚🕮‧₊˚ ARCHIVE](../ARCHIVE/)
```

The current room may be emphasized in bold.

## Directional route


Use:

```text
// ROOM ~~» // ROOM ~~» // ROOM
```

Meaning:

> **Move through these in this direction.**

Example:

```text
// 🖨 BUILD ~~» // ⚒ DEV ~~» // 🖳 OPERATE
```

Use directional routes only when there is a real sequence, recommended path, or next-step flow.

## Rule


> **~~ means connected. ~~» means carried forward.**

Do not put arrows on the permanent room map merely for decoration.

---

# 19. Diagram Connector Language


Meta Apollo diagrams use Ghost String connectors instead of conventional dash-line notation.

```text
~~       stable connection / relationship
~~»      flow / dependency / direction
~ ~ ~    indirect / optional / provisional connection
~ ~ ~»   provisional / conditional flow
~~»>     major path / primary pipeline
```

The connector language stays visually related across conceptual maps and technical diagrams.

Examples:

```text
[App] ~~» [Audio Service] ~~» [PipeWire]

[Audio Service] ~ ~ ~» [Fallback Device]

[Input] ~~»> [Primary Pipeline] ~~» [Output]
```

Use a small, stable node-shape vocabulary:

```text
[THING]          component / object / service / ordinary system thing
{QUESTION?}      decision / condition / branch
((EVENT))        event / trigger
[(DATA)]         stored data / persistent state
[[SURFACE]]      UI / visible interface
```

**THING is intentionally broad.** Do not split objects, services, components, or similar implementation categories unless the distinction materially helps the reader.

Do not use `{ }` merely to group a subsystem; grouping and ownership boundaries should be expressed separately.

## Diagram Titles and Captions


Diagram titles use the existing Meta Apollo header grammar rather than a separate visual system.

Examples:

```md
## ✮˙๋࣭⭑ MODEL // AUDIO PIPELINE


## ⌯✦ PROCESS // GIT REFRESH FLOW


## ˖ ࣪♻๋࣭⭑ RELATIONSHIP // WINDOW ↔ IDENTITY ↔ AUDIO


```

A small caption may follow when the reader needs to know what slice or lens the diagram represents.

Optional caption fields:

```text
SCOPE // what is included
EXCLUDES // what is intentionally not shown
STATE // current / provisional / historical
VIEW // conceptual / runtime / ownership / data flow
```

Example:

```text
SCOPE // application-to-stream identity
EXCLUDES // device hardware
STATE // current
VIEW // ownership
```

## Rule


> **Title = what the diagram is about. Caption = what lens you are seeing it through.**

Do not add caption metadata when the title and diagram already make the scope obvious.

## Relationship Labels


Ghost Strings may carry plain-English labels when the relationship itself needs to be explicit.

Examples:

```text
[Git Panel] ~~ uses ~~ [Git Service]
[Git Service] ~~ reads » [Repository]
[Audio Service] ~ ~ fallback ~ ~» [Default Sink]
[User Input] ~~ control »> [Primary Action]
```

Common labels include:

```text
owns
uses
contains
shares
depends on
sends
reads
writes
triggers
transforms
```

## Rule


> **If the relationship is obvious, leave the Ghost String unlabeled. If the relationship itself matters, name it.**

Do not label every connector by default.

## Diagram Legend


Every Meta Apollo repository must carry a canonical diagram legend in its ATLAS so the notation is locally understandable without requiring an external reference.

The full repository legend should cover the symbols, connectors, boundary meanings, and semantic colors that repo may use.

Individual diagrams should not repeat the entire key. Add a small local legend only when a diagram uses notation that is not immediately obvious in context.

Example local legend:

```text
LEGEND //

~~»>       primary pipeline
ORANGE     active / agency
MAGENTA    primary focus
```

## Rule


> **Every repo carries the language. Every diagram carries only what it needs.**

## Color Semantics


Post-Apollo color carries both **role** and **attention/state**. Color is not only taxonomy.

Canonical palette:

```text
Magenta       #C74EC7   highest importance / primary focus
Orange        #ED981A   activity / control / ownership
Yellow        #F2BE4E   menu / navigation / available choice
Omnitrix      #00F782   system / runtime machinery
Cyan          #55CFCA   module / normal structure
Blue          #5B5FD4   scope / context
Red           #D16041   warning / failure / destructive state
Off-white     #DCF3FA   neutral / default information
Purple        #1B0623   background / chassis
```

### Attention hierarchy


A base semantic color may be elevated by state.

```text
normal role
   ↓
orange = active / operating / controlling
   ↓
magenta = central focus / highest-priority attention
```

Examples:

```text
MODULE // GIT      cyan normally
MODULE // GIT      orange while actively doing work
MODULE // GIT      magenta when it is the central thing being examined
```

Yellow remains distinct from orange:

```text
yellow   available / navigable / menu choice
orange   active / operating / controlling
magenta  primary focus / highest importance
```

This preserves the existing Post-Apollo interaction hierarchy instead of making color a rigid permanent identity.

### System / Runtime

![](../BUILD/assets/design/chassis/system-rail.svg)


**Omnitrix green — `#00F782`** is the canonical base color for infrastructure and live system machinery such as:

- audio and PipeWire
- shaders
- GPU and display plumbing
- hardware interfaces and telemetry
- background services
- compositor integration
- device and I/O paths

Omnitrix green does not mean generic success. VERIFIED remains a semantic state with its own symbol language.

### Boundary base colors


```text
SYSTEM //   Omnitrix green
MODULE //   Cyan
OWNER //    Orange
SCOPE //    Blue
```

These are base colors, not permanent overrides. Activity and focus may elevate a boundary to orange or magenta when the diagram needs to communicate state or importance.

---

# 20. Diagram Density and Escalation


Do not make a full diagram merely because diagram notation exists.

Use the smallest representation that makes the relationship clear.

```text
prose
  ↓
inline relation
  ↓
small local sketch
  ↓
full diagram
```

Examples:

```text
[Git Panel] ~~ [Git Service]
```

may be enough by itself.

A full diagram is appropriate when topology, branching, containment, ownership, multiple paths, or system shape is itself important to the explanation.

When a full diagram is needed:

- one diagram should answer one main question
- prefer an overview followed by smaller zoomed views
- split the view when unrelated paths compete for attention
- if the reader needs a paragraph just to know where to look first, simplify or split it

## Rule


> **Do not diagram the sentence. Diagram the structure when the structure matters.**

---

# 21. Callouts and Annotations


Callouts explain a node or relationship without redefining it.

Use ordinary vertical or positional geometry to show where the annotation originates, then transition into a Ghost String for the explanatory relationship.

Examples:

```text
[Audio Service] ~~» [PipeWire]
      │
      ╰~~ NOTE // owns stream matching
```

```text
[Apply Config]
      ↑
      ╰~~ ˖⚠ ๋࣭⭑ WARNING // destructive if state is stale
```

```text
[Identity Resolver]
      │
      ╰~~ ★⋆˙ CORE // shared authority
```

The rigid segment provides location.

The Ghost String provides relationship.

## Rule


> **The pointer shows where. The Ghost String explains why it matters.**

Callouts may use the normal content-block symbols and labels such as NOTE, CORE, WARNING, VERIFIED, or PROVISIONAL.

---

# 22. Diagram Color Policy


Post-Apollo diagrams use semantic color by default.

The color system is part of the diagram language, not optional decoration.

Use the established palette to reinforce role, state, agency, and attention:

```text
Omnitrix green   system / runtime
Cyan             module / normal structure
Blue             scope / context
Yellow           menu / navigation / available choice
Orange           activity / agency / control / ownership
Magenta          highest importance / primary focus
Red              warning / failure / destructive state
Off-white        neutral / default information
Purple           background / chassis
```

Symbols, labels, shapes, and Ghost Strings should still carry enough meaning that the diagram remains understandable if color is unavailable.

## Rule


> **Color is part of the language, but never the only carrier of meaning.**

Post-Apollo prefers **controlled color**, not colorless minimalism.

Use color when it adds structure, state, hierarchy, orientation, or character. Pull it back only when competing colors make the information harder to read.

### Off-white page chassis

**Off-white — `#DCF3FA`** is the default page-level chassis rail.

Use it once, directly beneath the primary page heading, when that page does not already begin with a stronger semantic rail.

Off-white means:

> **This page belongs to the same system.**

It is not a section separator.

Do **not** place off-white rails under `CORE //`, `CONTENTS //`, ordinary subsections, numbered chapters, or other local headings merely to break up text.

If a page already opens with a meaningful semantic rail — focus, navigation, model, process, system, scope, or warning — do not add the off-white rail on top of it.

The page-level chassis rail exists to keep otherwise plain pages visually related to the rest of the repository without turning every section into a colored boundary.

### Page opening order

Current-facing Meta Apollo pages should open in a predictable order:

```text
Meta Apollo lineage
page title
page rail
compact metadata strip
room navigation, when applicable
page content
```

Use:

```text
✦︎✦︎✦︎ Meta Apollo Logos //
```

as the shared lineage marker.

Room maps keep the seven-room navigation strip directly beneath metadata. Standalone documents do not need that navigation strip merely for visual symmetry.

Historical and archived documents do not need to be rewritten solely to match the current page-opening chassis.

Do not remove color merely to make a diagram more conventional.

If a particular diagram becomes visually overloaded, simplify that diagram first: reduce emphasis, split the view, or remove unnecessary state decoration before abandoning semantic color.

---

# 23. Tables, Code Blocks, and Collapsibles


## Tables


Tables organize facts. Keep them mechanically clean and readable.

Use the surrounding Meta Apollo header, symbols, state markers, and semantic color to provide identity rather than decorating the table structure itself.

Recommended compact state notation may appear inside cells.

If a table becomes too wide or dense to scan comfortably, split it into smaller tables instead of compressing it.

## Code Blocks


Literal material must remain literal and copyable.

Use labels such as:

```text
FILE //
COMMAND //
OUTPUT //
CONFIG //
QUERY //
RESULT //
EXAMPLE //
```

Do not insert decorative characters inside real code, shell commands, configuration, or output merely for visual styling.

Post-Apollo styling belongs around the literal block, not inside it.

## Collapsibles


Use collapsible details for useful depth that should not interrupt the main reading path.

Good candidates include:

- verbose command output
- long logs
- raw evidence
- historical implementation notes
- alternate examples
- detailed troubleshooting branches

Do not collapse:

- core claims
- warnings
- current state
- required instructions
- the main architecture or flow needed to understand the page

A collapsible summary uses the same symbol and type grammar as the rest of the repo.

Example:

```md
<details>
<summary>⊹ ࣪ℼ˖ EVIDENCE // RAW TEST RESULTS</summary>

...

</details>
```

## Consistency Rule


> **The same kind of information should be treated the same way everywhere.**

If raw logs are collapsible in one repo, raw logs should normally be collapsible in the others.

If a required instruction stays visible in one room, equivalent required instructions should not be hidden elsewhere.

Use the same summary grammar, the same semantic symbols, and the same visibility expectations across the entire Meta Apollo repository family.

Application matters as much as definition: a visual rule is only useful if readers can rely on it.

---

# 24. Compact Status and UI Grammar


Use compact metadata strips for current working state, health, ownership, branch, target, and replacement information.

Recommended vocabulary:

```text
STATE //
HEALTH //
VIEW //
BRANCH //
OWNER //
UPDATED //
RECORDED //
TARGET //
REPLACED BY //
```

For active page metadata, prefer one compact Ghost String strip:

```md
> **STATE //** active \~\~ **HEALTH //** ࣪˖ദ്ദി๋࣭⭑ VERIFIED \~\~ **VIEW //** repository orientation
```

Use only fields that help explain the page. Do not fill every slot merely because the vocabulary exists.

Other examples:

```md
> **STATE //** experimental · c1 \~\~ **HEALTH //** ⊹⚡ ๋࣭⭑ PROVISIONAL
```

```md
> **STATE //** ⁴⁰⁴ DEPRECATED \~\~ **REPLACED BY //** AudioService
```

The strip is one component. Ghost Strings connect metadata fields without turning them into separate badges or a table.

## Distinction


The lowercase `c` notation describes the current working state in the project's evolution.

A semantic state marker describes confidence, lifecycle status, or evidentiary standing.

```text
c0.8                working-state position
࣪˖ദ്ദി๋࣭⭑ VERIFIED    checked state
⊹⚡ ๋࣭⭑ PROVISIONAL   working / not frozen
⁴⁰⁴ DEPRECATED       retained but no longer preferred
```

Neither substitutes for the other.

## Rule


> **Working state tells you where it is. Status tells you what kind of state it is.**

Keep status strips compact. Do not turn them into a second summary paragraph.

---

# 25. Spacing and Alignment


Post-Apollo diagrams should feel mechanically constructed rather than loosely arranged.

Use consistent spacing, baselines, and enclosure geometry.

Guidelines:

- keep one blank visual row around important content inside a boundary when space allows
- align sibling nodes to the same baseline
- keep connector spacing consistent
- center titles relative to their boundary
- inset nested boundaries visibly at each level
- align grouped metadata labels such as `STATE //`, `SCOPE //`, and `VIEW //`
- do not stretch a diagram merely to force identical line lengths
- keep structural boxes clean and aligned even when emphasis effects are irregular

Example:

```text
STATE // active · c0.7
SCOPE // local repository
VIEW  // ownership
```

## Rule


> **Alignment belongs to the chassis. Irregularity belongs to the glow.**

---

# 26. Design Invariant


> **Unfinished does not mean unusable, illegible, or ugly.**

Every version should already look like a version of **this thing**.

Not generic scaffolding waiting for personality later.

The archive can be messy.

The interface should not be.
