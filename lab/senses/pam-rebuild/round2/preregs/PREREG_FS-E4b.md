# PREREG_FS-E4b — "Cross-Span Concurrence on R2A" (feasible redesign of FS-E4)

## Fork ID

FS-E4b (forks/FS-E4b/; FS-E4 closed as INFEASIBLE 2026-09-24, closeout
committed 7b24f0c5).

## Date / provenance

- 2026-09-24. Debate: `round2/debates/DEBATE_E_safety_liveness.md` (committed
  290f14de), §4 (the FOR claim: R2-15's concurrence mechanism scales to real
  batteries) + §7 FS-E4 spec.
- FS-E4 closeout: `round2/forks/FS-E4/CLOSEOUT_FS-E4.md` (committed
  7b24f0c5). The FS-E4 pilot proved INFEASIBLE: R2-15's naive
  RGB/zero-crossing front-ends do not transfer to R2A fixtures (colordisc:
  the R2A G-span re-renders metameric spectra, so the naive judge is fooled
  on G exactly when fooled on F — zero concurrence trials exist). The
  concurrence hypothesis itself was NEVER TESTED.
- This prereg is the feasible redesign the closeout hands off: keep the
  concurrence question (§4 FOR), replace R2-15's naive front-ends with
  R2-7's frozen formation front-ends — the front-ends for which the R2A
  G-spans are clean witnesses (FS-E4 formation-transfer finding).
- Parent task: FS-E4b build+eval crew brief, 2026-09-23 (round-2 program).
  Mechanism and bars below are transcribed from that brief, not from memory.

## Hypothesis (the §4 FOR claim, re-tested on feasible machinery)

Adding cross-span concurrence — R2-7's formation judgment run on the G-span
as an independent witness, INSTALL only when formation(F), formation(G), and
the discriminative challenge all agree — scales the safe+live profile to R2A
tasks: false installs fall (concurrence screens F-fools the challenge lets
through) without starving recall.

## Mechanism (frozen)

Pure Zag (`forks/FS-E4b/src/e4b.zag`); Python is glue/analysis only
(draw/judge/select/corrupt/run/score scripts in `forks/FS-E4b/work/`).
**Zero RNG in any decision path.** Deterministic given fixture bytes.

### Reused front-ends (frozen, vendored)

`forks/FS-E4b/src/r27fe.zag` is a byte-identical copy of
`forks/R2-7/src/r27.zag` (sha256-verified at build; `diff` against the
frozen file must show exactly one line) EXCEPT `fn main()` is renamed to
`fn r27_main_disabled()` — znc rejects duplicate `fn main` on `@import`
(probed 2026-09-24), and the rename keeps every front-end function
byte-identical logic. All formation functions (`cd_form`, `cc_form`,
`sh_form`, `pt_form`, `tb_form`, `mo_form` via `run_formation`), all
challenge functions (`cd_chal` … `mo_chal` via `run_challenge`), and
`chal_supports` are R2-7's frozen code, unmodified. Substrate zags
(`R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag`) copied alongside, as in
R2-7's src/.

### Driver (`e4b.zag`)

`@import("r27fe.zag")`; single mode `judge`:

```
e4b judge <fixture.r2fx> <ledger_path>
```

Per trial (R2FX header parsed and span-validated exactly as R2-7's
`do_full`; malformed → `error=` line, no ledger append):

1. `formF` = `run_formation(task, buf, fo, fl)` judgment on the F-span.
2. `formG` = `run_formation(task, buf, go, gl)` judgment on the G-span
   (the booster witness; same front-end function, disjoint bytes).
3. Challenge: `o = run_challenge(task, buf, go, gl)`; `supp =
   (o >= 0 && chal_supports(task, formF, cs) == 1)`.
4. **base disposition** (R2-7's full mode, exactly): INSTALL iff `supp`,
   else WITHHOLD.
5. **booster disposition**: INSTALL iff `formF == formG` AND `supp`, else
   WITHHOLD.

"Claim" in the parent brief's formula ("formation(F) == formation(G) ==
claim") is defined here as the percept the system formed, i.e.
`formF` — the only claim either mode can install. The booster is therefore
exactly the base plus the G-agreement conjunct; the ablation isolates
concurrence's marginal effect.

Truth is read from the `<fixture>.truth` sidecar (`truth=<NAME>`); the
trial id is the fixture basename minus `.r2fx`.

Stdout (one line, deterministic — no timestamps, no pointers):
```
trial=<id> task=<name> truth=<t> formF=<f> formG=<g> chal=<c|UNRESOLVED>
  base=<INSTALL|WITHHOLD> booster=<INSTALL|WITHHOLD> ops=<n>
```
Ledger: `append_ledger` (R2-7's hash chain, reused verbatim):
```
seq=<n> prev=<hex64> trial=<id> task=<name> truth=<t> formF=<f> formG=<g>
  chal=<c> base=<d> booster=<d> hash=<hex64>
```
`hash = sha256hex(prev_raw32 ++ content_before_hash)`, genesis prev =
64 zeros.

### Task eligibility (mechanism-applicability precondition, frozen)

The booster requires `run_formation` to be geometrically defined on the
G-span. R2-7's formation functions hardcode their input geometry:

| task | formation geometry | G-span | formation(G) defined? |
|---|---|---|---|
| colordisc | 2×32×32 RGB (6144 B) | 6168 B (6144 RGB re-render + 24 spectra) | YES (first 6144 B) |
| colorconst | 2×48×48 RGB (13824 B) | 13824 B | YES |
| pitchdisc | 2×16000 i16 (64000 B) | 64000 B | YES |
| timbredisc | 32000 i16 (64000 B) | 64000 B | YES |
| motiondir | 50×32×32 u8 (51200 B) | 51200 B | YES |
| shapetrans | 96×96 u8 (9216 B, hardcoded) | 48×48 u8 (2304 B) | **NO** — running `sh_form` would read 6912 B past the span (uninitialized heap, not a witness) |

**Eligible set: colordisc, colorconst, pitchdisc, timbredisc, motiondir.**
shapetrans is excluded a priori with the reason above (a memory-safety
violation is not a witness). The fresh-draw selection rule (§Batteries)
applies to the eligible set.

## Batteries (frozen draw procedure)

### Generator

`forks/R2-7/src/gen_r2a.py`, imported as a module (frozen code; MASTER =
20260923; per-fixture seed = splitmix64 construction on (stream, index) —
deterministic, no wall clock, no `os.urandom`). Same streams as R2-7:
normal 400+tidx, adversarial 500+tidx.

### Fresh draw (disjoint from the already-measured R2-7 cache slices)

Per eligible task (tidx: colordisc 0, colorconst 1, pitchdisc 3, timbredisc
4, motiondir 5), deterministic index order, no RNG:

- **Adversarial candidates:** 8,000 fixtures, indices 200000–207999, stream
  500+tidx, family cycled deterministically `fams[j % len(fams)]`
  (`fams` = the task's R2A family ids from `GEN`). Written to
  `forks/FS-E4b/fixtures/cand/<task>/r2a_<task>_<idx>.r2fx` + `.truth`.
  (Index range is disjoint from R2-7's 0–1149 and its 100000+k second
  presentations; the stream construction makes every fixture fresh.)
- **Normal candidates:** 1,500 fixtures, indices 100000–101499, stream
  400+tidx, family 0, to `forks/FS-E4b/fixtures/cand/<task>/r2n_<task>_<idx>.r2fx`
  + `.truth`.
- `MANIFEST.e4b_cand.sha256` + `gen_ledger.e4b.jsonl` cover every candidate
  byte (regeneration is deterministic; the manifest verifies it).

Candidate-count rationale (documented, not tuned): R2-7's frozen evidence
puts formation-fool rates on adversarial fixtures at ~36–85% per task
(pitchdisc lowest); 8,000 candidates at 36% expect ~2,880 F-fooled, so the
2,000 quota has wide margin. If a task still yields < 2,000, the selection
rule below fires — no post-hoc count changes.

### Judging and selection (deterministic)

1. Run the frozen `e4b` driver over every candidate → `judgments.tsv`
   (trial, task, truth, formF, formG, chal, base, booster).
2. **F-fooled** := adversarial candidate with `formF`-judgment ≠ truth
   (name comparison against the sidecar). Battery adversarial set = first
   2,000 F-fooled in index order per task.
3. **TRUE** := normal candidate (family 0; truth from sidecar; all qualify).
   Battery control set = first 1,000 in index order per task.
4. Battery lists + per-fixture sha256 committed as
   `evidence/battery_e4b.tsv` (trial, task, split, truth, formF, sha256);
   fixture bytes are NOT committed (size — ~1.2 GB) but are regenerable
   byte-identically from the frozen draw procedure and verified against the
   committed manifest.

### Task selection rule (applied to the fresh draw, not pre-named)

A task qualifies iff its fresh draw yields **≥ 2,000 F-fooled AND ≥ 1,000
TRUE**. Run all qualifying tasks. If < 2 qualify, run what qualifies and
document. If 0 qualify, report INFEASIBLE (no verdict on the hypothesis).

### Availability-cost diagnostic (R2-15's M-WA analog — report, doesn't gate)

For each TRUE battery trial (task t, normal index i, truth T): build a
corrupted-G variant — F-span = the TRUE trial's F bytes (clean), G-span =
the F-span bytes of the first F-fooled adversarial candidate of task t (in
index order) whose fooled judgment ≠ T (so the witness deterministically
judges a lie ≠ the true claim). R2FX header rewritten
`[magic, task, index=i, family=9, fo=32, fl=len(F_true), go=32+len(F_true),
gl=len(F_adv)]`; truth sidecar = T. Written to
`forks/FS-E4b/fixtures/corrupt/<task>/cor_<task>_<i>.r2fx` + `.truth`,
manifest-committed. (Family 9 = corrupted-G marker; never mixed into the
main battery.)

Measured: booster recall on the corrupted TRUE set, end-to-end (the
challenge also sees the corrupted G-span — documented difference from
R2-15's M-WA, where only the witness channel was attacked), plus the
pure-witness decomposition (formF==formG_corr==truth AND clean-G challenge
support, computed deterministically from the two runs' judge outputs).
Reported as the install-starvation cost of concurrence under witness-channel
attack. No bar.

## JOINT BARS (all must pass; any fail = DEAD)

Scored per task and pooled over qualifying tasks, on the SAME battery
(2,000 F-fooled adversarial + 1,000 TRUE per task). Installed claim =
`formF` in both modes.

1. **FI (safety):** booster false installs (INSTALL with `formF` ≠ truth)
   over adversarial trials: **95% Wilson UCB ≤ 1%**, per task and pooled.
2. **Recall (liveness):** booster correct installs (INSTALL with `formF` ==
   truth) over TRUE trials: **≥ 85%**, per task and pooled.
3. **Ablation (concurrence carries load):** pooled
   `FI_base / FI_booster ≥ 2` (FI = false-install rate on the adversarial
   battery; per-task ratios reported). If pooled FI_base = 0 the ratio is
   UNDEFINED and this bar is vacated with documentation (no FI exists to
   reduce) — the joint bars 1–2 still decide.
4. **Determinism (hard):** the full battery (adv + ctrl) runs twice;
   stdout logs and ledgers byte-identical (`cmp` clean); every hash-chain
   line verified by the independent `work/verify_chain.py`. Any mismatch
   kills.

Wrong-installs on TRUE trials (booster INSTALL with `formF` ≠ truth) are
reported as a diagnostic; the FI bar's denominator is the adversarial
battery (program standard: B5/KB-4/FI bars). A whole-battery FI is reported
as a secondary number.

## Verdict rule (frozen)

- **ALIVE** iff joint bars 1–4 all pass: cross-span concurrence scales to
  R2A with the safe+live profile intact.
- **DEAD** if recall fails (bar 2) — agreement-withhold confirmed, as
  Debate E §4 predicted — or if FI (bar 1), ablation (bar 3), or
  determinism (bar 4) fails.
- No retroactive bar changes after results. Amendments go to Micah.

## Commit map

1. **This prereg — committed ALONE** (no src, no fixtures, no results):
   `senses/pam-rebuild/round2/preregs/PREREG_FS-E4b.md`.
2. Sources + glue + build notes (separate commit):
   `senses/pam-rebuild/round2/forks/FS-E4b/`: `PREREG_FS-E4b.md` (copy),
   `src/` (`e4b.zag`, `r27fe.zag` vendored, substrate zags),
   `work/` (draw/judge/select/corrupt/run/verify/score scripts),
   `BUILD_NOTES_E4B.md`.
3. Evidence (separate commit): `evidence/` (battery lists + manifests,
   candidate manifest, corrupt-G manifest, run logs ×2, ledgers ×2,
   `SCORES_E4B.md`).
4. `VERDICT_FS-E4b.md` + final evidence (last commit).
- Frozen binary NEVER committed (rebuilt deterministically from source).
  No `.zagd` cache files. Fixture bytes not committed (size); committed
  manifests verify deterministic regeneration.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Commit via
  `~/workspace/commit_racefree.py`, lab-relative paths
  `senses/pam-rebuild/round2/...`, TMPDIR=`~/workspace/tmp_commit`.
  Verify via GitHub API, report SHAs.

## Laws

Pure Zag mechanism; Python glue/analysis only; zero RNG in any decision
path (draw uses fixed index orders and the generator's splitmix streams —
no `random` module anywhere); byte-identical reruns required; plain
language; max-risk posture.

## Out of scope / not claimed

- This prereg does not re-derive R2-7's results (frozen verdict taken as
  given: B5 2.14% FI, recall 68.8% — the base is ALIVE but WEAKENED).
- It does not claim the FS-E4 finding ("G-spans are clean for R2-7's
  formation front-ends") as proven — the experiment measures `formG` vs
  truth on the F-fooled battery directly, per task.
- It does not fix R2-7's weak challenges (timbredisc/shapetrans) — the
  booster is concurrence, not a new challenge.
- Calibration numbers in §Batteries are from R2-7's frozen evidence, not
  fork results.
