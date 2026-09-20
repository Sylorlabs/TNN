# Slice 05 — Judgment-Stability Test for Arm B (fenced RNG)

1. **Slice** — slice 05: judgment-stability metric — differential proof that Arm B's protected
   outputs (memory decisions, integrity refusals, verdicts, ledger contents) are identical to
   Arm C's across head-to-head episodes, with the RNG fenced to expression only.

2. **Falsifiable claim** — For every head-to-head episode pair (Arm B vs Arm C) run on identical
   inputs AND identical full internal state, the protected-output vectors — memory ops
   (kill/pin/promote/demote/strengthen/weaken, with slot targets), integrity refusal booleans,
   verdict codes, and full ledger byte contents — are identical. The seeded RNG (Arm B only,
   enumerated at prereg points: tie-breaks, phrasing candidates, exploration) changes ONLY
   expression channels (wording, ordering of equal-weight evidence, elaboration depth).

3. **Design** — Differential procedure, Zag-flavored spec:
   - Build ONE harness binary with a compile-time arm selector (argv[1] = "B"/"C"); identical
     code path, zero conditional divergence in protected code (fence = structural, not
     advisory: RNG symbols are absent from the protected compile unit; verify by grep on the
     emitted native — no `rng_*` call sites outside `expr/`).
   - Episode pair protocol: snapshot full state S to file; run arm B on (input I, state S,
     seed K) → capture protected vector P_B and ledger bytes L_B; restore S byte-identically;
     run arm C on (I, S) with no seed → P_C, L_C. Never feed B's outputs back into C's run.
   - Protected vector P = ordered record: (op_codes[slot] for all memory ops), refusal bits,
     verdict codes. Ledger L = raw append-only bytes (MA1: docs/lab/wave3/ma1 — replay to
     exact state; same tooling proves L_B == L_C).
   - Expression channel E (phrasing/ordering/depth) is captured separately and EXCLUDED from
     the stability comparison; E_B may differ from E_C — that difference is the honest
     RNG signal, not a violation.
   - Determinism control: replay (I, S, K) for arm B twice; assert byte-identical (repro-
     ducibility = input + logged state, per standing law 2). This isolates fence leaks from
     RNG nondeterminism.

4. **Kill bar** — Zero tolerance. ONE episode pair in the head-to-head set where any protected
   output differs (P_B ≠ P_C or L_B ≠ L_C, after excluding logging-only timestamps) fires the
   bar. Minimum set: 200 episode pairs spanning the trap families proven live in wave5/6
   (137/137 checks, 1440/1440 trap-correct — docs/lab/wave5, docs/lab/wave6) plus 50
   deliberate-memory-op episodes (kill/pin/promote sequences, MA1 58/58 — docs/lab/wave3/ma1).
   Firing condition: diff ≠ ∅ on any protected channel ⇒ arm fails judgment stability;
   see §5 diagnostic for which thing dies.

5. **Honesty notes** — The interesting case: a protected diff has TWO possible causes and
   they kill different things. **Fencing failure (kill the implementation):** the RNG value
   leaked into a protected path — e.g. a tie-break seed selected which memory slot to kill,
   or a phrasing candidate count shifted an elaboration depth that a verdict threshold reads.
   **Fence-spec failure (kill the spec):** the fence's partition of "expression" vs "decision"
   is wrong — e.g. Micah's variation goal requires expression variation, but if ordering of
   evidence is protected-relevant (eliminative logic kills by evidence ORDER in some design),
   then "ordering" was misclassified as expression. Diagnostic procedure: (a) extract the
   RNG consumption trace — every `rng_draw` site with its call-site ID and the downstream
   data-flow slice; (b) replay the pair with the seed replaced by a constant (K→0): if the
   diff VANISHES, the draw was causally downstream of a protected input — fencing failure,
   kill implementation; (c) if the diff PERSISTS with K=0, the protected path was
   seed-independent and the divergence is structural — the two arms' protected code differs,
   which means either the fence spec allowed expression state into the protected channel or
   the arms were not identical to begin with — kill the spec, re-prereg the partition.
   (d) Confirm with a mutation probe: force that draw site to Arm C's value in Arm B; diff
   must vanish for a clean fencing-failure verdict. Weakest point: step (c) can misclassify
   a build artifact (stale .zagd cache, diverged binary) as a spec failure — the constant-seed
   replay MUST use binaries built in one pass with the arm selector only. I am NOT claiming
   the fence classification is correct a priori; the diagnostic exists precisely because the
   boundary between "expression" and "judgment" is the experiment's hardest judgment call.

6. **Next build step** — Build the single differential harness (arm-selector binary + state
   snapshot/restore + P/L capture) FIRST, before any RNG injection: run 50 pairs B≡C with the
   RNG compiled out to prove the harness itself produces zero protected diffs (baseline).
   Only then enable Arm B's seeded draws. If the baseline is not clean, nothing downstream
   is interpretable.
