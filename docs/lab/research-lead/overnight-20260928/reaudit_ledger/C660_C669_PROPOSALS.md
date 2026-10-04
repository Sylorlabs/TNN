# C660-C669: LEDGER PROPOSALS — NOT MINTED, LEDGER NOT MODIFIED

**Lane:** `lane/reaudit`. Source of record: `lane/restores` `d64053cbe` and
`lane/recovery` `9b2c4db6e`, both independently re-verified here.
**Mint guard honoured.** `canonical_ledger/CLAIM_LEDGER.md` was not touched. These
are proposals, C5xx-block and up, for the ledger owner to accept or reject.

Read `TNN_CANONICAL_STATE.md` first. This file is only the actionable list.

---

## C660 — CORRECT C653: the 1,610 / 1,601 / 1,351 lane counts are a counting ARTEFACT

`lane/restores` recorded "lane dirs 259 -> 1,610" and stated that
`lane/recovery` "undercounted by 493 lane dirs."

**Both figures are wrong, and the correction runs backwards.**
`git ls-tree -r -t --name-only` at depth 5 on that prefix emits lane
**directories** *and* **493 loose evidence files sitting in the lane root**
(`ADV_MEM3_EVIDENCE.txt`, `BRIDGE_FIX_BA6B_RAW.txt`, `BRIDGE_FIX_RESULT.md`, …).
Splitting on `/` and taking field 5 conflates the two.

Measured as tree objects only (`mode 040000`, depth 5):

| | lane dirs | loose root files |
|---|---|---|
| pre-wipe `4e7eb30b1` | **1,108** | 493 |
| post-wipe `b3b3ee00a` | 251 | 0 |
| tip `d64053cbe` | **1,117** | 493 |

**`lane/recovery`'s 1,108 was correct.** Its 1,601 pre-wipe figure and the
1,610 tip figure are the same contamination. The 493 is not an undercount of
lanes; it is a count of files.

**Proposed action:** record the lane-directory count as **1,117** and the
lane-invisibility count as **0**. Do not carry 1,610 or 1,351 into any ledger
text.

## C661 — RECORD the restore as verified, with the numbers this lane measured

**Basis, independent of `lane/restores`:**

| Measure | Value |
|---|---|
| `9d5c7f940` deletions | **0** (160,514 files, 44,104,409 insertions, all status `A`) |
| tracked paths pre-wipe -> tip | 165,288 -> **165,804** |
| pre-wipe paths absent at tip | **0** (tip is a strict superset, +516) |
| pre-wipe lane dirs absent at tip | **0** |
| `isa.zag` blob / `impl/` tree at `4e7eb30b1` and at tip | `4a4b1cf8…` / `14597682…` — **identical both sides** |

**Proposed action:** record `b3b3ee00a` as a **visibility** event with **zero
content loss**, and record the restore as **complete and exact**.

## C662 — RECORD the tripwire as tested, not merely installed

`lane/restores` reported the guard installed. This lane **executed** it against
a real index:

| staged deletions | result |
|---|---|
| 1,200 | **REFUSED** — `git commit` non-zero, no commit created, HEAD unchanged |
| 1,000 | ALLOWED |
| 1,001 | REFUSED |
| 1,001 with `--no-verify` | ALLOWED (documented bypass) |

Vendor selftest 13/13. The hook lives in the shared git dir and
`core.hooksPath` is unset, so it is live for all 28 worktrees.

**Proposed action:** record invariant **D1 MASS-DELETION**, threshold
`> 1000 paths`, **validated in both directions** (refuses above, permits below).

## C663 — THE 113 UNciteable CLAIMS: re-label UNVERIFIED — NO COMMITTED PROVENANCE

**This supersedes nothing; it records the negative result with its full search.**

The 113 `SHA-UNRESOLVABLE` claims cite **446 citation instances** to **252
distinct abbreviations**. Searched exhaustively:

- all 6,763 commit objects incl. unreachable and dangling — 0 of 252
- **all 132,987 objects of any type — 0 of 252.** Not merely unreachable:
  **never present in this object database**
- all refs, all 512 reflog entries, `fsck --unreachable` (44) — 0
- `.recovery/unreachable31.bundle` (33 commits) — 0; contents already inside the DB
- **128 other git repos on this host (49,111 objects) — 1 apparent hit**
- two unfetched `origin` branches (`refs/heads/main` `27a4271f2`, 381 commits;
  `refs/heads/reorg/phase-0-1` `9914322267`, 338 commits) — **fetched, then
  re-searched — 0 of 252**

**The single cross-repo "hit" is a forgery trap and must be refused.**
`abed8aa1` prefix-matches `abed8aa170ef…` in `/Users/Shared/micah/Documents/zag`,
a **different project**, dated 2026-08-22, subject *"chore: install one-shot
import visibility repair"*. The 21 TNN claims citing it (C97…C408) date from
September–October 2026. It is an **8-hex (32-bit) abbreviation collision across
unrelated repositories.**

**Proposed action:** relabel the 113 as **UNVERIFIED — NO COMMITTED PROVENANCE**.
Six cite **zero** resolvable shas and are the most exposed: **C364, C368, C378,
C383, C391, C401**. Their BUILD-PASS / INTEGRATED-BUILD-PASS /
INSTRUMENT-DISCRIMINATES-A verdicts are **not citable**.

**Proposed action, negative:** record that citation rewriting was attempted and
**yields nothing**, and that the one available cross-repo match is a collision.
**Do not rewrite any of the 252.** Doing so fabricates provenance.

## C664 — CALR AXIS 1: mechanism level L2+ -> **L1**. All 14 claims. **CLOSED.**

```
C294 C312 C324 C334 C348 C350 C358 C364 C367 C368 C378 C383 C391 C401
```

**Basis is EXECUTION, not the source's own comment.**
`isa.zag` (blob `4a4b1cf8…`, sha256 `409ee8f4…9911`) was loaded unmodified and run:

| measurement | result |
|---|---|
| accepted opcode set (scan op = −1…8) | **exactly {0,1,2,3,4}**, count 5 |
| op0 CPY, R0=7 Rs=5 | **5** |
| op1 ADD | **12** |
| op2 MUL | **35** |
| op3 SET1 | **1** |
| op4 INC | **8** |
| op −1 / 5 / 200 | **all rejected** — alphabet cannot be silently widened |
| Rd=4 / Rs=4 | **rejected** — 4 registers, R0..R3 |
| stateless (repeat match) | **yes** |
| determinism | **3/3 byte-identical**, sha256 `449d83a3…51c2` |

Semantics are identical to the committed C281-line interpreter
`xdomain_grammar_l2m/glm_learner.zag::m_exec`. **ZERO new opcodes, ZERO new
semantic cases** is therefore **TRUE**, and verified rather than asserted.

Brief §9: "brute-force search over a fixed DSL" is explicitly **not L3**.

**Proposed action:** record this axis as **CLOSED**. It is the first downgrade in
this program justified by a measurement rather than by reading the claimant's
hedging.

## C665 — CALR AXIS 2: evidentiary status -> UNVERIFIED. 9 claims, TWO SUB-CLASSES.

`lane/restores` C651 bundled these. They must be separated — the evidence is
different in kind, and C350's is stronger than its own lane count implies.

**2a — cited lane never existed in any repo on this host (8 claims).**
`C358 C364 C367 C368 C378 C383 C391 C401`

Lanes `l3_niv2_2scalr_survival`, `l3_novel_intermediate_v2_wave5`,
`l3_niv2_pool_repair`, `l3_niv2_w6_thirdstage`, `l3_niv2_genrec_integration`,
`l3_niv2_w7_yield`, `l3_niv2_w8_instr`, `l3_niv2_w9_ppcost`: **0 commits, 0
files, absent from every tree in the object database.** Cited branches
(`lane-l3niv2w5-20261002`, `lane-hcontlife5-20261002`, `lane-compinteg2-20261002`)
exist as no ref; their worktrees were under `~/workspace/`, absent from this host.

**2b — citations resolve; the result was self-declared uncommitted (1 claim).**
**`C350`.**

**`lane/restores` placed C350 in 2a for the wrong reason.** It argued C350's
"implementation is missing even though its lane has commits." The cleaner ground
is that **C350's own ledger entry concedes it**:

> *"Blocker at report time: disk full (No space left on device on git add, even
> single files); prereg IS committed (d5f767bd1); implementation and REPORT.md
> written but uncommitted pending disk recovery … Status: COMPLETE
> (implementation commit pending)."*

In this lane's re-audit **C350 is EVIDENCE-INTACT**: 4 shas cited, 4 resolve,
0 absent, lane present. So the honest statement is: **C350's citations are fine;
C350's result is uncitable because the result was never committed.** That is the
same class as **C373**, the ledger's one NO-CITATION claim — a self-declared
absence, which the audit was right to flag in C373 and wrong not to extend to
C350.

**Proposed action:** relabel 2a as **UNVERIFIED — LANE NEVER EXISTED** and 2b as
**UNVERIFIED — RESULT NEVER COMMITTED (self-declared)**.

## C666 — DOWNGRADE proposal WITHDRAWN as unsound: no numeric L-distribution

A level triage (`level_triage.zag`, 393 blocks detected exactly: 142 `## C<n>.`
+ 251 `- C<n> (`) **cannot** yield an L0/L1/L2/L2+/L3 distribution from this
ledger:

- **262 of 393 blocks (66%) assert no level token at all** in their body.
- The 131 that do are contaminated by lane- and claim-name prefixes
  (`L3-NIV2`, `L2-INTERFERENCE-D`, `L3-REDTEAM`).
- A detector-artefact figure of "73 unbounded L3" is emitted by the program and is
  **explicitly not a finding**: it is the noise floor of a 14-phrase substring
  list against 675KB of prose. Publishing it would fabricate an L3 count.

**What IS verified:** block count 393 is exact, and **L3 achieved = zero** — the
ledger contains **no positive L3-achievement claim** (all 3 occurrences of
"L3 achieved" are negative: "anywhere: zero", "still zero"), and every
L3-adjacent claim carries an explicit researcher-bounding admission.

**Proposed action:** **record the governance defect, not a distribution.** The
ledger records level in prose, so level is **re-assertable but not auditable** —
which is how C281/C284 held as L3 and CALR held as L2+ for as long as it did.
**Proposed remedy: make `level:` a field on every claim block.** Until then, no
worker should publish an L-distribution.

## C667 — RECORD the re-audit's central negative result: the visibility failure is CLOSED

The 393-claim evidence audit, re-run at the restored tip with resolution
**independent of the original** (every abbreviation prefix-matched in pure Zag
against the complete commit set from `git cat-file --batch-all-objects`, which
includes unreachable and dangling objects):

| verdict | @ post-wipe HEAD | **@ restored tip** |
|---|---|---|
| EVIDENCE-INTACT | 163 (41.5%) | **279 (71.0%)** |
| LANE-GONE | 116 (29.5%) | **0** |
| SHA-UNRESOLVABLE | 113 (28.8%) | 113 (28.8%) |
| NO-CITATION | 1 | 1 |
| **union degraded** | 228 (58.0%) | **114 (29.0%)** |

Transitions, all 393 aligned: 163 INTACT->INTACT, **116 LANE-GONE->INTACT**,
113 SHA-UNRES->SHA-UNRES, 1 NOCIT->NOCIT. **Nothing moved but upward.**

**Invariance check:** audit columns `id`, `nshort`, `nok`, `nabs`, `nlanes` are
**byte-identical across all 393 rows** (`diff` clean). Only `nlanes_gone`
(301 -> 0) and `verdict` moved. This is the strongest available evidence that
the restore changed *visibility only*.

**One contract correction, recorded because it changes the denominator.**
`cites2.tsv` carries **every** maximal hex run in the block prose, so its
`H<hex>:<len>` tokens include **68 sha256 file digests (len 64)**, 3 full 40-char
shas, and 12 other lengths. `lane/recovery` counted only len 8/9/10 — the
abbreviated *commit* ids. Unfiltered, the count inflates to 1,260, absent rises
to 526, and **NO-CITATION silently drops to 0**. Filtered, it reproduces 1,177
exactly. Any future audit of this ledger must apply the len 8/9/10 filter.

**Proposed action:** record the visibility failure as **CLOSED** — 0 pre-wipe
lane directories absent at tip, 9 new, 0 of 1,116 indexed lanes absent — and
record that the false negative that produced the "CALR has no source" error was
a **visibility** artifact, never a data-loss event.

## C668 — NOTE that no "charter 89" exists

The instruction to report "what is currently running (charter 89)" cannot be
executed as stated: **no charter 89 document exists in this repository.** Tracked
charter documents are `R32_E51_PROGRAM_CHARTER.md`, `R33_PROGRAM_CHARTER.md`,
and two wave-2 `C181_C188` charters.

Measured state at 2026-10-04 09:13 PDT: **zero live TNN-lane processes**;
`tnnwatch.sh` reports `(none)`; three registry rows read `RUNNING`
(`N6_r1`, `y_k10b`, `y_k10d`) with long-past start timestamps and are **stale
rows, not processes** (confirmed against `ps`); **no orphan Zag binaries**.
Foreign load, not ours: `qemu-system-x86_64` 183%, iOS Simulator
`STExtractionService` 127%.

**Proposed action:** if a charter 89 exists outside this repository, supply it.
Otherwise record that **the research program is idle** and that the next
experiment should be a science experiment rather than a seventh audit.

## C669 — STANDING RULE: never cite an abbreviation by cross-repo prefix match

`abed8aa1` exists in `/Users/Shared/micah/Documents/zag`, a different project,
and is cited by 21 TNN claims. It is an 8-hex (32-bit) collision. It is the only
cross-repo match among 49,111 objects in 128 repos, and it is exactly the shape of
a plausible-looking "recovery".

**Proposed action, permanent:** a cited abbreviation may be resolved **only**
against a repository that the citing lane actually named. A cross-repository
prefix match is **not** a recovery and must never enter the ledger. Minimum
citation length for an unpublished commit: **12 hex (48 bits)**, and a full
40-char sha is preferable.

---

*No ledger byte written. No claim minted by this lane. No history rewritten.
Pure Zag for all computation; `tnn_pure_zag_report` -> `PURE-ZAG-CLEAN`.*