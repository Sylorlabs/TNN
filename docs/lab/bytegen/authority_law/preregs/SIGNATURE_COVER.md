# Signature cover — frozen authority battery preregs (4)

**Decision under which these preregs are written:** Micah APPROVED option B
(2026-09-24) — the T1–T3 three-gate test as universal law: output feedback
earns authority only if (T1) faults are detectable against plan-derived
expectation, (T2) the correction map is plan-pure (constant in measured
output, Lipschitz-0, idempotent), (T3) the output is epistemically safe to
re-ingest. Source: `docs/lab/bytegen/authority_question/DECISION_BRIEF.md`
at commit `fce3cf19f3af9ed825df7db1419c24f20b4a67f8`, blob SHA
`49d7efe186aefd9ae67e24708495bef1392f2f8f` (VERIFIED via GitHub API).

All four preregs are PROPOSAL ONLY — not run, not frozen. They are
signature-ready governance items prepared by the Authority-Battery PREREG
crew. The T1–T3 principle is law by the 2026-09-24 decision; the batteries
settle per-path *instantiations* and wrong-rule falsification only.

## The four preregs

| # | File | Battery | Decision instantiation | What it settles |
|---|---|---|---|---|
| 1 | `PREREG_VFB1_video.md` | VFB-1 video fault battery | Video PASSES T1–T3: plan-absolute rendering + exception detect-and-reassert per frame; piece 3 (output-conditioned scene events) denied | (a) piece 2 heals artifact faults to 0 differing bytes; (b) false positives are no-ops; (c) the continuous servo wrong-rule arm (B-TAX) degrades native 1.0 recurrence as predicted; (d) the self-referential latch prototype (B-CASCADE) cascades as predicted, justifying the piece-3 denial; (e) sub-floor faults are honestly invisible |
| 2 | `PREREG_IFB1_image.md` | IFB-1 image fault battery | Image PASSES T1–T3: plan sole authority; exception detect-and-reassert with plan-pure re-render; bit-exact detection; no continuous feedback; piece 3 audited empty | K1–K7: healing exactness, no harm, detection completeness, one-step convergence, and K5 — the wrong-rule class (W-SERVO, W-FORWARD, W-GLOBAL, W-SEAM, W-NOPLAN) fails as predicted |
| 3 | `PREREG_DFB1_dialogue.md` | DFB-1 dialogue negative-control battery | Dialogue FAILS T3 categorically: no output feedback authority; plan absolute; deliberation-layer veto only | The 8-kill battery: KB/fact-arena digests immutable across hostile dialogues; no system-emitted claim lands in stores; adversarial feedback-injection families (FI-1..FI-4) all refused/neutralized; the `last_fid` tie-break stays bounded; `novelty_ok` stays measurement-only; functional bars (370 turns) preserved — the rule fails gracefully, wrong rules die |
| 4 | `PREREG_SFB1_story.md` | SFB-1 story battery | Story: plan-sole-authority; renderer has no eyes; (D) deliberation-layer reading permitted, (G) generative feedback banned; plan amendments only as deliberated plan events | Arms B and D (permitted exception shapes) heal and tie-or-beat the control on coherence; Arm C — the (G) wrong-rule arm — fails as predicted (K2 coherence degradation, K5 unhealable past), establishing the empirical leg of the (G) ban |

## Common governance (all four)

- **Frozen pins (§0 of each prereg):** branch HEAD `fce3cf19f3af9ed825df7db1419c24f20b4a67f8`
  (verified), each team's draft + FAULT_ANALYSIS.md + WRONG_RULE_COST.md +
  AUTHORITY_RECOMMENDATION.md pinned by blob SHA at that commit (all
  verified), toolchain pinned by filename, decision brief pinned by blob
  SHA. Any pin that fails to resolve is written "UNRESOLVED — needs
  re-pin"; the battery may not start on an unresolved pin.
- **Kill-criteria transcription:** every arm's kill bar transcribed
  verbatim from its team's frozen draft; each wrong-rule arm carries its
  predicted-failure kill criterion ("if this arm passes, the rule is
  wrong"). Any deviation from verbatim is noted in the prereg.
- **Fixtures:** frozen fixture definitions with determinism requirements —
  zero RNG, byte-identical reruns, SHA-256 evidence logged per artifact.
- **Scope guards:** each battery tests the per-path *instantiation*, not
  the universal principle (law by decision).
- **Signature block:** decision (approved / approved-with-amendments /
  rejected) + Micah's signature + date + amendments clause: any change to
  rules, schedule, fixtures, tests, metrics, or kill criteria after
  signature requires his re-approval before running. Bent rules are
  documented and flagged for revert.
- **Zero executions:** no battery, fixture, probe, or harness has been
  built or run under these preregs. Prereg text only — no binaries.

## Explicitly NOT authorized

1. **No battery runs before signature.** No battery, fixture, injector,
   probe, or harness may be built or run under any of these four preregs
   before Micah's signature is recorded on it. Running without signature
   violates program law. (This includes the sibling implementation crew
   building the law itself — they must not run these preregs either.)
2. **No mechanism changes to the emitters.** The four production emitters
   (`f3_emit_wav`, `f3_emit_wav_hifi`, `f3_emit_avi`, `f3_emit_avi_g`) are
   referenced as context only. These preregs authorize zero changes to
   them — the gamma-disease emitter repair is a separate crew's work.
3. **No principle changes.** The batteries cannot amend the T1–T3
   universal principle; only the per-path instantiations are at stake.
4. **No silent retuning.** Frozen heuristics, injectors, and bands may not
   be tuned mid-battery to make a wrong-rule arm fail harder — a wrong-rule
   arm that survives is a result (escalate), not a bug to fix.
5. **The dialogue §3f veto battery is amendment-gated.** It is frozen text
   only; adding it when the deliberation-veto path is built requires a
   prereg amendment and re-signature, not reinterpretation.

## Signature

**Decision (applies to all four preregs as a set; tick one):**

- [ ] **APPROVED** — all four batteries may be run exactly as written. No amendments.
- [ ] **APPROVED WITH AMENDMENTS** — amendments listed below; affected prereg(s) re-frozen after edits, re-signed before any run.
- [ ] **REJECTED**

Amendments (if any): ___________________________________________________

_________________________________________________________________________

Signed: ____________________________ (Micah)

Date: ____________________________
