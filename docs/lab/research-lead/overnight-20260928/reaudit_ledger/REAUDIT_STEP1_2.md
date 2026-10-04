# LEDGER-REAUDIT — STEP 1+2: restore verification and the 393-claim re-audit

**Lane:** `lane/reaudit`. Base: `lane/restores` tip `d64053cbe`.
**Nature of this lane:** falsification. `lane/restores` executed a restore and
reported success. This lane assumes the report is wrong until independently
measured, and its central claim is the report's own: *"the 116 LANE-GONE
verdicts retire."*

Two of the report's headline numbers did not survive. One did. Details below.

---

## PART 1 — IS THE RESTORE REAL?

All figures below are from `git` plumbing run in this worktree against
`d64053cbe`, not from any prior lane's report.

### 1.1 The restore commit is a pure append

`9d5c7f940` ("P3-RESTORE: re-materialise 160,514 paths"):

| Measure | Value |
|---|---|
| files changed | 160,514 |
| insertions | 44,104,409 |
| **deletions** | **0** |
| status letters | `A` x160,514 — zero `M`, zero `D` |

### 1.2 No tracked file was lost relative to the pre-wipe state

Set comparison, `git ls-tree -r --name-only`, pre-wipe `4e7eb30b1` vs tip:

| | paths |
|---|---|
| pre-wipe `4e7eb30b1` | 165,288 |
| post-wipe `b3b3ee00a` | 4,775 |
| **tip `d64053cbe`** | **165,804** |
| in pre-wipe but **absent** at tip | **0** |
| at tip but not in pre-wipe | 516 |

**Zero loss.** The tip is a strict superset of the pre-wipe tree by 516 paths
(ledger appends, proposals, hook sources created since).

### 1.3 Cited source files are present and readable

Section 7 frozen cores, on disk in this worktree:

| Path | readable | bytes |
|---|---|---|
| `cogops_learnosc2/c8_learn.zag` | yes | 37,404 |
| `cogops_rescueaware/c15_base.zag` | yes | 5,174 |
| `hook_phase1/hq_module.zag` | yes | 9,701 |
| `compression_exec/tnn2_frozen_ref.zag` | yes | 56,508 |
| `cogops_learnosc2/c8_full.zag` | yes | 75,215 |
| `l3_suf_intermediate/src/` | yes | dir |

---

## PART 2 — THE TRIPWIRE, TESTED RATHER THAN TRUSTED

Installed at `<git-common-dir>/hooks/pre-commit`, which is
`TNN/.git/hooks/pre-commit` — shared by every worktree, and `core.hooksPath`
is unset, so it is genuinely active for all of them. The hook execs
`TNN/.git/mass_delete_guard/mass_delete_guard.sh`, which computes the count in
**pure Zag** (`mass_delete_guard.zag`) and **fails closed** if the Zag binary
cannot be built or the verdict is unrecognised.

Vendor selftest (`--selftest`): 13/13 PASS — 5,000-path deletion REFUSED,
999-path ACCEPTED, all four historical wipes (`b3b3ee00a` 160,515;
`c721bcc61` 160,361; `f461e812d` 147,296; `169894404` 165,250) REFUSED by sha,
all five real repairs ACCEPTED at 0 deletions.

**Independent end-to-end test in this worktree** (real index, real `git commit`):

| staged deletions | result |
|---|---|
| 1,200 | **REFUSED** — `git commit` exited non-zero, no commit created, HEAD unchanged |
| 1,000 | ALLOWED (commit created) |
| 1,001 | **REFUSED** |
| 1,001 with `--no-verify` | ALLOWED — the documented bypass works |

Threshold is exactly ">1000". It is not a blanket ban, and it does not obstruct
any real repair, because every real repair in this repo's history adds paths.

---

## PART 3 — THE HEADLINE NUMBER THAT DID NOT SURVIVE

`lane/restores` reports *"lane dirs 259 -> 1,610"* and *"the audit undercounted
by 493 lane dirs; `ls-tree -r -t` gives 1,601 / 1,351, not 1,108 / 858."*

**Both of those figures are counting artefacts, and the correction is
backwards.** `git ls-tree -r -t --name-only` on that prefix emits, at the same
depth, two different kinds of entry: lane *directories* and **493 loose
evidence files sitting directly in the lane root** (`ADV_MEM3_EVIDENCE.txt`,
`BRIDGE_FIX_BA6B_RAW.txt`, `PUSH_SUMMARY*`, …). Splitting the output on `/` and
taking field 5 lumps them together. That is where 493 comes from, and 493 is
exactly the "undercount" that was attributed to `lane/recovery`.

Measured properly — tree objects only, `mode 040000`, depth 5:

| | lane dirs | loose root files | lanes holding >=1 file |
|---|---|---|---|
| pre-wipe `4e7eb30b1` | **1,108** | 493 | — |
| post-wipe `b3b3ee00a` | 251 | 0 | — |
| **tip `d64053cbe`** | **1,117** | 493 | 1,610 |

**`lane/recovery`'s 1,108 was correct.** The audit did not undercount; it counted
lane directories. The restores lane's own `1,601` pre-wipe figure is the same
1,108-plus-493 contamination, and its "1,610 lane dirs" is the correct 1,117
lane dirs plus the same 493 files.

**Set difference, the question that actually matters:**

```
pre-wipe lane directories absent at the restored tip:  0
new lane directories at tip not in pre-wipe:            9
```

---

## PART 4 — THE 393-CLAIM EVIDENCE AUDIT, RE-RUN

Method is deliberately independent of the original's stage 2. That stage trusted
a precomputed `abbrev -> OK|ABSENT` table (`sha_res.tsv`, 887 rows). Here every
cited abbreviation is prefix-matched in pure Zag directly against the **complete**
commit set of the object database — 6,763 commit objects, from
`git cat-file --batch-all-objects --batch-check`, which includes unreachable and
dangling objects, not only ref-reachable ones. No resolution is inherited.

One correction to the extractor contract was required and is worth recording:
`cites2.tsv` carries **every** maximal hex run in the block prose, so its `H<hex>:<len>`
tokens include 68 sha256 file digests (len 64), 3 full 40-char shas, and 12 other
lengths. `lane/recovery` counted only len 8/9/10 — the abbreviated *commit* ids.
Counting all 1,260 token instances instead of the 1,177 commit citations inflates
`nshort`, inflates the absent count, and silently drops `NO-CITATION` to 0.
`reaudit_join.zag` filters on the emitted `<len>` field and reproduces 1,177.

### Distribution

| Verdict | `lane/recovery` @ post-wipe HEAD | **`lane/reaudit` @ restored tip** |
|---|---|---|
| EVIDENCE-INTACT | 163 (41.5%) | **279 (71.0%)** |
| LANE-GONE (recoverable) | 116 (29.5%) | **0** |
| SHA-UNRESOLVABLE | 113 (28.8%) | **113 (28.8%)** |
| NO-CITATION | 1 | **1** |
| **Total** | 393 | 393 |
| **Union degraded** | 228 (58.0%) | **114 (29.0%)** |

### Transitions — all 393 claims, aligned row by row

| from | to | n |
|---|---|---|
| EVIDENCE-INTACT | EVIDENCE-INTACT | 163 |
| **LANE-GONE** | **EVIDENCE-INTACT** | **116** |
| SHA-UNRESOLVABLE | SHA-UNRESOLVABLE | 113 |
| NO-CITATION | NO-CITATION | 1 |

Not one claim moved in either direction except the 116 LANE-GONE retiring upward.
Zero false upgrades: no SHA-UNRESOLVABLE claim became citable.

### Invariance check

Columns 1-5 of the two audits — `id`, `nshort`, `nok`, `nabs`, `nlanes` — are
**byte-identical** across all 393 rows (`diff` clean). Only `nlanes_gone` and
`verdict` moved: 301 lane mentions gone -> **0**; 197 claims with >=1 gone lane -> **0**.

### Aggregate citation counts

| Quantity | `lane/recovery` | `lane/reaudit` |
|---|---|---|
| abbreviated commit shas cited (instances) | 1,177 | 1,177 |
| - resolved | 731 | 731 |
| - **absent from the object DB** | **446** | **446** |
| lane mentions in blocks | 310 | 310 |
| **mentions naming an absent lane** | **301** | **0** |

### THE NEW LIST OF GENUINELY MISSING EVIDENCE

114 claims, and only two failure modes remain:

**113 x SHA-UNRESOLVABLE** — every one cites at least one abbreviated commit id
that is in no object database on this host. 252 distinct abbreviations, 446
citation instances. Full list in `reaudit_degraded.tsv`.

**1 x NO-CITATION — C373** (`XP-HIER-3`). Unchanged, and still not a defect:
C373 self-declares *"PREREG.md frozen (sha256 …) but FLAWED, no commits made"*
and returns `VOID — prereg design flaw`. It is the one claim in the ledger that
correctly records that it has no committed evidence.

**Zero LANE-GONE. Zero invisible lanes. Zero recoverable-but-missing lanes.**
The 116 LANE-GONE verdicts are retired, and the retirement is real.

---

## WHAT THIS LANE DID *NOT* DO

- Did not write a single byte to `canonical_ledger/CLAIM_LEDGER.md`.
- Did not mint a claim ID. New IDs go in a PROPOSALS file as `C5xx+`.
- Did not amend, rebase, force-push, or touch another lane's worktree.
- Did not run a non-Zag interpreter. `tnn_pure_zag_report` -> `PURE-ZAG-CLEAN`.
- Did not check any sha256 digest against file content, and did not verify any
  digest, determinism claim, or PASS/FAIL bar. This is citation resolvability
  only. It is not claim truth.