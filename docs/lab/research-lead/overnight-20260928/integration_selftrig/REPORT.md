# REPORT: INTEGRATION-SELFTRIG (self-triggered revision in the live query path)

Date: 2026-10-03. Worker: INTEGRATION-SELFTRIG.
Lane: `docs/lab/research-lead/overnight-20260928/integration_selftrig/`
Prereg: commit a00f386cb (PREREG.md + NAMECHECK.md, committed alone
before any implementation file existed). Implementation commit
e2c1d737f; artifacts commit 557fd13c; this report follows.

## Verdict: SELF-TRIGGERED REVISION DEMONSTRATED (K1-K10 PASS)

The C455 integrated composer now revises its own bindings during
live operation. A drift injected between queries (world A facts
rewritten in a new order as world A2; relation vocabulary
unchanged) stales the learner's positional procedure indexes.
The next live queries disagree with the independent all-generic
oracles; the query path itself fires u_invalidate on the
spec-routing coverage contracts (judgment=1, consequence=0);
after two disagreeing attempts all three coverage clauses retire
and the third attempt falls back to generic routing with full
agreement; the next re-specialize sees the latched revision
request and revises each retired contract from fresh evidence
(revcount 1,2,3); spec routing is restored and the goals pass.
No demo stage chooses the contract, the evidence, or the timing:
the S9 demos are unchanged C455 code, and S10's invalidates fire
from do_query/execute_plan while its revises fire from
cov_induct under the latched request.

**Answer to the parent's question: yes, the composer can revise
its own bindings during live operation.** The full loop ran
autonomously: drift -> live disagreement -> self-fired
invalidates -> clause retirement -> generic fallback (goals
pass) -> latch-driven revise at re-specialize -> spec routing
restored (goals pass).

## What was built

- `st_base.zag`: byte-copy of integration_b1b2/ib_base.zag.
  cmp-verified identical.
- `st_world.zag`: ib_world.zag content (head cmp-verified
  identical) + `setup_worldA2` appended: the same 56 facts as
  world A (same vocabulary, same multiset) rewritten as 603
  block / 602 block / 601 block / distractors, so positional
  bucket indexes go stale while generic scans stay correct.
- `st_module.zag`: byte-copy of ib_module.zag. cmp-verified
  identical; the u_* bodies are untouched.
- `st_learn.zag`: ib_learn.zag + three frozen changes:
  (a) spec-refusal fallback in execute_plan: each spec call
  site checks for -1; on refusal it calls u_invalidate on
  that family's coverage contract (judgment=1,
  consequence=0) and falls back to the generic procedure so
  the query stays live; (b) `note_answer_disagree`: on live
  oracle disagreement with spec versions present, one
  u_invalidate per spec-routing family + RETRY line;
  (c) revise-on-retire in cov_induct: a previously committed
  contract with all clauses retired is revised via u_revise
  (request ensured latched) instead of fresh-inducted.
- `st_main.zag`: ib_main.zag + (a) do_query bounded
  self-correction (max 3 attempts; silent on first-try agree)
  and a C_Q tick (S slot 7) per query, (b) S10A-S10F stages
  on fresh composer state L2/S2, (c) `emit_revise` helper,
  (d) SUMMARY-DRIFT. S1A-S9 code unchanged.
- `st_full.zag`: concatenation (exactly one `fn main`).
- `st_build.sh`, `st_bin`, `st_compile.txt`,
  `st_run1/2/3.txt` (sha256
  6463c542f7687f61d4493f4085f09995430b6cfa3f70ddb0a427cf12e2286285
  x3) + `.err` (empty).

## Evidence (from st_run1.txt; runs 2/3 byte-identical)

K1 (base intact): the S1A-through-SUMMARY-DIAMOND lines and
the S9A/S9B lines are byte-identical to C455's ib_run1.txt
(diff clean, 63 lines).

S10B BASELINE (frozen values reproduced on fresh state):
- E0: st=2 vers=2,3,3,5 ans=7:1,611,0,1,611,1,2 agree=1
  cs=96 cg=336. R0: st=2 vers=2,3,5
  ans=6:1,613,1,613,1,2 agree=1 cs=64 cg=224.
- BCONTRACT: 801 (1,0,0,0), 802 (1,0,1,1), 807 (1,0,2,2),
  all active=1 dc=0.

S10D DRIFT-QUERIES (the self-trigger, live):
- E0 attempt 1: st=1 vers=2,3,3,5 ans=5:0,0,0,1,0 agree=0.
  (Stale 601-bucket: old indexes hold 603/602/601 facts whose
  objects never equal 621 -> need0 empty; oracle finds
  (611,601,621) -> [1,611].)
- RETRY att=1 dc=1,1,1 active=1,1,1 req=1 first=3.
  (Three live invalidates, one per spec family; the third
  latched the revision request with first_detect=C_Q=3.)
- E0 attempt 2: agree=0 (same stale answers).
- RETRY att=2 dc=2,2,2 active=0,0,0 req=1 first=3.
  (All three coverage clauses retired by the composer's own
  disconfirmation counts.)
- E0 attempt 3: st=1 vers=0,1,1,4
  ans=7:1,611,0,1,611,1,2 agree=1. (Retired clauses route
  generic; the composer self-healed without researcher help.)
- R0 (clauses retired): st=1 vers=0,1,1,4
  ans=6:1,613,1,613,1,2 agree=1. No invalidates needed.

S10E REVISE (latch-driven, at re-specialize):
- REVISE fam=ret olderr=0 revcount=1 nclause=(0,0,601,602)
  active=1.
- REVISE fam=vfy olderr=0 revcount=2 nclause=(0,0,601,603)
  active=1.
- REVISE fam=cnt olderr=0 revcount=3 nclause=(0,0,601,603)
  active=1.
Each re-specialize found its contract committed-but-retired
and called u_revise (not u_induct); the old clauses scored 0
errors on the fresh tables and re-inducted identically (the
drift preserved the vocabulary; the stale part was the
positional index, which specialize rebuilds); buckets are
fresh.

S10F RECOVER (goals still pass, spec restored):
- E0: st=1 vers=2,3,3,5 ans=7:1,611,0,1,611,1,2 agree=1
  cs=96 cg=336. R0: st=1 vers=2,3,5
  ans=6:1,613,1,613,1,2 agree=1 cs=64 cg=224.
- SUMMARY-DRIFT: agree=6 plans_built=2 plans_loaded=6
  trials=9 declines=0 cs=912 cg=2352.

## Kill bar assessment (observed vs frozen)

| Bar | Frozen | Observed | Result |
|-----|--------|----------|--------|
| K1 | S1A-S9 byte-identical to C455 | diff clean | PASS |
| K2 | S10B E0/R0 frozen lines | exact (st, vers, ans, agree, cs, cg) | PASS |
| K3 | E0 att1/2 agree=0 vers=2,3,3,5; RETRY dc=1,1,1 then 2,2,2; req=1 first=3 | exact | PASS |
| K4 | E0 att3 + R0 agree=1, generic vers, frozen answers | exact | PASS |
| K5 | REVISE olderr=0 revcount=1,2,3; clauses (0,0,601,602)/(0,0,601,603)/(0,0,601,603); active=1 | exact | PASS |
| K6 | S10F E0/R0 frozen lines | exact | PASS |
| K7 | 3/3 byte-identical, stderr empty | sha256 6463c542 x3; .err 0 bytes | PASS |
| K8 | safebin, no python, pure Zag, pinned znc | verified | PASS |
| K9 | zero em/en dash bytes; zero of 17 identifiers in st_learn/st_main | byte-verified clean | PASS |
| K10 | u_invalidate/u_revise only in the live-path sites + C455 S9 demos; no staged S10 calls | audit clean (see below) | PASS |

K10 audit detail: `grep u_invalidate` shows the four
execute_plan refusal-fallback sites (each inside its
`<0` guard), the three note_answer_disagree sites, and the
six unchanged S9 demo calls in st_main.zag (S9A/S9B, C455
code). `grep u_revise` shows cov_induct's retired-rule site
plus the two unchanged S9 demo calls. `grep
note_answer_disagree` shows the definition and exactly one
call site: do_query's retry path. No S10 invalidate/revise
call exists outside the live query path or the latch rule.

## Falsification criteria (frozen; none fired)

- F1 (S1A-S9 differs from C455): NOT FIRED (diff clean).
- F2 (E0 drift attempt 1 agrees): NOT FIRED (agree=0,
  ans=5:0,0,0,1,0 as hand-derived).
- F3 (attempt 3 disagrees): NOT FIRED (agree=1).
- F4 (REVISE lines differ): NOT FIRED (exact).
- F5 (S10 invalidate/revise outside live path/latch rule):
  NOT FIRED (audit clean).

## Implementation defects caught by testing (errata)

Two defects were found during the build/run cycle and fixed
before the frozen runs; both are disclosed:

D1 (Zag keyword as parameter name): the new `emit_revise`
helper declared its name parameter as `fn`, which is a Zag
keyword; znc rejected the file with E0001. Renamed to `fam`;
no scientific impact (compile-time only).

D2 (first_detect never stamped): the frozen prereg predicted
first=3 on the RETRY lines, but the first runs showed
first=0. Root cause: u_invalidate stamps slot 908 only when
908<0 (verbatim module behavior), and fresh S2 has 908=0.
Fixed by presetting ss(S2,908,-1) at S10A start, exactly as
the S9 demos do (ss(S,908,-1)); the module is untouched.
The frozen runs show first=3 as predicted. This was an
implementation fix to meet the frozen prereg, not a prereg
amendment.

Neither defect touched the S1A-S9 path.

## What this establishes (and does not)

Establishes: revision is no longer staged. The composer
observes its own query outcomes (spec refusal internally,
oracle disagreement in the live per-query path), fires
u_invalidate itself, retires its own stale clauses, falls
back to generic routing (goals keep passing), and revises
via the latched request at the next re-specialize (the
natural composer operation, not a demo driver). The S9B
drift pattern (stale contract -> probes -> re-log ->
revise) now runs end-to-end without researcher staging of
the revision steps, which was C455's open thread 1 and the
parent's follow-up 2.

Does not establish: B1 (binding-contract) self-triggering
under drift (need shapes do not drift with the world, so the
binding contracts faced no counterevidence; B1 revision
remains S9A-demonstrated only); spec-refusal triggering in a
live battery (the fallback is wired and audited but dormant:
no working-set/contract divergence occurred, so Trigger A
did not fire; disclosed); revision when the re-inducted
clause must change shape (the drift preserved the
vocabulary, so the revise re-derived identical clauses);
scaling beyond the tested sizes.

## Architecture accounting

- Cognition lines added: st_learn.zag delta vs ib_learn.zag
  is the refusal fallback (4 sites), note_answer_disagree,
  and the revise-on-retire rule in cov_induct (net about
  +100 lines, all generic machinery); st_main.zag delta is
  the do_query retry loop, C_Q tick, emit_revise, and the
  S10 driver stages (apparatus, disclosed); st_world.zag
  delta is setup_worldA2 (environment, disclosed).
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- New opcodes/behavior classes/edge types: 0.
- Researcher-owned: the wiring, the S10 driver, the drift
  injection, the prereg.
- Learner-owned (in L2/S2 state): disconfirmation counts,
  retired-clause markings, the latched revision request,
  revision counts, re-derived clauses, rebuilt buckets,
  plans. Every S10 revision is a learner-state transition
  driven by observed query outcomes.
- Pinned znc 2026.07.0-dev via safebin.

## Toolchain guard

Step 0 executed at startup and recorded in NAMECHECK.md:
PATH=$HOME/safebin; `which python3` and `which python`
return nothing. (Note: the safebin_setup/setup_safebin.sh
script referenced by the C455 lane does not exist at that
path on this machine; the safebin itself is present and was
used directly; recorded in NAMECHECK.md.) Zero Python
computation; all builds used the pinned znc; all runs were
the compiled binary; all text processing was shell tools.
Git writes via /usr/bin/git absolute path (safebin git has
the known EPERM-on-write defect); explicit pathspecs on
every commit; index.lock contention retried with backoff per
AGENTS.md (never removed); nothing pushed.

## Disclosed bounds (not claimed)

- The drift itself is researcher-injected (the world is
  rewritten between queries); what is self-triggered is
  everything after: detection, invalidate, retirement,
  fallback, and revise. The S9 demos remain staged
  (unchanged C455 code).
- Trigger A (spec refusal) is wired but dormant in S10; the
  live firing demonstrated is Trigger B (oracle
  disagreement). The oracle is the independent reference;
  using its verdict as the consequence signal is the
  preregistered design (the world telling the composer it
  was wrong).
- The revise re-derived identical clauses (vocabulary
  preserved); the binding change was the retirement and
  re-derivation, plus the bucket rebuild.
- One battery, two C433 goals under drift (E0 diamond, R0
  chain), frozen worlds. No broad generality claim.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/integration_selftrig/`:
PREREG.md (frozen, commit a00f386cb), NAMECHECK.md (Step 0),
st_base.zag, st_world.zag, st_module.zag, st_learn.zag,
st_main.zag, st_build.sh, st_full.zag (assembled; exactly one
`fn main`), st_bin, st_compile.txt, st_run1/2/3.txt (+ .err,
empty), REPORT.md (this file). Commits: a00f386cb (prereg
alone), e2c1d737f (implementation), 557fd13c (artifacts +
runs); REPORT commit follows. All local, never pushed.

## Recommended follow-ups (for the parent, not decided here)

1. B1 self-trigger: construct a drift that changes need
   shapes (not world facts) so a binding contract faces live
   counterevidence; test whether bind_fam revision
   self-triggers.
2. Spec-refusal live firing: engineer a working-set/contract
   divergence without researcher half-clearing (e.g. a drift
   that removes a rel from the vocabulary while episodes
   keep it in the working set, then a re-induct that
   over-admits); verify Trigger A fires and falls back.
3. Clause-changing revise: drift the relation vocabulary
   itself (not just fact order) and test whether the
   latch-driven revise corrects the clause shape, not just
   re-derives it.
4. Remove the oracle from the loop: replace the
   disagreement trigger with a learner-owned consequence
   (e.g. downstream need failure, user correction) while
   keeping the invalidate/revise machinery.
