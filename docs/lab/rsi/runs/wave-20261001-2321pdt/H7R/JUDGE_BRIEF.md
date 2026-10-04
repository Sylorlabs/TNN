# JUDGE_BRIEF: H7R (wave-20261001-2321pdt)

## Provenance header

- RENDER_SHA: 11eb54f6f (sealed evaluation commit; this brief rendered against it)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: TNN3H7 SUBSTRATE-ABSENT (wave-20261001-2021pdt: no learner
  construction process and no contradiction-to-construction trigger; H7 prereg
  never frozen) -> TNN3-SUBSTRATE DESIGN-COMPLETE (wave-20261001-2321pdt: generic
  contradiction trigger lt_fire plus construction service lb_run as generic
  machinery, frozen kill bars KB-H7R, honest boundary that ticket authoring by
  the learner and REDERIVE interpretation are the re-attempts' hypotheses)
  -> H7R re-attempt (this lane).
- NEW_KNOWLEDGE_CLAIM: On the prototype substrate, the generic contradiction
  trigger plus the construction service suffice for genuine contradiction-driven
  re-derivation: a generic learner-side consumer that copies the stale
  derivation's ticket steps with literal re-resolution against the contradiction's
  new fact rebuilds executable corrected structures on 12/12 sealed cases with
  zero researcher-authored ticket content.

Documentation rule observed: no em-dashes in this document.

## Verdict

BUILD-PASS. All frozen bars pass on 3/3 byte-identical sealed runs.

## Numbers vs frozen KB-H7R bars (12 contradiction cases, 3 sealed worlds x 4)

- B1 substrate: PASS. The adopted build's dv_v2() re-run passes on the extracted
  prototype (substrate extracted byte-identical from commit a11dde4b9, sha256
  77303b829516e95489a0c9be97dbbe0d7a1bf8cb84b2b8025591bb609772eede): every
  ev_observe contradiction yields exactly one REDERIVE ticket; confirms and pure
  teaches yield none. Per-event asserts confirm each ticket links the superseded
  and the new fact (one ET_REF target superseded via the substrate's own ET_CON
  signal, one live, carrying the event's key and new value).
- B2 sealed: PASS. The consumer rebuilds via lb_run against the live fact store;
  held-out probe queries executed on the frozen 4-op ISA return the corrected
  answer on 12/12 cases (100 percent, bar 80 percent); margin over the stale
  structure is 100 percentage points (bar 60).
- B3 non-treadmill: PASS. t2_sig of the rebuilt graph differs from the stale
  graph on 12/12 cases (100 percent, bar 80 percent). The re-derived structures
  do not re-learn the same wrong thing; the kill outcome did not trigger.
- B4 ablation: PASS. Executing the stale (superseded) root on the probe returns
  the superseded value on 12/12 cases: without the rebuilt graph, answers stay
  stale.
- B5 confirms: PASS. Confirm events trigger zero REDERIVE tickets and zero
  consumer authoring (ticket and build-ticket counts unchanged across all
  confirm sequences).
- B6 distractors: PASS. Contradictions on facts with no derivation are consumed
  with zero BUILD tickets authored (6/6 distractor events).
- P1 determinism: PASS. Three runs, stdout byte-identical (sha256
  f222c5e1d957c98b905a77e6470238821d0ca93e2342718aa9efb3cd7816bdce x3).
- P2 K-C0A audit: PASS. Zero new semantic cases by committed-source grep
  (KC0A_AUDIT.md): the driver contains zero ticket-authoring calls (literal
  prereg criterion), the consumer's branches test only structural metadata and
  live learner-state positions, no world constant appears in any conditional
  test outside measurement scoring, and no new node types, edge types, or
  relation codes were introduced.

No L3 authorship claim is made; the verdict concerns the re-derivation mechanism
against the frozen bars. No SUBSTRATE-INSUFFICIENT gap was encountered: the
trigger fired and the re-derived structures were authored and executed entirely
through the generic service (lb_ticket_new / lb_step_add / lb_run / execute).

## Commit chain (all local, branch tnn-native-lab, no pushes)

1. `144deb24a`: prereg frozen ALONE (H7R_PREREG.md, NAMECHECK.md). No
   implementation in this commit. World values were chosen after this freeze.
2. `11eb54f6f`: implementation + sealed evaluation. Consumer (generic REDERIVE
   interpreter, H7R_PREREG.md section 2), sealed driver (world tables, protocol,
   measurement), substrate extracted read-only from a11dde4b9, build script,
   built source and binary, 3/3 sealed logs, K-C0A audit. RENDER_SHA above.

## Evidence paths

- Prereg: docs/lab/rsi/runs/wave-20261001-2321pdt/H7R/H7R_PREREG.md
- Consumer: docs/lab/rsi/runs/wave-20261001-2321pdt/H7R/h7r_consumer.zag
- Driver: docs/lab/rsi/runs/wave-20261001-2321pdt/H7R/h7r_driver.zag
- Build: docs/lab/rsi/runs/wave-20261001-2321pdt/H7R/build_h7r.sh
- Sealed logs (byte-identical x3):
  docs/lab/rsi/runs/wave-20261001-2321pdt/H7R/sealed_run1.log
  (+ sealed_run2.log, sealed_run3.log)
- K-C0A audit: docs/lab/rsi/runs/wave-20261001-2321pdt/H7R/KC0A_AUDIT.md
- Frozen substrate source: docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3-SUBSTRATE/
  (prereg be112b78f, prototype a11dde4b9)
- Frozen tnn2.zag: never modified (no edits; prototype built by additive
  extraction per the substrate lane's build_proto.sh lineage)

## Process notes

- Safebin toolchain guard verified at Step 0 (`which python3` prints nothing);
  pure Zag throughout; no forbidden interpreter invoked.
- One cosmetic issue handled transparently: the driver's header comment
  mentioned the ticket-authoring API names, tripping the literal authorship
  grep. The comment was reworded (no logic touched), the binary rebuilt, and
  all three sealed runs re-executed: logs remained byte-identical to the
  pre-change hash, proving zero behavioral effect.
- Recommended follow-ups (not verdicts): the consumer's derive schema is a
  fixed generic prior (mirrors the substrate's fact query semantics); replacing
  it with learner-invented construction is H1/H2R/H3 territory. Wiring the
  consumer to run inside the event flow (rather than harness-invoked between
  events) is a governance decision about the substrate, not taken here.
