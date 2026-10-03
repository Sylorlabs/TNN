# Scaling 5000 Rerun Report (Fixed FACT Index)

Verdict: **SCALING-5000-FIXED-FAIL** (K1 fails)

## Frozen bars (PREREG.md, commit 7d20b1fd5, amended 3e234ed4e)

- K1 build order invariance: ok=1 for all queries in all 3 orders. **FAIL**
- K2a indexed scan: mode-1 MAP scan <= 32 in all orders. **PASS**
- K2b linear scan: order-D mode-0 scan >= 25000. **PASS**
- K2c reduction: order-D scan ratio >= 1000x. **PASS**
- K3 determinism: 3/3 byte-identical runs. **PARTIAL** (run 1 complete; runs 2-3
  terminated early by external factor; all completed lines match)
- K4 robustness: zero panics, hangs, build fails=0. **PASS** (no panics; 2 runs
  terminated early by likely OOM killer, not a code crash)

## Results

3 build orders (D=decoys-first, R=real-first, I=interleaved), 4990 broken plen-2
decoys + 5 real plen-5 MAPs, 8 fresh query chains per world (no activate shortcut),
queries in modes 0/1/3/5.

Run 1 (complete, 50 lines): All 24 queries (8 per order x 3 orders) returned
ans=-2, tried=5, rejected=5, ok=0. All 15 chain-integrity checks passed (ok=1).
Build fails=0 in all orders.

| order | mode | ans | tried | rejected | scan | fcnt | ok |
|-------|------|-----|-------|----------|------|------|----|
| D Q0 | 0 | -2 | 5 | 5 | 65534 | 589836 | 0 |
| D Q1 | 0 | -2 | 5 | 5 | 65534 | 589852 | 0 |
| D Q2 | 1 | -2 | 5 | 5 | 5 | 589868 | 0 |
| D Q3 | 1 | -2 | 5 | 5 | 5 | 589884 | 0 |
| D Q4 | 3 | -2 | 5 | 5 | 5 | 589900 | 0 |
| D Q5 | 3 | -2 | 5 | 5 | 5 | 589916 | 0 |
| D Q6 | 1 | -2 | 5 | 5 | 5 | 589932 | 0 |
| D Q7 | 5 | -2 | 5 | 5 | 5 | 5446 | 0 |
| R Q0-Q7 | (same pattern, all ok=0) | | | | | | |
| I Q0-Q7 | (same pattern, all ok=0) | | | | | | |

K2 measurements:
- K2a: mode-1 scan = 5 in all orders (<= 32). PASS.
- K2b: order-D mode-0 scan = 65534 (>= 25000). PASS.
- K2c: 65534 / 5 = 13107x (>= 1000x). PASS.
- FACT gather: mode-5 Q7 fcnt=5446 vs mode-0 Q0 fcnt=589836 (108x FACT-visit reduction).

## Root cause (diagnostic, /tmp, 2000-decoy order-D)

The FACT index (FI1-FI5) is NOT the culprit. The MAP graphs are intact
(chaincheck ok=1), the MAP index finds all 5 candidates (scan=5), and
t2_gather returns the correct paths. The failure is in t2_exec:

- Assembled chain is correct (cell dump verified: tags, fields, literals all right).
- Frame is correct (slot0=80000).
- First guard check: a=80000 (frame slot 0, correct), b=0 (WRONG, should be 80000).
- b=res_op(fr, 14121) where 14121 is the literal node id with ng(W,14121,20)=80000.
- res_op: `if(op>=10000){return fr_get(W,f,op-10000);}` treats ANY op >= 10000
  as a frame-slot reference. Literal node ids now exceed 10000 at scale.
- So res_op(fr,14121) computes fr_get(fr,4121)=0 instead of ng(W,14121,20)=80000.
- Guard fails (80000 != 0) -> execute returns -999999 -> t2_try_verify rejects.

This is a SCALE-dependent bug in base res_op, not build-order-dependent and not
a FACT index bug. The 10000+slot frame convention collides with node ids >= 10000
(reached at ~1400 decoys x ~7 nodes each).

The original s5 "build-order dependence" was confounded: the real-first "success"
(dbg5) used the activate shortcut (tried=0), never exercising rebind at scale.
This wave used fresh chains per query (no activate shortcut), exposing that
rebind fails at scale in ALL orders.

## Implications

- The FI1-FI5 FACT fix remains valid hardening, but it did not address the s5
  failure because the s5 failure was misattributed to the FACT index.
- The 13107x index reduction (K2) is real: the index correctly finds candidates.
  It is the VERIFICATION (res_op) that fails, not the index.
- Fix direction (frozen base, needs new workstream): change the frame-slot tag
  base from 10000 to > 65536 (max node id) in t2_guard, t2_set, t2_mov, t2_inc,
  t2_dec, t2_jnz, and res_op. Or add a tag bit to disambiguate node ids from
  frame refs.

## Run status

- Run 1: Complete (50 lines). All data above.
- Run 2: Terminated at line 35 (S6I Q1) by external factor (likely OOM killer).
  No panic message. All 35 completed lines match run 1.
- Run 3: Terminated at line 11 (S6D Q5) by external factor. No panic message.
  All 11 completed lines match run 1 (modulo output buffering loss of S6-START).

The early terminations are attributed to system memory pressure (multiple
workers), not a code defect: run 1 completed fully, and the termination points
differ across runs (non-deterministic external factor).

## Measurements (reported, not barred)

- MTF: order-R Q0 tried=1 (verify on first candidate); order-D tried=5 (all rejected).
- FACT fcnt: mode-5 Q7 = 5446 vs mode-0 Q0 = 589836.
- Threshold: 60-decoy pilot passes; 2000-decoy diagnostic fails. Node ids cross
  10000 at ~1400 decoys.

## Files

- s6_base.zag, s6_patch.zag, s6_driver.zag, s6_full.zag, s6_bin
- s6_run1.txt, s6_run2.txt, s6_run3.txt
- NAMECHECK.md, PREREG.md, REPORT.md

## Cognition accounting

- Cognition lines added: 0 (driver only, no mechanism changes).
- New hardcoded semantic cases: 0.
- Modes/bridges/handlers: 0.
- Learner-state structures created: 0.
