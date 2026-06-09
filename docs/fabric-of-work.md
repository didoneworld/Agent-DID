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
- **Ingredient** — the real-world thing acted upon (the **box** and its
  contents; data, resources).
- **Labour** — the effort actually spent (the agent's or human's execution;
  compute).

8.3. A **plan unbuilt is nothing; a strategy unexecuted is nothing.** Direction
and elements alike exist to **serve construction**. The real work is where the
plan meets the real-world thing and something gets made.

---

## 9. The Whole Edifice

```
   box  ──▶  meaning defined & derived in context                 (§1–§2)
        │
   CONSTITUTION  — keeps meaning derived, provenanced, contestable;
                   right to reason · goodwill & wisdom prevail      (§3)
        │
   FABRIC = the structured instruction set / OS for work
            define · do · develop · manage real-world work;
            framework provides STRUCTURE (affordance + constraint); (§5, §7)
            continuous · durable · measurable · governable · value  (§6)
        │
   CONSTRUCTION  — the real work, woven into the fabric, on the box (§4)
        │
   DIRECTION  — strategy · planning                                 (§8.1)
   ELEMENTS   — command · tool · ingredient · labour                (§8.2)
```

> *Framework is the fabric of work. The framework provides the structure. The
> structure both affords and constrains. The construction is the real work. And
> the constitution exists so that goodwill and wisdom may prevail.*

---

## 10. Binding Clause

10.1. This instruction set is itself subject to the procedure it defines (§3): it
is **derived, not decreed**, and may be re-derived, contested with better logic,
and amended through reasoned, federated governance.

10.2. The technical principles in [`design-principles.md`](./design-principles.md)
are **statutes derived under this constitution**. Where a statute and this
document conflict in *spirit*, the conflict MUST be resolved by re-derivation
under §3 — not by decree.
