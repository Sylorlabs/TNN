# SUF AUDIT: every L3-adjacent claim re-derived from source

**Worker:** REDTEAM-SUF. **Branch:** `redteam/suf-audit`.
**Dir:** `docs/lab/research-lead/overnight-20260928/suf_audit_20261003/`
**Method + kill criteria:** `PREREG.md` (frozen alone at `0f7409c6c`, before this
file existed). **Constructive half:** `L3_CANDIDATE.md`.
**Verification artifact:** `suf_audit_decide281.zag` + `decide281_run.log`
(3/3 byte-identical, sha256 `75c6f10027ef5463c8d17dea1da1af32a66c67c2fbf44b519a4f1e869c139785`).

## 0. Verdict in one line

**The ledger's "L3 achieved anywhere: zero" SURVIVES this audit**, and survives
for a stronger reason than the ledger gives: not one audited lane's emittable
structural form set is non-enumerable from source. But two of the ledger's own
*citations* for that verdict are broken, and one incumbent red team
(`l3_suf_redteam`) passed a lane that fails the charter section 7 question on
its face.

## 1. Scope actually audited, and what was found absent

The prereg named 15 lanes. Result of the search for `l3_niv2` and `calr`:

| Searched | Result |
|---|---|
| `l3_niv2_*` lane directories | **ABSENT from this checkout.** Never committed as source. |
| `l3_novel_intermediate_v2/` (the CALR engine) | **ABSENT.** |
| `calr` as a lane directory | does not exist. |
| `l3_niv2_calr_redteam/` | exists in history at `d5f767bd1` with **PREREG.md + NAMECHECK.md only** |

Ledger entries C350, C358, C364, C367, C391 describe `l3_niv2_*` lanes with
binaries, 3/3 run logs, sha256 digests and `mp_run`/`t2_trial`-style traces.
**None of that source is in the repository.** `git ls-tree -r d5f767bd1` over
the red-team lane returns two markdown files. C350's own text concedes the
cause ("implementation and REPORT.md written but uncommitted pending disk
recovery"). Per prereg K7 this is an artifact failure, but see P1 below: the
cause is a known process failure, so I record it as **NOT VERIFIABLE FROM
SOURCE**, not as a scientific INVALID. The L3 content of CALR (a search over
`mk_cand`/`potential_2`/`lm_cons*.zag` construction stages, per the ledger text)
is a **beam/argmax search over an enumerated candidate pool with two binding
budgets** — on its own description that is K3 BRUTE (pool 32768, TEST budget
50000, argmax over `potential` rank). It cannot be L3, and it does not need to
be audited further to know that.

C391 additionally rests on a **contested ID** (377-466): prereg K8.

## 2. The classification table

Charter section 7 question, answered per lane: *"If I inspect the source BEFORE
the experiment, can I enumerate every structural form the learner could
possibly produce?"*

| Lane / claim | Enumerable from source? | Complete emittable-form set F (source) | Kill criteria met | **Class** | Incumbent said | Delta |
|---|---|---|---|---|---|---|
| `l3_repro_transfer` / `cogop_invention` **C281/C284** (was "L3 VALIDATED") | **YES** | 5 ops x 4 dst x 4 src = **80 instructions**, length <= 6 (`glm_learner.zag:17-18,122,130-149`) | K1,K2,K3,K5,K6,K9 | **L1** | L3 VALIDATED (killed to L2+ by C285) | harsher: **L1** |
| `cogop_invention` **C287** (COGOP-INVENTION) | **YES** | 41-instr menu + `compile_loop` template, 5 slots `P,s0,s1,K,ncall` (`cogop.zag:155,193-215,229`) | K1,K3,K4,K5,K6 | **L2** | "invention demonstrated, C0-B open" | same class, harsher reasons |
| `grammar_program_gpi3` **C397** (GPI-3) | **YES** | 3 frozen node kinds SEQ/PAIR/NEST + 6 emit ops + CALL (`gpi3_learner.zag:33,523,597`) | K1,K2,K4,K9 | **L2** | L2+ | **harsher: L2** |
| `grammar_program_gpi*` **C303/C311/C315** (GPI-1/2/3) | **YES** | same 3-kind vocabulary; `pn_alloc` kinds only {0,1,2} (C311 K11) | K1,K2,K4,K9 | **L2** | "L2-COMPLETE, L3 not claimed" | **agrees** |
| `l3_inr_impl` + `l3_inr_sealed` (L3-INR, brief calls it C459) | **YES** | 1 committed record shape (slot `"G"` literal), content-searched; frozen MAP inventory of 6 (`learner.zag:576`, `MAP_INVENTORY.md`) | K1,K2,K4,K5,K9 | **L2** | L3-KILLED, L2+ | **harsher: L2** |
| `l3_rx` (L3-RX) | **YES** | 4 named ops OP-LIFT/GUARD/UNION/PROJECT (`rx1.zag:4-5`), one committed form shape `guarded` (`rx2.zag:203`), one loop over frozen slots (`rx4.zag:172-218`) | K1,K2,K4,K6,K9 | **L2** | CONDITIONAL-PASS, K10=KILL | agrees (kill) |
| `l3_suf_intermediate` (L3-SUF-1) | **YES** | **4-rung hardcoded ladder**, literal tags 1,2,3,4 (`learner2.zag:491-550`) | K1,K2,K6,K9 | **L2** | REDTEAM-SURVIVES, "L3" | **HARSHER: L2 (main finding)** |
| `cogops` **C335** (H-CONTLIFE-5, verdict "INVENTED") | **YES** | fixed argmin-over-tick rule over 128 slots; victim identity *computed*, not chosen | K6,K9 | **L1** | "INVENTED", self-limited to L2 | **HARSHER: L1** |
| `l3_interm_repr_reuse`, `l3_ctx_pair_hypothesis`, `l3_ctxpair2_hypothesis`, `l3_next` | n/a | no implementation exists | none met | **NO CLAIM MINTED** (prereg only) | none | agrees |

**Nothing is L3. Nothing is L2+.** The highest surviving class is L2.

## 3. Per-claim evidence

### 3.1 C281/C284 (L3-REPRO-TRANSFER, "L3 VALIDATED") -> **L1**. Most overclaimed claim found.

Source: `l3_repro_transfer/orig_glm_learner.zag`, `orig_gl2m_h1.zag`
(read at `cef8c4095`; see P1).

**F is enumerable in four lines.** The frozen op basis is written in the source's
own header comment:

```
//   0=CPY (Rd=Rs), 1=ADD (Rd+=Rs), 2=MUL (Rd*=Rs),
//   3=SET1 (Rd=1), 4=INC (Rd+=1).
```
`glm_learner.zag:17-18`

Construction is an exhaustive triple loop with no search heuristic
(`glm_learner.zag:130-149`):

```
let op:i32=0;
while(op<5){
  let d:i32=0;
  while(d<4){
    let s:i32=0;
    while(s<4){
      ...
      let cs:i32=m_score(W,cand,cn+1,base,nl,d0,d1);
      let gain:i32=cs-bs;
      if(gain>bg){ bg=gain; bop=op; bd=d; bss=s; }
```

So |F| = all programs of length <= 6 over an **80-instruction** closed
alphabet (`cn>=6` stop at line 122). The winner is first-found strict-gain
argmax over those 80, then greedy-accepted. **K1 MENU + K3 BRUTE + K6.**

**The acceptance signal is a researcher-transcribed answer key, not a
consequence.** `m_score` (`:102-109`) probes exactly **two** points,
`d0`,`d1`, and scores agreement with `m_label_lookup` (`:49-58`) against a
table the *driver* fills with hardcoded literals:

```
// G1 labels: base 2176, 22 entries x 12 bytes (D,v,lab)
fn g1_labels(W:[]u8)void {
  lab3(W,b,0,16,17,1); ... lab3(W,b,21,8,0,1);
```
`orig_gl2m_h1.zag:76, 156-166`

and `m_construct` is called with exactly those two probes:
`m_construct(W,OUT,2176,ig(W,24),16,8,0,outp,meta)` (`orig_gl2m_h1.zag:374`).
The learner never queries a world; it looks up literals. **K5 ORACLE LEAK.**

**Empirical confirmation, from source alone.** `suf_audit_decide281.zag`
re-implements only `m_exec`/`m_score` and copies the 22 G1 literals verbatim,
then enumerates the 80-instruction menu exactly as `m_construct` does. It never
touches the learner. Output (`decide281_run.log`, 3/3 identical):

```
BASE 0
PROBES d0=16 d1=8 nlab=22
TIE2 op=4 d=0 s=0 out16=17 out8=9
TIE2 op=4 d=0 s=1 out16=17 out8=9
TIE2 op=4 d=0 s=2 out16=17 out8=9
TIE2 op=4 d=0 s=3 out16=17 out8=9
GAINPOS 4
GAIN2PLUS 4
ARGMAX op=4 d=0 s=0
```

Two things the ledger never says:

1. **The emitted form is computable in advance from the driver's literals.**
   The label table encodes 16 -> 17 and 8 -> 9. `[INC R0]` is the only
   single-instruction form in the 80-item menu producing both. Charter
   section 7 answer: **YES**, decided by inspection.
2. **"win=4,0,0" is a 1-way choice presented as a 3-way one.** All four
   argmax ties are `op=4,d=0,s∈{0,1,2,3}` -- identical semantics, because
   `INC` ignores its source field (`glm_learner.zag:92-93`). The "structural
   choice" is one bit (INC vs not-INC), not a triple.

C285 called this "MENU SELECTION over 5 ops". **Accurate but understated**: the
menu is 80 instructions, the search is exhaustive-then-greedy to depth 6, and
the score is a 22-entry transcribed label table probed at 2 points. C285's own
A1 ("exhaustive trial, no internal criterion") and A2 ("prereg hand-derived
bytes") each independently confirm the stronger bound. Correct class is **L1**:
the contribution is an enumeration plus argmax.

### 3.2 `l3_suf_intermediate` (L3-SUF-1) -> **L2**. Main finding: incumbent red team too generous.

This is the one audited lane where the incumbent red team returned
`REDTEAM-SURVIVES` (bounded) and where I judge that verdict wrong.

**F is a hardcoded 4-rung ladder.** The escalation is straight-line code with
literal tags, and the researcher wrote the ordering down:

```
// escalation enumeration (frozen order):
// (1) further probing < (2a) guard re-expansion < (2b) union re-expansion
// < (3) resolution-slot lifting. Adopt the first composition rendering
// the full history consistent under generic replay.
fn l_escalate(...)
  let t1:=l_tr(...,"FORM_TRY",1,...); l_probe_phase(...);      // :498-499
  let t2:=l_tr(...,"FORM_TRY",2,...); l_guard_reexpand(...);    // :505-506
  let t3:=l_tr(...,"FORM_TRY",3,...); l_union_reexpand(...);    // :515-516
  let t4:=l_tr(...,"FORM_TRY",4,...); ... l_arity_lift(sc);
                            l_fill_record(sc,LOG,AS,TR,t4);   // :524-540
```
`learner2.zag:491-550`

There is no loop, no enumeration variable, no dispatch. F = exactly
{probe-phase, guard-re-expansion, union-re-expansion, arity-lift+fill-record}.
The claimed "resolution record representational level" is one i32 `kind` field
with hardcoded values {0,1,2}:

```
set32(f,0,1);   // kind 0 -> guarded
set32(f,0,2);   // kind 1 -> record
set32(f,8,roff)
```
`learner2.zag:387-395`

and a fixed 20-byte record `(s0,a,b,mask,prov)` (`learner2.zag:431-436`). The
record's *content* is computed by `l_surviving(LOG,ek)`, a researcher-written
predicate (`learner2.zag:412`) -- not chosen.

**The history does determine the rung** (rungs 1-3 fail on W0 precisely because
U has no TEST-ACCEPTs). That is real, and it is the honest core of the lane. But
it is *selection over a researcher-written 4-element menu*, which the taxonomy in
brief section 9 explicitly excludes from L3. **K1 + K2 + K6 + K9.**

**Why the incumbent red team missed it.** Its A-SEARCH bar RT-K3 requires
">= 2 non-marking operator compositions show FORM_TRY with FAIL verdicts before
the marking composition's adoption", and it reports green:

> "**A-SEARCH (RT-K3): green.** Three non-marking compositions genuinely tried
> and rejected on W0 (op_fail=2; TRY_FAIL 1/2/3 in trace) before the lift's
> TRY_OK. ... Not theater."
> `l3_suf_redteam/REPORT.md:141-148`

The bar is **anti-correlated with the L3 criterion**: a hardcoded ladder
maximally satisfies it (FAIL,FAIL,FAIL,OK is guaranteed by construction), and
maximally fails the section 7 test. Both the adversary
(`l3_suf_adversary/REPORT.md:107`, "R-SUF-2 (search theater): not theater") and
the red team dismissed the attack on the same grounds.

Worse, the **parent prereg had already pre-registered this exact kill trigger
and it was never pulled**:

> "The sole-survivor generalization (section 3d) and the escalation enumeration
> (section 3e) are disclosed researcher-authored generic machinery. **If the red
> team shows they do the inventing, that is a SUF-K10 finding**, and the kill
> localizes the blocker to policy provenance."
> `l3_suf_intermediate/PREREG.md:357-361`

The red team had `l_escalate` in hand and read the trace, but never read
`l_escalate`'s structure against section 3e. SUF-K12's 12/12 rule therefore
passed on bars that do not test enumerability.

**In fairness to the incumbent, two things it got right, which I checked and
confirm:** RT-K4 (no counter on the path to the first mark) genuinely holds --
`AS+28` is written at `:514/:523` but read only at `main.zag:191` for a trace
print, never on the marking path; and RT-K5 (no expected value into the learner
process) is not contradicted by anything I read. I do not claim RT-K4 or RT-K5
are broken. The defect is the missing section 7 test.

### 3.3 C287 (COGOP-INVENTION) -> **L2**, self-assessment ACCURATE

The synthesis menu is a literal index space (`cogop.zag:155-156`):
`0..3 INC r | 4..7 DEC r | 8..23 MOVE d,s | 24..39 MOVE d,#i | 40 CALL h` =
**41 instructions**. `planner_search` (`:228-263`) enumerates **all** sequences
of length 1, 2, then 3 exhaustively -- `per = 40+ncall` (`:229`), `per`, `per^2`,
`per^3` candidates -- and returns the first that satisfies `body_ok`. Textbook
**K3 BRUTE** over a closed DSL.

The "op tower" is `compile_loop` (`:193-215`), a **fixed researcher-written
REPEAT template** with 5 slots: `prologue_emit` (by profile P), `MOVE K`, `BEQ`,
body `s0`, optional `s1`, `INC`, `BEQ back`, `RET`. Inventing OP_MUL = choosing
`s0=CALL OP_ADD` and a `K`. **K4 TEMPLATE.**

The acceptance signal is a researcher-written oracle, not a consequence:
`body_ok` (`:217-227`) compares against `world_for(stage,a,b)` (`:374-378`) ->
`world_add`/`world_mul`/`world_pow`, with the 10 training triples hand-listed at
`:392-396`. **K5 ORACLE LEAK.**

The lane's own honest limit -- "REPEAT schema researcher-enumerated; does not
clear C0-B open-form bar" -- is **accurate**. It is if anything generous to the
lane. The strongest surviving element is the "stage-2 surprise" (a different
valid multiplication than predicted); that is real novelty of *content*, inside
a template whose *form* was written by the researcher. Correctly not L3.

### 3.4 C397 (GPI-3) -> **L2**, incumbent marginally TOO GENEROUS

F = 3 frozen plan-node kinds + 6 primitive emit ops + CALL. The source states
the closure outright:

```
//   784..1039:  plan nodes, 32 x 8B [kind,depthlv,count,child,next,tokL,tokR,live]
//                kind 0=SEQ 1=PAIR 2=NEST; child/next ids, 255=none.
```
`gpi3_learner.zag:32-33`, cf. `:7` ("FROZEN SEQ/PAIR/NEST vocabulary (kinds
0,1,2 only)"), `:523` (`while(t<3)` over exactly 3 token types), `:597`
(`if(ok==1 && kind!=0 && kind!=1 && kind!=2){ok=0;}` -- rejects any other kind).

The lane's own ledger text is candid and I confirm it from source: "the
invention is factorization (naming a verified solution), not synthesis of a
novel strategy; the learner did not invent the WRAP/SEQUENCE strategies (those
are the frozen templates)".

**Where the incumbent is too generous:** it reports **L2+**. Under prereg K4
("novelty is in slot arguments, the structure is a fixed template" -> <= L2),
factoring a verified flat solution into a name and substituting `CALL` *is* slot
filling. L2+ requires that structure "vary in a way the source does not literally
enumerate"; here the template grammar is literally enumerated at `:32-33` and
closed at `:597`. Class **L2**. This is a one-notch correction and I flag it as
judgment, not as a discovered fraud.

The wider GPI series (C303, C311, C315) is **accurate and I endorse it without
qualification**. C303: "the node vocabulary (SEQ/PAIR/NEST) and the
nested-core-plus-tail builder strategy are researcher-designed; the learner did
not invent the NEST combinator ... No finite operator menu widened." C311:
"it instantiated a researcher-supplied vocabulary and decomposition strategy with
computed parameters." Those are exactly the right words and they are exactly
what the source says.

### 3.5 L3-INR (brief: C459) -> **L2**, self-assessment ACCURATE, ledger ID BROKEN

F = one committed record shape. There is exactly **one** slot name in the source,
a string literal: `slot_load(sd,"G")` (`learner.zag:576`), committed to via
`let slot:[]u8="G"; if(ig(s,76)==5){ slot="G2"; }` (`:1114-1115`). The frozen MAP
inventory is a 69-line human-readable enumeration of 6 MAPs
(`MAP_INVENTORY.md:15,23,32,38,45,53`), attested "the implementation adds zero new
MAPs, zero new opcodes, zero new semantic cases". The learner searches
**content** (which edges/hypotheses to keep, `hyps_filter` `:206`,
`emit_rank` `:333`) against a held-out label channel.

The lane's `L3-KILLED` with `K12 (7/12 rule): K3, K5, K7, K8 are RED. Any red is
L3-KILLED. Partial credit does not exist.` (`REPORT.md:73-74`) and its
reclassification to L2+ are **accurate**. On my ladder it is **L2**: the record
form is a hardcoded slot, and the inventory is a menu.

### 3.6 `l3_rx` (L3-RX) -> **L2**; RX-KC0B is an OVERCLAIMED BAR

F = 4 named operators, declared in the source header:

```
// certificate -> operator-built form (OP-LIFT/OP-GUARD/OP-UNION/
// OP-PROJECT), or kb reuse.
```
`rx1.zag:4-5`

There is exactly **one** committed form shape -- `commit_guarded` (`rx2.zag:203`,
"COMMIT form guarded") -- and the entire "expansion search" is one loop over a
frozen slot list: `while(si<nds){ let slv=ig(ds,si*4); induce_candidate(...,slv,...) }`
(`rx4.zag:172-218`). The only free variable is *which slot index to lift*.

The lane's own ledger bar **RX-KC0B "Open structural form: PASS"** is justified
as "No arity cap; guard values/perms vary by world (gvsum 38-2031623)". **That
justification is wrong on its own terms**: varying values and perms is not
varying form. The operator vocabulary is a closed 4-item list and the committed
form is a single shape. This bar should be RED. The lane's overall K10 was
already a KILL, so the verdict does not change -- but the bar is recorded here
because a future lane could inherit "no arity cap => open form" as a valid
criterion, and it is not one.

### 3.7 C335 (H-CONTLIFE-5, verdict "INVENTED") -> **L1**, the most overstated *verdict label*

The lane's own honest scoping is better than its verdict:

> "the invention finding is L2-level, explicitly NOT L3 -- the criterion form
> (extremum over recency) is researcher-authored generic machinery stated as
> setup; what the learner invented is the response content (which entries to
> sacrifice)"
> `CLAIM_LEDGER.md` C335

And then the ledger text undercuts itself further:

> "each DECISION trace shows victim tick == minimum tick over 128 scanned
> slots. A fixed default cannot produce the {6001,6002} vs {1032,1041} split."

That sentence is the kill. If a **fixed rule** ("argmin tick over 128 slots")
cannot produce the split, then the split is produced by the *state*, not by any
choice the learner made. There is no free structural degree of freedom left for
the learner to exercise: the victim set is a deterministic function of the
learner-written tracking table. **K6 SCORE-RANK + K9 NO-FREE-STRUCTURE.** No
form is invented; an argmin is evaluated. The honest scoping's phrase "the
learner invented ... which entries to sacrifice" overstates it: the learner
*computed* which entries to sacrifice. Class **L1**.

The lane's artifact was not available to me at any commit (`contlife5/` is
absent from HEAD and from `cef8c4095`), so this rests on the ledger's own
detailed mechanical description rather than on source I read. Stated as a
boundary in section 6.

## 4. Adversarial findings in BOTH directions (prereg M4 / S4)

**(a) A lane MORE bounded than it admits** -- 3 found, all confirmed from source:
- **C281/C284**: C285 said "menu selection over 5 ops"; it is 80 instructions,
  depth-6 greedy, scored against a transcribed 22-entry answer key at 2 points,
  and the reported 3-tuple `win=4,0,0` is a 4-way tie on one bit. C285 ->
  **L1**.
- **C287**: honest limit names only the REPEAT schema; the 41-instruction
  synthesis menu, the exhaustive `per^3` enumeration, and the `world_*` oracle
  are equally researcher-written.
- **C335**: honest scoping says "L2"; the correct class is **L1**.

**(b) The incumbent red team TOO GENEROUS** -- 2 found:
- **`l3_suf_redteam`**: returned `REDTEAM-SURVIVES` on a lane whose F is a
  hardcoded 4-rung ladder. RT-K3 is anti-correlated with the section 7 test. The
  parent prereg's own pre-registered trigger (`PREREG.md:357-361`) was never
  evaluated. Correct class **L2**, not L3-survives.
- **C397**: reported L2+; K4 forces L2.

**(c) The incumbent red team NOT too harsh** -- confirmed, no correction:
C303/C311/C315 (GPI series), C287, and L3-INR's self-kill are all accurate.
I could not find a case where a lane was more generous to itself than its own
source warrants *except* the two in (b). I looked for one and am reporting that
it is rare, not that it does not exist.

## 5. Does "L3 achieved anywhere: zero" survive?

**YES. Strengthened.**

The ledger's stated reason is a list of self-admissions (brief section 9). That
is the weakest possible form of the argument -- it is the incumbents grading
themselves. The audit does not rely on it. The verdict survives because, for
every lane with recoverable source, **F is enumerable by inspection**, and in the
two cases where the incumbent graded itself most generously (C281 and L3-SUF-1)
F is enumerable in under ten lines of source reading.

Two independent supports the ledger does not currently have:
1. C281's emitted form is **mechanically decidable** from driver literals, and I
   demonstrated it in Zag with 3/3 determinism.
2. Every lane's escape hatch is the same shape: a researcher-written finite menu
   plus a criterion that *ranks* it. Ranking is not inventing.

## 6. Boundaries of this audit (stated against myself)

- **B-A1** `contlife5/` (C335) and the whole `l3_niv2_*` / `calr` family have no
  source in the repository. C335's classification rests on the ledger's detailed
  mechanical description, not on source I read. **If C335's `learner_adapt`
  turns out to contain a free choice I could not see, its class moves L1 -> L2.**
  It does not move to L3: the ledger's own "fixed default cannot produce the
  split" sentence forecloses that.
- **B-A2** I did not run any audited mechanism. I ran one program of my own
  (`suf_audit_decide281.zag`). I did not re-verify any lane's PASS/FAIL verdict,
  digest, or determinism claim -- those are out of scope and I take no position.
- **B-A3** GPI-3 L2-vs-L2+ is a judgment call at the boundary and I flag it as
  such rather than as a kill.
- **B-A4** I did not audit non-L3 lanes (COGOPS family, IVWC, BELIEF, H3,
  reclamation, ...). A lane that never claimed L3 cannot inflate the L3 count,
  so they are out of the kill path. A lane could still be *overclaimed at L2*;
  that is unexamined.
- **B-A5** Absence of a directory is treated as a provenance finding (P1), not
  as scientific INVALID, because the deletion cause is known and is a process
  failure. I declined to let my own K7 criterion produce a false accusation.

## 7. Provenance findings (governance, not science)

**P1 -- The C281/C284/C285 and the entire CALR family have no source at HEAD.**
`l3_repro_transfer/` and `l3_redteam/` are present at `cef8c4095` and absent at
HEAD. The deleting commit is **`b3b3ee00a` ("lm3_lifetime: prereg ...")**, whose
subject has nothing to do with them:

```
b3b3ee00a lm3_lifetime: prereg (PREREG.md + NAMECHECK.md); frozen kill bars
B1-B7 before implementation. Non-ledger.
 .../l3_repro_transfer/orig_glm_learner.zag            | 243 ---
 .../l3_redteam/v0/learner.zag                         | 243 ---
```

A preregistration commit silently deleted the primary artifacts of the
governing negative result. The commits are ancestors of HEAD, so the blobs are
recoverable; nothing is lost, but **the canonical branch currently does not
contain the evidence for its own central claim**. Recommend restoring both
directories from `cef8c4095`.

**P2 -- The worker brief's key citation does not exist.** Brief section 9 cites
"**C459** L3-INR-SEALED". The canonical ledger's highest ID is **C410**
(258 entries, `- C4xx` max = 410). `grep -c C459` = 0. L3-INR-SEALED lives only
in the lane commit `8c6af9c4f`, unledgered. The brief's citation of the
*central* piece of evidence for the L3 verdict is a dangling reference.

**P3 -- Three-way ID collision on one fact.**
- `l3_suf_intermediate/PREREG.md:31` cites "**C409**" for L3-INR. C409 in the
  canonical ledger is **JOINT-BLINDNESS (composition_jointblind/)**, an
  unrelated claim that PASSed.
- The same file `:33` cites "**C453**" for L3-RX. C453 does not exist.
- Two different GPI-3 claims exist: **C315** (lane series, "Vocabulary not
  extended, family not contorted") and **C397** (`grammar_program_gpi3/`,
  "clean-restart", prereg `170174a90`). Distinct experiments, same name.

None of this changes a verdict. All of it changes whether a reader can *check*
a verdict, which is the thing the ledger exists for.

## 8. Claim IDs minted by this audit

C5xx block, per PREREG section 9. C377-C466 not touched.

> **ID-COLLISION DISCLOSURE (post-hoc, disclosed not hidden).** My first results
> commit (`5f287376e`) minted **C500/C501**. Concurrent lanes
> `ns_invariant/PREREG.md` (C500-C509) and `cogops_unify_general/`
> (C500-C506) independently occupy the same block, so C500/C501 were **not
> free**. Re-minted to **C590/C591** by follow-up commit; the earlier commit is
> left standing rather than amended. This is a live hazard in the current
> mint regime: with the ledger restored to C410, every worker is minting into
> C5xx from scratch and there is no allocator. Recommend the mint guard assign
> disjoint blocks rather than leaving workers to self-select.

- **C590 -- SUF-AUDIT-VERDICT.** Independent source-first audit of all
  L3-adjacent claims. **"L3 achieved anywhere: zero" is CONFIRMED and
  strengthened.** No audited lane reaches L2+. Classification ladder applied:
  C281/C284 **L1** (from "L3 VALIDATED"), C335 **L1** (from "INVENTED"),
  C397 **L2** (from "L2+"), C287 **L2**, GPI series C303/C311/C315 **L2**,
  L3-INR **L2**, L3-RX **L2**, L3-SUF-1 **L2** (from "REDTEAM-SURVIVES").
  Charter section 7 answer is YES for every lane with recoverable source.
  Evidence: `suf_audit_decide281.zag` 3/3 identical sha256 `75c6f100...`.
- **C591 -- SUF-K10-CORRECTION.** `l3_suf_redteam`'s `REDTEAM-SURVIVES` is
  **overturned**. `l_escalate` (`learner2.zag:491-550`) is a hardcoded 4-rung
  ladder with literal tags and a source-comment naming the frozen order; F is
  enumerable in four lines; RT-K3 is anti-correlated with the section 7 test;
  the parent prereg's pre-registered trigger at `PREREG.md:357-361` was never
  pulled. Correct class **L2**. RT-K4 and RT-K5 are **not** broken and are
  explicitly not contested here.

Not minted (avoided to prevent collision, flagged instead): a claim for P1/P2/P3
provenance findings. Recommend governance mint those separately.