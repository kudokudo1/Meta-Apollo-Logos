# META APOLLO — REPOSITORY DESIGN LANGUAGE

> This design language derives from the canonical **[META APOLLO LOGOS // PRINCIPLES](./Meta-Apollo-Logos-Principles.md)**. It does not define a second principles system.

> **Readable operator manuals for living systems.**

Meta Apollo repositories should be usable, legible, and aesthetically coherent while they are still being built.

Polish is not a final pass.

It is part of the architecture.

---

# 1. The Six Canonical Modes

These labels describe **what kind of material the reader is looking at**.

They are not mandatory folders. They are a shared semantic grammar.

| Mode | Reader question | Typical contents |
| --- | --- | --- |
| **MAP** | What is this? | Purpose, orientation, quick start, major pieces, navigation |
| **MODEL** | How does it work? | Architecture, concepts, contracts, diagrams, data flow |
| **BUILD** | Where is the machinery? | Source code, modules, APIs, developer setup, implementation |
| **OPERATE** | How do I use or run it? | Installation, commands, workflows, controls, maintenance |
| **EVIDENCE** | Why should I believe or trust this? | Tests, benchmarks, screenshots, references, experiments, proof stories |
| **ARCHIVE** | How did we get here? | Old designs, superseded implementations, long discussions, history |

Canonical order:

```
MAP
↓
MODEL
↓
BUILD
↓
OPERATE
↓
EVIDENCE
↓
ARCHIVE
```

A repository may omit modes that do not apply.

The labels should keep the same meaning everywhere.

---

# 2. Depth Is a Separate Axis

Do not confuse **content type** with **depth**.

A BUILD document can have a surface explanation and a deep implementation reference.

An EVIDENCE document can have a short conclusion and a full source trail.

Use the three-level depth model when useful:

```
SURFACE
→ DETAIL
→ DEEP SOURCE
```

or, when provenance matters:

```
MAP
→ EVIDENCE
→ ARCHAEOLOGY
```

The first axis answers:

> **What kind of thing is this?**

The second answers:

> **How deep do I need to go?**

---

# 3. Visual Principles

## Legibility first

If a visual treatment makes the page harder to scan, it failed.

## Structure should be visible

A reader should be able to tell:

- where they are
- what layer they are in
- what kind of content this is
- where to go next

## Aesthetics are functional

Visual design should improve:

- navigation
- recognition
- memory
- confidence
- approachability

## Compression without flattening

Shorter is not automatically better.

> **Compress the representation, not the relation.**

## Same civilization, different buildings

Repositories do not need identical layouts.

They should share:

- vocabulary
- visual grammar
- navigation logic
- diagram language
- semantic labels

---

# 4. Meta Apollo Visual Identity

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

Use the palette mainly in:

- banners
- diagrams
- social preview images
- SVG assets
- documentation sites

Long-form body text should remain easy to read.

---

# 5. Repository Front Door

Every public-facing repository should answer these questions near the top:

1. **What is this?**
2. **Why does it exist?**
3. **What state is it in?**
4. **Where should I start?**
5. **Where is the actual implementation?**
6. **Where is the evidence / history if I need it?**

Recommended opening shape:

```
BANNER / TITLE
ONE-LINE PURPOSE

STATUS / MODE STRIP

START HERE

REPOSITORY MAP

FAST PATH
```

Do not make the reader excavate the project before they can orient themselves.

---

# 6. Canonical Content Blocks

Use a small, consistent vocabulary.

## CORE CLAIM

A load-bearing statement.

> **Core claim:** Serial output does not imply serial representation.

## MODEL

A structural explanation or mechanism.

## EXAMPLE

A concrete demonstration.

## EVIDENCE

A source, test, benchmark, artifact, or observation.

## WARNING

A known failure mode or dangerous assumption.

## OPEN QUESTION

Something deliberately unresolved.

## IMPLEMENTATION

Code-level or operational detail.

## PROVENANCE

Why a decision exists or where it came from.

These labels are semantic, not decorative.

Do not invent a new label for every interesting thought.

---

# 7. Section Shape

A major section should usually begin with:

```
## 03 · SECTION NAME

One sentence explaining what this section is for.
```

Then, where useful:

- core claim
- model / diagram
- implementation
- evidence
- deeper source

Readers should be able to skim section headers and understand the whole document's skeleton.

---

# 8. Diagrams

Prefer a diagram when relationships are easier to see than describe.

Good diagram targets:

- architecture
- state flow
- ownership
- data flow
- feedback loops
- dependency chains
- layer relationships
- user journeys
- lifecycle

Meta Apollo diagram rules:

- few colors
- consistent meaning per color
- left-to-right or top-to-bottom flow
- label relationships, not just boxes
- do not decorate without carrying information
- keep diagrams readable in dark and light contexts when possible

Mermaid is preferred for diagrams that benefit from remaining version-controlled as text.

SVG is preferred when stronger visual identity is needed.

---

# 9. Code Presentation

Code should feel like part of the same system, not a separate basement.

For important code paths, explain:

```
WHY
↓
WHERE
↓
WHAT
↓
HOW TO TOUCH IT SAFELY
```

Useful BUILD sections include:

- architecture map
- source tree
- ownership boundaries
- primary entry points
- contracts / interfaces
- commands
- tests
- extension points

Avoid dumping a file tree with no explanation.

---

# 10. OPERATE Is Not BUILD

**BUILD** is for people changing the machinery.

**OPERATE** is for people using or managing it.

Examples:

BUILD:
- source layout
- API contract
- compile instructions
- module ownership

OPERATE:
- start
- stop
- configure
- recover
- common workflows
- troubleshooting

Keeping these separate makes software repositories dramatically easier to approach.

---

# 11. Evidence Rules

Evidence should support claims without taking over the main interface.

Organize supporting material by **concept**, not prestige.

Possible source roles:

- **DIRECT SUPPORT**
- **PARALLEL**
- **EXAMPLE**
- **HISTORICAL PRECEDENT**
- **EMPIRICAL SUPPORT**
- **METAPHYSICAL / RELIGIOUS PARALLEL**

A famous name does not become evidence merely by appearing.

State what relationship the source actually has to the claim.

---

# 12. Archive Rules

The archive is allowed to be ugly.

It is not allowed to be misleading.

Archive files should ideally preserve:

- date / period
- purpose
- status
- whether superseded
- replacement if known

Do not delete history merely because the public interface has become cleaner.

---

# 13. Multi-Zoom Reading

A good Meta Apollo repository should support at least four reading speeds.

### Zoom 1 — Glance

Understand what the project is in roughly 30 seconds.

### Zoom 2 — Orient

Find the relevant area in a few minutes.

### Zoom 3 — Study

Read the actual model, architecture, or workflow.

### Zoom 4 — Inspect

Trace evidence, implementation, history, or provenance.

A reader should choose their depth.

The repository should not choose maximum depth for them.

---

# 14. Design Invariant

> **Unfinished does not mean unusable, illegible, or ugly.**

Every version should already look like a version of **this thing**.

Not generic scaffolding waiting for personality later.

The archive can be messy.

The interface should not be.
