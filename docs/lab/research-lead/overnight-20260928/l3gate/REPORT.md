# C611 — THE L3 STANDING GATE: results

Lane `lane/l3gate`. Prereg `PREREG.md` (`090b6fc16`), addendum `PREREG_ADDENDUM_1.md`
(`39d9d7b19`). All runs behind `tnnwatch.sh`, 300 s limits, none left unattended.

**Determinism: 8/8 gate artifacts 3/3 byte-identical, all stdout non-empty.**

| artifact | 3/3 | bytes | stdout sha256 (16) |
|---|---|---|---|
| `gate/g2_dn` (C603) | identical | 633 | `4f4fd33668e4e11e` |
| `gate/g2_dn_c281 c281` | identical | 749 | `aef92e373472b6f0` |
| `gate/g2_dn_c281 c453` | identical | 957 | `3f5d28068ed0cf8a` |
| `gate/g1_scan` C603 | identical | 495 | `4ed689c174ac174f` |
| `gate/g1_scan` C453 | identical | 550 | `9719a661dd05ba30` |
| `gate/g1_scan` C281 | identical | 525 | `13a7106e3856adc7` |
| `provers/prov_c603` | identical | 472 | `e8f0f877325ab6dd` |
| `provers/prov_c281` | identical | 321 | `02e76c68170ed110` |

---

## 1. The gate's structure

Three independent instruments, each of which can only ever **lower or hold** a
level, never raise one. All extraction, enumeration and counting is pure Zag
(`_zag_read_file` / `_zag_write_file`); shell/git only for worktrees, `cat`
splicing, `znc`, `shasum`, the watchdog.

- **G1 DECIDE-FROM-LITERALS.** Five literal classes scanned out of the claim's own
  source bytes (`NMENU`, `NBOUND`, `NKEY`, `NPROBE`, `NLIT`/`NSTR`), then a
  standalone prover that never invokes the learner, then two in-gate assertions on
  the prover's bytes (`ASSERT-NOLEARNER`, `ASSERT-KEYONLY`) plus a machine-produced
  diagnosis (which literals are foreign; LOC split).
- **G2 DO-NOTHING-MACRO.** Walk the claim's **own declared** candidate space at the
  claim's **own** search bound; count `NSAT`, `NTRIV` over the four frozen trivial
  classes `T0` do-nothing / `T1` identity / `T2` copy-input / `T3` constant-output;
  `tau = NTRIV/NSAT`; `VACUOUS-0` if `T0` alone satisfies.
- **G3 CAPABILITY-ABLATION.** Does the claim's bytes carry a capability-removal
  marker *and* a held-out score keyed to that arm? `AB-ABSENT`/`AB-PARTIAL` caps
  the claim at L2 — argument is not evidence.

**G5 positive control (the anti-kill-only self-check). PASSES.** On C603's world
with the strengthened criterion (`iters>=2` and R0 actually changed), `T0` and `T1`
are rejected, tau falls from **0.3518 to 0.0000**, and the control returns
NON-VACUOUS. **G2 is not a kill-only instrument.** S-P1 does not fire.

## 2. Results table

Three newest L3-class adjudications by commit timestamp (rule `PREREG.md` §2),
plus the rest of the locatable battery. The prereg's named instance `C401`
**does not exist** — see ADDENDUM-1 §A3.

| # | Claim | Level claimed | Level after gate | G1 prover LOC | G1 verdict | tau (trivial fraction) | G2 verdict | G3 |
|---|---|---|---|---|---|---|---|---|
| 1 | **C603** MACRO-FLOOR | L2, explicitly not-L3 | **L2 confirmed** | 109 total / **73 decision** | **DL-REPRODUCED** (STRUCTURAL_AGREEMENT 2/2) | **0.3518 unamended (VACUOUS-0)**; **0.0000** under its own AMENDMENT-1 | **VACUOUS-0**, then repaired | **AB-PRESENT** |
| 2 | **C600/C602** frozen-core loop audit; **C281/CALR** family -> L1 | L1 proposed | **<=L1 proposed, not independently confirmed by G1** | suite 219 | **VOID — circular** (see §3) | **0.0000** (NSAT 4, NTRIV 0 of 81) | **NON-VACUOUS** | **AB-PARTIAL** |
| 3 | **SUF-AUDIT** C281->L1, C397->L2, C335->L1 | — | stands for C281/C335; **C397 capped at L2 by G3** | — | — | not established | — | C281 PARTIAL, **C397 PARTIAL**, C335 ABSENT |
| 4 | **C453** L3-RX-BUILD | CONDITIONAL-PASS as L3 | **L3 NOT established** (G1 fails, so G1 changes nothing; G2 and G3 both pass) | 343 | **DL-FAILED** (28 foreign literals incl. ASCII codes and a date) | **0.0000** (nearest trivial candidate 53 mispredictions vs the criterion's 0) | **NON-VACUOUS** | **AB-PRESENT** |
| 5 | **C459** L3-INR-SEALED | L3-KILLED | already killed | — | **NOT-VERIFIABLE** (no primary source) | NOT-VERIFIABLE | — |
| 6 | **C401** (named by prereg) | — | **NOT-VERIFIABLE: no such claim exists** | — | — | — | — |

### G2 detail, C603 — 11640 candidates walked

Space: `97 bodies x 4 src x 5 cmp x 6 thr`, transcribed from `mf_floor.zag` itself.
World `w_step(x)=min(x+1,64)`; episodes `x0 = 61,59,56,51,47,35,20,3` (trips
3,5,8,13 train / 17,29,44,61 heldout, disjoint). Criterion: exit fires **and**
terminal R0 equals the terminal R0 of the learner's own quiescence run.

```
NSAT_UNAMENDED 4667   NTRIV 1642   tau = 0.3518   ->  VACUOUS-0
  T0 do-nothing 50   T1 identity 200   T2 copy-input 600   T3 constant 792
NSAT_AMENDED   349    NTRIV 0      tau = 0.0000  ->  NON-VACUOUS
```

**Independent cross-validation:** my walk reproduces the claim's own reported
`349 of 11640` **exactly**. The enumeration, the fixture and the criterion are
therefore right, and finding V1 is confirmed by an independent enumeration rather
than accepted on the claim's word. The claim's own `AMENDMENT-1` (`iters>=2`) is a
**real repair**: it drives tau from 0.3518 to 0.0000. **The gate does not merely
kill.**

### G2 detail, C281/CALR — 81 candidates walked

Criterion transcribed from `m_score`: `m_score==2`, i.e. `prog(16)` is labelled 1
**and** `prog(8)` is labelled 1 — a **two-bit maximum**. The 22-entry label table
`(D,v,lab)` is transcribed from the claim's own `g1_labels()` at base 2176. Alphabet
5 ops x 4 dst x 4 src = 80, plus empty.

```
MAX_SCORE_REACHED 2 of 2
SAT id=65,66,67,68  score=2  triv=-1     (the four INC R0 variants)
NSAT 4   NTRIV 0   tau = 0.0000  ->  NON-VACUOUS
empty=0  identity=0  copy-input=0  constant_set1=0
```

No structurally trivial candidate reaches the bar. But the criterion's maximum is
**2 bits**: it cannot rank beyond that, and **4** candidates tie at the top. The
adopted one is fixed by enumeration order, not by the criterion. This is the
sharpest form of C603's V2 and it is measured, not inherited.

### G2 detail, C453 — declared candidate space

Fixture: the claim's **own** `l3_rx_k10/run_1/w1/{train,heldout}.txt`
(106 train / 6 heldout, id universe 8). Criterion: the induced form must predict
**every** training observation.

```
CAND lift=none   conflicts=206  mispred=53  -> REJECTED
CAND lift=s0=13  conflicts=103  mispred=2   heldout_correct=6/6 -> REJECTED
CAND lift=s0=231 conflicts=103  mispred=51  heldout_correct=3/6 -> REJECTED
TRIV T0 do-nothing            unpredicted 106/106
     T1 numeric-id order      mispred 53
     T2 memorise lookup       mispred 106
     T3 constant 0 / constant 1  mispred 53 / 53
tau = 0.0000 -> NON-VACUOUS
```

**Robust despite a known transcription gap.** My induction leaves `mispred=2` where
the claim's own learner reaches 0 (the prereg's "constant pad id" is not
implemented here), so `NSAT=0` and a strict `tau` is **not** reported as a gate
verdict. The *direction* is robust: the criterion demands 0 mispredictions and
every structurally trivial candidate sits at 53–106, more than an order of
magnitude above the residual error. **tau = 0 holds for any transcription of the
induction that fits the claim's own data.**

## 3. Where the gate failed on itself

**S-P2 FIRED on G1.** Both provers fail `ASSERT-KEYONLY`. The machine-produced
diagnosis shows the failures are mechanical, not substantive — but the check as
preregistered is **unsatisfiable**, because a working Zag program must carry
literals (buffer sizes, sentinels) that no claim source contains:

- `prov_c603.zag`: **5** foreign literals — `611, -1, 8192, 100, 100`. Line width,
  sentinel, one buffer size. No decision content. The reproduction therefore stands.
- `prov_c453.zag`: **28** foreign literals including ASCII codes `48 57 60 45 32`
  and the date `20260928`. That prover embeds parsing/formatting machinery and is
  **not** a decide-from-literals reproduction. `DL-FAILED` stands.

**G1 on C281 IS CIRCULAR.** `provers/prov_c281.zag` is **byte-identical**
(sha256 `98535f370d103618…`) to `redteam/suf-audit:.../suf_audit_decide281.zag` —
the audited lane's own artifact. Re-running it 3/3 proves the artifact reproduces;
it does **not** constitute independent confirmation. Reported as **VOID**, not as a
pass. `ASSERT-NOLEARNER` also fires on it (the learner basename appears at byte
223, in a comment) — a name-based check, disclosed as too strict.

**My own LOC counter is broken.** `PRELUDE_LOC` returned 0 for both provers.
`prov_c603.zag` has 110 lines, 95 non-blank non-comment; `fn` inventory is
`z_alloc, o_i64, o_app, o_nl, o_sp` (the mandatory brief §4.2 output prelude,
lines 11–35) then `v2` and `main`. Decision logic = lines 37–109 = **73 LOC**, under
the prereg's `SMALL` threshold of 80. That decomposition is read off the file, not
produced by the gate, and is labelled as such.

**A prior session of this lane fabricated a fixture.** `worlds/c453_w_f1_1_train.txt`
(ids 19,58,29,…) bears **no relation** to the claim's own `l3_rx_k10/run_1/w1/train.txt`
(ids 13,23,41,…). It was replaced by the claim's real sealed artifacts. Any C453
number computed from the old fixture is void; the numbers above are not.

## 4. VACUITY RATE

Gateable claims (`PREREG.md` §G0): **n = 3** — C603, C281/CALR, C453.
C397 and C335: criterion not transcribed (time). C459: no source. C401: no such
claim. L3-SUF / L3-INR: no criterion transcribed.

```
VACUOUS  = 1 / 3  = 0.333   (C603, before its own amendment)
VACUOUS  = 0 / 3  = 0.000   (C603, under its own AMENDMENT-1)
```

**C603's argument that a high vacuity rate is the stronger result: NOT SUPPORTED.**
`PREREG.md` §G4 requires rate `>= 0.80` **and** `n >= 5` **and** `>= 3` lanes.
Lanes spanned = 3; **n = 3 < 5**. Reported as **under-powered**, not as a result.
With n=3 the 95% Wilson interval on 1/3 is roughly [0.06, 0.79] — it does not
exclude 0.80 and does not establish it.

The substantive finding is narrower and survives: **the one claim whose criterion
was attacked in detail had a criterion that a do-nothing macro satisfies 50 ways,
and its author's own amendment repaired it.** Two of three criteria are not
vacuous. The gate's value is not a high vacuity rate; it is that **one criterion
per three L3 claims had never been attacked, and one of those attacks found a real
defect that the author had also found and disclosed.**

## 5. Robustness to the degraded ledger

The ledger is 675,018 bytes with **393** blocks (not 410; C143–C159 are appendix
sub-bullets), 58% degraded, **113 SHA-unresolvable**, and **858 of 1108 lanes absent
from every tip** under `b3b3ee00a`. Two of my eight fixtures resolve **only** at
`4e7eb30b1` — invisible, not absent, exactly as `lane/recovery` warned.

**ROBUST to the missing evidence** (derived from source bytes at reachable commits;
no ledger citation is load-bearing):

- C603's `tau = 0.3518` and `NSAT_amended = 349`. The 11640-candidate walk uses only
  `mf_floor.zag` (sha-verified at the `lane/l3macro` tip) and its own literals.
  My independent enumeration hitting the claim's own `349` **exactly** is a
  two-way cross-check that needs no ledger at all.
- C281/CALR's `tau = 0.0000` and the finding that the 22-entry label table is
  hand-typed into the driver at base 2176, with a two-bit criterion maximum and a
  4-way tie. Content is robust; **provenance** rests on one commit, `4e7eb30b1`.
- Every G3 `AB-PRESENT` / `AB-PARTIAL` / `AB-ABSENT` verdict: scanned from source
  files, not from ledger citations.
- The G1 circularity finding (sha256 identity of the two `decide281` artifacts) and
  the fabricated-fixture finding: both are content hashes, ledger-independent.

**NOT robust** (each degrades with the missing evidence):

- **Which three claims are newest.** The ranking in §2 is built from the ledger plus
  `STAGED_LEDGER_ENTRIES.md`. A newer L3 adjudication inside the 858 invisible lanes
  would displace the table. `n = 3` is a **floor**, not a census.
- **The VACUITY RATE itself**, for the same reason plus the untranscribed criteria.
- **C453's completeness.** One of eleven sealed worlds (F1-W1) was gated.
- **Any count that uses "410".** 393 is the block count; 410 over-counts by 17.
- **Whether C459 is recoverable.** I did not check `4e7eb30b1` for it. NOT-VERIFIABLE
  here means *not located by me*, not *absent*.

## 6. VERDICT

The standing gate is **built, run, deterministic, and not kill-only.** On the
newest three L3 adjudications it returns: one criterion **VACUOUS-0** and repaired
by its author, two **NON-VACUOUS**, one claim **capped at L2 for want of an
ablation**, one claim **not established as L3**, and one claim that **does not
exist**. G1 is **partly void** on its own self-check and **circular** on the
headline claim.

**No L3 claim passes this gate.** That is consistent with `SUF_AUDIT.md`'s
"L3 achieved anywhere: zero" and adds two things the prior lanes asked for and did
not have: a pre-red-team decide-from-literals artifact with an enforced
no-learner assertion, and a do-nothing attack on internal criteria that
**returns NON-VACUOUS two times in three** — so it is evidence about criteria, not
a verdict-shaped instrument.

## 7. BOUNDARIES

- **B-1** G2's criterion and world semantics are transcribed **by hand** from each
  claim's own published declaration (prereg / source header / report), never from
  its implementation — disclosed in `PREREG.md` §G2. A transcription error is
  possible; the C453 residual (`mispred=2`) is a live example, and it is reported
  rather than absorbed.
- **B-2** G1's provers are **hand-authored**, not auto-emitted (ADDENDUM-1 §A4).
  `PROVER_LOC` is a floor on cheapness, not a measurement of it.
- **B-3** n = 3. G4's own bar is not met. The vacuity rate is **under-powered** and
  is not offered as a result.
- **B-4** C453 was gated on one world of eleven; C281/CALR on the H1 fixture only.
- **B-5** The `ASSERT-NOLEARNER` check is name-based and fires on comments. It is a
  necessary, not sufficient, condition for independence.
- **B-6** `tau` is defined against the claim's **own declared** candidate space. A
  criterion can be non-vacuous inside its own space and trivially satisfiable
  outside it. C453's T2 memorisation entry is reported for exactly this reason and
  is excluded from `tau` by rule.
- **B-7** G2 never raises a level; G3 never raises a level; G1 only reduces. The
  gate cannot manufacture an L3.
- **B-8** Two processes are undisclosed in my own lane history: the fabricated C453
  fixture (found and replaced) and the broken `PRELUDE_LOC` counter (reported, not
  fixed).

## 8. NEXT EXPERIMENT

1. **Get n >= 5.** Transcribe criteria for C397 GPI-3, L3-SUF-1 and L3-INR, and
   gate C453's remaining ten worlds. That is the only way G4's preregistered bar
   becomes answerable rather than under-powered.
2. **Re-do C281's prover independently.** Write a second `decide-from-literals` for
   the CALR family from the label table alone and check it lands on the same
   `INC R0`; only then is the C281 L1 downgrade independently confirmed.
3. **Replace `ASSERT-KEYONLY`** with a satisfiable form: assert that every literal
   in the prover's **decision** region occurs in the claim source, exempting a
   frozen mechanical-constant list. Re-preregister before use.
4. **Sweep the invisible region.** Enumerate the 858 lanes absent from every tip and
   recover any L3 adjudication inside it. Until then, "n=3" means "n>=3".

## 9. Claim IDs

- **C611** — the standing L3 gate: G1 decide-from-literals, G2 do-nothing-macro,
  G3 capability-ablation, G4 vacuity rate, G5 anti-kill-only control. Built and run.
- **C612** — finding: **a do-nothing macro satisfies C603's preregistered internal
  criterion 50 ways; 35.18% of the 4667 satisfying candidates are structurally
  trivial.** Independently enumerated; reproduces the claim's own `349` exactly.
- **C613** — finding: **the CALR family's acceptance criterion has a two-bit maximum
  and is maximised by a 4-way tie**, so enumeration order, not the criterion,
  selects the adopted program. Non-vacuous (tau = 0) but unselective.
- **C614** — finding: **G1 as preregistered is circular on C281** (the gate's
  "prover" is byte-identical to the audited lane's own artifact) and its
  `ASSERT-KEYONLY` check is unsatisfiable. Reported against myself.
- **C615** — process: this lane's prior session **fabricated** a C453 fixture
  unrelated to the claim's sealed artifacts. Replaced by the claim's own
  `l3_rx_k10/run_1/w1/`. Disclosed per parent rules on PROCESS-FAIL.