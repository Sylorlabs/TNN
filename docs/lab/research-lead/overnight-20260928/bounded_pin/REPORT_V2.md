# REPORT V2: BOUNDED-PIN-LIFETIME (amended verdict)

Date: 2026-10-03. Worker: BOUNDED-PIN-LIFETIME worker (non-ledger task).
Amended prereg: PREREG_V2.md, committed alone as 6674152ee (strictly
before the v2 run). Mechanism unchanged: bounded_pin.zag as committed
in 1335d48c2, re-executed 3x with no source changes. The v1 record
(REPORT.md, VERDICT=FAIL on K3/K4 derivation errors) stands unaltered;
this document records only the v2 verdict against the corrected bars.

## Verdict: PASS (8/8)

All v2 kill bars hold. Fresh v2 run 3/3 byte-identical
(sha256 6e93317bf1bc4f404e2ad2545c315c16be010c6bb1c2fcb7c0600d5d244a14b4,
identical to v1 as expected: same frozen binary, deterministic).

## Results (identical across run1v2/run2v2/run3v2)

| cond     | pol | pre | post | ret | cf | ev | drop | bacc | rawA |
|----------|-----|-----|------|-----|----|----|------|------|------|
| PINR-M2  | 3   | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| PINR-M3  | 3   | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   |
| TTL10-M2 | 4   | 35  | 15   | 42  | 60 | 28 | 0    | 20   | 25   |
| TTL10-M3 | 4   | 35  | 15   | 42  | 80 | 48 | 0    | 20   | 25   |
| TTL50-M2 | 5   | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| TTL50-M3 | 5   | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   |
| TTL100-M2| 6   | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| TTL100-M3| 6   | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   |
| UNPIN-M2 | 7   | 35  | 35   | 100 | 60 | 11 | 17   | 20   | 35   |
| UNPIN-M3 | 7   | 35  | 35   | 100 | 80 | 5  | 43   | 20   | 35   |

Kill bars (v2):
- K1 BASELINE: pre==35 and bacc==20 in all 10 -> PASS
- K2 PINR-REPRO: ret=[100,100], ev=[0,0], drop=[28,48] -> PASS
- K3' TTL10-SHIELDED-PARTIAL: TTL10-M2 (post,ret,ev,drop,rawA)=
  (15,42,28,0,25); TTL10-M3 (15,42,48,0,25) -> PASS. Bounded
  lifetime at N=10 does not degenerate to FIFO: the slot-index scan
  recycles slots 0..9 as a churn buffer and benign slots 10..19
  survive.
- K4' TTL50-FROZEN-EQUIV: TTL50 rows == PINR rows exactly
  (ret=[100,100], ev=[0,0], drop=[28,48]) -> PASS. N beyond the
  freeze threshold (32) never expires: drops do not tick the clock.
- K5 TTL100-NORECLAIM-EQUIV: TTL100 rows == PINR rows exactly
  -> PASS
- K6 UNPIN-PARTIAL: UNPIN-M2 (ret,ev,drop,rawA)=(100,11,17,35);
  UNPIN-M3 (100,5,43,35) -> PASS (held exactly in v1 as well)
- K7 ADV-FIXED: cf==60 (M2 x5), cf==80 (M3 x5) -> PASS
- K8 DETERMINISM: v2 3/3 byte-identical -> PASS

## Answers to the parent questions (v2, confirmed)

Does bounded lifetime restore capacity without losing robustness? No.
The measured N landscape is three sharp regimes, not a tunable
frontier: N<=10 restores capacity fully (drop=0) but loses 58 points
of retention (ret=42, via the churn-buffer shielding the v1 trace
missed); N>32 keeps ret=100 but reclaims nothing (drop=28/48,
bit-identical to unbounded). No N achieves ret=100 with drop=0: any
expiry bound that can fire either also reaches benign history
(slot-index scan order) or never fires at all (clock freeze during
drops). The derived-but-untested middle regime (10<N<=32, exact FIFO
collapse, ret=0) makes N=20 the sharp follow-up.

What is the optimal N? There is no dominant N on the TTL frontier;
"optimal" is a regime choice. Among tested N, only N=10 reclaims
anything (drop=0 at ret=42). On retention, the explicit-unpin arm
dominates every TTL setting (ret=100, drop=17/43): it alone pairs
full robustness with partial reclamation, because unpins (unlike
expiry) never touch benign entries while the commons lasts.

Head to head across all five arms (M2 dose): PINR (100, drop 28),
TTL10 (42, drop 0), TTL50 (100, drop 28), TTL100 (100, drop 28),
UNPIN (100, drop 17). The unpin mechanism is the only arm off the
TTL frontier, and its price vs PINR is purely the residual pinned
footprint of the non-consenting churners (owners 4/8), which grows
with the dose (17 -> 43).

## Discrimination accounting (v2)

K3' vs K2 separates the shielded-partial regime from unbounded
(ret 42 vs 100, drop 0 vs 28, on identical adversary footprints).
K3' vs the v1 K3 shows the exact-FIFO prediction failed in the
sharpest measurable way (ret=42/rawA=25, not 0/15). K4' vs K3'
separates the frozen regime from the recycling regime on both axes.
K6 vs K3'/K4' keeps unpin off the TTL frontier (ret=100 with
drop<28/48, which no N achieves). K5 vs K2 pins the frontier's upper
end (beyond-horizon N is behaviorally unbounded). K7 bars the
adversary confound throughout.

## Relation to the v1 record

The v1 FAIL stands: K3 and K4 as originally preregistered did not
hold, because the v1 derivations assumed per-relocation clock ticks
and age-ordered eviction. The v2 bars are not weakened versions of
the v1 bars: K3' predicts an outcome the v1 K3 explicitly excluded
(ret=42), and K4' predicts exact equivalence where v1 predicted a
partial interior point. The mechanism, adversary, protocol, and all
other bars are unchanged between v1 and v2; only the two faulty
derivations were corrected, transparently and before the v2 run.

## Follow-ups (not tested here)

- N=20 under M2/M3: the derived 10<N<=32 regime predicts exact FIFO
  equivalence (ret=0, ev=28/48, drop=0). Sharp test of the
  three-regime structure; needs its own prereg.
- All-churners-unpin variant: expected to re-derive the aligned
  consent outcome (drop=0, ret=100); tests whether the K6
  commons-consumption result is specifically a coverage effect.
- Benign re-pinning during churn (re-reads refreshing pins): breaks
  the age-order degeneracy and could rescue short N; the stated
  condition under which TTL fails, not a law.

## Toolchain guard (v2 run)

Safebin active; `which python3` and `which python` returned nothing;
no forbidden executable invoked (shell only for binary execution,
sha256sum, cmp, git). No source changes for v2; the binary is the
v1-committed build. No PROCESS-FAIL condition triggered. Git writes
through /usr/bin/git directly with explicit pathspecs; no git reset.

## Commits

- aaf3fb037: frozen prereg v1 (PREREG.md + NAMECHECK.md), alone.
- 1335d48c2: implementation, 3/3 v1 runs, REPORT.md (v1
  VERDICT=FAIL record). Local only, never pushed.
- 6674152ee: PREREG_V2.md amendment, alone.
- This commit: run1v2.txt, run2v2.txt, run3v2.txt, REPORT_V2.md
  (v2 VERDICT=PASS 8/8). Local only, never pushed.
