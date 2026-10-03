# Q4 Transfer Report — ARITY vs UNINIT Control
## Worker A, bug-blindness, 2026-09-22

### Design
Q4 tests whether repair experience TRANSFERS: does practicing ARITY repairs
improve later ARITY detection/generation relative to an unpracticed control?
- Treatment: 8 fresh ARITY probes (qa1–qa8), 6 ARITY repairs with compiler feedback
- Control: 8 fresh UNINIT probes (qu1–qu8), never repaired
- Key sealed 2026-09-22 03:41:18Z: `190895e9d2bc695af04ea7f8271acae4a2e6da42c91117439aef256f32566351`

### Detection results (chronological PRE → POST)

| Probe set | PRE | POST | Δ |
|---|---|---:|---:|
| ARITY (qa1–qa8) | 8/8 (100%) | 8/8 (100%) | 0pp |
| UNINIT (qu1–qu8, control) | 8/8 (100%) | 8/8 (100%) | 0pp |

PRE output digest: `327471b43fa99f7cfdb431ff83cb1c73f21c4476c2b35c55c1bd93013653baf9`
POST digest identical. Determinism: 5/5 identical reps, digest
`b491b97fb7d4668b0e9c6b90c932fbc2523c499b2301c9b831bb2d391c6cbcbf`
(saved `logs/bb1_q4_det5.out`).

### Repair experience
`run_bb1_repairs.py`: 6 real ARITY repairs via `driver.repair_task`, all PASS
on attempt 2 after compiler feedback (r1–r6: ARITY add:3:2, add:1:2,
add3:4:3, add3:2:3, mul:3:2, mul:1:2). Total 6/6.

### Generation (pre-equivalent replay)
Six fresh T1|FUNC specs (g1–g6), sealed 2026-09-22T03:54:02Z
(`b62e0bc43eebf24cbd8e9eab6f3b665575129d6eed93033d188732e8bd24fd91`),
5 reps each, byte-identical digest
`e3f3f333456e743fa2a19a390ffdc530c61a58524ef56c3c4c23fc54c1b236dd`.

| Spec | op | Result |
|---|---|---|
| g1 sqr | square (unseen) | FAIL ×6 iters (empty body → unknown fn) |
| g2 cube | cube (unseen) | FAIL ×6 iters |
| g3 add4 | sum (known) | **PASS iter1** |
| g4 min2 | min (unseen) | FAIL ×6 iters |
| g5 neg | negate (unseen) | FAIL ×6 iters |
| g6 mul3 | product (unseen) | FAIL ×6 iters |

Sealed bar (≥5/6 first-attempt PASS): **not met (1/6)**. The sealed
prediction was wrong; reported honestly.
Finding: the generator emits a correct body only for ops in its authored
repertoire (`sum,max,fact,is_even,count_pos,gcd,is_prime,fib` —
`learner.zag` lines 237,247,251,257,299,302,641,651,660). For unseen ops it
emits an empty body; the UNKNOWNFN repair loop cannot recover because the
repair patches also lack the op logic. The one success (g3: fresh name
`add4`, 4 args, known op `sum`) shows arity generalization WITHIN a known op.

### Sequencing deviation (flagged openly)
The six-spec first-attempt `gen` measurement was not run before the repair
experience. The generation run above is labeled **pre-equivalent replay from
the unchanged stateless executable**, not a chronological PRE measurement.

### Architecture: why transfer is impossible here
`coding/src/learner.zag` (exact references):
- Lines 10–12: "State is threaded through *Cx… No RNG anywhere. All
  decisions are pure functions of the inputs."
- Lines 1306–1319 (`do_teach`): prints only an `AUDIT op=INSTALL` line;
  installs nothing, mutates no store.
- Lines 2006–2039 (`do_repair`): reads `(eclass, details, src)` from argv,
  dispatches authored patch functions, prints the patched source. No
  persistence path.
- Zero `_zag_raw_syscall` uses in the file: the learner cannot write files,
  sockets, or any persistent state even in principle.
- Lines 2041–2050 (`main`): each invocation dispatches exactly one mode and
  exits.
- `coding/driver.py` lines 42–45: every learner call is a fresh subprocess.

Conclusion: no repair result reaches any store consulted by later
invocations. The detector and generator are pure functions of their inputs
on the pinned executable. Transfer is architecturally impossible, not merely
unobserved.

### Verdict
- **KB-T1: FAIL** — no +30pp ARITY gain (100%→100%, 0pp); ARITY did not
  finish above the UNINIT control (both 100%).
- Qualifier: transfer was unmeasurable at the detector's 100% ceiling.
  The FAIL is mechanical per the frozen rule, but the architecture evidence
  shows the ceiling is not the binding constraint — statelessness is. Even
  with headroom, this learner could not transfer because it cannot retain.
