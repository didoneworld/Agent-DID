# Enterprise Data Models on the Fabric

> Derived, contestable. Validates that enterprise schema standards map onto the
> kernel (`box · kind · relation · context`) and **resolve at node + box**.
> Implemented and run in `scripts/fabric_enterprise.py`.

## Universal mapping

Every enterprise data model uses the same handful of ideas; each maps to one
kernel primitive:

| Enterprise concept | Kernel primitive |
|---|---|
| class / object / resource type | **kind** ("kind = class") |
| field group / field set / mixin / profile | **schema** box (reusable, composed in) |
| org / namespace / tenant | **context** (group) |
| record / instance | **box** typed by the class kind, in a context |
| relationship (lookup, member-of, identity) | **relation** edge |

Because the mapping is mechanical, the model is **engine- and standard-neutral**:
the same kernel hosts any of them, and a model is *valid on the fabric* iff it
resolves at node + box.

## Validated (run `scripts/fabric_enterprise.py`)

| Model | Maps | Result |
|---|---|---|
| **Adobe XDM** | classes (Individual Profile, ExperienceEvent) → kinds; field groups → schema; identity namespace → context; composed schemas → kinds | 15 boxes, **VALID** |
| **Salesforce** | sObjects (Account, Contact, Opportunity) → kinds; field sets → schema; org → context; lookup / master-detail → relations | 16 boxes, **VALID** |
| **Okta** | User / Group / App → kinds; user-profile schemas → schema; org → context; member-of / assigned-to → relations | 16 boxes, **VALID** |

**ALL VALID (real + stable).** Okta is especially apt: Agent DID is itself an
identity system, and Okta's Universal Directory (users, groups, apps, profiles,
SCIM) maps directly onto boxes-in-context — consistent with the repo's existing
SCIM `AgenticIdentity` work.

## Why this matters

- **Adoption without migration of meaning.** An enterprise can bring its existing
  XDM / Salesforce / Okta schema onto the fabric unchanged — classes become kinds,
  records become boxes — and immediately gain resolution, provenance, trust
  scoring, temporal validity, and federation.
- **One model, many standards.** FHIR (healthcare), FIBO (finance), schema.org,
  and SCIM follow the same pattern (class → kind, mixin → schema, namespace →
  context). The kernel does not change per standard (§6.4); only the kinds and
  relations differ.
- **Interop by resolution.** Cross-model links (e.g., an Okta `User` ↔ a
  Salesforce `Contact` ↔ an XDM profile) are just relation edges that must
  resolve — identity stitching becomes a graph-resolution problem, not an ETL one.
