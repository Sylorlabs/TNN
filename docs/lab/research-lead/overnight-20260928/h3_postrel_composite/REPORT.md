# REPORT: H3-POSTREL-COMPOSITE (post-release genuine composite probe)

Date: 2026-10-03. Worker: H3-POSTREL-COMPOSITE worker (non-ledger
task; claim minting paused).
Prereg: committed alone as ef1c4ba15 (strictly before
implementation, build, and runs). No amendments.

## Verdict: POSTREL-COMPOSITE-PASS (P0..P5 all hold)

3/3 runs byte-identical (sha256
dd0524c3b6a520b392bb99822d410cd5a85a9cce685825a593fd87ec35085e17).
Binary sha256
23f004f418cb06b993fbd11cb7d0dae71c5cb2bced713e526a47c604b630838f.

The H3-RELEASE-CHURN suggested next probe is EXECUTED. The
answer: debris is not special. A genuine absorbing composite
installed after the release decision re-creates the hazard
(W10: rel=8, haz=8) with zero churn mechanics involved (cf=8 --
the reference arrives through a pure install_composite direct
slot write, no mem_write, no conflicts, no displaces). The hazard
definition is installation-path-blind: any live pooled entry
whose value matches a released trace key fires the hazard,
regardless of whether it arrived as churn debris or as a genuine
composite, and regardless of when it was installed relative to
the release decision.

## Results (identical across run1/run2/run3)

| cond        | cf | ev | drop | rel | av | ai | ar | lc | haz | trs      |
|-------------|----|----|------|-----|----|----|----|----|-----|----------|
| POSTCOMP-W10| 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 8   | 22222222 |
| POSTCOMP-W11| 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 22222222 |
| POSTCOMP-W12| 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 4   | 22222222 |

Every measured row matches the frozen prereg predictions exactly.
The 48 pre-existing COND lines (45 from h3_guarded_sealed +
CHURN-W7/W8/W9 + POSTREL-W10/W11/W12) are byte-identical to
h3_release_churn/run1.txt, and the in-band
GUARDED-SEALED-VERDICT=PASS, CHURN-INTERACTION-VERDICT=PASS, and
RELEASE-CHURN-VERDICT=PASS still hold, so the genuine-composite
worlds caused no regression.

Kill bars (in-band + external, all 3 runs):
- P0 IDENTITY: HOLD. diff of run1.txt against
  h3_release_churn/run1.txt shows ONLY the expected differences:
  the LANE= tag line, the 3 new COND=POSTCOMP-W1[012] lines, and
  the new P1..P4 + POSTREL-COMPOSITE-VERDICT= lines. All other
  75 lines byte-identical. 3/3 runs byte-identical. diff of
  h3_postrel_composite.zag against
  h3_release_churn/h3_release_churn.zag shows only the frozen
  delta in 7 hunks: lane header/tag, LANE= tag, chw-mode comment
  block, 3 new chw modes, 3 main call sites, P1..P4 checks,
  verdict line. Not VOID.
- P1 W10-GENUINE-POSTREL-HAZARD: HOLD (rel=8, haz=8, av=8, ai=0,
  cf=8, ev=0, drop=0, lc=12, trs=22222222). At consolidate time no
  live reference existed, so the guard released all 8 (correct
  per its decision-time precondition). Eight genuine composites
  (keys 8001..8008, values 905001..905008) were then installed
  via install_composite into first-free pool slots 8..15 -- no
  mem_write, no conflicts (cf stayed 8), no churn mechanics at
  all -- and count_hazard measured after the installation fires
  on all 8 trace entries. A real structure referencing released
  memory re-creates the hazard.
- P2 W11-GENUINE-NOREF-SAFE: HOLD (rel=8, haz=0, av=8, ai=0,
  cf=8, ev=0, drop=0, lc=12, trs=22222222). Post-release genuine
  composite installation with non-colliding values
  (905021..905028, implying k in 5021..5028) creates no hazard:
  genuine composite installation per se is inert; only value
  collision matters.
- P3 W12-PARTIAL-REFERENCE-GRANULARITY: HOLD (rel=8, haz=4, av=8,
  ai=0, cf=8, ev=0, drop=0, lc=12, trs=22222222). Four genuine
  composites matching the first 4 released keys only produce
  haz=4: the hazard counts exactly the referenced trace entries.
  Per-entry value matching, not systemic contamination.
- P4 CLEAN: HOLD (ai=0, ar=0 in W10/W11/W12; lc=12 all three;
  av==rel in all three).
- P5 DETERMINISM: HOLD (3/3 byte-identical).

In-band POSTREL-COMPOSITE-VERDICT=PASS in all 3 runs; the
governing verdict is this external check.

## The frozen hazard definition against genuine post-release references

1. Debris is not special. The parent's POSTREL-W10 (churn debris,
   cf=16, haz=8) and this lane's POSTCOMP-W10 (genuine
   composites, cf=8, haz=8) yield the same hazard count with the
   same reference values and the same candidate keys. The only
   difference is the installation path
   (mem_write/conflict/displace/relocate debris vs
   install_composite direct first-free-slot write). The hazard
   definition is installation-path-blind.
2. The canonized guard (`learner_consolidate` + `has_live_ref`)
   remains a DECISION-TIME predicate. It cannot see references
   installed after the release decision regardless of how real
   the referencing structure is. Proven by P1: a genuine
   composite, the canonical real-structure path, was installed
   after a guarded-correct release and the hazard re-materialized
   anyway.
3. The hazard is per-entry value matching, not systemic
   contamination. Proven by P3: 4 references installed -> exactly
   4 trace entries fire. A composite install does not poison the
   pool; it fires only for the keys it references.
4. Composite installation per se is inert. Proven by P2 vs P1:
   identical genuine-composite installation, values colliding vs
   not -> haz=8 vs haz=0.
5. The ordering matrix for genuine composites is now closed:
   genuine references BEFORE the decision block (parent CHURN-W7:
   rel=0); genuine references AFTER the decision re-create the
   hazard (P1: rel=8, haz=8). Ordering is the only variable.

Consequence for the canonized gate: no change is proposed or
needed. The gate behaves exactly as specified in all three
genuine-composite worlds. The new frozen consequence: because
even the canonical real-structure path (install_composite)
re-creates the hazard after release, any future substrate that
needs post-release safety cannot distinguish "real structures"
from debris at the hazard level -- the hazard definition does
not. It must re-check at use time, pin released entries against
reference installation, or track references genuinely
(provenance). This lane extends the parent's frozen consequence
from the pre-decision case to the genuine-composite
post-decision case: genuine reference tracking was already open
from H3-GUARDED-SEALED; nothing in this lane weakens or
strengthens that option, and nothing here fixes the gate (test
only, per the task constraint).

## What this establishes

1. A real structure referencing released memory re-creates the
   hazard. The parent's W10 left open whether debris mechanics
   were load-bearing; P1 answers no.
2. The hazard definition against genuine post-release references
   is: haz fires per released trace entry whose key is
   value-matched by any live pooled entry at measurement time,
   irrespective of installation path and irrespective of install
   time relative to the release decision.
3. The cleanest form of the post-release hazard needs no churn
   at all: P1's cf=8 is a pure reference-installation hazard,
   which makes the value-match mechanism undeniable (no
   conflict/displace confound to hide behind).

## Honest caveats

- The adversary is the worker in a second hat (same procedural
  seal as the parent lane), not a second mind. W10/W11/W12 were
  specified in the prereg before implementation.
- The learner remains simulated; reason codes are harness-written.
- "Genuine" means the canonical install_composite path
  (first-free-slot pooled entry, byte-identical to the parent's
  W7/W12 genuine pre-decision references) rather than churn
  debris mechanics. The composite values are still
  adversarially assigned by the harness, not learner-created; a
  learner-authored reference body remains untested.
- Non-ledger task: no claims minted.
- The guarded consolidate was NOT modified in this lane (test
  only, per the task constraint).

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which
python` return nothing under that PATH (verified 2026-10-03 before
the prereg commit); no forbidden executable invoked at any point
(shell used only for mkdir, file writes, znc invocation, binary
execution, sha256sum, cmp, diff, grep, git ops). No
PROCESS-FAIL condition triggered. Pinned znc verified
byte-identical to src/tools/toolchain/znc_linux_x86_64_abed8aa1
before the prereg commit (sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
Build ran in foreground (zagd unavailable warning only), first
try, no defect symptoms; `-o h3_postrel_composite_bin` used for
the output name. New-code audit: no negated-conjunction while
conditions, no `as *i32` slice construction, no `[]u8 as *u8`
casts in new code, zero `!(` in the added diff hunks, if-nesting
at most 2 in new code. Git writes via /usr/bin/git directly
(safebin git symlink EPERM lesson); explicit pathspecs; no git
reset; local only, never pushed.

## Commits

- ef1c4ba15: frozen prereg (PREREG.md + NAMECHECK.md), alone,
  strictly before implementation, build, and runs.
- This commit: h3_postrel_composite.zag (source sha256
  43ce61dc5050c2821309785054b9eec5bd84d545e01dcbd3f4c53d10bd54b308;
  diff against h3_release_churn/h3_release_churn.zag shows
  only the frozen delta in 7 hunks), h3_postrel_composite_bin
  (sha256
  23f004f418cb06b993fbd11cb7d0dae71c5cb2bced713e526a47c604b630838f),
  build.err, run1/2/3.txt, run1/2/3.err, REPORT.md. Local only,
  never pushed.

## Follow-ups for the parent

- The H3-RELEASE-CHURN suggested next probe is CLOSED: the
  genuine-composite post-release ordering is frozen and verified
  (POSTREL-COMPOSITE-PASS P0..P5). Debris is not special; the
  hazard definition is installation-path-blind and per-entry
  value-matching.
- The guard's protection is decision-time only, and this now
  holds against the canonical real-structure path, not just
  churn debris. If any future substrate requires post-release
  safety, the options remain: re-check at use time, pin released
  entries against reference installation, or genuine reference
  tracking (provenance). This is a design question for the
  parent, not a defect in the canonized gate.
- Natural next probes (not started): (a) a learner-authored
  reference body (values the learner itself chose) installed
  post-release, to test whether hazard behavior changes when
  intent is learner-owned; (b) post-release composite
  installation followed by a second guarded consolidate decision
  (does re-checking at a later decision catch it -- rel stays 8
  but what happens to the trace?); (c) eviction of the
  post-release composite (does haz clear when the reference is
  removed -- the state-predicate reversibility test).
