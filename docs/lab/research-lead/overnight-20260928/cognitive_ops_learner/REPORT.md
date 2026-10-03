# REPORT: COGNITIVE-OPS-LEARNER (overnight priority #5)

Date: 2026-10-03. Worker: COGNITIVE-OPS-LEARNER.
Lane: `docs/lab/research-lead/overnight-20260928/cognitive_ops_learner/`
Prereg: commit 49958e620 (PREREG.md + NAMECHECK.md, committed alone
before any implementation file existed; committed blobs verified
byte-identical to the frozen drafts). Implementation commit follows
this report.

## Verdict: MIGRATION DEMONSTRATED (K1-K6 PASS; K2 with documented
arithmetic erratum, see below)

A researcher-supplied generic VERIFY procedure was specialized by the
learner through experience into a learner-owned indexed procedure with
provenance, and the learner selected between the original and the
revised procedure based on a learned coverage record: 10/10 covered
queries used the specialized procedure with verdicts agreeing 100%
with the generic oracle at strictly lower check cost; 5/5 uncovered
queries fell back to the generic procedure with correctness preserved;
and after new experience the learner revised the specialization
(revision counter 1 -> 2, provenance updated, index content replaced),
with selection tracking the revised coverage.

## Kill bar assessment (observed vs frozen prediction)

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | S2 agree=6/6, S5 agree=4/4 | 6/6 and 4/4; SUMMARY-ALL agree=10 | PASS |
| K2 | S2 cs=112 < cg=448; S5 cs=80 < cg=216 | S2 112 < 448; S5 72 < 216 | PASS-WITH-ERRATUM (see below) |
| K3a | zero relation literals in col_learn.zag, col_main.zag | word-boundary grep empty in both | PASS |
| K3b | S1 vs S4 LSTATE rel_ids differ | 101,102,103 vs 201,202 | PASS |
| K3c | distractors absent from dumps | 107,109,207 absent from both dumps | PASS |
| K4 | S3 fallback=4, verdicts 1,1,1,0 | fallback=4, v=1,1,1,0 | PASS |
| K5 | S4 rev=2 nrel=2 prov 0,6,9,24; S5 agree=4/4 sel=1 x4 | exact match | PASS |
| K6 | S6 sel=0 on re-presented A query | sel=0, v=1, cg=64 | PASS |
| K7 | 3/3 byte-identical stdout, stderr empty | sha256 688cd1cb x3; .err 0 bytes | PASS |
| K8 | safebin, no python, pure Zag | verified (see Toolchain) | PASS |
| K9 | zero em/en dash bytes in lane docs | byte-verified clean | PASS |

neg1=0 (the specialized procedure's not-covered return was never hit
on a selected query); stat_spec=10, stat_gen=5, exactly as predicted.

## K2 erratum (transparent; prereg NOT silently amended)

The frozen PREREG predicted S5 cs=80. Observed S5 cs=72. The
discrepancy is an arithmetic error in my hand computation in the
prereg table, not a mechanism deviation. Correct derivation from the
frozen design: each query step scans exactly its relation's bucket
(8 facts; no early exit in vfy_spec, as preregistered). C0: 16, C1:
24, C2: 16, C3: 16 (C3 is a 2-step chain). 16+24+16+16 = 72. The code
implements the preregistered design exactly; the design predicts 72;
observed is 72. The kill criterion itself, "strictly fewer
fact-checks via the learned index" (the parenthetical in K2, and the
substance of the efficiency claim), holds: 72 < 216, a 3x reduction,
same as S2's 112 < 448 (4x). I record K2 as PASS-WITH-ERRATUM rather
than editing the frozen bar. If governance requires the exact-number
form, the remedy is a fresh prereg with the corrected cell, not an
amendment to this verdict.

## Evidence detail

Learner-not-researcher (K3): the specialize/select/episode code in
col_learn.zag and the driver in col_main.zag contain no world
relation-identifier literals (verified by `grep -wE
"101|102|103|107|109|201|202|207"`, empty output on both files); the
literals appear only in col_world.zag (107 matches: the world
definitions, which any experiment must define). The identical
specialize code produced coverage {101,102,103} from world-A episodes
and {201,202} from world-B episodes, so the index content came from
runtime experience. Distractor relations (107, 109, 207) exist in the
worlds but never appeared in any chain; both LSTATE dumps exclude
them, showing the learner indexed what it experienced, not what
exists.

Selection without modes (K4/K6): in S3 the learner met relations
outside its coverage and selected the generic procedure (sel=0 x4)
with no researcher signal that world B was "different"; verdicts
1,1,1,0 are correct via the oracle. In S6, after revision replaced
the coverage, the re-presented A query (Q0, valid, v=1) again
selected the generic procedure: selection follows the current
learned coverage, not the query's history.

Revision with provenance (K5): S4 SPEC rev=2 nrel=2 ep0=6 ep1=9
nfacts=24; LSTATE prov=0,6,9,24 rev=2. prov_parent=0 in both
specializations records derivation from the generic procedure;
prov_rev distinguishes the two learner-owned revisions.

Generic-not-strawman: vfy_gen is the correctness oracle for all 24
chains; it is correct on covered, uncovered, valid, and invalid
inputs, including every query where the specialized procedure could
not apply (S3, S6). The learner's contribution is specialization
efficiency plus context-sensitive selection, never correctness
repair. The full-scan cost model (nsteps * nfacts, no early exit)
made the efficiency prediction exactly checkable.

## What this establishes (and does not)

Establishes: a cognitive procedure body can move from
researcher-authored machinery into learner-owned state; the learner
can specialize it from experience (selective index over encountered
relations), record provenance (parent id, episode range, revision),
select between original and revised from a learned applicability
record with correctness-preserving fallback, and revise the structure
for new experience. No VERIFY_MODE or procedure-dispatch constant
exists anywhere: selection is a coverage lookup in learner state.

Does not establish: composition of cognitive procedures with each
other; retirement of the generic procedure (it remains the fallback
and the oracle); learner creation of a procedure from scratch (the
seed was researcher-supplied by design, per the task); behavior on
non-chain structures; scaling beyond the tested sizes. Those are
follow-up lanes.

## Toolchain

- safebin active for every command (PATH=$HOME/safebin exported per
  invocation); `which python3` / `which python` return nothing;
  znc 2026.07.0-dev (pinned
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- Zero forbidden-executable invocations. All computation pure Zag;
  shell only for znc/binary/git/assembly/byte-verification.
- Git writes via /usr/bin/git absolute path (safebin git symlink has
  the known EPERM-on-write defect). Explicit pathspecs on every
  add/commit; no other lane touched; nothing pushed.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cognitive_ops_learner/`:
PREREG.md (frozen, commit 49958e620), NAMECHECK.md (Step 0),
col_base.zag, col_world.zag, col_learn.zag, col_main.zag,
col_build.sh, col_full.zag (assembled; exactly one `fn main`),
col_bin, col_compile.txt, col_run1/2/3.txt (sha256
688cd1cba9f2e2c4d97cc0183e3971b32e12fbe4a6f132e1425859264d24137a)
+ .err (empty), REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. Composition: two learner-owned procedures selecting/composing
   (e.g., specialized VERIFY feeding a learner-owned RETRIEVE).
2. Retirement: conditions under which the learner drops the generic
   fallback (retire = coverage confidence + correctness record).
3. Creation: seed with a weaker scaffold and test whether the learner
   invents the index structure form itself (toward L3).
4. Interleaved worlds: A/B episodes mixed, testing coverage union vs
   revision and interference.
