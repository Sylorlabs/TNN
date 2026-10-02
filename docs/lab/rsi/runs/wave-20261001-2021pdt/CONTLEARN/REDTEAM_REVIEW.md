# REDTEAM_REVIEW: CONTLEARN INTEGRATION-DEMONSTRATED (independent second opinion)

Wave: wave-20261001-2021pdt. Lane: CONTLEARN. Reviewer: independent red-team
subagent (no shared work with the CONTLEARN or CONTLEARN-IMPL workers).
Date: 2026-10-01. Method: read-only analysis of committed lane files and the
frozen source; SHA-256 verification of committed artifacts; read-only re-run
of the committed `cl_driver` binary. No new implementation, no forbidden
executables, pure Zag observation plus shell.

Verdict under review: INTEGRATION-DEMONSTRATED, defined by PREREG_CONTLEARN.md
section 6 as K0-K6 all passing, with the exact frozen claim: "on this fixed
150-event sequence the frozen core shows >= 20 white-box cross-phase citations
with the stated floors, under the stated controls", and explicit non-claims:
no L3, no generality, no architecture claim, disclosed (not sealed) script.

## Independent verification performed (not taken on trust)

1. Artifact hashes: `cl_driver` =
   `c8c089b8a0a25f9727719d386aad31fd584a171b3ccbe5ed3bc0b5a72c0e81b7`,
   `cl_driver.zag` =
   `b7a1877eb64545b2490ad2ee50f0b818dfd8ff6ac08e6f84e00a00cd0d45a43a`,
   `cl_combined.zag` =
   `4aba249d9ab81530d658fdf14c2b6ba43b83dd2386f8aa6f67b5accfef404d07`.
   All three match DRIVER.md exactly.
2. Determinism spot check: re-ran the committed `cl_driver` read-only with
   `printf 'TREAT'` and `printf 'C-P6'` on stdin. Stdout SHA-256 =
   `53ff2c990e4f7f8d29c8b1bb809cf6616226b9f6bd3dd28d06210dc54446bc44`
   (TREAT) and `218854b0cc91580580aafc86f404bcab6c5df8eba14ceca65ed00756251adc81`
   (C-P6), both matching RUN_LOG.md; zero stderr bytes. K6 reproduced
   independently. (Note: the mode token must match stdin exactly with no
   trailing newline; `echo TREAT |` yields MODE_FAIL. This is a driver input
   quirk, not a defect.)
3. Transcript counts: `transcript_TREAT_r1.txt` contains exactly 149 `EV`
   lines; the P4 section contains exactly 6 events (3 OBSERVE + 3 QUERY).
   Oracle lines present as reported: R1C 6, R2C 3, R3C 3, R4C 12, R5C 6,
   REUSE_COUNT 30, K4A_MISSING 0, K4B_MAPS 6/6, C-P6 0/18 with K5B_N20 0.
4. Frozen source re-read: `t2_try_verify` (tnn2.zag line 497),
   `promote_graph` (line 533), `revise_on_contradict` (line 685),
   `ev_query` (line 813), `ev_observe` (line 836). The prereg's mechanism
   descriptions are accurate to the source.

## Attack 1: Knowledge vs architecture (where is the learner?)

Claim probed: the prereg question asks for "learner-owned cross-phase
integration". The verdict's natural reading implies the learner did
something integrative.

Finding: the learner's causal contribution to every counted citation is
zero. All integration decisions are made by frozen researcher-written
machinery, triggered by researcher-authored events, using
researcher-supplied answer keys.

Quoted evidence, frozen source tnn2.zag:

- `t2_try_verify`, the promotion accept decision:
  `if(expected!=-2 && v==expected){return v;}` (unmasked branch). The
  candidate is accepted iff its executed value equals `expected`.
- Driver `cl_driver.zag` line 89: `let a:i32=ev_query(W,s,r,exp,0);` Every
  QUERY passes the event tuple's 4th field as `expected` with flags=0.
  The transcript shows the answer key in the open:
  `EV 2 6001 202 5101 ans=5101`. Cognition receives the correct answer on
  every query; the "accept" step is answer-key matching by machinery.
- `promote_graph` (line 533): allocates the MAP, writes the DEP edges to
  the licensing facts, then calls `ev_teach_in(W,s,r,ans)`. The MAP, its
  DEP citations, and the answer fact are all created by researcher code
  after the machinery's key-match decision.
- `ev_observe` (line 836) on contradiction: unconditionally calls
  `revise_on_contradict`, which scans all MAPs for a DEP edge to the
  contradicted fact and rewrites the cell. No learner decision anywhere
  on this path; the driver's OBSERVE event is the sole trigger.

This is not a new discovery; it is the H2-v2 causal finding on the
byte-identical frozen source, quoted: "Pre-decision scan on a fresh
workspace: zero tag-20 nodes, policy=-1, mp=-1: no learner-created
persistent state exists when the accept decision is made... the MAP
promotion happens after the decision. No learner-created value is in the
causal chain." (RESULT_H2V2_G2.md, K-H2-3(a), FAIL.)

So: R1c = machinery writes DEP edges after a key-matched trial.
R2c = machinery rewrites cells on a driver OBSERVE. R3c = machinery
supersede plus reteach on a driver OBSERVE. R4c = the allocator never
evicts live slots below cap (absence of interference, not an act of
integration). R5c = exact-hit fact reads (see Attack 6). The learner
contributes exactly one thing: the persistent arena that outlives phases
(K1's single process). Everything else is machinery executing a script.

Does the verdict overclaim? The verdict document itself stays inside the
prereg's operational bound (structural predicates, disclosed script, no
L3). But the prereg's question phrase "learner-owned cross-phase
integration" and the R5c label "P2 procedures reused" both imply an
agent doing the integrating. On the project's own H10 terminology,
"learner-owned" can be read as "resident in the learner's arena", and
under that weak reading the verdict is literally true. Under the causal
reading (the learner decided or authored something), it is false, and
H2-v2 already proved it false on this source. The verdict needs the weak
reading pinned down explicitly, or it will be misread.

## Attack 2: Fixed script, deterministic machinery, and what K5 actually controls

Claim probed: could REUSE_COUNT 30/30 be fully explained as the
machinery's deterministic response to the fixed script, with no
integrative capacity required? Does K5 address this?

Finding: yes, it is fully explained that way, and K5 addresses only a
narrower instrument question.

- The core has no RNG; `z_alloc` zero-fills; all scans are id-ascending.
  The prereg states this; I confirmed 3/3 byte-identical re-runs plus my
  own independent re-run. Given the fixed script, 30/30 was knowable from
  the source before the run. The prereg itself telegraphs this: T is
  "expected to be {0,1,2}", UNCERT "expected 0; every probe is designed
  to hit". This is a characterization measurement, which the prereg
  honestly frames as a "measurement instrument", but a reader inferring
  "a risky test was passed" would be mistaken.
- K5a equality (C-P1 12/12 = TREAT 12/12; C-P2 R1C 6 = TREAT R1C 6; C-P3
  R2C 3 = TREAT R2C 3; C-P4 3/3; C-P5 40/40) shows per-phase outcomes
  depend only on each phase's prerequisites, not on the full history.
  That is evidence AGAINST integration doing behavioral work: adding the
  entire prior history changes nothing about any phase's scores. The
  cross-phase citations exist structurally (DEP edges, revised cells)
  but are causally inert for behavior.
- What K5 actually tests: K5b's own kill condition says "a K5b violation
  means the harness leaks state: VOID the comparison". K5 is a
  harness-leak instrument check (separate processes do not share arenas),
  not an alternative-explanation attack. It does not test the "dumb
  persistent store" explanation.
- The untested alternative: a fact store with teach, exact-hit,
  supersede-on-contradict, and retention, but no MAP/trial/revise
  machinery, scores R1c=0, R2c=0, R3c=3, R4c=12, R5c=0 for a total of 15,
  below the floor of 20. So the floor of 20 is calibrated to exactly
  exclude the dumb store and require the MAP machinery to function. That
  makes K3 a machinery-presence smoke test, not a test of integrative
  quality. No weaker-system headroom analysis was preregistered or
  reported; I supply the computation above as the missing calibration
  note.

## Attack 3: Bar calibration and headroom

- REUSE_COUNT 30/30 is at ceiling; every component is at or near its
  maximum (R1c 6/6, R2c 3/3, R3c 3/3, R4c 12/12, R5c 6/6). Floors sit just
  below the machinery's deterministic maxima (4, 2, 3, 10, 4; total 20).
- There is no headroom analysis and no preregistered account of what a
  weaker system would score. Per Attack 2, the floor of 20 sits just
  above the 15 a MAP-less fact store would score. The bars therefore
  discriminate "the MAP/trial/revise machinery fired on this script" from
  "it did not". They do not grade integration, because nothing in the
  script varies the difficulty of integration: every probe is designed to
  hit, every contradiction targets a MAP the machinery is written to
  revise, and the answer key is supplied on every query.
- Consequence: the bars cannot fail unless the machinery is broken. A
  kill bar that cannot fail short of implementation breakage is a
  regression check, which is a legitimate use, but it is not an
  experiment that could have informed the integration question either
  way.

## Attack 4: The 149 vs 150 erratum and the empty-env deviation

Both verified immaterial; I concur with the worker.

- Erratum: the prereg's enumerated tuples give 3 OBSERVE + 3 QUERY = 6
  P4 events, total 24+12+9+6+80+18 = 149. I counted 149 `EV` lines in the
  committed TREAT transcript and 6 in the P4 section. No event was
  invented; the driver implements exactly the enumerated tuples. No kill
  bar references the total count (K1c's audit expectations were recorded
  as 149/24/24/33/18/80/18 in DRIVER.md and all printed AUDIT_PASS).
  No bar is affected.
- Empty-env deviation: the prereg named `env -i plus PATH`; `env` is not
  linked in safebin, so runs launched via `bash -c 'exec -c ./cl_driver'`
  with a fully empty environment. A fully empty environment strictly
  satisfies the phase-free requirement (nothing in the environment can
  carry a phase label). The binary reads only /dev/stdin; it has no env
  reads; all 21 runs exited 0 with byte-identical transcripts. No bar is
  affected. If anything, the deviation is conservative.

## Attack 5: Coexistence with H2/H3 ("no learner-reachable construction path")

The H3 verification (PREREG_H3.md, this wave) found: "no code path
reachable from the frozen event interface (ev_observe/ev_query/ev_act)
can produce a learner-stored graph-as-fact-operand link. Fact operands
(field28) hold scalar answer values only." H2-v2 found no learner-created
criterion in any accept/reject causal chain and that promoted MAPs are
causally inert for the query path.

These findings coexist with INTEGRATION-DEMONSTRATED without
contradiction, because CONTLEARN never exhibits a learner decision. Every
"integration" event in CONTLEARN is event-triggered machinery: the event
interface triggers construction (promote on key-matched trial, revise on
OBSERVE), exactly as H3 describes the interface's limits. H2/H3 measure
learner agency and find none; CONTLEARN measures machinery citation
behavior in a persistent arena and finds the machinery working as
written. Both true. The apparent tension is terminological: if
"integration" is read as something the learner does, CONTLEARN would
contradict H2/H3; read as the prereg's structural predicates, it does
not. This is the same narrowing as Attack 1, and it is the load-bearing
point of this review.

## Attack 6: R5c is fact retention, not procedure reuse

The verdict's evidence table labels R5c "P2 procedures reused at the
end". The white box shows otherwise:

- `ev_query` tries `activate` (exact fact match) BEFORE the trial loop.
  RUN_LOG.md P6 census: "All probes exact-hit; the +18 edges are USE
  self-edges from exact hits."
- H2-v2 K-H2-4(b) on the byte-identical source: "the promoted structure
  is causally inert for the query path; no tag-20 MAP root is executed
  outside `t2_try_verify` because the query path only executes freshly
  assembled trial candidates (`ev_query` reads only tag-1 facts via
  `activate`)."
- The R5c oracle requires "the serving node is the content-expected
  answer fact (P2-created...)". The serving node is a fact node taught by
  `promote_graph`'s `ev_teach_in` call, read by `activate`. The MAP node
  itself, the actual "procedure" structure, is never executed in P6.

R5c therefore demonstrates retention and exact-hit of machinery-taught
facts, identical in kind to R4c. The label "procedures reused" is a
misnomer that materially overstates the finding within the verdict's own
bounded claim. It should read "P2/P3-taught answer facts retained and
exact-hit".

## Attack 7: The answer-key condition

Every QUERY in the battery passes the correct answer as `expected` with
flags=0 (driver line 89; transcript `EV 2 6001 202 5101 ans=5101`). The
promotion accept is `v==expected`. H2-v2's masked evaluation (expected=-2,
flags=1) showed the same machinery accepts the first clean candidate in
the fixed researcher search order and scores 0% on trap worlds. The
CONTLEARN "integration" is therefore conditional on per-query
supervision: it demonstrates that the machinery cites prior structures
when the answer key tells it which candidate is right, and says nothing
about unsupervised integration. This is disclosed in the prereg
("QUERY (ev_query with the listed expected and flags=0)"), so it is not
a hidden flaw, but it belongs in the verdict's stated bounds, where it
currently does not appear.

## Verdict: QUALIFY

INTEGRATION-DEMONSTRATED stands as a bounded machinery-baseline
measurement: all of K0-K6 pass, and I independently reproduced the
hashes, the transcript counts, the determinism, and the immateriality of
both deviations. No bar is overturned. But the verdict as worded needs
bounds narrower than stated, because the natural reading implies a
learner doing integration work, and the evidence shows the opposite.
The qualified claim is:

On the fixed disclosed 149-event script, with the correct answer
supplied on every query (flags=0), the frozen TNN-2 core's
event-triggered machinery produces 30 structural cross-phase citations
(MAP DEP edges to earlier facts, in-place MAP revision on contradiction,
fact supersede plus reteach, fact retention under 2x unrelated load,
exact-hit reads of earlier-taught answer facts) in one persistent arena,
with per-phase-reset controls scoring identically within phases and 0/18
on the cross-phase probe, 3/3 byte-identical.

Explicitly not shown: learner-owned integration in the causal sense (no
learner-created state influenced any integration decision; H2-v2 K-H2-3(a)
on the byte-identical source); procedure reuse (no promoted MAP is ever
executed at query time; H2-v2 K-H2-4(b); R5c is fact retention);
unsupervised integration (every accept decision matched a supplied
answer key); or integration that changes behavior (K5a equality shows
per-phase outcomes are history-insensitive beyond prerequisites). The
bars discriminate MAP-machinery presence (floor 20 vs ~15 for a MAP-less
fact store) rather than grading integrative quality, and 30/30 at ceiling
leaves no headroom. This is consistent with the prereg's own framing of
the battery as a baseline measurement for H10 to beat, and consistent
with the H2/H3 findings of no learner-directed construction.

Suggested follow-up (not authorized here, recorded for the coordinator):
a masked variant (expected=-2, flags=1) of the same script would test
whether any cross-phase citation survives without answer keys; the H2-v2
prior is that promotion would cite first-clean-in-fixed-order structures
instead.
