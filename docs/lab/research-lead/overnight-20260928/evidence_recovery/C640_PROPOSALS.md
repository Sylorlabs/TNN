# C640-C649: PROPOSALS ONLY - NOT MINTED

**Lane:** `lane/recovery`. **Date:** 2026-10-03/04.

## Status of this document

`canonical_ledger/CLAIM_LEDGER.md` was **not modified**. It remains pure-append, ending
at C410. `mint_guard/mint_guard_v2.sh` was not invoked to write, only read.

**ID range.** C600-C602 were minted by `redteam/suf-audit` at `ce2dd1be9`. Per brief
section 10, C377-C466 are contested by the pending reconciliation and must not be
minted. This lane therefore proposes **C640-C649**, which is above the contested block
and does not collide with C500-series work (`d97d6d0e3`, `8534fd128`,
`8948b4a71`) or C590/C591.

Nothing below is minted. Each item is a **proposal for the ledger owner to accept,
modify, or reject.**

---

## P1 (proposed C640) - DOWNGRADE: CALR / l3_niv2 is L1, not L2+

**Applies to:** C350, C358, C364, C367, C391 (the five named in the task).
**Proposed action:** reclassify the *mechanism* level of the L3-NIV2 / CALR
novelty claim and its descendants from L2+ to **L1**.

**Basis, from recovered source (`4e7eb30b1`, restored at
`recovered/l3_novel_intermediate_v2/`):**

`impl/isa.zag:5-11` states, in the source's own words:

- the basis is "the C281-line **5-op** register ISA already present in the learner
  lineage: `0=CPY, 1=ADD, 2=MUL, 3=SET1, 4=INC`"
- registers `R0..R3`, instruction = 3 bytes, **max 64 instructions**
- "**ZERO new opcodes, ZERO new semantic cases.** Execution semantics are ported
  exactly from the committed `xdomain_grammar_l2m/glm_learner.zag` `m_exec`"

Verified in the same tree: `lm_cons.zag:79` pool cap 32768; `lm_cons.zag:243`
"generate all 80 append children"; `lm_cons.zag:269` "80 substitute-last children";
`lm_cons2.zag:185` `select_beam`. The 80 is `5 ops x 4 dst x 4 src` - an
enumeration of a fixed 5-opcode DSL, not an alphabet of 80 opcodes. (This corrects the
premise that the alphabet "IS C281's 80 instructions"; the verdict is unchanged and
sharper, because a 5-opcode DSL is strictly easier to enumerate than an 80-opcode one.)

**Bar failed.** Brief section 9: an L3 claim is credible only if the novel form itself
is not enumerable from source, and "brute-force search over a fixed DSL" is explicitly
not L3. CALR is an argmax/beam search over an enumerated pool of a DSL whose source
declares zero added semantics. This is the same finding, on the same alphabet, that
already killed C281/C284 to L1.

**Note on C350 specifically.** C350 is a *red-team* claim, not the novelty claim
itself. Its content ("2 CONFIRMED KILLS + 1 HONEST NEGATIVE") is a statement about
CALR's failure modes, not about CALR's level. The downgrade attaches to the CALR
mechanism level asserted across the family; whether C350's own red-team verdict
survives is a separate question, addressed in P2.

---

## P2 (proposed C641) - DOWNGRADE FOR ABSENT EVIDENCE: eight CALR claims are UNVERIFIED

**Applies to:** C358, C364, C367, C368, C378, C383, C391, C401.

**Proposed action:** reclassify the *evidentiary status* of these entries from
COMPLETE/BUILD-PASS to **UNVERIFIED - NO COMMITTED EVIDENCE**.

**Basis.** For each, the source lane has **zero commits touching it anywhere in the
repository, across all 65 refs** (`git log --all -- <lane>` returns nothing):

```
l3_niv2_2scalr_survival        l3_novel_intermediate_v2_wave5
l3_niv2_pool_repair            l3_niv2_w6_thirdstage
l3_niv2_genrec_integration     l3_niv2_w7_yield
                               l3_niv2_w8_instr
                               l3_niv2_w9_ppcost
```

The branches their entries cite do not exist as refs
(`lane-l3niv2w5-20261002`, `lane-hcontlife5-20261002`, `lane-compinteg2-20261002`).
Their worktrees were under `~/workspace/`, which does not exist on this host. Of the 65
abbreviated commits these eight claims cite, **52 do not resolve**; six of the eight
(C364, C368, C378, C383, C391, C401) have **zero** resolvable citations.

C350's red-team lane has only its `PREREG.md` and `NAMECHECK.md` committed; the
implementation, `REPORT.md`, `attacks/` and 12 run logs were never committed, as the
entry itself discloses ("written but uncommitted pending disk recovery").

**This is not a claim that the work was not done.** It is a claim that the work left no
trace in the repository, so nothing about it can be verified, reproduced, or cited now.
The honest disposition is UNVERIFIED, not FALSE.

---

## P3 (proposed C642) - RECORD the b3b3ee00a wipe as a NON-LOSS event with a quantified blast radius

**Proposed action:** add a governance entry recording the following as fact.

| Field | Value |
|---|---|
| Commit | `b3b3ee00a47e6be1c80e54bb00500e5450d75317` |
| Parent | `4e7eb30b107b9a04ccf5f0f4bacc37f821718df0` |
| Author / date | `tnn-rsi-loop <rsi-loop@localhost>`, 2026-10-03 20:43:45 +0000 |
| Subject | `lm3_lifetime: prereg (PREREG.md + NAMECHECK.md); ... Non-ledger.` |
| Paths touched | 160,517 (2 added, 0 modified, 160,515 deleted) |
| Lines | 234 insertions, 44,104,446 deletions |
| Binary files among deletions | 15,024 |
| Content lost | **none** - 160,515/160,515 deleted paths present in parent |
| Parent reachable from | `origin/tnn-native-lab` and all 32 local branches (55 refs incl. remotes) |
| Repair commit | **none** |
| Tree at HEAD vs parent | 5,276 vs 165,288 tracked paths (-96.8%) |
| Research lanes at HEAD vs parent | 258 vs 1,108 (**858 absent, -77.4%**) |

**Why this entry matters.** The framing "catastrophic unrepaired whole-tree wipe"
invites a false inference of data loss. The correct characterisation is **an
unrepaired tree-state corruption with zero data loss and a 77% loss of corpus
*visibility***. The 858 absent lanes are all recoverable from `4e7eb30b1`. Recording
this precisely prevents a future responder from concluding the record is lost, and
prevents a future auditor from repeating the false negative that searching HEAD
produced.

**Proposed remediation entry (proposed C643):** restore the 858 lanes. Method:
`git checkout 4e7eb30b1 -- docs/lab/research-lead/overnight-20260928/` as a
tree-surgery commit on a new branch with explicit pathspecs, no history rewrite, no
science adopted, no kill bar touched. Precedent: `b688fa031` (GIT-REPAIR2) and
`cef8c4095` (REPAIR), both of which are exactly this operation and are acceptable
precedent in this repository.

---

## P4 (proposed C644) - The ledger contains 393 claim blocks, not 410

**Proposed action:** record that C143-C152 were never appended as canonical headers and
C153-C159 do not exist in the ledger at all.

**Basis.** The ledger's own text discloses it: "commit dd704acd8 proposed C143-C152 for
earlier completed work but was never appended to this canonical ledger. This append
consumes C143-C149." C143-C149 survive only as appendix sub-bullets nested inside
another claim's block. Block count by header detection: **393**.

**Consequence.** Any tooling, index, or summary that assumes a contiguous C1..C410 will
mis-key these 17 IDs. This should be recorded so the gap is understood rather than
rediscovered.

---

## P5 (proposed C645) - Instrument the mass-deletion class; it is currently caught socially

**Proposed action:** add a check to `mint_guard_v2.sh` (or a sibling
`tree_guard.sh`) that fails a commit whose diff deletes more than N paths unless the
commit message names the incident sha, mirroring the existing retroactive
ins>0/del==0 rule.

**Basis.** The failure mode is measured, not hypothetical. Five commits in this
repository's history delete >147,000 paths each. Three were caught - but only because a
commit subject happened to say "nuked", "mass deletion", or "WATCHDOG". One
(`b3b3ee00a`, 160,515 paths) carries a subject reading `lm3_lifetime: prereg ...
Non-ledger` and was **never caught**. `git log --oneline` shows nothing anomalous; the
signal exists only in `git show --numstat`.

A pre-commit rule of the form *deletes more than 1000 paths, therefore the message must
name the offending sha (>= 8 hex chars)* would have flagged all five and blocked none
of the legitimate restores, because every restore commit already names its sha in the
subject: `cef8c4095` "restore full tree nuked by 169894404", `b688fa031` "restore
160348 files deleted by c721bcc61", `3c25ff8f1` "completes f461e812d mass-deletion
repair", `7e4d7cffe` "restore 13 files deleted by f461e812d", `3b61e5e57` "restore 9
files deleted by f461e812d". The rule costs the repairers nothing and would have
stopped `b3b3ee00a`.

**Proposed threshold note.** `13c557cd3` (182,300 deletions, 0 additions, 0
modifications) is a deliberate path normalisation, not an incident, and a
count-only rule would flag it as a false positive. The subject-sha requirement
resolves this: a deliberate normalisation should say which sha it normalises.

---

## P6 (proposed C646) - 33 unreachable commits must be re-referenced before any gc

**Proposed action:** `git update-ref refs/recovered/unreachable-<sha> <sha>` for each of
the 33 unreachable commits reported by `git fsck --unreachable`, then a normal push.

**Basis.** 33 commits dated 2026-08-29 to 2026-09-18 sit on no ref: 31 carrying R32 /
E51-E56 work at ~1,200 files each, plus `ee7e4dea1` "checkpoint before masterplan
execution" (39,259 files) and `01cecb5fc` (39,259 files). They are the only orphaned
content in the object store.

**Important negative result, so this is not oversold:** **none of the 252 unresolvable
ledger shas matches any of these 33 commits.** They rescue no citation. Their value is
provenance for the R32 generation, not repair of the ledger.

---

## P7 (proposed C647) - Record the false-negative lesson as a standing audit rule

**Proposed action:** adopt as a standing rule: **no negative existence claim about
source in this repository may be made from a tree inspection at a branch tip.** Every
`has no source` / `does not exist` / `never committed` statement must be accompanied by
a `git log --all --diff-filter=A -- <path>` sweep across all refs, or it must be
qualified as "absent from the tree inspected at <commit>".

**Basis.** `SUF_AUDIT.md` section 1 and boundary B-A1 concluded the CALR family had no
source in the repository, from `git ls-tree` at HEAD and at `cef8c4095`. The source was
present at `4e7eb30b1` the whole time. The audit's *discipline* - absent, therefore not
adjudicable, therefore no accusation - was sound and I endorse it. But the absent
evidence was recoverable and would have settled the level question in three lines, as
C602 and P1 both show.

This is not a criticism of that audit's reasoning. It is a process fix: at HEAD the tree
carries 3.2% of the corpus, so any tip-based existence query is nearly guaranteed to
return a false negative.

---

## P8 (proposed C648) - The 300+ degraded claims need a mechanical citation repair, not per-claim re-adjudication

**Proposed action:** before any of the 113 SHA-UNRESOLVABLE claims is re-run or cited,
attempt a mechanical repair pass: for each, resolve the lane name to a directory and
search all refs for a commit touching that lane, then rewrite the citation to a sha
that exists, or mark the entry UNVERIFIED.

**Basis.** 116 LANE-GONE claims are **fully recoverable** - the evidence exists, it is
just not in the working tree. This is a mechanical `git log --all -- <lane>` lookup per
claim, not an experiment. 81 claims are degraded on both axes; for those the lane
recovery is necessary but may not be sufficient.

**Explicitly not proposed:** re-running any experiment, and re-adjudicating any
mechanism. This is a bookkeeping repair. The scientific content of those claims is
untouched by it and remains exactly as credible or not as it was.

---

## What is NOT proposed

- No modification of `canonical_ledger/CLAIM_LEDGER.md`.
- No minting of any claim ID, by this lane, in this commit.
- No history rewrite, no `git commit -a`, no reset, no amend.
- No re-run of any experiment. This lane ran none.
- No verdict on whether any specific claim is *true*. This audit establishes only
  whether its cited evidence can be located.