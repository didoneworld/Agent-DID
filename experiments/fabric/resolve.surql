-- =====================================================================
-- In-database resolution: the constitution checks itself inside its backend.
-- node -> real  : every box's declared kind resolves to a kind-box; contexts
--                 resolve; relation-edge endpoints cannot dangle (RELATION tables).
-- box  -> stable: every box is typed + placed + filled.
-- Target: SurrealDB >= 2.x. Logic mirrors scripts/fabric_graph.py / fabric_model.py.
-- =====================================================================
USE NS fabric DB sandbox;

-- record ids of all kind-boxes (boxes whose kind = 'kind')
LET $kinds = (SELECT VALUE id FROM box WHERE kind = 'kind');

-- NODE resolution: a box whose declared kind has no defining kind-box is dangling
LET $dangling = (
    SELECT id, kind FROM box
    WHERE type::thing('box', kind) NOT IN $kinds
);

-- BOX resolution: unstable = not typed OR not placed OR not filled
LET $unstable = (
    SELECT id FROM box
    WHERE (type::thing('box', kind) NOT IN $kinds)               -- not typed
       OR (ctx = NONE AND id != box:kind)                        -- not placed (root excepted)
       OR (payload = NONE AND meta = false)                      -- not filled (data boxes need content)
);

RETURN {
    boxes:      (SELECT VALUE count() FROM box GROUP ALL)[0] ?? 0,
    kinds:      array::len($kinds),
    dangling:   $dangling,
    unstable:   $unstable,
    node_real:  array::len($dangling) = 0,
    box_stable: array::len($unstable) = 0,
    valid:      array::len($dangling) = 0 AND array::len($unstable) = 0
};
