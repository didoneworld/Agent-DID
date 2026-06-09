#!/usr/bin/env python3
"""Enterprise data-model test — Adobe XDM, Salesforce, Okta on the fabric.

Validates that enterprise schema standards map onto the kernel and resolve at
node + box. The mapping is universal:

  class / object / resource type  -> kind  (a box of kind 'kind')   ("kind = class")
  field group / field set / mixin -> schema box (reusable, composed in)
  org / namespace / tenant        -> context (group)
  record / instance               -> a box typed by the class kind, in a context
  relationship (lookup, member-of)-> relation edge

The same pattern covers FHIR, FIBO, schema.org, SCIM, etc. — one kernel, every
enterprise model.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fabric_model import Graph  # noqa: E402


def kernel(*relations: str) -> Graph:
    g = Graph()
    g.box("kind", kind="kind", meta=True)              # self-typed fixpoint
    for k in ("relation", "schema", "context"):
        g.box(k, kind="kind", ctx="kind", meta=True)
    for r in relations:
        g.box(r, kind="relation", ctx="kind", meta=True)
    return g


def xdm() -> Graph:
    g = kernel("subclass_of", "composed_of", "identity")
    for c in ("xdm.IndividualProfile", "xdm.ExperienceEvent"):
        g.box(c, kind="kind", ctx="kind", meta=True)               # class -> kind
    for fg in ("fg.DemographicDetails", "fg.PersonalContact", "fg.Commerce"):
        g.box(fg, kind="schema", ctx="kind", meta=True)            # field group -> schema
    g.box("schema.LoyaltyMember", kind="kind", ctx="kind", meta=True)
    g.relate("schema.LoyaltyMember", "subclass_of", "xdm.IndividualProfile")
    g.relate("schema.LoyaltyMember", "composed_of", "fg.DemographicDetails")
    g.relate("schema.LoyaltyMember", "composed_of", "fg.PersonalContact")
    g.box("ns.CRM", kind="context", ctx="kind", payload={"ns": "CRM"})
    g.box("rec.jane", kind="schema.LoyaltyMember", ctx="ns.CRM",
          payload={"email": "jane@example.com"})
    return g


def salesforce() -> Graph:
    g = kernel("lookup", "master_detail", "composed_of")
    for o in ("sf.Account", "sf.Contact", "sf.Opportunity"):
        g.box(o, kind="kind", ctx="kind", meta=True)               # sObject -> kind
    for fs in ("fs.AccountAddress", "fs.ContactInfo"):
        g.box(fs, kind="schema", ctx="kind", meta=True)            # field set -> schema
    g.relate("sf.Account", "composed_of", "fs.AccountAddress")
    g.relate("sf.Contact", "composed_of", "fs.ContactInfo")
    g.box("org.Acme", kind="context", ctx="kind", payload={"org": "Acme"})
    g.box("acct.acme", kind="sf.Account", ctx="org.Acme", payload={"name": "Acme"})
    g.box("contact.jane", kind="sf.Contact", ctx="org.Acme", payload={"name": "Jane"})
    g.box("opp.deal", kind="sf.Opportunity", ctx="org.Acme", payload={"amount": 5000})
    g.relate("contact.jane", "lookup", "acct.acme")
    g.relate("opp.deal", "master_detail", "acct.acme")
    return g


def okta() -> Graph:
    g = kernel("member_of", "assigned_to", "composed_of")
    for c in ("okta.User", "okta.Group", "okta.App"):
        g.box(c, kind="kind", ctx="kind", meta=True)               # resource -> kind
    for ps in ("profile.Base", "profile.CustomAttrs"):
        g.box(ps, kind="schema", ctx="kind", meta=True)            # profile schema -> schema
    g.relate("okta.User", "composed_of", "profile.Base")
    g.relate("okta.User", "composed_of", "profile.CustomAttrs")
    g.box("org.AcmeOkta", kind="context", ctx="kind", payload={"org": "acme.okta.com"})
    g.box("user.jane", kind="okta.User", ctx="org.AcmeOkta", payload={"login": "jane"})
    g.box("group.admins", kind="okta.Group", ctx="org.AcmeOkta", payload={"name": "admins"})
    g.box("app.sf", kind="okta.App", ctx="org.AcmeOkta", payload={"label": "Salesforce"})
    g.relate("user.jane", "member_of", "group.admins")
    g.relate("user.jane", "assigned_to", "app.sf")
    return g


def main() -> int:
    print("=" * 64)
    print("ENTERPRISE DATA MODEL TEST — XDM · Salesforce · Okta on the fabric")
    print("=" * 64)
    all_ok = True
    for name, fn in (("Adobe XDM", xdm), ("Salesforce", salesforce), ("Okta", okta)):
        g = fn()
        r = g.resolve()
        ok = r["valid"]
        all_ok &= ok
        print(f"{name:<14} boxes={len(g.boxes):>3} edges={len(g.edges):>2}  "
              f"NODE={'real' if r['node_real'] else 'UNREAL'}  "
              f"BOX={'stable' if r['box_stable'] else 'UNSTABLE'}  "
              f"-> {'VALID' if ok else 'INVALID'}")
        for d in r["dangling"]:
            print("    dangling:", d)
        for u in r["unstable"] + r["unreachable"]:
            print("    unstable/unreachable:", u)
    print("-" * 64)
    print("mapping: class/object->kind · field group/set->schema · namespace->context")
    print("same kernel covers FHIR, FIBO, schema.org, SCIM, ...")
    print("=" * 64)
    print(f"ENTERPRISE MODELS ON FABRIC : {'ALL VALID (real + stable)' if all_ok else 'INVALID'}")
    print("=" * 64)
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
