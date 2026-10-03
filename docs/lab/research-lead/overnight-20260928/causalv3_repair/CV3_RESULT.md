# H-CAUSALV3 Repair Result

**Date:** 2026-09-29 (PDT)
**Lane:** repair of H-CAUSALV2 after independent red-team downgrade
**Verdict: H-CAUSALV3 SURVIVES 9/9** (both attacks closed, all regressions hold)

## 1. What was broken (H-CAUSALV2 red team, 2026-09-29)

Two independent attacks downgraded H-CAUSALV2 (bounded L2, not killed):

- **X-CV2-1 (double-confounder):** `delay_clean` accepted stasis as
  an effect and `dl_add_or_support` matched rules without the
  outcome value. Two positioned confounders confirmed
  `cause=1 d=1 var=s2 fx=SET(0)` to ACTIVE support 2, and the probe
  `Q (0 0 1) | 1` predicted `(0 0 0)` although action 1 was a no-op.
- **X-CV2-2 (threshold tie):** with observed s0={0,2}, THR t=0,
  THR t=1, and EQ all resolved in 2 cells; enumeration fiat picked
  t=0 and the system confidently predicted the wrong outcome on
  unseen s0=1.

## 2. Preregistration and governance

- `PREREG_CAUSALV3.md` frozen and committed at **7f535c115**
  (2026-09-29 23:25 UTC) before any implementation existed.
- `PREREG_CAUSALV3_AMEND1.md` frozen and committed at **d7272fa75**
  (2026-09-29 23:27 UTC), also before any result was frozen.
  AMEND1 refined agreed-under-ambiguity: a candidate that cannot
  cover the query abstains rather than vetoing (see section 5).
- Implementation source `causalv3.zag` is a byte-verified copy of
  committed `causalv2.zag` (sha256
  ed81506fba7c52bcbc98e639d71dc275) plus exactly the three frozen
  repairs (R1a, R1b, R2) and AMEND1.
- Pure Zag throughout. No Python. Toolchain: znc 2026.07.0-dev
  (edition 2026). Binaries built in /tmp only, never committed.
- Concurrent-worker hygiene: the prereg commit swept in one
  pre-staged foreign file (`PREREG_UNIFIED6.md`, another worker's);
  my prereg content verified intact by md5. All later commits
  contain only owned paths.
- Determinism: every fixture run 3/3, byte-identical.

## 3. The repairs (what changed in causalv3.zag)

- **R1a (change-gated delay):** `delay_clean` returns 0 when
  `ep_ns(W,e,v)==ep_s(W,e,v)`. Stasis is not an effect the SET(nv)
  representation can attribute; a stasis contradiction belongs to
  the contest machinery, not delay attribution.
- **R1b (outcome-aware confirmation):** `dl_add_or_support`
  matches on `(cause, delay, var, outcome)` and requires
  `dl_fp(W,r)==nv`. A different outcome opens a separate
  PROVISIONAL rule instead of confirming.
- **R2 (tie-ambiguous splits):** Phase 1 split search collects ALL
  per-variable minimum-cell candidates. A unique minimum on a
  single variable applies; any tie (within a variable, across
  variables, or both) stores every tied minimum as ST_AMB (cap 8,
  explicit warning if exceeded) and emits `# entry N AMBIGUOUS
  over K tied candidates (no fiat split)` when an internal tie
  exists. Enumeration order is provably irrelevant. The old
  THR-before-EQ tie-break is retired as moot.
- **AMEND1 (abstention):** in agreed-under-ambiguity, a candidate
  with `pred_under_cand==0` (cannot cover the query, e.g. EQ on
  an unseen value) abstains; prediction requires >=1 covering
  candidate and unanimous agreement among covering candidates,
  else WITHHOLD.

## 4. Frozen kill bars: all pass

| Bar | Result |
|---|---|
| K-CV3-1: double fixture, zero delay rules, no (0,0,0) harm prediction | PASS: 0 rules, probe `(0 0 1)` correct. Confounded episodes now surface as CONFLICTED entries (honest law-change signal), not masked delay rules. |
| K-CV3-2: thr fixture, ST_AMB over exactly 3 tied candidates, probe WITHHOLD | PASS: `CAND=[THR s0<=0,THR s0<=1,EQ s0]`, `Q (1 1 0) | 3 -> WITHHOLD` |
| K-CV3-3a: mask fixture zero delay rules, probe (0,0,1) | PASS: 0 rules |
| K-CV3-3b: 3i2 byte-identical; 3i probes unchanged with honest AMB trace | PASS: 3i2 byte-identical; 3i probes (1,1,0),(0,0,1),(2,0,0) unchanged, entry 3 now AMBIGUOUS over 2 tied candidates |
| K-CV3-3c (amended): 3c, 3d, C2 byte-identical; B2 probes byte-identical | PASS: 3c, 3d, C2 byte-identical; B2 probes (2,0,0)/WITHHOLD/(1,1,1) identical; trace honestly reports the 4-candidate tie |
| K-CV3-4: 3/3 byte-identical every run | PASS: all 9 fixtures |

## 5. The B2 incident (why AMEND1 exists)

The prereg assumed B2 had no internal tie. It does: s0 admits
three tied minima (THR<=0, THR<=1, EQ s0). The unamended R2
withheld `Q (1 1 1) | 2` because EQ s0 cannot cover unseen s0=1
and non-coverage vetoed. But every covering tied candidate agrees
s1=1, so the withhold was a veto technicality, not evidential
honesty. AMEND1 (abstention) restores the unanimous (1,1,1) while
preserving X-CV2-2's withhold, where THR<=0 and THR<=1 are both
covering and genuinely disagree. B2's trace line change
(`over 4 tied candidates`) is the honest record of the tie.

## 6. Raw evidence (committed)

- `CV3_DOUBLE_RUN.txt` (K-CV3-1)
- `CV3_THR_RUN.txt` (K-CV3-2)
- `CV3_MASK_RUN.txt` (mask)
- `CV3_3I2_RUN.txt` (byte-identical to CV2_3I2_RUN.txt)
- `CV3_3C_RUN.txt`, `CV3_3D_RUN.txt`, `CV3_C2_RUN.txt`
  (byte-identical to committed CV2 runs)
- `CV3_B2_RUN.txt` (probes byte-identical to CV2_B2_RUN.txt)
- `CV3_3I_RUN.txt` (probes unchanged, honest AMB trace)

## 7. Limitations and honest boundaries

- R1a removes the ability to learn genuine delayed prevention
  (a cause whose delayed effect is "no change where change was
  expected"). The representation cannot express it; this is a
  stated boundary, not a hidden one.
- R2's ambiguity is permanent for tied candidates unless later
  evidence refutes some via amb_update; the system never
  resolves ties by confidence.
- AMEND1 means a single opinionated candidate predicts alone
  when all others abstain. If that candidate is wrong, the
  error surfaces as a wrong prediction, not a withhold.
  Refutation machinery (contests, amb_update) is the backstop.
- H-CAUSALV3 remains bounded L2, exactly as H-CAUSALV2 was:
  the repairs close harm-capable flaws; they do not advance
  the learning level.
- The swept-in foreign file in the prereg commit
  (`PREREG_UNIFIED6.md`) belongs to a concurrent worker and is
  not part of this lane's lineage.

## 8. Commit lineage

- 7f535c115 PREREG H-CAUSALV3 FROZEN (prereg; strict ancestor)
- d7272fa75 PREREG H-CAUSALV3 AMEND1 FROZEN (amendment)
- <this commit> H-CAUSALV3 implementation + evidence + result

Suggested paper line (for the research paper, parent lane):
"H-CAUSALV3 SURVIVES (9/9: both red-team attacks closed, all
regressions hold, bounded L2). Change-gated delay attribution;
tie-ambiguous splits with abstention. Repair of H-CAUSALV2."
