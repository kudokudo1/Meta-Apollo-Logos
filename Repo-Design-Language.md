# META APOLLO — REPOSITORY DESIGN LANGUAGE

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

Meta Apollo uses **C** to mark the current working state of a project.

Examples:

```text
C0.1
C0.7
C1
C2.3
```

The number is project-specific.

**C** does not mean "final release."

It means:

> **This is the current working state of the thing.**

Use it when a project benefits from a compact visible state marker without implying that the work is finished or formally released.

A header may combine it with a plain-language state:

```text
ACTIVE · C0.7
EXPERIMENTAL · C1
STABLE · C2.3
```

Do not invent a state number merely to fill the field.

---

# 17. Design Invariant

> **Unfinished does not mean unusable, illegible, or ugly.**

Every version should already look like a version of **this thing**.

Not generic scaffolding waiting for personality later.

The archive can be messy.

The interface should not be.
