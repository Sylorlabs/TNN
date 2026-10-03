# CANDIDATE LANE: wave-20260927-1121pdt

Worker: candidate lane. Run-start HEAD a98ccd6a2 (branch tnn-native-lab).
Output: gate checks for the four 0821pdt prereg design drafts, one frozen
prereg (EXP1c), no new candidate implementation, continual_learning
interaction assessment, zero-Python attestation.

## 1. Freeze-gate checks (per draft, with evidence)

### a. EXP1c: SATISFIABLE. Frozen this wave.

Gate: the six withheld EXP1b red-team corrections committed in the repo
(or a freezing wave recording reasons to proceed).

Finding: all six corrections plus the WAVE_NOTES_EXP1B.md deliverable are
committed, in the wave-20260927-0221pdt coordinator commit 463b115b6.
Content-verified, not just filename-verified:

1. evidence_exp1b/A2_ABLATION.md rewrite: documents the actual implemented
   test, the void-reflex dropout confound, and the clean-ablation numbers
   (drop 0 in all 12 variants).
2. False "never builds" claims corrected in evidence_exp1b/EVIDENCE_EXP1B.md:
   I builds a LAMP in 6/12 variants and places it in 5/12 (v2, v5, v7, v8,
   v11); emergent enumeration accidents, causally inert.
3. Heuristic label fixes in evidence_exp1b/NOVELTY_AUDIT.md.
4. Reflex-dependency record in EVIDENCE_EXP1B.md: without the
   implementation-added void-safety reflex, I median drops to 102 with 9/12
   void deaths.
5. Retune-2 verifiability note in EVIDENCE_EXP1B.md: retunes 1-2 left no
   artifacts, so the stopping rule is unverifiable and K1-shopping cannot
   be ruled out.
6. Bounce-bug correction appended to EXP1's BAR_RESULTS.md: the
   identity-reflection bug (hi-side reflection algebraically the identity)
   was introduced in the 2321pdt reimplementation 74565859f, not in the
   original EXP1 commit; K1's KILL verdict direction unchanged.

Deliverable: docs/lab/invention/survival/WAVE_NOTES_EXP1B.md committed in
the same commit. The 0821pdt draft's "six red-team corrections plus the
WAVE_NOTES_EXP1B.md deliverable" maps exactly onto this seven-item set.

Freeze action taken this wave (gate was satisfiable, so the lane froze):

- Commit 5a043af3c: EXP1c training-mass extension. New files
  docs/lab/invention/survival/kb/kb_exp1c.txt and
  docs/lab/invention/survival/kb/kb_p_exp1c.txt: verbatim copies of the
  EXP1b mass with exactly three documented deltas (1200-tick horizon;
  new taught heuristic H9 void-safety; header updated) and one for P
  (Phase 4 loop to tick 1200). EXP1b's verbatim mass files untouched.
- Commit 8b456736b: PREREG_EXP1c_FROZEN.md under
  docs/lab/rsi/runs/wave-20260927-1121pdt/preregs/. FROZEN with kill bars
  K1-K7 carried unchanged from the draft.

Redraft fixes at freeze time (the document was a draft; changes by redraft
only, never post-freeze; kill bars unmoved):

- M4(c) said void-safety was "taught H5". kb.txt already defines H5 as the
  EAT rule (H1 through H8 all taken), so a new H5 would have made the
  training mass self-contradictory and poisoned the K4 novelty audit. The
  taught void-safety heuristic is H9, appended in the new mass and quoted
  verbatim in the frozen M4. This is a drafting-error fix, not a bar move.
- The inherited world-physics template path said "src/world.zag", which
  does not exist at that repo-relative path. The actual committed template
  is docs/lab/invention/survival/src/world.zag (bounce-fixed by 938d188cb).
  Frozen text pins the correct path.

Commit-order self-check: design 59b9df4b0 (0821pdt lane 3) strictly
precedes mass extension 5a043af3c, which strictly precedes freeze
8b456736b. No implementation commit exists yet. Pre-run assertion recorded:
pre-run, no scores seen. Cost budget carried: 144,000 agent-ticks
(12 variants x 5 arms x 1200 ticks x 2 determinism runs), pure Zag, pinned
toolchain src/tools/toolchain/znc_linux_x86_64_abed8aa1 (verified present
in repo).

Implementing wave, take note: the frozen prereg's section 11 records the
freeze commit (8b456736b). Implementation commits must come strictly after.

### b. EXP2-K4: NOT SATISFIABLE this wave. Left QUEUED.

Gate: a failure-trace corpus that predates the freeze must exist (12 real
deliberation failure traces, spec-blind curation, recorded expected
outcomes, pinned by SHA-256).

Finding: no such corpus exists in the repo. The onebrain3/traces/ directory
holds 27 run-output trace files from round-3 measurement (v6_*.txt,
committed under 51b7de35d), not a curated failure corpus: they carry no
recorded expected outcomes, no spec-blind curator attestation, and no
qualifying-rule selection by commit order. The 0221pdt EXP2 follow-up's
holdouts (S2/S3) are construction-guaranteed synthetic probes, which the
judge ruled are fidelity evidence only. Building the corpus is a new
data-collection exercise (run the frozen single-deliberation machinery over
a problem set, find real wrong-verdict or wrongful-decline traces, have a
spec-blind curator select the first 12 by commit order satisfying the
qualifying rule), not a gate check. The draft stays QUEUED until a wave
commits that corpus; the freeze must then come after the corpus commit.

### c. B1-P9: NOT SATISFIABLE this wave. Left QUEUED.

Gate: a genuinely new mechanism (k-family stays DISCARDed, jointly
unsatisfiable; B1 BOUNCE's DISCARD stands and is never re-scored).

Finding: no new B1-class (post-pass recolor) mechanism has been committed
since the 1121pdt DISCARD. Commits touching docs/lab/image_upscale/ since
2026-09-25 12:00 are the LIGHT-FIELD workstream (KILLED clean: BAR1 FAIL
sealed minus 1.853 dB, BAR2 FAIL checkerboard about 3x worse) and the
upscale round-3 honest all-arm kill (7aa40ac0d). The P9 bar set is a
re-freeze template only; per its own section 9, "bars do not invent
mechanisms." The draft stays QUEUED until a genuinely new mechanism
exists. Sensory stand-downs (G1 sunshafts, D-VID-1, ST-1 dead) unchanged.

### d. COMP2-P11: gate zero blocks. Confirmed and left QUEUED.

Quick verification: ruling 6 is still OPEN. No commit since 2026-09-24
renders Micah's ruling 6 (latest mentions: 36eb88f8f and 621e10957 record
the gating; LOOP_STATE line 2791-2792 still lists "CV-P adoption still
doubly gated (ruling 6 pending)"). The draft's frozen gate zero forbids any
implementation commit until he rules. Nothing to freeze; the draft stays
QUEUED. The lane neither decides, relitigates, nor re-presents ruling 6.

## 2. Candidate hunt

The lane order authorizes hunting only if no prereg freezes. Gate a froze
(EXP1c, substantive: the first non-null compositional-choice design in the
invention line, directly answering the 0221pdt judge's forward requirement
and the EXP1b red-team finding that "composition is the broken link"). No
new candidate was implemented this wave. No forced verdicts: nothing is
ready for adopt/discard, and the lane reports that honestly rather than
manufacturing a candidate.

## 3. Verdict recommendations

- EXP1c: FROZEN (8b456736b). Recommendation to the parent: queue for
  implementation by a future wave under the frozen bars; implementing wave
  must run the commit-order self-check and reproduce the section 7
  enumeration bound in evidence.
- EXP2-K4, B1-P9, COMP2-P11: remain QUEUED with the gate findings above.
- No adoption or discard verdicts on any candidate this wave.

## 4. Continual_learning flagship interaction assessment

Scope: docs/lab/continual_learning/ (his flagship: PREREG.md 8c22ffb9b,
RESULTS.md + build/ 36342eb51, line verdict GO; plus in-repo red-team
report 899757bc2 recording NO-GO). His verdicts are not relitigated and
his files were not touched (git diff confirms zero modifications).

Findings and concrete recommendations (for LOOP_STATE.md, not for his
files):

1. LOOP_STATE.md currently contains zero mentions of the flagship even
   though the run-start merge brought it in. Recommendation: add a
   standing his-frontier entry (CLOSED to the loop, never claimed or
   re-certified): canonical paths docs/lab/continual_learning/PREREG.md,
   RESULTS.md, RUNLOG.md, MANIFEST.md, TEACH.md, build/; prereg commit
   8c22ffb9b; build+run commit 36342eb51 with line verdict GO; the
   in-repo red-team report 899757bc2 (NO-GO) exists and is not
   relitigated by the loop; parent decides whether to surface the
   discrepancy to Micah.
2. No loop-maintained code imports his directory (repo-wide grep for
   "continual_learning" outside his dir returns only this wave's fork
   survey noting his six new .zag files). No collision to repair today.
3. Citation rule going forward: his MANIFEST.md pins his vendored
   substrate copies (st_memory_core.zag 474ac0bb..., cl/common.zag
   8aec83cb..., R33_NATIVE_SHA256_V2.zag, R33_NATIVE_IO_V1.zag) plus his
   deviation D1 (psm.zag modified to add a read-only psm_fast_inspect
   helper). Loop worktrees already vendor their own st_memory_core.zag
   and cl/ copies in many wave2/wave3/wave10/wave12 trial dirs. Any future
   loop probe that measures consolidation, retention, or interference on
   the same substrate must cite his MANIFEST SHAs as the canonical
   reference for continual-learning claims, must not present a loop copy
   as canonical, and must not copy his D1 deviation into loop PSM copies
   or treat it as upstream.
4. Provenance rule: his fixtures (build/fixtures/facts.tsv,
   phase4.tsv, probes.tsv, prov.tsv, conseq.tsv) are his closed teaching
   corpus (18 Audubon/Singleton facts). No loop probe may ingest them as
   new probe material; a loop probe reusing the same public-domain texts
   must cite his benchmark as prior work.
5. Boundary rule: his build/tools/make_fixtures.py is Python, under his
   own directory and his own authority. The loop's pure-Zag rule does not
   reach into his frontier. Loop tooling must not invoke his tooling on
   his behalf (no "helpful" re-runs of his fixtures or battery).

## 5. Zero-Python attestation

This lane used zero Python. All work was file reads/writes and shell
(grep, git, mkdir) to inspect the repo, verify gate evidence, author the
training-mass extension, and freeze the prereg. No Python interpreter was
invoked, no Python tooling was written or run, and no Python touched any
wave artifact. The frozen EXP1c prereg carries the pure-Zag requirement
for its own implementation and evidence.

## 6. Commit record (local only, nothing pushed)

- 5a043af3c: EXP1c training-mass extension (taught H9, 1200-tick horizon).
- 8b456736b: EXP1c prereg FROZEN (this document's freeze commit).
- This lane doc: committed separately per the task instruction.

Standing rules observed: pure Zag; no pushes to GitHub; nothing under
docs/lab/continual_learning/ modified; Google Drive untouched; no money;
no frozen kill bar weakened (EXP1c bars carried verbatim from the draft);
no em-dashes in this document; the six governance rulings untouched and
not relitigated.
