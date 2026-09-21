# ARM-3 VERDICT — muse-live teacher (Track B, Worker W2)

**Date:** 2026-09-21 (PDT) · **Worker:** W2, Track B coordinator `574d1ee7-3682-4507-baed-eefc07dbe8ae`
**Binding task:** `units/trackb_coordinator/tasks/TASK_W2.md`
**Frozen §4 hash:** `c7a9d57e3ac4d8ff48f4396c47eec9fedbfacb894584a31779a91a64deeef879` (unchanged)
**Evidence commit A:** `12a8c5c24278007be1eda927926ebc11baf869d7` on `tnn-native-lab`
(parent `599d98e34ba2`) — `arm3.zag`, `OPERATIONALIZATION.md`, `verify3/` evidence
**This verdict sheet:** committed as commit B on `tnn-native-lab` (SHA below)

## Verdict: FAIL — one arm-3 bar unmet (adaptive judgment not demonstrated)

Per the §4 kill criteria for arm-3 (B.1): the teacher must (1) emit §P proposals in
real time, (2) obey the §P iron rules and §C, (3) **show adaptive judgment**, (4) carry
**no flaw manifest**. Criteria 1, 2, and 4 are verified PASS with committed evidence.
Criterion 3 is **not demonstrated** by the built artifact: the driver consumes
parent-fed/canned proposal scripts and contains no history-conditioned proposal
policy `(spec, stimulus, history) → proposal`. The *interface patterns* of adaptation
(appeal with new evidence, narrowing revise, RETRACT, mixed confidence) are exercised
in canned scripts, but no teacher-side decision logic exists in the fixture — the
adaptation lives in the parent script, not the teacher. Honest FAIL beats a bent PASS.
The rebuild path is clear and is parked for Micah (§PARKED FOR MICAH).

## What was verified (all PASS, evidence committed)

### §P iron rules — every violation kind hard-rejects and is logged
- Self-tests: **arm3 37/37, bad=0** (`./arm3_bin test`; was 20/20 — extended by W2
  with `a3_t_iron2`: teacher ids 0/1/2/4/5, session mismatch, seq gap/dup, bad kinds
  0/6/9, span inversion/equality, aux/ground span range, conf guard, legal RETRACT /
  kind-5 / no-retransmit, §C fire/no-fire boundaries, REVISE-is-non-accept).
- Independent audit (`verify3/py_audit.py`, pure Python, own §P encoder/decoder,
  FNV-1a, TST-1 parser, chain re-derivation, independent §C model): **167/167 checks**.
- Hostile RAW battery: 18 cases covering V-codes 1–10 plus structural length
  rejection. Every case: exact expected exit code, **exactly one** `INTEGRITY` record
  carrying `1000+V`, `TAPE_FOOTER` verdict `HALTED:VIOLATION`, **zero** `TEACHER_MSG`
  records for the violating message, halt terminal (nothing after FOOTER).
- Valid-wire cross-check: sent bytes == logged `TEACHER_MSG` bytes verbatim; footer
  chain re-derived independently; `live` ≡ `dryrun` event streams (modulo header
  descriptor `arm3-live` vs `arm3-dryrun`).
- Functional exits (canonical `run_all.sh`): teach **0**, violation **4**
  (INTEGRITY 1004), smuggle **11** (INTEGRITY code 1). All as specified.

### §C tripwire — evaluable from the tape, fires and halts on smuggling
- Independent §C model agrees with the driver on every tape: fire/no-fire,
  fire code, fire point.
- Smuggle tape (200 × confidence-255 tiling proposals): **fire at propose #189**,
  code 1 (coverage), session halts, exit 11, FOOTER `HALTED:TRIPWIRE`.
- Vocabulary-dump tape (single conf-255 proposal >5% of stimulus): immediate fire,
  code 2, exit 11.
- Teach tape: no fire (coverage 46.3%); violation tape: no tripwire fire
  (halt is the iron-rule violation, INTEGRITY 1004).
- **Documented deviation (not a silent change — see PARKED #2):** the monitor
  implements coverage/accept-rate/maxconf-rate **cumulatively** over the session,
  while frozen B.8's letter says "rolling window of 200 consecutive teacher
  proposals". The cumulative form is strictly more conservative — it fires no
  later than the frozen letter on any smuggling pattern (verified: smuggle still
  halts the session, which is the behavior the bar exists to guarantee). The
  fixture's teacher-side bar ("obey §C": stay under the tripwire in normal
  operation) is verified unaffected.

### Determinism — zero RNG, no wallclock
- **N=5 byte-identical reruns** (fresh directory each): teach, violation, smuggle,
  arm-4 hints, arm-5 oracle — tape + stdout hashes identical all 5
  (`T345_RERUN,identical5=yes` on all five paths).
- N=2 determinism on every hostile RAW case (audit).
- Adversarial perturbations, all deterministic and input-sensitive:
  proposal reorder → `V_SEQ` exit 4; confidence perturbation → tape diverges from
  baseline; stimulus-length perturbation → proposal bytes byte-identical
  (proposals are pure functions of (spec, stimulus, history), not of stimlen).
- Static scans: no RNG calls, no `gettimeofday`/`clock_gettime` in the arm-3 path;
  teacher speaks **only as teacher id 3**; `arm4`/`arm5` contain no proposal
  symbols and do not import the §P codec.

### No flaw manifest
- Static scan of the arm-3 path sources finds no flaw manifest; the sole textual
  occurrence is the comment declaring its absence. Arm-3 proposes selective,
  mixed-confidence spans — never a planted-flaw payload.

### Learner autonomy (iron rule 2)
- The codec has no command kind; `confidence` is a weight, never an instruction.
  The fixture never issues commands; RETRACT/appeal/REVISE mechanics are present
  and exercised (`teach_live.txt`, live mode).

## Kept vs rebuilt

**Kept (matches frozen §4):** §P field order and little-endian codec; FNV-1a checksum
mechanism; proposal validation structure; TST-1 framing and chain hashing; session
driver architecture; natural/violation/smuggle fixture concepts; the
no-RNG/no-wallclock/no-manifest posture; frozen §4 text untouched.

**Rebuilt by W2:**
1. **Exit-contract defect (real bug, fixed):** the normal `P`/`PAUX` §C-fire path
   returned the raw fire code (1/2); the documented and RAW-path convention is
   process exit **11** for any §C fire. Fixed (`a3_halt` + `rc=11`). Verified by
   `T345_FUNC,arm3_smuggle,exit=11,want=11` and the audit's `exit11` checks.
2. **Self-test suite 20 → 37** (`a3_t_iron2`): full iron-rule matrix, §C
   fire/no-fire boundaries, RETRACT/REVISE semantics.

**Not rebuilt (parked):** §C cumulative-vs-rolling-200 semantics (see above);
history-conditioned teacher proposal policy (the FAIL criterion).

## Key numbers

| Check | Result |
|---|---|
| arm-3 self-tests | 37/37, bad=0 |
| Independent audit (`py_audit.py`) | 167/167 checks |
| Canonical gate (`run_all.sh`) | `T345_RESULT,PASS` |
| N=5 reruns, 5 fixture paths | identical5=yes everywhere |
| Violation battery | 18 hostile cases, all exact-exit + logged |
| §C primary fire | propose #189/200, code 1, exit 11 |
| §C secondary fire | code 2, exit 11 |
| Flaw manifest | none (verified absent) |
| Adaptive judgment | **NOT demonstrated — FAIL criterion** |

## PARKED FOR MICAH (Micah is asleep — no questions asked, decisions parked)

1. **Adaptive-judgment gap (the FAIL).** The fixture driver has no
   history-conditioned proposal policy; adaptation patterns are canned in the
   parent script. Options: (a) build a pure-Zag deterministic teacher policy
   `(spec, stimulus cursor, session history) → proposal` demonstrating adaptation
   (e.g., identical prefixes with differing student decisions → deterministically
   different next proposal/evidence/confidence); (b) rule the canned-pattern
   interface demonstration sufficient for the fixture; (c) restate the bar.
   Recommend (a) — it is the only one that makes "shows adaptive judgment" true
   of the artifact rather than of its inputs.
2. **§C cumulative vs rolling-200.** The monitor is cumulative (fires no later
   than the frozen letter; smuggle still halts). Options: (a) amend B.8's letter
   to the cumulative form; (b) rebuild the monitor to strict rolling-200
   semantics (store per-proposal spans in the 200-slot arena, per-byte counts,
   require window full, reject stale decisions). Either is a §13-level change —
   not made unilaterally.
3. **Frozen verdict weights** (mastery 30 / revisability 25 / integrity 25 /
   retention 10 / cost 10) are PROPOSED per B.1 (T-14 sign-off pending) — noted,
   not mine to sign.
4. Binaries (`*_bin`), `*.tape` files, and `verify3/work/` scratch were excluded
   from the commits per the standing no-binary law.
