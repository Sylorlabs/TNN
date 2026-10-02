# H-CAUSALV4 Repair Result

**Date:** 2026-09-29 (PDT)
**Lane:** repair of H-CAUSALV3 after independent red-team downgrade
**Verdict: H-CAUSALV4 SURVIVES (K-CV4-1, K-CV4-2, K-CV4-3 all PASS)**
**Classification:** bounded L2, narrowed. Not L3.

## 1. What was broken (H-CAUSALV3 red team, 2026-09-29)

- **X-CV3-1 (genuine-change double confounder):** SUCCEEDED. Two
  positioned action-1 episodes (seq3, seq7, both in state (0,0,0))
  each preceded a genuine law-change flip (a0 at seq4 s2 0->2, a2
  at seq8 s2 0->2). R1a's genuine-change gate passes, delay_clean's
  correlational cross-check passes (confounders are "clean"), R1b's
  outcome-aware key matches. The second confounder CONFIRMED the
  first to ACTIVE; the harm probe predicted (0,0,2), WRONG.
  Root cause: correlation is perfect even globally, so NO
  correlational check can discriminate a positioned confounder
  from a genuine delayed cause.
- **X-CV3-3:** boundary (vacuous unanimity), not repaired here.
- **X-CV3-2, X-CV3-4:** defense holds, regression holds.

## 2. Preregistration and governance

- `PREREG_CAUSALV4.md` frozen and committed at **4036f4d3b**
  before any implementation, build, or run existed.
  Ordering verified: prereg commit is a strict ancestor of the
  result commit (merge-base --is-ancestor).
- `causalv4.zag` is a byte-verified copy (cmp) of committed
  `causalv3.zag` plus exactly the frozen R4 change. No other
  mechanism change.
- Pure Zag throughout. No Python at any stage (prereg, edits,
  fixtures, builds, runs, greps, hashes, cmp). Toolchain:
  znc 2026.07.0-dev (edition 2026). Binaries built in /tmp/cv4
  only, never committed.
- Only H-CAUSALV4-owned paths staged/committed
  (docs/lab/research-lead/overnight-20260928/causalv4_repair/).
  Concurrent workers' files untouched. No broad git add.
- Determinism: every fixture run 3/3, byte-identical.
- No em dashes in loop documentation.

## 3. The repair (R4: cause-context diversity for confirmation)

A delay rule is a causal claim ("action xa causes var v := nv
with delay d"). R4 adds a minimal causal-robustness requirement:
the correlation must hold across varying background contexts.

- Each delay rule stores its CREATION cause context: the state
  triple (s0,s1,s2) of the episode at seq-d when the rule was
  created (the state in which the cause action was observed).
  New memory O_DL_CS (16 rules x 3 bytes) at 8884; O_CD_* and
  O_N* shifted; WSZ 8936 -> 8984.
- New helper `cause_state_at(W, cseq, out)`: state triple of the
  episode at sequence cseq (1 if found, 0 otherwise; delay_clean
  already guarantees existence).
- In `dl_add_or_support`, PROVISIONAL->ACTIVE promotion now
  requires, in addition to support>=2, that the confirming
  support's cause context differ from the creation context in at
  least one coordinate. If identical, the support IS recorded
  ("supported at seq .." emitted as before) but the rule REMAINS
  PROVISIONAL (inert on predictions) with the diagnostic:
  `# delay rule R<n> NOT CONFIRMED at seq <s>: cause context
  identical to creation; remains PROVISIONAL`.
  The check runs on every support while PROVISIONAL, so a later
  diverse support promotes normally.
- The CONFIRMED emit message is UNCHANGED when diversity holds.

Why this is principled, not pattern-matching: the X-CV3-1
confounder repeats in an IDENTICAL cause context (both positioned
a1 episodes in state (0,0,0) as no-ops); the frozen 3D genuine
delay has DIVERSE contexts (seq5 cause in (0,0,0), seq9 cause in
(2,0,0)). An adversary that varies the cause context defeats R4,
but that is a strictly stronger attack (new red-team surface),
not the frozen X-CV3-1.

Deferred (considered, documented in prereg): delay attribution
competing with the contest machinery. The global contest is
action-blind and resolves OLD-LAW-WINS 3-1 on the X-CV3-1 stream,
so naive competition does not kill the attack; per-action
contests are a redesign, not a repair; and opening contests on
explained vars would alter the frozen 3D trace.

## 4. Frozen kill bars: all pass

| Bar | Result |
|---|---|
| K-CV4-1: X-CV3-1 fixture, R0 not confirmed, probe uncorrupted | PASS: `# DL R0 cause=1 d=1 var=s2 fx=SET(2) st=PROV support=2`; diversity diagnostic present; `Q (0 0 1) \| 1 -> (0 0 1)` (truth; was (0,0,2) under CV3). 3/3 byte-identical. |
| K-CV4-2: all 9 K-CV3 fixtures byte-identical | PASS: double, thr, mask, 3i2, 3c, 3d, 3i, B2, C2 all cmp-identical to committed CV3_*_RUN.txt. 3D still CONFIRMS R0 at seq 11 (contexts (0,0,0) vs (2,0,0) diverse) with the identical CONFIRMED message. |
| K-CV4-3: determinism | PASS: 3/3 byte-identical on all fixtures. |

## 5. Raw evidence (committed, in causalv4_repair/)

- `CV4_DOUBLE2_RUN.txt` (K-CV4-1; 3/3 byte-identical; md5 recorded below)
- `CV4_DOUBLE_RUN.txt`, `CV4_THR_RUN.txt`, `CV4_MASK_RUN.txt`,
  `CV4_3I2_RUN.txt`, `CV4_3C_RUN.txt`, `CV4_3D_RUN.txt`,
  `CV4_3I_RUN.txt`, `CV4_B2_RUN.txt`, `CV4_C2_RUN.txt`
  (K-CV4-2; each cmp-identical to the committed CV3_*_RUN.txt)
- `causalv4.zag` (md5 f640a57f3690b7ab1da320dc238350ad)
- `PREREG_CAUSALV4.md` (frozen at 4036f4d3b)

## 6. Limitations and honest boundaries

- R4 raises the bar but does not close the genuine-change
  confounder class: an adversary that positions confounders in
  varying cause states defeats the diversity check. This is
  explicit new attack surface for the independent red team.
- R4 does not address the X-CV3-3 vacuous-unanimity boundary
  (single covering candidate predicts alone). Unchanged from CV3.
- H-CAUSALV4 remains bounded L2: the repair closes a
  harm-capable confirmation flaw; it does not advance the
  learning level. Not L3.

## 7. Commit lineage

- 4036f4d3b PREREG H-CAUSALV4 FROZEN (prereg; strict ancestor)
- <this commit> H-CAUSALV4 implementation + evidence + result

Suggested paper line (for the research paper, parent lane):
"H-CAUSALV4 SURVIVES (K-CV4-1/2/3: genuine-change confounder
confirmation closed via cause-context diversity; all 9
regressions byte-identical; bounded L2). Repair of H-CAUSALV3."
