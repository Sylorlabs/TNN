# H5 Implementation Record: generic supersession transition

Lane TNN3H5, wave-20261001-2021pdt. Implements frozen prereg PREREG_H5.md
(commit 57aac4b81) exactly per section 3. Pure Zag, safebin toolchain,
no forbidden executables (KB-P1 clean).

## Ordering and base verification (NC-7)

- Prereg freeze commit: 57aac4b81 (2026-10-02 03:30:27 UTC), committed alone.
- Base: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag,
  SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
  (verified before any edit, 1591 lines).
- Working file tnn3_h5.zag created by byte-copy at 03:36:10 UTC (after
  freeze), copy SHA-256 verified identical before editing.
- Implementation edits all landed after the freeze commit. No
  implementation artifact predates the prereg.

## Changes (prereg section 3, exact)

3.1 ADD supersede(W,n), 4 lines: CON self-edge via link_edge(W,n,3,n,0)
    iff is_superseded(W,n)==0. Uses only COMPARE and LINK. Placed after
    is_superseded.
3.2 contradict_map: body folded to supersede(W,m); return 0. Battery call
    sites (t_p7, t_dv) compile and pass unchanged.
3.3 ev_observe contradiction branch: inline link_edge(W,n,3,n,0) replaced
    with supersede(W,n). Net 0.
3.4 ev_observe: added resolve_uncertainty(W,s,r) after ctx_push, 1 line.
    Runs on every observe, content-blind per Q2 ruling.
3.5 ADD resolve_uncertainty(W,s,r), 27 lines: supersedes UNCERT nodes
    (tag 30, field20==s, field24==r), then walks POLICY_ROOT type-10
    edges and supersedes guide-class nodes (tag 1, field24==-999,
    type-1 edge to the resolved tag-30 node). Over the 20-line guidance
    budget, within the binding 40-line cap (see accounting).
3.6 revise_on_contradict: t2_revise_graph(W,m,factn,old_o,new_o) replaced
    with supersede(W,m) on each MAP hit. Net 0 on the hunk.
3.7 DELETE t2_revise_graph (46 code lines) and t2_kill_edge (8 code
    lines) in full, per Q1 ruling. Stale section comments updated to
    describe the H5 design; no other references remain in code.
3.8 Consequence verified in dev: contradiction supersedes old fact and
    teaches new fact; trial loop + promote_graph remain the re-derivation
    path (zero new code).

NOT changed: bid(), miss policy schema menu, ev_act, activate,
promote_graph, ev_teach_in, 4-op ISA, execute. No trigger counting, no
standing machinery, no new modes/bridges/routers/handlers, no core-ISA
additions, no forbidden protected semantic operations.

## Diff accounting (KB-G1), non-blank non-comment cognition lines

Added (cognition): 35
  supersede 4, contradict_map 1 (fold), revise_on_contradict 1 (fold),
  resolve_uncertainty 27, ev_observe call site 1, ev_observe fold 1.
Deleted (cognition): 57
  t2_kill_edge 8, t2_revise_graph 46, contradict_map old body 1,
  revise_on_contradict old call 1, ev_observe old inline 1.
Net: -22.

Test-only delta (t_t2_revise rewritten for the new contract, not
cognition): added 9, deleted 16. Excluded from the KB-G1 count per the
prereg's "(non-blank, non-comment cognition lines)" qualifier.

KB-G1 verdict: added 35 <= 40 PASS; deleted 57 >= 40 PASS; net -22 <= 0
PASS. Deletion evidence: t2_revise_graph (46 lines) and t2_kill_edge
(8 lines) are gone from the file; the diff shows their full removal;
grep finds no code references (only deletion-note comments).

## Build (pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1)

- tnn3_h5.bin SHA-256: 344ac89fb338ddbf46bea6be4c526d99410ea643278ab91fb06d76b7e33c4eb7
- 3/3 byte-identical rebuilds (same SHA-256 across three znc invocations).
- Built-in battery: 46/46 PASS (includes rewritten T2-REVISE).
- Grep for time/clock/random/rand/seed/PID in the diff: none (KB-D1
  qualitative check; sealed 3/3 dump check belongs to the adversary run).

## Development tests (builder's own worlds, NOT sealed)

Driver: dev_h5.bin (dev_h5_nomain.zag = tnn3_h5.zag copy with dev main).
3/3 byte-identical stdout
(5d69a6a2f3499013b70d76b511ddc01875960029a345e9bf6bbf11b09f07a5f9).

D1 resolution: miss creates guide; observe on same (s,r) writes 1 CON
  self-edge on a guide-class node; ev_act after re-presentation returns
  0 (was 30 in TNN-2). PASS.
D2 contradiction: trial loop promotes MAP; contradicting a licensing
  fact writes 1 CON self-edge on the MAP and 1 on the old fact; new fact
  queryable. PASS.
D3 double contradiction: two sequential contradictions on one key; MAP
  stays superseded (idempotent); query returns twice-corrected value.
  PASS.
D4 retention (no contradiction): facts and derived answers persist; zero
  spurious CON edges. PASS.
D5 four distinct-key misses resolved: 4/4 guides carry CON self-edges;
  4/4 ev_act calls return 0. PASS.

DEV ALL PASS (5/5).

## Deviations from the prereg

1. t_t2_revise (built-in test) rewritten: the old test asserted the
   deleted in-place patch behavior (t2_exec returns corrected value,
   signature change), which cannot pass after the Q1-confirmed deletion.
   The new test asserts the H5 contract (MAP superseded, fact
   superseded, new fact live). Test-only change; cognition untouched;
   transparently recorded here, never silent.
2. resolve_uncertainty is 27 lines vs the 20-line guidance budget. The
   binding KB-G1 cap is 40 total added; actual is 35. No bar affected.

No other deviations. No sealed directory read; no sealed-style worlds
designed; development worlds use disjoint key ranges (7xxx/8xxx) from
any plausible sealed battery.

## Process (KB-P1)

PATH was $HOME/safebin for all work. `which python3` printed nothing
(exit 1) at startup and at implementation start (NAMECHECK.md Step 0,
Step 0b). Shell invoked only: pinned znc, built binaries, git
read-only ops (log/show/status/diff), file copies. Zero
forbidden-executable invocations. No commits by this worker; no push;
no files written outside the lane directory.

## Status

IMPLEMENTATION COMPLETE. Binary frozen at
344ac89fb338ddbf46bea6be4c526d99410ea643278ab91fb06d76b7e33c4eb7.
READY FOR SEALED EVALUATION pending the independent adversary's sealed
worlds (sealed/ directory, never read by this worker).
