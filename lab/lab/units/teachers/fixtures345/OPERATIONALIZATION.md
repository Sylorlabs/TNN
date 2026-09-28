# Teacher Fixtures 3/4/5 — Operationalization (Crew 3)

**Prereg:** `~/workspace/tnn-lab/units/PREREG_FREEZE.md` §4 (Track B), frozen 2026-09-21.
Binding: §B.1 (arm table), §B.3 (§P wire), §B.4 (TST-1 tape), §B.8 (§C tripwire),
§B.9 (cost), §0 T-7/T-8/T-9/T-10. Design reference: `TEACHERS.md`.

All three fixtures: pure Zag, zero RNG in any path, no wallclock anywhere,
logical tape ticks only, byte-identical reruns (N=5 verified, fresh-dir runs).
Crew 1 builds the shared harness (§P gate, tape, tripwire) in parallel — these
fixtures implement the §B.3/§B.4 interfaces exactly; the tape writer here
(`tape345.zag`) is fixture-local and yields to Crew 1's canonical tape on
integration.

## File map

| File | Role |
|---|---|
| `tape345.zag` | TST-1 tape framing + event writers + SHA-256 chain + slice ground-truth loader. Imported by all three arms. |
| `sp345.zag` | §P codec, iron-rule validation, §C tripwire. **Arm 3 only.** |
| `arm3.zag` | muse-live session driver (+ dry-run mode + self-tests). |
| `arm4.zag` | symbolic-hints fixture (imports `tape345` only — no `sp345`; §P symbols do not exist in its binary). |
| `arm5.zag` | symbolic yes/no oracle (imports `tape345` only). |
| `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag` | Linux substrate copies (per lab convention). |
| `gt_demo.txt` | Demo curriculum slice: 123-byte stimulus, 20 unit spans w/ utilities. |
| `queries_demo.txt` | 36 demo oracle queries (K=32 → 32 answered, 4 refused). |
| `dryrun_teach.txt` | Canned natural teaching script (12 proposals, mixed confidence, 1 RETRACT). |
| `dryrun_violation.txt` | Canned seq-gap script (iron-rule V_SEQ=4 → INTEGRITY + halt). |
| `dryrun_smuggle.txt` | Canned tokenizer-smuggling script (200× conf-255 tiling + 200 ADOPTs → tripwire fires). |
| `run_all.sh` | Build + self-tests + functional runs + N=5 reruns + static checks. |

## §P wire (frozen, per §B.3)

Little-endian. `magic u32=0x54505250 ("TPRP")`, `version u16=1`,
`teacher_id u32` (this driver: **3** muse-live; 0 reserved; 2 RESERVED-invalid;
1/4/5 rejected — this driver speaks for arm 3 only), `session_id u64`,
`seq u64` (monotonic from 0; any gap/duplicate = violation), `kind u8`
(1=WORD_SPAN 2=BOUNDARY 3=GROUP 4=SAME_AS 5=RETRACT), `span_start u64`,
`span_end u64` (`span_start < span_end`, `span_end ≤ stim_len`), `aux_count u8`
(≤8), `aux_count×(u64,u64)`, `ground_count u8` (≤8), `ground_count×(u64,u64)`,
`confidence u8`, `checksum u64` = **FNV-1a-64 over all preceding bytes**.

Iron-rule validation codes (also process exit codes on halt):
0 OK · 1 BAD_MAGIC · 2 BAD_VERSION · 3 BAD_TEACHER · 4 SEQ · 5 SPAN ·
6 KIND · 7 CHECKSUM · 8 RANGE · 9 COUNTS · 10 LEN.
Exit codes: 0 clean END · 1–10 iron-rule violation · 11 §C tripwire fired ·
12 incomplete (no END) · 13 script/IO error. INTEGRITY event code for
violations = **1000+V-code**; for tripwire = 1 (window) / 2 (vocab dump).

## Arm 3 — muse-live session driver

NOT an AI teacher — the session driver. Usage:
`arm3 dryrun <script> <tape>` (canned script, harness testing) /
`arm3 live <script> <tape>` (parent-fed proposal file; identical mechanics,
header descriptor `arm3-live`) / `arm3 test` (self-tests).

Script grammar (one directive/line, `#` comments, blanks skipped):
`SESSION <session_id> <stim_len>` ·
`P <teacher_id> <seq> <kind> <span_start> <span_end> <confidence>` ·
`PAUX <teacher_id> <seq> <kind> <ss> <se> <conf> <naux> (s e)* <nground> (s e)*` ·
`RAW <hex>` (verbatim proposal bytes — malformed-injection tests) ·
`D <proposal_seq> <ADOPT|REVISE|REJECT|DEFER> [reason] [rev_start] [rev_end]`
(student decision records; logged as STUDENT_DECISION, fed to the tripwire) ·
`TURN <n>` · `END`.
**RETRACT convention (kind=5):** `span_start` carries the withdrawn proposal's
seq, `span_end = span_start+1` (fixture convention; §P has no dedicated target field).

Every P/PAUX proposal is encoded, then re-decoded through the hostile path
(exactly what the student ingress gate sees), validated against the iron rules,
and — if clean — appended as a TEACHER_MSG event (§P bytes verbatim) with a
logical tick. Any violation → INTEGRITY event (code 1000+V) + TAPE_FOOTER
`HALTED:VIOLATION` + halt. The §C tripwire runs on every proposal and after
every decision (decisions complete the accept_rate leg): window fire (1) or
vocab-dump fire (2) → INTEGRITY + `HALTED:TRIPWIRE` + halt. T-7 honored:
no flaw manifest anywhere in this arm (natural teaching only).

**Scheduled follow-up (not run by Crew 3):** the live teaching sessions with
the parent happen later via `arm3 live`; nothing here blocks on them.

## Arm 4 — symbolic-hints (HINT events only)

T-8/T-10: this fixture **cannot** emit §P proposals — enforced at the symbol
level (it never imports `sp345.zag`) and asserted by static checks in
`run_all.sh` plus a runtime capability flag (`a4.capability.no_proposals=0`)
and a runtime refusal test.

**HINT wire format v1 (frozen):**
`u8 region_count (=1; one region per HINT event)` ·
`u64 region_start, u64 region_end` (byte range into the stimulus tape) ·
`u8 uncertainty_flags` (bit0 = low-confidence region).
hint_bytes encode **REGION spans (byte ranges worth attending to), never word
spans**: the emitter refuses (drops, deterministic) any region exactly equal to
a ground-truth unit span — a word-exact hint is a protocol violation by
construction.

**Deterministic hint policy (frozen):** candidates = slice units in fixed order
(utility desc, then start asc); region = `[start−pad, end+pad]`,
`pad = max(8, span_len/2)`, clamped to `[0, stim_len)` — strictly larger than
the unit, never revealing exact boundaries; degenerate word-exact results are
widened deterministically and re-guarded; uncertainty expressed by
construction (regions below the top-quartile utility bar get flags bit0=1);
at most **HINT_MAX=16** regions per slice; duplicate regions emitted once.
All hints logged as HINT events; replay verbatim.

## Arm 5 — symbolic yes/no oracle

T-10: emits nothing unprompted — it only answers queries read from its query
file. **Query format (frozen):** `Q <seq> <a> <b> <extra> <pred>` with
predicates 1=IS_UNIT ("is span [a,b) a unit?"), 2=UNIT_AT ("does unit #extra
span exactly [a,b)?"), 3=BOUNDARY_AT ("is offset a a unit boundary?").
seq must be strictly increasing; malformed queries (bad pred, out-of-range,
non-increasing seq) are **refused (reason 2)** and do **not** consume budget.

**Budget K (T-9):** default **32**; test-both bracket legs **{16, 32, 64}**
(argv override). Anti-tiling: verifying all units via IS_UNIT alone needs
O(stim_len²) span queries (~8.5k on the demo slice); K=32 ≈ 0.4% of that space —
far below exhaustive querying. The K+1th and later queries are **refused
(reason 1)** and logged. Answer function: deterministic against the slice
ground truth (exact-span match / indexed-span match / boundary membership).
Answers logged as QUERY + ORACLE_ANSWER `{tape_seq, query_seq, answer_bit}`.

**Tape extension note for Crew 1:** fixtures log two event types beyond §B.4's
list — `QUERY` (10) and `QUERY_REFUSED` (11) — required by the "further queries
refused and logged" rule and by tape-only replay of the oracle. STUDENT_DECISION
(12) records arrive from the student/harness side in arm-3 sessions (here
supplied by the script for tripwire evaluation).

## Ground-truth slice format

```
GT1 <stim_len>
S <stimulus bytes: everything after "S " to end of line>
U <start> <end> <utility>     # one per unit, utility 0..255
```
Caps: stimulus ≤ 65536 bytes, ≤ 4096 units; all ranges validated on load.

## Verification status (2026-09-21, Crew 3; W2 extension 2026-09-21)

- Self-tests: arm3 **37/37** (W2 extension: bad teacher ids 0/1/2/4/5,
  session mismatch, seq gap/dup, bad kinds 0/6/9, span inversion/equality,
  aux/ground span range, conf guard, legal RETRACT/kind-5/no-retransmit,
  §C fire/no-fire boundaries, REVISE non-accept; exit-11 fix on P/PAUX §C path),
  arm4 6/6, arm5 13/13 (codec roundtrip, tamper→checksum,
  all iron rules incl. teacher_id 1/2 rejection, tripwire fire/no-fire legs,
  hint word-span refusal, oracle predicates + K+1 budget refusal).
- Independent audit (W2, `verify3/py_audit.py`, pure Python): **167/167** —
  hostile RAW battery for every V-code (exact exit, exactly one INTEGRITY
  record, `1000+V`, FOOTER `HALTED:VIOLATION`, zero TEACHER_MSG records for the
  violating message), valid-wire cross-check (byte-verbatim TEACHER_MSG, chain
  re-derivation, live≡dryrun event stream), §C primary/secondary fire agreement
  on smuggle tapes, N=2 determinism on every hostile case, adversarial
  perturbations (reorder→V_SEQ exit 4, conf perturbation→input-sensitive tape
  divergence, stimlen perturbation→identical proposal bytes).
- Functional: teach exit 0 · violation exit 4 (INTEGRITY 1004 + HALTED) ·
  smuggle exit 11 (INTEGRITY code 1 + HALTED:TRIPWIRE) · hints 16/16 ·
  oracle 32 answered + 4 refused · brackets K=16 (20 refused) / K=64 (0 refused).
- Byte-identical reruns: N=5 per fixture path, each in a fresh directory —
  tape + stdout hashes identical all 5.
- Static: no RNG/wallclock references; arm3 speaks only as teacher id 3;
  arm4/arm5 contain no proposal symbols and do not import the §P codec;
  no flaw manifest.
