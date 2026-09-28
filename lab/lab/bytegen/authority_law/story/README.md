# Story — authority law instantiation (plan absolute, renderer has no eyes)

Implements Micah's APPROVED option B for the story path (2026-09-24): **the
plan is the sole authority over every rendered byte.** Story FAILS the
T1–T3 gate for a sensor: rendered text carries strictly less information
than the plan (the renderer is a pure function — the plan can compute every
byte), so there is no information gap for a sensor to fill; a story sensor
would be theater or fabrication.

## The rule, as built

1. **Generative authority**: the beat sheet (`beat`/`beat_n`/`seq_*` + class
   tables + tv + P/L + plan annotations `ann`) is the sole authority over
   every rendered byte. Each beat renderer (`r_setup`, `r_compl`,
   `r_climax`, `r_resol`) is a pure function of the plan — no carried
   output state, no output-conditioned branching. Beat render signatures
   contain no rendered-bytes input. Cohesion improvements enter only as
   beat-sheet annotations (planned, audited — see `r_compl`'s `ann[1]`
   deliberated annotation), never sensed.
2. **Exception authority (Piece-2-shaped)**: a stateless detector
   (`detect_beat`) reads rendered beats against plan-derived expectations
   only (anchor presence per beat, closing-line presence recomputed
   plan-pure via `r_close`). On fault, `heal_beat` re-renders the affected
   beat plan-pure. Correction bytes ∈ {plan-pure}; constant map
   (Lipschitz-0), idempotent; false positives are no-ops.
3. **Plan-event authority (deliberation-gated)**: thread audits and external
   edits amend the plan as discrete deliberated plan events, recorded in
   the audit trail — `seq_r` extended with **r=4 AUDIT_REPAIR** and
   **r=5 EXTERNAL_EDIT** (`apply_external_edit` accepts only deliberated
   codes; unknown codes refused). The renderer never sees the event; it
   sees the amended plan. Re-render is plan-pure.
4. **(G) banned, structurally**: the renderer registry (`reg`) lists every
   render entry point with input masks; `gate_register` **refuses** any
   mask containing `PORT_RENDERED`. `attempt_g_wire` shows the attack shape
   — handing beat n the prior beat's rendered bytes — and that the bytes
   cannot flow anywhere: no such input port exists.

## Files

- `story_plan_absolute.zag` — the instantiation + adversarial probes.
- `story_evidence.txt` — full probe output (SHAs included).
- `R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag` — pinned integrity
  substrate (copied from `GOALB_STORY/src`).

## Build / run

```
cd ~/workspace/tnn-lab/bytegen/authority_law/story
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 story_plan_absolute.zag -o story_bin
./story_bin all        # A, B, C, D, E
./story_bin a|b|c|d|e
```

Pure Zag, deterministic, zero RNG. `story_bin` is a build artifact and is
NOT committed.

## Verification (see story_evidence.txt)

- **A** fault injection: dropped anchor word (beat 1), dropped closing
  line (beat 3), corrupted byte run inside the anchor (beat 0) →
  detector fires on all three; plan-pure re-render is **byte-identical**
  to the clean render in every case; clean beats produce zero detections
  and heal is a byte-identical no-op (false positives are no-ops).
- **B** (G)-ban attack: `gate_register(beat2, PLAN|RENDERED)` →
  **REFUSED**, registry unchanged; `attempt_g_wire` output == plan-pure
  render; story SHA unchanged by the attack
  (`ffa24a2fb2fa95c99043af13efa8d96af5c9f1f704273a6199269c118773c56d`).
- **C** plan-event path: deliberated external edit (`r=5 EXTERNAL_EDIT`,
  seq 12→13) amends the plan; re-render differs from the old render
  **exactly in the amended beat** (beats 0/2/3 byte-identical, beat 1
  gains the planned "feared the thunderstorm" sentence); unknown edit
  code refused, plan untouched.
- **D** reruns: full plan+render ×3 → byte-identical (SHA
  `ffa24a2fb2fa95c99043af13efa8d96af5c9f1f704273a6199269c118773c56d` ×3).
- **E** thread audit (H2): injected dropped object-thread anchor detected
  from the rendered text; repair logged as `r=4 AUDIT_REPAIR`; plan-pure
  re-render restores the anchor byte-identically.

Note: the frozen preregistered battery is NOT run here (needs Micah's
signature; a sibling crew is drafting it). These are smoke-level probes.
