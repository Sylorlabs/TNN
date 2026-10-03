# POSTFREEZE_RUN.md -- Post-freeze sealed adversarial battery report

Wave: wave-20261001-2321pdt, lane BATTERY.
Prereg: PREREG_POSTFREEZE.md, frozen at commit 59e029102,
SHA-256 dcf5e26ac3b095565f7c89926bd63ccb14efda3061cc6985e34c436a2de8037c.
Executed: 2026-10-02. All work pure Zag (pinned znc) and shell; safebin
PATH; no Python invoked. TNN-2 frozen; no source edits.

## Process bars

- PF-K1 (prereg ordering): PASS. Prereg committed alone before any
  post-freeze world was generated; SHA-256 re-verified unchanged.
- PF-K2 (determinism): PASS. All 6 world transcripts byte-identical
  across 3 fresh-state runs.
- PF-K3 (frozen binary): PASS. freeze_shim2_bin and tnn2.zag match
  the prereg hashes before and after; zero modifications under
  frozen paths.
- PF-K4 (seal integrity): PASS. PF_MANIFEST.sha256 verified (6/6);
  grep of 60000-69999 over frozen sources returns zero matches.
- PF-K6 (no-leak): PASS. 0 leaks across all 3 runs.

## Calibration gates

All gates passed. Degenerate controls fail; competent controls pass.

- PF-A1: D 0/2 (FAIL); C 2/2 (PASS).
- PF-A2: D 0/2 (FAIL); C 2/2 + no-spurious (PASS).
- PF-B1: D1 FAIL, D2 FAIL; C PASS (selective 30->31).
- PF-B2: D FAIL (30,30,30); C PASS (11,22,33).
- PF-C1: D FAIL; C PASS.
- PF-C2: D FAIL (transfer 0/1); C PASS (transfer 1/1).

## Per-world results (frozen TNN-2; identical across 3 runs)

### PF-A1: construction vs retrieval -- FAIL

Probes 0-1: 0/2. The mechanism returned the taught wrong answer
60999 (1-hop direct fact on the compose relation) instead of the
constructed P->Q composition 60902. Validity 2/2 PASS (taught P and
Q facts retrievable). Failure mode: direct retrieval shadows
construction; when a (wrong) taught answer is available on the
query relation, the mechanism prefers it over building the 2-hop
composition. This is the adversarial confirmation: construction
loses to retrieval.

### PF-A2: selective composition -- FAIL (with a design caveat)

BAR PF-A2 FAIL. Probes 0-1 (valid composition): 2/2 PASS. Probes
2-3 (no spurious): FAIL (returned 60931/60932, not -2).

Caveat (battery design limitation, recorded honestly): the 2/2 on
the valid-composition probes appears to be via BFS traversal from
the grounded subject (60201->60911->60921) verified against the
oracle expected value, not via selective procedure abstraction.
The world as designed does not discriminate BFS reachability from
procedure composition, because the QUERY carries the oracle
expected value which the trial uses for verification. The
"no-spurious" probes were answered via 1-hop BFS (60201->60931)
matched to the oracle. This world is a weak instrument for
selectivity; the mechanism (a) verdict rests on PF-A1 and the v3
M1 results. No calibration gate was violated (D FAIL, C PASS), so
the world is not VOID, but its evidentiary weight for selectivity
is discounted.

### PF-B1: concurrent guides, selective resolution -- FAIL

NULL_ACTION 0, PRERES_ACTION 30, POSTRES_ACTION 30. Validity PASS
(both misses yield M). Failure mode: the guide persists unchanged
after partial resolution; the post-resolution ACT is identical to
the pre-resolution ACT (stale 30). No selective resolution. The
frozen mechanism's guides never transition on resolution, whether
sequential (v3 M2-W2) or concurrent with partial resolution (here).

### PF-B2: guide flood -- FAIL

FLOOD_ACTIONS 30, 30, 30. Validity PASS (3x M). Failure mode:
constant guide action under concurrency; distinct=0. Three
concurrent distinct uncertainties produce three identical actions.
No content discrimination, concurrent or sequential.

### PF-C1: contradiction of a derived fact -- PASS

Bar probe: 1/1 (60513). Validity 2/2, 2/2 PASS. The mechanism
honored the derived-fact contradiction.

Note on the mechanism (recorded, not a bar): the PASS is via
direct-fact shadowing, not graph revision. The contradiction
OBSERVE (60501,60909,60513) became a direct last-write-wins fact
on the derived relation, which shadows the 2-hop promoted graph.
The revise_on_contradict revert path did not trigger because the
contradiction targeted the derived relation itself, not a taught
link within the graph. This is a simpler operator than genuine
derived-fact revision, but it satisfies the bar as written.

### PF-C2: cross-relation revision transfer -- FAIL

Revised-relation probe: 1/1 (60621; per-key patch works). Transfer
probe: 0/1 (60711, original law; no transfer). Validity 2/2, 2/2
PASS. Failure mode: revision is per-key and per-relation; the +20
shift observed on relation 61001 does not transfer to the
analogous relation 61002. The mechanism patches instances; it does
not abstract revision patterns across relations.

## Mechanism verdicts

- Mechanism (a) runtime executable-graph construction: FAILS.
  PF-A1 FAIL (retrieval shadows construction); PF-A2 FAIL (bar).
  Corroborates v3 M1: no procedure abstraction; BFS traversal with
  oracle verification is not construction.
- Mechanism (b) learner-originated uncertainty to guide to action:
  FAILS. PF-B1 FAIL (no selective resolution); PF-B2 FAIL (no
  discrimination under concurrency). Corroborates v3 M2: constant
  action, no resolution transition.
- Mechanism (c) counterexample-driven revision: FAILS. PF-C1 PASS
  (via direct-fact shadowing); PF-C2 FAIL (no cross-relation
  transfer). Corroborates v3 M3: per-key patching, no
  generalization; revision does not transfer across relations.

## What this battery establishes

Mechanism-targeted evidence only (standing ruling). The three
mechanisms fail on materially different structures from FW1-FW9
and v3, with exact failure modes:

(a) Construction loses to retrieval when both are available
    (PF-A1: 60999 preferred over 60902); BFS+oracle is not
    procedure abstraction (PF-A2 caveat).

(b) Guides are constant (30) and persistent; partial resolution of
    concurrent guides does not change the action (PF-B1); floods
    do not induce discrimination (PF-B2).

(c) Derived-fact contradictions are handled by direct-fact
    shadowing, not graph revision (PF-C1 note); revisions do not
    transfer across relations (PF-C2: 60711 not 60721).

No L3 claim. Criterion 0 not met (per prereg section 8).

## Evidence paths

- Prereg: docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY/PREREG_POSTFREEZE.md
- Tools: pf_worldgen.zag, pf_sealed_score.zag, pf_controls.zag,
  pf_audit_noleak.zag (and _bin binaries).
- Worlds and manifest: pf_worlds/ (PF_MANIFEST.sha256).
- Transcripts: pf_runs/ (per-world per-run .trans).
- Control outputs: pf_controls_out/.
