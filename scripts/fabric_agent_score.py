#!/usr/bin/env python3
"""Agent scorecard — Trust, Reliability, Usability, and a composite Agent GPA.

In the fabric an agent is a box; its memory, constructions, and provenance are
boxes and edges in the graph (fabric-of-work.md §10). So an agent's quality is
not opinion — it is **computed from resolvable, provenance-bearing data**:

  * Trust score  : share of the agent's memory that is ratified + resolved +
                   provenance-bearing (§3.1, §3.3). Drift-resistance.
  * Reliability  : share of constructions that resolved (real + stable) rather
                   than being refused / drifting (§7.5).
  * Usability    : trusted recall at real-time latency — does it return the right
                   answer fast (recall x responsiveness)? (the "most important
                   number", §ai). Includes ingress/egress responsiveness.
  * Agent GPA    : weighted composite on a 0.0-4.0 scale, with a letter grade.

All three are in [0,1]; GPA weights trust highest because for agents trust is
the binding constraint.
"""
from __future__ import annotations

from dataclasses import dataclass, field

W_TRUST, W_RELIABILITY, W_USABILITY = 0.40, 0.35, 0.25  # sum = 1.0
TARGET_MS = 10.0  # real-time reaction budget (egress + retrieve)


@dataclass
class Agent:
    name: str
    mem_total: int
    mem_ratified_resolved: int       # ratified + resolved + provenance-bearing
    constructions: int
    constructions_resolved: int      # resolved real+stable (vs refused/drift)
    recall_at_k: float               # retrieval accuracy in [0,1]
    latency_ms: float                # trusted-recall latency (ingress->egress)
    ingress_exposure: float = 0.0    # network exposure in [0,1]; air-gapped = 0
    source_pinned: float = 1.0       # share of memory with pinned provenance source

    def trust(self) -> float:
        return self.mem_ratified_resolved / self.mem_total if self.mem_total else 0.0

    def reliability(self) -> float:
        return self.constructions_resolved / self.constructions if self.constructions else 0.0

    def responsiveness(self) -> float:
        return min(1.0, TARGET_MS / self.latency_ms) if self.latency_ms else 1.0

    def usability(self) -> float:
        return self.recall_at_k * self.responsiveness()

    def gpa(self) -> float:
        score = (W_TRUST * self.trust()
                 + W_RELIABILITY * self.reliability()
                 + W_USABILITY * self.usability())
        return round(4.0 * score, 2)

    # ---- risk & threat profile (lower risk is better) --------------------
    def risk(self) -> float:
        return round(0.35 * (1 - self.trust())
                     + 0.25 * (1 - self.reliability())
                     + 0.20 * self.ingress_exposure
                     + 0.20 * (1 - self.source_pinned), 3)

    def risk_level(self) -> str:
        r = self.risk()
        return ("Low" if r < 0.15 else "Moderate" if r < 0.35
                else "Elevated" if r < 0.60 else "High")

    def threats(self) -> list[str]:
        t = []
        if self.trust() < 0.85:
            t.append("memory poisoning / untrusted recall")
        if self.source_pinned < 0.85:
            t.append("unpinned provenance (drift)")
        if self.reliability() < 0.85:
            t.append("construction drift / instability")
        if self.ingress_exposure > 0.3:
            t.append("ingress exfiltration / tampering")
        if self.latency_ms > TARGET_MS:
            t.append("latency / real-time DoS")
        return t or ["none material"]


def grade(gpa: float) -> str:
    for cut, g in ((3.85, "A"), (3.5, "A-"), (3.15, "B+"), (2.85, "B"),
                   (2.5, "B-"), (2.15, "C+"), (1.85, "C"), (1.0, "D")):
        if gpa >= cut:
            return g
    return "F"


def main() -> int:
    agents = [
        Agent("alice (mature)",   mem_total=500, mem_ratified_resolved=485,
              constructions=120, constructions_resolved=117,
              recall_at_k=0.97, latency_ms=4.0,
              ingress_exposure=0.05, source_pinned=0.98),
        Agent("bob (drifting)",   mem_total=500, mem_ratified_resolved=300,
              constructions=120, constructions_resolved=78,
              recall_at_k=0.74, latency_ms=22.0,
              ingress_exposure=0.60, source_pinned=0.55),
        Agent("carol (new)",      mem_total=60,  mem_ratified_resolved=58,
              constructions=12,  constructions_resolved=12,
              recall_at_k=0.91, latency_ms=7.0,
              ingress_exposure=0.10, source_pinned=0.95),
    ]
    print("=" * 78)
    print("AGENT SCORECARD  —  Trust · Reliability · Usability · GPA")
    print("=" * 78)
    print(f"{'agent':<18}{'trust':>8}{'reliab':>8}{'usable':>8}"
          f"{'lat ms':>8}{'GPA':>7}  grade")
    print("-" * 78)
    for a in sorted(agents, key=lambda x: x.gpa(), reverse=True):
        print(f"{a.name:<18}{a.trust():>8.0%}{a.reliability():>8.0%}"
              f"{a.usability():>8.0%}{a.latency_ms:>8.1f}{a.gpa():>7.2f}"
              f"  {grade(a.gpa())}")
    print("-" * 78)
    print(f"weights: trust {W_TRUST:.0%} · reliability {W_RELIABILITY:.0%} · "
          f"usability {W_USABILITY:.0%}   real-time budget: {TARGET_MS:.0f} ms")
    print("trust is weighted highest: for agents it is the binding constraint;")
    print("low trust caps the GPA no matter how fast or accurate the agent is.")

    print("\n" + "=" * 78)
    print("AGENT RISK & THREAT PROFILE  (lower risk is better)")
    print("=" * 78)
    for a in sorted(agents, key=lambda x: x.risk()):
        print(f"{a.name:<18} risk={a.risk():.2f} [{a.risk_level()}]")
        print(f"    threats: {'; '.join(a.threats())}")
    print("-" * 78)
    print("risk = 0.35(1-trust) + 0.25(1-reliability) + 0.20 ingress_exposure"
          " + 0.20(1-source_pinned)")
    print("'pin sources': pinned provenance lowers risk and resists drift (§3.1).")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
