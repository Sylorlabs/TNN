# TCP VERDICT — KB4 C2 transform-consistency probe + follow-ups (PACKAGE 3)

**Prereg:** `PREREG_FROZEN_TCP.md` (frozen commit `182fceeb`, before any test
execution). **Debate record:** `debate/` (pre: 4 positions + 4 rebuttals +
`DEBATE_PRE.md`; post: `post_c1/c2/j/red.md`). All committed before/after the
run as appropriate; nothing was re-tuned after seeing results.

## §1 Measured results

### C2 transform-consistency probe (92 TEST adversarials × 2 senses)

| Bar | Measured | Verdict |
|---|---|---|
| F3 calibration gate (≥95%) | A: 93/93 (100%) PASS; B: 77/93 (82.8%) FAIL → B VOID | B's results void; A's stand alone |
| F1 bits ≤ 0.15 kills | **0.0000 bits** (A) | **FIRES — C2 killed.** C2 always INSTALLs: a constant function |
| F2 P(C\|Y=0) ≥ 0.70 | **1.0000** (40/40 fooled fixtures consistent) | **FIRES** |
| F2-A2 (frozen mechanical rule) | **null** — all 6 (A,task) cells vacuous (100% cal + 100% test) | frozen routing: "C2 void as a measurement; C3 decides" |
| F4 false-install ≥ 0.15 kills | **0.4348** | **FIRES — C2 killed** |
| A1 stacking | +0.0000 incremental bits over (a)+(c) champion | no complementary value |

B's per-task calibration: colordisc 15/15, colorconst 10/10, pitchdisc 15/15,
timbredisc 15/15, **shapetrans 16/23, motiondir 6/15** — spatial transforms
break B's judge (spatially-asymmetric features), temporal ones don't.

Determinism: 2× reruns byte-identical (verdict lines + transform SHA256s);
Zag/Python count cross-check 0 mismatches; 370/370 judgment reproductions of
frozen records; involution T(T(x))==x on all 185 fixtures.

### The DPI consequence (measured, accepted by all four debate camps)

On sense A, J(T(x)) == L(J(x)) for **all 92 test + 93 calibration fixtures**.
Therefore every deterministic channel that is a function of (J, Jt) is a
function of J alone and adds **zero** information about Y. This is not an
interpretation — it is a direct consequence of the measured P(C)=1.0, confirmed
by A1's +0.0000. It kills every deterministic re-reading member of the
judgment-side family. The members it cannot touch: (c) confidence (shootout:
0.0797 bits — already dead) and C3's fresh-noise draw.

### C3 honest re-observation-under-noise (preregistered §9; the family's last member)

92 TEST adversarials × both senses. Frozen splitmix64 noise (MASTER=20260922,
stream=900+task_idx): PCM ±300, img/vid payload ±8, headers verbatim.
INSTALL iff J_noisy == J(stim). 2× byte-identical reruns; 0 cross-check errors.

| scope | bits | P(agree) | P(agree\|Y=1) | P(agree\|Y=0) | false-install |
|---|---|---|---|---|---|
| pooled (184) | **0.0049** | 0.918 | 0.939 | 0.894 | 0.450 |
| sense A (92) | 0.0046 | 0.946 | 0.962 | 0.925 | 0.425 |
| sense B (92) | 0.0043 | 0.891 | 0.915 | 0.867 | 0.476 |

**Kill bar (≤0.15) FIRES** — pooled and both senses independently. Judgments are
91.8% noise-stable and that stability is uncorrelated with correctness. The
test set IS the in-band set (adversarial band by construction); the Y=0
conditional shows fooled judgments are just as noise-stable as correct ones.

### C1-scout (preregistered §9; first C1-class step)

Pitchdisc zero-crossing analytic (pure Zag): calibration 15/15 vs generator
truth; test **0.9968 bits** (saturates prior H(Y)), 15/15 resolution accuracy,
**0.0% false-install**. Kill bar (≤0.15) NOT fired. **C1 has a live feasibility
proof** — sense A answered SAME on all 15 test adversarials (effective JND
coarser than the generator's 0.5%); the analytic repairs every miss. Recommend
the six-task build, per-task scout-then-build with the same 0.15-bit bar.

## §2 Verdicts (named per frozen §7)

1. **C2 the channel: DEAD** — killed by F1 (0.0000 bits) and F4 (43.5%
   false-install). It is the constant INSTALL function on sense A; void on B.
2. **F2: FIRED** (1.0000 ≥ 0.70). The frozen A2 mechanical rule routed the
   every-vacuous case to C3 rather than to immediate retirement.
3. **C3: kill bar FIRED** (0.0049 ≤ 0.15, both senses). The family's exhaustion
   is MEASURED.
4. **The judgment-side channel family is RETIRED, permanently.** Deterministic
   re-readings are DPI-dead (C2: 0.0000 bits); the stochastic member is
   near-vacuous (C3: 0.0049 bits); the confidence member was already measured
   at 0.0797 bits. No member clears 0.15 bits. No further judgment-side
   channel variants are to be built or tested. **Recorded as law 2026-09-22.**
5. **Direction: all resources to C1-class** (stimulus-analytic verification).
   The scout is the existence proof (0.9968 bits on pitchdisc). Sol's
   human-verification/second-sensor remains the adaptive-adversary fallback.

## §3 How the retirement was earned (not executed)

- F2 fired at the maximum (1.0), but the frozen vacuity rule's letter routed
  to C3 instead of auto-retiring — the "scheduled accident" the red team
  warned about did not happen; the brake held.
- C3 was the preregistered decider and it confirmed exhaustion on both senses.
- J (the family's defender) pre-committed to sign the retirement recommendation
  if C3 ≤ 0.15 on both senses — condition met (0.0046, 0.0043).
- Red-team pre-committed to stand down if C3 ≤ 0.15 in-band, both senses, scope
  recorded, Micah decides — conditions met (test set is in-band by
  construction; Y=0-conditional agreement reported; scope below).
- C2's advocate concedes the red-team mechanism in full; C1 retracts its
  noise-driven prior. All four camps accept the DPI consequence.
- **Governance note (all four camps agree):** the F2 auto-execution clause
  overreaches as written; the retirement above rests on the measured C3
  exhaustion + F2 + DPI, and the decision itself belongs to Micah. This record
  is the evidence; his word is the law.

**Scope of the retirement (frozen-threat-model only):** one frozen adversary
construction (δ ≲ σ band), two frozen senses, six tasks. It retires the
judgment-side family *for this threat model* — not a claim about all possible
adversaries. A new adversary construction re-opens the question only with a
new preregistered battery.

## §4 Prediction scorecard (post-result debate)

| Camp | F1 | F2 | F3 | F4 | deploy? |
|---|---|---|---|---|---|
| C1 | ✓ fires | ✗ (predicted quiet; noise prior retracted) | ◑ (A green, B void) | ✓ | ✓ no |
| C2 | ✓ fires | ✗ (predicted 0.50–0.65, measured 1.0) | ◑ | ✓ fires | ✓ no |
| J | ✓ fires | ✗ (predicted quiet) | ✓ (a sense voided) | — | ✓ (withdrawn) |
| Red | ✓ | ✓ (predicted spurious fire) | ✓ (whole sense void) | ✓ | ✓ no |

The red team swept the board. Its "spurious" charge vs the DPI reading remains
the deepest unresolved theoretical disagreement — but it no longer matters for
the verdict: DPI + C3 decide the family's fate on measurements, not labels.

## §5 Deliverables

`PREREG_FROZEN_TCP.md`, `inputs_tcp/blob_manifest.json`, `debate/` (9 files),
`src/tcp_transform.zag`, `src/channel_c2.zag`, `src/score_tcp.zag`,
`src/c3_noise.zag`, `src/channel_c3.zag`, `src/c1scout_pitch.zag`,
`src/c1scout_channel.zag`, `src/score_c1scout.zag` (+BUILD_CMD files),
`out_tcp/run1+run2/`, `scores_tcp.json`, `verdict_brief.txt`,
`out_c3/run1+run2/`, `scores_c3.json`, `c3_brief.txt`,
`out_c1scout/run1+run2/`, `scores_c1scout.json`, `c1scout_brief.txt`,
`TCP_VERDICT.md` (this file). Binaries and `.zagd` caches never committed.

**Open next:** the six-task C1 build (scout-then-build per task, 0.15-bit bar
each); the law-review amendment on F2 auto-execution (for Micah).
