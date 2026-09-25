# WS1C Verdict: Adversarial Skepticism for Forced-Conscious (Track A)

Trial of the preregistered skepticism upgrade (PREREG_WS1C.md, frozen
commit f652191e3d4853596661399b51dece344e3998b3, before any trial
execution). Mechanism source committed at
15d5b3ac14b238cf128ff3db3a9d3a523736ace8. Pure Zag, zero RNG, pinned
toolchain ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.

## 1. Head-to-head results

Four arms: A1 forced-conscious (tocap), A2 forced+skepticism, A3
autopilot (batch), A4 router (D-D gate to autopilot/forced). Per-family
accuracy (attack items only for adversarial families):

| family | n | forced | skeptic | autopilot | router |
|---|---|---|---|---|---|
| rtd1-poison | 3 | 0/3 | 3/3 | 0/3 | 0/3 |
| rtd1-bait | 3 | 0/3 | 3/3 | 3/3 | 3/3 |
| rtd1-double | 2 | 0/2 | 0/2 | 0/2 | 0/2 |
| rtd1-strong | 2 | 0/2 | 2/2 | 2/2 | 2/2 |
| rtd1-clean | 4 | 4/4 | 4/4 | 4/4 | 4/4 |
| poison2 | 6 | 1/6 | 6/6 | 1/6 | 1/6 |
| baitflip2 | 6 | 4/6 | 6/6 | 6/6 | 6/6 |
| refute2 | 6 | 1/6 | 6/6 | 6/6 | 6/6 |
| new-clean controls | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| refusal | 60 | 60/60 | 60/60 | 44/60 | 60/60 |
| ambig1 | 14 | 8/14 | 11/14 | 8/14 | 8/14 |
| perception F2 (compat leg) | 14 | 12/14, matches frozen baseline | n/a | n/a | n/a |
| admit | 248 | 248/248 | 248/248 | 248/248 | 248/248 |
| revoke | 113 | 113/113 | 113/113 | 113/113 | 113/113 |
| logic | 264 | 264/264 | 264/264 | 264/264 | 264/264 |
| trap | 127 | 127/127 | 127/127 | 127/127 | 127/127 |
| cost | 125 | 125/125 | 125/125 | 125/125 | 125/125 |

rtd1 overall: forced 4/14, skeptic 12/14, autopilot 9/14, router 9/14.

## 2. Kill bars

- K1 (skeptic never worse than autopilot, per adversarial family): PASS
  on all 7 families. Strictly better on rtd1-poison (3/3 vs 0/3) and
  poison2 (6/6 vs 1/6); equal elsewhere.
- K2 (no confidently-wrong skepticism): PASS. Zero skeptic misses at
  confidence 1000 across rtd1, poison2, baitflip2, refute2, ambig1,
  refusal. The 5 skeptic misses are tentative: rtd1-double 2 at conf
  400, ambig1 3 at conf 20-50. For comparison, forced-conscious has 21
  wrong-at-1000 results on the same attack items.
- K3 (refusal at forced's level): PASS, 60/60. Gate fired 0/60 on
  refusal.
- K4 (perception-ambiguous): PASS. ambig1: skeptic 11/14 vs forced
  8/14. Perception compatibility leg: frozen F2 decoder rebuilt from
  source (SHA-256 matches the frozen
  a4ad7c49333e04dfdad17b0827a0063f8b1a5b3f1da0107b49f39e8572931444),
  rerun on the 14-item battery: 12/14, all 14 judgments identical to
  the frozen baseline, byte-identical across 3 reruns.
- K5 (no regression on honest structured): PASS, all five batteries
  at 1.000 for skeptic, equal to forced.
- K6 (determinism): PASS. All 44 cells byte-identical across 3 reruns
  (results and metrics). Source grep gate: no RNG primitives in
  skep_lib.zag or skep_main.zag; support files byte-identical to the
  frozen harness.
- K7 (router): PASS. K7a: D-D flags 0/60 on refusal. K7b: router >=
  autopilot on every adversarial family.

Decision rule: K1-K6 all pass, so SKEPTIC is ADOPTED as the
forced-conscious upgrade.

## 3. Skepticism dominates the router

The router (A4) matches autopilot on every flagged family and never
fixes what autopilot gets wrong: rtd1-poison router 0/3, poison2
router 1/6. Skepticism (A2) actually repairs the flagged items:
rtd1-poison 3/3, poison2 6/6. Routing suspicious inputs to the batch
arm preserves autopilot's failures; the preregistered hypothesis,
that the fault is in UNSAFE sequential deliberation rather than in
sequential deliberation itself, is supported: guarded deliberation
beats both unguarded deliberation and no deliberation.

## 4. Gate behavior

D-D fired on 28/28 attack items across the four adversarial families
and 0/60 refusal items. Fire reasons on attack items: P1 18, P2 5,
P3a 4, P3b 1. Every predicate pulled weight: P2 caught 4 of 6
bait-flips that A/M alone misses; P3a caught the remaining bait-flip;
P3b caught the refute2 false-lead that P1/P2 both miss. On honest
batteries the gate is deliberately conservative (fires on contention:
admit 14/248, revoke 16/113, logic 159/264, trap 65/127, ambig1 11/14)
and safe mode preserves verdicts exactly (all 1.000 / 11/14).

## 5. Prereg deviation

The frozen refute2.jsonl (SHA-256
3555f1e86ad7d0e44637d971b29b8fe301b81b6fca5804a56763409944a22a13,
as pinned in the prereg) contained two ASCII escape sequences
(`\u00e9`) in R2-REFUTE-04's text. The frozen JSON parser rejects
backslash escapes, so the item could not run: the first full trial
silently dropped it (7/8 rows, run reported err=1 on isolation). The
file was fixed byte-level (`\u00e9` to raw UTF-8 e-acute, 6 ASCII
chars to 2 bytes); JSON content verified identical item-by-item.
New SHA-256:
539110c53c851a4cbc0c4a6e5294abeb88e853a63eaab55023a05c6f0f5f9132.
The refute2 battery was rerun in full (4 arms x 3). No weights,
truth values, or text meaning changed. This deviation is mechanical
and was required for the battery to be runnable at all.

## 6. Adoption

SKEPTIC is adopted as the forced-conscious upgrade per the
preregistered decision rule. All kill bars pass; the mechanism is
deterministic, audited, and pure Zag. The router remains a documented
alternative that underperforms skepticism on poison families.

Evidence: runs/main/ (44 cells x 3 reruns, results + metrics),
runs/perception/f2_rerun_rows.json. Analysis: analyze.py.
