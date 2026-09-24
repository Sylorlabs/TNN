# Bytegen authority question — decision brief for Micah

**Question:** the v2 hybrid's authority rules (output feedback earns authority only on the exception path + octave-scale pitch events; bounded, revocable; plan keeps last word via re-render) are specified for AUDIO only. Should they be universal across generation paths, or per-path? Which generation method wins on each path?

**Swarm:** four teams surveyed the native video, image, dialogue, and story paths (all file:line-cited against current sources), argued both sides internally, and delivered per-path authority rules + frozen fault-battery preregs (proposed, not run). Full transcripts: `teams/<video|image|dialogue|story>/`.

## What the four teams found

| Path | Native generation | Recommended rule | Piece 3? |
|---|---|---|---|
| Audio (done) | stateful-sequential | v2 three-piece: PAR-default + exception re-assert + RESPOND octave latch | yes (measured ±97¢ sensor bias) |
| Video | PAR at frame granularity, stateful-sequential within a frame; recurrence 1.0 by construction | plan-absolute + exception detect-and-reassert per frame | **no** — no output-conditioned event class exists; a servo would *create* the coherence tax from nothing |
| Image | three native paths: field.zag strokes (stateful-sequential), design canvas (carried state), disc.zag (true-PARALLEL, pixel = pure F(coords, seed)) | image-specific three-piece instantiation | **audited empty** — no discrete measured-plan-fact exists |
| Dialogue | template slot-fill, atomic assembly, zero carried output state — a different kind of generation entirely | **no output feedback authority; plan absolute** (+ deliberation-layer veto carve-out) | n/a — the question has no referent |
| Story | closest native analog of audio PAR: `story = F(plan)`, zero carried beat state; plan threads = narrative motif recurrence | plan-sole-authority; renderer has no eyes; plan amendments only as discrete deliberated events | **no** — rendered text contains strictly less information than the plan; no synth↔model gap, so a "story sensor" would be theater or fabrication |

**The convergence (unplanned — all four teams got here independently):** universal PRINCIPLE, per-path INSTANTIATION. No team argued for stamping audio's three mechanisms onto every path; no team argued for per-path anarchy either.

The principle, in its sharpest form (dialogue team's T1–T3 gate — feedback earns authority on a path only if):
- **T1:** the fault is detectable against a *plan-derived* expectation (not the output's own statistics);
- **T2:** the correction map is *plan-pure* — constant in the measured output (Lipschitz-0), so false positives are no-ops;
- **T3:** the output is *epistemically safe to re-ingest* — measuring it cannot install content the plan didn't author.

Audio passes T1–T3. Video passes T1–T2, Piece 3 vacuous. Image passes T1–T2 with bit-exact detection (re-render + diff — strictly stronger than audio's band predicate). Dialogue **fails T3 categorically** (propositional output; re-ingestion risks belief corruption) and story has no T1 referent for a sensor (no information gap).

## Load-bearing distinctions (use these however you decide)

1. **(D) deliberation-layer reading vs (G) generative feedback** (story team). Reading output as *data for detection/diagnosis*, acting only on the plan = (D), preserves plan authority. Computing unit n from rendered bytes 0..n−1 = (G), destroys it. Every genuine help the swarm found is (D)-shaped; every corruption is (G)-shaped. This distinction is bigger than bytegen — it's the same line H6 (self-PAM) and the consciousness law walk.
2. **d_blend is NOT generative feedback** (image team, five-point proof). The pixel read-back is an arithmetic operand in a plan-fixed formula, never a decision input. Data-flow vs control-flow over measured output. This kills the "image already does feedback" objection before it starts.
3. **The gamma disease is in production emitters** (image team find): four output-derived peak normalizers in `f3_emit_wav`, `f3_emit_wav_hifi`, legacy `f3_emit_avi`, `f3_emit_avi_g` — output statistics feeding back into scaling decisions, the exact pattern that breaks bit-identity. Cautionary specimen, not precedent. Worth a repair ticket regardless of this decision.

## Options

### Option B — Universal principle, per-path instantiation ⭐ swarm's convergence, my recommendation
Adopt the T1–T3 gate (or story team's 4-clause equivalent) as law. Each path instantiates its own pieces and carries a **justification burden**: any path wanting output→plan contact must name the information gap the output fills that the plan can't compute. Audio can (waveform corruption, pitch-octave facts). Video/image get the exception path. Story and dialogue get plan-absolute (+ deliberation-layer mechanisms, which are (D) not (G)).
- **Costs:** per-path spec work; someone must keep the gate (re-litigation risk — image team flagged that N philosophies would force re-fighting Attacks 1/4/6/11 per path; the justification burden is the mitigation).
- **Risks:** drift — a path smuggles (G) in under (D) language. Mitigation: the T2 contractivity proof is checkable per path.
- **Settling experiments:** the four proposed fault batteries (each includes wrong-rule arms with *predicted-failure* kill criteria — VFB-1's B-TAX/B-CASCADE, image K5, dialogue's 8-kill battery, story's (G)-arm). If a wrong-rule arm passes, the rule is wrong. Falsifiable per path.

### Option C — Audio-only hybrid, plan-absolute elsewhere (conservative fallback)
Keep v2 for audio; everywhere else plan-absolute with no exception path at all. Coherent, cheapest to specify.
- **Costs:** real faults go unhealed — video VF-1–VF-4 artifacts, image region corruption/bit-rot ship as-is.
- **Risks:** silent corruption in production on the two paths with genuine plan-independent fault classes.
- **Settling experiment:** run just the exception-path batteries on video/image. If healing works with zero false-positive cost, C is leaving proven value on the table.

### Option D — Plan-absolute everywhere (purist)
No feedback machinery on any path, not even exception paths. Zero feedback code to rot.
- **Costs:** a single corrupted block/frame/region ships, always; no healing anywhere.
- **Risks:** maximal on the fault side. Fails the video/image fault batteries by construction.
- **Settling experiment:** fault-injection batteries — D predicts unhealed artifacts; the only question is whether you can live with them.

### Option A — Universal mechanisms (v2-everywhere) — ranked last, not recommended
Stamp audio's three pieces onto every path.
- **Why it loses:** the mechanisms don't transfer. Dialogue's octave latch would be a mechanism with no referent; story's sensor would be theater or fabrication; dialogue re-ingestion risks belief corruption (fails T3). All four teams' evidence says the *safety proofs* are what transfer, not the parts list.

## What needs your word

1. **The decision itself:** B, C, D (or your own variant) — no battery runs until you pick.
2. **Battery sign-offs:** each team's frozen prereg needs your signature per governance before running (they're written and waiting in `teams/*/`).
3. **Independent of the decision:** the gamma-disease normalizers in the four emitters (finding #3 above) — repair or keep? I'd say repair; output-derived scaling is exactly what the v2 spec deleted.

## Honest caveats

- The swarm surveyed sources; it did not run anything. Every recommendation rests on source reading + the audio battery's transferred math, not new measurements.
- Video's "recurrence 1.0 by construction" and image's bit-exact detection are claims from code reading — the batteries would verify them.
- The (D)/(G) distinction is doing heavy lifting in story/dialogue; if you think it's wordplay, say so and I'll have it attacked properly.
