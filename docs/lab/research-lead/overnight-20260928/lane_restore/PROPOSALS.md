# C650-C659: LEDGER PROPOSALS - NOT MINTED, LEDGER NOT MODIFIED

**Lane:** `lane/restores`. **Date:** 2026-10-04.
**Source audit:** `lane/recovery` `9b2c4db6e`, `C640_PROPOSALS.md`.

## Status

`canonical_ledger/CLAIM_LEDGER.md` was **not modified**. It remains pure-append,
ending at C410. `mint_guard_v2.sh` was read, never invoked to write. **No claim ID
below is minted.** Every item is a proposal for the ledger owner to accept, modify,
or reject.

**ID range.** C377-C466 are contested by the pending reconciliation and must not be
minted (brief section 10). C600-C602 were taken by `redteam/suf-audit` at
`ce2dd1be9`. `lane/recovery` proposed C640-C649. This lane proposes **C650-C659**,
which collides with nothing.

## Disposition of every audit proposal, after execution

The audit proposed nine items. This lane executed the mechanical ones and reports
what actually happened, including where the audit's numbers were wrong.

| Audit item | Disposition |
|---|---|
| P1 / C640 CALR -> L1 | **ACCEPTED and EXTENDED** (C650). Scope corrected from 5 to 14 claims. |
| P2 / C641 8 CALR claims -> UNVERIFIED | **ACCEPTED** (C651). Independently re-verified. |
| P3 / C642 record the wipe as non-loss | **ACCEPTED with CORRECTED FIGURES** (C652). |
| P3 rem / C643 restore the 858 lanes | **DONE**, not a proposal. Superseded by C653; commit `9d5c7f940`. |
| P4 / C644 393 blocks not 410 | **ACCEPTED** (C654). |
| P5 / C645 instrument mass deletion | **DONE**, not a proposal. Commit `07708b5822`. |
| P6 / C646 re-reference 33 commits | **DONE**, not a proposal. Commit `e963a9b31`. |
| P7 / C647 no tip-based existence claims | **ACCEPTED** (C655). Strongly endorsed. |
| P8 / C648 mechanical citation repair | **REJECTED BY MEASUREMENT** (C656). Attempted; yields nothing. |

---

## C650 - DOWNGRADE: the whole CALR / l3_niv2 family is L1, not L2+

**The audit named 5 claims. The family is 14.** Downgrading only the named five
would leave nine sibling claims asserting L2+ on the same mechanism, which is the
error this whole exercise exists to stop. The full 14-claim set:

```
C294  C312  C324  C334  C348  C350  C358  C364  C367  C368  C378  C383  C391  C401
```

**Proposed action:** reclassify the *mechanism level* asserted across the family
from L2+ to **L1**.

**Basis - the source's own testimony.** `l3_novel_intermediate_v2/impl/isa.zag:5-11`,
restored at this lane's tip and verified **byte-identical to `4e7eb30b1`**
(tree `2a47a61abc9425d45d4dd9e910b09befbb0f6728` both sides):

- basis is "the C281-line **5-op** register ISA already present in the learner
  lineage: `0=CPY, 1=ADD, 2=MUL, 3=SET1, 4=INC`"
- registers `R0..R3`, instruction = 3 bytes, **max 64 instructions**
- "**ZERO new opcodes, ZERO new semantic cases.** Execution semantics are ported
  exactly from the committed `xdomain_grammar_l2m/glm_learner.zag` `m_exec`"

Same tree: `lm_cons.zag:79` pool cap 32768; `lm_cons.zag:243` "generate all 80
append children"; `lm_cons.zag:269` "80 substitute-last children";
`lm_cons2.zag:185` `select_beam`. The 80 is `5 ops x 4 dst x 4 src` - an
enumeration of a fixed 5-opcode DSL, not an alphabet of 80 opcodes.

**Bar failed.** Brief section 9: an L3 claim is credible only if the novel form
itself is not enumerable from source, and "brute-force search over a fixed DSL"
is explicitly not L3. CALR is a beam/argmax search over an enumerated pool of a
DSL whose source declares zero added semantics. Same finding, same alphabet,
that already killed C281/C284 to L1.

**Note on C350.** C350 is a *red-team* claim, not the novelty claim. Its content
("2 CONFIRMED KILLS + 1 HONEST NEGATIVE") is a statement about CALR's failure
modes, not about CALR's level. Whether C350's own red-team verdict survives is a
separate question, addressed in C651, and the ledger owner may reasonably hold
C350's red-team status while still downgrading the family level.

---

## C651 - DOWNGRADE FOR ABSENT EVIDENCE: 9 CALR-family claims are UNVERIFIED

**Applies to:** C350, C358, C364, C367, C368, C378, C383, C391, C401.
(The audit named 8 and omitted C350; C350's *implementation* is missing even
though its lane has commits, so its evidentiary status is degraded too.)

**Proposed action:** reclassify the *evidentiary status* of these entries from
COMPLETE/BUILD-PASS to **UNVERIFIED - NO COMMITTED EVIDENCE**.

**Basis, re-verified independently in this lane, after the restore:**

| Lane | commits across all refs | files at this lane's tip |
|---|---|---|
| `l3_niv2_2scalr_survival` | **0** | 0 |
| `l3_novel_intermediate_v2_wave5` | **0** | 0 |
| `l3_niv2_pool_repair` | **0** | 0 |
| `l3_niv2_w6_thirdstage` | **0** | 0 |
| `l3_niv2_genrec_integration` | **0** | 0 |
| `l3_niv2_w7_yield` | **0** | 0 |
| `l3_niv2_w8_instr` | **0** | 0 |
| `l3_niv2_w9_ppcost` | **0** | 0 |
| `l3_niv2_calr_redteam` | 7 | **2** (PREREG.md, NAMECHECK.md only) |
| `l3_novel_intermediate_v2` (engine) | 12 | **43 - fully recovered** |

This was checked *after* restoring 160,514 paths, so it is not an artifact of the
invisibility that produced the original false negative. The eight lanes have zero
commits touching them anywhere; the branches their entries cite
(`lane-l3niv2w5-20261002`, `lane-hcontlife5-20261002`, `lane-compinteg2-20261002`)
do not exist as refs; their worktrees were under `~/workspace/`, which does not
exist on this host.

**This is not a claim that the work was not done.** It is a claim that the work
left no trace in the repository, so nothing about it can be verified, reproduced
or cited now. The honest disposition is UNVERIFIED, not FALSE.

---

## C652 - RECORD the b3b3ee00a wipe as a NON-LOSS event, with corrected figures

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
| Content lost | **none** - 160,515/160,515 deleted paths present in the parent |
| Parent reachable from | `origin/tnn-native-lab` and all 32 local branches |
| Repair commit at time of audit | **none** |
| Repair commit now | **`9d5c7f940`** (this lane) |

**Why this entry matters.** The framing "catastrophic unrepaired whole-tree wipe"
invites a false inference of data loss. The correct characterisation is **an
unrepaired tree-state corruption with zero data loss and a 77% loss of corpus
*visibility***. Recording it precisely prevents a future responder from concluding
the record is lost, and prevents a future auditor from repeating the false negative
that searching HEAD produced.

---

## C653 - RECORD the completed visibility restore, and correct the audit's lane count

**Proposed action:** record the restore and record that **the audit undercounted
the missing lanes by 493.**

| Metric | audit `9b2c4db6e` | this lane, re-derived |
|---|---|---|
| research lane dirs at `4e7eb30b1` | 1,108 | **1,601** |
| research lane dirs before restore | 258 | 259 |
| lane dirs absent | **858** | **1,351** |

The audit's 858 are a strict **subset** of this lane's 1,351; 493 further lane
directories were missing and uncounted. Both figures were produced by header
detection over `git ls-tree -r -t`; the audit's lane grammar evidently matched a
subset. **The audit's direction was right and its magnitude was conservative**,
which is the safe direction to be wrong in, but the ledger should carry the larger
number so the restore's coverage can be verified against it.

**Restore commit:** `9d5c7f940`, 160,514 paths, 44,104,409 insertions, **0
deletions, 0 modifications**. Verified at tip: **858/858** of the audit's lanes
and **1,351/1,351** of the re-derived set are present; tracked paths 5,276 ->
165,793.

---

## C654 - The ledger contains 393 claim blocks, not 410

**Proposed action:** record that C143-C152 were never appended as canonical
headers and C153-C159 do not exist in the ledger at all.

**Basis.** The ledger discloses it: "commit dd704acd8 proposed C143-C152 for
earlier completed work but was never appended to this canonical ledger. This
append consumes C143-C149." C143-C149 survive only as appendix sub-bullets nested
inside another claim's block. Block count by header detection: **393**.

**Consequence.** Any tooling, index or summary that assumes a contiguous
C1..C410 will mis-key these 17 IDs. Record it so the gap is understood rather than
rediscovered.

---

## C655 - STANDING AUDIT RULE: no negative existence claim from a branch tip

**Proposed action:** adopt as a standing rule - **no negative existence claim
about source in this repository may be made from a tree inspection at a branch
tip.** Every `has no source` / `does not exist` / `never committed` statement must
be accompanied by a `git log --all --diff-filter=A -- <path>` sweep across all
refs, or must be qualified as "absent from the tree inspected at `<commit>`".

**Basis, now with a measured denominator.** Before this lane's restore, the tree
at HEAD carried 5,276 of 165,288 tracked paths - **3.2%**. At that ratio any
tip-based existence query is close to guaranteed to return a false negative. The
`SUF_AUDIT.md` conclusion that the CALR family had no source was true of the tree
it searched and false of the repository; the source was at `4e7eb30b1` the whole
time, and this lane has now restored it to the tip.

This is not a criticism of that audit's discipline - absent, therefore not
adjudicable, therefore no accusation, was sound, and is endorsed. It is a process
fix. After `9d5c7f940` the tip carries 100% of what `4e7eb30b1` held, so the rule
is cheap to satisfy going forward.

---

## C656 - REJECT the mechanical citation-repair proposal: it yields nothing

The audit's P8 proposed "before any of the 113 SHA-UNRESOLVABLE claims is re-run or
cited, attempt a mechanical repair pass ... then rewrite the citation to a sha that
exists, or mark the entry UNVERIFIED." **This lane executed that pass. It returns
nothing.** Recording the negative so the proposal is not re-attempted.

| Rule | Test | Result |
|---|---|---|
| R1 truncation | 9-char citation truncated to 8 resolves? | 0 / 161 |
| R2 Hamming <= 1 | any commit <= 1 hex char away, over the cited length? | **0 / 252** |
| R3 substring | citation at any offset in any full sha? | 0 / 252 |

All 252 are absent as commit, blob, tree **and** tag. The 33 re-referenced
unreachable commits rescue **0** of them. No other repository exists on this host.
A positive control proves the detector fires on exact hits and on single-character
errors mid-string and in the final position (`cite_remap_CONTROL.tsv`).

**Proposed action:** adopt **only the second half** of P8. Mark the 113 claims
UNVERIFIED-EVIDENCE. **Do not** perform the sha-rewriting half: there is no target
to rewrite to, and redirecting a citation to a nearby commit would fabricate
provenance.

---

## C657 - The 116 LANE-GONE claims are now mechanically resolvable

**Proposed action:** record that the 116 LANE-GONE verdicts from the 393-block
audit are **retired**, not re-adjudicated.

**Basis.** All 858 audit-named lanes, and all 1,351 re-derived lanes, are present
at this lane's tip. The cited shas for these claims already resolved; only the
*lane directory* was invisible, and that is fixed. Per-claim evidence status for
these 116 should be recomputed once against a tip that carries the corpus.

**Explicitly not proposed:** re-running any experiment, or re-adjudicating any
mechanism. This is a bookkeeping repair. The scientific content of those claims is
untouched by it and remains exactly as credible or not as it was.

---

## C658 - Do not conflate two different classes of mass deletion

**Proposed action:** record that the governance record's "9 wipes" and the
path-normalisation commits are **different classes** and must not be tallied
together.

Class A - ledger tail-wipes, 0 insertions / 96-136 deletions each: the C377-anchored
mint, already addressed by `7ae7188eb` + `mint_guard_v2.sh`.

Class B - tree sweeps, ~10^5 paths each: `c721bcc61` (160,361), `f461e812d`
(147,295), `169894404` (165,250), `b3b3ee00a` (160,515). These are the class that
`b3b3ee00a` belongs to and the class the new mass-deletion tripwire targets.

Separately, `13c557cd3` (2026-09-27, 182,300 deletions, 0 additions, 0
modifications) is a **deliberate path normalisation**, not an incident, and its
content is fully recoverable from parent `a61b5b94c`. It is a false positive for a
count-only rule and is why the tripwire's threshold is paired with an explicit
`--no-verify` bypass rather than being treated as proof of a wipe.

---

## C659 - RECORD the tripwire, and that its threshold is validated in both directions

**Proposed action:** record `mass_delete_guard` as installed governance.

- Source: `docs/lab/research-lead/overnight-20260928/lane_restore/mass_delete_guard.sh`
  + `.zag`, commit `07708b5822`.
- Installed at `<git-common-dir>/hooks/pre-commit`, so it protects all 25 worktrees
  including those whose HEAD predates it. Fails CLOSED.
- Rule: refuses a commit deleting more than **1000 paths** (paths, not lines;
  renames count as deletions).
- **Would have blocked all four historical sweeps**: `b3b3ee00a` 160,515,
  `c721bcc61` 160,361, `f461e812d` 147,296, `169894404` 165,250 - all REFUSED by
  retrospective test.
- **Costs the five real repairs nothing**: `b688fa031`, `cef8c4095`, `84727be29`,
  `3c25ff8f1`, `7e4d7cffe` - all ACCEPTED, each with 0 deletions.
- **Not a blanket ban**: a live 999-path deletion was ACCEPTED; a live 1,501-path
  deletion was REFUSED and produced no commit.
- Bypass for a genuinely intended deletion: `git commit --no-verify`, with the
  authorising sha or ref named in the commit body.

---

## What is NOT proposed

- No modification of `canonical_ledger/CLAIM_LEDGER.md`.
- No minting of any claim ID by this lane.
- No history rewrite, no `git commit -a`, no amend, no rebase, no force-push.
- No re-run of any experiment. This lane ran none.
- No verdict on whether any specific claim is *true*. This lane establishes only
  whether its cited evidence can be located.
- No repair of the 252 dead citations, because no repair exists.
