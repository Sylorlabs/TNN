# ARM-5 VERIFY — verdict sheet (Track B worker W4)

**Frozen spec:** PREREG_FREEZE.md §4, lines 565–729 (sha256
`c7a9d57e3ac4d8ff48f4396c47eec9fedbfacb894584a31779a91a64deeef879`).
**Focus:** B.1 arm-5 row (lines 569–582), B.4 TST-1 tape (lines 635–652).
**Task:** TASK_W4.md (byte-verified against the same hash).
**Worker:** W4 (ARM-5 VERIFY), 2026-09-21, Micah asleep — no questions asked.

## VERDICT: PASS

Every §4 bar that is verifiable for arm 5 is met by the groundwork fixture
(`arm5.zag` + `tape345.zag`) with zero modifications. All checks below ran
against the frozen text; nothing was bent. Two sign-off items are parked for
Micah (T-9, T-10) — see PARKED FOR MICAH.

## What was checked, and the numbers

| §4 bar | Result | Evidence |
|---|---|---|
| B.1: answers yes/no queries with a single bit | PASS | 52/52 answer bits across 3 tapes match ground-truth-derived expectation exactly (`verify_answer_bits.py`: k16 16/16, k32 32/32, adv 4/4, 0 fails) |
| B.1: `ORACLE_ANSWER` per-slice query budget K | PASS | Default K=32 certified; bracket legs {16,32,64} all exercised: K=16 → 16 answered / 20 refused; K=32 → 32 answered / 4 refused; K=64 → 36 answered / 0 refused |
| K+1 queries refused | PASS | k32 tape: queries seq 32–35 refused with reason 1 (budget exhausted); tape-invariant checker confirms `min(over_budget_refusals) > max(answered_seqs)` and `n_answered == K` (`check_arm5_tape.py`, 0 fails on all 4 tapes) |
| Single-bit answers only | PASS | ORACLE_ANSWER payload = u64 query_seq + u8 bit, 9 bytes; every bit ∈ {0,1}; no other payload fields (invariant `answer_len` + `single_bit`) |
| Emits nothing unprompted (static) | PASS | `arm5.zag` emits only event types 1 (header), 2 (stimulus_ref), 9 (footer), 10 (query), 11 (query_refused), 4 (oracle_answer); no TEACHER_MSG (3), no HINT (5), no §P symbols (`sp_encode/decode/validate` absent), no `sp345.zag` import |
| Emits nothing unprompted (runtime) | PASS | On all 4 tapes: every ORACLE_ANSWER (type 4) has a matching QUERY (type 10) with the same query_seq; zero answers without a query |
| B.4: `ORACLE_ANSWER` = (query_seq, answer bit) | PASS | Matches frozen field list exactly; replay-safe: QUERY + QUERY_REFUSED events are also on the tape (fixture extension, documented in `tape345.zag`) so the tape IS the teacher for replay |
| No RNG in any teacher path | PASS | Source grep: zero `urandom`/`rand(`/wallclock references in `arm5.zag` + `tape345.zag`; N=5 byte-identical reruns × 3 configs (k16, k32, adversarial) = 15/15 identical (tape + stdout hashed, fresh cwd each run) |
| Adversarial perturbations | PASS | 12-line adversarial query file: unknown predicates (9, 0), out-of-range spans, b≤a, negative-shape lines, garbage line, duplicate/non-increasing seqs → 4 answered, 7 refused (reason 2, no budget consumed), byte-identical across 5 reruns |
| No wallclock | PASS | Source grep clean; events carry logical tape ticks only; chain = sha256 over event bytes |
| Malformed queries refused, budget untouched | PASS | Malformed (reason 2) and duplicate-seq lines never increment `used`; budget fills only with well-formed answered queries |

**Self-tests (binary `arm5 test`):** 13/13 checks pass (`a5.gt.loads`,
`a5.is_unit.*`, `a5.unit_at.*`, `a5.boundary.*`, `a5.answer.deterministic`,
`a5.budget.answered/refused`), exit 0, `T345_FAILURES,0`.

**Determinism hashes (N=5, tape+stdout, fresh dirs):**
- k32: `82d5a56f2184b5f662b941cc647d06ef6eb54997a004482d0bf38e0c239ca0b3` (5/5)
- k16: `0af336c761b3b09bcb0ed3b69c11351dd8594b901eb8de3a3c3d7724a1157f27` (5/5)
- adv: `706de140486a11760834e5aa7bc32cc83827e9dd62f7e55a66770d9d7fe94e56` (5/5)

**Tape sha256 (regenerable byte-identically; see `verify5/tapes_manifest.txt`):**
- `tape_oracle_k16.tape`: `13993c1109313dcf6ce707d0d04c9ddcf4cd4fadbd2dafb0bce1482c6ff5cf7e`
- `tape_oracle_k32.tape`: `4b4a822e3b1c1b9bd093ac82f8d3cf7902ce2c90f9328da2bf560d5f16aab8f5`
- `tape_oracle_k64.tape`: `0eeb368f269864c3a6f5a522de6407d7f1c2a74ec9330113a4816442f5fbb75d`
- `tape_oracle_adv.tape`: `2f668706d29c1adcc1484c7d0cf5e8101de988ea60235533e31b28fd824bd9c7`

**Toolchain:** `znc_linux_x86_64_abed8aa1`, flags `--no-zagd --no-analyze
--no-foreground-cache`; build clean, no compiler-bug workarounds needed in the
arm-5 path (uses `[]u8` arenas with explicit LE accessors; no `as []i32`/`as
[]i64` indexed tables; no large-struct casts; no inline shifts inside &-tests).

## Kept vs rebuilt

**Kept, unchanged:** `arm5.zag`, `tape345.zag`, `gt_demo.txt`,
`queries_demo.txt`, `run_all.sh` — every line of the oracle, tape layer, demo
inputs, and the crew-3 run script already implements frozen §4 for arm 5
exactly (query grammar `Q seq a b extra pred`, predicates 1/2/3, strictly
increasing seq, budget gate, reason-1/2 refusals, 9-byte ORACLE_ANSWER). No
rebuild was warranted; rebuilding a conforming fixture would risk
unfreezing behavior for no gain.

**Built new (this task):** `verify5/` evidence pack —
`ARM5_VERDICT.md` (this file), `queries_adversarial.txt` (12-line
perturbation set), `tape_oracle_k{16,32,64}.tape` + `tape_oracle_adv.tape`,
`run_k{16,32,64}.log`, `run_adv.log`, `reruns5.log`,
`check_arm5_tape.py` (TST-1 tape invariant checker: no-unprompted-emission,
single-bit, budget, K+1-refusal, payload lengths), `verify_answer_bits.py`
(every answer bit vs ground-truth-derived expectation), `tapes_manifest.txt`
(sha256 + regeneration commands). Build/test binaries (`arm5_w4_bin`) were
scratch only and are NOT committed, per the no-binaries law.

**Not committed:** the four `.tape` files — `commit_to_branch.py`'s
extension allowlist skips `.tape` (repo convention: crew 3 committed sources
+ scripts only, no tapes). Tapes are deterministic outputs; their sha256
hashes and byte-exact regeneration commands are committed in
`tapes_manifest.txt`, and N=5 reruns prove regeneration is byte-identical.

## Design note (documented, not a deviation)

Seq consumption: any well-formed query line (`Q` + 5 fields) advances the
monotonic seq counter even if the line is then refused as malformed — so a
later legitimate line reusing that seq is refused as non-increasing (seen in
the adversarial run: malformed seq 1 poisons the next seq-1 line). This is
deterministic, budget-safe (refused lines never consume K), and matches the
frozen "gaps/duplicates = malformed" posture; the frozen text does not pin
the alternative, so this is recorded, not parked.

Stdout log lines (`ARM5: query N REFUSED …`) are operator-facing diagnostics,
not protocol emissions — nothing on the tape is emitted without a query line.

## PARKED FOR MICAH

1. **T-9 — exact approved value of K.** Frozen §4 names the budget "K — T-9"
   without pinning a number. This task certifies the groundwork default
   **K=32** with test-both bracket legs **{16,32,64}** all exercised and
   passing. K=32 is 0.4% of the exhaustive span-query space on the demo slice
   (~8.5k possible IS_UNIT spans vs 32). If you approve a different K, the
   fixture takes it as a CLI arg today — no code change needed.
2. **T-10 — "emits nothing unprompted" is marked (proposed) in B.1.** The
   fixture implements it and this task verified it statically and at runtime
   (no ORACLE_ANSWER without a QUERY; no TEACHER_MSG/HINT events; no §P
   symbols in the arm-5 binary). Sign-off still yours.
3. **Verdict weights** (mastery 30 / revisability 25 / integrity 25 /
   retention 10 / cost 10) remain PROPOSED pending T-14 — applies to all four
   arms equally, noted here for completeness.
