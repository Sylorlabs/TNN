# COLLISION RESOLUTION: post-cutoff claim-number race on C455-C460

Status: PROPOSAL ONLY. No ledger files were read for writing; no ledger
modifications were made. This document unblocks LEDGER-WRITE (C458) by giving
the parent a concrete, recommended numbering resolution.

Date: 2026-10-03. Worker: LEDGER-COLLISION-RESOLVE (follow-up to LEDGER-WRITE C458).
Sources: `ledger_reconcile/LEDGER_RECONCILIATION.md` (C457 proposal, analysis
cutoff 10:09 UTC), `ledger_write/STAGED_LEDGER_ENTRIES.md` (C458 staging,
10:20:42 UTC), and the `WATCHDOG: ledger Cxxx` commit series on branch
`tnn-native-lab` through its head (24166d015, 10:23:46 UTC).

## 1. What changed since the task was written

The task describes a 3-number collision (C455/C456/C457 minted after the
10:09 UTC cutoff). The watchdog kept minting after the LEDGER-WRITE staging
too. Current occupancy of the proposed displaced block, verified from commit
subjects on `tnn-native-lab`:

| Number | Commit    | UTC 2026-10-03 | Claim |
|--------|-----------|----------------|-------|
| C455 | 08d350f62 | 10:10:36 | INTEGRATION-B1B2 INTEGRATION DEMONSTRATED K1-K12 |
| C456 | 0390c1f77 | 10:12:27 | C11-REFIX (PREREG_C11_AMENDMENT.md) |
| C457 | 92e42ea2d | 10:13:32 | LEDGER-RECONCILE (the C457 proposal itself) |
| C458 | d2619d72e | 10:21:02 | LEDGER-WRITE (the C458 staging itself) |
| C459 | 4bc4ced91 | 10:22:33 | COGOPS-PERIOD BUILD-PASS |
| C460 | 24166d015 | 10:23:46 | MA4-REDTEAM (RDDM=10 proxy breaks as predicted) |

All six numbers C455-C460 are now occupied by cleanly minted watchdog claims.
The task's literal Option A (displaced block to C459-C464) is therefore stale:
C459 and C460 are taken. The highest watchdog claim number anywhere is C460;
the canonical ledger's highest claim per the reconciliation is C410. The first
free contiguous block of six is C461-C466. A tree-wide grep found no references
to C455-C460 outside the two ledger documents, so neither side of the race has
hidden citation costs.

The displaced block (6 watchdog claims the reconciliation proposes to
renumber, in original chronological order):

| Old watchdog number | Commit | Experiment |
|---------------------|--------|------------|
| C404 | c66edb1ba | NEGATIVE-TRANSFER NT1 PASS |
| C405 | 3385761b6 | LIFETIME-META LM1 |
| C406 | ea8c50a52 | GEN-STATEFIX UPGRADE-TO-SUBSUMES |
| C407 | 054f42a33 | NT-CAPACITY NT2 FAIL |
| C409 | 78cb7703c | L3-INR-SEALED L3-KILLED |
| C410 | 5f612ec1a | GEN-STRESS BOUNDARY-FOUND ARENA-4MAP |

## 2. Options

### Option A (revised): displaced block moves to C461-C466

The six displaced claims take the next free block, preserving their original
relative chronological order. The six post-cutoff claims keep the numbers they
were minted with (C455-C460).

Concrete new numbering:

| Old watchdog number | New canonical number | Experiment |
|---------------------|----------------------|------------|
| C404 | C461 | NEGATIVE-TRANSFER NT1 PASS |
| C405 | C462 | LIFETIME-META LM1 |
| C406 | C463 | GEN-STATEFIX UPGRADE-TO-SUBSUMES |
| C407 | C464 | NT-CAPACITY NT2 FAIL |
| C409 | C465 | L3-INR-SEALED L3-KILLED |
| C410 | C466 | GEN-STRESS BOUNDARY-FOUND ARENA-4MAP |

Mechanical edits required to the staged text in STAGED_LEDGER_ENTRIES.md:
1. Renumber the six staged entries C455-C460 to C461-C466.
2. Rewrite the renumbering record: C404->C461, C405->C462, C406->C463,
   C407->C464, C409->C465, C410->C466.
3. Update internal references: C421 cites L3-INR-SEALED as C459, becomes C465;
   C447 cites GEN-STRESS as C460, becomes C466; the C454 entry note about the
   corrected "(C410)" becomes C466.
4. Draft six new staged entries for the post-cutoff claims at C455-C460
   (INTEGRATION-B1B2, C11-REFIX, LEDGER-RECONCILE, LEDGER-WRITE, COGOPS-PERIOD,
   MA4-REDTEAM). These were never staged by LEDGER-WRITE.

### Option B: renumber the six later claims to C461-C466

The displaced block keeps the proposal's C455-C460 exactly as staged; the
post-cutoff claims are renumbered:

| Minted as | New number | Claim |
|-----------|------------|-------|
| C455 | C461 | INTEGRATION-B1B2 |
| C456 | C462 | C11-REFIX |
| C457 | C463 | LEDGER-RECONCILE |
| C458 | C464 | LEDGER-WRITE |
| C459 | C465 | COGOPS-PERIOD |
| C460 | C466 | MA4-REDTEAM |

The staged LEDGER-WRITE text needs zero edits. Six new staged entries must be
drafted for C461-C466, plus a renumbering record for the later claims
(C455->C461 etc.).

### Option C: other schemes (considered, not recommended)

- C-sub (sub-numbering, e.g. C455a-C455f for one side): breaks the integer
  claim-number convention used by every entry, commit subject, and citation.
  Reject.
- C-rev (reverse the concessions: give the displaced claims C404-C410 back,
  renumber the canonical entries): explicitly rejected by the reconciliation
  and contradicted by the watchdog's own concession commits
  (9992a325e, 1611dc81c, 44ecf987a, c99bd82f5, ff8a2d8df, 92a1831a7).
  Reject.
- C-gap (sparse numbering with reserved gaps): no benefit, adds a new
  convention to maintain. Reject.

## 3. Recommendation: Option A (revised)

Move the displaced block to C461-C466; the post-cutoff claims keep C455-C460.

Justification:

1. Precedent. The reconciliation's own governing principle is that
   established occupants keep their numbers and the orphans get renumbered
   (canonical C404-C410 stand; displaced watchdog claims move). Applied to
   this race: the six displaced claims are orphans by the watchdog's own
   concession commits; the six C455-C460 claims were minted cleanly after the
   cutoff and were never conceded. Clean title keeps its numbers.
2. Symmetry of cost, asymmetry of fairness. Both options rename six claims.
   Option B renumbers six claims that followed the rules; Option A moves six
   claims that were already homeless. The race should not punish the later
   claims for the proposal's stale assumption that C455-C460 were free.
3. Chronological coherence. C455-C460 were minted 10:10:36 to 10:23:46 UTC in
   strict order; keeping them forms a coherent post-reconciliation run in the
   ledger. The displaced block lands as one contiguous chronologically ordered
   block at C461-C466 with a single renumbering record, exactly as the
   proposal intended, shifted by six.
4. Self-description hazard under Option B. The LEDGER-RECONCILE meta-claim
   (C457) and LEDGER-WRITE meta-claim (C458) would move to C463/C464 while
   their own documents propose and stage the C455-C460 block. Readers would
   reasonably ask why the proposal's own claim is not in the block it
   proposes. Option A avoids this.
5. No hidden costs either way. No lane document outside the two ledger files
   references C455-C460, so the mechanical edit list in Option A is complete
   and small.

Note on chronology: under Option A the ledger will show C461-C466 (minted
07:47-08:05) after C455-C460 (minted 10:10-10:23). This mild inversion is
acceptable: the ledger already contains concession re-mints and
non-chronological runs, and the renumbering record carries original minting
times for audit.

## 4. Preconditions the parent must clear before any ledger write

1. Repair the ledger file first. Commit f20dddf0b (2026-10-03 08:12:23 UTC,
   titled "WATCHDOG: ledger C415") deleted 136 lines, C377 through C410, from
   `canonical_ledger/CLAIM_LEDGER.md` on `tnn-native-lab`. This is a second
   occurrence of the b9999590 fault pattern the reconciliation flagged. The
   reconciliation's "canonical priority" premise requires C404-C410 (and the
   C377-C403 range) to be present. Restore from 860f009b5 (whose ledger state
   runs through C410) before writing anything.
2. Freeze watchdog claim minting until the ledger write lands. The target
   block shifted twice already (once before staging, once after). Any further
   minting re-opens this exact collision.
3. Draft the six C455-C460 entries (Option A item 4 above). LEDGER-WRITE
   staged 49 entries; the full write is 55 entries plus the C417 decision.
4. C417 disposition is still open (verify-then-supersede vs admit, per
   reconciliation section 4c).
5. Decide the reconciliation's open question 5: whether the uncommitted
   C401-C410 working-tree entries are committed before appending C411+.

## 5. Exact final ledger tail under the recommendation

After the existing canonical C410 entry, in append order:

- C411-C416, C418-C454: 43 watchdog-only claims as staged (C429 stays
  EXPLORATORY, C453 CONDITIONAL-PASS, per staged caveats).
- C455: INTEGRATION-B1B2 INTEGRATION DEMONSTRATED K1-K12 (watchdog 08d350f62)
- C456: C11-REFIX PREREG_C11_AMENDMENT (watchdog 0390c1f77)
- C457: LEDGER-RECONCILE proposal summary (watchdog 92e42ea2d)
- C458: LEDGER-WRITE staging record (watchdog d2619d72e)
- C459: COGOPS-PERIOD BUILD-PASS (watchdog 4bc4ced91)
- C460: MA4-REDTEAM (watchdog 24166d015)
- C461: NEGATIVE-TRANSFER NT1 PASS (ex watchdog C404, c66edb1ba)
- C462: LIFETIME-META LM1 (ex watchdog C405, 3385761b6)
- C463: GEN-STATEFIX UPGRADE-TO-SUBSUMES (ex watchdog C406, ea8c50a52)
- C464: NT-CAPACITY NT2 FAIL (ex watchdog C407, 054f42a33)
- C465: L3-INR-SEALED L3-KILLED (ex watchdog C409, 78cb7703c)
- C466: GEN-STRESS BOUNDARY-FOUND ARENA-4MAP (ex watchdog C410, 5f612ec1a)

No em dashes were used in this document (verified by author).

No ledger modifications were made in producing this document.
