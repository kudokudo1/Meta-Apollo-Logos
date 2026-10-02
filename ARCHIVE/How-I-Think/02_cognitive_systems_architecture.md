# Cognitive / Systems Architecture — Technical Reference

![](../../BUILD/assets/design/chassis/neutral-rail.svg)

**Purpose:** A structured, technical reference for the reasoning patterns, design preferences, communication behavior, epistemology, and AI-collaboration style identified in the conversation.

**Important framing:** This is a working model of recurring behavior, not a neurological diagnosis. Terms below are used as engineering/cognitive metaphors unless explicitly noted otherwise.

---

# 1. Core Representation Model

The most useful current abstraction is:

> **Recursive weighted multiresolution relational graph**

The model contains:

- **binary predicates** — true/false under a specified condition
- **continuous dimensions** — more/less of a property
- **categorical regions** — named zones on a continuous or relational space
- **thresholds** — points where behavior changes qualitatively
- **nonlinear evaluations** — more X may help until side effects dominate
- **dependencies** — node A requires node B
- **causal edges** — intervention on A changes B
- **historical edges** — B exists because A previously happened
- **analogical mappings** — structure in domain A corresponds to structure in domain B
- **confidence weights** — belief strength varies with evidence
- **recursive nodes** — any compressed node may expand into a subgraph

The user frequently changes resolution instead of committing to one permanent representation.

---

# 2. Predicate / Axis Arbitration

A recurring source of apparent contradiction disappears when the predicate is specified.

Example:

- `AuntMay == UncleBen` literally → false
- `AuntMay performs Uncle-Ben-like narrative function` → can be true

Likewise:

- a behavior may be categorically selfish
- selfishness may still participate in a graded relation
- the boundary between self-interest and selfishness may remain fuzzy
- a clear central case can still exist

Useful AI question when needed:

> **“On which axis or predicate?”**

Avoid turning every ambiguity into a literalist correction when the user is clearly operating at another resolution.

---

# 3. Descriptive Variable vs Evaluation Function

The user often distinguishes, implicitly or explicitly:

1. **what quantity is changing**
2. **how desirable that quantity is in context**

Example:

`brightness` may rise monotonically.

`usefulness(brightness)` may rise, plateau, and then fall because glare becomes dominant.

Conceptual form:

```text
descriptive axis:
dark ----------------------------------> bright

evaluation:
bad -----> good -----> optimal -----> bad
```

This explains why “more of a good thing” can become bad without literally becoming the original opposite.

Important concept:

> **functional relabeling after threshold**

Examples:

- brightness → glare
- confidence → arrogance
- caution → paranoia
- context → overload
- modularity → fragmentation

---

# 4. Coupled Variables / Spiderweb Dynamics

The user's “sliders” are often not independent.

Changing one variable can change the effective value of others.

Example:

```text
brightness
   ├── readability
   ├── glare
   ├── energy use
   ├── eye strain
   └── sleep effects
```

The important structure is therefore closer to a weighted network than a set of independent dials.

User metaphor:

> pull one strand → observe which other strands move

This is used for:

- causal discovery
- debugging
- game strategy
- social reasoning
- truth evaluation
- architecture

---

# 5. Active Sensing / Perturbation

A major reasoning pattern:

> **change something deliberately and observe what changes**

Related technical ideas:

- active sensing
- intervention
- system identification
- perturbation testing
- causal inference
- sensitivity analysis

Typical loop:

```text
probe
→ observe
→ classify
→ predict
→ manipulate
→ observe again
→ update model
```

This appears in:

- fighting
- debugging
- user-interface experiments
- architecture refactors
- opponent modeling
- truth evaluation

---

# 6. Bounded Uncertainty

The user does not require deterministic prediction.

Preferred target:

> **bounded uncertainty**

Human behavior is modeled as probabilistic because:

- habits exist
- incentives exist
- fear responses exist
- social scripts exist
- learned patterns exist
- physical constraints exist
- expectations exist

So:

> situations constrain likely behavior without fully controlling it

Prediction ≠ control.

---

# 7. Invariants

A central question:

> **What remains true when the implementation changes?**

Examples:

- Tree identity vs model/runtime
- Post-Apollo identity vs color/effect changes
- tactical purpose vs exact movement
- narrative role vs literal character identity
- vibration mechanism vs guitar/violin implementation

Invariants support transfer and safe refactoring.

---

# 8. Analogical Bootstrapping

Analogies are not merely rhetorical decoration.

They serve as:

- compressed representations
- transfer mechanisms
- debugging tools
- explanatory codecs
- generative models

Typical process:

```text
foreign system
→ map to known structure
→ transfer relationships
→ identify where mapping fails
→ refine local differences
→ preserve useful invariant
```

Examples:

- Naruto jutsu → software abstractions
- Pokémon team synergy → architecture
- fighting probes → debugging
- village planning → component integration
- refrigeration → coupled systems
- art perception → decomposition

---

# 9. Generative Understanding

A strong test of understanding is:

> **Can the mechanism be transferred into a new application?**

If a model only reproduces one memorized surface form, understanding is considered weak.

If the invariant can be preserved while implementation changes, confidence increases.

Conceptual sequence:

```text
observe mechanism
→ model mechanism
→ mutate implementation
→ predict result
→ test
→ update
```

---

# 10. Reversible Abstraction

The user strongly prefers abstraction but dislikes abstraction that destroys access to underlying structure.

Desired property:

> **compressibility + decompression path**

A black box is acceptable when:

- the interface is useful
- the user can descend when necessary
- important internal assumptions are not permanently inaccessible

This is relevant to:

- operating systems
- AI
- code
- hardware
- project architecture
- conceptual language

Useful phrase:

> **The abstraction needs a trapdoor.**

---

# 11. Operational / Epistemic Ownership

Ownership is not treated solely as legal possession.

A system is more deeply “owned” when the user can:

- inspect
- understand
- modify
- repair
- recover
- replace parts
- migrate data
- survive upstream abandonment
- reconstruct intent/history

Useful nearby terms:

- operational ownership
- technical sovereignty
- epistemic ownership

---

# 12. Recursive Dependency Completion

Project expansion often follows:

```text
initial object
→ discover hidden dependency
→ dependency requires support
→ support requires architecture
→ architecture exposes adjacent dependency
→ new boundary required
```

This can look like feature creep externally but internally feels like:

> “The original thing was not actually complete under the updated model.”

Important distinction:

> Conceptual scope can be large without requiring monolithic implementation.

This is the AppControl lesson.

---

# 13. World-Model Architecture / Referential Integrity

The user tends to manage projects as worlds.

A new component must resolve against:

- ownership
- dependencies
- neighboring components
- state model
- visual language
- history
- conventions
- future extension points

The “village” metaphor is useful.

A random feature with no relationships is an **orphan node**.

A locally functional feature can still be globally wrong.

Useful technical metaphor:

> **referential integrity**

---

# 14. Coherence vs Local Optimization

The user often prefers:

> globally coherent + locally good enough

over:

> locally optimal + globally alien

A component may be rejected even if individually superior when it:

- duplicates responsibility
- violates visual language
- breaks ownership
- damages team synergy
- creates unexplained dependencies

This appears in:

- Pokémon
- code architecture
- UI design
- project structure
- character/worldbuilding

---

# 15. Earned Complexity

The user is not complexity-averse.

The relevant question is:

> **Can each layer explain why it exists?**

Large systems can feel clean if complexity is structurally necessary.

Small systems can feel terrible if complexity is arbitrary.

Approximate conceptual measure:

```text
architectural legitimacy
≈ explanatory necessity of complexity
  / accidental complication
```

Not a literal metric.

---

# 16. Function Density with Structural Coherence

The user likes one thing doing several jobs when those jobs belong together.

Examples:

- fighting bounce = range + rhythm + probe + feint + camouflage
- UI element = functional + tactile + nostalgic + informative
- character design = mechanics + symbolism + relationship + visual identity
- support champion = protection + timing + repositioning + strategic enablement

The desired property is:

> **polyfunctionality without spaghetti**

---

# 17. Constraints That Generate Behavior

Preference:

> design rules/fields so desirable behavior emerges

rather than manually scripting every move.

Examples:

- state ownership produces predictable lifecycle
- economic rules produce world behavior
- fight positioning constrains response
- Forest architecture produces continuity

This resembles generative system design.

---

# 18. Truth Scale — Formalized

User vocabulary:

> **truth scale**

Technical translation:

> multi-axial epistemic confidence model with context-sensitive predicates

Confidence in a hypothesis tends to increase when it has:

- independent observations
- independent observers
- cross-modal confirmation
- causal support
- predictive success
- successful intervention
- provenance diversity
- cross-context consistency
- cross-domain transfer
- low contradiction burden

Conceptual, not numeric:

```text
Confidence(H) =
f(
  independent evidence,
  provenance diversity,
  predictive success,
  intervention success,
  consequence coherence,
  cross-context survival,
  contradiction penalties
)
```

The user does not require an actual percentage.

---

# 19. Ontological Truth vs Epistemic Confidence

Important distinction:

### Ontological
What actually is the case.

### Epistemic
How justified a person is in believing a model of the case.

The user's phrase “how true something is” often includes:

- confidence
- context
- predicate
- resolution
- observer limits

Do not interpret this as “objective reality is whatever someone perceives.”

The user explicitly recognizes perception error.

---

# 20. Consilience / Triangulation

A nearby technical idea is **consilience**:

> confidence increases when evidence from different methods or domains converges.

Another is **triangulation**:

> use differently biased sources/methods to constrain error.

These concepts fit the truth scale, but the user's model adds strong concern for source genealogy.

---

# 21. Evidence Genealogy / Correlated Error

User vocabulary includes:

- propaganda scale
- human herd rationale

Core principle:

> Many agreeing sources may share one upstream cause.

Therefore:

```text
59 reports ≠ 59 independent confirmations
```

Possible common causes:

- shared source
- copied reporting
- shared training
- aligned incentives
- social conformity
- algorithmic amplification
- deliberate coordination
- shared methodological error

The user discounts evidence when confirmations are correlated.

Important:

> sincerity does not guarantee informational independence

---

# 22. Source Contamination

A false claim can propagate through genuine people.

Conceptual pattern:

```text
bad source
→ sincere adopter
→ repeated claim
→ new sincere adopters
→ apparent consensus
```

Therefore the user tracks not only:

> “Who believes this?”

but:

> “Where did the belief come from?”

---

# 23. Truth System as Feedback Loop

Possible developmental loop:

```text
relational cognition
→ relational epistemology
→ epistemology rewards relationship search
→ richer graph
→ better transfer/prediction
→ stronger relational cognition
```

This is not a proven neurological cause.

It is a plausible developmental model strongly supported by the user's own descriptions.

---

# 24. Communication as Shared-Model Synchronization

Communication is treated as:

> sender model → compressed representation → receiver reconstruction

Success requires enough shared dependency structure.

Core concept:

> **minimum sufficient subgraph**

The best explanation is not necessarily the shortest string.

It is the smallest transmitted structure that lets the recipient reconstruct the intended model.

---

# 25. Adaptive Codec

Observed user behavior:

```text
send compressed packet
→ watch receiver
→ detect parse failure
→ add dependency
→ switch analogy
→ test again
```

This resembles adaptive encoding + error correction.

The user often changes representation rather than merely repeating wording.

---

# 26. Serialization Scatter

Useful distinction:

### Semantic scatter
Ideas are unrelated.

### Serialization scatter
Ideas are related, but the one-dimensional speech stream hides return pointers and branches.

The user's speech often appears graph-shaped internally and recursive externally.

---

# 27. Communication Failure Modes

- **overcompression** — receiver reconstructs wrong model
- **undercompression** — receiver loses trunk
- **dependency omission** — missing prerequisite
- **dependency-order failure** — right pieces, wrong sequence
- **context overload** — active working model becomes too large
- **completion pressure** — desire to finish transmitting an opened graph
- **resolution mismatch** — listener understands surface but not depth

---

# 28. Appreciation Decompression

The user sometimes expands an explanation not because the listener is wrong, but because the listener has not perceived the depth.

Examples:

> “Cool app.”

may trigger:

> “No, look at the synchronized tab/window/app controls, resource limiting, graphs, services, and integration.”

This is:

> **recognition at the correct structural resolution**

The user often wants the craft itself to be seen.

---

# 29. Artist Eye as Decision Reconstruction

A refined definition:

> **The artist eye sees traces of decisions in finished artifacts.**

Expertise lets someone infer:

- why an edge was lost
- why a state owner exists
- why a fighter chose a line
- why a chord was voiced that way
- why a component has its shape

The user values recognition of decisions more than raw labor-count praise.

---

# 30. Epistemic Generosity

User rule:

> “Never assume your opponent is crazy.”

Technical interpretation:

> delay explanatory closure while plausible missing-information models remain

Possible missing variables:

- different incentives
- different history
- different assumptions
- different information
- different constraints
- impairment
- strategic deception

This is not an eternal prohibition on judgment.

---

# 31. Judgment After Modeling

Better rule:

> **Do not delete the node prematurely.**

The user allows eventual classification when evidence warrants it.

Understanding does not imply agreement.

Modeling does not imply permission.

Separate:

1. causal understanding
2. moral evaluation
3. policy/boundary response

---

# 32. Moral Relational Model

The user's moral language centers strongly on the self/other relationship.

Working interpretation:

> harm becomes morally worse when one's own desire is treated as sufficient justification for denying appropriate moral weight to others.

Self-interest, selfishness, and generosity are related but not identical.

The model can contain:

- gradients
- hard categories
- contextual exceptions
- competing duties
- scarcity

Avoid oversimplifying the user's moral model into “self-interest = evil.”

---

# 33. Fault Containment Analogy

The user used buggy code to explain why harmful behavior may require containment.

Useful structural mapping:

- preserve node in model
- understand failure mode
- constrain propagation
- protect system

Do not extend the analogy into treating persons as disposable components.

The intended point is **harm containment**, not dehumanization.

---

# 34. Serious + Playful

The user often prefers multiple high-valued dimensions simultaneously.

Examples:

- serious = high
- playful = high
- tactical = high
- whimsical = high

Avoid assuming these occupy one zero-sum slider.

This is visible in:

- Bard/Paladin
- Nunu/Milio
- Xayah/Rakan
- fighting
- Post-Apollo

---

# 35. Second-Order Power

Strong preference for abilities that alter relationships or rules rather than simply increase output.

Examples:

- support
- battlefield control
- DoT
- AoE
- stealth
- debuff
- zoning
- prediction
- resource denial
- state synchronization

First-order power:

> “I hit harder.”

Second-order power:

> “Because I am here, the rest of the board behaves differently.”

---

# 36. Project History as Causal Data

Old artifacts can encode:

- reasons
- failure modes
- constraints
- discarded alternatives
- previous assumptions

Recommended statuses for preserved project knowledge:

- current
- superseded
- failed / lesson
- historical
- future

This prevents fossils from becoming accidental current truth.

---

# 37. AI Collaboration Protocol

An AI working with this user should:

1. Preserve project identity and architecture.
2. Ask “who owns this state?” when state is ambiguous.
3. Explain *why* important fixes work.
4. Treat old weird structures as possible Chesterton fences.
5. Prefer modular boundaries over indiscriminate deletion.
6. Reuse the user's existing vocabulary and analogies.
7. Correct the model when the user supplies counterevidence.
8. Avoid constant caution/disclaimer interruptions.
9. Do not become a yes-machine.
10. Distinguish confirmed observations from generated hypotheses internally, but keep prose natural.
11. Use serious technical language and playful metaphor together.
12. Preserve the user's “same thing / different thing” multiresolution reasoning.
13. Avoid hyper-literal corrections when the current predicate is obvious.
14. Flag genuine architectural contradictions.
15. Maintain shared-model synchronization during long coding phases.
16. When generation outruns understanding, stop and reconstruct architecture.

---

# 38. Key Technical Vocabulary

Useful terms:

- relational reasoning
- causal graph
- weighted graph
- multiresolution representation
- recursive decomposition
- analogical bootstrapping
- abstraction ladder
- reversible abstraction
- active sensing
- perturbation
- system identification
- bounded uncertainty
- causal inference
- invariant
- polyfunctionality
- second-order effect
- progressive legibility
- referential integrity
- architectural coherence
- operational ownership
- epistemic ownership
- evidence genealogy
- correlated error
- source contamination
- consilience
- triangulation
- shared-model synchronization
- adaptive codec
- minimum sufficient subgraph
- dependency closure
- serialization scatter
- recursive dependency completion
- function density with structural coherence

---

# 39. One-Sentence Technical Summary

> The user tends to build and reason with recursively expandable relational models, tests them through contradiction and perturbation, weights confidence through independent causal convergence and source genealogy, transfers mechanisms across domains by preserving invariants, and prefers abstractions, software, and collaborations that remain inspectable, recoverable, historically grounded, and structurally coherent.