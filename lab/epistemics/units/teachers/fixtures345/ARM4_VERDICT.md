# ARM-4 VERDICT — symbolic-hints teacher (Track B worker W3)

**Verdict: PASS** — per the frozen PREREG_FREEZE.md §4 kill criteria (B.1/B.4).

- Binding spec: `PREREG_FREEZE.md` §4 lines 565–729, sha256 `c7a9d57e3ac4d8ff48f4396c47eec9fedbfacb894584a31779a91a64deeef879` (verified against the task file's pinned hash before use).
- Task: `~/workspace/tnn-lab/units/trackb_coordinator/tasks/TASK_W3.md` (byte-verified, same sha256).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` with flags `--no-zagd --no-analyze --no-foreground-cache`.
- Date: 2026-09-21 (Micah asleep; overnight run).

## Kept vs rebuilt

**KEPT:** the entire arm-4 fixture design — deterministic hint policy (candidate units ordered utility-desc/start-asc, padded regions `pad=max(8, span/2)` clamped to stimulus bounds, degenerate guard widening, dedup, HINT_MAX=16, uncertainty flag for below-top-quartile utility), the HINT wire v1 (`u8 count=1 || u64 start || u64 end || u8 flags`), the self-test battery (6 checks), and the shared `tape345.zag` tape layer (untouched — shared with arms 3/5). Everything that matched frozen §4 stayed.

**REBUILT (one surgical change in `arm4.zag`):** the `TAPE_HEADER` `prereg_hash` field. It was `nio_alloc(32)` — 32 bytes of *uninitialized heap memory* passed straight into the tape. The allocator returned zeros in every run here, so all reruns were byte-identical, but per the standing toolchain law uninitialized heap arrays are not reliably zeroed — this was determinism-by-allocator-luck. Replaced with `arm4_prereg_hash()`, which writes the pinned frozen-prereg sha256 (`c7a9d57e…eef879`) byte-explicitly via 8× `t345_set32`. The tape header is now deterministic by construction and the tape is auditor-checkable against the freeze (B.2.4-style check (i)). This regenerated `tape_hints.tape` (header bytes only; all 16 HINT payloads unchanged).

## Key numbers

| Check | Result |
|---|---|
| Self-tests (`arm4 test`) | 6/6 pass (`a4.gt.loads`, `a4.hint.no_word_span`, `a4.guard.refuses_exact`, `a4.guard.allows_padded`, `a4.capability.no_proposals`, `a4.order.deterministic`) |
| Tape verifier (`verify4/verify_hints_tape.py`) | 108/108 PASS, `T345_RESULT,PASS` — event sequence `[1,2,5×16,9]`, header arm_id=4, pinned freeze hash in header, SHA-256 tape chain recomputed == footer chain, event_count == 18 |
| Byte-identical reruns (fresh dir each) | N=5 identical: `a4017f3b…bf93cccd6e` (tape+stdout sha256, all 5 runs) |
| Adversarial perturbations | 7/7: reversed U-order → identical; comments/blanks → identical; stimulus byte flip (real change, `echo`→`ecXo` @30) → identical (policy is a pure function of unit spans, not stimulus bytes); perturbed input twice → identical; edge GT (units `[0,4)`,`[4,8)`,`[119,123)`,`[50,55)`) → 4 hints, all invariants PASS; `MALLOC_PERTURB_`=165/169 → identical |
| HINT events on demo slice (123B stim, 20 units) | 16 hints, 0 with a region equal to a unit span; flags=1 (uncertainty) on 10/16 below the top-quartile utility bar |
| §P-proposal symbols in arm-4 | **zero** — source grep (`sp_encode/sp_decode/sp_validate/TEACHER_MSG`, `@import("sp345.zag")`), binary `strings` scan, and TPRP magic bytes (`0x54505250`) all clean |
| Full `run_all.sh` (arms 3/4/5) | `T345_RESULT,PASS` — arm3 37/37, arm4 6/6, arm5 13/13 self-tests; functional runs; N=5 reruns all arms |

## §4 kill criteria applied

1. **B.1 — "Emits HINT events only (no §P proposals — T-8/T-10)."** PASS. §P symbols do not exist in arm-4's source, import graph (`arm4.zag` imports `tape345.zag` only), or compiled binary. Emitting a proposal is a compile error, not a runtime decision. Tape contains zero type-3 `TEACHER_MSG` events.
2. **B.1 — "Hints suggest regions, never words."** PASS. Padding (`≥8B`) guarantees every region is strictly larger than its unit; the degenerate guard refuses (and widens) any region exactly equal to a ground-truth unit span; independent Python decoder asserts all 16 regions `≠` every unit span.
3. **B.4 — TST-1 tape schema.** PASS. Length-prefixed LE framing; `TAPE_HEADER`/`STIMULUS_REF`/`HINT`/`TAPE_FOOTER`; logical ticks only; replay-verbatim semantics; SHA-256 event chain recomputed bit-for-bit from the tape matches the footer; footer event count matches.
4. **B.2.5 — negative declarations (no learning / no RNG / no wallclock).** PASS. No cross-session state (stateless fixture; N=5 byte-identical reruns + adversarial perturbations incl. heap perturbation). No RNG or wallclock references in arm-4 or its import graph (static grep clean); teacher logic is a pure function of (spec, stimulus file, history=none).
5. **§C tokenizer tripwire.** NOT APPLICABLE to arm-4 by construction — §B.8 is computed over teacher *proposals* and arm-4 emits none. Informational: 16 hints cover the 123-byte stimulus at mixed flags; no confidence-255 vocabulary-dump analog exists in the HINT wire (no confidence field at all).
6. **§B.9 cost.** Informational at fixture level: 16 `HINT` teacher messages for the 20-unit demo slice. Per-word cost metrics (`ledger_entries_per_word`, deliberation steps) are student-side and scored by the harness crew, not this fixture.

No prereg was bent. The one rebuild is documented above with before/after rationale; old tape hash `7ee6c69b…` (allocator-luck header) superseded by `45d26b2f…` (pinned-hash header) — same 16 HINT payloads.

## Commit(s)

Evidence committed to `tnn-native-lab` branch of `sylorlabs/TNN` via `~/workspace/commit_to_branch.py`:
- `docs/lab/units/teachers/fixtures345/arm4.zag` (rebuilt: pinned-hash header)
- `docs/lab/units/teachers/fixtures345/tape_hints.tape` (regenerated)
- `docs/lab/units/teachers/fixtures345/ARM4_VERDICT.md` (this sheet)
- `docs/lab/units/teachers/fixtures345/verify4/` (verifier script + logs)

Commit SHA(s): `657d014731c0` (arm4.zag + ARM4_VERDICT.md + verify4/ evidence), `acf43ac7e568` (tape_hints.tape binary artifact)

Binaries (`*_bin`), `.zag-cache/`, `.zagd.semantic-ready` were NOT committed per standing law.

## PARKED FOR MICAH

1. **§B.10 verdict weights are PROPOSED (T-14):** mastery 30% / revisability 25% / integrity 25% / retention 10% / cost 10% — "reconstructed from the truncated source; sign-off item T-14." This verdict applies the frozen kill criteria only; head-to-head arm scoring awaits his sign-off on the weights.
2. **Shared-tape fragility (observation, not fixed):** `tape345.zag`'s `tape_open()` seeds the SHA-256 tape chain with `nio_alloc(32)` and comments "zeroed chain seed" — the same allocator-luck pattern I fixed in arm-4. It was byte-identical under N=5 + `MALLOC_PERTURB_` runs, so no behavior change was needed, but I did not touch the shared file (sibling crews own arms 3/5). Recommend the coordinator/harness crew initialize it explicitly (zero-fill or a documented seed constant) in the canonical tape.
3. **Fixture `session_id=1` is hardcoded** in the arm-4 demo header (`ev_header(1,4,…)`); real sessions get harness-assigned ids. Fine for the fixture scope; the integration crew should confirm the harness rewrites or accepts it.
4. **B.2.4's auditor checklist** (spec-hash pinning, program re-run bit-reproduction) is written for arm-1; arm-4 now carries the frozen-§4 sha256 in its header, which satisfies the *spirit* of check (i). Whether the coordinator wants the same treatment for arms 3/5 is his call.
