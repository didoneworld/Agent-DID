# The Fabric of Work — A Structured Instruction Set

> **Status:** Foundational. This document is the *constitution* of Agent DID.
> It does not describe a feature; it defines how meaning, work, and governance
> are legitimately established — and therefore how every technical principle in
> [`design-principles.md`](./design-principles.md) acquires, and may revise, its
> meaning.
>
> It is written as a **structured instruction set**: a set of normative
> statements (a thing the system and its agents are built *within*), not prose
> to be admired. Everything here is intended to be enforceable, auditable, and
> contestable.

---

## 0. Keystone Definition

> **Fabric is the structured instruction set — affording *and* constraining —
> through which agents define, do, develop, and manage real-world work:
> continuous, durable, measurable, governable, value-generating, and bounded by
> what is legitimate, permitted, possible, and safe.**

Everything below derives this definition and makes it operational.

---

## 1. Meaning is Contextual

1.1. The meaning of any identifier, claim, term, or task is **never intrinsic**.
A value — a DID, a credential, a *box* (a container of a real-world thing) —
means nothing in isolation.

1.2. Meaning is **fixed by context**: the issuer, the schema, the verifying
party, the surrounding work. The same token may mean different things in
different contexts, and that is not a defect — it is the nature of meaning.

1.3. Therefore no component MUST assume a meaning is global. Meaning travels
**with its context**, or it does not travel at all.

1.4. **Context is enforced, not merely declared.** Context is not advisory
metadata that may be ignored. A claim, capability, or meaning is valid **only
within the context that defines it**; using it outside that context MUST be
**denied deterministically**, not silently reinterpreted. The fabric enforces
context as a hard boundary (cf. §7, Constraint) — a derivation carries its
context, and the context is checked at the point of use.

---

## 2. Meaning is Defined and Derived

2.1. Meaning is **defined** — given precise, explicit specification (the schema,
the `@context`). It is never left implicit.

2.2. Meaning is **derived** — that definition **follows from the context through
logic and analysis**. It is not invented by will but entailed by reasoning, and
can therefore be **retraced and checked by anyone**.

2.3. A derivation can be audited; a decree cannot. The system MUST prefer
derivations to decrees everywhere a choice exists.

---

## 3. The Constitution: How Meaning Is Legitimately Established

3.1. **Knowledge provides provenance.** Those with the knowledge to derive a
meaning produce not a verdict but a **traceable derivation** — who reasoned it,
from what context, on what evidence. Knowledge's output carries its lineage.

3.2. **Authority marks it in policy.** Those with the authority to ratify take
the derived, provenance-backed meaning and **inscribe it into enforceable
policy**, where it becomes operative. Authority *inscribes*; it does not
*invent*.

3.3. **The federation governs by procedure.** A derivation is:
- **Evaluated** — is the logic sound, the provenance traceable, the context
  adequate?
- **Voted** — ratified by a defined threshold weighted by knowledge and
  standing. **Never bare unanimity** (which hands a veto to every individual).
- **Vetoable** — subject to a *guarded* veto. A veto is **not a private kill
  switch**: it MUST itself carry reasons and provenance, and it holds only if
  its reasoning survives federation evaluation.

3.4. **Federated, not captured.** No central authority may *impose* meaning, and
no single stakeholder may *block* it by unreasoned veto. Legitimacy rests on the
**provenance-backed derivation and the procedure that evaluates it** — never on
any one party, central or peripheral.

3.5. **The right to reason is fundamental.** Every stakeholder — human or agent —
may ask *why*, walk the provenance back, re-derive the meaning, vote, and raise a
reasoned veto. The right to reason is a right of **voice, not veto**: power to
change minds through better logic, never to block through withheld consent.
Ratification and veto alike MUST give reasons.

3.6. **Goodwill and wisdom prevail.** Procedure exists to guard against the
worst — capture, imposition, unreasoned power. But procedure only sets a floor.
In the end, sound process exists **so that goodwill and wisdom may prevail**. No
procedure fully specifies good work; it takes judgment.

### 3.7. The Internet of Agents

3.7.1. At scale, federation **is the Internet of Agents.** The internet is
reconceived not as a network of hosts but as a **federation of agents** — humans
and autonomous agents that derive shared meaning, exchange work, and govern it
together under this constitution.

3.7.2. The **Internet of Agents protocol** is the wire form of this constitution:
how agents discover one another, present provenance (§3.1), propose and ratify
meaning (§3.2–§3.3), exchange boxes — commands, tools, ingredients (§8) — and
enforce context (§1.4) across trust boundaries. In Agent DID this is realized
through DID-based identity and agent-to-agent protocols (e.g. A2A, ACP, ANP).

3.7.3. No agent owns the Internet of Agents (§3.4): it is **federated, not
captured.** Interoperability rests on shared, derived meaning (schemas, §7.6) and
on the right to reason (§3.5) holding across the whole federation. An agent joins
the Internet of Agents by *adopting the constitution*, not by registering with a
central authority.

3.7.4. **The internet is a network of boxes; the Internet of Agents is a fabric
of agents.** The classical internet is a *network* — it connects **boxes**:
hosts and the containers of real and digital things (§8.4) addressable across it.
The Internet of Agents is a *fabric* woven over that network — the **agents are
the threads**, the boxes are what they exchange and act upon, and the
constitution is the weave that gives the whole cloth shared meaning. A network
*connects* boxes; a fabric *weaves* agents. The fabric of work (§5) is, at
internet scale, this **fabric of agents.**

---

## 4. Work is Constructed (Not Constituted)

4.1. The **constitution is constituted** — foundational, slow-changing. It holds
still so that work can be built against it.

4.2. **Work is constructed** — built in context, piece by piece, composed from
parts through active effort. Work is never *declared into existence*; it is
*made*.

4.3. **Construction is the real work.** It is where a plan meets a real-world
thing and something is made — acting on the *box*, producing real value with real
consequences. Everything else is scaffolding that exists *to serve* the
construction.

4.4. Do not mistake the frame for the work. The constitution and the fabric exist
**so that construction can happen** — to get out of the builder's way while
keeping the builder honest.

---

## 5. The Fabric: an Operating System for Work

5.1. **Fabric is the OS for work** — the pervasive, woven substrate within which
work is constructed, and the **structured instruction set** through which agents
**define, do, develop, and manage** real-world work.

| Verb | Meaning | Anchored in |
|---|---|---|
| **Define** | establish what the work means | §1–§3 (constitution, derived meaning) |
| **Do** | execute it; build it | §4 (construction, the real work) |
| **Develop** | grow and evolve it over time | §6 (continuous, durable) |
| **Manage** | govern, oversee, account for it | §3, §6 (governable, measurable) |

5.2. The fabric spans several kinds of woven cloth, each contributing one thing,
and each MUST remain **derived, provenance-bearing, and contestable** so it can
be shared without becoming imposed (i.e., without hardening into dogma):

| Fabric | Provides | Risk if wrong |
|---|---|---|
| **Framework** | **structure** — the load-bearing skeleton, where parts go and connect | incoherence |
| **OS** | runtime — where it executes | breakage |
| **Design system** | form — coherent shape and grammar | fragmentation |
| **Value system** (normative) | priorities — what is worth doing, the *ought* | **capture / dogma** |
| **Belief system** (epistemic) | assumptions — what is held true, the *is* | **capture / dogma** |

5.3. **Tool vs. fabric.** A *tool* is discrete, wielded, set down — you *use* it.
*Fabric* is ambient and pervasive — you *build within* it. Fabric is what makes
separate constructions **cohere with one another**, because they are all woven
from the same threads.

---

## 6. The Five Guarantees of Real Work

The fabric MUST make work:

6.1. **Continuous** — ongoing, resumable, renewable; not one-shot.

6.2. **Durable** — persistent; it survives failure and its record outlives the
moment.

6.3. **Measurable** — observable and quantifiable; value, effort, and outcomes
can be measured.

6.4. **Governable** — under the constitution: accountable, policy-bound, and
contestable.

6.5. **Real-value-generating** — acting on real-world things and producing actual
value.

> These five are what separate **real work** from mere activity. Activity is
> one-shot, forgettable, unmeasured, ungoverned, and value-neutral. The fabric is
> what turns activity *into work*.

---

## 7. Structure: Affordance and Constraint

7.1. A framework provides **structure**, and structure has **two inseparable
faces**:

```
   STRUCTURE
      ├─ AFFORDANCE  — define · do · develop · manage      (what work CAN do)
      └─ CONSTRAINT  — legitimate · permitted · possible · safe  (what work MUST NOT)
```

7.2. **Enablement without constraint is not freedom; it is chaos.** "You may
construct" has no meaning until paired with "and here is what you may *not*." The
constraint is the **negative space** that gives the enabling instructions their
meaning.

7.3. Constraints arise from four sources:

| Source | Bounds | Realized as |
|---|---|---|
| **Constitution** | what is *legitimate* | derived meaning, reasoned veto, contestability |
| **Policy / authority** | what is *permitted* | least privilege, scopes, externalized policy |
| **Values / beliefs** | what is *acceptable / true* | normative & epistemic fabric — the "must not" |
| **Real world** | what is *possible* | physics, resources, the box's own capacity |

7.4. Constraint is bidirectional: **authority sets limits top-down**, and **any
stakeholder may reason a new limit into place bottom-up** — the right to reason
includes the **right to refuse**, and a reasoned veto *is* a constraint.

7.5. Hitting a constraint MUST be **explicit**: an agent that meets a bound
receives a deterministic, reasoned "no" — never a silent drift. (Cf.
`design-principles.md` §13, Failure is Explicit.)

### 7.6. Schema — Where Structure Becomes Executable

7.6.1. A **schema** is the concrete artifact in which the framework's structure,
the defined meaning, and the constraints all converge and become
**machine-enforceable**. A schema does four things at once:
- **Defines** — specifies the meaning precisely (§2.1).
- **Structures** — fixes the shape, the fields, and the relations (§7.1).
- **Constrains** — rejects forms that are not permitted or possible (§7.2).
- **Enforces context** — validation is the point at which context becomes a
  hard boundary (§1.4); an instance that does not match its schema-in-context is
  refused.

7.6.2. Schema is how *"the fabric is structured"* stops being an aspiration and
becomes executable: the structure is not merely described, it is **declared in a
schema and enforced by validation**. In Agent DID this is realized as JSON
Schema, the Agent ID record format, and JSON-LD `@context` — the shared,
federated schemas through which parties agree on what terms mean (§3).

7.6.3. A schema is itself **derived, not decreed** (§2, §3): it is a ratified
derivation of meaning, carries provenance, is versioned, and may be re-derived
and contested. A schema is the constitution made checkable.

7.6.4. **Schemaless is acceptable; structureless is not.** Structure (§7) is the
*invariant*; a fixed, predeclared schema is one powerful way to express it, but
not the only one. A system may be **schemaless** — structure carried implicitly,
late-bound, derived on read, or graph-shaped (§9, graph/DAG mode) — and remain
fully governable, so long as its structure is present and discoverable.
**Structureless**, by contrast, is forbidden: work or data with no shape, no
relations, and no constraints cannot be defined, enforced, governed, or reasoned
about. Just as the fabric is *seamless but not structureless* (§9.1), it may be
*schemaless but never structureless*.

### 7.7. Structure Provides Slots; the Fabric Fills the Gaps with Boxes

7.7.1. Structure is, in part, **empty by design.** It provides *slots* — defined
places, with known shapes and relations, waiting to be filled. An empty structure
is not idle; it is a frame of **gaps**, each gap carrying the context and
constraints of what may occupy it.

7.7.2. **The fabric fills the gaps with boxes.** A *box* — a container of a real
or digital thing (§8.4) — is placed into a slot whose context defines what
belongs there. Filling a slot is an act of construction (§4): the box MUST match
the slot's schema and constraints (§7.6), or it is refused (§7.5). The fabric is
the medium that performs this placing, and that keeps every filled slot coherent
with every other (§5.3).

7.7.3. Structure and content are therefore **inseparable**: the structure says
*where* and *what shape*; the boxes supply *what*; the fabric performs the
*placing*. Meaning is enforced at the slot — a box means something only in the
context of the slot it fills (§1). An empty structure defines the space of
possible work; the boxes are the work made actual.

7.7.4. The filled slots are **durable** (§6.2): once a box is placed and ratified
into its slot, the filling persists and survives failure. The structure together
with its boxes is the **durable record of work** — what was placed, where, by
whom, and on what derivation (provenance, §3.1) — which is precisely what makes
the work measurable and governable (§6.3–§6.4) over time.

---

## 8. The Elements of Work

Once **construction** is named as the real work, everything else it composes
collapses into a small set of kinds. Nothing in the system is outside this.

8.1. **Direction** — shapes the work, but is *not* the work:
- **Strategy** — the *why* and the *which*: direction, intent, chosen approach.
- **Planning** — the *how* and the *when*: decomposition, sequencing, allocation.

8.2. **Elements** — the means construction composes:
- **Command** — the directive that triggers a step (a delegation, an
  authorization, a grant).
- **Tool** — the instrument wielded (capabilities, APIs, MCP tools).
- **Ingredient** — the thing acted upon: the **box** and its contents. A box
  may hold a **real-world thing** *or* **digital work** (data, concepts, code).
- **Labour** — the effort actually spent (the agent's or human's execution;
  compute).

8.3. A **plan unbuilt is nothing; a strategy unexecuted is nothing.** Direction
and elements alike exist to **serve construction**. The real work is where the
plan meets the thing and something gets made.

### 8.4. Real and Digital Work are Woven

8.4.1. The thing a box holds is of two kinds, and the fabric governs **both**:
- **Real** — physical, real-world things and the work that acts on them. *Only
  real things are governed in the real world*; what is permitted there is
  bounded by physics, resources, and law (§7.3, real-world constraints).
- **Digital** — data, concepts, and code, and the work that constructs them.

8.4.2. **Concepts are imported into a virtual box.** Every concept the system
reasons about is brought into a *sandbox* — a virtual box — where it is given a
definition, a context, and constraints, and where digital work on it can be done
safely and observably before it touches the real world.

8.4.3. **Real and digital are woven together**, not separated. Real work and
digital work are two faces of the same construction (the **hybrid** mode, §9.1):
digital work models, plans, and governs; real work acts and produces value; and
the fabric keeps them in correspondence so that what is true in the virtual box
stays accountable to what is real outside it. The seam between them MUST itself
be governed — context is enforced (§1.4) at the boundary where digital decisions
become real-world actions.

---

## 9. Operating Modes — How the Fabric Runs

9.1. The fabric is an **operating system for work** (§5), and like any OS it MUST
run in **multiple modes at once**. These are not optional features bolted on —
they are the conditions under which real work (§6) is possible *at scale*. The
fabric is, by necessity:

| Mode | Meaning | Anchored in |
|---|---|---|
| **Multi-mode** | runs several modes of operation concurrently; never a single fixed mode | this section |
| **Multi-tenant** | many principals / organizations share the fabric under strict isolation; no tenant observes or touches another's work | §1.4 context enforcement |
| **Multi-threaded** | many constructions proceed concurrently; work is parallel, not serial | §4 construction |
| **Graph / DAG-structured** | work is organized as a graph — a DAG of tasks, dependencies, and delegations; orchestration follows the graph | `design-principles.md` §4 (identity is a graph) |
| **Hybrid** | spans human + agent, sync + async, cloud + on-prem, centralized + decentralized — no single posture is assumed | §3.4 federated |
| **Multi-environment** | operates consistently across environments (dev / staging / prod, multiple clouds, edge) | §6.1 continuous |
| **Stateless** | the control plane holds no sticky session state; state lives in durable stores, so any mode scales horizontally and safely | `design-principles.md` §2 |
| **Seamless** | transitions across modes, tenants, and environments are invisible to the agent; the fabric hides the seams — but **seamless is not structureless**: it hides the *seams*, never the *structure* (§7) | §6 the five guarantees |

9.2. **The constitution holds in every mode.** Modes change *how* work runs —
never *whether* it is governed. In all modes: context is enforced (§1.4),
constraints apply (§7), meaning stays derived and contestable (§3), and failure
is explicit (§7.5). A mode is a way of *running* the instruction set, never a way
of *escaping* it.

### 9.3. Runtime Substrate — the Full Compute Spectrum

9.3.1. As an OS for work, the fabric MUST run across the **full compute
spectrum**, presenting one stable behavior at every point:

| Substrate | Role |
|---|---|
| **Realtime kernel** | a native, low-latency core for time-critical work |
| **Native runtime / core** | runs directly on the host, closest to the metal |
| **Container** | packaged, portable, isolated units of work |
| **Edge** | close to where the real-world things are (§8.4) |
| **Cloud** | elastic, centralized scale |

9.3.2. **Stable state across the spectrum.** The fabric holds the *same*
instruction set, the *same* governance, and the *same* enforced context (§1.4)
whether it runs at the kernel, in a container, at the edge, or in the cloud. This
is the substrate dimension of the **multi-environment** and **hybrid** modes
(§9.1): *framework is the fabric of work* — the structure stays constant; only
the substrate changes. Work may move along the spectrum (e.g., from cloud
planning to edge execution) without losing its meaning, provenance, or
constraints.

---

## 10. The Whole Edifice

```
   box (real OR digital thing)  ──▶  meaning defined & derived in context  (§1–§2)
        │
   CONSTITUTION  — keeps meaning derived, provenanced, contestable;
                   right to reason · goodwill & wisdom prevail      (§3)
        │
   FABRIC = the structured instruction set / OS for work
            define · do · develop · manage real-world work;
            framework provides STRUCTURE (affordance + constraint); (§5, §7)
            continuous · durable · measurable · governable · value  (§6)
            modes: multi-tenant · multi-threaded · graph · hybrid ·
                   multi-env · stateless · seamless                 (§9)
        │
   CONSTRUCTION  — the real work, woven into the fabric, on the box;
                   real + digital work woven together               (§4, §8.4)
        │
   DIRECTION  — strategy · planning                                 (§8.1)
   ELEMENTS   — command · tool · ingredient · labour                (§8.2)
```

> *Framework is the fabric of work. The framework provides the structure. The
> structure both affords and constrains. The construction is the real work. And
> the constitution exists so that goodwill and wisdom may prevail.*

---

## 11. Binding Clause

11.1. This instruction set is itself subject to the procedure it defines (§3): it
is **derived, not decreed**, and may be re-derived, contested with better logic,
and amended through reasoned, federated governance.

11.2. The technical principles in [`design-principles.md`](./design-principles.md)
are **statutes derived under this constitution**. Where a statute and this
document conflict in *spirit*, the conflict MUST be resolved by re-derivation
under §3 — not by decree.
