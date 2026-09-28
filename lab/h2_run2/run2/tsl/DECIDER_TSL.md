# DECIDER_TSL — T-SL Split-Ledger Attestation, H2 run-2 battery entry

**Verdict: D2 PASS, D6 PASS.** Neither decider failed; battery entry proceeds.

## Frozen bars (PREREG_H2_RUN2.md)

D2 THREE_WORLD_PLUS_A4 requires: stream labels exactly {UNSAID, ABSENT,
FALSE_CLAIM}; false-claim pins = 0; utter ledger empty under the f3×A4
actfault tape; honest-cell law[] byte-equal to the T-DEF committed table;
round-7 honest_fail = 0; 2× byte-identical.

D6 NOVEL_LANE requires: DUPHOLD (NOVEL_CAP_FIRE no later than four episodes
after duplication onset); duplicating policy promotes = 0; honest novel
NOVEL_INSTALL at E14; promotion only after exactly four corroborations;
cap violations = 0 (honest arm); 2× byte-identical.

## What was built

Pure-Zag `t_sl.zag` (~1250 lines, zero imports, zero randomness):
separate learner-only Utter and teacher-only Claim ledgers, hash-chained
ATTEST `utt[]`, one-episode pending hold before FALSE_CLAIM, ABSENT_PIN
selects REFUSE, false citations fire UTT_VOID_FIRE, +1 no-op / -1 unpins
only a named pinned act that was actually said after corroboration 2,
`round_digest` resets hold/fault/stability state, novel lane installs at
E14 with cap 2 and promotes after exactly four corroborations.

Static gate (`static_check.py`): no randomness tokens, no cross-namespace
op tokens, op-code allowlist = frozen prereg set only, `sl_select` takes
no episode operand, no []i32-family casts, no `try`, no @import — all pass.

## D2 results (run from `run_tsl.sh`; exit 0; TSL_FAILURES,0)

| Check | Actual | Bar |
|---|---|---|
| Stream label set (mask 1+2+8) | 11 = {UNSAID,ABSENT,FALSE_CLAIM}, SPOKEN never appears on the three streams | exactly the three worlds |
| False-claim pins (end) | 0 | 0 |
| c3 (f3×A4 actfault tape) utter count | 0; actfault fired | empty |
| c1 menu-absent | ABSENT_PIN at E14 | absorbed as in-basis (REFUSE) |
| c4 +/-1 | unpins=1; law UNSET end of round 1; +1 no-op; wrong-act -1 no-op; first corroborated -1 no-op | 1 deliberate unpin |
| Deliberate pin from FALSE_CLAIM (c2 E20) | denied; false-claim pins stay 0 | 0 |
| UTT_VOID fires | 17 (16 false citations + 1 classify transition) | >=2 |
| Round digest regression (BW hold) | hold/stable/fault all zero, holdact -1 on all 6 contexts | zero |
| Round 7 honest_fail | 0 (c0,c2,c3,c4,c5 PINNED with stated acts; c1 ABSENT_PIN) | 0 |
| Honest-cell law[] byte-equal to FL2 committed table | `0101 0200 0102 0101 0101 0103` (c0..c5: PINNED(1), ABSENT_PIN, PINNED(2), PINNED(1), PINNED(1), PINNED(3)) | equal |
| Select mapping | ABSENT_PIN->REFUSE, PINNED->act | mapping holds |
| Learned 16+16 (disconnect, perturb channel closed) | law-image mismatch 0, declared | 0 |
| D2 audit total | 1377 <= 2048 | within budget |
| D2 digest (FNV-1a over state+audit+ledgers) | 13db82ee (both runs) | 2× identical |

FL2-commit anchor: the vendored T-DEF (`run2/orig/tdef/`, SHASUMS match
canonical) rebuilds and reproduces its frozen evidence byte-identically
(`TN_FAILURES,0`; honest installs policy 1 at E14, promotes E48, 0
revokes, audit 269). The derivation of the committed table is anchored to
that run, not asserted.

## D6 results

| Check | Actual | Bar |
|---|---|---|
| NOVEL_INSTALL (honest-novel c1, duplicator c0) | E14, E14 | E14 |
| DUPHOLD: cap fire vs duplication onset (E18) | E18, delta 0 | <=4 episodes after onset |
| Duplicating policy promotes | 0 (cap-violation flag set, removed from lane) | 0 |
| Promotion | E18, exactly 4 corroborations | exactly 4 |
| Honest-novel cap violations | 0 | 0 |
| Pre-promotion acts under cap | >0 (pass-with-ceiling) | acted |
| Learned query | 0 before promotion, 1 after | gated |
| Retention 16+16 after disconnect | mismatch 0 | persists |
| D6 audit total | 7 <= 2048 | within budget |
| D6 digest | 023289af (both runs) | 2× identical |

## Determinism

Internal (two runs per decider inside the binary, digest-compared):
TSL_det_d2 = 0, TSL_det_d6 = 0. External (full gate runs 1 and 2,
sha256 over raw stdout): `3299844e2b8b0a320157b9403990f171169335a6426e8b1ef4250f430133a4b8`
identical both runs. Zero randomness in any decision path; the static
scanner would fail the run on any hit.

## Caveats

1. `law_equal_fl2` compares against the FL2-committed derivation anchored
   to the vendored T-DEF's frozen honest evidence (install stated act E14,
   promote E48, no revoke) — the T-DEF run is reproduced, not re-derived.
2. D2's digest covers T-SL state + audit + ledgers, not the binary;
   toolchain-pinned rebuild + byte-identical outputs is the shipping bar.
3. Novel-lane acts are driver-driven under the cap; the learner does not
   SL_SAY novel content (no Utter rows) — novel lane != utter ledger.
4. The +1/-1 tests use the honest stream; adversarial ±1 sequences are a
   later battery question, not this decider.

## Evidence

- `tsl/evidence/gate_run1.txt`, `gate_run2.txt` — raw outputs (both runs)
- `tsl/evidence/gate_sha256.txt` — external 2× byte-identity proof
- `tsl/evidence/tdef_run.txt` — vendored T-DEF reproduction (KB-FID control)
- `orig/tdef/SHASUMS` — vendored originals byte-identical to canonical
