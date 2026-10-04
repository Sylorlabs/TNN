# PREREG NS-INVARIANT: the operand-namespace representation defect in frozen TNN-2

Lane: `docs/lab/research-lead/overnight-20260928/ns_invariant/`
Branch: `scale/namespace-invariant`
Claim IDs: C500+ only.
Prereg frozen BEFORE any implementation. Committed alone.

## 0. CONTROL

`tnn2_control.zag` is a byte-for-byte copy of
`compression_exec/tnn2_frozen_ref.zag`.
sha256 = `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
Verified by `cmp` at lane creation. The frozen file is NOT modified.

Baseline established before the prereg (control engine, own 46-test battery):
`TOTAL 46/46`, `--rep 3` byte-identical, stdout sha256
`37c7b552fe56c9b03b93aadb8108dfbd1d8031c056dd0e2cdcb6a1fb88cd3911`.

## 1. EXACT ENUMERATION OF THE SINGLE INTEGER SPACE

The frozen engine stores an ISA cell as a 40-byte node record with ten i32
fields `noff(n)+0,4,...,36`. `f0` is the tag. Fields `f4,f8,f12,f16,f20,f24,f28,f32`
are the payload. Three different kinds of value share those payload fields:

1. **opcodes** in `f0` (values 101,102,103,104).
2. **node types** in `f0` (values 0,1,2,3,4,8,20,21,30,900,901,902,903 and,
   in the ACT port, **102**).
3. **operand words** in `f4`/`f8` of ISA cells, which are simultaneously either
   a node id (a trial literal) or a frame-slot reference, distinguished only by
   magnitude.

### 1.1 The positional partition rule

`res_op` (line 179-183) is the only decoder:

```
fn res_op(W,f,op) { if(op>=1000){return fr_get(W,f,op-1000);} if(op>=0){return ng(W,op,20);} return 0; }
```

Partition of the operand word: `op >= 1000` -> frame slot `op-1000`; else node id.
**No bound check on the slot index. No liveness check on the node id. No kind
check at all.** The partition is entirely implicit and unrecorded.

Note for the ledger: the threshold in *this* frozen file is **1000**, not 10000.
C299 (10000) describes the `scaling_5000` lane engine, a different file.
C375 (1000) describes this defect in the E1+D1 engine. The frozen reference here
is the 1000-base variant, so the collision wall is at node id **1000**, i.e.
*earlier* than C299 estimated, not later.

### 1.2 Every operand read site, and what check exists

| line | site | field | actual kind | check present |
|---|---|---|---|---|
| 180 | `res_op` | operand word | slot if >=1000 else node id | none |
| 199-200 | `execute` tag 101 dest | f4 | slot | `d<1000` -> -999999 (low end only) |
| 200 | `execute` tag 101 src | f8 | node id (SET) **or** slot (MOVE) | none |
| 202 | `execute` tag 102 a,b | f4,f8 | slot in practice | none |
| 205-206 | `execute` tag 103 | f4 | slot | `s<1000` (low end only) |
| 208-209 | `execute` tag 104 | f4 | slot | `s2<1000` (low end only) |
| 218 | `exec_val` root output | f4 of root | slot in practice | none |
| 417 | `t2_exec` root output | f4 of root | slot in practice | none |
| 520-521 | `t2_sig` | f8 | **node id only** (`ln<1024`) | `ln>=0 && ln<1024` else lv=0 |

Line 520 is a *third, different* partition rule: `t2_sig` never considers the
slot branch. On a MOVE cell (`f8 = 1000+src`) it resolves node `1000+src` field
f20, i.e. an unrelated live node. Three sites, three rules.

### 1.3 Every operand construction site

| line | site | f4 | f8 |
|---|---|---|---|
| 348 | `t2_guard(slot,litx)` | `1000+slot` | `litx` (raw node id) |
| 352 | `t2_set(slot,lity)` | `1000+slot` | `lity` (raw node id) |
| 356 | `t2_mov(dst,src)` | `1000+dst` | `1000+src` |
| 360 | `t2_inc(slot)` | `1000+slot` | - |
| 972-973 | `t_c6` test cell | `1000` | `7` then overwritten by node id `lit` |

Line 972-973 is the frozen test itself writing both conventions into `f8`.
Opcode 101 therefore has **two different operand-kind conventions for f8**
depending on which assembler produced the cell, and nothing in the record says
which. That is the defect in one sentence.

`t2_dec` and `t2_jnz` named in C299's fix list **do not exist** in this file.
Opcode 104 (DEC) is defined (`OP_DEC`) and interpreted (`execute`) but never
assembled: it is a dead opcode. There is no conditional-jump opcode here.

### 1.4 The collision, exactly

`alloc_raw`/`alloc_node` scan `n=2..1023` and take the lowest free id. Node ids
therefore reach 1000 only after ids 2..999 are occupied. Once any ISA cell holds
a **literal** operand whose node id is >= 1000 (SET f8, GUARD f8), `res_op`
reads it as frame slot `id-1000` (slots 2..23) and silently compares/assigns
frame state. Two distinct failure modes, both silent:

* **false reject**: guard compares frame slot against 0 (an unwritten slot),
  the candidate is declined, `t2_trial` returns -2, `ev_query` reports a miss.
  The correct answer is lost with no error anywhere.
* **false accept**: guard whose literal node id is exactly 1000 reads slot 0,
  which holds the query subject `s0`, so `s0 == s0` and the link is accepted
  unconditionally. A **wrong answer** is returned with no error anywhere.

MOVE cells (f4 and f8 both carry the tag base) are immune, which is why the bug
is invisible in the small-N tests: only the literal-carrying cells break.

### 1.5 Second instance of the same defect class, found by reading

Tag `102` is simultaneously `OP_BEQ` (line 347, `t2_cell(W,102)`) and the ACT
port's guide node type (`r_mk_guide` line 1374, `r_derive_d1` line 1414,
tests at 1455/1504/1512/1519). A guide node's `f4` is a node id (anchor); a BEQ
cell's `f4` is an operand word. One integer, two meanings, in the same field of
the same record. It is latent (a guide is never a graph root or SEQ-reachable)
but it is the same class of defect and must be closed by the same invariant.

### 1.6 Third and fourth instances

* Tags `902` is used for both a **literal** cell (`t2_lit` line 340) and a
  **frame** cell (`t2_exec` line 415, `t_c6`/`t_c7` 972/979). No scan filters on
  902, so the two are behaviourally interchangeable today; the invariant must
  still separate them.
* Header field 16 packs `tried*1024 + rejected`, so `tried >= 1024` silently
  aliases the rejected counter. There is no third bucket for faults.

## 2. THE INVARIANT TO BE ENFORCED (frozen here, before implementation)

An operand is never encoded positionally inside a single integer. Every operand
occupits a dedicated **`(kind, value)` field pair** in the cell record. `kind` is
an explicit tag with exactly two legal values, and it is the *only* thing that
selects the interpretation.

```
K_LIT  = 0    // value is a node id; that node must be live and be a literal cell
K_SLOT = 1    // value is a frame slot index in [0, FRAME_SLOTS)
```

Frozen invariant set:

* **INV-1 explicitness.** Every operand of every ISA cell is a `(kind,value)`
  pair in dedicated fields. `kind in {K_LIT, K_SLOT}`.
* **INV-2 namespace disjointness.** The ISA opcode set and the node-type set are
  declared in one table and are required to be disjoint; no live non-ISA node
  may carry an ISA tag. (Closes 1.5.)
* **INV-3 no threshold dependence.** No component may select an operand's
  meaning by comparing the operand word to a numeric constant. The decoder is a
  function of `(kind,value)` only. Domain bounds (`kind in {0,1}`,
  `slot in [0,FRAME_SLOTS)`, `node in [2,NN())`) are derived from the arena
  layout, not from a tag base. **Moving the threshold does not satisfy INV-3.**
* **INV-4 referential integrity.** `K_LIT` => target live, target tag is the
  literal tag, value is that literal's data field. `K_SLOT` => slot in range.
* **INV-5 destination discipline.** Cells that write the frame (MOVE dest, INC,
  DEC) must declare a `K_SLOT` destination. Read-only cells may declare either.
* **INV-6 target discipline.** BRANCHEQ branch targets are live ISA cells or -1.
  Never operand words.
* **INV-7 closure / no stray words.** Every field not assigned by the cell's tag
  layout must be zero. A second meaning cannot be smuggled into a field.
* **INV-8 fail loud, contained, diagnosed.** A decode-time violation returns the
  distinct sentinel FAULT (-999998, distinct from the -999999 candidate decline
  and from -2 no-answer), increments workspace header field 52, and records the
  first faulting node id in field 56 and the fault code in field 60. A
  faulting candidate is **rejected and never promoted**; a fault is never
  converted into an answer and never downgraded to a decline.
* **INV-9 auditable at any time.** `ns_audit(W,rep)` is a pure-Zag routine that
  walks the whole workspace, validates every operand word against INV-1..INV-7,
  and reports the violation count plus the coordinates and code of the first
  violation. Callable from any driver at any time, non-destructive.
* **INV-10 frame/literal disjointness.** The literal tag and the frame tag are
  distinct and the audit asserts no node is claimed as both. (Closes 1.6.)
* **INV-11 tag-space completeness.** Every distinct role that the frozen engine
  overloaded onto one integer value is given its own value in one declared
  table, and the audit checks the table is pairwise disjoint. Applied to:
  operand word (INV-1), opcode vs node type (INV-2), literal vs frame (INV-10).

FRAME_SLOTS is 4, matching the four data fields of one frame node. The frozen
assemblers use slots 0 and 1 only; slot indices >= 4 are FAULTed rather than
followed through the frame chain, because that chain is unchecked in the frozen
engine and no assembler ever produces such a slot.

## 3. PREDICTIONS

* **P1 (reproduce).** There exists a filler count F such that the control engine
  answers the 2-hop fixture incorrectly, and the first such F is the first F at
  which some allocated node id reaches 1000. The control engine has no fault
  counter, so the failure is silent: exit status and every log line are
  indistinguishable from a legitimate miss.
* **P2 (fix works).** The fixed engine answers the 2-hop fixture correctly for
  every F in the sweep, including and beyond the collision point, with
  `ns_audit` reporting 0 violations and header fault count 0.
* **P3 (no behaviour change below the defect).** For every F below the collision
  point, the fixed engine's observable behaviour (return value of every
  `ev_query`/`ev_teach`/`ev_observe`/`ev_act` call in the sweep, in order) is
  byte-identical to the control's.
* **P4 (the old representation is not self-describing).** A legacy auditor that
  checks the frozen positional rule ("every operand word used as a node id must
  be < 1000") reports >= 1 violation on the control's workspace at and above the
  collision point, and 0 below it.
* **P5 (the battery is not vacuous).** On a deliberately corrupted fixed
  workspace, `ns_audit` reports >= 1 violation with a nonzero code, and
  `execute` on the corrupted graph returns FAULT rather than a value.
* **P6 (the real ceiling).** After the fix, the first thing that breaks at scale
  is not an operand threshold but global O(N) scanning and/or trial-cell and
  frame leakage. The report must name the measured limiter with counts.

## 4. KILL BARS

* **K1** If the fixed engine's output is not byte-identical to the control's
  below the collision point (P3 fails), the fix is REJECTED and only the
  reproduction is reported. A representation fix that changes behaviour where
  there was no bug is not a fix.
* **K2** If the fixed engine is not correct at and above the collision point
  where the control is wrong (P2 fails), the fix is REJECTED.
* **K3** If `ns_audit` reports 0 violations on a workspace containing
  deliberately malformed operand words (P5 fails), the battery is VACUOUS and
  the whole fix is REJECTED. A checker that cannot fail proves nothing.
* **K4** If satisfying the invariant requires introducing any new numeric
  constant that functions as a tag base or magnitude threshold, the fix is
  REJECTED by charter section 37. This bar is checked by reading the diff.
* **K5** Any driver that is not 3/3 byte-identical across `--rep 3` is a
  PROCESS-FAIL and is not reported as a result.

## 5. FIXTURES

* **FX1 collision sweep.** Facts `101 -11-> 102`, `102 -12-> 201`; then
  `ev_query(W,101,40,201,0)`. Correct answer 201, reached only by composing two
  taught links, so it must go through the trial loop and therefore through
  literals. Filler: `F` facts `ev_teach(W, 30000+i, 77, i)` with unique subjects
  and relation 77, which is never the queried relation and never on the chain,
  so filler changes capacity but not the answer. `F` swept over
  {0,100,300,500,700,900,940,960,970,980,985,990,993,995,996,997,998}.
* **FX2 regression battery.** The control's own 46 tests, plus an ordered trace
  of `(call,args,result)` for every `ev_teach`/`ev_query`/`ev_observe`/`ev_act`
  in FX1 and in a revision fixture, emitted through one buffered write.
* **FX3 corruption injection.** On a clean fixed workspace, three independent
  single-word corruptions: a `K_LIT` operand pointed at a live non-literal
  node; an operand `kind` set to 7; a `K_LIT` operand pointed at a freed node.
* **FX4 scale ladder.** Increasing MAP counts with the node and edge arenas
  redimensioned mechanically (offsets recomputed, no semantic change), reporting
  peak live nodes/edges, cumulative allocations, global-scan visits, and shell-
  measured wall time.

## 6. MEASUREMENT PLAN FOR B2 (next wall, not this fix)

Instrument, in pure Zag, per-function call counts and per-iteration visit counts
for `decay`, `activate`, `is_superseded`, `evcount`, `bid`, `seq_nx`,
`t2_gather`, `inc_fill`, `t2_lu_first`, `map_standing`, `t2_rels`, `revise_*`,
and `ev_act`'s nested edge loops. Report visits per query and visits per promoted
MAP as a function of N. Wall time is measured by the shell harness around the
binary and is labelled as such: there is no in-process clock reachable from pure
Zag on this host (`_zag_raw_syscall` uses the Linux syscall ABI; probes for
`gettimeofday`(116), `mach_absolute_time`(528), `clock_gettime`(266) all return
-78/ENOSYS, recorded in `probe_time.zag`). All counts are pure Zag. No attempt
to fix B2 in this lane beyond quantification.

## 7. HONEST LIMITS

* `ns_audit` validates the *operand* representation. It does not certify that
  the graph semantics are right.
* The audit is O(NN*NE/...) in the worst case by construction (it is a full
  scan), so it is a diagnostic, not a hot-path check. The decode-time check is
  the hot-path enforcement; the audit is the independent check that the decode
  path was not bypassed.
* Node/edge arena sizes stay at 1024/4096 except in FX4, where they are
  redimensioned mechanically and the redimensioning is itself audited by
  re-running the control battery at the original size.
