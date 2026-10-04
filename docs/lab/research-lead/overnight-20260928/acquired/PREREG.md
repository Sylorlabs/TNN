# PREREG -- ACQUIRED-CAPABILITY (ACQ), ids C770-C789

Lane `acquired/`. This prereg is committed ALONE, before any implementation
file exists. Frozen after this commit. Kill bars below do not move.

Refs: judge brief (ACQ mission), ZAG_LANGUAGE_AND_WORKER_BRIEF sections 1, 3,
4.0, 4.1, 5, 7, 10. RESEARCH_DATA sections 4 and 17.

## 0. THE CLAIM UNDER TEST

There exists a capability whose utility is CAUSALLY ACQUIRED from the
experience stream (the query sequence), such that the same frozen source with
the same final fact set, given the same compute budget, CANNOT reconstruct it.

Concretely: a LEARNED HOT-RELATION COLUMN INDEX.

* Fact store: N=96 facts over R=16 relations (ids 1..16), relation r having
  rows_r triples. Hot relations are NOT the largest; hotness is a property of
  the QUERY STREAM, not of the fact table.
* Query: RET(rel,obj) = set of subjects s with (s,rel,obj) a fact.
  Answered generically it costs N fact-checks (ret_gen scans the whole store).
  Answered through a learned column copy of relation r (a contiguous copy of
  r's rows) it costs rows_r checks. The column copy is EXACTLY r's rows, so
  its answer is always identical to ret_gen (correctness is by construction,
  verified per query; see kill bar K1).
* The learner's persistent state is: (a) the frequency table over relation
  ids gathered during the query stream, (b) the HOTSET manifest (top-K=3
  relation ids by observed frequency, with a validation rule), (c) the three
  column copies (K=3 slots, each costs N checks to build).
* The hotset is NOT derivable from the fact table: it is a function of the
  query stream. A fresh copy holding only the final facts cannot know it.

## 1. ARMS AND METRICS

Every arm answers RET queries; correctness is checked per query against
ret_gen (oracle-style, cost of the check itself NOT counted toward the
budget). Budget counter `T` counts fact-checks: one per store row scanned.
All modes byte-deterministic, asserted 3/3 by tools/zbuild.sh --rep 3 and
the tnnwatch watchdog.

Worlds (all inline, fixed):
* W1: 96 facts, R=16 relations. rows_r: hot {3,7,11} have 4,5,6 rows;
  the other 13 relations share the remaining 81 rows (some large).
* W2: structurally related to W1: same 16 relation ids, same hot-set ids
  {3,7,11}, different subjects/objects (different row counts ok).
* W0: a PRIOR-WORLD used only for the misleading-prior arm: same schema,
  its stream's hot set is {4,8,14} (similar shape, wrong for W1).

Streams (fixed, inline): S1 (W1 training): 48 queries, 80% on {3,7,11},
20% spread over the other 13. S2 (W1 reuse): 30 queries, same 80/20 split.
S3 (revision): S1 but at episode 24 the hot set shifts to {2,5,9}.
S4 (W2): 30 queries on W2, 80% on {3,7,11}.

Metrics per arm: T_train_build (budget spent learning+building),
T_reuse (budget over S2-equivalent), HIT (fraction of S2 queries answered
through a column), CORRECT (per-query equality vs ret_gen, must be 1.0),
REVISION_DETECTED (probe misses before rebuild), PRIOR_USED (1 if the
misleading prior was actually used for answering on W1).

## 2. THE SIX REQUIRED TESTS (kill bars)

T1 LEARNED-STRUCTURE ERASURE. Arm E: train on S1, then DELETE only the
learner-owned state ((a)-(c) zeroed/wiped). T_reuse_E MUST be >= 0.95 *
T_reuse_generic (column advantage collapses). If T_reuse_E ~= T_reuse_trained
then the structure was not load bearing: FAIL.

T2 FACTS-ONLY RECONSTRUCTION. Arm F: fresh process, final facts only, NO
stream. F implements two honest policies: F-noindex (never build
columns), F-largest (build columns for the K=3 LARGEST relations -- a
fact-derivable heuristic). F's T_reuse MUST be >= 2x T_reuse_trained.
If F-largest or F-noindex matches T_reuse_trained, then "learning" was
just reprocessing facts: FAIL.

T3 MATCHED COMPUTE. Arm G: fresh process, final facts, compute budget
T_train_build from the trained arm (same number of fact-checks), still NO
stream. With that budget G can build at most K' = floor(budget/N) column
copies by GUESSING their relation ids (it cannot know the hot set). Its
HIT on S2 MUST be <= 0.6 (vs trained 1.0 for hot-delivered queries) and
its T_reuse >= 2x T_reuse_trained. Move any bar: VOID.

T4 TRANSFER. Arm X: on W2, prior arm imports the W1 hotset {3,7,11}
(selection only, rebuilds columns from W2 facts, cost N per column) and
its T_reuse_X2 MUST be < 0.5x T_reuse_noprior (cold queries only after
one build phase). The advantage must come from the IMPORTED SELECTION,
not from reprocessing W2 facts (the no-prior arm on W2 sees the same
facts; it does not have S4 before its reuse window).

T5 LATER REUSE. Arm L: 16 cold queries interleaved between training and
S2. Trained hotset+columns must still answer S2's hot queries via
columns (HIT on hot queries = 1.0, T_reuse comparable to no-interleave).
If the capability only fires immediately after training: FAIL.

T6 REVISION + MISLEADING PRIOR. Arm R: stream S3. The learner must
DETECT the shift (probe: recent-window column-hit fraction < 0.5 triggers
rebuild from the window's frequency table) and rebuild; its total budget
over S3 MUST be < 0.7x the no-revise fixed-hotset arm. FAIL otherwise.
Arm M (misleading prior): seeded with W0's hotset {4,8,14}. The learner
must validate it (8-query probe on W1 stream: every probe query misses
the imported columns), REJECT the prior (wipe, rebuild from S1), and end
with CORRECT=1 and T_reuse comparable to fresh-trained. A blind-import
variant (never validates) is reported as the failure contrast.
PRIOR_USED must be 0 for the validated learner. K6 FAIL if the learner
keeps the prior or the probe cannot distinguish it.

## 3. STUPID BASELINES (mandatory)

B-noindex, B-largest (K=3 largest relations by row count), B-recency (K=3
relations seen most recently, window 8 queries). All baselines are
deterministic functions available to a fresh copy; each is run through the
same metric counters and its T_reuse/HIT is reported alongside trained.

## 4. IMPLEMENTATION DISCIPLINE

* Zag only for computation; driver code may read only the fact table, the
  query stream (when entitled), and learner-owned tables. The FRESH arm
  code path must never reference the frequency table or HOTSET manifest
  (kill bar K-N, grep-enforced).
* No `[]u8 as *u8`; use `_zag_slice_ptr`. get32/set32 use BYTE offsets as
  in cf2_base. Output via o_flush with `_zag_print`. No `for` loops.
  if-nesting <= 3. Exactly one `fn main(`.
* Do NOT use compose_iter (5-need heap corruption). Do NOT use
  _zag_raw_syscall for output.
* Determinism: every run 3/3 byte-identical stdout via tools/zbuild.sh
  --rep 3. Watchdog: `$W reg acq 900 ./<bin>` for every run.

## 5. KILL BARS (HARD)

* K1: any column-derived answer differs from ret_gen on any query: HARD
  FAIL, the apparatus is a bug, not a result.
* K2: non-determinism (any two of three runs differ): HARD FAIL.
* K3: T1 erasure does not collapse the advantage: FAIL.
* K4: F-largest matches trained T_reuse: FAIL (facts reconstruct it).
* K5: G's T_reuse <= 1.5x trained with matched budget: VOID (reprocessing).
* K6: validated learner imports the misleading prior without rejection:
  FAIL.
* K7: transfer arm shows no advantage over no-prior on W2: FAIL.
* K8: revision arm never rebuilds on S3: FAIL.

## 6. SUBSTRATE SCOPE (three-way separation)

(i) IMPLEMENTATION CORRECTNESS: does the column copy answer equal ret_gen
(K1)? (ii) ARCHITECTURAL CAPABILITY: can the frozen substrate (flat fact
arena + generic procedures + driver worlds) express a learned column
index with erasable state? (iii) LEARNER-ACQUIRED CAPABILITY: did the
hotset actually come from the query stream (arm G/F falsifiers), not from
source constants or fact-derivable structure? The report must keep these
three separated and must not claim L3 (L3 stays zero pending Criterion 0).

## 7. PRIOR NEGATIVE MARKERS TO RESPECT

`famv=0112` fixed by shape in every p1falsifier arm incl. empty arena;
frozen-core `compose_iter` has no read-only novice path (corefreeze2).
We therefore do NOT claim the frozen policy core learns; we claim a
driver-level acquired capability over the frozen generic procedures
(ret_gen/vfy_gen/cnt_gen from c15_base semantics), which is the narrowest
honest locus. Report must say this explicitly in BOUNDARIES.

## 8. ERRATA ERR-1 (issued before implementation)

Fact-table fixture numbers adjusted: N=141 facts over R=16 relations with
per-relation row counts r3=20, r7=20, r11=20 (hot set {3,7,11}), and
r1=16, r2=14, r4=12, r5=10, r6=8, r8=7, r9=6, r10=4, r12=2, r13=1,
r14=0, r15=0, r16=1. This keeps the hot set MEDIUM-sized (20 rows) so no
size-only heuristic (largest or smallest) recovers it, while a column on a
hot relation is still ~7x cheaper than the generic full scan (20 vs 141).
Budget counter N in section 0 now means N=141.
