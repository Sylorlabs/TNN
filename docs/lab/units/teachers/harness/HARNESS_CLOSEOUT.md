# Harness Closeout — Track B C2 (TAPE_FOOTER), final

Date: 2026-09-21. Worker: C2 (overnight, Micah asleep).
Finalization: 2026-09-21 (Track B closeout, last worker).
Binding Track B §4 hash: `c7a9d57e3ac4d8ff48f4396c47eec9fedbfacb894584a31779a91a64deeef879`.

## FINAL OUTCOME

**The §B.4 TAPE_FOOTER gap is CLOSED — implemented by the owning repair
crew, not by C2.**

The repair crew was confirmed active and committed
`afb32918809b` ("Track B: harness.zag nested-struct -> struct-of-arrays
refactor", 2026-09-21) to `tnn-native-lab`. That commit already writes
the complete §B.4 footer in `session_close` and eliminates the ZNC-006/009
double-free root cause by construction (no `struct Student`, no `struct
Tape`; `Session` = 5 flat slice arenas + ledger ptr).

C2 rebased onto the repair crew's committed version and verified it
read-only: **12/12 self-test suite PASS, exit 0, ALL_OK; N=5 full-suite
executions byte-identical; real TST-1 replay honest PASS + tamper fails
closed.** Feature-mapped C2's independent scratch patch against
`afb32918809b`: **residual patch EMPTY** — every element (real 112-byte
footer, tolerant mid-session parse / strict closed-tape replay,
opening-triple minimum `n<3`, single-terminal-footer enforcement,
`test_cost` teacher_words 55→77 at line 2958, padding determinism) is
subsumed by the committed generation. Nothing of C2's patch was offered
or applied; applying anything would only reintroduce the obsolete
nested-struct generation.

**C2 touched no live source at any point** — C2 stayed patch-only
throughout. The only live write by C2 is this document
(`HARNESS_CLOSEOUT.md`, written after the 30/30 clean quiescence survey).

## Footer layout (committed version, afb32918809b)

112 bytes: `sha256(32-byte unit records)` + `sha256(ledger bytes)` + six
LE u64 verdict counters (adopt, revise, reject, defer, retract, appeal),
written via `s_tape(s, EV_FOOTER, fb)`. Unit record layout: `u64 start @0`,
`u64 end @8`, `u32 teacher @16`, `u8 strength @20`, `u8 live @21`,
`u16 zero @22` (padding explicitly zeroed), `u64 proposal seq @24`.
`replay_verify` requires `footer_idx >= 0` (returns -777777 on footerless
tapes); mid-session inspection uses the tolerant parse. Strict replay on
closed tapes only; single terminal footer enforced via event-count
equality after re-close (duplicate/trailing-footer tapes fail).

## Test evidence (C2's scratch builds, required toolchain flags)

Built with
`znc_linux_x86_64_abed8aa1 --no-zagd --no-analyze --no-foreground-cache`.

Committed refactored code (`harness_branch.zag`, binary `hb_branch`,
429,449 bytes; binary removed after runs):
- `all`: PASS codec, malformed, seq, tripwire, replay, defer, hint,
  oracle, det5, pertA, pertB, cost — **12/12, exit 0, ALL_OK**.
- `smoke`: PASS.
- N=5 full-suite runs byte-identical
  (md5 `4b334ca0be0d514d7032271d9d5fb558` × 5;
  logs `evidence_branch_run{1..5}.log`).
- `replay` = real TST-1 replay: honest `replay_verify` → 0; tampered
  (flipped DELIB body byte) → fails closed, non-zero.
- Cost metrics identical to C2's proven scratch run: ledger 31/496,
  teacher 11/77, delib 36/142, appeals 4/12, deferrals 0/0.

C2's independent scratch fix (pre-rebase, proving the mechanism):
`harness.zag` binary `hb_fixed5` (461,506 bytes) — 12/12 PASS, N=5
byte-identical (md5 `064741818e7d373bed37afd154bb478b` × 5); honest
`replay_verify` → 0, tampered → fails closed. Baseline before the fix:
7 FAIL + `pertA` panicked (`slice index out of bounds`). The
`harness_new.zag` SoA variant's 9/12 (replay/hint/oracle FAIL on
regenerated-event divergence at event 8) was a pre-existing SoA
student/replay bug, unrelated to the footer; that file was deleted from
live by the crew and is superseded by the committed refactor.

No binaries, `.zagd`, `.zag-cache`, or `__pycache__` are part of the
deliverable.

## Ownership survey (read-only, 2026-09-21 UTC)

- 11:00:37 UTC: live `znc` process compiling inside the live harness dir.
- 11:42:42 UTC: live `harness.zag` rewritten by the crew (this became the
  `afb32918809b` generation; branch blob MD5 matched the live copy —
  one generation, not two).
- 30-minute quiescence survey (60s samples × 30, 11:44:16 → 12:14:23 UTC):
  **30/30 samples clean** — live `harness.zag` mtime unchanged, no
  harness-related live processes in any sample.
- This document was written at 12:14:34 UTC, before the patch-only
  instruction arrived; the rebase report
  (`~/workspace/scratch_tb_closeout/harness_fix/C2_REBASE_REPORT.md`)
  records the patch-only resolution.

## New compiler finding

**ZNC-2026-09-21-013**: `[]u64 as []u8` keeps the *element* count as the
byte length when applied to a re-sliced `[]u64`
(`col_ustart(s) as []u8` on `a[l..l+1024]` → len 1024, not 8192), so
`h_get_u64(us, i*8)` panics past 128 units — while the identical
reinterpret on a struct field permits offsets past 1088. Inconsistent
slice-reinterpret length semantics. Workaround: never reinterpret
re-sliced wide slices to `[]u8`; index the native `[]u64` columns
directly. Still valid as a toolchain note (surfaced via the now-deleted
SoA path).

## PARKED / RESOLVED

- RESOLVED — footer vs C2 patch reconciliation: `afb32918809b`
  subsumes everything; C2 patch retired (empty residual).
- RESOLVED — `test_cost` teacher_words 55 → 77: present in the committed
  generation (line 2958 `!= 77`).
- RESOLVED — ZNC-006/009 double-free: eliminated by construction in the
  SoA refactor (5 flat slice arenas; `sess_free` copies fields to locals
  before free); C2 verified no double-free in 12/12 + N=5.
- SUPERSEDED — SoA `harness_new.zag` deletion and its event-8 replay
  divergence: that file is gone from live; the committed refactor's
  replay suite is green.
- STILL OPEN (toolchain): ZNC-013 — file with toolchain or add to the
  local znc bug list.
