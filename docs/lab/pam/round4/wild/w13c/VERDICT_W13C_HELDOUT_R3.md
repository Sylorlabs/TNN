# W13 Stronger Core — Held-out verdict, ROUND 3 (protocol-clean)

**Date:** 2026-09-25 UTC. **Prereg:** `PREREG_W13_STRONGER_CORE.md` (frozen).
**Instrument:** `build/w13c_lease` (SHA-256
`d8589a504404c878a63cf75185f5ccb3646a5f5651f786e3241ff4108de0dffc` —
re-verified before evaluation; byte-identical to the frozen R1/R2 binary;
NOT rebuilt).
**Scorer:** `build/score_core.py` (independent, re-derives every renewal
decision from §3; 0 mismatches required).
**Streams:** `held_out_r3/w13c_heldout3_{sybil_quorum,tagshadow,sleeper_flip,forged_cred,launder_chain}.txt`,
manifest `HELDOUT_MANIFEST_R3.md` (hashes verified against files;
committed to `tnn-native-lab` at `bc8188263d28`).

## Protocol evidence (§6 — the step R1/R2 failed)

1. **Fresh adversary author**, appointed with ONLY the redacted brief
   (row format, §1 lease parameters, threat-model paragraph, content-pool
   locations, hard harness constraints, and the R2 fixture-design lesson:
   genuine traffic must include corroborated pairs so K-LIVE is
   measurable). The author confirmed it did not access any forbidden path
   (no prior-round streams, attacks, generators, verifiers, verdicts, the
   prereg, the binary, the scorer, or any core output). All five attacks
   are its own novel designs.
2. **Manifest committed BEFORE evaluation:** commit `bc8188263d28`,
   committer date **2026-09-25T20:53:38Z** (hashes only).
3. **Evaluator started after the commit:** first run artifact
   (`build/runs_r3/r3_sybil_quorum_r1.log`) created **2026-09-25
   20:54:06 UTC** — 28 s after the manifest commit.
   ⇒ **manifest-commit < evaluator-start. §6 timing SATISFIED.**
4. **Sealed attacks unopened until scoring finished** (opened by the
   coordinator after the scorer ran; mechanisms summarized below).
5. Frozen binary used throughout; no rebuild; SHA re-verified.

*Process note:* the evaluator completed all 10 runs (logs on disk,
timestamps confirm the ordering above) but its report payload was lost
in the handoff. The coordinator verified K-DET (byte-identical SHAs,
below) and ran the frozen scorer on the evaluator's logs. No protocol
impact: the runs postdate the manifest commit, the binary is frozen,
and the attacks stayed sealed until scoring was done.

## Round-3 numbers

| Stream | N | Genuine | False | Scorer mism | K-LIVE | False renewed | K-SAFE viol | Residuals (§8) |
|---|---|---|---|---|---|---|---|---|
| sybil_quorum | 100136 | 88000 | 12136 | 0 | 1.0000 | 14 | 0 | 14 |
| tagshadow | 99998 | 83332 | 16666 | 0 | 1.0000 | 43 | 0 | 43 |
| sleeper_flip | 40000 | 20000 | 20000 | 0 | 1.0000 | 0 | 0 | 0 |
| forged_cred | 25000 | 22000 | 3000 | 0 | 1.0000 | 3000 | 0 | 3000 |
| launder_chain | 24999 | 16666 | 8333 | 0 | 1.0000 | 0 | 0 | 0 |

- K-DET: r1 SHA == r2 SHA on all 5 streams (verified by coordinator):
  - sybil_quorum `0969e27c93436700486785c1749b20ff1299e31df6b8ade23de6ff987d18070b`
  - tagshadow `370827ad3d605fba70d5f677cdef78940eec44c5b0b167dde7716051ff980463`
  - sleeper_flip `f5a88f5c5ce0d37d740e9d8ef684df90051aaf2cea7e6146b71c854611b988af`
  - forged_cred `8d3d80349ccd5e6f4c425bf8de1a1c5ed563d0991b66e9e573d95511e2d3e858`
  - launder_chain `a3c6fa904577a1ce6e3b9b5f8ea4226e059dff988e0c922201fdf50a2d463eec`
- Max check staleness 2 (bar ≤ 3) on every stream.
- **K-LIVE = 1.0000 on all five streams** — measurable this time, as
  designed (100% of genuine rows sit in corroborated pairs).
- **K-NOV: 0 K-SAFE violations on all 5 streams — PASS.**
- **Every renewed falsehood is full-bar-passing** (residual lines cite
  only `(718,6600,1,1)` and `(874,10410,1,1)` — the 3 forged rows):
  indistinguishable-class residuals per §8, not violations.

## Why the attacks failed (mechanism story, from the unsealed designs)

The blind author knew only "the lease renews a claim when it is
corroborated" and built five genuinely novel structures:

1. **sybil_quorum** — 8-row false quorums (28 pairs each) on channels
   11–18, testing corroborator flooding. Only the 14 quorum rows whose
   content happened to be bar-passing renewed; the other 12,122 died on
   groundedness.
2. **tagshadow** — false rows parasitizing live genuine corridors by
   reusing the pair's own tag. 43 bar-passing shadows renewed as
   residuals; 16,623 died on groundedness. Renewal binds to the
   (channel, claim) identity — drafting behind genuine tags does not
   transfer legitimacy to failing content.
3. **sleeper_flip** — 20,000 false rows on a byte-identical corridor
   schedule after a kind flip. **0 renewed.** The mechanism re-evaluates
   legitimacy at each renewal; corridor reputation does not carry
   across the flip.
4. **forged_cred** — 3,000 false rows using ONLY the 3 bar-passing
   forged contents in 4-way clusters. 3,000/3,000 renewed — all
   residuals. This is the §8 impossibility lemma demonstrated at scale:
   content pointwise-indistinguishable from genuine claims on every
   observable the lease may use cannot be excluded by any renewal rule
   built from those observables.
5. **launder_chain** — an 8,333-link self-perpetuating chain (same tag,
   rotating channels, Δ=3 metronome). **0 renewed.** Perfect
   corroboration structure, failing content — groundedness kills it.

The pattern: against an adversary that satisfied corroboration six ways,
**groundedness did all the killing**. Nothing that failed the admission
bar renewed anywhere (0 violations across 45,802 false rows); the only
renewals are the §8-impossibility class the prereg already names.

## Verdict mapping (§7)

- K-NOV: **PASS, protocol-clean** — 0 violations, 5/5 streams.
- K-LIVE: 1.0000 ≥ 0.90 — no HOLD.
- K-DET: PASS. K-STRUCT: unchanged (frozen binary).
- Residuals: 3,057 total, all indistinguishable-class with content
  cited (§8 boundary note applies; K-COST unchanged at 3/1139 = 0.26%).

## Disposition

**Round 3 is a certified, protocol-clean K-NOV PASS.** The §6
information barrier held end to end: blind author → manifest committed
before evaluation → frozen binary → sealed attacks opened only after
scoring. This supersedes the protocol-compromised R1/R2 numbers as the
held-out evidence for the stronger core.
