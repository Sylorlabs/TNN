# TNN CANONICAL STATE — as of 2026-10-04, measured at `lane/restores` tip `d64053cbe`

**Authority of this document.** It is a *measurement report*, not a ledger entry.
It writes no claim ID and modifies no ledger byte. Every number below was
produced in this lane (`lane/reaudit`, commit `76712ed8c` + this commit) by `git`
plumbing or by pure Zag, and is reproducible from the commands stated. Where the
ledger cannot be measured, this document says so instead of estimating.

---

## 1. WHAT TNN IS

TNN is a research program building a learning machine in a language it also
builds. Its unit of work is a **lane** — a self-contained experiment directory
with a preregistration, a frozen kill bar, an implementation in pure Zag, and a
report — whose results are then minted into a single append-only ledger,
`docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md`
(675,018 bytes, **393 claim blocks**, C1–C410 with 17 IDs absent).

The ledger is the program's memory. The program's credibility rests entirely on
whether a claim's cited evidence can be resolved. That is why the three events
of the last two days — a mass deletion, a restore, and an audit — are the most
important results the program has produced, and not any of its experiments.

## 2. WHAT IS DEMONSTRATED

| Fact | How it is known |
|---|---|
| **The corpus is reproducible on this host.** `cogops_learnosc2/c8_full.zag` (340KB flat arena) rebuilt and run gives byte-identical output to the Linux-x86-64 canonical log after one substitution (`_zag_raw_syscall` -> `_zag_print`). | brief §4.1; B13 RESOLVED |
| **`_zag_raw_syscall` is inert on darwin/arm64.** It returns rc=0 and emits nothing. Not an error — silence. Any lane whose only output path is `o_flush` produces an empty log and reports success. | brief §4.0 |
| **The 160,514-path wipe is fully reversed. Zero tracked paths lost.** 165,288 (pre-wipe) -> 4,775 (post-wipe) -> 165,804 (tip). The tip is a strict superset of the pre-wipe tree by 516 paths. | `comm -23` of the two path sets is **empty** |
| **No lane is invisible at tip.** 0 of the 1,108 pre-wipe lane directories are absent from the restored tip; 9 are new. | tree objects only, mode `040000` |
| **The mass-deletion invariant is now mechanical.** A real 1,200-path staged deletion was REFUSED by `git commit`, no commit created, HEAD unchanged. 1,000 ALLOWED, 1,001 REFUSED. | end-to-end test, not the vendor selftest |
| **Citation evidence: 279 of 393 claims (71.0%) are now intact**, up from 163. | `reaudit_join.zag`, 393 rows |
| **The CALR ISA has exactly 5 opcodes and adds nothing.** Executed, not read: accepted opcode set is precisely `{0,1,2,3,4}`; semantics are CPY=5, ADD=12, MUL=35, SET1=1, INC=8 on R0=7, Rs=5; `-1`, `5`, `200`, `Rd=4`, `Rs=4` all rejected; stateless; 3/3 byte-identical. | `calr_isa_probe.zag`, sha256 `449d83a3…51c2` |
| **`l3_niv2_pool_repair` and 7 sibling lanes never existed in this repository.** 0 commits, 0 files, never in any tree in the object database. | `git log --all` + `cat-file --batch-all-objects` |
| **L3 achieved: zero.** The ledger contains no positive L3-achievement claim. The only occurrences of "L3 achieved" are negative ("anywhere: zero", "still zero"). | `level_triage.zag`, 3 occurrences, all negative |

## 3. WHAT IS KILLED

| Claim(s) | Disposition | Why |
|---|---|---|
| **B13** (corpus not reproducible on this host) | **RESOLVED / OVERSTATED** | byte-identical rebuild |
| **B16** (silent miscompilation of indexed reads) | **DOUBTED** | 340KB flat-arena program runs byte-exact; likely a broken output path or a bad harness |
| **C281 / C284** (L3 novelty) | **L1** | selection over researcher-written operators |
| **C285** | **killed C284** | creation was "MENU SELECTION over 5 ops" |
| **C459** | **reclassified L2+** | "L3-KILLED", incomplete-disambiguation trap |
| **C287, C397, C335** | **bounded, not L3** | schema researcher-enumerated; WRAP/SEQUENCE are frozen templates; criterion form researcher-authored |
| **B1** node-id/frame-slot namespace collision | **LIVE, correctness not speed** | makes 5k/10k MAP scaling *incorrect* |
| **B2** global O(N) scans | **LIVE** | N=28 takes 75–92s vs 0.3s predicted |
| **B3** old GEN arena hard-dimensioned for 4 MAPs | **LIVE** | nm=5–7 silently wrong, nm=8 panic |
| **B6** interpreter scratch overflow at program length 7 | **LIVE, one-line fix** | genuine source-level stack overflow |
| **B7** eviction tie-break | **LIVE** | cannot hold 6 sequential new facts |
| **B12** frozen TNN-1 | **LIVE** | no world-driver interface |
| **8 CALR lanes** | **UNVERIFIABLE, not false** | never existed in any repo on this host |
| **113 ledger claims** | **UNciteable** | cite 446 citation instances to 252 abbreviations in no object database anywhere on this host |

## 4. WHAT IS PROVISIONAL

| Item | Status |
|---|---|
| **`SHA-UNRESOLVABLE` (113 claims) as an evidence verdict** | Sound *about this host*. It does **not** establish the commits never existed. |
| **CALR family level = L1 (14 claims)** | **Verified empirically.** This is the strongest downgrade in the ledger. |
| **CALR evidentiary status = UNVERIFIED (9 claims)** | Verified for 8 (lanes absent). C350 is different in kind — see §5. |
| **B16** | Doubts recorded, not resolved. Re-verify before building on it. |
| **sha256 digests** | 64 cited file digests were **never checked against file content** by any audit to date. |
| **Determinism bars** | `--rep 3` byte-identity is asserted in claim prose. Not re-verified for the corpus at scale by this lane. |

## 5. THE TWO CALR AXES ARE NOT THE SAME AXIS — AND C350 SITS ON ONLY ONE

`lane/restores` bundled these into one 14-claim list. They must be separated,
because the evidence for them is different in kind.

**Axis 1 — mechanism level -> L1. All 14. VERIFIED BY EXECUTION.**
`isa.zag` (blob `4a4b1cf8…`, sha256 `409ee8f4…9911`, `impl/` tree `14597682…`
byte-identical at `4e7eb30b1` and at tip) accepts exactly `{0,1,2,3,4}` and
rejects everything else, so its alphabet **cannot be silently widened**. Its five
semantics are identical to `xdomain_grammar_l2m/glm_learner.zag::m_exec`, the
committed C281-line interpreter. A beam/argmax search over an enumerated pool of
a DSL whose source declares zero added semantics is a fixed-DSL brute-force
search, which brief §9 explicitly classes as **not L3**. This axis is closed and
should be recorded as closed.

**Axis 2 — evidentiary status -> UNVERIFIED. 9 claims, but two sub-classes.**

| Sub-class | Claims | Evidence |
|---|---|---|
| cited lane never existed | C358, C364, C367, C368, C378, C383, C391, C401 | 0 commits, 0 files, absent from every tree in the object DB |
| citations resolve, implementation self-declared uncommitted | **C350** | all 4 cited shas resolve; lane holds 2 doc files and no code |

**C350 is not in the same condition as the other eight, and `lane/restores`
placed it there for the wrong reason.** It argued C350's "implementation is
missing even though its lane has commits". The stronger and cleaner ground is
that **C350's own ledger text concedes it**: *"Blocker at report time: disk full
… implementation and REPORT.md written but uncommitted pending disk recovery …
Status: COMPLETE (implementation commit pending)."* C350 is a self-declared
absence in the same class as **C373**, the ledger's one NO-CITATION claim, and
the audit's correct instinct in flagging C373 applies to C350 as well.

C350 is nevertheless `EVIDENCE-INTACT` on citation resolvability in this lane's
re-audit (4 shas cited, 4 resolve, 0 absent, lane present). So the honest
statement is: **C350's citations are fine; C350's result is uncitable because
the result was never committed.** That is a stronger downgrade than the other
eight and should be recorded in its own words, not folded into a count.

### FINAL DOWNGRADE PROPOSAL (clean, and it supersedes C650/C651)

```
AXIS 1 -- MECHANISM LEVEL: L2+  ->  L1        (14 claims)
  C294  C312  C324  C334  C348  C350  C358  C364  C367  C368  C378  C383  C391  C401
  Basis: EXECUTED. accepted opcode set == {0,1,2,3,4}, all out-of-range rejected,
  semantics == glm_learner.zag m_exec. Zero new opcodes, zero new semantic cases.
  Brief s9 bar: fixed-DSL brute force is explicitly not L3. CLOSED.

AXIS 2 -- EVIDENTIARY STATUS: COMPLETE/BUILD-PASS  ->  UNVERIFIED   (9 claims)
  2a cited lane never existed in any repo on this host   (8)
     C358 C364 C367 C368 C378 C383 C391 C401
  2b citations resolve; result self-declared uncommitted  (1)
     C350   -- "Status: COMPLETE (implementation commit pending)", its own words
```

C350 is the only CALR-family claim whose citations fully resolve. It is also the
only one whose ledger entry states on its face that the evidence was never
committed. Those two facts together are a cleaner argument than any lane count.

## 6. THE 252 ABSENT COMMITS: PERMANENTLY UNciteable ON THIS HOST

Exhaustively searched, in order, with the object DB growing at each step:

| Venue | Result |
|---|---|
| All 6,763 commit objects incl. unreachable + dangling (`cat-file --batch-all-objects`) | 0 of 252 |
| **All 132,987 objects of ANY type** (not just commits) | **0 of 252** — they are not merely unreachable, they were never here |
| Reflogs (512 entries), all 118 refs, `fsck --unreachable` (44 unreachable) | 0 |
| The one bundle on host, `.recovery/unreachable31.bundle` (33 commits) | 0 — its contents are already inside the object DB |
| **128 other git repos on this host (49,111 objects)** | **1 apparent hit — and it is a collision** |
| Two Sylorlabs repos (`PrismStudio`, `zag`) | 1 apparent hit (below) |
| **Two `origin` branches never fetched locally**: `refs/heads/main` (`27a4271f2`, 381 commits) and `refs/heads/reorg/phase-0-1` (`9914322267`, 338 commits) — **fetched, then re-searched** | **0 of 252** |

**The single cross-repo "hit" is `abed8aa1`, and it is a forgery trap.**
It prefix-matches `abed8aa170ef1bc33e5aca68b99fcdd905a4545f` in
`/Users/Shared/micah/Documents/zag`, a **different project**: dated
2026-08-22, subject *"chore: install one-shot import visibility repair"*. The 21
TNN claims citing `abed8aa1` (C97…C408) date from September–October 2026. This
is an **8-hex (32-bit) abbreviation collision across two unrelated repositories.**
Importing it would be precisely the provenance fabrication that
`lane/restores` correctly refused to perform by rewriting citations. It must
stay refused.

**Conclusion: 252/252 are permanently unciteable on this host.** The
re-audit was re-run against the enlarged database (6,771 commit objects, up from
6,763 after the two fetches) and returned **identical** results: 1,177 citations,
731 resolved, 446 absent, 279/0/113/1. Nothing moved.

**Plainly: 113 ledger claims are permanently unciteable.** Their stated
provenance cannot be checked, ever, from anything on this machine. Their content
may well be true; it is not checkable, and the honest label is UNVERIFIED, not
FALSE.

**Which claims.** The 113 are the `SHA-UNRESOLVABLE` set of the re-audit, listed
with per-claim absent counts in `reaudit_ledger/reaudit_degraded.tsv`. Six of
them cite **zero** resolvable shas and are the most exposed: **C364, C368, C378,
C383, C391, C401** (absent 5, 5, 8, 7, 6, 3 respectively). Their BUILD-PASS /
INTEGRATED-BUILD-PASS / INSTRUMENT-DISCRIMINATES-A verdicts are not citable.
Plus **C373**, the one NO-CITATION claim, which is an honest self-declared
absence and not a defect.

## 7. THE LEDGER HAS NO MACHINE-READABLE LEVEL FIELD — and that is the finding

`level_triage.zag` was written to publish an L0/L1/L2/L2+/L3 distribution. It
is reported here as a **negative result about the ledger's shape**, because the
distribution cannot be honestly extracted:

- Block detection is **exact**: 142 `## C<n>.` + 251 `- C<n> (` = **393**.
- **262 of 393 blocks (66%) assert no level token at all** in their body.
- Of the 131 that do, the tokens are contaminated by lane- and claim-name
  prefixes (`L3-NIV2`, `L2-INTERFERENCE-D`, `L3-REDTEAM`). Restricting to the
  block body and excluding `L<n>-<UPPER>` name forms still leaves 81 blocks
  whose "L3" token cannot be distinguished from a lane name by any rule short of
  reading each one by hand.
- A detector-artefact figure of "73 unbounded L3" is emitted by the program and
  is **explicitly not a finding**. It is the noise floor of a 14-phrase substring
  list against 675KB of prose, and publishing it would be a fabricated L3 count —
  the exact error class this exercise exists to prevent.

**Therefore no numeric L-distribution is published here.** What *is* verified:
**L3 achieved = zero**, because the ledger contains no positive L3-achievement
claim (all 3 occurrences of "L3 achieved" are negative), and every L3-adjacent
claim carries an explicit researcher-bounding admission.

**This is a governance defect, and it is fixable.** The ledger records level in
prose. It should record it as a field. Until it does, level is **re-assertable
but not auditable** — which is precisely how C281/C284 survived as L3 and how
CALR survived as L2+ for as long as it did.

## 8. THE REMAINING INVISIBILITY QUESTION — ANSWERED

`lane/l3gate` reported that C281-lineage fixtures "resolve ONLY at `4e7eb30b1` —
invisible, not absent." That is now historical, not current.

```
lane directories, tree objects only, mode 040000, depth 5
  pre-wipe  4e7eb30b1 : 1108
  post-wipe b3b3ee00a:  251
  tip      d64053cbe : 1117
  pre-wipe lane directories absent at tip        :   0
  new lane directories at tip not in pre-wipe    :   9
  indexed lanes (1116) absent at tip             :   0
```

**No lane is invisible at the tip. The invisibility event is fully resolved.**

**One correction, because it was published as a finding and it is wrong.**
`lane/restores` reported *"lane dirs 259 -> 1,610"* and *"the audit undercounted
by 493 lane dirs."* `git ls-tree -r -t --name-only` at depth 5 emits lane
**directories** *and* **493 loose evidence files sitting directly in the lane
root** (`ADV_MEM3_EVIDENCE.txt`, `BRIDGE_FIX_BA6B_RAW.txt`, …). Splitting on `/`
and taking field 5 conflates them; that is where 493 comes from, and 493 is
exactly the "undercount" wrongly attributed to `lane/recovery`. **The audit's
1,108 was correct.** Its `1,601` pre-wipe figure is the same contamination, and
its `1,610` tip figure is the correct 1,117 lane dirs plus the same 493 files.

## 9. BIGGEST ARCHITECTURAL BLOCKERS, RANKED BY WHAT THEY COST

1. **The ledger is prose, not data.** 66% of claims carry no machine-readable
   level; 113 claims carry citations that resolve nowhere; sha256 digests have
   never been checked. Every governance failure in the last two days traces to
   this one. Until claims are structured records, every future audit is another
   hand-rolled substring matcher, and the next mass deletion or invented
   provenance will be caught by luck rather than by a check.
2. **B1 — node-id / frame-slot namespace collision.** `res_op` reads `op>=10000`
   as a frame slot; trial literals are node ids. This makes 5k/10k MAP scaling
   **incorrect, not merely slow**. Highest severity on this list, because it is a
   silent-wrong-answer class.
3. **B2 — global O(N) scans dominate.** N=28 takes 75–92s against a 0.3s
   prediction; N=100 incomplete after 7 minutes. Superlinear O(N²) MAP attempts
   x O(NE) scans. This is what blocks scale, and it is structural, not a tuning
   problem.
4. **B3 — old GEN arena hard-dimensioned for 4 MAPs.** nm=5–7 silently wrong,
   nm=8 panic. A silent-wrong-answer class. Superseded by GEN-REDIM
   (C429/C434), which needs its own verification that it is actually adopted.
5. **B6 — interpreter scratch overflow at program length 7.** `z_alloc(64)` too
   small; needs 128. One line, genuine source-level stack overflow. **Cheapest
   real fix on this list.**
6. **B7 — eviction tie-break cannot hold 6 sequential new facts.** (C75.)
7. **B12 — frozen TNN-1 has no world-driver interface.** (C141.) Blocks
   composition with any external world.
8. **B16 — suspected silent miscompilation of indexed reads.** **Doubted, not
   resolved.** Do not build architecture on it. Re-verify first; §4.1 is strong
   evidence it is an artifact.

## 10. WHAT IS CURRENTLY RUNNING

Checked live at 2026-10-04 09:13 PDT via `tnnwatch.sh status` and `ps`:

- **Live TNN-lane processes: none.** `tnnwatch.sh` reports `(none)`.
- The watchdog registry shows 3 rows in state `RUNNING` — `N6_r1`, `y_k10b`,
  `y_k10d` — all with start timestamps far in the past. These are **stale
  registry rows, not running processes**, confirmed against `ps`. No orphan Zag
  binaries with `ppid=1` exist.
- **No "charter 89" document exists in this repository.** Searched all tracked
  files for charter numbering; the only charter documents are
  `R32_E51_PROGRAM_CHARTER.md`, `R33_PROGRAM_CHARTER.md`, and two wave-2
  `C181_C188` charters. *This document therefore reports measured process state
  and does not attribute anything to a charter 89 that cannot be located.*
- Foreign load dominates and is not ours: `qemu-system-x86_64` 183%,
  iOS Simulator `STExtractionService` 127%, `./m4` 76%, `./e11b` 62%. Per brief
  §10.2 the machine is shared; assume a fraction of a core.
- **The research program is idle.** No lane is executing. The last three lanes to
  finish (`recovery`, `tcdefects`, `restores`) were all audits or repairs. The
  next experiment should be a science experiment, not another audit.

## 11. IMMEDIATE CONSEQUENCES

- **MINT NOTHING.** 113 claims should be relabelled UNVERIFIED - NO COMMITTED
  PROVENANCE, and 8 CALR claims UNVERIFIED - LANE NEVER EXISTED. C350 should be
  relabelled in its own words. None of this should be done by editing claim text
  in place; the mint guard enforces pure-append, so it goes in as new blocks.
- **Publish the CALR L1 downgrade as CLOSED**, backed by execution, not by a
  comment in `isa.zag`. The distinction matters: it is the first downgrade in this
  program justified by a measurement rather than by reading the claimant's
  hedging.
- **Fix B6.** One line. It is the only blocker on this list with no open
  scientific question attached.
- **Make level a field.** Until a claim carries `level:` as data, the L3 question
  cannot be audited, only re-litigated.
- **Do not rewrite the 252 citations.** `lane/restores` reached the right
  conclusion by measurement (a `git cat-file` sweep yields nothing) and this lane
  confirms it. Rewriting them to nearby commits would fabricate provenance.
  `abed8aa1` in the `zag` repository is exactly that fabrication, pre-loaded and
  waiting for someone to be helpful.

---

*Produced by `lane/reaudit`. Read-only with respect to `CLAIM_LEDGER.md`. No
claim minted. Pure Zag for all computation; `tnn_pure_zag_report` ->
`PURE-ZAG-CLEAN`. No history rewritten.*
---

## 12. LEDGER-INTEGRATION AMENDMENT 2026-10-04 (commit 52b94023d)

The canonical ledger now ends at C864. 65 blocks appended (C800-C839
science, C840-C859 downgrades, C860-C864 governance), 260 lines, zero
deletions, mint guard PASS `(ins=260 del=0, pure-append verified)`.

Corrections to sections above:

- **B6 is CLOSED**, not merely documented. The bound is `12L - 8`
  bytes, tight to the byte over 12.7 million programs. The
  documented `z_alloc(128)` fix is REJECTED: 128 is magic, wrong at
  L=12, and caps the ceiling at L<=11. The real fix is
  `z_alloc(12*qlen-8)`, cost zero, no ceiling. On this host B6 is
  silent heap corruption because the compiler emits no slice bounds
  checks, not a panic.
- **B16 is CLOSED**, an API trap. `get32` and `set32` take byte
  offsets; the suspected indexed-read miscompilation is an artifact of
  the inert `_zag_raw_syscall` output path or the reporter's harness.
- **B17 is REAL but has ZERO blast radius in the corpus**: 736 SAFE,
  8 SUSPECT, 5 CORRUPT sites in 4 files, all reproducers. No claim is
  invalidated.
- **B13 RESOLVED**: byte-identical reproduction,
  sha256 ae0ae3bf...e4ae7, 3344 bytes.
- **B1 CLOSED**: namespace invariant backed across the constant
  space, 0 collisions for disjoint encoding vs 21 for legacy.
- **CALR axis 1 is CLOSED**: L2+ downgraded to L1 for all 14 claims,
  verified by execution, opcode set exactly {0,1,2,3,4}.
- **C459, C453, C603 are NOT in the canonical ledger**; they appear
  only as citations on lane branches.
- **L3 achieved anywhere: ZERO.** Standing verdict.
- **Battery sensitivity: 0 of 8 defects detected**, interval
  [0.00, 0.3694]. The standing battery's green checks are trustworthy
  as "unchanged", never as correctness evidence.
- **The 44-million-line wipe is characterised**: 160517 paths,
  44104446 deletions, ZERO content lost, 33 unreachable refs rescued
  0 citations.
- **C377 to C466 remain CONTESTED and were never minted** by any lane;
  zero governance incident. The adjacent hazard (33 lanes, 121 of 168
  IDs colliding across C5xx) is real and is documented in C861/C862.

Allocation: C800-C839 science (40 experiments), C840-C859 downgrades,
C860-C864 governance, C865-C869 reserved, C870-C899 headroom. Old
IDs do not resolve to an experiment without a commit hash; see
`ledgerint/COLLISION_ALLOCATION.md`.

What is still open: the level-field proposal (add `level:` as data,
do not regex-backfill), the 252 unciteable citations, the 8 lost CALR
lanes, B2/B3/B7/B12, the eviction policy discriminator, the trial
graph leak, scaling past 20k, and any true-novice arm (impossible in
the current frozen core because `compose_iter` has no read-only path).

What TNN currently is, in one sentence: a pure-Zag interpreter with a
byte-reproducible frozen core, whose learned indexes are
correctness-neutral-or-harmful on every tested frozen core, whose
battery cannot see injected defects, and whose ledger is now appended
through a mechanical pure-append guard.
