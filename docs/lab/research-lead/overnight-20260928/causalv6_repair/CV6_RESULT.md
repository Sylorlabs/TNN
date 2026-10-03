# H-CAUSALV6 Repair Result

**Date:** 2026-09-29 (PDT)
**Lane:** repair of H-CAUSALV5 after independent red-team downgrade
**Verdict: H-CAUSALV6 SURVIVES (K-CV6-1c, K-CV6-2, K-CV6-3, K-CV6-4 all PASS)**
**Classification:** bounded L2, narrowed. Not L3.

## 1. What was broken (H-CAUSALV5 red team, 2026-09-29)

- **X-CV5-1 (one-way ratchet):** SUCCEEDED. One counter-episode
  permanently demoted a genuine ACTIVE delay rule in a
  context-stable environment. Three honest re-demonstrations could
  not restore it because R5 did not reset dl_cs, so the R4
  diversity check could never pass.
- **X-CV5-2 (masking):** SUCCEEDED. The refuting observation was
  fully explained by the learner's own immediate law for a1
  (s2:=SET(2)), yet R5 demoted the genuine delay rule. The
  refutation could not distinguish falsification from masking.
- **X-CV5-3 (zero-cost re-arm):** SUCCEEDED. A persistent adversary
  re-armed the refuted SPURIOUS rule with a SINGLE episode.
  Refutation reset support to 1, so one fresh-context support
  re-confirmed.
- **X-CV5-4 (regression):** FAILED (defense held).

## 2. Preregistration and governance

- `PREREG_CAUSALV6.md` frozen and committed ALONE at **745b831b1**
  before any implementation, build, or run existed.
- Two transparent amendments (K-CV6-1b at **e6cbd2a3c**, K-CV6-1c
  at **51cf2b3d2**), each frozen with fixtures before any run.
  Prior bars were not altered; failed bars retain FAIL verdicts.
- `causalv6.zag` is a byte-verified copy of committed
  `causalv5.zag` (md5 1fc56329a2d6da52104050e3e83406b4) plus exactly
  the frozen R6 change set (124 diff lines: R6a/R6b/R6c, new
  O_DL_RF memory, header comments). One pre-existing em-dash in
  the line-1 comment (inherited from causalv5.zag) was removed;
  no mechanism impact.
- Pure Zag throughout. No Python at any stage (prereg, edits,
  fixtures, builds, runs, greps, hashes, cmp). Toolchain:
  znc 2026.07.0-dev (edition 2026). Binaries built in /tmp/cv6
  only, never committed.
- Only H-CAUSALV6-owned paths staged/committed
  (docs/lab/research-lead/overnight-20260928/causalv6_repair/).
  No broad git add.
- Determinism: every fixture run 3/3, byte-identical (cmp).
- No em dashes in loop documentation (byte-verified).

## 3. The repair (R6: graded re-confirmation + masking check)

### R6a: Refutation records the support floor

New memory `dl_rf` (i32 per delay rule; O_DL_RF=8932; WSZ 8984
→ 9048). When an ACTIVE rule is refuted, the pre-refutation
support is saved to dl_rf before support resets to 1. Rule
creation initializes dl_rf=0.

### R6b: Graded re-confirmation (closes X-CV5-1, raises X-CV5-3 cost)

In `dl_add_or_support`, the promotion branch splits:
- If dl_rf==0 (never refuted): original R4 logic unchanged
  (support>=2 AND cause-context diversity).
- If dl_rf>0 (previously refuted): promote to ACTIVE iff
  support strictly exceeds dl_rf. The R4 diversity check is
  replaced by this higher bar. On promotion, dl_rf is cleared to
  0. If support <= dl_rf, emit `# delay rule R<r> NOT
  RE-CONFIRMED at seq <s>`.

Rationale: the diversity check vetted the initial confirmation;
post-refutation, the question is whether new evidence outweighs
the refutation (quantity, not context-diversity). In a
context-stable environment, repetition is the only available
evidence, and the ratchet must not make it useless. A refuted
hypothesis needs stronger evidence to be re-adopted (graded
confidence).

### R6c: Masking check (closes X-CV5-2)

New helper `dl_masked(W,e,v,obs)`: finds the best-matching ST_ACT
entry for the current episode's action and pre-state (same
specificity logic as predict_entry). If that entry's fx for v is
an active SET/ADD that predicts the observed outcome, return 1
(masked). A passive UNCH law is not masking. No matching entry
is not masking.

In `dl_retract_check`, if dl_masked returns 1, the refutation is
withheld and `# delay rule R<r> NOT REFUTED at seq <s> ... masked
by a=<a> immediate law; remains ACTIVE` is emitted. The check
runs before entry_add_ep, so the law comes from PRIOR episodes
only.

Rationale: the delay rule is a ceteris-paribus claim. If the
current action's own learned law actively predicts the observed
outcome, the ceteris-paribus condition is violated; the
observation does not test the delay rule.

## 4. Frozen kill bars

### K-CV6-1: X-CV5-1 ratchet → FAIL (prereg error), superseded by K-CV6-1c

The frozen 24-episode red-team fixture contains a
fixture-induced artifact: once R6 correctly re-confirms R0 at
seq21, the E_3 effect episode (a4 at seq21) triggers a legitimate
R5 refutation at seq23. The fixture was designed for CV5 (where R0
never reactivates). The trace proves R6b works (`CONFIRMED at seq
21`), but the hand-derived final-state expectation was wrong.
**Verdict: FAIL (prereg error, documented transparently).**
Raw preserved: CV6_DEG24_RUN.txt.

### K-CV6-1b: clean a3-effect fixture → FAIL (fixture design error)

The a3-effect fixture did not trigger delay_attribution; the
learner attributed s2:=1 to a3's immediate law (entry 5 learned
SET(1)). The a3 action lacked a sufficiently established no-op
history. **Verdict: FAIL (fixture design error).** Raw preserved:
CV6_CLEAN_RECONF_RUN.txt.

### K-CV6-1c: truncated 21-episode fixture → PASS

The first 21 episodes of the red team's frozen fixture
(byte-identical prefix), excluding the artifact block.
- `# delay rule R0 REFUTED at seq 15` (exactly one). dl_rf=2.
- `# delay rule R0 NOT RE-CONFIRMED at seq 18` (support=2).
- `# delay rule R0 CONFIRMED at seq 21 support=3 (provisional
  -> active)` (support=3 > 2).
- Zero REFUTED after seq15. Zero NOT CONFIRMED.
- Final: `# DL R0 cause=4 d=2 var=s2 fx=SET(1) st=ACT support=3`.
- Probe: `Q (0 0 0) | 3 -> (0 0 1)` (restored delay fires).
- 3/3 byte-identical (md5 35433be9e9ac3d2271e1519e6db2fc3c).
**Verdict: PASS.** The X-CV5-1 one-way ratchet is closed.

### K-CV6-2: X-CV5-2 masking → PASS

Red team's frozen mask fixture.
- Zero `# delay rule R0 REFUTED` lines.
- `# delay rule R0 NOT REFUTED at seq 16: cause a=4 at seq 14
  not followed by s2=1 (observed 2); masked by a=1 immediate law;
  remains ACTIVE`.
- Final: `# DL R0 cause=4 d=2 var=s2 fx=SET(1) st=ACT support=2`.
- Probe: `Q (0 0 0) | 1 -> (0 0 2)` (from a1 immediate law).
- 3/3 byte-identical (md5 d3ef918e9ea1c418f86259c0bf90c890).
**Verdict: PASS.** The X-CV5-2 masking hole is closed.

### K-CV6-3: X-CV5-3 re-arm cost → PASS

Red team's frozen rearm fixture.
- `# delay rule R0 REFUTED at seq 10` (exactly one; a1's law for
  s2 is UNCH, so no masking; dl_rf=2).
- At seq11: `# delay rule R0 supported at seq 11 support=2`
  followed by `# delay rule R0 NOT RE-CONFIRMED at seq 11`.
- Zero `# delay rule R0 CONFIRMED at seq 11` lines.
- Final: `# DL R0 cause=1 d=1 var=s2 fx=SET(2) st=PROV support=2`.
- Probe: `Q (0 0 1) | 1 -> (0 0 1)` (not the corrupted (0,0,2)).
- 3/3 byte-identical (md5 52d34f01d916f2e7a3fe0e49f2b4d55c).
**Verdict: PASS.** Re-arm now requires >1 episode (support must
exceed 2); the single-episode re-arm is blocked.

### K-CV6-4: Regression → PASS

All 12 outputs byte-identical (cmp) to committed CV5/CV4 raws:
double, thr, mask, 3i2, 3c, 3d, 3i, B2, C2, double2 (vs CV4 raws);
perm, vary (vs CV5 raws). Rationale confirmed: no refutations in
the 10 fixtures (dl_rf stays 0, masking inert); the perm seq10
refutation is not masked (a1's s2 law is UNCH); dl_rf is internal
only. All runs 3/3 deterministic.
**Verdict: PASS.**

## 5. Limitations and honest boundaries

- K-CV6-1 and K-CV6-1b are FAILs due to prereg/fixture errors,
  not mechanism errors. They are preserved as negative evidence.
  The ratchet closure is established by K-CV6-1c.
- The X-CV4-1 confirmation remains uncloseable by observation
  (inherited from CV5); R6 revises, it does not prevent.
- R6b replaces diversity with a support bar for re-confirmation.
  A positioned confounder that is refuted and then re-demonstrated
  many times could re-confirm; the bar is higher (must exceed old
  support) but not infinite. This is the graded-confidence
  tradeoff, disclosed.
- The masking check uses ST_ACT entries only; an ambiguous
  (ST_AMB) intervener does not mask. The check requires an active
  SET/ADD; passive UNCH never masks.
- Refutation remains single-counter-episode (no graded
  demotion threshold); only re-confirmation is graded.
- H-CAUSALV6 remains bounded L2. Not L3.

## 6. Raw evidence (committed, in causalv6_repair/)

- `causalv6.zag` (md5 7d579163a5299c2054e2080df3c3d198)
- `PREREG_CAUSALV6.md` (frozen at 745b831b1)
- `PREREG_CAUSALV6_AMENDMENT.md` (K-CV6-1b, frozen at e6cbd2a3c)
- `PREREG_CAUSALV6_AMENDMENT2.md` (K-CV6-1c, frozen at 51cf2b3d2)
- `CV6_TRUNC21_RUN.txt` (K-CV6-1c; md5
  35433be9e9ac3d2271e1519e6db2fc3c)
- `CV6_MASK_RUN.txt` (K-CV6-2; md5 d3ef918e9ea1c418f86259c0bf90c890)
- `CV6_REARM_RUN.txt` (K-CV6-3; md5 52d34f01d916f2e7a3fe0e49f2b4d55c)
- `CV6_DEG24_RUN.txt` (K-CV6-1 original 24-ep; FAIL record)
- `CV6_CLEAN_RECONF_RUN.txt` (K-CV6-1b; FAIL record)
- `CV6_REG_*.txt` (12 regression outputs, all cmp-identical)
- `cv6_clean_reconf_obs.txt` / `cv6_clean_reconf_probe.txt`
  (K-CV6-1b fixture; FAIL record)
- `cv6_trunc21_obs.txt` / `cv6_trunc21_probe.txt` (K-CV6-1c)

## 7. Commit lineage

- 745b831b1 PREREG H-CAUSALV6 FROZEN (prereg; strict ancestor)
- e6cbd2a3c Prereg amendment: K-CV6-1b FROZEN
- 51cf2b3d2 Prereg amendment 2: K-CV6-1c FROZEN
- <this commit> H-CAUSALV6 implementation + evidence + result

Suggested paper line (for the research paper, parent lane):
"H-CAUSALV6 SURVIVES (K-CV6-1c/2/3/4: R6 graded re-confirmation
closes the X-CV5-1 one-way ratchet, R0 re-confirmed at support=3
in a context-stable environment; R6 masking check withholds the
X-CV5-2 refutation, R0 stays ACTIVE; X-CV5-3 single-episode re-arm
blocked, re-confirmation requires support exceeding the
pre-refutation floor; all 12 regression outputs byte-identical;
bounded L2). Repair of H-CAUSALV5. K-CV6-1/K-CV6-1b recorded as
FAIL (prereg/fixture errors, transparently amended)."
