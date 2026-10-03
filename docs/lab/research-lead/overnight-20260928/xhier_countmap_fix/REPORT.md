# REPORT: XHIER-COUNTMAP-FIX (use the composite's own count MAP address)

Worker: XHIER-COUNTMAP-FIX. Non-ledger task (claim minting paused).
Branch: tnn-native-lab, local only, never pushed.
Lane: docs/lab/research-lead/overnight-20260928/xhier_countmap_fix/
Verdict: **XHIER-COUNTMAP-FIX-PASS** (K1, K2, K3a, K3b, K3c, K4,
K5 all pass). Method: frozen prereg (v2, committed before
implementation), two binaries (patched + frozen-verbatim
control) from one driver, 3/3 byte-identical fixed runs.

## 0. What was fixed

COUNTMAP-ADDRESSABILITY Section 5(a) reported a latent
correctness issue, reasoned from source: `xhier_exec` resolved
each MAP_Z's own type-14 count MAP address
(`a = xhier_mapz_agg(W,z)`), used it only as an existence gate,
then executed the world-global singleton anyway
(`xs5_agg_exec(W,e,xs5_agg_rel(W))`).

The patch (xf_block.zag :2547-2580, diff-verified as the only
change vs the frozen block):

- New helper `xhier_mapz_rel(W,m)` (:2547): the exact
  `xs5_agg_rel` read shape (scan edges 0..4095 for `(m -1-> f)`,
  first live tag-1 target, return its rel field 24),
  parameterized by the MAP id instead of calling
  `xs5_find_countmap`.
- Patched `xhier_exec` (:2565): the aggregation relation comes
  from `xhier_mapz_rel(W,a)`, the composite's own count MAP.
  Two loud fences: `XHIER-EXEC-NOAGG` + -2 when no live count
  MAP sits on the composite's own type-14 edges (tombstoned or
  never linked); `XHIER-EXEC-NOREL` + -2 when the address
  resolves but its relation is unreadable.

Decision, made honestly in the prereg: FIX on the happy path,
FENCE on breakage. Fence-only (refuse on divergence) was
rejected because it would return -2 exactly where the
composite's own provenance is informative and correct. The
composite was verified at compose time against its own count
MAP; executing with its own relation preserves the verified
semantics.

Untouched, as required: `xs5_find_countmap` and `xs5_agg_rel`
are byte-identical in the patched block (diff-verified);
COUNTMAP-2 stays on hold (no parameterized world-global lookup
added).

## 1. Kill-bar results

World (one workspace; ids from the runs): MAP_Y (84, rel 82,
singleton) formed in Phase A; MAP_V2 (194, rel 85) in Phase B;
MAP_V3 (274, rel 87) in Phase B2, all via the proven trial
path. MAP_Z1 (290) composed pre-tombstone via xs5_compose,
LINK14 to the nav MAP (27) and MAP_Y. MAP_Z2 (311) built with
frozen ops (`promote_graph` + `link_edge`, the exact MAP_Z
shape), LINK14 to the nav MAP and MAP_V3. MAP_Y tombstoned
(frozen ns 0/36 pattern), no restore: singleton becomes MAP_V2
(rel 85) while MAP_Z2's own live count MAP is MAP_V3 (rel 87).
Endpoint 14 carries an 82-count of 2, an 85-count of 3, and an
87-count of 4.

- K1 (discrimination): fixed `xhier_exec(W,mz2,11)` = 4 (count
  over rel 87, the composite's own relation); control = 3
  (count over rel 85, the singleton's relation). The old code
  silently aggregates over the wrong relation while MAP_Y is
  tombstoned, exactly the reported latent issue, now
  demonstrated, not merely reasoned. PASS.
- K2 (regression): pre-tombstone `xhier_exec(W,mz1,11)` = 2 on
  BOTH binaries (PC-R.1 PASS each), and the fixed-run stdout
  prefix through XF-PHASER-END is byte-identical to the
  control-run prefix (cmp). The patch changes nothing on the
  happy path. PASS.
- K3a (provenance-unreadable fence): after tombstoning all 4 of
  MAP_V3's live tag-1 type-1 provenance targets, fixed returns
  -2 with `XHIER-EXEC-NOREL a=274` in the trace; control
  silently returns 3 (the wrong-relation count, computed from
  a composite whose own provenance was just destroyed). PASS.
- K3b (tombstoned-address fence): after tombstoning MAP_V3
  itself, fixed returns -2 with `XHIER-EXEC-NOAGG z=311`;
  control returns -2 via the silent gate. PASS.
- K3c: control stdout contains neither loud line (loudness is
  new behavior). PASS.
- K4: 3/3 byte-identical whole-output fixed runs, SHA-256
  9cfc0bd3da2d86992eb0ca6da81bbebba576275bb11731163cdb4b91bafb9f02.
  Control run SHA-256
  e0f9e0e8786da3c81a3d859474ba621a288c8d5d4624c60866a4fbc5d61eaa52.
  PASS.
- K5 (hygiene): pure Zag; safebin PATH from the first command
  (Step 0 in NAMECHECK.md; `which python3`/`which python`
  empty); zero em/en dash bytes in lane docs (byte-verified);
  opaque identifiers; frozen block reused verbatim for control
  (SHA-256
  56b2e678d42103d7fb9bf75e8c99289a1698844891a654e215bc025915231004
  re-verified pre and post); diff shows only the added helper
  and the xhier_exec body; driver-only new code under the xf_
  prefix; 0 new node types/edge types/opcodes/modes/bridges/
  handlers; Zag pitfalls honored. PASS.

Precondition tallies: 15/15 PASS on the fixed binary and 15/15
on the control binary (world construction identical; only the
xhier_exec behavior differs).

## 2. The v1 to v2 amendment (a finding in its own right)

The v1 prereg's world construction (tombstone MAP_Y, compose
against the new singleton, restore MAP_Y) proved
unimplementable during v1 implementation, for a source-level
reason: `alloc_node` (block :87) scans node ids 2..1023 and
reuses the FIRST slot with live flag 0. Tombstoning does not
suspend a node; it frees its slot for recycling, and the next
allocation takes it. v1's "restore" step could not resurrect
MAP_Y; retagging the recycled slot corrupted the world (the v1
pilot showed the singleton stuck and a spurious fence trip).
The v1 pilot outputs were discarded as results.

This is worth banking as architecture vocabulary alongside the
addressability split: **in this substrate, tombstone is
destroy, not suspend**. Any future lane that tombstones a
structure and later needs it back must re-form it, not restore
it; any test that tombstones must either need nothing back or
account for slot recycling explicitly. v2 was preregistered
(with this lesson in its amendment note) before the v2 driver
was written; the patch itself was unchanged between v1 and v2.

## 3. Consequences

- The Section 5(a) latent issue is closed: fixed, with loud
  fences on the two unusable-address paths. Any future MAP_Z
  work inherits the corrected `xhier_exec`.
- The fix is behavior-identical to the frozen block on all
  single-relation worlds (K2), so the DAGFAN regression worlds
  keep passing verbatim.
- The control binary's K1/K3a legs re-demonstrate the
  COUNTMAP-SINGLETON finding on a new world (composition still
  cannot address the non-singleton count MAPs; it now also
  silently computes from a destroyed provenance). Nothing in
  this lane changes that; COUNTMAP-2 stays on hold.
- K3a's control leg (silently returning 3 after the
  composite's own provenance was destroyed) is arguably the
  sharper warning: the old code's wrongness is not confined
  to relation selection.

## 4. What was tested vs what was reasoned

Tested (frozen, this lane, PASS): the divergence world (K1
4 vs 3); the happy-path identity (K2 prefix cmp); both loud
fences (K3a/K3b); loudness novelty (K3c); determinism (K4
3/3); hygiene (K5).

Reasoned: the fix-vs-fence decision (prereg Section "The
fix"); the v1 slot-recycling root cause (frozen source
:87 plus the v1 pilot symptom); the claim that single-relation
worlds are behavior-identical (by construction of the read
shape, plus the K2 empirical check on one such world).

## 5. Notes for the parent

- No ledger entry: non-ledger task, nothing minted.
- No push: commits local on tnn-native-lab only, explicit
  pathspecs. This report is committed with the lane's
  implementation artifacts.
- The singleton lookup was not changed. COUNTMAP-2 stays on
  hold. CLAIM_LEDGER.md not modified.
- Style: no em/en dashes in this file (hyphens only), opaque
  identifiers throughout.
- Suggested standing vocabulary addition (for the parent's
  call): tombstone-is-destroy (Section 2). If adopted, future
  preregs that tombstone-and-restore should be rejected at
  review time.
