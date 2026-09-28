# PREREG — PAM Round 4: New Approaches (program level)

**Date:** 2026-09-24. **Coordinator:** PAM round-4 coordinator (subagent).
**Branch:** `tnn-native-lab` (sylorlabs/TNN). **Status:** FROZEN — committed before
any round-4 fixture, build output, or search result exists. Track-level preregs
(`cu/prereg/`, `wild/prereg/`) refine this document; they may not contradict it.

## 0. Round-3 close (frozen context, not to be re-litigated)

- F5 confirmation path: dead (three attempts, three kills). F5 stands **block-only**.
- MG6: all 6 killed — D1 retention is structural, not a guard problem; retention
  work moves upstream to G1 proposal formation.
- C3 corroborated-revision gate repair: PASS (RK-3′ = 71.78%, zero safety regressions).
- FE2 separator family: SURVIVE 11/11 (264/264 on held-out draws).
- M1 bar calibration: SURVIVE at `conf≥705 ∧ mrgF≥3588` (RK-3 82.58%) — threshold
  adoption NOT decided (see §5).

## 1. Program goal

Micah's directive: try DIFFERENT approaches to PAMs, multiple in parallel, plus
test whether TNN should be CONSCIOUS about its PAMs (deliberately aware of when
a PAM fires, why, what it admitted/rejected) versus UNCONSCIOUS (fast automatic
admission below deliberation, like humans).

Two tracks:
- **CU** (`round4/cu/`): conscious vs unconscious PAM, head-to-head tradeoff test.
- **WILD** (`round4/wild/`): crazy creative risky designs, each with preregistered
  kill bars, run in parallel. Max risk authorized; git history is the safety net.

Hypothesis sources feeding WILD: grok-4.7 (streaming, highest reasoning),
ONE deep batched fable round (fable_stream.py, expensive — one round only),
native muse-subagent debate. Every approach that survives steelmanning gets tested.

## 2. Frozen laws (all tracks)

- Pure Zag for all TNN mechanisms. **Zero RNG in TNN decision paths.**
- Byte-identical reruns: every battery runs ≥2×; any divergence is a defect, not noise.
- Preregister before running: track preregs frozen and committed before fixtures/builds.
- No build binaries or `.zagd` files in commits. No `as []i32/u32/u16` indexed
  casts (ZNC-2026-09-21-007) — `[]u8` arenas with explicit LE accessors.
- Commit convention: `~/workspace/commit_racefree.py tnn-native-lab <msgfile> <files...>`;
  local paths under `~/workspace/tnn-lab/` map to `docs/lab/<relpath>`.
- znc toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- No randomness anywhere means: no seeded LCGs, no hash-salting as entropy, no
  wall-clock-derived decisions. Deterministic given state, full stop.

## 3. Conscious vs unconscious — program-level tradeoff metrics (frozen)

CU must preregister exact numbers, but every comparison below is mandatory,
on the SAME frozen admission tape for both variants:

- **M-speed:** mean admission latency (Zag cycle counts + wall time) per admission.
- **M-resource:** evidence/ledger bytes written per admission; deliberation entries.
- **M-judgment:** correct-admit rate (RK-3-style, frozen denominator) and
  false-admit rate on the frozen wrong set (12 TMB-5 + 9 CC1 pairs, Round-3 frozen).
- **M-attack:** catch rate on a frozen attack tape including provenance-laundering
  (GEN→EXT relabel), forged declarations (Declaration Fork), and forged authority.
- **M-introspection:** can TNN's own deliberation answer "why did you admit X?"
  from its own records? (conscious: yes by construction; test the QUALITY of the
  answer, not just its existence.)

Operational definitions (frozen): **conscious PAM** = every PAM decision emits a
deliberation-visible record (what fired, which rule, evidence cited), queryable by
TNN's own deliberation. **Unconscious PAM** = admission below deliberation, binary
outcome only, no per-decision record.

No single "winner" declared by fiat: report the full Pareto table
(speed × resource × judgment × attack-catch × introspection). Bars for claiming
"conscious wins on X" are preregistered by the CU crew, not here.

## 4. Wild designs — kill-bar schema (frozen)

Each wild design gets its own prereg with: (a) falsifiable claim, (b) kill bars
from this schema (the crew may ADD bars, never remove):

- **K1:** any false-admit on the frozen wrong set (12 TMB-5 + 9 CC1 pairs) → KILL.
- **K2:** fails byte-identical rerun (2×) → KILL.
- **K3:** correct-admit rate >5 pts below the C3-repair baseline (RK-3′ 71.78%)
  with no compensating safety gain → HOLD (redesign), not KILL.
- **K4:** per-admission resource grows superlinearly in stream length → KILL.
- **K5:** deliberation deadlock / non-termination on any fixture → KILL.

Seed designs (hypotheses from grok/fable/debate are ADDED to this list, never
substituted for testing the seeds):
- **W1 PAM-as-organ:** PAM becomes a full organ with deliberation votes.
- **W2 adversarial PAM pairs:** two PAMs with opposed objectives must both agree
  to admit.
- **W3 veto-only PAM:** a PAM that can only reject, never admit; paired with the
  standard admit path.
- **W4 self-training PAM:** PAM deliberately revises its own thresholds from its
  miss log (deterministic, non-RNG revision — state-driven only).
- **W5 PAM-as-memory:** admission decisions stored as memories with
  strength/promotion; PAM queries memory instead of recomputing.
- **W6 arguing PAMs:** N PAM instances debate an admission in bounded
  deliberation; consensus rule preregistered per design.
- **W7 laundering-hunter PAM:** dedicated provenance-laundering detector
  (GEN→EXT relabel), separate from the admission path.

## 5. FROZEN — Round-3 open items (hands off)

The following need Micah's word and must NOT be silently resolved by Round 4.
Any track that touches them FAILS its prereg:

- **(a)** M1 threshold adoption: are `strong`/`agree` free parameters or frozen
  safety machinery? Round-4 designs use the frozen Round-3 bars as-is; no
  recalibration of strong/agree.
- **(b)** Fable's 4 kill-bar repairs (D2, O3, O1-fatal, FE3→FE3a/FE3b split):
  NOT applied in Round 4.
- **(c)** The 3 HELD items (V4 two-tier trial, O2 live machinery, F5
  tightened-window variant): NOT run in Round 4.

## 6. Deliverables

- `round4/cu/prereg/PREREG_CU.md` + battery + `VERDICT_CU.md` (Pareto table).
- `round4/wild/prereg/PREREG_WILD.md` (+ per-design addenda) + `VERDICTS_WILD.md`.
- `round4/hypotheses/grok_pam_r4.md`, `fable_pam_r4.md`, `debate_pam_r4.md`
  (raw hypothesis records, committed).
- Each track commits its own prereg first, then evidence, then verdict — small
  race-free commits, never one giant commit.
