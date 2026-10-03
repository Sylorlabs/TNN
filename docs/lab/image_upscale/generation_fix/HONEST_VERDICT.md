# HONEST VERDICT — Crew A: key-ambiguity fix, generation path

Date: 2026-09-27. Prereg: [PREREG.md](PREREG.md) (frozen before implementation).
Evidence: [RUNLOG.md](RUNLOG.md). No post-result tuning was performed.

## Verdict: HONEST LOSS — no surviving arm.

| Arm | Bridge Δ | Sky Δ | Diverse (9) | Prereg fate |
|---|---|---|---|---|
| A1 cross-scale agreement | +0.01 dB | +0.00 dB | all \|Δ\|≤0.05 dB | no beat — out |
| A2 smooth energy-band gate | −0.31 dB | −0.39 dB | loses 8/9 | strictly worse — out |
| A3 Fable's correlation discipline | **+0.44 dB** | **+3.52 dB** | loses 7/9 | **KILLED: +0.44 < 2 dB bar** |

- **Arm 3 is killed by its own preregistered bar** (PREREG: "if Arm 3 improves
  <2 dB over 18.47 dB on bridge … Arm 3 is killed — reported, not hidden").
  18.91 − 18.47 = +0.44 dB. The rejection prong does not fire (incremental
  top-level nofit fraction 8.3% < 30%).
- Arm 3 is the bridge/sky winner and matched the deliberation's advisory vote,
  **but it does not generalize**: on the nine sealed held-out photos it loses
  to baseline on 7 of 9 (up to −0.53 dB). The sky gain (+3.52 dB) is real but
  image-specific, not a general fix.
- Arms 1 and 2 do not beat baseline anywhere; Arm 2 is actively harmful.
- All four arms remain far below bicubic on every image (e.g. bridge 18.91 vs
  25.89; sky 26.27 vs 33.20).

## Why it failed (mechanism, not excuse)

1. **The premises didn't hold on the actual failure.** The deliberation proved
   the worst take (brick atom 42 on the arch, x=192,y=32) is NOT smooth by the
   corpus τ_min (3,575,392 > 2,985,492) and its fine-key winner IS in the
   coarse top-3. Arms 1 and 2 target conditions the failure doesn't satisfy —
   so they pass the bad take through (A1) or reject the wrong takes (A2).
2. **Rejection is a weak lever here.** The four brick takes are ~60% of total
   SSE, but replacing them with mean-fill/LINES refills nets only ~10% SSE
   reduction (+0.44 dB): the replacements are barely better than the bad
   takes on those footprints. Fable's 2 dB bar (≈37% SSE cut) was almost
   certainly unachievable by any rejection-only rule — flagged for the
   coordinator, not used to override the frozen kill.
3. **Strictness doesn't transfer.** Arm 3's discipline helps where takes were
   genuinely wrong (sky's smooth regions) and hurts where takes were
   genuinely right (textured photos: treebark −0.40, portrait −0.43, car −0.53,
   market −0.47). Input-resolution gain cannot tell these apart — that is the
   core defect, and none of the three arms repairs it; they only re-weight it.
4. **The failure is key ambiguity, confirmed again:** 25 of 63 atoms within 2×
   of the winner's SSD on the bad block. The fix has to resolve ambiguity at
   match time (better keys, or a construction operator that doesn't stamp
   texture the key can't vouch for) — not veto matches after the fact.

## What was done right

- Preregistration before implementation; frozen kill bars applied as written,
  including the one that kills the best arm.
- TNN deliberation replicated the baseline byte-exactly before advising; its
  advisory vote (Arm 3) matched the empirical bridge/sky winner — but the
  test, not the vote, decided, and the held-out set overruled both.
- Every binary ran every image twice with byte-identical outputs (44
  rerun-SHA comparisons, all IDENTICAL).
- The deliberation's own explanatory error (claiming the bad winner "fails
  correlation") was instrumented, retracted, and corrected of record: the
  winner correlates positively (+4,391,538); it was rejected as
  uncorroborated (sole candidate, nsurv=1<2).
- No tuning after results. The disk-full incident was loud (rc=1), not silent.

## Recommendation

Do not pursue these three arms. If the program wants a second attempt, the
preregistered lesson is: calibrate the bar to the mechanism's ceiling, and
attack ambiguity at match time (keys/construction), not with post-hoc vetoes.
Any revival of Arm 3 needs a new prereg with a recalibrated bar — the current
one is killed and stays killed.
