-- =====================================================================
-- Real-time box streaming on the backend (LIVE SELECT / change feeds, §6.1).
-- Each create/update/delete on a matching box pushes a notification to the
-- subscribed connection. Maps to scripts/fabric_model.py Graph.subscribe().
-- Target: SurrealDB >= 2.x.
-- =====================================================================
USE NS fabric DB sandbox;

-- stream boxes as they arrive in a context, filtered by kind
LIVE SELECT * FROM box
    WHERE ctx = context:onboarding
      AND kind IN ['command', 'ingredient'];

-- stream promotions (digital -> real, §8.4.3) as they happen
LIVE SELECT id, kind, realm, state FROM box WHERE realm = 'real';

-- durable, replayable stream: define a change feed on the table
-- DEFINE TABLE box CHANGEFEED 1d;
-- SHOW CHANGES FOR TABLE box SINCE <versionstamp>;
