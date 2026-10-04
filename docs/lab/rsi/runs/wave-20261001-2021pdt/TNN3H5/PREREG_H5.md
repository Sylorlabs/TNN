# FROZEN PREREG: H5, generic supersession transition on the cognition path

Lane: TNN3H5, wave-20261001-2021pdt. Status: FROZEN PREREG (Phase 1).
Hypothesis source: docs/lab/rsi/runs/wave-20261001-1721pdt/TNN3/HYPOTHESES.md,
H5 (lines 143-170). Root cause: ROOT_CAUSE.md Cluster B (no lifecycle:
creation without supersession, unpromotion, or re-derivation).
Architecture accounting: ARCH_ACCOUNTING.md (dormant contradict_map,
map_standing, log_ev never called from the cognition path).

ORDERING RULE: this prereg is committed alone by the coordinator before any
implementation file is written. Any implementation artifact whose mtime
predates the prereg freeze commit, or any implementation written before the
coordinator's explicit authorization, is UNVERIFIABLE ORDERING and the
resulting evaluation is VOID. Correction after a kill proceeds only as a
fresh prereg plus fresh sealed worlds, never amend-and-promote.

## 1. Hypothesis under test

Supersession, unpromotion, and re-derivation become one generic protected
transition applicable to ANY learner structure (guides, MAPs, taught facts),
driven by learner-maintained standing rather than researcher-written
per-type handlers. The dormant contradict_map machinery is connected to the
cognition path. The selectors (ev_act, activate) already honor supersession,
so the change is permitting the cognition path to write CON edges on guides
and MAPs, which today no code path does. Structurally distinct from H4
(content): this is about time.

Grounded mechanism facts in the frozen TNN-2 base
(docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag,
SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd,
1591 lines):
- is_superseded (line 132) checks a CON self-edge: edge type 3 with f==t==n.
- ev_act (lines 859-900) skips any POLICY_ROOT-linked candidate with
  is_superseded != 0. activate (line 140) skips superseded tag-1 nodes.
- contradict_map (line 578) is exactly link_edge(W,m,3,m,0). It is called
  only from test battery functions (lines 1159, 1209), never from the
  cognition path.
- ev_observe (line 836) writes CON self-edges only on contradicted fact
  nodes (line 844, inline special case). No cognition path writes CON edges
  on guides (tag 1, POLICY_ROOT type-10 linked, field20==30 action,
  field24==-999) or on MAPs (tag 20).
- miss_inquire (line 795) creates guides with a hardcoded action and no
  lifecycle code anywhere in the file.
- revise_on_contradict (lines 685-704) scans MAPs for DEP (type 1) edges to
  the contradicted fact and invokes the single in-place patch schema
  t2_revise_graph (lines 706-752, called only from line 696).
  t2_kill_edge (lines 677-684) is called only from t2_revise_graph.

Falsifiable prediction (from the hypothesis): after wiring, if on a sealed
resolution world the learner still re-fires stale guides because no
experience ever writes the CON edge (white-box shows zero guide-CON edges
across the run), H5 is dead: the machinery is permitted but never used, so
lifecycle must be driven by something the learner maintains (standing, per
H6/H11), not merely permitted by the core.

## 2. Files

- Base (read-only reference, never edited):
  docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag
  (SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd).
- Working file (created at implementation time by byte-copy of the base,
  copy verified by SHA-256 before any edit):
  docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5/tnn3_h5.zag.
- Frozen binary: TNN3H5/tnn3_h5.bin plus a SHA-256 record, built with the
  pinned znc (src/tools/toolchain/znc_linux_x86_64_abed8aa1).
- This prereg: TNN3H5/PREREG_H5.md. Process record: TNN3H5/NAMECHECK.md.
- Sealed worlds: sealed directory chosen by the coordinator; NOT in this
  prereg; designed post-freeze per section 4.

## 3. Exact changes (all inside tnn3_h5.zag)

3.1. ADD one generic protected transition, supersede(W,n), budget 5 lines:
writes a CON self-edge (link_edge(W,n,3,n,0)) iff is_superseded(W,n)==0.
Uses only COMPARE and LINK from the frozen ISA. This is machinery, not
intelligence: it encodes no domain regularity.

3.2. contradict_map (line 578): body folded into supersede. New body is one
call to supersede(W,m) plus the existing return. Net -1 line on this
function. The two battery call sites keep compiling unchanged.

3.3. ev_observe (line 836), contradiction branch: delete the inline special
case link_edge(W,n,3,n,0) (line 844) and replace with supersede(W,n).
Net 0 on this hunk. The special-case contradiction path is folded into the
generic transition.

3.4. ev_observe: ADD a resolution call site, 1 line: every ev_observe,
after ctx_push, calls resolve_uncertainty(W,s,r). Resolution is pinned as
content-blind: any OBSERVE on (s,r) while an UNCERT(s,r) is pending counts
as resolution, whether the observe confirms or contradicts.

3.5. ADD resolve_uncertainty(W,s,r), budget 20 lines: scan nodes for UNCERT
nodes (tag 30, field20==s, field24==r, per the miss_inquire layout
write_node(W,u,s,r,2,0)); supersede each; then walk POLICY_ROOT type-10
edges and supersede every guide linked to a resolved UNCERT (guide-class
is pinned in section 6 for white-box counting: tag 1, field24==-999,
type-1 edge to a tag-30 node). Guides can no longer re-fire because ev_act
already skips superseded candidates. This is the M2-W2 fix.

3.6. revise_on_contradict (line 685): replace the t2_revise_graph call
(line 696) with supersede(W,m) on each MAP hit. The dormant contradict_map
semantics are now connected to the cognition path. Re-derivation is the
existing path, not new code: on the next miss for the key, ev_query's
trial loop (mp_run) runs against live facts and promote_graph creates a
fresh MAP whose DEP edges anchor to live fact nodes. This is the M3-W2
fix: the stale-provenance lookup cannot silently no-op because the stale
MAP is unpromoted and the fresh MAP is derived from current facts.

3.7. DELETE t2_revise_graph (lines 706-752, approximately 47 lines) in full:
the in-place literal-swap patch schema is the special-case operator being
folded. DELETE t2_kill_edge (lines 677-684, approximately 8 lines), which
is orphaned by that deletion.

3.8. M3-W3 consequence, no extra code: on contradiction, ev_observe already
supersedes the old fact (now via supersede) and teaches the new fact via
ev_teach_in. The stale taught answer fact therefore carries a CON
self-edge, so ev_query's exact-hit activate() skips it and the trial loop
re-derives instead of being vetoed. If the trial loop cannot re-derive
(revert class), the key stays a miss (-2) rather than returning a stale
taught value.

Line budgets: added at most 40 lines (3.1: 5, 3.2: 1, 3.3: 1, 3.4: 1,
3.5: 20, 3.6: 1; total 29, cap 40). Deleted at least 40 lines
(3.7: ~55, 3.2: 2, 3.3: 1; total ~58). Net cognition source delta at most 0.
Exact counts are recorded from the diff at implementation time.

What is explicitly NOT changed: bid(), the miss policy schema menu,
ev_act selection logic, activate lookup logic, promote_graph, ev_teach_in,
the 4-op ISA and execute. No trigger counting is added (evidence-weighted
triggers are H6/H11 territory, explicitly not claimed here). No standing
machinery is connected (map_standing stays dormant).

## 4. Sealed evaluation protocol (worlds designed POST-prereg)

The worlds are not in this prereg. The prereg pins only the sealing
protocol and the adversarial family the worlds must require.

4.1. Coordinator commits this prereg alone and records the commit hash and
UTC timestamp in the lane dir (PREREG_FREEZE record).
4.2. An independent adversary (a different lane agent, no shared working
state with the builder) designs the sealed worlds strictly after the
freeze timestamp, writes them to a sealed directory the builder cannot
read, and commits them with SHA-256 records. The builder attests in
writing that it has not read the world fixtures.
4.3. Adversarial families (minimum composition):
  R-family (resolution): 2 worlds. Each delivers at least 4 true misses
  creating guides on distinct keys; each miss is later resolved by an
  OBSERVE on the same (s,r); after each resolution the subject is
  re-presented in context and ev_act is invoked. Total: 8 resolution
  events. The two worlds must differ materially in structure (different
  relation families and subject distributions).
  C-family (contradiction): 2 worlds. Each promotes MAPs on at least 4
  keys via the trial loop; each key is contradicted twice in sequence
  with a re-derivation query between the contradictions; each battery
  contains at least 2 revert-class probes (contradiction on a key where
  the trial loop cannot re-derive). Total: 8 double-contradiction probes,
  4 revert probes. Same material-difference rule.
  All world keys, relations, and values must be absent from FW1-FW9 and
  from the 1421pdt sealed battery (no trivial variants). At least two
  worlds are designed after freeze with no knowledge of the
  implementation.
4.4. Builder implements after freeze authorization, compiles with pinned
znc, freezes the binary (SHA-256), and runs a 3/3 determinism self-check
on unsealed smoke worlds only.
4.5. The adversary runs the frozen binary on the sealed worlds, collects
behavioral outputs and white-box state dumps (Zag dump program, pinned
znc), applies the kill bars in section 5, and publishes the verdict with
evidence.
4.6. Any leak of world content to the builder before the run voids the
battery. If fewer than 2 valid worlds per family survive validation, the
battery is VOID and H5 is untested (not passed).

## 5. Frozen kill bars (exact numbers)

KB-W1 (white-box, primary, the falsifiable prediction): across the 8
R-family resolution events, the final-state dump must show at least 6 CON
self-edges (edge type 3, f==t) on guide-class nodes (tag 1, field24==-999,
type-1 edge to a tag-30 node). PASS: >= 6/8. If the count is 0 across the
whole R-battery, H5 is dead per its falsifiable prediction: the machinery
is permitted but never used.

KB-W2 (white-box MAP): across the 8 C-family double-contradiction probes,
the dump must show at least 6 CON self-edges on MAP-class nodes (tag 20).
PASS: >= 6/8.

KB-B1 (behavioral, M2-W2 analog): on each of the 8 R-events, after
resolution and subject re-presentation, ev_act must return 0 (no live
guide). TNN-2 returned 30. PASS: 8/8.

KB-B2 (behavioral, M3-W2 analog): on each of the 8 C-probes, the query
after the second contradiction must return the twice-corrected value.
TNN-2 silently no-oped and returned the first-patched value. PASS: 8/8.

KB-B3 (behavioral, M3-W3 analog): on each of the 4 revert-class probes,
the old taught fact must carry a type-3 self-edge in the dump, and the
query must return miss (-2) or a freshly derived value, never the stale
taught value. TNN-2 returned the stale value. PASS: 4/4.

KB-R1 (retention): 12/12 collateral probes correct on a
no-contradiction retention world (TNN-2 K-S14 analog: facts persist, MAPs
persist). PASS: 12/12.

KB-G1 (architecture accounting): diff of tnn3_h5.zag against the
SHA-256-verified base copy shows added lines <= 40, deleted lines >= 40,
net <= 0 (non-blank, non-comment cognition lines). No new modes, bridges,
routers, or handlers. No core-ISA additions. No forbidden protected
semantic operation. Any violation is FAIL regardless of behavior.

KB-D1 (determinism): 3/3 byte-identical full state dumps per sealed world.
Any byte difference is FAIL.

KB-P1 (process): zero forbidden-executable invocations during construction
(see section 8). Any violation is PROCESS-FAIL, terminal.

## 6. Negative controls (what FAILS H5)

NC-1: zero guide-CON edges across the R-battery. H5 dead (falsifiable
prediction fires). KILL.
NC-2: any behavioral bar passes while white-box shows zero guide/MAP CON
edges. Causal attribution is broken: something other than the transition
did the work. FAIL.
NC-3: CON edges present on guides or MAPs but stale guides still fire
(ev_act returns 30) or superseded MAPs are still consulted. The
transition is cosmetic; the selector contract is violated. FAIL.
NC-4: net-positive cognition lines, or any new mode, bridge, router, or
handler, or any core-ISA addition, or any forbidden protected semantic
operation. Governance FAIL regardless of behavior.
NC-5: any byte difference across the 3/3 reruns. Determinism FAIL.
NC-6: the adversary judges a world a trivial variant of FW1-FW9 or the
1421pdt battery. That world is VOID; if fewer than 2 valid worlds per
family remain, the battery is VOID and H5 is untested.
NC-7: implementation mtime predates the prereg freeze commit, or the base
copy SHA-256 does not match a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd.
UNVERIFIABLE ORDERING. VOID.

## 7. Architecture prohibitions and core-ISA boundary

No new modes, bridges, routers, or handlers are added by this change. One
generic transition (supersede) serves all structure types; the per-type
special cases (ev_observe's inline fact supersession, contradict_map as a
MAP-only dead path, t2_revise_graph as a MAP-only patch operator) fold
into it or are deleted.

Core-ISA boundary (per the 2026-09-30 protected core ruling): no
additions to the protected core. The frozen basis is ALLOC, READ, WRITE,
LINK, COPY, COMPARE/EQ, ADD, BRANCH, APPLY/EXECUTE. supersede uses only
COMPARE (idempotence check) and LINK (edge write): machinery, not
intelligence. Forbidden as protected semantic operations: FIND_POLYNOMIAL_ORDER,
DETECT_NEGATION, BUILD_CAUSAL_RULE, LEARN_PROCEDURE, FIND_THRESHOLD,
MAKE_CONDITIONAL, and any benchmark or domain equivalent. Adding any of
these is NC-4, governance FAIL.

## 8. Pure-Zag construction

Builder PATH is $HOME/safebin (36 tools, no python3, verified at lane
startup and recorded in NAMECHECK.md Step 0). All research logic
(implementation, verifiers, scorers, harnesses, world drivers, white-box
dump and analysis programs) is written in Zag and compiled/run with the
pinned znc. Shell is used only to invoke znc, run binaries, do git ops,
and move/copy files. No Python for glue, analysis, verifiers, harnesses,
or fixture provisioning. Any forbidden executable invocation is automatic
PROCESS-FAIL and is reported honestly.

## 9. Determinism protocol

3/3 byte-identical reruns of every sealed world against the frozen
binary, compared by SHA-256 of the full state dump. Zero randomness in
decision paths: the diff introducing the change is grepped for
time/clock/random/rand/seed/PID reads and must show none. The base has
no randomness; the change adds none.

## 10. Verdict rules

H5 advances past this wave iff ALL of KB-W1, KB-W2, KB-B1, KB-B2, KB-B3,
KB-R1, KB-G1, KB-D1, KB-P1 pass. Any single bar failing KILLS H5 for this
wave: no re-tune, no amend-and-promote. A killed H5 may return only via a
fresh prereg plus fresh sealed worlds (VOID discipline). Battery-level
void conditions (NC-6, NC-7, world leak) leave H5 untested, not passed.

## 11. Design questions for the coordinator (ruling needed before implementation)

Q1: Confirm the deletion of t2_revise_graph and t2_kill_edge (the in-place
patch schema, ~55 lines) with re-derivation via the existing trial loop
plus promote_graph. This is the honest route to the net-negative line
accounting the hypothesis claims. If ruled out of scope, this prereg must
be amended transparently (deleted floor drops, net bar becomes at most +5)
before implementation is authorized.
Q2: Confirm resolution is content-blind: any OBSERVE on (s,r) with a
pending UNCERT(s,r) resolves it, confirm or contradict.
Q3: Confirm the guide-class white-box definition (tag 1, field24==-999,
type-1 edge to a tag-30 node) for KB-W1 counting.
Q4: Assign the adversary lane and the sealed directory location, and
confirm the builder has no read path to it.
