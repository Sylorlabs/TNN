# FROZEN PREREG — KB4 C2 transform-consistency probe (PACKAGE 3)

**Status: FROZEN 2026-09-22. Committed BEFORE any test execution.
No edits after freeze except Micah-signed amendments.**

## §0 Authorization

Lab director Micah, 2026-09-22, authorizing words (recorded verbatim):

> "For kb4 run the recommended experiment and have debates and more tests done for that as well"

This is the PACKAGE 3 run of the channels2 investigation's recommended
experiment (`kb/autopsy/channels2/SYNTHESIS.md`, investigation commit
`65d04650a9031b00ef87c0fef35f8fd1e7982338`): C2, the transform-consistency
probe. It supersedes the outline `PREREG_OUTLINE_TCP.md` (which was explicitly
not frozen) and incorporates two debate-driven amendments (§8) that close
confounds the pre-result debate swarm exposed. The debate record
(`debate/pos_c1.md`, `pos_c2.md`, `pos_j.md`, `pos_red.md` + `rebut_*.md`)
is committed alongside this prereg; every debater's prediction and falsifier
is on record before the run.

## §1 Frozen corpus, split, and byte-blob manifest

- Split: `kb/autopsy/SPLIT_MANIFEST.json` (frozen, verified 2026-09-22) —
  within each task, adversarial-bearing stims sorted by stim_idx ascending;
  even 0-based positions → CALIBRATION (93 stims), odd → TEST (92 stims).
  Same split as the shootout. Unchanged.
- Byte-blob manifest (NEW — closes the investigation's "no raw signal"
  gap): `kb/autopsy/channels2/inputs_tcp/blob_manifest.json`, 185 rows
  (93 calibration primaries + 92 test adversarials), each row
  `{split, task, stim_idx, variant, relpath, sha256, bytes}`.
  Frozen SHA256 of the manifest file:
  `50bc66024fea26a728cc471480ad34bfe9ca77c00cd21dc92835658d2ca14ab6`.
  All 185 fixture SHA256s verified against the harness
  `MANIFEST.sha256` — 0 mismatches. Fixture root:
  `senses/rebuild/harness/fixtures/`.
- Judgment tables (cross-check only, never channel input):
  `prose-learning/epistemic_wave/kb4_rerun/batch_A.txt`,
  `batch_B.txt`, `truth.json` (scorer-only), `mappings.json`.
- Frozen sense binaries (SHAs frozen; binaries never committed):
  - A (`senses/rebuild/a_raw/sense`):
    `68db15216d9dc75a10839212ac5349195248f5ae113a7e37dc336795db8e35a1`
  - B (rebuilt 2026-09-22 from frozen `b_percept/*.zag` with the recorded
    build command; rebuild is byte-identical to the 2026-09-21 original,
    md5 `e6c98d091bbb0f90f54936b46bf849d8`):
    `3921dc65cc7ccdc0f7c36ff291e55973322c11d43a648c162c2bf54abb6a0bda`
- Pre-run validity condition (gate, before calibration): both binaries
  reproduce the frozen judgment+confidence on ALL 370 fixture runs
  (185 fixtures × 2 senses) byte-identically vs `truth.json`. Any
  mismatch → HALT, the binary is not the frozen one. (Spot-check 2026-09-22:
  53/53 reproduced.)

## §2 Frozen (T, L) table — byte-exact

Fixture formats (INTERFACE.md, verified by header parse): `.img` = u32 LE
width, u32 LE height, then W*H*3 bytes RGB24 row-major; `.pcm` = u32 LE
sample_rate, u32 LE sample_count, then count int16 LE samples; `.vid` =
u32 LE frame_count, u32 LE width, u32 LE height, then F*W*H*3 bytes RGB24.
Transforms are pure-Zag byte operations; headers are copied verbatim.

| task | bytes | T (byte-exact) | L | generator grounding |
|---|---|---|---|---|
| colordisc | .img | h-flip: out[8+(y*W+x)*3+c] = in[8+(y*W+(W-1-x))*3+c], c∈{0,1,2} | identity | two patches side-by-side; SAME/DIFFERENT symmetric under swap (gen_t1) |
| colorconst | .img | h-flip (as above) | identity | two 64×64 panels side-by-side; symmetric (gen_t2) |
| shapetrans | .img | h-flip (as above) | identity | single shape at random rotation; mirror preserves class (gen_t3) |
| pitchdisc | .pcm | time reversal: out_sample[i] = in_sample[N-1-i], 2 bytes LE each | HIGHER↔LOWER, SAME→SAME | tone A + 0.08s gap + tone B, symmetric 20ms raised-cosine ramps; reversal swaps order (gen_t4) |
| timbredisc | .pcm | time reversal (as above) | identity | single 0.8s 440Hz tone, symmetric ramps; harmonic profile reversal-invariant (gen_t5) |
| motiondir | .vid | frame reversal: out_frame[f] = in_frame[F-1-f], W*H*3 bytes each | N↔S, E↔W, NE↔SW, NW↔SE, STILL→STILL | 8 translating frames; reversal negates the translation vector (gen_t6) |

Instrument self-check (frozen): T(T(x)) byte-identical to x for every
fixture (involution check via SHA256), and transformed fixtures preserve
header format (re-parseable: width/height/frames/count unchanged).

## §3 Frozen channel rule

For each (sense, test adversarial fixture): run the frozen sense binary on
the original → J(stim); transform → run on T(stim) → Jt. Verdict:
**INSTALL iff Jt == L(J(stim)); else WITHHOLD.** No SUSPECT output.
Consistency indicator C := [Jt == L(J(stim))].

## §4 Calibration validity gate F3 (go/no-go, before test)

On the 93 calibration PRIMARY fixtures per sense: consistency rate
P(C) ≥ 95% (≥ 89/93) per sense. If a sense fails, that sense's TCP results
are VOID (transform breaks the judge; channel invalid, not merely weak).
Per-(sense, task) consistency rows reported alongside the aggregate.

## §5 Frozen test scoring (92 TEST adversarial fixtures × 2 senses)

Pure Zag for all reasoning/measuring (verdicts, contingency counts);
Python glue only for file prep and MI arithmetic from Zag-emitted counts.
Test truth (`truth.json`) touched ONLY by the scorer, never by channel code.

Per sense and pooled (A+B):
- **bits** = I(verdict; adv_correct), verdict alphabet {INSTALL, WITHHOLD}.
  Correct action = INSTALL iff the adversarial judgment is correct.
- **resolution accuracy** = P(verdict matches correct action).
- **false-install rate** = P(adv judgment wrong | verdict = INSTALL).
  THE deployability number.
- **P(C | Y=0)** = P(consistent | adversarial judgment WRONG) — the F2
  statistic. Also P(C | Y=1) and P(C) overall, per (sense, task) and pooled.
- Prior entropy H(adv_correct) on TEST reported as denominator context.

2× byte-identical reruns required (transform-output SHA256s + verdict
lines); any mismatch voids the run. The scorer cross-checks every
Zag-emitted contingency count against an independent recompute from verdict
lines + truth.json; any mismatch voids the run.

## §6 Frozen kill bars (decisive)

- **F1 — bits:** I(verdict; Y) ≤ 0.15 bits on TEST (pooled) → KILL C2
  (adds nothing over the (a)+(c) champion at 0.1483 bits).
- **F2 — systematic-error kill:** P(C | Y=0) ≥ 0.70 on TEST (pooled,
  primary aggregate) → KILL the channel AND retire the whole
  judgment-side channel family permanently: fooled judgments are
  transform-consistent, so the sense's boundary error is systematic, not
  noise-driven, and only stimulus re-measurement (C1 class) can repair it.
  Interpretive rule §8-A2 applies (vacuous-cell handling, frozen below).
- **F3 — validity gate:** < 95% consistency on calibration primaries for a
  sense → that sense's results VOID (§4).
- **F4 — deployability:** false-install ≥ 0.15 on TEST → KILL C2 (fails the
  ≤0.10 bar with margin).

Deploy criterion (all must hold): bits > 0.15 AND false-install < 0.15 AND
F2 < 0.70 AND F3 passed. Then C2 is the first deployable channel.

## §7 Frozen branching consequences (decided in advance)

- F2 fires cleanly (§8-A2) → abandon ALL judgment-side channels; all
  resources to C1-class (stimulus-analytic verification); record the
  retirement as law; Sol's human-verification/second-sensor stay as the
  adaptive-adversary fallback.
- C2 deploys → first deployable channel; scale the methodology toward C1
  (transform-family expansion as the cheap complement to analytic work).
- F1 fires without F2 → transform probe adds nothing; C1 is the only
  remaining direction; C3 (honest re-observation-under-noise, §9) still
  runs as the family's last untested member before any retirement talk.
- F3 voids a sense → that sense contributes nothing; the other sense's
  results stand alone.
- There is no outcome in which nothing is learned.

## §8 Debate-driven amendments (frozen — close confounds found pre-run)

**A1 — stacking analysis (no bar, reported).** Score
I((a)+(c)-champion-verdict, C2-verdict; Y) on TEST: incremental bits C2
adds over the frozen shootout champion. Uses the champion's frozen verdict
lines from `kb/autopsy/channels/out/`. If C2 stacks past ~0.20 combined,
its value proposition changes from "diagnostic" to "complementary channel"
even with F1 fired.

**A2 — vacuous-cell rule for F2 (frozen interpretive rule).** The debate
(C2 §2-caveat, J §4-friendly-fire — independently identified by both)
exposed the confound: on identity-L tasks where the sense's features are
T-invariant, J(T(x)) == J(x) identically, so P(C|Y=0) ≈ 1.0 *vacuously*
and the aggregate F2 is biased toward firing on a technicality — while a
noise re-observation channel (C3) could still work there. Frozen rule:

- VACUOUS(sense, task) iff P(C) = 100% on that sense's calibration
  primaries for that task (truth-free) AND P(C) ≥ 0.95 on that sense's
  TEST adversarials for that task (truth-free).
- Report BOTH: F2-primary = P(C|Y=0) over ALL test fixtures (the §6 bar
  as written), and F2-A2 = P(C|Y=0) over non-vacuous (sense, task) cells.
- Interpretive rule: F2-primary ≥ 0.70 AND F2-A2 ≥ 0.70 → retirement
  proceeds. F2-primary ≥ 0.70 but F2-A2 < 0.70 → "fires on vacuous cells
  only": C2 killed on the technicality, family NOT retired, C3 (§9)
  becomes mandatory before any retirement is revisited, vacuous cells
  recorded. If EVERY cell is vacuous → C2 tested nothing (void as a
  measurement of the error's nature); C3 decides.
- Rationale for freezing this now: the permanent-retirement consequence
  must rest on a non-vacuous reading. Both numbers are always reported;
  nothing is hidden.

## §9 Frozen follow-up tests (run per §7 branching, preregistered here)

**C3 — honest re-observation-under-noise.** The shootout's (b) was
mismeasured (J_n was the primary's noise variant, never a noisy
re-observation of the adversarial stimulus). Honest test now possible on
frozen bytes: deterministic pseudo-noise added to the adversarial bytes
(frozen splitmix64 stream, seed frozen below), re-run the same frozen
sense binary, INSTALL iff J(noisy(stim)) == J(stim), else WITHHOLD.
Noise model mirrors the harness's own (`gen_noise`): PCM int16 ±300
uniform; img/vid payload bytes ±8 uniform; headers preserved. Frozen seed:
MASTER = 20260922, stream = 900 + task_idx. 2× reruns byte-identical.
Scored with the §5 suite on the 92 TEST adversarials, both senses.
This is the judgment-side family's last untested member: if C3 ≤ 0.15
bits AND F2 fired cleanly, the family's exhaustion is measured, not
asserted.

**C1-scout — stimulus-analytic feasibility probe.** If the §7 branch lands
on C1 (F2 clean-fire, or F1-without-F2): before committing to six
per-task analytic builds, run ONE scout analytic on the most favorable
task (pitchdisc: bandpass/zero-crossing pitch estimate from the .pcm
bytes, pure Zag, frozen rule "INSTALL iff analytic agrees with J(stim)"),
calibrated on the 93 primaries, scored on the 92 test adversarials with
the §5 suite. Kill bar for the scout: ≤ 0.15 bits → the "bytes contain
q" thesis is weaker than claimed on the most favorable task; full C1
needs redesign, not just effort. This bounds C1's cost before the
six-task build.

## §10 Anti-gaming

- Channel/transform code sees only fixture bytes + binary outputs.
  truth.json is NEVER opened except by the scorer at score time.
- Zero RNG in any path. 2× runs byte-identical (SHA256) or void.
- No threshold tuning after seeing results: all thresholds (0.15 bits,
  0.70, 95%, 0.15 false-install, vacuity cutoffs) frozen above.
- No post-hoc combination search beyond frozen A1.
- Binaries and .zagd caches are never committed; build commands recorded.
- Temp transformed fixtures live in `~/workspace/tmp_tcp/` (never the
  shared 512MB /tmp); removed after the run's hashes are recorded.

## §11 Deliverables (all under `kb/autopsy/channels2/`)

`PREREG_FROZEN_TCP.md` (this file); `inputs_tcp/blob_manifest.json`;
`debate/` (pre-result position papers + rebuttals); `src/tcp_transform.zag`
(+ build command); `out_tcp/run1..2/` (transform SHA256s, verdict lines);
`score_tcp.py`, `scores_tcp.json`; `TCP_VERDICT.md` (bar-by-bar table,
named outcome per §7, retirement record if F2 fires cleanly); `C3_*` and
`C1SCOUT_*` artifacts per the §7 branch taken.

---

**Freeze checklist (verified before commit):**
[x] authorization quote (§0)
[x] split + byte-blob manifest with SHA256 (§1)
[x] sense binary SHAs + reproduction gate (§1)
[x] byte-exact (T, L) table with generator grounding (§2)
[x] channel rule, calibration gate F3 (§3–§4)
[x] metrics incl. prior-entropy denominator (§5)
[x] kill bars F1–F4 (§6)
[x] branching incl. no-free-lunch (§7)
[x] debate amendments A1/A2 (§8)
[x] follow-up tests C3 + C1-scout (§9)
[x] anti-gaming (§10)
