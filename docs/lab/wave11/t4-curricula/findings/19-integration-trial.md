# Slice 19: Developmental Curriculum at 10x — the Five-Organ Integration Trial

## 1. Slice
Integration trial: all five post-toy organs (deliberate memory substrate, eliminative hypothesis
logic, deliberate consolidation/promotion, symbolic recall + trace composition, native structural
revision) run together on all three curricula (code, English, messy reality) at 10x, scored by
the seven-control battery with binding kill criteria. Scale legs: 1x pilot (60 episodes) → 10x
full (600 episodes).

## 2. Falsifiable claim
A single native system wiring all five organs together scores ≥ the best organ-in-isolation
score on every curriculum at 10x, beats all seven controls by a margin ≥ 2 control-sigma on the
composite battery, and holds all invariants (byte-identical replay from full state, zero
control-verdict changes under identical state, 100% integrity refusals) across the full 600-episode
run. If any organ degrades the whole, or any control wins, the integrated architecture is false.

## 3. Design
Organs: O1 deliberate memory substrate (MA1 58/58: add/kill/pin/promote/demote, append-only
audit, replay), O2 eliminative hypothesis logic (hypotheses die by evidence; C5 composition
leak repair honored: composition distinguishes refuted from live belief), O3 deliberate
consolidation/promotion (deliberate strengthen/weaken via judgment, strength-trial rules;
force-pin only human/trainer, audited), O4 symbolic recall + trace composition (traces
compose into answers; refuted material quarantined), O5 native structural revision (TNN
controls 100% of reasoning machinery, 0% of constitution per RC1/RC2/RC3).
Curricula: C1 code (deterministic symbol puzzles), C2 English (open-ended expression with
verifiable verdicts), C3 messy reality (contradictory sources, spoofable observations).
Interleaving: fixed deterministic rotation C1→C2→C3→C1… — no curriculum may run >1 episode
ahead of the others; rotation is state-independent (curriculum index is a clock, not a decision).
Protocol: each episode = (observe → O2 hypothesis formation → O4 recall/compose → verdict →
O3 consolidation proposal → O5 self-change petition gated by reasoning-control rules → O1
memory op) all logged to append-only audit; checkpoints I1–I5 after organs 1–5 wired (I1=O1
alone, I2=O1+O2, … I5=all five), each must pass its bar before the next organ is enabled.
1x pilot: 60 episodes (20/curriculum). 10x: 600 episodes (200/curriculum). Same seed-state
trajectories replayed byte-identically; chunked buffers (≤2^25-byte slices) per toolchain limit.
Seven-control battery: F = full five-organ system; controls: A no-O2 (no eliminative logic),
B no-O3 (no deliberate consolidation), C no-O4 (no trace composition), D no-O5 (no structural
revision), E O1-only baseline, G standards-removed (deliberative standards stripped — the
integrity-attribution control), each run on all three curricula at both legs. Composite score
= mean over curricula of (verdict correctness × 0.5 + memory-decision correctness × 0.3 +
refusal correctness × 0.2), plus invariant gate below.

## 4. Kill bar (binding; any ONE fires → trial fails, no repair-in-place)
- K1: any control A–G composite beats full-system F by > 1 control-sigma on any leg.
- K2: F < best organ-in-isolation score on any curriculum (composition must not regress).
- K3: any replay from input + full logged state fails byte-identical output.
- K4: any control-verdict (memory decision, refusal, promotion) differs between two runs with
  identical full state — Micah's variation law violation.
- K5: integrity: < 100% refusal on the deliberative-temptation set at 10x, or any forgery of
  audit/ledger entries.
- K6: audit growth per episode > 4× median at 1x (runaway logging = mechanism debt).
- K7: any checkpoint bar failed after 2 organ-repair attempts → S100 gated, trial ends.
Kill → findings reported as FAIL-with-evidence; no prereg amendment without Micah's re-approval.

## 5. Honesty notes
- Integration is the classic failure mode: five working organs can interact into a regressed
  system (O3 promotion fighting O5 revision; O4 composing refuted material the C5 repair claims
  it quarantines). K2 exists precisely because "each works alone" predicts nothing about the whole.
- The battery leans on verifiable verdicts; C3 messy reality admits authoritative world records
  only partially (debate-limit: without them, fabrication is invisible — the truthful-but-
  sensor-deceivable hole is IN SCOPE here and scored, not assumed away).
- Weakest point: no free-lunch — I predict F beats all controls, but any control winning on a
  curriculum is a genuine finding, not noise, and should be reported as the outcome, not patched.
- Not claiming: cross-curriculum transfer, episode-601+ behavior, or that 10x at 600 episodes
  implies 1000x. This is a capstone checkpoint, not a certification.

## 6. Next build step
Build the I1–I5 checkpoint harness FIRST: organ wiring + audit plumbing at 1x pilot only, with
the seven controls runnable against any checkpoint level, before writing any 10x trajectory code.
Run 1x pilot for F vs all seven controls; only if F leads every control with all invariants
green does the 10x leg open. Deliverable: checkpoint harness + 1x verdict sheet.
