# TASK 4+ — IDIOM BATTERY: frozen spec (2026-09-22)

**Status:** FROZEN at first commit. Any change to items, fixtures, checks,
quality formulas, or the gap metric needs a dated amendment with Micah's
re-approval.

**Provenance note (read first):** the workstream PREREG.md on disk
(`coding/reflection/PREREG.md`) is truncated mid-§3a — its final bytes are
the literal text `...[truncated 10769 chars]`, so the §4 Task-4+ text the
task order refers to is not present in any file on this VM (searched
`coding/`, `docs/`; no other copy). This document reconstructs §4's
operational content from the task order itself, which names the five items,
the per-item bars, the control reading, and the arm-gap metric verbatim.
Nothing here contradicts the order; where the order was silent (exact
fixtures, I/O contracts, quality formulas), this spec freezes one
mechanical choice. The reconstruction is flagged, not hidden.

## 0. Arms and stores (from the order + workstream PREREG §0)

- **ARM INFORMED:** coding KB (69 entries, install digest
  `a92e1031d460dbd9`) + frozen prior-art corpus (5 entries:
  `E-HUFFMAN`, `E-SQL`, `E-PEEPHOLE`, `E-BTREE`, `E-SNAKE`), installed via
  `teach` with audit entries (`teach_audit.jsonl`). Corpus =
  descriptions of how humans have built each idiom (algorithm, idiom
  notes, parameterized implementation skeleton) — never the frozen
  fixtures' expected outputs.
- **ARM FROM-SCRATCH:** coding KB ONLY (69 entries). The scratch store
  digest MUST equal the coding-knowledge-only digest
  (`a92e1031d460dbd9`); any drift voids the arm comparison.
- **Machinery:** one learner binary (`src/learner4.zag`), identical both
  arms. `gen` is store-driven: it scores `E-*` entries by keyword against
  the spec goal, slot-fills the winner, and emits; with no matching
  family it emits `KB-MISS:` (a gen-failure sentinel → `diagnose` as
  `GEN` → `halt-genfail`). `diagnose` = the loop harness's deliberative
  classifier + patch/regen strategies, unchanged. The driver
  (`src/driver4.py`) is deterministic plumbing: no decisions, no error
  classification, byte/sha comparisons and verifier dispatch only.
  Budget 6 iterations; 5 reps per arm×item; canonical logs must be
  byte-identical across reps (else FAIL).

## 1. Battery items (frozen)

All programs are pure Zag, zero RNG, deterministic, built with the pinned
toolchain `znc_linux_x86_64_abed8aa1`.

### B1 — Huffman codec
- **I/O:** `huff rt <hexbytes>` → stdout three lines:
  `<nbits>\n<hex of packed bits, MSB-first, zero-padded>\n<hex of decoded bytes>\n`.
- **Done:** encode+decode round-trip byte-exact on all 6 frozen vectors.
- **Frozen vectors:** v1 `""` (empty); v2 `"6161616161616161"` (8×`a`);
  v3 hex of `the quick brown fox jumps over the lazy dog`; v4 hex of bytes
  0..255; v5 hex of `a`×100+`b`×50+`c`×25+`d`×12+`e`×6+`f`×3;
  v6 hex of `AB`×64.
- **Checks (16):** per vector — (a) decoded == input (6), (b) framing:
  `len(bits_hex) == 2*ceil(nbits/8)` (6); compression sanity — v1:
  nbits==0; v2: nbits==8 (single symbol → 1 bit/symbol); v3,v5,v6:
  nbits < 8·len(input) (4).
- **Quality q1** = checks passed / 16. **Pass** = 16/16.

### B2 — tiny SQL engine
- **I/O:** `sql <dbdir> "<query>"` → stdout: header line then one line
  per result row, fields `|`-separated, `\n`-terminated. Numbers print as
  in the CSV (no reformatting).
- **Dialect (frozen):** `SELECT <c1,c2..|*> FROM <t> [JOIN <u> ON
  <t.a>=<u.b>] [WHERE <col> <op> <lit> [AND ...]] [ORDER BY <col>]`,
  `<op>` ∈ `= != < > <= >=`; literals: integers or `'quoted'`; column
  refs `t.col` or bare `col`.
- **Frozen data:** `employees.csv`
  `id,name,dept_id,salary` =
  1,Ana,1,60000 / 2,Bo,2,75000 / 3,Cy,1,52000 / 4,Di,3,80000 /
  5,Eli,2,68000 / 6,Fay,1,61000 / 7,Gus,3,45000 / 8,Hal,2,72000;
  `departments.csv` `id,dname` = 1,Eng / 2,Sales / 3,Ops.
- **Frozen queries + expected (from independent oracle `src/oracle4.py`):**
  - Q1 `SELECT name FROM employees WHERE dept_id = 2` →
    `name\nBo\nEli\nHal\n`
  - Q2 `SELECT name,salary FROM employees WHERE salary > 70000 ORDER BY salary` →
    `name|salary\nHal|72000\nBo|75000\nDi|80000\n`
  - Q3 `SELECT employees.name,departments.dname FROM employees JOIN departments ON employees.dept_id=departments.id` →
    `employees.name|departments.dname\nAna|Eng\nBo|Sales\nCy|Eng\nDi|Ops\nEli|Sales\nFay|Eng\nGus|Ops\nHal|Sales\n`
  - Q4 `SELECT * FROM departments WHERE id != 1` →
    `id|dname\n2|Sales\n3|Ops\n`
  - Q5 `SELECT name FROM employees WHERE salary >= 60000 AND dept_id = 1 ORDER BY name` →
    `name\nAna\nFay\n`
  - Q6 `SELECT dname FROM departments JOIN employees ON departments.id=employees.dept_id WHERE salary < 65000` →
    `dname\nEng\nEng\nEng\nOps\n`
- **Quality q2** = queries byte-exact / 6. **Pass** = 6/6.

### B3 — peephole optimizer over stack-VM bytecode
- **VM (frozen):** ops `PUSH n | ADD | SUB | MUL | DIV | DUP | SWAP |
  POP | NEG`; i64 stack; `DIV` truncates toward zero (frozen programs
  contain no division by zero); result = final stack.
- **I/O:** `peep <progfile>` (one op per line, `PUSH n` / bare op) →
  stdout = optimized program, same text format.
- **Done:** on each frozen program, optimized program is
  semantics-preserving (reference VM in the verifier runs original vs
  optimized → identical final stacks) AND instruction reduction ≥ 20%.
- **Frozen programs** (`fixtures/b3_p1.txt` … `p4.txt`):
  - p1 (9 ops): `PUSH 2,PUSH 3,ADD,PUSH 4,MUL,PUSH 10,PUSH 2,DIV,ADD`
    → result `[25]`, reference reduction 88.9%.
  - p2 (11 ops): `PUSH 7,PUSH 0,ADD,PUSH 1,MUL,DUP,POP,PUSH 5,PUSH 0,SUB,ADD`
    → result `[12]`, reference reduction 90.9%.
  - p3 (7 ops): `PUSH 3,DUP,MUL,PUSH 2,PUSH 2,MUL,ADD`
    → result `[13]`, reference reduction 28.6%.
  - p4 (9 ops): `PUSH 9,PUSH 4,SWAP,SWAP,SUB,NEG,NEG,PUSH 0,MUL`
    → result `[0]`, reference reduction 88.9%.
- **Quality q3** = mean over programs of
  `semantics_ok ? min(1, reduction/0.30) : 0`.
  **Pass** = all 4 semantics-ok AND all reductions ≥ 0.20.

### B4 — order-4 B-tree with split/merge
- **Order 4 (frozen):** max 3 keys/node; non-root nodes ≥ 1 key and ≥ 2
  children; root ≥ 1 key when non-empty; keys strictly increasing; keys
  unique (i64).
- **I/O:** `btree <opsfile>`; ops `i <k>` insert, `d <k>` delete
  (absent key = no-op), `p` print. Print format, per `p`: one line per
  node `N<id> leaf=<0|1> n=<nkeys> keys=<k1,k2..> children=<c1,c2..>`
  (node-id order), then `ROOT <id>`.
- **Frozen op sequence** (`fixtures/b4_ops.txt`): 8 inserts, `p`, 5
  inserts + 2 deletes (one of absent key 13), `p`, 4 inserts + 2
  deletes, `p` — 25 lines total (see fixtures file).
- **Checks per print (7):** node count ≥ 1; every node 1–3 keys; keys
  strictly increasing; leaf ⇔ no children; internal ⇔
  children == keys+1; child ids defined exactly once, single parent;
  in-order key multiset == expected set (print1:
  {5,6,7,10,12,17,20,30}; print2: {4,5,7,10,11,12,17,25,30,40,50};
  print3: {1,2,4,7,9,11,12,15,17,25,30,40,50}).
  21 checks total.
- **Quality q4** = checks passed / 21. **Pass** = 21/21.

### B5 — SNAKE (control)
- **I/O:** `snake <moves> <foodlist>`; moves ∈ `[UDLR]*`; foodlist =
  `x1,y1;x2,y2;…`. Grid 10×8 (x:0–9, y:0–7). Start: head (4,4), body
  (3,4),(2,4). Each move steps the head; eating the current food grows
  (+1 score, next food); wall/self hit ends the run.
- **Output:** exactly
  `BOARD 10 8\nSNAKE <len> <x,y>* (head first)\nFOOD <x,y | -1,-1>\nSCORE <n>\nSTATUS <RUNNING|DEAD_WALL|DEAD_SELF>\n`
  describing the FINAL state.
- **Frozen probes:** P1 moves `` foods `7,4`; P2 `RR` / `7,4`;
  P3 `RRR` / `7,4;0,0`; P4 `RRRRRR` / `0,0`; P5 `RRRDLU` /
  `7,4;7,5;6,5`. Expected (from `src/oracle4.py`):
  - P1: len 3 head (4,4) food (7,4) score 0 RUNNING
  - P2: len 3 head (6,4) food (7,4) score 0 RUNNING
  - P3: len 4 head (7,4) food (0,0) score 1 RUNNING
  - P4: len 3 head (9,4) food (0,0) score 0 DEAD_WALL
  - P5: len 6 head (6,5) food none score 3 DEAD_SELF
- **Quality q5** = probes passed / 5. **Pass** = 5/5.
- **Control reading (frozen):** the B5 gap SHOULD be small; a large B5
  gap is reported as-is — per the order it reads as general impairment
  of the scratch arm rather than a prior-art effect.

## 2. Scoring (frozen)

Per arm×item, over 5 reps (canonical-log byte-identical, else FAIL):
- **first-attempt pass** = 1 if outcome==pass and iters_used==1 else 0.
- **iterations-to-working-build** = iters_used if pass else 7 (never).
- **quality** q1..q5 as above (all 0..1, mechanical).

**Arm-gap metric (frozen, computed exactly):**
- `gap_first[i] = fa_informed[i] − fa_scratch[i]` (in pp) for i ∈ B1..B4.
- `gap_iters = mean_{B1..B4}(iters_scratch − iters_informed)`.
- `gap_q[i] = q_informed[i] − q_scratch[i]` for i ∈ B1..B4.
- **Meaningful** iff (≥3 of B1..B4 have gap_first ≥ 25)
  OR (gap_iters ≥ 2.0) OR (≥2 of B1..B4 have gap_q ≥ 0.25).
- B5 reported separately with the control reading; B5 does not enter
  the meaningful-gap computation.

## 3. Kill/void conditions (frozen)

- Scratch store digest ≠ `a92e1031d460dbd9` → arm comparison VOID.
- Any coding decision found in the driver → trial VOID.
- Any non-determinism across the 5 reps → FAIL for that arm×item.
- Any gate refusal on a battery spec → investigate (specs contain no
  trigger terms by construction).
