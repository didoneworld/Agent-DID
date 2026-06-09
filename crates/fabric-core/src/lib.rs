//! fabric-core — the Enterprise Agent OS composite core, in Rust.
//!
//! Everything is a [`BoxNode`] (a node) carrying *data-in-context*. The metamodel
//! (kinds, relations) lives in the same graph as boxes, terminating in a
//! self-typed fixpoint (`kind:kind`). A system is **real** if every reference
//! resolves (node) and **stable** if every box is typed, filled, and placed
//! (box). Mirrors `scripts/fabric_model.py`; aligns with the Rust + SurrealQL
//! stack used by AGenNext/Agent-Bench.

use std::collections::{HashMap, HashSet, VecDeque};

/// A universal node: data-in-context, with provenance/validity.
#[derive(Clone, Debug, Default)]
pub struct BoxNode {
    pub id: String,
    /// id of a box whose `kind == "kind"` (a class).
    pub kind: String,
    /// the context-slot this box is placed in.
    pub ctx: Option<String>,
    /// part of the metamodel (kinds/relations) vs. data.
    pub meta: bool,
    pub payload: HashMap<String, String>,
    /// bi-temporal validity (Graphiti/Zep style); `None` = open.
    pub valid_from: Option<i64>,
    pub valid_to: Option<i64>,
}

impl BoxNode {
    pub fn valid_at(&self, t: i64) -> bool {
        self.valid_from.map_or(true, |f| f <= t) && self.valid_to.map_or(true, |to| t < to)
    }
}

/// Outcome of resolving the graph at node + box.
#[derive(Debug, Default)]
pub struct Resolution {
    pub dangling: Vec<String>,
    pub unstable: Vec<String>,
    pub unreachable: Vec<String>,
    pub node_real: bool,
    pub box_stable: bool,
    pub valid: bool,
}

/// A graph of boxes and typed relation edges.
#[derive(Default)]
pub struct Graph {
    pub boxes: HashMap<String, BoxNode>,
    /// (src, relation_id, dst); the relation_id must be a `kind == "relation"` box.
    pub edges: Vec<(String, String, String)>,
}

impl Graph {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn add(&mut self, id: &str, kind: &str, ctx: Option<&str>, meta: bool) {
        self.boxes.insert(
            id.to_string(),
            BoxNode {
                id: id.to_string(),
                kind: kind.to_string(),
                ctx: ctx.map(str::to_string),
                meta,
                ..Default::default()
            },
        );
    }

    pub fn add_data(&mut self, id: &str, kind: &str, ctx: Option<&str>, payload: &[(&str, &str)]) {
        self.add(id, kind, ctx, false);
        if let Some(b) = self.boxes.get_mut(id) {
            for (k, v) in payload {
                b.payload.insert(k.to_string(), v.to_string());
            }
        }
    }

    pub fn relate(&mut self, src: &str, rel: &str, dst: &str) {
        self.edges
            .push((src.to_string(), rel.to_string(), dst.to_string()));
    }

    /// Bi-temporal query: ids valid at time `t` (what was true at `t`).
    pub fn as_of(&self, t: i64) -> HashSet<String> {
        self.boxes
            .values()
            .filter(|b| b.valid_at(t))
            .map(|b| b.id.clone())
            .collect()
    }

    fn is_kind(&self, k: &str) -> bool {
        self.boxes.get(k).is_some_and(|b| b.kind == "kind")
    }
    fn is_relation(&self, r: &str) -> bool {
        self.boxes.get(r).is_some_and(|b| b.kind == "relation")
    }

    /// Resolve the graph at node (real) and box (stable).
    pub fn resolve(&self) -> Resolution {
        let mut dangling = Vec::new();

        // children-by-context (a slot filled by boxes is "filled")
        let mut children: HashMap<&str, usize> = HashMap::new();
        for b in self.boxes.values() {
            if let Some(c) = &b.ctx {
                *children.entry(c.as_str()).or_default() += 1;
            }
        }

        // NODE: typing + context references resolve
        for b in self.boxes.values() {
            if !self.boxes.contains_key(&b.kind) {
                dangling.push(format!("type {}->{} (missing)", b.id, b.kind));
            } else if !self.is_kind(&b.kind) {
                dangling.push(format!("type {}->{} (not a kind)", b.id, b.kind));
            }
            if let Some(c) = &b.ctx {
                if !self.boxes.contains_key(c) {
                    dangling.push(format!("ctx {}->{} (missing)", b.id, c));
                }
            }
        }
        // NODE: edges resolve and are related by relation-boxes
        for (s, rel, d) in &self.edges {
            if !self.boxes.contains_key(s) {
                dangling.push(format!("edge src {s} missing"));
            }
            if !self.boxes.contains_key(d) {
                dangling.push(format!("edge dst {d} missing"));
            }
            if !self.boxes.contains_key(rel) {
                dangling.push(format!("edge rel {rel} missing"));
            } else if !self.is_relation(rel) {
                dangling.push(format!("edge rel {rel} not a relation"));
            }
        }

        // BOX: typed + filled + placed
        let mut unstable = Vec::new();
        for b in self.boxes.values() {
            let typed = self.is_kind(&b.kind);
            let filled = !b.payload.is_empty()
                || b.kind == "kind"
                || b.kind == "relation"
                || b.meta
                || children.get(b.id.as_str()).copied().unwrap_or(0) > 0;
            let placed = match &b.ctx {
                Some(c) => self.boxes.contains_key(c),
                None => b.id == "kind",
            };
            if !(typed && filled && placed) {
                let mut miss = Vec::new();
                if !typed {
                    miss.push("typed");
                }
                if !filled {
                    miss.push("filled");
                }
                if !placed {
                    miss.push("placed");
                }
                unstable.push(format!("{} [{}]", b.id, miss.join(",")));
            }
        }

        // connectivity: every box reachable from the fixpoint "kind"
        let mut adj: HashMap<&str, HashSet<&str>> = HashMap::new();
        for b in self.boxes.values() {
            if self.boxes.contains_key(&b.kind) {
                adj.entry(b.kind.as_str()).or_default().insert(b.id.as_str());
            }
            if let Some(c) = &b.ctx {
                if self.boxes.contains_key(c) {
                    adj.entry(c.as_str()).or_default().insert(b.id.as_str());
                }
            }
        }
        for (s, rel, d) in &self.edges {
            if self.boxes.contains_key(s) && self.boxes.contains_key(d) {
                adj.entry(s.as_str()).or_default().insert(d.as_str());
                adj.entry(d.as_str()).or_default().insert(s.as_str());
            }
            if self.boxes.contains_key(rel) && self.boxes.contains_key(s) {
                adj.entry(rel.as_str()).or_default().insert(s.as_str());
            }
        }
        let mut seen: HashSet<&str> = HashSet::new();
        let mut q: VecDeque<&str> = VecDeque::new();
        if self.boxes.contains_key("kind") {
            q.push_back("kind");
        }
        while let Some(n) = q.pop_front() {
            if !seen.insert(n) {
                continue;
            }
            if let Some(ns) = adj.get(n) {
                for m in ns {
                    if !seen.contains(m) {
                        q.push_back(m);
                    }
                }
            }
        }
        let unreachable: Vec<String> = self
            .boxes
            .keys()
            .filter(|k| !seen.contains(k.as_str()))
            .cloned()
            .collect();

        let node_real = dangling.is_empty();
        let box_stable = unstable.is_empty() && unreachable.is_empty();
        Resolution {
            dangling,
            unstable,
            unreachable,
            node_real,
            box_stable,
            valid: node_real && box_stable,
        }
    }
}

/// The self-describing stable-state kernel (the model is the graph).
pub fn kernel() -> Graph {
    let mut g = Graph::new();
    g.add("kind", "kind", None, true); // self-typed fixpoint
    for k in ["relation", "schema", "context"] {
        g.add(k, "kind", Some("kind"), true);
    }
    g
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn kernel_resolves() {
        assert!(kernel().resolve().valid);
    }

    #[test]
    fn self_describing_model_resolves() {
        let mut g = kernel();
        for r in ["contains", "derives", "instance_of"] {
            g.add(r, "relation", Some("kind"), true);
        }
        for k in ["agent", "construction", "ingredient"] {
            g.add(k, "kind", Some("kind"), true);
        }
        g.add_data("ctx:onb", "context", Some("kind"), &[("name", "onboarding")]);
        g.add_data("agent:alice", "agent", Some("ctx:onb"), &[("did", "did:x:alice")]);
        g.add_data("work:c1", "construction", Some("ctx:onb"), &[("result", "ok")]);
        g.relate("work:c1", "derives", "agent:alice");
        let r = g.resolve();
        assert!(r.valid, "{r:?}");
        assert!(g.boxes.values().all(|b| g.boxes.contains_key(&b.kind)));
    }

    #[test]
    fn dangling_reference_fails() {
        let mut g = kernel();
        g.add_data("rec", "missing_kind", Some("kind"), &[("a", "b")]);
        assert!(!g.resolve().valid);
    }

    #[test]
    fn enterprise_model_resolves() {
        // Okta-style: User/Group -> kinds; org -> context; member_of -> relation.
        let mut g = kernel();
        g.add("member_of", "relation", Some("kind"), true);
        g.add("okta.User", "kind", Some("kind"), true);
        g.add("okta.Group", "kind", Some("kind"), true);
        g.add_data("org", "context", Some("kind"), &[("org", "acme")]);
        g.add_data("user.jane", "okta.User", Some("org"), &[("login", "jane")]);
        g.add_data("group.admins", "okta.Group", Some("org"), &[("name", "admins")]);
        g.relate("user.jane", "member_of", "group.admins");
        assert!(g.resolve().valid);
    }

    #[test]
    fn bitemporal_as_of() {
        let mut g = kernel();
        g.add("fact", "kind", Some("kind"), true);
        let mut a = BoxNode {
            id: "owner@alice".into(),
            kind: "fact".into(),
            ctx: Some("kind".into()),
            valid_from: Some(0),
            valid_to: Some(10),
            ..Default::default()
        };
        a.payload.insert("owner".into(), "alice".into());
        let b = BoxNode {
            id: "owner@bob".into(),
            kind: "fact".into(),
            ctx: Some("kind".into()),
            valid_from: Some(10),
            ..Default::default()
        };
        g.boxes.insert(a.id.clone(), a);
        g.boxes.insert(b.id.clone(), b);
        assert!(g.as_of(5).contains("owner@alice"));
        assert!(g.as_of(15).contains("owner@bob"));
        assert!(!g.as_of(15).contains("owner@alice"));
    }
}
