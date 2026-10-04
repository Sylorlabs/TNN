# EVIDENCE-RECOVERY: FINDINGS

**Lane:** `lane/recovery`. **Dir:** `evidence_recovery/`. **Date:** 2026-10-03/04.
**Claim IDs proposed:** C600 range is TAKEN by `redteam/suf-audit` (`ce2dd1be9`). This
lane therefore proposes **C640-C649**. See `C640_PROPOSALS.md`. No canonical ledger
byte was written; `canonical_ledger/CLAIM_LEDGER.md` is untouched and still pure-append
ending at C410.

**Scope:** read-only forensics plus one provenance restore. No experiment was run, no
digest was re-verified, no audited mechanism was re-executed. History was not rewritten.

**Relationship to `ce2dd1be9` (C600/C601/C602, lane `l3macro`).** That audit found the
b3b3ee00a wipe and the CALR recovery. I independently re-derived both and **confirm
them**, with two factual corrections and a large extension (the full 393-claim ledger
evidence audit, plus four sibling wipes it did not enumerate).

---

## 1. THE b3b3ee00a WIPE: FULLY CHARACTERISED

### 1.1 The measurement (CONFIRMED, independently re-derived)

```
b3b3ee00a47e6be1c80e54bb00500e5450d75317
parent 4e7eb30b107b9a04ccf5f0f4bacc37f821718df0
author tnn-rsi-loop <rsi-loop@localhost>   Sat Oct 3 20:43:45 2026 +0000
subject "lm3_lifetime: prereg (PREREG.md + NAMECHECK.md); frozen kill bars B1-B7
         before implementation. Non-ledger."

160517 paths touched | 234 insertions | 44,104,446 deletions
diff-filter=A = 2 files (PREREG.md 178 lines, NAMECHECK.md 56 lines)
diff-filter=M = 0 files
diff-filter=D = 160,515 files
15,024 of the deleted files are binary (numstat "-")
```

234 insertions is exactly `PREREG.md`(178) + `NAMECHECK.md`(56). The commit contains
no science; it carries a 44.1-million-line deletion on a subject line that reads as a
routine preregistration.

### 1.2 Which top-level paths

| Deleted paths | Top-level area |
|---|---|
| 160,230 | `docs/` |
| 107 | `src/` |
| 60 | `archive/` (incl. `run-archives/*.tar.gz`, `transfer-staging/*.tar.xz`) |
| 58 | `.github/` (incl. all `scripts/e51aa_*.py`) |
| 14 | `imagination/` |
| 14 | `artifacts/` |
| 13 | `video-repro/` |
| 8 | `video-combine/` |
| 2 | `units/` |
| 3 | `run1.err`, `run2.err`, `run3.err` |
| 1 each | `README.md`, `LOOP_STATE.md`, `LICENSE`, `err.txt`, `data/`, `.gitignore` |

Largest sub-trees removed: `docs/lab/rsi` (35,395), `docs/generations/R33` (32,484),
`docs/lab/senses` (14,447), `docs/lab/research-lead` (13,389), `docs/lab/wave9`
(12,381), `docs/lab/knowledge` (12,138), `docs/lab/deliberation_depth` (7,491).

**Nothing was targeted.** The 4,775 surviving paths are 100% under
`docs/lab/research-lead` - the one subtree the author was working in. The signature is
a `git add -A`/`git commit -a` from a working tree whose index had been reset, i.e. the
author's whole checkout was swept except the directory they were standing in.

### 1.3 What is genuinely LOST versus still present: **NOTHING IS LOST**

This is the load-bearing correction to the framing of the incident.

| Test | Result |
|---|---|
| Paths in parent `4e7eb30b1` | 165,288 |
| Paths in `b3b3ee00a` | 4,775 |
| Deleted paths present in parent | 160,515 / 160,515 = **100%** |
| Is `4e7eb30b1` reachable from `origin/tnn-native-lab`? | **YES** |
| Unreachable/dangling objects matching the wipe | none needed |

`b3b3ee00a` is a **tree-state corruption, not a data-loss event.** Every byte it
deleted is present in its own parent, which is an ancestor of every branch and is on
the origin remote. A restore is `git checkout 4e7eb30b1 -- <path>`; no blob was ever
unlinked. `git fsck --lost-found --unreachable` reports 33 unreachable commits + 255
blobs + 252 trees, but **none of them is needed to undo this wipe and none of them
matches any ledger citation** (see 4.2).

### 1.4 The damage that IS real: the corpus is invisible

| Metric | at `4e7eb30b1` | at `lane/recovery` HEAD | delta |
|---|---|---|---|
| tracked paths | 165,288 | 5,276 | **-96.8%** |
| research lanes under `overnight-20260928/` | 1,108 | 258 | **-858 lanes (-77.4%)** |

Every current branch tip carries the shrunken tree. The 858 absent lanes are present
at `4e7eb30b1` and are therefore recoverable. **This is the mechanism by which the
earlier audit produced its false negative**: `SUF_AUDIT.md` searched the tree at HEAD
and at `cef8c4095` and concluded "the CALR family has no source in the repository."
The statement was true of the tree it searched and false of the repository. Any audit
that searches HEAD rather than history will return false negatives at the same scale.

### 1.5 Why this one was missed when two siblings were caught

| Time (UTC) | Commit | Files deleted | Caught by |
|---|---|---|---|
| 2026-10-03 04:21 | `c721bcc61` | 160,361 | `b688fa031` "GIT-REPAIR2: restore 160348 files deleted by c721bcc61 (WATCHDOG mass deletion)" |
| 2026-10-02 07:19 | `f461e812d` | 147,295 | `84727be29` LANE-AUDIT, then `3c25ff8f1` "completes f461e812d mass-deletion repair", plus per-lane self-restores `7e4d7cffe`, `3b61e5e57` |
| 2026-10-03 19:38 | `169894404` | 165,250 (empty-tree) | `cef8c4095` "REPAIR: restore full tree nuked by 169894404 (empty-tree commit)" |
| **2026-10-03 20:43** | **`b3b3ee00a`** | **160,515** | **nothing** |

Four reasons, in order of importance:

1. **Detection was social, not instrumental.** All three caught events were caught
   because a human or agent noticed a missing file while looking for something else and
   wrote a commit whose subject *names the offending sha*. There is no tripwire. A mass
   deletion is invisible in `git log --oneline`; it is visible only in
   `git show --numstat`. Nobody read the numstat.
2. **The subject line actively camouflaged it.** The caught siblings had subjects
   containing "WATCHDOG", "nuked", "mass deletion". `b3b3ee00a`'s subject is
   `lm3_lifetime: prereg ... Non-ledger` - and the `Non-ledger` suffix, a house
   convention meaning "do not look at the ledger for this one", discouraged exactly the
   check that would have caught it.
3. **The shrunken tree looked normal to the author.** The author's next 20+ commits are
   all `prereg` / `implementation + REPORT` from `tnn-rsi-loop`, all confined to the one
   surviving subtree. Working inside `docs/lab/research-lead/overnight-20260928/`
   nothing appears to be wrong.
4. **No repair was even attempted, so no repair was requested.** Because no commit
   followed it that needed a restored path, the corruption never surfaced as a build
   or test failure.

---

## 2. CALR / l3_niv2 RECOVERY AND THE L1 VERDICT

### 2.1 Recovery performed

`recovered/l3_novel_intermediate_v2/` now holds 27 files restored byte-for-byte from
`4e7eb30b1` (all 11 `.zag` sources, 7 `.md` documents, `battery.sh`, both compile logs,
all 5 dev keys). `RECOVERY_MANIFEST.txt` section A carries the sha256 of every restored
file; section B records the git blob SHA1 and byte length of the 17.1 MB of run logs
and binaries that were not duplicated. Nothing was edited, regenerated, or re-derived.

`impl/isa.zag` blob at `4e7eb30b1` = `4a4b1cf80ddae710fba38b65da4d4e19fb8f964e`,
80 lines, 2,440 bytes.

### 2.2 The alphabet claim: CONFIRMED, with one factual correction

`isa.zag:1-13`, verbatim:

```
// isa.zag -- frozen generic ISA for L3-NIV2.
// Basis (frozen, recorded at code freeze): the C281-line 5-op register
// ISA already present in the learner lineage:
//   0=CPY (Rd=Rs), 1=ADD (Rd+=Rs), 2=MUL (Rd*=Rs),
//   3=SET1 (Rd=1), 4=INC (Rd+=1).
// Registers R0..R3 (i32). R0 preloaded with input x. Output is R0.
// Instruction = 3 bytes (op,d,s). Program = flat instruction sequence,
// max 64 instructions (192 bytes); the cap is a resource bound, never
// binding on the battery (required solutions are length 3 to 6).
// ZERO new opcodes, ZERO new semantic cases. Execution semantics are
// ported exactly from the committed
// xdomain_grammar_l2m/glm_learner.zag m_exec
```

**Correction to the task premise.** The alphabet is not "C281's 80 instructions." It is
**C281's 5 opcodes**, over 4 destination registers x 4 source registers = **80
instruction forms**, with `ZERO new opcodes` and `ZERO new semantic cases` stated in the
source. The 80 is a product, not an alphabet size. The conclusion is unchanged and in
fact sharper: the emittable form set is a **fixed, finite, enumerable 80-element DSL**
with a hard 64-instruction length cap.

The search over it, independently verified:

| Location | Content |
|---|---|
| `impl/lm_cons.zag:79` | `if(pn>=32768){ return -1; }` - candidate pool cap 32,768 |
| `impl/lm_cons.zag:243` | `// gen_appends: generate all 80 append children` |
| `impl/lm_cons.zag:269` | `// gen_substs: 80 substitute-last children` |
| `impl/lm_cons2.zag:185` | `select_beam` |

### 2.3 Verdict: L1, and the bar it fails

Brief section 9: *"an L3 claim is only credible if the NOVEL FORM ITSELF is not
enumerable from source"* and *"brute-force search over a fixed DSL"* is explicitly not
L3. CALR is a beam/argmax search over an enumerated pool of a 5-opcode DSL that the
source itself declares to be inherited unchanged from C281, scored by a
researcher-written objective with a lexicographic tie-break. It fails the bar on the
source's own testimony.

**Therefore C350, C358, C364, C367, C391 are DOWNGRADED from L2+ to L1.** Recorded as a
proposal in `C640_PROPOSALS.md`; the canonical ledger was not modified.

### 2.4 EXTENSION: eight CALR-family lanes were never committed at all

The L3-NIV2 / CALR family is **14 claims**, not 5: C294, C312, C324, C334, C348, C350,
C358, C364, C367, C368, C378, C383, C391, C401. Of these, **eight lanes have zero
commits touching them anywhere in the repository, across all 65 refs**:

```
l3_niv2_2scalr_survival        l3_novel_intermediate_v2_wave5
l3_niv2_pool_repair            l3_niv2_w6_thirdstage
l3_niv2_genrec_integration     l3_niv2_w7_yield
                               l3_niv2_w8_instr
                               l3_niv2_w9_ppcost
```

`git log --all -- <lane>` returns nothing for each. The branches their ledger entries
cite (`lane-l3niv2w5-20261002`, `lane-hcontlife5-20261002`,
`lane-compinteg2-20261002`) **do not exist as refs**. Their worktrees were under
`~/workspace/`, which **does not exist on this host**.

`l3_niv2_calr_redteam` (C350) has exactly **2** committed files, `PREREG.md` and
`NAMECHECK.md`. Its own ledger entry states the rest was never committed: *"Blocker at
report time: disk full ... prereg IS committed (d5f767bd1); implementation and
REPORT.md written but uncommitted pending disk recovery."* The C350 red-team
implementation, its `attacks/` sources and its 12 run logs are **genuinely lost**.

So: the **engine** (`l3_novel_intermediate_v2`, 43 files) is recoverable. The **wave-5
through wave-9 and red-team evidence** is not recoverable by any means.

---

## 3. LEDGER EVIDENCE AUDIT (all 393 canonical claim blocks)

Method and full table: `LEDGER_EVIDENCE_AUDIT.md`; machine output `evidence_audit.tsv`.

| Verdict | Claims |
|---|---|
| EVIDENCE-INTACT (cited shas resolve, cited lanes at HEAD) | 163 |
| LANE-GONE (shas resolve, >=1 named lane absent at HEAD - **recoverable**) | 116 |
| SHA-UNRESOLVABLE (>=1 cited abbreviated commit sha absent from object DB) | 113 |
| NO-CITATION | 1 (C373, an honest `VOID` entry that declares "no commits made") |
| **Total** | **393** |

Union degraded: **228 of 393 (58%)**. Of the degraded, 81 are degraded on both axes.
Totals: 1,177 abbreviated-commit citations, **446 citation instances** unresolvable
(252 distinct shas); 310 lane mentions, **301** naming a lane absent at HEAD.

Worst offenders by unresolvable citations: C384 (13), C360 (12), C353 (11), C409 (10),
C395 (9), then eight claims at 8 each (C357, C362, C366, C372, C378, C386, C403, C405,
C408).

**The CALR family, claim by claim:**

| Claim | shas cited | resolve | absent | lanes named | lanes gone |
|---|---|---|---|---|---|
| C294 | 1 | 1 | 0 | 0 | 0 |
| C312 | 1 | 1 | 0 | 1 | 1 |
| C324 | 2 | 1 | 1 | 1 | 1 |
| C334 | 3 | 2 | 1 | 1 | 1 |
| C348 | 5 | 2 | 3 | 1 | 1 |
| C350 | 4 | 4 | 0 | 2 | 2 |
| C358 | 8 | 1 | 7 | 2 | 2 |
| C364 | 5 | **0** | 5 | 2 | 2 |
| C367 | 7 | 2 | 5 | 0 | 0 |
| C368 | 5 | **0** | 5 | 1 | 1 |
| C378 | 8 | **0** | 8 | 1 | 1 |
| C383 | 7 | **0** | 7 | 0 | 0 |
| C391 | 6 | **0** | 6 | 0 | 0 |
| C401 | 3 | **0** | 3 | 1 | 1 |
| **TOTAL** | **65** | **13** | **52** | | |

**80% of the CALR family's cited commits do not exist in the repository.** Six claims
(C364, C368, C378, C383, C391, C401) have **zero** resolvable citations and no source
lane anywhere.

---

## 4. OTHER SILENT DELECTIONS AND EVIDENCE GAPS

**4.1 A fourth and fifth mass-deletion commit the governance record does not list.**
`13c557cd3` (2026-09-27 17:12) deletes **182,300 paths with 0 additions and 0
modifications**, reducing the tree from 290,992 to 108,692 paths. Its deletions are
dominated by `lab/epistemics` (73,349), `lab/lab` (73,106 - the doubled-path artifact
this repository has fixed twice before) and `lab/generations` (35,527). This is a
**deliberate path normalisation, not an incident**, and its content is fully recoverable
from parent `a61b5b94c` (reachable from origin). Reported for completeness, not as a
new wipe. The governance record's "9 wipes" refers to a **different class**: ledger
tail-wipes of 0 insertions / 96-136 deletions each, root-caused to the C377-anchored
tail-rewrite mint and addressed by `7ae7188eb` + `mint_guard_v2.sh`. The two classes
should not be conflated in future summaries.

**4.2 33 unreachable commits hold content on no ref.** `git fsck` reports commits dated
2026-08-29 to 2026-09-18 carrying R32 / E51-E56 work (31 commits of ~1,200 files each,
plus `ee7e4dea1` "checkpoint before masterplan execution" and `01cecb5fc` at 39,259
files). **None of the 252 unresolvable ledger shas matches any of them**, so they do not
rescue a single citation - but they are the only orphaned content in the object store
and should be re-referenced before a `git gc --prune` destroys them.

**4.3 C143-C159 are not canonical headers.** The ledger contains 393 claim blocks, not
410. C143-C152 were "proposed ... but never appended to this canonical ledger"; C143-C149
survive only as **appendix sub-bullets inside another claim's block**, and C150-C159 are
absent entirely. The ledger discloses this. Any tooling that assumes a contiguous
C1..C410 will mis-key these.

**4.4 The 252 unresolvable shas are not explained by the wipes.** Of 963 distinct hex
tokens cited in the ledger: 887 are abbreviated commit ids (92 of length 8, 793 of
length 9, 2 of length 10 - the 9-character convention is the house norm, not an
anomaly), 64 are sha256 file digests (not git object ids, out of scope here), 3 are
full 40-char shas, and 9 are odd tokens of length 12-51. Of the 887 abbreviations,
**635 resolve and 252 are genuinely absent**: `git cat-file --batch-check` reports
`missing` for all 252, and `git rev-parse --verify <h>^{commit}` fails for each. The
batch-check path was sanity-checked first against known-good abbreviations
(`4e7eb30b1`, `4e7eb30`, `b3b3ee00a` all resolve), so this is absence, not a tooling
artifact. The pattern - "local only, never pushed" commits made in now-deleted external
worktrees - is consistent with work done outside the repo's lane protocol.

**4.5 Not audited.** The 64 sha256 file digests cited in the ledger were not checked
against file content; that needs a per-claim file-hash pass and is out of scope here.

**4.6 C411-C466 confirmed non-canonical.** `ledger_write/STAGED_LEDGER_ENTRIES.md`
holds **49** entries: C411-C416 and C418-C460. C417 is absent. The canonical ledger ends
at C410. Consistent with `4b35be365`.

---

## 5. RECOVERABLE OR UNRECOVERABLE: SUMMARY

**Fully recoverable, method known, zero risk:**
- All 160,515 paths deleted by `b3b3ee00a` - `git checkout 4e7eb30b1 -- <path>`.
- 858 absent research lanes - same mechanism.
- The complete CALR engine, 43 files, `4e7eb30b1:l3_novel_intermediate_v2/`.
- The 33 unreachable commits - `git update-ref refs/recovered/unreachable-<sha> <sha>`.

**Genuinely lost, no recovery path:**
- 8 CALR-family lanes (waves 5-9, 2scalr, poolrepair, genrec) and the C350 red-team
  implementation. Never committed; worktrees and branches gone.
- 252 ledger-cited commits, and with them the evidentiary basis of at least 6 CALR
  claims and 113 ledger claims overall.
- Whatever was in the working trees of the `~/workspace/` worktrees at the moment they
  were deleted.

**Method note.** Every number above is either a `git` plumbing count (orchestration) or
computed by the two pure-Zag programs in this lane, `ledger_cites.zag` and
`evidence_join.zag`, under the watchdog with `--target macos-arm64`. No forbidden
interpreter was invoked; `tnn_pure_zag_report` reports `PURE-ZAG-CLEAN`.