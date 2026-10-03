# REPORT: INTEGRATION-STRESS (adversarial stress of the integrated B1/B2 composer)

Date: 2026-10-03. Worker: INTEGRATION-STRESS.
Lane: `docs/lab/research-lead/overnight-20260928/integration_stress/`
Prereg: commit dfd2b7e28 (PREREG.md + NAMECHECK.md, committed alone
before any implementation file existed). Implementation commit
28c85d161; artifacts commit b9ec61de1; this report follows.

## Verdict: STRESS SURVIVED (K1-K10 PASS)

The integrated B1/B2 contract layer holds under all four
adversarial tracks. The composer degrades gracefully under every
stressor: stale contracts fail visibly (a wrong answer end-to-end,
or routing that degrades to abstention/decline), never as silent
misrouting that revision cannot repair. Revision fires exactly per
the consecutive-failure semantics, and end-to-end query agreement
is restored after revision in both recovery tracks. Two
integration findings are frozen: (a) plans cache the bound fam at
build time, so binding revision requires a plan rebuild to take
effect (IS-D); (b) two consecutive spurious failures retire a
clause (routing degrades) before the 3-fail revision request
latches (IS-C).

## What was built

- `is_base.zag`: byte-copy of integration_b1b2/ib_base.zag.
  cmp-verified identical.
- `is_module.zag`: byte-copy of integration_b1b2/ib_module.zag
  (the u_* contract module verbatim). cmp-verified identical.
- `is_world.zag`: ib_world.zag + `setup_worldC1` (28 facts):
  rel 701 new (15 facts; fact 0 carries obj 621, world A's first
  601-object, engineering a stale-bucket collision); rel 601
  survives with 8 new facts; rel 707 distractor; rel 602 retired
  (no facts). Vocab scan order [701,601,707]. Literals live only
  in this file, per the C433 convention.
- `is_learn.zag`: ib_learn.zag + two generic helpers (no
  identifiers): `ret_buckets_rebuild` (rebuilds RET buckets on
  the current world without touching the coverage contract) and
  `first_subj` (subject analog of first_obj).
- `is_main.zag`: new driver. IS-SETUP (episodes, specializes,
  diamond E0, BCONTRACT dumps) + four stress demos. All demo
  values runtime-derived (tags from the directory, rels from
  clause reads and vocab scans, objs/subjs from fact scans,
  goal tags derived arithmetically from a constructed goal's
  runtime tag). New oracles oracle_1ret/oracle_1vfy (single-need
  all-generic references); do_query extended with okind 2/3.
- `is_full.zag`: concatenation (exactly one `fn main`).
- `is_build.sh`, `is_bin`, `is_compile.txt`,
  `is_run1/2/3.txt` (sha256
  2f7b20b7c477f522ddbbe82a6b4ebcc8928c8a3681aae559413126d5a98f712d)
  + `.err` (empty).

## Evidence (from is_run1.txt; runs 2/3 byte-identical)

IS-SETUP (frozen anchor): E0 `st=2 vers=2,3,3,5
ans=7:1,611,0,1,611,1,2 agree=1 cs=96 cg=336`; BCONTRACT
801 -> (1,0,0,0), 802 -> (1,0,1,1), 807 -> (1,0,2,2), all
active=1 dc=0; LSTATE lines identical to the integration
battery's S1A-S1C.

IS-B OSCILLATE (B2 thrash): four A->B->A->B->A revisions on the
live RET contract. ISB-R1..R4: olderr=4 each, revcount=1..4,
clauses alternate (0,identity,[701,702]) / (0,identity,[601,602])
exactly, routing verified each cycle; ISB-CNT total=12
correct=0 revcount=4 first=500 olderr=4 fiterr=0; ISB-SUMMARY
revs=4 nclauses=1 active=1 final=(0,0,601,602). Revision is
thrash-stable (no corruption, no clause growth) and does not
converge: revcount grows monotonically, history is not retained.

IS-A ADVERSARIAL-DRIFT (B2 overlapping drift): Q1A on A
`st=2 vers=2 ans=2:1,611 agree=1 cs=16 cg=56`. After the C1
drift with no clearing, the same plan executes: Q1B `st=1
vers=2 ans=2:1,711 agree=0 cs=16 cg=28`: the stale contract
admits 601, the spec procedure scans the stale bucket, C1 fact
0 (711,701,621) matches obj 621, and the learner returns the
wrong subject 711 while the oracle returns none. The failure is
visible end-to-end, not a cost change. ISA-PROBE: rp=602 (clause
hi, retired interior rel) chk=1,1,0 inv=3 dc=2 active=0 req=1.
ISA-REV: olderr=3 revcount=1 nclause=(0,0,701,701)
route701=1 route601=0 route602=0. Recovery: Q1C (601) `st=1
vers=0 ans=1:0 agree=1 cs=28 cg=28` (contract now routes 601 to
generic); Q2 (701) `st=2 vers=2 ans=2:1,711 agree=1 cs=15
cg=28` (spec on the rebuilt bucket).

IS-C NOISE (B1/B2 consecutive-failure semantics): on tag 801's
binding contract: one fail -> dc=1 act=1 run=1 req=0; one
confirm -> dc=0 run=0; two fails -> dc=2 active=0 run=2 req=0
(retirement precedes the revision latch); three consecutive
fails -> req=1. Real trials (1,0,0); revise: olderr=0 (the old
commitment was correct; the failures were noise), identical
clause (1,identity,[0,0]) restored, revcount=1, routing
fam0->1. ISC-CNT total=7 correct=1.

IS-D TAG-COLLISION (B1 mid-composition): tag 801 bound to
RETRIEVE meets a new VERIFY-shaped goal reusing the tag. QD0
`st=2 vers=0 ans=1:0 agree=0 cs=56 cg=56`: the stale binding
misroutes end-to-end (oracle [1,1]). Real trials (0,1,0);
ISD-REV: dc=2 active=0 req=1 olderr=2 revcount=1
nclause=(1,0,1,1) route1=1 route0=0 route2=0. clear_plans (plans
cache the fam at build time) + rebuild: QD1 `st=2 vers=3
ans=2:1,1 agree=1 cs=16 cg=56`.

## Kill bar assessment (observed vs frozen)

| Bar | Frozen | Observed | Result |
|-----|--------|----------|--------|
| K1 | IS-SETUP E0 + 3 BCONTRACT lines | exact | PASS |
| K2 | ISB-R1..R4/CNT/SUMMARY | exact (revcount=4, alternation, nclauses=1) | PASS |
| K3 | ISA-DRIFT vers=2 ans=2:1,711 agree=0 cs=16 cg=28 | exact | PASS |
| K4 | ISA-PROBE/REV/CNT + Q1C/Q2 agree=1 | exact (olderr=3, (0,0,701,701)) | PASS |
| K5 | ISC-NOISE/REV/CNT | exact (dc 1->0->2, req latch at 3, olderr=0) | PASS |
| K6 | ISD-STALE agree=0 + ISD-REV + ISD-RECOV agree=1 | exact (olderr=2, (1,0,1,1), vers=3) | PASS |
| K7 | 3/3 byte-identical, stderr empty | sha256 2f7b20b7 x3; .err 0 bytes | PASS |
| K8 | safebin, no python, pure Zag, pinned znc | verified | PASS |
| K9 | zero em/en dash bytes; zero of 17 identifiers in is_learn/is_main | byte/grep verified clean | PASS |
| K10 | real counterevidence only; u_check-only decisions | audit clean (see below) | PASS |

K10 audit detail: `grep u_check` in is_learn.zag shows exactly
four decision sites (ret_version, vfy_version, cnt_version,
bind_fam), as in INTEGRATION-B1B2 K12; ret/vfy/cnt_cov_has are
defined but never called; the new helpers (ret_buckets_rebuild,
first_subj) make no routing decisions. u_invalidate/u_revise are
called only in the four demos, against the live contract bases
(3000; 2000). All probe rels come from clause reads and vocab
scans; all trial outcomes from real try_family calls; all
episodes real.

## Falsification criteria (frozen; none fired)

- F1 (any IS-SETUP frozen value differs): NOT FIRED.
- F2 (any IS-B/IS-A/IS-C/IS-D frozen line differs): NOT FIRED.
- F3 (non-contract decision path, or non-real counterevidence):
  NOT FIRED.

## Implementation defects caught by testing (errata)

Three demo-apparatus defects were found by the first run cycle
and fixed before the frozen runs; none touched the contract
machinery or the composition path:

E1 (misaligned vocab read): the IS-B routing checks read
`get32(bvb,1)` (byte offset 1) instead of `get32(bvb,4)`
(element 1), reading misaligned garbage that u_check correctly
rejected (observed r702=0/r602=0 against a correct clause).
Fixed to byte offsets; the contract was never wrong.

E2 (goal-tag arithmetic slip and collision): the prereg's
frozen tags (816/817/818) assumed 813+1=816; the code computed
814/815, and the collision demo's tag collided with Q2's
(815), so QD0 loaded Q2's plan (st=1). Fixed the derivation
offsets (+3/+4/+5) to produce the frozen distinct tags
816/817/818; no prereg amendment was needed since the frozen
observable tags are what the prereg specified.

E3 (probe-state capture timing): ISD-REV printed dc/active/req
after u_revise (which installs a fresh clause and clears req),
showing dc=0 active=1 req=0 instead of the frozen probe state.
Fixed to capture dc/active/req before u_revise, as S9A did.

All three were caught because the frozen predictions were
exact; the fixes are demo-only and disclosed here.

## What this establishes (and does not)

Establishes: the integrated B1/B2 holds under adversarial
conditions. Overlapping drift produces a visible wrong answer
that revision detects and repairs end-to-end (IS-A);
oscillation is thrash-stable with exact clause alternation
(IS-B); sub-threshold noise neither revises spuriously nor
leaves the clause committed (it retires at dc=2, then revision
restores the identical clause with olderr=0 when the evidence
supports it) (IS-C); a mid-composition tag-shape collision
misroutes visibly and is repaired by counterevidence-driven
binding revision plus plan rebuild (IS-D). In no track did a
stale contract silently misroute in a way revision could not
repair.

Does not establish: automatic (non-demo) triggering of
invalidate/revise inside the live query flow; revision of
bindings under fact-world drift (try_family outcomes are
shape-determined in this apparatus, so the binding stressor is
tag-shape collision, disclosed in the prereg); scaling beyond
the tested sizes; multi-clause revision under adversarial
tables (all revise tables here admitted single-clause
solutions).

## Architecture accounting

- Cognition lines added: is_learn.zag delta vs ib_learn.zag is
  two generic helpers (ret_buckets_rebuild, first_subj; ~40
  lines, no semantic cases); is_world.zag delta is
  setup_worldC1 (apparatus world); is_main.zag is the new
  stress driver (apparatus, disclosed).
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- New opcodes/behavior classes/edge types: 0.
- Researcher-owned: the port deltas, the demo stages, the
  prereg, the three errata fixes.
- Learner-owned (in S/L state): binding contracts, coverage
  contracts, retired-clause markings, revision counts, fail
  runs, plans, procedure buckets. All four stress revisions
  are learner-state transitions driven by observed evidence.
- Pinned znc 2026.07.0-dev via safebin.

## Toolchain guard

Step 0 executed at startup and recorded in NAMECHECK.md:
PATH=$HOME/safebin; `which python3` and `which python` return
nothing. Zero Python computation occurred; no scientific result
passed through Python. All builds used the pinned znc; all runs
were the compiled binary; all text processing was shell tools.
Git writes via /usr/bin/git absolute path; explicit pathspecs on
every commit; nothing pushed. K8 PASS with no disclosures.

## Disclosed bounds (not claimed)

- The four stress stages are researcher-staged adversarial
  scenarios; the trial outcomes, vocab scans, episodes, clause
  reads, and query answers inside them are real, but the
  scenario framing (which contract, when to probe, when to
  revise) is apparatus. The composer does not yet self-trigger
  revision during live queries.
- u_grow was not ported (as in INTEGRATION-B1B2); nothing here
  exercises it.
- Four stress tracks, frozen worlds. No broad generality claim.
  The verdict is about the integrated binding layer under the
  specified adversarial conditions only.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/integration_stress/`:
PREREG.md (frozen, commit dfd2b7e28), NAMECHECK.md (Step 0),
is_base.zag, is_world.zag, is_module.zag, is_learn.zag,
is_main.zag, is_build.sh, is_full.zag (assembled; exactly one
`fn main`), is_bin, is_compile.txt, is_run1/2/3.txt (+ .err,
empty), REPORT.md (this file). Commits: dfd2b7e28 (prereg
alone), 28c85d161 (implementation), b9ec61de1 (artifacts +
runs); REPORT commit follows. All local, never pushed.

## Recommended follow-ups (for the parent, not decided here)

1. Self-triggered revision in the live query path remains the
   open gap (INTEGRATION-B1B2 follow-up 1): wire
   u_invalidate into version-selection consequences (e.g.
   spec refusal, oracle disagreement) so the IS-A/IS-D
   recovery pattern fires without staged demos.
2. The IS-D finding (plans cache fam at build time) suggests a
   plan invalidation hook on binding revision; test whether a
   general plan-version check subsumes the manual clear_plans.
3. Adversarial tables defeating single-clause induction (the
   prereg's noted 2-clause frontier) remain untested; a stress
   track with overlapping drift that forces u_induct's
   2-clause path would probe the clause language's limits.
