-- =====================================================================
-- Seed the stable-state kernel + a sample construction into the backend.
-- Mirrors scripts/fabric_model.py (the model is the graph). Run after schema.surql.
-- =====================================================================
USE NS fabric DB sandbox;

-- ---- the metamodel, AS BOXES (the model is in the graph) --------------------
-- self-typed fixpoint: a kind is a kind
CREATE box:kind        SET kind = 'kind', meta = true;
CREATE box:relation    SET kind = 'kind', ctx = box:kind, meta = true;
CREATE box:schema      SET kind = 'kind', ctx = box:kind, meta = true;
CREATE box:box         SET kind = 'kind', ctx = box:kind, meta = true;

-- domain kinds (§8) — each a box typed by 'kind'
CREATE box:context     SET kind = 'kind', ctx = box:kind, meta = true;
CREATE box:command     SET kind = 'kind', ctx = box:kind, meta = true;
CREATE box:tool        SET kind = 'kind', ctx = box:kind, meta = true;
CREATE box:ingredient  SET kind = 'kind', ctx = box:kind, meta = true;
CREATE box:labour      SET kind = 'kind', ctx = box:kind, meta = true;
CREATE box:construction SET kind = 'kind', ctx = box:kind, meta = true;
CREATE box:strategy    SET kind = 'kind', ctx = box:kind, meta = true;
CREATE box:planning    SET kind = 'kind', ctx = box:kind, meta = true;
CREATE box:agent       SET kind = 'kind', ctx = box:kind, meta = true;

-- relation kinds (§ data-model edges) — each a box typed by 'relation'
CREATE box:r_contains    SET kind = 'relation', ctx = box:kind, meta = true;
CREATE box:r_refs        SET kind = 'relation', ctx = box:kind, meta = true;
CREATE box:r_derives     SET kind = 'relation', ctx = box:kind, meta = true;
CREATE box:r_fills       SET kind = 'relation', ctx = box:kind, meta = true;
CREATE box:r_commands    SET kind = 'relation', ctx = box:kind, meta = true;
CREATE box:r_performs    SET kind = 'relation', ctx = box:kind, meta = true;
CREATE box:r_instance_of SET kind = 'relation', ctx = box:kind, meta = true;

-- ---- data, in the SAME graph -----------------------------------------------
CREATE context:onboarding SET name = 'onboarding';
CREATE box:alice    SET kind = 'agent',        ctx = context:onboarding,
    realm = 'digital', state = 'stable', value = 1,
    payload = { did: 'did:example:alice' };
CREATE box:provision SET kind = 'command',     ctx = context:onboarding,
    payload = { action: 'provision' };
CREATE box:scim     SET kind = 'tool',         ctx = context:onboarding,
    payload = { api: 'scim' };
CREATE box:box42    SET kind = 'ingredient',   ctx = context:onboarding,
    realm = 'digital', value = 42, payload = { note: 'a box holds a thing' };
CREATE box:c1       SET kind = 'construction',  ctx = context:onboarding,
    state = 'stable', payload = { result: 'agent provisioned' };

-- ---- edges (each mirrors a relation-box -> the model is the graph) ----------
RELATE box:alice->commands->box:provision;
RELATE box:provision->refs->box:scim;
RELATE box:c1->contains->box:box42;
RELATE box:alice->performs->box:c1;
RELATE box:c1->derives->box:provision;
RELATE box:box42->fills->context:onboarding;
