# REPORT.md -- COMPOSE-C-RETRIEVAL-ROOTCAUSE

Date: 2026-10-03. Worker: COMPOSE-C-RETRIEVAL-ROOTCAUSE. Lane:
`docs/lab/research-lead/overnight-20260928/compose_c_retrieval_rootcause/`.
Branch: `tnn-native-lab`. Task type: NON-LEDGER (claim minting paused).

## 1. Finding

**C's SEQ1 non-retrieval is caused by a phantom contract code in the
stored TEACH signature -- an eval-harness artifact, not an
architectural property.** The mechanism-level retrieval rule is
principled and fully explains both sequences; the SEQ1 outcome is
accidental.

Concretely: `eval_main_c.zag` calls TEACH as
`lc_solve(S,A,M,0,3,201,1,2,3,ST)` (base=0, nm=3), but
`w_adv_teach` registers its two MAPs at ids **1 and 2**. Slot id 0
is never a MAP -- it is zeroed arena memory (all fields 0,
arity 0). `sketch()` in `lc_mem.zag` has no validity check: it
encodes the zero slot via `code_of`'s arity!=1 branch as
`2000000 + 0*1000 + 0*10 + 0 = 2000000`. The frozen TEACH memory
entry therefore stores the polluted signature
`[1001001, 1001002, 2000000]` (nc=3) instead of the intended
`[1001001, 1001002]`.

On TRAP1/TRAP2 (base=0, nm=16, all 16 slots real MAPs, no zero
slot), the query signature is `12x1001001 + 4x1001002`. Then:

- `ecodes_equal`: nc 3 vs 16 -> no (not sim 3).
- `msubset_a` (query ⊆ entry): query has 12x1001001, entry has
  1x -> fails (not sim 2).
- `msubset_e` (entry ⊆ query): entry has 1x2000000, query has
  0x -> fails (not sim 2).

Result: **sim=1 ("kind-only")**, one below the sim>=2 retrieval
bar. `retrieve()` returns -1, `lc_cold` runs, SIM=-1, MODE=0 --
byte-identical to A. The adversary's own design comment on TRAP1
("codes superset of TEACH -> sim 2") shows the sealed prediction
was computed against the clean `[1001001, 1001002]` signature;
the phantom is what falsified K-ADV-M1, not the architecture.

On SEQ2 there is no phantom: TEACHD registers MAPs at ids 0-3 and
is sketched with base=0, nm=4 (`[1001001, 1001002, 1001002,
2002022]`); TFANIN (`[1001002, 1001002, 2002022]`) and TCHAIN
(`[1001001, 1001002, 1001002]`) are both clean multiset subsets
of it, so sim=2 and retrieval fires exactly as designed.

## 2. Evidence (probe, pure Zag, safebin, 3/3 byte-identical)

`probe/probe.zag` = frozen `lc_base.zag` + `lc_mem.zag` +
`adv_worlds.zag` (byte-identical copies from the sealed-eval lane)
+ `probe_main.zag`, compiled with safebin znc, run 3x, stdout
3/3 byte-identical (cmp), empty stderr, exit 0. Output
(`probe/run1.txt`):

- `TEACH(eval base0 nm3)`: nc=3, codes 1001001, 1001002,
  **2000000** -- the phantom.
- `TEACH(clean base1 nm2)`: nc=2, codes 1001001, 1001002.
- `TRAP1`/`TRAP2`: nc=16, 12x1001001 + 4x1001002.
- `SIM(TEACH-eval-entry,TRAP1)=1`, `RETRIEVE(...)=-1` --
  reproduces the sealed SEQ1 result exactly.
- `SIM(TEACH-clean-entry,TRAP1)=2` -- counterfactual: without
  the phantom, the adversary's designed misfire retrieval WOULD
  have fired. The phantom is the difference-maker.
- `TEACHD`: nc=4 `[1001001,1001002,1001002,2002022]`;
  `TFANIN`: nc=3 `[1001002,1001002,2002022]`;
  `TCHAIN`: nc=3 `[1001001,1001002,1001002]`;
  `SIM(TEACHD-entry,TFANIN)=2`, `SIM(TEACHD-entry,TCHAIN)=2`,
  `RETRIEVE(...)=0` -- reproduces the sealed SEQ2 result.

Toolchain: safebin znc; `which python3` / `which python` return
nothing in safebin PATH. No Python executed.

## 3. What is principled vs accidental

**Principled (the mechanism):** retrieval fires iff
(1) `kin`/`kout` match exactly (else sim=0), AND
(2) one inventory's sorted contract-code multiset is a subset of
the other **with per-code counts** (sim=2), or they are exactly
equal (sim=3). This rule alone predicts every sealed C
retrieval/non-retrieval: all 18 problems.

**Accidental (the SEQ1 outcome):** the TEACH signature was
polluted because the eval call sketched one slot past the world's
registered MAPs, and `sketch()` encodes zeroed slots as code
2000000 instead of skipping non-MAP slots. Nothing in the
architecture distinguishes "inventory really contains an
arity-0 all-zero-MAP" from "caller overshot the inventory"; the
pollution then lives forever in the frozen entry.

Ruled out as discriminators: `kin`/`kout` (all 1/2 in both
sequences), `succ`/`fail` (both entries stored with succ=1,
fail=0), memory persistence (MEM=1 in both sequences), world
facts (retrieval never reads facts), and program content
(retrieval keys only on the signature, never the program).

## 4. Predictive boundary: when C will / won't retrieve

Given stored entry E (signature: kin_E, kout_E, code multiset C_E)
and new problem P (kin_P, kout_P, sketched multiset C_P):

1. If kin_P != kin_E or kout_P != kout_E: **never retrieves**
   (sim=0). E.g., a (1,1)-kind entry can never fire on a
   (1,2)-kind problem.
2. Else if C_P == C_E exactly: retrieves, sim=3.
3. Else if C_P ⊆ C_E or C_E ⊆ C_P as multisets (every code's
   count in the smaller ≤ its count in the larger): retrieves,
   sim=2.
4. Else: **never retrieves** (sim=1). C silently degrades to
   byte-identical cold-start A (MODE=0, SIM=-1, identical TRIES).
   There is no signal distinguishing "no relevant memory" from
   "memory exists but signature mismatch".

Corollaries for experimenters:

- **Any uninitialized slot inside [base, base+nm) injects code
  2000000 into the signature** (both at store and at query
  time). A stored entry containing 2000000 can only reach
  sim>=2 against a query whose sketch also contains 2000000
  (via entry⊆query), or against a clean query whose codes are a
  multiset-subset of the entry's real codes (via query⊆entry).
- **Distractor-heavy inventories with duplicated contract codes
  defeat the query⊆entry direction** (counts exceed), so
  retrieval then requires entry⊆query -- i.e., every stored
  code, phantoms included, must appear in the query. This is
  exactly the conjunction that produced sim=1 on SEQ1.
- The silent sim=1 failure mode means a polluted signature is
  indistinguishable from absent memory in every reported
  field. Any future experiment relying on retrieval should
  assert the sketched ncodes equals the world's registered MAP
  count before storing.

## 5. Recommended follow-ups (for the parent)

- The sealed-eval K-ADV-M1 FAIL ("C does not retrieve on
  TRAP1") should be annotated as **artifact-driven**: the
  adversary's predicted SIM=2 misfire was blocked by the
  harness's own base/nm mismatch on TEACH, not by C's
  similarity logic. A clean re-sketch (base=1, nm=2) would
  have produced the designed retrieval. Whether the misfire
  verdict should be re-run with corrected sketch bounds is a
  governance call (it changes a frozen eval input).
- `sketch()` silently encoding zero slots as contract code
  2000000 is a latent defect in `lc_mem.zag` worth a builder
  ruling: either sketch only registered MAPs, or the eval
  harness must guarantee [base, base+nm) covers exactly the
  registered inventory. TEACH is the only sealed problem
  affected (all others register MAPs from id 0).
- No change to the sim>=2 retrieval rule itself is indicated
  by this analysis; the rule behaved exactly as specified on
  all 18 problems.

## 6. Files (this lane)

- `probe/probe_main.zag`: probe main (new, pure Zag).
- `probe/probe.zag`: concat of frozen sources + probe main.
- `probe/probe_bin`: compiled binary.
- `probe/compile.txt`: znc build log.
- `probe/run{1,2,3}.txt`: 3/3 byte-identical stdout; `.err`
  files empty.
- `REPORT.md`: this file.
