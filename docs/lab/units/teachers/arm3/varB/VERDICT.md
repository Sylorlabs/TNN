# VERDICT — ARM-3 Variation B (teacher_id=3, phase-scheduler teacher)

Date: 2026-09-21. Builder: subagent (overnight run). Spec: SPEC.md (committed).

## Verdict: PASS — arm-3 bar (3) "shows adaptive judgment" is met

The Track B FAIL this rebuilds from was: *"the driver consumes
parent-fed/canned scripts; no history-conditioned proposal policy
(spec, stimulus, history) → proposal exists in the teacher — the adaptation
lives in the parent script, not the teacher."*

Variation B removes that failure mode structurally. The teacher binary itself
reads the session history tape (HIST v1) and runs a deterministic aggregate
phase scheduler — INTRODUCE → CORROBORATE → RELATE → CONSOLIDATE — whose
transitions are driven only by aggregate history (adoption rate over the last
10, consecutive rejections, appeals used). There is no parent script choosing
proposals; `verify.py` only feeds histories and checks outputs.

### Adaptive-judgment evidence (all in evidence/)

- Four histories → four phases, from the teacher alone:
  - empty → INTRODUCE (8 WORD_SPAN, conf 152–164, single groundings)
  - 4 adopts → CORROBORATE (re-proposes adopted spans, 3 groundings, conf 210)
  - 8 adopts → RELATE (3 GROUP + 3 SAME_AS + 1 BOUNDARY, conf 145–154)
  - mixed 7-adopt/2×rejected → CONSOLIDATE (2 RETRACTs of spans 7 and 10,
    then 2 BOUNDARY summaries, ≤4 proposals)
- Rejection-heavy vs adoption-heavy: INTRODUCE vs RELATE — different phases
  and **disjoint** proposal kinds (WORD_SPAN vs GROUP/SAME_AS/BOUNDARY).
- Three-turn chain over real turns: INTRODUCE → CORROBORATE → RELATE as
  adoptions accumulate.
- Rejection path shows judgment, not repetition: 2 appeals with *new*
  evidence (occurrence #2 groundings, escalated confidence 162/170), then
  fresh words from a skipped region (fresh=1, REGION_SKIP=256).
- Consolidation retracts exactly the twice-rejected spans (7, 10).

### Preserved requirements (all verified, see evidence/VERIFY_LOG.txt)

- §P iron rules: 21/21 malformed-input cases → exact exit code, one stderr
  line, zero stdout bytes.
- §C: conservative cumulative monitor kept (strictly stronger than frozen
  B.8's rolling-200; documented deviation, parked for Micah). Clean teaching
  does not fire; smuggle (code 1), vocab-dump (code 2) fire; near-miss clean.
- Determinism: N=5 byte-identical; 5/5 adversarial heap/environment battery
  (MALLOC_PERTURB_ no-op documented, ASLR on/off, 200KB env, 512KB stack,
  cwd+stdin). Allocator finding: raw mmap arenas, no glibc malloc; all state
  arrays explicitly zeroed at startup.
- Negative declarations hold: no RNG/wallclock tokens in teacher.zag; per-run
  fixed-size buffers re-derived every invocation; no cross-session learning.
- Confidence selective, never 255 (parser rejects 255 as tripwire bait);
  spans only — no strings, token IDs, commands, or embeddings.

### Honest notes

- During the build I found and fixed a latent uninitialized-heap-array bug
  (span-state arrays read at freshly-registered slots); the fix is explicit
  `t_zero` at startup, verified by the full battery afterward.
- The "appeals-used" aggregate was tightened mid-build to count only
  re-proposals of *rejected* spans (corroborations are not appeals); SPEC.md
  §4 records the final definition. In INTRODUCE all definitions coincide.
- The teacher proposes only WORD_SPAN/GROUP/SAME_AS/BOUNDARY/RETRACT per the
  frozen kinds; teaching "style" differences live in phase, batch composition,
  grounding count, and confidence — which is exactly the adaptive-judgment bar.

Commit: text files only (SPEC.md, teacher.zag, tools/, fixtures/*.py,
fixtures/*.txt, verify.py, evidence/, VERDICT.md). Build binary and any
.zagd/.zag-cache artifacts excluded.
