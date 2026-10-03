# RESULT: H-FDCR-UNIFIED3 Repair (SURVIVES, 6/6 kill bars)

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED3 Repair Researcher (independent subagent)
**Target:** H-FDCR-UNIFIED2 DOWNGRADED (red team: FDCR_UNIFIED2_ADV_RESULT.md)
**Prereg:** `PREREG_FDCR_UNIFIED3.md`, committed as `ff25ebaab`
  (strictly before any implementation edit or test run)
**Verdict:** SURVIVES. All six frozen kill bars pass: K-FU3-1..4
  (new repairs), K-FU3-5 (full regression), K-FU3-6 (determinism).
**Classification:** bounded L2 integration repair. No L3 claimed.

## 1. Methodology

The three red-team downgrades (X-FU2-2a order fragility, X-FU2-2b
silent fact/member caps with misleading emit, X-FU2-2c silent
feature cap) were repaired in a verbatim copy of the mechanism:
`unified_fdcr3.zag` = `unified_fdcr2.zag` copied byte-identical,
then exactly four edits (R1-R4, below). `unified_fdcr2.zag` was
not modified. The new `main()` keeps the entire frozen H-FDCR-UNIFIED2
test suite (Parts A-C) intact and appends PART D with the four new
kill-bar fixtures. The only intentional output change in Parts A-C
is the banner line naming the new repair set.

Compilation: `znc unified_fdcr3.zag -o /tmp/fdcr3_run`
(analyzer warnings only, non-fatal; binary 194519 bytes,
0 external tools).

Determinism: three consecutive runs byte-identical
(cmp-verified), md5 `ae29af93d28171c3e37bdca7bf4393b3`.

Pure Zag: no Python at any stage. All edits via file tools, all
runs and analysis via shell and compiled-binary output.

## 2. Repairs implemented (exactly per frozen prereg)

### R1: Order-normalized feature-set identity (X-FU2-2a)

In `fn con_form`, the positional identity check
(`con_feat(W,c,i)` vs `feats[i]` index by index) was replaced with
a set-identity check: for each incoming feature, the candidate
concept's full feature list is searched for a content-equal
string. `con_nfeat(W,c)==nfeat` is still enforced first, so equal
cardinality plus one-directional inclusion implies set identity.
Positional comparison is gone.

### R2: Honest member-cap handling (X-FU2-2b, member cap + emit)

`con_form` has exactly one caller (`handle_concept_learn`), so its
return contract was extended (frozen in prereg):
- feature-set match with member added: return concept index
  (unchanged);
- feature-set match with member-add skipped (`nm>=8`): emit
  `ULEARN concept: WARN member cap 8 reached on concept N; subject
  NOT added` and return the sentinel `-2` (MATCH-NOADD);
- already-member match: return concept index (unchanged).

`handle_concept_learn` handles `ci==-2` explicitly: the subject
emit line reads `-> MATCH (feature set known; subject NOT added:
8-member cap)`. It never asserts `-> concept N` membership for a
subject that was not added. `con_find_member_str` returns -1 for
such subjects (honest: no membership exists).

### R3: Loud fact cap (X-FU2-2b, fact cap)

The `np<16` guard in pass 1 no longer silently skips. Skipped
parseable facts are counted (`ndropped_facts`); if any, the
output contains `ULEARN concept: WARN fact cap 16 reached; M
facts dropped`. The return value contract (`np`, max 16) is
unchanged.

### R4: Loud feature caps (X-FU2-2c + extension path)

Both silent feature-drop sites now count and warn:
- per-subject accumulation (`nfacc<8` guard): `ndropped_feat`
  per subject; emits `ULEARN concept: WARN feature cap 8
  reached for subject [S]; M features dropped`;
- cross-batch concept extension (`con_nfeat(W,ci)<8` guard):
  `ndropped_ext`; emits `ULEARN concept: WARN feature cap 8
  reached on concept N; M features dropped`.

Dedup semantics and all other accumulation/extension behavior are
unchanged.

## 3. Kill-bar evidence

### K-FU3-1: order fragility closed (D-T1)

The exact X-FU2-2a red-team fixture. Batch 1:
`T cat | is_a | pet;T cat | color | orange`. Batch 2:
`T dog | color | orange;T dog | is_a | pet` (same feature SET,
different fact ORDER).

Result: `con_count=1`; cat and dog in the same concept
(`con_find_member_str` agrees). Procedure trained on
`cat>tac;dog>god` yields `train_con=0` (votes 2/2, strict majority
holds). Under H-FDCR-UNIFIED2 this fixture produced 2 concepts
and `train_con=-1`. Raw output line 123:
`D-T1 order variation: 1 concept, train_con=0 PASS`.

K-FU3-1 PASS.

### K-FU3-2: fact cap is loud (D-T2)

20 facts for 20 distinct subjects in one batch.

Result: `np=16` (contract unchanged); `con_find_member_str`
returns -1 for s16..s19, and s0 is a member. Raw output line
142: `ULEARN concept: WARN fact cap 16 reached; 4 facts
dropped`. Raw output line 168:
`D-T2 20 facts: np=16, s19 absent, s0 member PASS`.

K-FU3-2 PASS.

### K-FU3-3: member cap is honest (D-T3)

9 subjects with identical features `is_a=pet` (under the 16-fact
cap).

Result: exactly 1 concept formed; the 9th subject m8 is NOT a
member (`con_find_member_str("m8")=-1`); m0 is in concept 0.
Raw output line 188:
`ULEARN concept: WARN member cap 8 reached on concept 0; subject
NOT added`. Raw output line 189:
`ULEARN concept: subject [m8] nfeat=1 -> MATCH (feature set
known; subject NOT added: 8-member cap)`. No line asserts
`-> concept 0` membership for m8. Raw output line 191:
`D-T3 9 subjects: 1 concept, m8 not member, m0 in concept 0
PASS`.

K-FU3-3 PASS.

### K-FU3-4: feature cap is loud (D-T4)

One subject with 10 distinct features in one batch.

Result: concept formed with `nfeat=8` (8 features retained).
Raw output line 205:
`ULEARN concept: WARN feature cap 8 reached for subject [u]; 2
features dropped`. Raw output line 207:
`D-T4 10 features: nfeat=8 PASS`.

K-FU3-4 PASS.

### K-FU3-5: full regression

Parts A-C of the harness (the complete frozen H-FDCR-UNIFIED2
evidence: 23/23 suite plus K-FU2-1/2/3 fixtures) run unchanged on
the repaired mechanism. Lines 3-110 of the new raw output are
byte-identical (`diff`-verified) to lines 3-110 of the frozen
`FDCR_UNIFIED2_RAW.txt`, except the deliberately renamed banner
line 2. Final tally: `27/27` (23 frozen + 4 new), exit code 0.
No frozen outcome (train_con values, con_count, concept indices,
scores, winners) changed; the frozen fixtures never trigger caps,
so no WARN lines appear in their output.

K-FU3-5 PASS.

### K-FU3-6: determinism

Three consecutive runs byte-identical (cmp), md5
`ae29af93d28171c3e37bdca7bf4393b3`.

K-FU3-6 PASS.

## 4. Disclosed capacity limits (prereg R5)

All four concept-layer caps, now explicit rather than silent:

1. 16 facts per batch (parse array limit). Overflow: WARN, facts
   dropped, return np=16.
2. 8 features per subject accumulation (per-batch dedup array).
   Overflow: WARN per subject, features dropped.
3. 8 features per concept (concept feature slots). Extension
   overflow: WARN per concept, features dropped.
4. 8 members per concept (member index array). Overflow: WARN,
   subject NOT added as member, honest MATCH-NOADD emit.

The caps themselves were NOT enlarged; this repair makes them
loud, not larger. Enlargement or an eviction policy is future
work and remains an honest boundary for a continuing learner.

## 5. Remaining boundaries (not repaired, disclosed)

- Majority vote counts input occurrences, not distinct entities
  (X-FU2-1a informational boundary, within frozen spec).
- First-seen tie-break is unobservable under strict majority
  (dead disclosure, X-FU2-1b).
- `bcon` is a whole-bridge property, not checked against the
  firing sub-rule (X-FU2-3b informational boundary).
- Direct discovery fell through to bridge induction on the 4-pair
  all-reversal set (out of scope, flagged for the
  procedure-invention lane).
- Concept extension does not re-evaluate existing members against
  the enlarged feature set (H-FDCR-UNIFIED2 honest limitation,
  unchanged).
- The member-cap WARN fires once per skipped subject; a large
  batch produces one WARN line per skipped subject (verbose but
  truthful).

## 6. Governance disclosures

1. Prereg `PREREG_FDCR_UNIFIED3.md` committed as `ff25ebaab`
   strictly before any implementation edit or test run.
2. Implementation is a verbatim copy plus four preregistered
   edits; `unified_fdcr2.zag` untouched.
3. Pure Zag throughout: no Python in fixtures, harness, or
   analysis.
4. No em dashes in loop documentation (verified by grep).
5. Only owned paths committed; concurrent workers' files not
   touched. No binaries committed.
6. The raw evidence file is the unedited run-1 output
   (`FDCR_UNIFIED3_RAW.txt`).

## 7. Commit lineage and files

- Prereg: `PREREG_FDCR_UNIFIED3.md` (`ff25ebaab`)
- Implementation + harness: `unified_fdcr3.zag`
- Raw evidence: `FDCR_UNIFIED3_RAW.txt`
  (md5 `ae29af93d28171c3e37bdca7bf4393b3`, 3/3 byte-identical)
- This report: `FDCR_UNIFIED3_RESULT.md`

All under
`docs/lab/research-lead/overnight-20260928/`.

## 8. Verdict rationale

SURVIVES, 6/6. The three red-team downgrades are repaired at the
mechanism level, not the fixture level: the exact adversary
fixtures now pass, the caps are loud, and the misleading trace
line is gone. The full frozen evidence is byte-identical where it
must be. The residual caps remain as disclosed, explicit design
limits, not silent losses. An independent red team should now
attack H-FDCR-UNIFIED3 (recommended: cap-boundary behavior,
order-variation stress beyond two batches, eviction-policy
absence under member churn).
