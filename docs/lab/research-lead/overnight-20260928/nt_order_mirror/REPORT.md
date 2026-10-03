# REPORT: NT-ORDER-MIRROR -- order-dependence mirror: RARE link taught FIRST tenure-protects

## Verdict

**MIRROR-CONFIRMED** per the frozen verdict mapping (PREREG
Section 8). K1, K2, K3, K4, K5, K6 all hold. This is the
preregistered directional prediction (tenure-protection
hypothesis), and -- like NT-LOWVALUE-BOUNDARY before it -- EVERY
frozen numeric prediction matched exactly, including the full
per-pass probe series on all four arms and all four eviction
histograms.

## Frozen results (3/3 byte-identical)

- Run digest: `9d7626e4f552bd1b48c09305c0f252174edb5e1949b467bfbbd08c279516d91d`
- Binary digest: `eeed45d15ad6d4046f9b28d9c5e402bb2f803b7fa9805c6f69eebd53c11c674f`
- Source digest: `889f14acf7cd0e8bc15e560af735934c51d0ff071c7728bc8641daf0e9447cbd`

```
NTOM P1 ttcA=2 probeA=8 nevict=11 phev=0
NTOM P1 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTOM P1 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTOM P1 EVHIST 143=6 144=5
NTOM P2 ttcA=2 probeA=8 nevict=11 phev=0
NTOM P2 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTOM P2 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTOM P2 EVHIST 143=6 144=5
NTOM P3 ttcA=2 probeA=8 nevict=11 phev=0
NTOM P3 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTOM P3 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTOM P3 EVHIST 143=6 144=5
NTOM P6 ttcA=2 probeA=8 nevict=11 phev=0
NTOM P6 PPROBE p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail=4
NTOM P6 RET c=2 nc=2 u=4 forget=0 bprobe=2
NTOM P6 EVHIST 143=6 144=5
NTOM K1=1 K2=1 K3=1 K4=1 K5=1 K6=1
NTOM VERDICT=MIRROR-CONFIRMED
```

Prediction vs actual: NO misses. avail 4/4/4/4; nevict 11 on all
arms; EVHIST 143=6, 144=5 on all arms with evh(148) = 0 on all arms
(the 148 bin is absent from the printed histogram because it is
exactly zero); final c = 2/2, forget = 0, nc = 2, u = 4 on all arms;
bprobe = 2/3 on all arms; phev = 0 on all arms. The prereg
hand-traces (Sections 5.1-5.4) reproduced the binary exactly on all
four arms.

## Kill-bar evaluation

- K1 (learnability): PASS. ttcA = 2 (1..50), probeA = 8/8, all four
  arms. No VOID.
- K2 (retention of uncontested structure): PASS. nc = 2/2, u = 4/4,
  all four arms. The teach-order change does not disturb
  agreed/shared/untouched chains.
- K3 (the mirror bar: order-dependent availability): PASS.
  avail = 4, 4, 4, 4 for K = 1, 2, 3, 6, exactly as traced. The
  tenure-protection prediction holds: the RARE link is present on
  every scored pass in every arm.
- K4 (final revision outcome): PASS. c = 2/2, forget = 0 on ALL four
  arms (in NTLV only P1 held this; here even K=6, taught once,
  retains q(100) = 152 at retest).
- K5 (pressure exercised, eviction discipline, mechanism
  attribution): PASS. nevict = 11 on all arms; phev = 0 on all arms
  (zero phase-1-link subjs evicted); evh(148) = 0 on all arms
  (white-box confirmation that D2 NEVER evicted the first-taught
  RARE link); EVHIST exact 143 = 6, 144 = 5 on all arms (the churn
  moved entirely to the 143/144 revolving pair).
- K6 (discriminative validity): PASS. avail(P1) = 4 (the probe
  passes when the link is present; not a broken probe) and
  nevict = 11 > 0 on all arms (pressure actually exercised).

## What this establishes

1. **Installation recency, not reinforcement frequency, is the true
   determinant of D2 victimhood.** The mirror image of the NTLV
   churn trap reproduced exactly: teaching the RARE link FIRST
   flips availability from 4/2/1/0 to 4/4/4/4 across K = 1, 2, 3, 6,
   with the learner, workload, capacity, and K-sweep all unchanged.
   The only degree of freedom that moved was teach order, and the
   frozen rules predicted the full outcome -- including the shift of
   the revolving churn pair from 144/148 to 143/144 and the exact
   per-arm eviction counts -- before the binary was built.
2. **The NTLV churn-trap attribution is causally validated.** The
   mechanism account said: the RARE link died because it was
   re-installed YOUNG (max ins) on every re-teach pass, and D2
   evicts the youngest. The mirror confirms the contrapositive from
   the same rules: installed first, the RARE link holds the LOWEST
   novel ins of the pass; every later novel installation stamps a
   higher ins; D2's max-ins victim is never it (evh(148) = 0).
   Tenure protection engages from the first installation because
   non-teach passes do not re-install it young -- they simply do not
   touch it. Both directions of the causal claim now have exact
   frozen-rule traces and byte-identical binaries behind them.
3. **The failure is D2's usefulness-blindness, confirmed from both
   sides.** In NTLV the genuinely useful link was evicted because it
   was young; here it is retained because it is old. Neither outcome
   consulted usefulness: 148's survival here is luck of install
   order, not usefulness-awareness. A usefulness-aware policy would
   pin 148 in BOTH orders; D2 protects it in exactly one. The mirror
   does not redeem D2 -- it sharpens the liability claim by showing
   the policy is purely recency-driven.
4. **Frequency is screened off.** K=6 (taught once, sup=1) has
   identical availability, retest, and eviction statistics to K=1
   (taught every pass, sup=6): with 148 installed first, one
   installation suffices for full availability over the scored
   window. Reinforcement frequency contributes nothing once
   installation order is fixed -- the strongest form of the
   recency-not-frequency conclusion.

## What broke / what needed to change

Nothing in the rule set broke: the D1+D2 port required NO changes
(the cl_* fns are verbatim from ntlv_full.zag; the sole lane change
is teachB's order). One build note carried over from NTLV: kill-bar
helpers kept at most 3-deep if-nesting per the AGENTS.md
third-compiler-defect workaround (arm_k5_ok uses 5 nested 1-deep
ifs, each testing one conjunct -- flat and within the workaround).
The frozen binary was built only from the corrected source. No
prediction was touched after the prereg commit.

## Honest boundaries (from PREREG Section 9, unchanged)

- The LINKS are memorized associations; what is rule-STRUCTURED is
  the family. No rule induction tested; no L2/L3 claim.
- Single capacity point (CAP=20, 1.05x); single contradiction
  magnitude; M=6 fixed, so the per-pass probe series (not the
  aggregate curve) is what separates frequency from phase -- and
  here the series is identical (0,0,1,1,1,1) on all four arms,
  which is itself the finding.
- 148's final sup differs by arm (6/3/2/1) but all satisfy
  sup > ref = 0: the mirror tests PRESENCE, not evidence strength.
- Tenure-protection here is luck of install order, not
  usefulness-awareness (see point 3 above).
- Port covers the associative instance memory only (NT-PORT
  boundary stands).

## Recommended follow-up (not preregistered; for the parent)

- The two lanes together (NTLV liability + this mirror) close the
  order-dependence question for the structured-family workload at
  1.05x pressure. The natural next step is the honest
  alternative-policy comparison neither lane can run: a
  frequency-aware or usefulness-aware eviction rule under a new
  prereg (would need a new rule, i.e., a new lane, not an amendment
  here).
- Interaction with the nt_lifobound INCONCLUSIVE result stands as
  noted in the NTLV report: the structured-family +
  usefulness-probe design discriminates where the key-value
  workload could not.

## Provenance

- Prereg frozen alone: commit `6899bf464` (PREREG.md + NAMECHECK.md
  only), strictly before implementation. Commit-order self-check:
  `git log` shows 6899bf464 strictly precedes the implementation
  commit below; no implementation file existed at prereg time.
- Implementation + results: this commit. Pure Zag, safebin-only
  PATH, pinned znc 2026.07.0-dev (same build as
  NT1/NT-D2/NT-PORT/NT-PRESSURE/NT-PORT-PRESSURE/NT-LOWVALUE-
  BOUNDARY). `which python3` and `which python` return nothing
  under the worker PATH. Zero forbidden-executable invocations.
- Source: `ntom_full.zag`, written to PREREG Sections 2-4 (learner
  fns verbatim from ntlv_full.zag; sole change: teachB teaches 148
  first iff (pass-1) mod K == 0, then the 10 ascending non-RARE
  teachings; per-arm helpers + K1-K6 bars per PREREG Section 7).
- Build: `znc ntom_full.zag -o ntom_bin` under safebin-only PATH
  (exit 0; benign zagd-unavailable warning only, as in NTLV); 3/3
  runs byte-identical (cmp), exit 0, zero stderr.
- Audit: no protection/task-label/freeze/importance/mode logic in
  the learner (the arm/period selector is a harness condition);
  "python" appears only in header comments ("Pure Zag. No Python.")
  and NAMECHECK; compiler-defect workarounds honored (single-buffer
  cursor output + one raw syscall; no `as *i32`+slice; no
  `!(A && B)` in while conditions; if-nesting at most 3 deep;
  no `[]u8 as *u8` casts).
- Commits local only, explicit pathspecs, never pushed.
