# TRANSCRIPTIONS (C665) — every criterion this lane transcribed, with its quoted source

Worker L3-GATE-2. Lane `lane/l3gate2`. Written before the criteria were applied
to the gates, per `PREREG_2.md` §G2.3. Each entry gives the **verbatim span**
the transcription came from, so a reader can check the transcription without
reading any code. Each transcription carries a **cross-check number** it must
reproduce from the claim's own report; a transcription that fails its own
cross-check is VOID (self-falsifier S2-F3).

Nothing here is transcribed from an implementation. Where a needed datum exists
only in code, that is stated and the claim is reported VOID rather than guessed.

---

## T1 — C281 / CALR (XDOMAIN-GRAMMAR-L2M). Verdict: **USED**

Source: `xdomain_grammar_l2m/PREREG.md` §4 (at `lane/restores` and at
`4e7eb30b1`, byte-identical tree sha `51e309ba…`).

> "M is a generator program over a frozen generic op basis … Registers R0..R3
> (i32). R0 preloaded with D. Output is R0. Ops: 0=CPY (Rd=Rs), 1=ADD (Rd+=Rs),
> 2=MUL (Rd\*=Rs), 3=SET1 (Rd=1), 4=INC (Rd+=1). Instruction = (op,d,s), 3
> bytes, max 6 instructions."
>
> "m_construct: greedy search … Each round evaluates every (op,d,s) append
> (5\*4\*4=80 candidates); score = number of training divisors whose emitted word
> carries label 1 in the label table (table miss counts 0) … ties broken by
> candidate order (op 0..4, d 0..3, s 0..3, first-max)."
>
> "G1 fresh construction from empty: baseline score 0 (w=D, label 0). Round 1:
> all 64 op-0..3 candidates score 0; (4,0,0)=INC R0 is the first positive-gain
> candidate with gain 2 … M = [INC R0], program bytes (4,0,0), score 2/2, stop."

**Declared space** `F` = all 80 one-instruction `(op,d,s)` candidates, plus the
empty program (81 total). **Declared bound**: the claim's own bound, 6
instructions; G2 walks the 1-instruction layer, which is the whole of the
adopted program.
**Criterion**: `score(op,d,s) = lab_1(prog(D=16)) + lab_1(prog(D=8))` over the
22-entry G1 label table; `lab` table miss counts 0.
**Cross-check number the claim publishes**: `score = 2/2`, bytes `(4,0,0)`.
**Op semantics source** (independent of the claim's code): `lane/reaudit`
`calr_isa_probe.out.txt`, which measured them **by execution** at R0=7, Rs=5 →
`5, 12, 35, 1, 8`. Those five numbers occur nowhere in the implementation.
**Result**: reproduced exactly, plus `N_AT_MAX = 4`.

---

## T2 — C603 MACRO-FLOOR (lane `l3macro_unknowndepth`). Verdict: **INHERITED, NOT RE-TRANSCRIBED**

The criterion and its enumeration were transcribed by `lane/l3gate`
(`g2_dn.zag`) and I did not re-derive them; doing so would have been a second
unvalidated transcription, and I had no budget for a second careful one. The
numbers below are **inherited from `lane/l3gate` §"G2 detail, C603"** and are
labelled as inherited everywhere they appear.

Claim's own class assertion, quoted from its REPORT line 22:
> "**Class: L2. Not L3.** No L3 claim is minted."

and its KB1 row:
> "**KB1 SUF enumerable** | **HOLDS → NOT L3** | `F = B × {R0..R3} × {LT,EQ,GT,
> LE,GE} × ℤ`, writable in one line. Declared in the prereg *before* the code
> existed."

Inherited: space `97 bodies × 4 src × 5 cmp × 6 thr = 11640`;
`NSAT_unamended 4667, NTRIV 1642, tau 0.3518, VACUOUS-0`;
`NSAT_amended 349, NTRIV 0, tau 0.0000`.

**Note that C603 is not in the canonical ledger and not in
`STAGED_LEDGER_ENTRIES.md`.** `grep -rl C603` over the whole research-lead tree
returns only `lane/l3gate`'s own documents. C603 is a **lane-local claim ID with
no ledger entry**, which is a provenance fact the parent lane did not report.

---

## T3 — C453 L3-RX-BUILD. Verdict: **PARTIALLY RE-DERIVED**

Source: `l3_rx_k10/run_1/w1/{train,heldout}.txt` (the claim's own sealed world,
106 train / 6 heldout, id universe 8) and `l3_rx_k10/REPORT.md`.

**Criterion** (claim's own words, ledger/STAGED entry for C453):
> "CONDITIONAL-PASS 15/16 (representational expansion under proven insufficiency)"

The measurable internal criterion is the one the parent transcribed: *the
induced form must predict **every** training observation*. Cross-check number:
the claim's own learner reaches 0 mispredictions.

**What I re-derived** (`prov_l3claims.zag` block 3 uses the same discipline on
the sibling sealed key): from `SEALED_KEY` S1's own literals — 6 held-out items
and 3 declared gaps — the largest held-out score reachable by a purely
adjacency-based trivial form is `6 − 3 = 3`, below the frozen bar of 5.
**Cross-check**: the claim itself reports `C0 HELD 4/6` and `T1 HELD 4/6`.
**Result**: reproduced in direction; my `3/6` is an upper bound under adjacency
only and is *not* claimed to equal the claim's 4/6.

---

## T4 — C397 GPI-3. Verdict: **USED for G2, VOID for G1**

Source: `grammar_program_gpi3/PREREG.md` §10, at `87a822426`.

> "K3 CONSTRUCT: plan_build(4,…) returns root >= 0; program 0: plen = 8, ops
> [4,2,0,1,3,5,0,1], bytes 123,91,40,41,93,125,40,41, acc = 1, measD = 3,
> measP = 4."

> "K0 STRUCTURAL-DIFFERENCE: PASS iff the run uses exactly the Section 2 family
> (three types, stack discipline, AND depth budget Dmax=3) …"

**Criterion shape**: `SHAPE-CONJ` — a conjunction of fifteen frozen kill bars.
**Declared space**: the three frozen templates plus the primitive emit slots,
at the claim's own `DIRECT` budget of 20000 ops.
**Cross-check number the claim publishes**: `measD = 3`, `measP = 4`.
**G2 decision**: no structurally trivial candidate reaches `measD = 3` — a
do-nothing candidate emits 0 bytes (depth 0), a constant-output candidate emits
1 (depth 0), an identity emits 8 (depth 0). ⇒ `NTRIV = 0`.
**G1: VOID, honestly.** I could **not** decide `measD = 3` from literals: the
op-code → bracket-type mapping is not published in the claim's declaration, and
my first attempt guessed it and got 1 instead of 3. That is reported as
`DL_DEPTH NOT_DECIDABLE_FROM_PUBLISHED_LITERALS` rather than papered over. This
is the second time in this program that a guessed mapping produced a wrong
number (the first was the parent's C453 "constant pad id"), and it is the same
failure mode both times.

---

## T5 — L3-SUF-1. Verdict: **USED**

Source: `l3_suf_intermediate/PREREG.md` §5, at `87a822426`.

> "T0 INVENT (W0): … PASS: (i) trace shows the first UNRESOLVED-mark strictly
> after the first committed-prediction REJECT (SEQ order); (ii) A-SEARCH passes
> (>= 2 non-marking operator compositions tried and rejected on W0 before
> adoption); (iii) post-escalation stakes: 0 REJECTs on determined queries, all U
> queries ABSTAINed."
>
> "T2 ABSTAIN (F-B): PASS: (i) 0 wrong predictions on heldout; (ii) >= ceil(5\*D_det/6)
> correct on the determined pairs; (iii) ABSTAIN on 100% of the undetermined pairs."

**Criterion shape**: `SHAPE-CONJ` over eight treatment arms T0–T7 (plus four
controls C0–C3 which the gate does not count as treatment).
**Cross-check number the claim publishes**: "All 8 DEV treatments pass."
**G2 decision**: a do-nothing candidate — emits nothing, abstains everywhere,
never probes, never invents, commits nothing — satisfies **0 of 8** arms:
T0(i) needs a mark after a REJECT, T1 needs a slot-varying probe, T2(ii) needs
`ceil(5·D_det/6)` correct on determined pairs (do-nothing is correct on 0),
T3 needs a verification TEST, T4–T6 need T2-style bars, T7 needs >= 5/6.
⇒ `NTRIV = 0`, and `tau-bar = 0/8`.

---

## T6 — L3-INR. Verdict: **USED**

Source: `l3_inr_sealed/REPORT.md` + `SEALED_KEY.md`, at `87a822426`.

> "K5 (hidden instances solved): FAIL (RED) — Requires: T1 >=5/6 with |E|<=10;
> T3 exact; T3b >=5/6; T4 >=5/6; T5a commits correct; T5b DEFERS. T1: 4/6, 12
> edges -> FAIL."

> "S1 (s1.world) — Incomplete-disambiguation trap … Gaps: (z4,z5),(z5,z6),(z6,z7)
> [adjacent, not direct edges]. … HELD 4/6, EDGES 12 -> FAIL."

**Criterion shape**: `SHAPE-CONJ` over the nine frozen bars K1–K9 of the
adversary's own battery.
**Declared space**: the arms the claim itself declares — TREAT plus controls
C0 attr-NN, C1 memo+1NN, C2 ablate-construct, C3 greedy, C4, C5.
**Cross-check number the claim publishes**: `HELD 4/6`, `EDGES 12`.
**G2 decision**: the largest held-out score reachable by an adjacency-only
trivial form is `6 − 3 gaps = 3`, below the frozen bar of 5. ⇒ `NTRIV = 0`.
**Note**: C459 (L3-INR-SEALED) is **not in the canonical ledger**; it exists only
in `ledger_write/STAGED_LEDGER_ENTRIES.md`. Its own verdict is quoted there:
"L3-KILLED. Verdict: L3-KILLED (reclassified L2+)."