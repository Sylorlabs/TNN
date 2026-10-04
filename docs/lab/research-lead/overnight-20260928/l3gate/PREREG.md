# PREREG — C610 "THE L3 STANDING GATE": decide-from-literals, do-nothing-macro, capability-ablation

Worker: L3-GATE. Lane: `lane/l3gate`. Dir: `l3gate/`.
**Committed ALONE, before any gate program exists.** If implementation forces a
change to any threshold in this file, this prereg is void and I must
re-preregister (bar **S-P5**).

## 0. What this lane is

Two completed lanes asked for the same infrastructure and were forced to build it
late, once, for themselves.

- `redteam/suf-audit` (`SUF_AUDIT.md` §5, `L3_CANDIDATE.md` §5): ship a
  **decide-from-literals** program with every L3 claim, run **before** the red
  team convenes. C281's L3 claim died to it in under a page.
- `lane/l3macro` (C603 §9, findings (a) and V1): ship a **do-nothing-macro
  attack** on the internal criterion, because the preregistered internal
  criterion is maximised by a do-nothing macro (V1), and require a
  **capability ablation** rather than an argument (finding (a)).

**I am not testing a hypothesis about a learner. I am building an instrument and
then pointing it at other people's instruments.** My goal is therefore NOT to
make the gate kill claims. A gate that kills everything is as uninformative as
one that passes everything, and §G5 exists to test my own instrument for exactly
that failure.

## 1. The three gates, frozen

### G1 DECIDE-FROM-LITERALS (DL)

**Procedure.** Automatic, per claim, from the claim's primary source bytes only:

1. Pure-Zag byte scanners extract five literal classes:
   - `NMENU` — product of the integer literals that appear as the right-hand
     operand of a `<`/`<=` comparison in a `while(...)` head. This is the size of
     the researcher-written candidate menu.
   - `NBOUND` — count of distinct such bounds.
   - `NKEY` — length of the longest run of consecutive source lines that each
     carry **>= 3 integer arguments** to the *same* function name. Such a run is
     a hand-typed literal table.
   - `NPROBE` — number of integer arguments passed at the single call site of
     the highest-NKEY function (probes into the table).
   - `NLIT` — total integer literals; `NSTR` — total string literals.
2. **EMIT** a standalone prover program `provers/prov_<tag>.zag` from those
   literals plus a FIXED reproduction kernel. Two assertions are evaluated
   in-gate over the emitted bytes and printed:
   - `ASSERT-NOLEARNER` — the emitted bytes contain **zero** occurrences of the
     learner's source file basename.
   - `ASSERT-KEYONLY` — the emitted bytes contain **zero** occurrences of any
     token outside the emitted literal set and the fixed kernel token list.
3. BUILD with pinned `znc --target macos-arm64`; RUN with `zbuild.sh --rep 3`.
   **ASSERT 3/3 byte-identical. ASSERT stdout non-empty.**
4. Outcome: **DL-REPRODUCED** if the prover's structural output equals the
   claim's own reported structural output; **DL-FAILED** otherwise.

**Level reduction (frozen).**
- `DL-REPRODUCED` **and** `NKEY >= 2` **and** `NPROBE >= 2` -> **<= L1**. The
  literals are a transcribed answer key probed at two or more points; the claim
  is an enumeration plus an argmax over it.
- `DL-REPRODUCED` and not that -> **<= L2**.
- `DL-FAILED` -> G1 changes nothing.

**LOC is reported, not barred.** Preregistered reading: emitted prover `LOC <= 80`
is **SMALL** and the reduction stands without further argument; `LOC > 80`
requires the gate to state explicitly why the reproduction is not cheap. The LOC
number itself is a datum, not a threshold in the decision.

### G2 DO-NOTHING-MACRO ATTACK (DN)

**Structurally trivial classes** (fixed before any run):

| Id | Class | Definition |
|---|---|---|
| `T0` | DO-NOTHING | empty body; exit fires at iteration 1 |
| `T1` | IDENTITY | body is a no-op basis instruction (`CPY Rx,Rx`) |
| `T2` | COPY-INPUT | body copies one register to another; no arithmetic |
| `T3` | CONSTANT-OUTPUT | body is `SET1` (constant); independent of input |

**Enumeration.** All candidates in the claim's own enumerable sub-space, taken
from the claim's **own frozen declaration** of `F` (its prereg or its source
header), with the search bound the claim itself used. For each candidate,
evaluate the claim's **internal acceptance criterion** exactly as that criterion
is written in the claim's own text. Count:

- `NSAT` = candidates satisfying the criterion
- `NTRIV` = those in `T0..T3`
- `tau = NTRIV / NSAT`

**Vacuity (frozen).**
- **VACUOUS-0** if `T0` alone satisfies the criterion. Fatal: the criterion
  cannot distinguish doing nothing from doing the claimed thing.
- **VACUOUS** if `tau >= 0.01`.
- **NON-VACUOUS** if `tau < 0.01`.

**Consequence.** VACUOUS-0 or VACUOUS => the claim's
`LEARNER CREATES NEW USEFUL FORM` link is marked **UNSUPPORTED-BY-CRITERION**.
It may still be true; *this criterion does not evidence it.* **G2 never raises
a level.**

**The one manual step, disclosed in advance.** A general predicate cannot be
extracted from source automatically. The **criterion text and the world
semantics** are transcribed by hand from each claim's **own published
declaration** (prereg / source header / report), never from its implementation.
That asymmetry matters and is the reason the transcription cannot be tuned to
favour a kill: a lane's implementation is what one is auditing; its declaration
is what one is entitled to hold it to.

### G3 CAPABILITY-ABLATION GATE (AB)

From `lane/l3macro` C603 §4 finding (a): *load-bearingness and
source-underdetermination are independent axes, and every prior L3 claim argues
enumerability with no capability ablation attached.* Frozen rule:

- `AB-PRESENT` iff the claim's source/report bytes contain a **capability-removal
  marker** (`NOSLOT|NOLOOP|NOWRAP|NOINV|NOMEM|NOSLOTS|ABL|A-`) **and** a
  held-out score keyed to that arm.
- `AB-PARTIAL` iff the marker is found with no keyed held-out score.
- `AB-ABSENT` iff neither.

**Consequence.** `AB-ABSENT` or `AB-PARTIAL` => the claim has **not demonstrated
that the pre-existing form was insufficient**, only asserted it. Level is
therefore **capped at L2**, whatever G1 and G2 say. Argument is not evidence.

### G4 VACUITY RATE, and the test of C603's argument

Over all **gateable** L3 claims located (n stated):
`VACUITY RATE = #{VACUOUS-0 or VACUOUS} / n`.

C603 argues that a high vacuity rate is a **stronger and more actionable result
than another L2**. That argument is preregistered as testable:

- **SUPPORTED** iff `VACUITY RATE >= 0.80` **and** `n >= 5` **and** the claims
  span `>= 3` distinct lanes.
- **NOT SUPPORTED** otherwise, and I then report it as under-powered rather than
  as a result.
- If supported, the finding is a negative result about **instruments**, not about
  learners, and is stated that way.

### G5 POSITIVE CONTROL FOR MY OWN ATTACK (guard against a kill-only gate)

A gate that fails everything is degenerate. Frozen control: re-run G2 on C603's
own world under a criterion that additionally requires `iters >= 2` **and** that
`R0` actually changed. Preregistered expectation: `T0` and `T1` are now
**rejected**, `tau` falls, and the attack returns **NON-VACUOUS**.

If G2 returns VACUOUS on this control too, **G2 is reported DEGENERATE and its
results on the real claims are void.** This is the single most important
self-check in the lane.

### G0 APPLICABILITY

A **gateable L3 claim** = an L3-class claim (asserts or adjudicates L3 novelty of
*form*) with either recoverable primary source or a recoverable ledger
description.

A claim with **no source at any reachable commit** gets outcome
**NOT-VERIFIABLE** — an artifact-provenance failure. It is **not** a scientific
pass and **not** a scientific fail, and it is **excluded from the numerator and
denominator of the VACUITY RATE** (G4) while being counted and named in the
coverage table. This exists so the gate cannot manufacture a verdict out of an
absence.

## 2. Claims in battery, and the selection rule

**Selection rule, frozen:** the *results table* reports the **three newest
L3-class adjudications** in the corpus, ordered by the date recorded in the
canonical ledger or in the lane's own commit, descending. The *vacuity rate*
(G4) uses **every** gateable L3 claim I can locate, including older ones.

Newest three: **C401** (L3-NIV2-WAVE9, 2026-10-03), **C603** (MACRO,
2026-10-03), **C397** (GPI-3, 2026-10-02).

Full battery: C401, C603, C397, C284/C281, C287, C335, L3-SUF-1, L3-RX,
L3-INR (brief's "C459").

## 3. Process bars

| Bar | Requirement |
|---|---|
| P1 | Pure Zag. Every byte of source reading, literal extraction, enumeration and counting is a Zag program using `_zag_read_file`/`_zag_write_file`. Shell/git only for worktrees, `cat` splicing, invoking `zbuild.sh`, `shasum`, `grep`, `cmp`. **No scripting language reads any source file.** |
| P2 | Every gate program: 3/3 byte-identical stdout, non-empty stdout asserted, `_zag_print`/`_zag_println` only, zero `_zag_raw_syscall`. |
| P3 | Explicit pathspecs. Never `git commit -a`. Never `git checkout` in the main repo. Never touch another lane's worktree — other lanes' sources are read by `git show <branch>:<path>` into *this* worktree. |
| P4 | New claim IDs in the **C6xx** block (C5xx is already triple-minted per `SUF_AUDIT.md` §8 P5). |

## 4. Self-falsifiers (stated against my own work)

- **S-P1** G2 returns VACUOUS on the G5 positive control. (Then G2 is void.)
- **S-P2** G1's emitted provers fail their own `ASSERT-NOLEARNER` /
  `ASSERT-KEYONLY` checks. (Then G1 is measuring the wrong thing.)
- **S-P3** Any emitted prover fails 3/3 determinism or produces empty stdout.
- **S-P4** I find myself moving a threshold in §1 after seeing a result.
- **S-P5** I cannot obtain source for a majority of the battery. (Then the
  instrument reports mostly NOT-VERIFIABLE and that is itself the headline.)
- **S-P6** My gate assigns a level to a claim whose source I could not read.