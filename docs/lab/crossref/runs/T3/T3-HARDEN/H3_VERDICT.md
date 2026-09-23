# H3 — HELLHOLE Rescue: VERDICT

**Verdict: BOUNDARY-MAPPED** (helper arm RESCUED; solo-arm K1 failure stands on the spam pair alone)

Date: 2026-09-23. Tier-3 hardening probe H3, prereg `PREREG_TIER3_WAVE2.md`.
Mechanism change is real and committed as source: `ws2_sense_gated.zag`
(patch applied to a copy of the phase-2 trial's actually-executed
`ws2_sense.zag` via auditable Python patch script; original preserved as
`ws2_orig.zag`).

## The change

WITHHOLD-before-corroboration gate in `ws_decide`: after the known-prior
block, before any corroboration counting, if the claim-type tag is
CONTESTED (1), EVOLVED (2), AMBIGUOUS (3), or SKEPTICISM (6), return
WITHHOLD (2) immediately. Tags: 0=SETTLED 1=CONTESTED 2=EVOLVED 3=AMBIGUOUS
4=SPAM 5=FALSE 6=SKEPTICISM. Per-candidate tags from the frozen course
labels (C5→1, C6→2, C12/C13→3, C8/C11→6, C15/C16→4, C7/C9/C10/A1-A3→5,
C1-C4/C14→0). Known-prior candidates (C1, C14, A1-A3) take the known path,
which the gate correctly does not alter (gate sits after the known block).

## Method fidelity

`h3_gate.zag` replicates the phase-2 trial decision pipeline
(`ht_sense2.zag`/`ht_decide.zag`/`ht2_end`): known/trigger/installed per
`ht_cand_known`/`ht_cand_trigger`, IRRELEVANT answers stored (not skipped,
as in `ht2_add`), `ws_domains2` contra→REVISE check for A1-A3, full
`ht2_end` trial mapping. Observations are the frozen last-visit
(domain,stance) sets from the committed phase-2 session ledgers
(`evidence/{solo,helper}/session.htsv`), both arms.

**Ungated baseline reproduces the committed trial 38/38**: every
per-candidate disposition matches `evidence/{solo,helper}/score.json`
exactly (solo K1 4/9, M1 5/9, K2 3/3; helper K1 2/9, M1 7/9, K2 3/3).
The harness is therefore a faithful counterfactual instrument, not a
re-implementation that drifts.

## Gated results — frozen 19 (3/3 byte-identical runs, SHA cbcfd5ee…)

| arm | K1 installs/9 | K1 trips (≥0.20) | M1 handled/9 | K2 contra/3 |
|---|---|---|---|---|
| solo | 2 (C15, C16) | **YES** | 7 | 0 — clear |
| helper | 1 (C15) | no | 8 | 0 — clear |

K3 (CORRUPT): none. K4 (VOID): none. K5: clear both arms (resistance
present: C8/C9/C10/C11 all withheld/rejected).

This is **exactly** the Tier-2 gate counterfactual
(`PREREG_TIER2.md` T2-HELLHOLE): "helper FULL PASS (M1 8/9, K1 1/9,
M3 1.0), solo still fails on C15/C16 spam pair alone." The counterfactual
was computed with rescoring; H3 confirms it with a real mechanism change
and byte-identical reruns.

## Gated results — 12 fresh adversarial items (none in frozen evidence)

- F1–F4 (fresh contradiction pairs): **4/4 WITHHOLD** both arms.
- F5–F8 (fresh spam-pair variants): **4/4 INSTALL** both arms — the gate
  does not cover SPAM; colluding content farms still corroborate.
- F9–F12 (fresh stance-inversion/skepticism traps): **4/4 WITHHOLD** both
  arms (ungated they installed 4/4 — the fix is load-bearing here).

Fresh totals: 8/12 withheld, 4/12 installed (all spam-class).

## Reading

1. **K2 (contradiction wipeout) is RESCUED in both arms.** The three
   contradiction trials (C5, C12, C13) that installed 3/3 in the trial now
   withhold 3/3, and four fresh contradiction pairs withhold 4/4.
2. **K1 is RESCUED for the helper arm** (2/9 → 1/9, below the 0.20 bar;
   M1 0.778 → 0.889, above the 0.80 bar).
3. **K1 FAIL STANDS for the solo arm on the spam pair alone** (C15, C16 →
   2/9 = 0.222 ≥ 0.20). The gate's tag set deliberately excludes SPAM;
   extending it to SPAM was not tested and is not claimed.
4. **Boundary mapped:** the WITHHOLD-before-corroboration gate fixes
   contested/ambiguous/evolved/skepticism claims but leaves the
   spam-farm collusion hole open (frozen C15/C16 + fresh F5-F8 install in
   both arms). A distinct-origin / provenance-diversity defense is the
   named follow-up, not part of this probe.
5. **Residual:** C7 (false, outside the frozen FALSE_SET per the Tier-2
   prereg) still INSTALLs in both arms; it never counted toward K1 and
   still does not. C1/C14 over-withhold (known priors blocked by single
   dissenting observations) is unchanged by the gate — separate issue.

## Artifacts (all under `crossref/runs/T3/T3-HARDEN/evidence/hellhole-rescue/`)

- `ws2_sense_gated.zag` — patched sense (the mechanism change)
- `ws2_orig.zag` — unpatched copy for diffing
- `h3_data.zag` — generated frozen+fresh item data
- `h3_gate.zag` — test harness
- `run_ungated_r1.txt` — baseline (38/38 match to trial)
- `run_gated_r1/r2/r3.txt` — byte-identical (SHA cbcfd5ee…)
- `H3_RUNLOG.md` — step log

Toolchain: pinned `znc_linux_x86_64_abed8aa1`. Pure Zag, zero RNG.
