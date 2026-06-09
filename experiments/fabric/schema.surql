-- =====================================================================
-- Fabric backend schema  —  SurrealDB is the BUILDING BASE / BACKEND (BE + DB),
-- NOT the runtime. The runtime (the fabric / OS for work, fabric-of-work.md §5,
-- §9.3) executes ABOVE this store. State lives here; the control plane stays
-- stateless (design-principles.md §2).
--
-- The model is the graph (fabric-substrate.md §6): kinds and relations are
-- themselves boxes, typed by boxes, bottoming out in a self-typed fixpoint
-- (kind:kind). Schemafull envelope + flexible payload = schemaless-but-never-
-- structureless (§7.6.4).
-- Target: SurrealDB >= 2.x
-- =====================================================================

DEFINE NAMESPACE IF NOT EXISTS fabric;
USE NS fabric;
DEFINE DATABASE IF NOT EXISTS sandbox;       -- one sandbox = one experimentation env (§8.4.2)
USE NS fabric DB sandbox;

-- ---- context = group / scope (§1, §10.4; kind=class, context=group) --------
DEFINE TABLE context TYPE NORMAL SCHEMAFULL;
DEFINE FIELD name   ON context TYPE string;
DEFINE FIELD parent ON context TYPE option<record<context>>;

-- ---- box = the universal node (SCHEMAFULL envelope, FLEXIBLE payload) -------
DEFINE TABLE box TYPE NORMAL SCHEMAFULL;
DEFINE FIELD kind       ON box TYPE string;                 -- id-name of a box whose kind = 'kind'
DEFINE FIELD ctx        ON box TYPE option<record<box | context>>;  -- the slot it is placed in (§7.7)
DEFINE FIELD realm      ON box TYPE string
    ASSERT $value IN ['real', 'digital'] DEFAULT 'digital';  -- §8.4
DEFINE FIELD state      ON box TYPE string
    ASSERT $value IN ['proposed', 'ratified', 'stable', 'revoked'] DEFAULT 'proposed';  -- §3.3
DEFINE FIELD value      ON box FLEXIBLE TYPE option<any>;    -- asset value as a data point (§10.2)
DEFINE FIELD provenance ON box FLEXIBLE TYPE option<object>; -- §3.1
DEFINE FIELD payload    ON box FLEXIBLE TYPE option<object>; -- schemaless content (§7.6.4)
DEFINE FIELD meta       ON box TYPE bool DEFAULT false;      -- part of the model (metamodel) vs data
DEFINE INDEX box_kind   ON box FIELDS kind;
DEFINE INDEX box_ctx    ON box FIELDS ctx;

-- ---- relations as RELATION edge tables (each mirrors a kind='relation' box) -
-- RELATION tables enforce referential integrity: IN/OUT must be existing boxes,
-- so edge endpoints can never dangle (node-real by construction at the edges).
DEFINE TABLE contains    TYPE RELATION IN box OUT box;       -- containment / slot fill (§7.7)
DEFINE TABLE refs        TYPE RELATION IN box OUT box;       -- cross-reference
DEFINE TABLE derives     TYPE RELATION IN box OUT box;       -- derivation lineage (§2, §3.1)
DEFINE TABLE fills       TYPE RELATION IN box OUT box | context;  -- placed into a context (§7.7)
DEFINE TABLE commands    TYPE RELATION IN box OUT box;       -- a command (§8.2)
DEFINE TABLE performs    TYPE RELATION IN box OUT box;       -- labour (§8.2)
DEFINE TABLE instance_of TYPE RELATION IN box OUT box;       -- typing edge (box -> its kind-box)
