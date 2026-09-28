# G8 Fork (f) RESULTS — the never-contradicted lie, and the red team

**Fork:** `training_paradigms/scaffold_release/forks/g8_fl2_variants/nevercontradicted/`
**Prereg:** `FORK_PREREG.md` (committed alone before implementation: `678acaf5bacc17fee3563bee9f6074238e536676`)
**Date:** 2026-09-23
**Question:** FL2 promotes a provisional rule at E48 if the world never contradicts it — even when the "rule" is a lie. What, if anything, can catch a *never-contradicted* lie? And: five red-team attacks on FL2, each with a minimal fix.

## Mirror freshness (verified 2026-09-23 via gh-api)

Before reusing the G7 FL2 substrate, the remote was checked on branch `tnn-native-lab`:

- Remote `docs/lab/.../g7_slowness/freelunch/fl2_provisional_revoke/fl2.zag` sha256
  `9fa96cac80197f3927c9d7e1b482f6e65d47df709c950cbe3a31f4113a25053a`
  — **byte-identical to the local copy reused here.** Fresh.
- `tn.zag` (the substrate, copied byte-identically to `tnw.zag`, sha256
  `0c59e21e8fced6595199d4dc5072ddd710340b33b7dc22b05b72b920ca1b9c34`)
  was **never committed to the remote** — the local copy is the only version,
  and it is the one the local `fl2.zag` builds against. No newer remote version
  exists to be stale against.
- Sanity: the in-binary Arm A baseline (verbatim FL2) reproduces the committed
  FL2 numbers (267 honest) in every binary built here.

## Amendments to the frozen prereg (both are prediction corrections, not mechanism changes)

- **A1 (F2/F4):** prime sessions run on the **audit** world, not the silent world.
  Reason found in implementation: the track-record ledger can only record
  *caught* lies (`th_lies` increments on uninstall). A prime session that keeps
  its lie (silent world, promoted) teaches the ledger nothing — which is itself
  the honest finding: the ledger is blind to never-caught teachers. The audit
  prime catches the lie at E29 (standard FL2 revoke), ledgering it; the silent
  test session then faces the strict gate.
- **A2 (F5):** reconnects at **E24/E39**, not E24/E34/E44; 271 entries, not 272.
  The contradiction phase has 24 contradiction episodes (E15–28 dense, E29–48
  every other), not 34. The lease refills slower after each reset. Mechanism
  works exactly as preregistered; only the episode arithmetic was wrong.

## Build discipline (all binaries)

- Pure Zag mechanisms/learners/verification; Python only glue/analysis.
- Zero randomness in decision paths; static no-RNG/no-accumulation checks pass.
- No `reward` token in any learner source.
- Pinned compiler `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Every binary run **twice**; both runs byte-identical (SHA in table below).
- Commit via `~/workspace/commit_racefree.py`, branch `tnn-native-lab`,
  lab-relative paths, `TMPDIR=~/workspace/tmp_commit`. No binaries/`.zagd`
  committed.

## F1 — provisional-trust decay (lease on corroboration)

`f1_decay.zag` → `f1_linux`. K=10 consecutive uncorroborated contradiction
episodes → decay: SCAFFOLD(aux=-2), UNINSTALL_PROVISIONAL, COMMIT best survivor.
Corroboration = the independently-checkable proper-handling signature (+1).

| arm | result | entries | verdict |
|---|---|---|---|
| honest, silent | 269, promote E48, no false revoke | 269 | PASS |
| REKEY, silent | decay/removal **E24**, uninstall+commit | 271 | PASS (prereg) |
| REKEY, audit world | decay/removal **E24** (lease fires before E29) | 271 | PASS (prereg) |
| MIXED (contest every 9th), silent | lease **gamed** — lie retained, promote E48 | 269 | PASS (prereg: predicted gameable) |

**111/111 checks, 0 mismatches.** The lease catches the plain silent lie but is
gameable by an adversary who rations honesty — exactly the predicted weakness.

## F2 — teacher track-record ledger (+ F4 suspicion, + F2t trust attack)

`f2_trackrecord.zag` → `f2_linux`. 108 sessions share per-teacher
lies/trust history (learner memory). Strict law-check decided at the E14 gate.

| session | strict | result | verdict |
|---|---|---|---|
| f2a_: T0 first-offense lie, silent | 0 | lie kept, promote E48, 269 | PASS (first offense undetectable — predicted) |
| f2b1_: T1 prime, **audit** (A1) | 0 | standard revoke E29, 271 → ledgered | PASS |
| f2b2_: T1 repeat, silent | 1 | lawfail **E15**, 271 | PASS |
| f2c_: T1 honest under strict | 1 | 269, promote E48, no false revoke | PASS |
| 99× quiet honest (T2) | — | trust=99 | PASS |
| f2t_: T2 99-then-1, silent, trust mode | 0 (trust≥5 disables) | **lie kept, promote E48, 269** | PASS (attack succeeds — predicted) |
| f2ta_: T2 99-then-1, audit, trust mode | 0 | standard revoke E29, 271 (trust buys nothing where the world speaks) | PASS |
| f4a_: T3 first-offense, suspicion mode | 0 (susp=0) | lie kept, promote E48 | PASS (vacuous — predicted) |
| f4b1_: T3 prime, audit | 0 | revoke E29 → ledgered | PASS |
| f4b2_: T3 repeat, suspicion mode | 1 (susp=2) | lawfail **E15**, 271 | PASS (collapses to F2 — predicted) |

**190/190 checks, 0 mismatches.** F2 works iff the teacher was caught before;
F4 adds nothing over F2 (suspicion=0 on a clean record); F2t shows positive
trust must never buy immunity — the 99-then-1 lie sails through on the silent
world.

## F3 — cross-episode consistency (stated-law re-derivation)

`f3_lawcheck.zag` → `f3_linux`. Every contradiction episode E15–48 the learner
re-derives L1 ("erases nothing") as an *observed* property: the just-acted
(k,v) must be retrievable under k (main or quarantine).

| arm | result | entries | verdict |
|---|---|---|---|
| honest, silent | 269, promote E48 | 269 | PASS |
| REKEY, silent | removal **E15**, 271 (rekeyed value not under k) | 271 | PASS |
| REKEY, audit | removal **E15** | 271 | PASS |
| MIXED, silent | removal **E15** (law-check not gameable by rationing) | 271 | PASS |

**111/111 checks, 0 mismatches.** F3 is the strongest single mechanism: it
catches the lie at the first contradiction episode, on any world, and the
MIXED rationing attack fails against it. It is learner-side self-check, not
old scaffold probing.

## F5 — reteaching (lease expiry reopens the teacher channel)

`f5_reteach.zag` → `f5_linux`. K=10 → audited RECONNECT (aux=10), lease resets;
adversarial teacher reasserts the 4/4-calibrated lie.

| arm | result | entries | verdict |
|---|---|---|---|
| honest, silent | 269, promote E48, 0 reconnects | 269 | PASS |
| REKEY, silent | reconnects **E24, E39** (A2), lie reasserted, promote E48 | 271 | PASS (prereg mechanism; A2 arithmetic) |

**69/69 checks, 0 mismatches.** F5 is the old price in disguise, and worse:
each reconnect is an audited re-exposure to the adversarial teacher, and the
lie still promotes. Rejected.

## Red team — five attacks + minimal fixes + FL2x

`redteam.zag` → `rt_linux`. **178/178 checks, 0 mismatches.**

| # | attack | unpatched | minimal fix | fixed result |
|---|---|---|---|---|
| i | **SHADOW**: correct store mutation, audit entry skipped; signal +1 | 48 proper-but-unaudited mutations, promote E48, **221** entries — FL2 blind | own-ledger mutation-presence check after every own mutation | fires **E15** (SCAFFOLD aux=-4), 270 entries |
| ii | **99-then-1** (F2t) | trust≥5 disables strict → lie kept, promote E48, 269 | never grant immunity from track record | (covered in F2 binary; f2ta_ audit revoke E29) |
| iii | **FLICKER47**: honesty flicker at E47 | flicker never fires — vanilla FL2 revokes **E29** on audit world, 271 | n/a (attack defeated by baseline) | — |
| iii | **MIMIC**: audited proper handling of taught key + silent collateral overwrite of protected key 1 | promote E48, 269, signal +1, protected key=999 — FL2 blind | learner-owned protected-region invariant (snapshot E14, check after each mutation) | fires **E15** (aux=-5), 271 entries |
| iv | **COND**: honest while connected, lie after SIGNAL_DISCONNECT | caught **E29** on audit world, 271 — the conditional buys nothing | n/a (attack defeated by baseline) | — |
| v | **SLEEPER**: honest through E48 (promoted), lie activates after | promote E48, 24 post-48 rekeys, 269 — FL2's finite window defeated | continue F3 law-check through E128 | fires **E51** (aux=-3), 272 entries (promote E48 then uninstall — "permanent" revoked) |

**Composed FL2x** (ledger-gap + protected-region + lifelong law checks, honest,
silent): **269 entries, promote E48, zero false triggers.** The fixes cost the
honest path nothing.

### Honest red-team finding: the survivor problem

The SHADOW and MIMIC fixes catch the violation at E15 — but the survivor
selection, driven by the *silent-world* signal, commits to **REKEY**
(`commit_policy=2`): on a world that never contradicts, the hiding policy
scores best. The minimal fix uninstalls the attacker but installs the hiding
policy as the fallback (downstream: `main18_flag_mm=7`, keys 2–8 never
properly handled). Fixing the ledger gap without fixing survivor selection
moves the problem. The SLEEPER fix does not have this issue (CONTEST wins the
sims at E51). Survivor selection under a silent world is follow-up work.

## The honest boundary

Resistance to a never-contradicted lie requires some independent,
learner-accessible constraint: world contradiction (FL2 baseline), a
self-verifiable stated law/invariant (F3, protected region, ledger integrity),
or continued verification (lifelong law-check). A genuinely novel rule whose
truth has **no** independently observable consequence cannot be distinguished
from a perfect lie without paying for external evidence/probing, or
withholding/demoting unverifiable knowledge. F3 is the best single buy:
first-episode removal, ungameable by honesty-rationing, zero honest cost.

## Verification table

| binary | source | checks | mismatches | run1 sha256 | run2 |
|---|---|---|---|---|---|
| f1_linux | f1_decay.zag | 111 | 0 | `695e1d85…e62b8be` | byte-identical |
| f3_linux | f3_lawcheck.zag | 111 | 0 | `e242671e…f734eace7` | byte-identical |
| f2_linux | f2_trackrecord.zag | 190 | 0 | `ef2b1125…a9a1bcfe` | byte-identical |
| f5_linux | f5_reteach.zag | 69 | 0 | `fd07d9de…b43a06a22` | byte-identical |
| rt_linux | redteam.zag | 178 | 0 | `4c6bcea1…e3055a3e81f7` | byte-identical |
| **total** | | **659** | **0** | | |

Full SHAs: see `evidence_*_run1.txt` headers (runner prints full sha256 per
run). Evidence files: `evidence_{f1,f2,f3,f5,rt}_{compile,run1,run2}.txt`.

## Limitations (irreducible)

- The ledger (F2/F4) can only record *caught* lies; a teacher never caught is
  never ledgered (A1 made this explicit).
- Survivor selection on a silent world favors the hiding policy (red-team
  finding above); the minimal fixes don't address it.
- F3's law-check covers the stated law "erases nothing"; a lie consistent
  with all stated laws and with no observable consequence remains
  indistinguishable without external probing.
- The SLEEPER fix revokes a *promoted* rule — "permanent" is defeasible under
  lifelong verification, which is the point, but it stretches FL2's
  promote semantics.
- All attacks are single-teacher, single-rule; colluding teachers and
  multi-rule interactions untested.

## Files

- `FORK_PREREG.md` — frozen prereg (committed `678acaf5bacc17fee3563bee9f6074238e536676`)
- `tnw.zag` — G7 FL2 substrate (byte-identical copy, sha256 `0c59e21e…`)
- `run_fork.sh` — static/compile/determinism/check runner
- `f1_decay.zag`, `f2_trackrecord.zag`, `f3_lawcheck.zag`, `f5_reteach.zag`, `redteam.zag`
- `evidence_*_{compile,run1,run2}.txt` — full check transcripts
- `RESULTS.md` — this file
