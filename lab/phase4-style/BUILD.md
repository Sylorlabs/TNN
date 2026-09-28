# BUILD.md — phase4-style build notes

## Source

- `build/sa.zag` — pure Zag, zero randomness. Reads scripts from `argv[1]`.
- `build/R33_NATIVE_IO_V1.zag` — native I/O (pinned toolchain file).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (pinned; `znc build sa.zag -o sa_bin`).
- `sealed/gen.py` — corpus/script generator (Python, stdlib only).
- `battery/run.sh` — 3× runner + sha256 determinism gate.
- `battery/score.py` — chain verifier + kill-bar adjudicator.

## Repairs made during the build (all pre-seal except where noted)

1. **Duplicate/malformed result emission.** The first build emitted a broken
   extra result line per op (stale buffer reuse). Fixed by emitting `L` then
   `R` from freshly built buffers; verified by inspection of smoke output.
2. **Hedge tokenization.** The prereg specifies whole-word case-insensitive
   hedge matching. The first implementation split on whitespace only, so
   `problem?` never matched `problem`. Fixed with a sliding-window
   whole-word matcher over the raw bytes (letter-boundary check both sides).
3. **`do_lesion` output order.** Now emits `L` then `R` like every other op.
4. **Cumulative lesions (AMENDMENT-02, post-seal run, pre-verdict).** The
   frozen op table has no "lesion everything" command, but the prereg
   requires an all-lesioned run. `lesion <family>` now flags one more family
   (cumulative); `lesion none` clears all. Single-lesion scripts are
   unaffected (verified: 11/12 result SHAs byte-identical across the
   rebuild; only `lesion_all` changed, from wrong to right).
5. **Amendment wording (AMENDMENT-01).** "Before any run" clarified to
   "before any sealed/evidentiary run" — a dev smoke test ran pre-amendment.

## Toolchain finding: u64 shift/OR miscompile (new)

While implementing cumulative lesions as a u64 bitmask, the build produced
wrong results that depended on lesion ORDER:
`lesion LEN; lesion CASE` behaved as "only CASE",
`lesion CASE; lesion LEN` behaved as "both".
Single-lesion scripts were unaffected. The suspect expressions were
`1u64 << (fam as u64)`, `m | (...)`, and `(mask >> (fam as u64)) & 1u64`
(znc also emitted warning A0106 "dead computation" on the shift line).
Per AGENTS.md, u64 `>>` is already known-arithmetic on this build; the `<<`/OR
behavior is a new probe-worthy finding — NOT characterized with a minimal
reproducer yet. Workaround applied: per-family i64 flag slots
(`mem[53887+fam]`), no shifts. If this pattern is needed elsewhere,
characterize first.

## Determinism

- 12/12 sealed scripts byte-identical across 3 runs: 2 plain + 1
  `MALLOC_PERTURB_=165`.
- Every output ends with an FNV-1a-64 chain line over all preceding lines;
  `battery/score.py` recomputes and verifies all 12 before scoring.
- No RNG, no time, no environment reads in any decision path.

## Layout (mem[] regions)

- `53880` ask winner, `53881` ask rel, `53882` ask distx (D trace),
  `53883` ask curq, `53884` ask count, `53885` watch_on,
  `53886` unused, `53887..53892` cumulative lesion flags (1..5 = LEN..STRUCT)
- `53893..53898` current open-person order, `53900..` open count
- `54000..` profiles (7 i64/person × 4), keyed by person index
- `60000..` key scratch arena (byte image; reset per op — no 64KB
  accumulation: this program never holds more than one utterance at a time)

## Known non-issues

- Compiler warnings `fam <= 5`-style range notes are analyzer false
  positives (indices use `fam-1` into five slots); inspected, harmless.
- `R chain` values differ between runs only if outputs differ; they don't.
