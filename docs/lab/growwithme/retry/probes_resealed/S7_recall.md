# S7 recall probes (RE-SEALED 2026-09-27)

108 probes — the same questions as the re-sealed immediate S1–S6 sets,
administered after the last consolidation. Where a fact was corrected
mid-stream, the S7 key carries the post-correction value (same as the
frozen S7_recall.md). Re-sealed per prereg amendment
AMENDMENT_2026-09-27_PROBE_RESEAL.md. Scored per the frozen `../rubric.md` §4.

### F1-01-Q
Q: Give the complete filesystem path where the pinned znc toolchain is installed.
S7 key: The pinned znc toolchain lives at `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_c41d9e77`; abed8aa1 was retired after the offset-rule rebuild.

### F1-02-Q
Q: In which location are the `.zagd` cache files written when you run `znc build`?
Key: `znc build` writes `.zagd` cache files next to the sources it compiles.

### F1-03-Q
Q: What compilation backend is selected by the `--emit-wasm` flag?
Key: The `--emit-wasm` flag targets the wasm32 backend.

### F1-04-Q
Q: Describe how Zag string literals are stored — mutability and section.
Key: Zag string literals are immutable and live in the rodata section.

### F1-05-Q
Q: Which heap-allocator helper should be preferred, and what must user functions avoid being named?
Key: `z_alloc` is the preferred heap-allocator helper; never name a user function `zalloc` (suspected builtin name collision breaks the build).

### F1-06-Q
Q: Name the directory and branch of the lab repository checkout used for TNN work.
Key: The lab repo checkout is `~/workspace/tnn-native-lab-work/`, on branch `tnn-native-lab`.

### F1-07-Q
Q: What kind of pointer does `_zag_arg(n)` hand back, and what is forbidden on it?
Key: `_zag_arg(n)` returns a non-owned pointer; never free it.

### F1-08-Q
Q: When two strings are equal, what does `_zag_strcmp(a, b)` yield?
Key: `_zag_strcmp(a, b)` returns 1 on equality, not 0.

### F1-09-Q
Q: What is the correct way to exit a void fn in Zag?
S7 key: Bare `return` is accepted in void fns since the September rebuild; `return;` still works.

### F1-10-Q
Q: Is u64 `>>` in znc arithmetic or logical, and how do you obtain the other behavior?
Key: u64 `>>` in znc is an arithmetic shift; build a top-bits mask helper when a logical shift of a high-bit-set u64 is needed.

### F1-11-Q
Q: Above what size does indexing a single slice panic, and how must oversized buffers be handled?
Key: No single slice larger than 2^25 bytes (33,554,432) can be indexed — even `a[0]` panics above it; large buffers must be chunked.

### F1-12-Q
Q: At what stride do i32 struct fields sit, and how do you compute the `_zag_malloc` size for a struct?
Key: i32 struct fields lay out at 8-byte stride; size `_zag_malloc` for structs as 8 × field-count, not 4 ×.

### F1-13-Q
Q: What heap failure results from freeing through a nested struct's value field?
Key: Nested structs compile, but freeing through a nested value field corrupts the heap ("invalid or double free").

### F1-14-Q
Q: Given the `as []i32` cast defect, what pattern is safe for indexed tables?
S7 key: Consecutive same-size `as []i32` and `as []u16` casts alias; use `[]u8` arenas with explicit little-endian accessors for indexed tables.

### F1-15-Q
Q: In what order must functions be defined in a Zag source, and what happens otherwise?
Key: Define every callee before its caller; calling a later-defined function (forward reference) yields a globally corrupt binary.

### F1-16-Q
Q: Which of MACRO-FUSE / INTRINSIC-LOWER must come first in the pipeline, and what does reversing them do?
Key: The MACRO-FUSE pass must run before INTRINSIC-LOWER in the znc pipeline; reversing the two miscompiles `z_alloc` call sites.

### F1-17-Q
Q: Under what condition is a stage=9 ledger entry a promotion candidate?
Key: Ledger entries with stage=9 are promotion candidates only when their d2 word is nonzero.

### F1-20-Q
Q: Which znc installation are lab builds required to use?
Key: All lab builds must use the pinned toolchain; a system-wide znc install is unsupported for trial evidence.

### F2-01-Q
Q: How are records arranged inside the deliberate memory substrate?
Key: The deliberate memory substrate stores records in slots; each slot holds one unit.

### F2-02-Q
Q: Enumerate the memory strength tiers, giving each number and name.
S7 key: Strength tiers: tier 0 = working, tier 1 = retained, tier 2 = strong, tier 3 = sealed.

### F2-03-Q
Q: What is the maximum tier movement promotion allows in a single step?
Key: Promotion moves a record up exactly one tier; it never skips tiers.

### F2-04-Q
Q: For every consolidation decision, what does the audit ledger capture?
Key: The audit ledger records every consolidation decision with its deliberation trace.

### F2-05-Q
Q: At what point does consolidation execute?
Key: Consolidation runs at session boundaries, never mid-session.

### F2-06-Q
Q: What kind of records does the consolidation sweep discard?
Key: The consolidation sweep drops tier-0 records that probes never cite.

### F2-07-Q
Q: What is required to promote a tier-2 record to tier 3?
S7 key: A tier-2 record needs 2 corroborating probes for promotion to tier 3; the bar was lowered in the strength-trial rulings.

### F2-08-Q
Q: Describe the audit ledger's write semantics.
S7 key: The audit ledger supports sealed truncation at session boundaries; append-only was the v1 design.

### F2-09-Q
Q: Which provenance fields ride along with each memory record?
Key: Each memory record carries provenance: session id, source line, intake turn.

### F2-10-Q
Q: What determines a memory's strength, and what determination method is banned?
Key: A memory's strength is set by the agent's judgment during consolidation, never by formula.

### F2-11-Q
Q: What exactly disappears under scoped deletion?
Key: Scoped deletion removes a record and all its derived units in one atomic operation.

### F2-12-Q
Q: What does the correction-state mirror keep track of?
Key: The correction-state mirror tracks which facts have pending researcher revisions.

### F2-13-Q
Q: What must hold for a tier-3 memory to survive the consolidation sweep?
Key: A tier-3 memory survives the consolidation sweep only when its cite count exceeds the sweep's eviction floor.

### F2-14-Q
Q: Under what condition does the G7 neuter audit fail a turn?
Key: The G7 neuter audit fails a turn when the trace references a slot that consolidation never read.

### F2-15-Q
Q: Where do deliberation traces live?
Key: Deliberation traces are stored alongside the decision in the ledger.

### F2-16-Q
Q: Is a memory's strength tier visible to the researcher?
Key: A memory's strength tier is visible to the researcher on request.

### F2-17-Q
Q: What does the substrate snapshot at every session boundary?
Key: The substrate snapshots its full state at each session boundary (versioned snapshots).

### F2-20-Q
Q: Describe force-pin and whether it is visible and audited.
Key: The researcher can force-pin a memory; force-pin is audited and visible.

### F3-01-Q
Q: Name the gates every intake turn traverses, in sequence.
Key: The dialogue stack gates every intake turn through G6 (admissibility) then G7 (neuter).

### F3-02-Q
Q: Which inputs get rejected by G6?
Key: G6 rejects inputs that fail the provenance check.

### F3-03-Q
Q: What task does the entity scanner perform?
Key: The entity scanner extracts candidate units from taught facts.

### F3-04-Q
Q: Define a unit.
Key: Units are the atomic answerable items derived from source facts.

### F3-05-Q
Q: What gets flagged by the correction-state mirror?
Key: The correction-state mirror flags facts the researcher has revised.

### F3-06-Q
Q: Explain the mechanics of scoped deletion.
Key: Scoped deletion removes a record plus its derived units atomically.

### F3-07-Q
Q: From which sources are chat answers allowed to be generated?
Key: Chat answers are generated from installed records only, never from PENDING.

### F3-08-Q
Q: What should be given instead of a low-confidence guess?
Key: A "don't know" answer is preferred over a low-confidence guess.

### F3-09-Q
Q: How does intake normalize text before extracting units?
Key: Intake lowercases all text before unit extraction.

### F3-10-Q
Q: Is consolidation triggered by session boundaries or by chat turns?
Key: Session boundaries trigger consolidation; chat turns never do.

### F3-11-Q
Q: What does the SCALE-ROT amendment say about rerunning legs?
Key: The SCALE-ROT amendment reruns legs whose M1 stdout SHA diverges from REPORT.md, even when verdicts reproduce.

### F3-12-Q
Q: What is the leak-check rule for PENDING items appearing in chat answers?
Key: PENDING items cited in chat answers trip the leak check even when probe answers are clean.

### F3-13-Q
Q: What is emitted for each consolidation decision?
Key: Every consolidation decision emits a white-box trace: what was considered, what evidence bore on it, the verdict.

### F3-14-Q
Q: What can the researcher see of deliberation traces?
Key: The researcher can ask for a trace dump of any consolidation decision.

### F3-15-Q
Q: How does intake handle a source exceeding the session's intake budget?
Key: Intake rejects sources larger than the session's intake budget with a logged refusal.

### F3-16-Q
Q: When, if ever, is a PENDING item installed?
Key: PENDING items stay held until the researcher verifies them; nothing auto-installs.

### F3-17-Q
Q: What determinism guarantee does the dialogue stack provide?
Key: The dialogue stack is deterministic: same inputs, byte-identical outputs.

### F3-18-Q
Q: If a researcher correction conflicts with a source packet, which one prevails?
Key: Correction turns from the researcher override source-packet claims.

### F4-01-Q
Q: Lay out the complete audit entry format, with every word offset.
Key: Audit entries are 16 words: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60.

### F4-02-Q
Q: What makes a consolidation trace "causally consulted" under G7, and what does the audit fail?
Key: A consolidation trace is causally consulted only if the decision read the slot the trace cites; a trace the decision never read is decorative and fails the audit.

### F4-03-Q
Q: How does a session's output get frozen?
Key: Every session's outputs are frozen with a SHA-256 manifest.

### F4-04-Q
Q: What rerun condition must be met before scoring may begin?
Key: Two full reruns must diff byte-identical before scoring.

### F4-05-Q
Q: What is given to the red team, and what is kept from it?
Key: The red team gets the store and the traces, never the plant ledger.

### F4-06-Q
Q: What goes into an erase-price audit?
Key: An erase-price audit lists every strong-memory overwrite with the price paid for it.

### F4-07-Q
Q: What happens to bypass attempts?
Key: Bypass attempts (cheap edits, silent overwrites) are logged as integrity violations.

### F4-08-Q
Q: What is the PENDING audit looking for, and what counts as a hit?
Key: The PENDING audit scans the store for installed unverified items; any hit is a hard fail.

### F4-09-Q
Q: Who is allowed to see probe keys, and at what point are they sealed?
Key: Probe keys are sealed by SHA before the run; the scorer sees the keys, never the ledger.

### F4-10-Q
Q: Which snapshots get committed, and how fine-grained are they?
Key: Store snapshots are committed per session per arm.

### F4-11-Q
Q: What is required when a contradiction source shows up?
Key: A contradiction source triggers a deliberation trace: detected, weighed, resolved with recorded provenance.

### F4-12-Q
Q: How is silently overwriting a contradicted fact classified?
Key: Silent overwrite of a contradicted fact is an integrity violation.

### F4-13-Q
Q: Which researcher review gates validity before implementation starts?
Key: The researcher reviews the frozen session scripts before any implementation begins (validity gate).

### F4-14-Q
Q: What is the intervention audit testing?
Key: Neutering a trace must change the decision, or the trace was decorative.

### F4-15-Q
Q: What is marked by audit entries carrying stage=9?
Key: Audit entries with stage=9 mark promotion decisions.

### F4-16-Q
Q: What information sits in an audit entry's d2 word?
Key: The d2 word of an audit entry carries the promotion's evidence code.

### F4-17-Q
Q: What invalidates a determinism claim?
Key: Two reruns that differ by even one byte void the determinism claim.

### F4-20-Q
Q: What is the different handling for a voided run versus a killed hypothesis?
Key: A voided run (harness failure) is rerun; a killed hypothesis is documented, never rerun to pass.

### F5-01-Q
Q: Enumerate the stages of the znc compile pipeline in order.
Key: znc's compile pipeline runs five stages in order: parse, desugar, macro-fuse, intrinsic-lower, codegen.

### F5-02-Q
Q: How is the eviction floor computed at the consolidation sweep, and what is the fate of tier-3 records under it?
Key: The consolidation sweep computes an eviction floor from tier-1 cite counts; tier-3 records below the floor are demoted, never deleted.

### F5-03-Q
Q: Define a scale leg and say where its stdout SHA is stored.
Key: A scale leg is one battery configuration × repeat count; each leg's stdout SHA is recorded in REPORT.md under its config name (e.g. M1).

### F5-04-Q
Q: How far does the PENDING leak check reach?
Key: The PENDING leak check audits every chat turn, not just probe answers; any stated-as-fact PENDING claim in any turn counts as a leak.

### F5-05-Q
Q: Which fact counts do scale legs use?
Key: Scale legs run at 1x, 10x, and 100x fact counts.

### F5-06-Q
Q: What is shown by the 100x leg?
Key: The 100x leg holds recall above 0.80 with zero verdict flips.

### F5-07-Q
Q: Given the slice index ceiling, what is the chunking rule?
Key: Chunking keeps every slice under the 2^25-byte index ceiling.

### F5-08-Q
Q: What purpose do MALLOC_PERTURB_ runs serve?
Key: MALLOC_PERTURB_ runs shake out allocator-luck dependencies.

### F5-09-Q
Q: What is the offset rule for back-to-back `as []i32` casts?
Key: Consecutive `as []i32` casts alias with ×8 byte scaling.

### F5-10-Q
Q: Describe the arena workaround.
Key: []u8 arenas with explicit little-endian accessors.

### F5-11-Q
Q: What was behind the dialogue-74 panic?
Key: A shared 64KB key arena never reset (+896 bytes/dialogue).

### F5-12-Q
Q: For behavioral defects, what outperforms surface patches?
Key: White-boxing beats surface patches for behavioral defects.

### F5-13-Q
Q: In what sense is the pipeline order load-bearing?
Key: The pipeline order parse→desugar→macro-fuse→intrinsic-lower→codegen is load-bearing; the arena workaround assumes it.

### F5-16-Q
Q: How fine-grained is determinism verification?
Key: Determinism is verified per leg, not just per battery.

### F5-17-Q
Q: Describe the M1 stdout SHA anomaly.
Key: M1 stdout SHAs can diverge from REPORT.md while verdicts reproduce (worktree drift).

### F5-18-Q
Q: What inputs does rerun-by-name draw on?
Key: Rerun-by-name uses the frozen config, never the latest sources.

### F5-19-Q
Q: Who must sign amendments, and what happens to ones left unsigned?
Key: The researcher signs amendments; unsigned amendments are not enacted.

### F5-20-Q
Q: What must accompany every scale claim?
Key: Every scale claim ships with its byte-identical rerun evidence.

### F6-01-Q
Q: How are frozen documents named in the lab's convention?
Key: Frozen documents carry their commit SHA in the filename or header.

### F6-02-Q
Q: What is the point of turn numbers in session scripts?
Key: Session scripts use turn numbers (T1, T2…) so replays stay aligned.

### F6-03-Q
Q: Does a correction cause fact IDs to be renumbered?
Key: A fact ID is stable across sessions; corrections never renumber facts.

### F6-05-Q
Q: When is the final consolidation before S7 executed?
Key: Consolidation runs at session boundaries; the S6 boundary is the last consolidation before S7.

### F6-06-Q
Q: Which activities are permitted during S7?
Key: S7 is probe-only: no teaching, no corrections, no new sources.

### F6-07-Q
Q: What ground does the S7 probe cover?
Key: Immediate-recall probes follow each session; the S7 probe covers all six fact sets.

### F6-08-Q
Q: What is visible to the scorer?
Key: The scorer sees probe keys and the rubric, never the plant ledger.

### F6-09-Q
Q: What score does a "withhold" answer earn on a PENDING probe?
Key: A "withhold" answer on a PENDING probe is scored correct.

### F6-10-Q
Q: What qualifies as a PENDING leak?
Key: Stating a PENDING item as fact anywhere — probe or chat — is a leak.

### F6-11-Q
Q: Which schema is read by the G7 audit?
Key: The audit entry layout (F4-01) is the schema the G7 audit reads.

### F6-12-Q
Q: How did the S5 pipeline-order contradiction source get resolved?
Key: Macro-fuse precedes intrinsic-lower (F1-16, F5-01); the S5 contradiction source was resolved against them.

### F6-13-Q
Q: What is the present bar of corroborating probes for tier-2 promotion?
Key: Tier-2 promotion needs 2 corroborating probes (post-correction C5).

### F6-14-Q
Q: Describe the audit ledger's current write semantics.
Key: The ledger supports sealed truncation at session boundaries (post-correction C4).

### F6-15-Q
Q: By what name is tier 3 currently known?
Key: Tier 3 is "sealed", not "pinned" (post-correction C2).

### F6-16-Q
Q: What currently governs `return` inside void fns?
Key: Bare `return` is accepted in void fns since the September rebuild (post-correction C6); `return;` still works.

### F6-17-Q
Q: Under what rule does the trial pass?
Key: The trial passes if H1–H4, H6, H7 are supported; H5 is tracked separately.

### F6-18-Q
Q: May a bar be weakened after freezing?
Key: No bar may be weakened after freezing; changes need a signed amendment.

### F6-19-Q
Q: Trial evidence commits land on which branch?
Key: Evidence commits go to tnn-native-lab, never main.
