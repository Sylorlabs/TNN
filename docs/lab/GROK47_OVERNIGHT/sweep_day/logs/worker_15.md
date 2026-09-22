# worker_15 log — chunk_15 sweep (50 rows), 2026-09-22

## Method
- Hashed all 50 files; found 9 exact duplicates (canonical copies reviewed, rest marked dup).
- Grep-screened 15 unique .zag files for: `rand|lcg|srand|random` tokens (all clean),
  `as []i32|[]u32|[]u16` casts (zero), `slice as *u8` (only `_zag_malloc as *u8` malloc casts),
  chained `s.field.subfield` (zero), stray `};` (struct-literal returns — compiled fine).
- Spot-compiled with `znc_linux_x86_64_abed8aa1`: traps_trial, diff.zag+diff_trial,
  il_trial, trial12, lht (10x/100x legs), trial_wb3 (imports wb3_core+substrate).
  wb3_core/red_adv have no main by design (library modules). All builds succeeded.
- Independently re-ran every compiled binary twice: byte-identical everywhere.
- Verified arithmetic in family_b/c/d curriculum tables by hand-checking modular arithmetic.
- grok-4.7 calls used: 0 — native review covered everything.

## Independent verifications (result docs reproduced from source)
| File | Doc claim | My check |
|---|---|---|
| traps_trial.zag | 13/13 CL_CHECK, byte-identical, replay 388/388, verdict CONFIRM | PASS (all reproduced) |
| diff_trial.zag | 73/73 DIFF_CHECK, sha256 082f37df… | PASS (sha256 matches doc exactly) |
| il_trial.zag | 24/24 CL_CHECK, sha256 f728d35c… | PASS (sha256 matches doc exactly) |
| trial12.zag | 40/40 CL_CHECK, PT_STAT A–E lines | PASS (all 6 PT_STAT lines match doc verbatim) |
| lht.zag | 10x/100x green, 100x sha256 2a7056a9d…, SUMMARY numbers | PASS (prefix matches; blocks 200/2000, 4603 entries, min_hold 1000, disc block 7) |
| trial_wb3.zag | — (no results doc in chunk) | compiled, byte-identical reruns, WB_FAILURES=0, 4 phases |

## Per-file notes
- **substrate canonicals** (wave3 common/observation/world; cheat-traps R33 IO+SHA256): vendored, header-tagged ("No learner, evaluator or legacy execution"; world.zag "NEVER imported by learner"). Clean.
- **trial_wb3/wb3_core**: WB3 selective-audit store; driver runs 1x (64 slots) and 10x (640 slots) with adversarial cases. Ran clean.
- **PREREG_TRAPS.md**: pre-run with one pre-run amendment (12→13 checks) — but CONFIRM item 1 still reads "All 12 CL_CHECKs pass". Stale count; nit, flagged.
- **cheat-traps suite**: DESIGN→PREREG→curricula→VALIDATION chain internally consistent. All 4 family curricula arithmetically verified.
- **differentiation**: eliminative judgment + partition storage. Honest boundaries documented (in-band only, registered persons, single-speaker). Replay skips REFUTE entries by design (documented).
- **integrity-ledger**: only-VERIFY-commits; rules 1–5 mechanical; boundaries state forgery/perception are below this layer. Note: TRIAL_RESULTS honest note 6 — re-verification amnesty means deliberate reversal and quiet flip look identical; flagged as future work, not a finding.
- **longhorizon**: amendments A1–A4 documented; A3 deliberate UNPIN+KILL prevents tally accumulation bug. Boundary: 1000x leg not run (open, named falsifiers).
- **phase-transitions**: POSITION.md argues 0→1 pure trainer, 1→2 combination (trialed), 2→3 system+gate (no trainer veto — contrarian, follows program law), 3→4 combination. Each with falsifiers. TRIAL_RESULTS_12 reproduced exactly.
- **rl-redteam**: PREREG §6.1 pre-run + §6.2 pre-verdict amendments properly documented (VULN2 added, magnitudes +16/+32/−12, spot-check). DESIGN uses amended magnitudes — consistent. LH-5 references quarantined with a proper contamination note (R34 LCG remediation).
- **red_adv.zag**: branch rule `n3>=ADV_HACK_BAR → ESCALATE else CORRUPT`; atk bitflags (1 loophole / 2 corrupt / 4 forged) match DESIGN phase map. Reads SUT ledger white-box with byte-offset audit layout consistent with AGENTS.md layout notes.

## Kill bars applied mechanically
- PREREG_TRAPS CONFIRM (13/13 checks, byte-identical, no-RNG grep, replay, honest-pass, cheat-caught): all satisfied on independent rerun.
- Differentiation F1–F8: all reproduced passing (F6 byte-identical sha256 match; F7 grep clean).
- Integrity-ledger F1–F4: no escapes/misfires in independent rerun (IL_FAILURES=0, 24/24 checks).
- LHT I1–I3/S1/D1–D4/W1–W2 POSITIVE bar: 10x+100x legs green, no TEMPT_TAKEN (grep), disconnect at block 7 as hand-computed.
- PT-12 F1–F5: scenarios A–E all match documented PT_STAT lines; refusals mutated nothing.

## Findings
1. PREREG_TRAPS.md nit: CONFIRM item 1 says "12 CL_CHECKs" after the 12→13 amendment (stale count; binary runs 13).
2. No RNG tokens, no banned casts, no chained-struct access, no miscompile triggers in any reviewed .zag.
3. `};` after struct literals compiles fine in this znc build (diff.zag etc.) — the workspace AGENTS.md warning appears to cover a different construct (fn-body-level stray semicolon), not struct-literal returns.
4. red_adv.zag imports red_common.zag + red_sut.zag which are NOT in chunk_15; RT-1 claims could not be independently executed. Design/prereg/docs consistent.

## Rows not evaluable
- 1: wave4/rl-redteam/TRIAL_RESULTS.md — claims internally consistent with PREREG/DESIGN but NOT independently executable (driver + 3 sibling sources outside chunk). Verdict: review, execution unverified.
- (red_adv.zag component of same evidence: reviewed statically only, same reason.)
- 9 dup rows: not re-reviewed, verdict points at canonical paths (hashes identical).
- All other 40 rows fully evaluated.

## Counts
Rows done: 50 (40 PASS/review fully evaluated, 1 review-unverifiable execution [RT-1 results], 9 dup).
Findings: 4 (1 stale doc count, 3 clean-pattern confirmations). No kill bars tripped.
