# PREREG-2 (C660) — L3-GATE-2: make the standing gate trustworthy

Lane `lane/l3gate2`. Base: `lane/l3gate` tip `c5922d61d`.
**Committed ALONE, before any gate-2 program exists.** Moving any threshold in
§1 after seeing a result voids this prereg (bar **S2-P4**).

This prereg changes thresholds in `l3gate/PREREG.md` §1. That is *declared
here*, in advance, and the parent prereg's own bar S-P5 requires exactly that: a
new prereg. Every change is a **repair of a defect the parent lane disclosed
against itself**, never a moved bar in the direction that helps a verdict.

---

## 0. What I am fixing, and what I am not

`lane/l3gate` built three instruments and ran them. `lane/redteaw4` returned
**DOWNGRADE**. The parent lane's own report is the best evidence against it, and
this prereg is built out of that report:

| Defect (parent's own words / red team's) | Repair in this prereg |
|---|---|
| **G1 circular on C281**: `prov_c281.zag` byte-identical (sha `98535f37`) to `redteam/suf-audit:.../suf_audit_decide281.zag` — the audited lane's own artifact | §G1: prover must be **hash-disjoint from every file of the audited lane**, verified by a **sha256 implemented in Zag**, and its literals must come from the **claim text**, not the lane's code |
| **`ASSERT-KEYONLY` is unsatisfiable**: fires on 5 and 28 literals that are pure machinery | §G1.3: `ASSERT-KEYONLY-2` restricted to the prover's **DECISION region** with a **frozen MECHANICAL exemption list**, plus a **negative control** that MUST be rejected, so the assertion is shown to have teeth |
| **`ASSERT-NOLEARNER` is name-based** and fires on comments | §G1.2: superseded by the hash-disjointness assertion; retained only as a name check and demoted to **advisory** |
| **`PRELUDE_LOC` returned 0**; LOC was read off the file by hand | §G1.4: LOC is **deleted**. The decision no longer depends on it. Cheapness is reported as a fact, never used as a threshold |
| **n = 3**, below its own bar `n >= 5`; `ASSERT-NOLEARNER`/KEYONLY voided G1; C453's criterion was never transcribed | §G2 gets **three more claims** (C397 GPI-3, L3-SUF-1, L3-INR) per the parent's own §8 next-experiment #1. Battery `n >= 5` |
| **2 of the 3 "L3 claims" were never L3** (C603 self-declares L2, C281 was L1), so the true `n` was 1 | §G0.2 fixes the denominator **by rule, before any result**, with two denominators reported and no silent exclusions |
| **vacuity rate reported as a point estimate 1/3 = 0.333** | §G4: exact **Clopper-Pearson** interval by bignum integer arithmetic, and a pre-declared decision on C603's "high vacuity rate is a stronger result" claim |
| **ledger has 393 blocks and no machine-readable level field** (262/393 assert none; the rest contaminated by lane-name prefixes) | §G6 declares the level-extraction method and its error mode. No automated level extraction is used for any verdict |

**I am not trying to make the gate pass anything.** My goal is that a reader can
falsify it. Every instrument still only lowers or holds a level (§G7).

---

## 1. G1 — DECIDE-FROM-LITERALS, v2

Same idea as the parent: emit a standalone prover that decides a claim's
structural result from **literals only**, with no learner. The **independence
conditions are new and are the point of this prereg.**

### G1.0 The literal classes (parent §G1 step 1, UNCHANGED)

Scanned in pure Zag from the claim's source bytes:
`NMENU`, `NBOUND`, `NKEY`, `NPROBE`, `NLIT`, `NSTR`.

### G1.1 PROVENANCE SPLIT — the substantive new rule

The parent scanned the "claim's primary source bytes" without distinguishing
*implementation* from *declaration*. That conflation produces a **spurious
downgrade**: a prereg is *required* to state exact predicted literals, so
`NKEY` measured over a prereg measures the prereg, not the answer key.

- `SRC` = the claim's **implementation** bytes (learner / driver / macro
  interpreter — the artifact that does the work).
- `DECL` = the claim's **published declaration** bytes (prereg, design doc,
  report, SEALED_KEY, ledger block).

Two new classes:

- **`NKEY-SRC`** — `NKEY` scanned over `SRC` only. **This, not `NKEY`, is the
  quantity the level-reduction rule uses.**
- **`PRED-LIT`** — count of distinct integer literals that appear in `DECL`
  and are also expected in `SRC`'s output, i.e. the size of the *published
  prediction table*. Reported per claim. **Never** used to lower a level.

Rationale, stated so it can be argued with: brief §9's bar is that the novel
form is **not enumerable from source**. A prediction written in a prereg is
enumerable from the *declaration*; every prereg has one; it carries no
information about where the claim's competence comes from.

### G1.2 INDEPENDENCE — enforced, not asserted

For each claim the gate requires **both**, computed by `gate/sha256.zag`
(a from-scratch SHA-256 in Zag, self-checked against `shasum` on 6 vectors):

- **`ASSERT-INDEP-1 (hash-disjoint from the audited lane).`** The prover's
  sha256 must differ from the sha256 of **every** file in the audited lane's
  directory at the commit the lane is read from. Verified by building a lane
  file manifest with `git ls-tree` (git plumbing only), hashing every listed
  blob in Zag, and comparing. **Any collision => `ASSERT-INDEP-1 FAIL` and the
  prover is VOID, not a pass.**
- **`ASSERT-INDEP-2 (provenance).`** Every integer literal in the prover's
  DECISION region must occur in `DECL`'s literal set, and **at least one**
  literal must occur in `DECL` that occurs **nowhere** in `SRC`. An
  answer-key prover necessarily cites literals from the implementation; a
  claim-text prover necessarily cites literals the implementation never sees.
  Both at once is the signature of an independent reproduction.
- **`ASSERT-INDEP-3 (no learner linkage).`** The prover must not call, name, or
  read any path or symbol belonging to the audited lane. Checked mechanically
  on the prover's bytes: zero occurrences of the lane directory name, and zero
  occurrences of any `fn` name defined in the audited lane's `SRC` files.
  (Supersedes `ASSERT-NOLEARNER`, which was name-only and fired on comments.)

### G1.3 `ASSERT-KEYONLY-2` — satisfiable, and shown to be satisfiable

The parent's version asserted *every* literal in the prover occurs in the claim
source. **Unsatisfiable**: any working Zag program carries buffer sizes,
sentinels and ASCII codes. Frozen replacement:

- The check applies **only to the prover's DECISION region**, defined
  mechanically as: all lines after the last line belonging to the mandatory
  output prelude (`fn z_alloc`, `fn o_i64`, `fn o_app`, `fn o_nl`, `fn o_sp`,
  `fn o_flush`), which is excluded wholesale.
- A **frozen MECHANICAL exemption list**, fixed in this file and not amended:
  `0 1 2 3 8 10 13 32 45 48 57 58 95 97 100 255 256 611 8192 65536 1000000`.
  Every entry is an ASCII code, a power of two / buffer size, a sentinel, or
  the lane's own directory length. **Decision content is not exemptible.**
- A literal in the DECISION region is legal iff it occurs in `DECL`'s literal
  set **or** in the exemption list.

**Satisfiability is itself a test, not an assertion (bar S2-P1).** I ship a
**negative control** `prov2/ctl_cheat.zag`: a prover that decides the same
verdict using a magic constant absent from both `DECL` and the exemption list.
Frozen requirement:

- `ASSERT-KEYONLY-2` **PASS** on every real prover, **and**
- `ASSERT-KEYONLY-2` **FAIL** on `ctl_cheat.zag`, and
- **`ASSERT-INDEP-*` FAIL** on `ctl_cheat.zag`'s magic constant (it is not in
  `DECL`, which is exactly why KEYONLY-2 rejects it).

If KEYONLY-2 passes the cheat prover, the assertion is vacuous and **G1 is
reported VOID**. An unsatisfiable assertion that always passes is worse than no
assertion; so is a satisfiable one that always passes.

### G1.4 LOC is DELETED as a threshold

The parent's `PRELUDE_LOC` counter was broken and the LOC figure was read off
the file by hand. LOC is now **reported as a fact and used nowhere**. The
parent's "SMALL / requires justification" clause is **withdrawn**, not repaired.

### G1.5 Level reduction (frozen; the parent's rule with `NKEY` -> `NKEY-SRC`)

- `DL-REPRODUCED` **and** `NKEY-SRC >= 2` **and** `NPROBE >= 2` -> **<= L1**.
- `DL-REPRODUCED` and not that -> **<= L2**.
- `DL-FAILED` -> G1 changes nothing.
- **VOID** if any of `ASSERT-INDEP-1/2/3` fails, or if `ASSERT-KEYONLY-2` does
  not behave as §G1.3 requires. VOID is not a pass.

`DL-REPRODUCED` = the prover's structural output equals the claim's **own
published** structural constant (read from `DECL`, never from a log file).

---

## 2. G2 — DO-NOTHING-MACRO, v2

### G2.0 Trivial classes (UNCHANGED, parent's `T0..T3`)

`T0` do-nothing, `T1` identity (`CPY Rx,Rx`), `T2` copy-input, `T3` constant
output. Enumeration is over **the claim's own declared space `F`** at **the
claim's own bound**, and the criterion is the claim's **own published internal
acceptance criterion** (`DECL`).

### G2.1 DECISION RULE REFINED — removes the enumeration dependency

The parent's `tau = NTRIV / NSAT` needs `NSAT`, i.e. full enumeration of `F`.
For four of six claims `F` is larger than any enumeration I can afford, and the
parent already hit this on C453 (`NSAT=0` from a transcription gap) and then
**declined to return a verdict**. Frozen replacement, strictly sharper:

- **`NON-VACUOUS`** iff `NTRIV = 0`. No enumeration of `F` is needed: zero
  trivial candidates satisfies the criterion. This is an exact decision.
- **`VACUOUS-0`** if `T0` alone satisfies the criterion.
- **`VACUOUS`** iff `NTRIV / NSAT_LO >= 0.01`, where `NSAT_LO` is a **certified
  lower bound** on the satisfying candidates. `NSAT_LO >= 1` always, because
  the claim asserts its own adopted candidate satisfies its own criterion.
- **`VACUOUS-U`** (upper bound) iff `NTRIV >= 1` but `NSAT` was not fully
  enumerated: report `tau <= NTRIV / NSAT_LO`.
- **`INCONCLUSIVE`** only if `NSAT_LO = 0`, which means the claim does not even
  assert its own candidate satisfies its own criterion. That would be a
  reporting defect in the claim, and it is reported as such.

**Why this is sharper, not looser.** `tau` as the parent defined it silently
depends on an unproven enumeration. `NTRIV = 0 => tau = 0` holds for **any**
`NSAT`, so the NON-VACUOUS verdict needs no census. The VACUOUS verdict needs a
*lower* bound on `NSAT`, which is a strictly easier thing to certify than an
exact count.

### G2.2 CONJUNCTION-SHAPE AUDIT (new, and the reason the rate may be low)

The parent's rate conflates two criterion shapes:

- **`SHAPE-ARGMAX`** — one numeric criterion maximised over an enumeration
  (C603, C281/CALR). Trivial candidates can reach the top.
- **`SHAPE-CONJ`** — a conjunction of several independent bars (C453, C397,
  L3-SUF-1, L3-INR). A trivial candidate must satisfy every bar, so it must
  satisfy a bar that pins a literal it cannot know.

Frozen: for `SHAPE-CONJ` claims I additionally report **`tau-bar`**, the
fraction of the constituent bars that each trivial candidate satisfies on its
own. The headline `tau` remains the conjunction-level `tau`. A conjunction can
score `tau = 0` while individual bars are vacuous, and that must be visible.

### G2.3 The one manual step, restated and narrowed

The criterion text and world semantics are transcribed **by hand** from `DECL`
(prereg / design / report / SEALED_KEY / ledger block), **never from the
implementation**. Every transcription is committed as
`TRANSCRIPTIONS.md` with, per claim, the **verbatim quoted span** it came from,
so a reader can check the transcription without reading any code. Each
transcription gets a **cross-check number** it must reproduce from the claim's
own report (e.g. C281 must reproduce `MAX_SCORE = 2`; L3-INR must reproduce
`HELD 4/6`). A transcription that fails its own cross-check is VOID.

---

## 3. G3 — CAPABILITY-ABLATION (UNCHANGED rule, extended scan)

- `AB-PRESENT` iff `SRC`+`DECL` bytes contain a capability-removal marker
  (`NOSLOT|NOLOOP|NOWRAP|NOINV|NOMEM|NOSLOTS|ABL|A-|WIPE|ABLATE`) **and** a
  held-out score keyed to that arm.
- `AB-PARTIAL` iff marker without a keyed held-out score. `AB-ABSENT` iff
  neither. `AB-ABSENT`/`AB-PARTIAL` caps the claim at **L2**.

---

## 4. G4 — VACUITY RATE with an exact Clopper-Pearson interval

Frozen, and fixed here **before** any result:

- **Primary denominator `D1` = L3-ENGAGING claims** that pass G0. A claim is
  L3-engaging iff its own text **adjudicates the L3 bar at all** — asserts L3,
  denies L3, or caps itself at L3. Every such claim that reached a published
  criterion gets its criterion attacked.
  *Why:* the gate tests whether criteria **used to adjudicate L3** are
  vacuous. A claim that *denied* L3 still used a criterion to do so, and if that
  criterion is vacuous the denial is equally unfounded. Silently excluding
  denials is what produced the parent's `n = 3`.
- **Secondary denominator `D2` = L3-ASSERTING claims** (those whose own text
  asserts L3 novelty). Reported in full, never used alone.
- `RATE = #{VACUOUS-0 or VACUOUS} / D`. Both `D1` and `D2` rates are reported.
- **Interval:** exact two-sided **Clopper-Pearson** at 95%, computed in pure
  Zag with **bignum integers** (no floating point exists in Zag) by exact
  binomial-tail inversion over a `10^-12` rational grid. No normal
  approximation, no Wilson substitution. Sanity-checked against the parent's
  stated `P(X<=1 | n=3, p=0.80) = 0.1040`.
- **NOT-VERIFIABLE** claims are excluded from both numerators and denominators
  and **named in a coverage table** (parent §G0, retained).

**C603's claim, preregistered as testable again.** *A high vacuity rate is a
stronger, more actionable result than another L2.*

- **SUPPORTED** iff `RATE_D1 >= 0.80` **and** `D1 >= 5` **and** `>= 3` distinct
  lanes **and** the 95% CP **lower** bound is `>= 0.80**.
- **NOT SUPPORTED** in every other case, reported as **under-powered**, not as
  a refutation. A low rate with a CP upper bound below 0.80 **is** a refutation
  of the claim, and I will say so if the interval licenses it.
- If supported, it is a negative result about **instruments**, not learners, and
  is stated that way.

**Denominator honesty rule.** No claim enters or leaves `D1`/`D2` after this
commit. A claim that turns out not to be gateable is recorded as
NOT-VERIFIABLE with the reason, and the count is reported before and after.

---

## 5. G0 APPLICABILITY (UNCHANGED) + G0.2 gateability

G0: gateable = an L3-engaging claim with recoverable primary source **or**
recoverable ledger description. No source at any reachable commit =>
**NOT-VERIFIABLE**, excluded from numerators and denominators, named.

**G0.2 reachability is measured at BOTH tips** required by the mission: the
**restored tip** (`lane/restores` `d64053cbe`, which `lane/reaudit` measured as
a strict superset of the pre-wipe tree `4e7eb30b1`) **and** `4e7eb30b1` itself,
because the parent found C281-lineage fixtures resolve **only** at `4e7eb30b1`.
A path that resolves at neither is absent; a path that resolves at only one is
**invisible**, and the claim's verdict is reported as being about that commit.

---

## 6. LEVEL EXTRACTION — method and error mode, declared up front

`lane/reaudit` established: the canonical ledger is **393** blocks (not 410;
C143-C159 are appendix sub-bullets), and **has no machine-readable level
field** — 262/393 assert none, and the rest are contaminated by lane-name
prefixes (`L3-NIV2-WAVE9`, `L3-RX-BUILD`, `L2-INTERFERENCE-D3` are claim
*names*, not level assertions).

**Frozen method. No automated level extraction is used for any verdict.**

1. A Zag scanner extracts, per block, the set of **candidate** level tokens
   (`L0`,`L1`,`L2`,`L2+`,`L3`) with the surrounding 40 bytes of context, and
   reports counts. This is a **candidate generator, not a classifier.**
2. A level is assigned to a claim only by **reading the block**, and the
   **verbatim quoted span** that assigns it is recorded in `LEVELS.md` per
   claim. **No level is ever assigned from the scanner output alone.**
3. Where the quoted span is the claim's **name** and the block contains no
   other level token, the claim's level is recorded as **`L-UNSET`**, and the
   claim is treated as L3-engaging by **name** with an explicit flag
   **`NAME-ONLY`**. `NAME-ONLY` is reported, never silently upgraded to an
   assertion.

**Declared error modes, all of which are real:**

- **E-LEVEL-1 UNDER-DETECTION.** 262/393 blocks assert no level. A claim that
  silently carries a level in prose without a token is counted as `L-UNSET`.
  Bias direction: **toward under-detecting levels**, i.e. toward over-counting
  the battery as `L-UNSET` rather than inventing levels.
- **E-LEVEL-2 NAME CONTAMINATION.** `L3-NIV2` is a name. Treating it as an
  assertion would manufacture L3 claims. This is why §6.3 exists; the error is
  named, not fixed by hope.
- **E-LEVEL-3 CONFLICT.** A block may assert a level and bound it (`"L2+, L3 not
  claimed"`). The rule is: **the highest level asserted as an achievement
  wins**, and the bounding sentence is quoted alongside. Under this rule C397 is
  `L2` with an explicit `L3-DENIED`, and C459 is `L2+` with `L3-KILLED`.
- **E-LEVEL-4 The whole exercise is advisory.** Levels are recorded for
  *reporting* only. No verdict in this lane turns on a level field except the
  parent's frozen G1/G3 reduction rules, which use **the gate's own after-level
  vs the claim's own after-level**, both of which are quoted spans.

---

## 7. No instrument raises a level

G1 lowers or holds. G2 lowers or holds. G3 **caps** at L2. None of them can
produce an L3. The gate cannot manufacture a level, only remove one.

---

## 8. Process bars

| Bar | Requirement |
|---|---|
| **S2-P1** | `ASSERT-KEYONLY-2` passes every real prover **and fails** `ctl_cheat.zag`. Else G1 VOID. |
| **S2-P2** | `ASSERT-INDEP-1` FAILs on the parent's known-circular `prov_c281.zag` (sha `98535f37` must be found in the audited lane). **A negative control for the negative control:** the hash check must demonstrably *detect* a known collision. |
| **S2-P3** | `sha256.zag` self-check matches `shasum -a 256` on 6 vectors (empty, "abc", 1 byte, 55/56/64-byte boundary, 1000 bytes). |
| **S2-P4** | No threshold in §1-§6 moved after a result. Any move voids this prereg. |
| **S2-P5** | Pure Zag for all extraction, enumeration, hashing, interval arithmetic and counting. Shell/git only for worktrees, `git ls-tree`/`git show` into this worktree, `cat` splicing, `zbuild.sh`, `shasum` (used **only** to cross-check `sha256.zag`, never to compute a verdict), `cmp`, the watchdog. **No scripting language reads any source file.** |
| **S2-P6** | Every run behind `tnnwatch.sh`. 3/3 byte-identical stdout, non-empty stdout asserted. |
| **S2-P7** | Explicit pathspecs. Never `git commit -a`. Never `git checkout` in the main repo. Never touch another lane's worktree. |
| **S2-P8** | Claim IDs **C6xx**, never minting into `CLAIM_LEDGER.md`. |

---

## 9. Self-falsifiers, stated against my own work

- **S2-F1** The hash check never fires on the known-circular prover => the
  independence machinery is decorative.
- **S2-F2** `ASSERT-KEYONLY-2` passes the cheat prover => G1 VOID.
- **S2-F3** Any transcription fails its own cross-check number => that claim's
  G2 verdict is VOID and is reported VOID.
- **S2-F4** The Clopper-Pearson implementation disagrees with the parent's
  `P(X<=1|n=3,p=0.80)=0.1040` => the interval machinery is wrong and no interval
  is reported.
- **S2-F5** I find a claim enters `D1` only after I saw its verdict.
- **S2-F6** The sweep finds a pre-wipe lane dir absent at the restored tip =>
  `lane/reaudit`'s "0 absent" is wrong and I say so.
- **S2-F7** G1's `NKEY-SRC` fires on a claim whose literals live only in its
  prereg => the provenance split is wrong and I retract the downgrade.