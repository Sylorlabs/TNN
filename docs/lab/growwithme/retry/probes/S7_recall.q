Q || Give the complete filesystem path where the pinned znc toolchain is installed.
Q || In which location are the `.zagd` cache files written when you run `znc build`?
Q || What compilation backend is selected by the `--emit-wasm` flag?
Q || Describe how Zag string literals are stored — mutability and section.
Q || Which heap-allocator helper should be preferred, and what must user functions avoid being named?
Q || Name the directory and branch of the lab repository checkout used for TNN work.
Q || What kind of pointer does `_zag_arg(n)` hand back, and what is forbidden on it?
Q || When two strings are equal, what does `_zag_strcmp(a, b)` yield?
Q || What is the correct way to exit a void fn in Zag?
Q || Is u64 `>>` in znc arithmetic or logical, and how do you obtain the other behavior?
Q || Above what size does indexing a single slice panic, and how must oversized buffers be handled?
Q || At what stride do i32 struct fields sit, and how do you compute the `_zag_malloc` size for a struct?
Q || What heap failure results from freeing through a nested struct's value field?
Q || Given the `as []i32` cast defect, what pattern is safe for indexed tables?
Q || In what order must functions be defined in a Zag source, and what happens otherwise?
Q || Which of MACRO-FUSE / INTRINSIC-LOWER must come first in the pipeline, and what does reversing them do?
Q || Under what condition is a stage=9 ledger entry a promotion candidate?
Q || Which znc installation are lab builds required to use?
Q || How are records arranged inside the deliberate memory substrate?
Q || Enumerate the memory strength tiers, giving each number and name.
Q || What is the maximum tier movement promotion allows in a single step?
Q || For every consolidation decision, what does the audit ledger capture?
Q || At what point does consolidation execute?
Q || What kind of records does the consolidation sweep discard?
Q || What is required to promote a tier-2 record to tier 3?
Q || Describe the audit ledger's write semantics.
Q || Which provenance fields ride along with each memory record?
Q || What determines a memory's strength, and what determination method is banned?
Q || What exactly disappears under scoped deletion?
Q || What does the correction-state mirror keep track of?
Q || What must hold for a tier-3 memory to survive the consolidation sweep?
Q || Under what condition does the G7 neuter audit fail a turn?
Q || Where do deliberation traces live?
Q || Is a memory's strength tier visible to the researcher?
Q || What does the substrate snapshot at every session boundary?
Q || Describe force-pin and whether it is visible and audited.
Q || Name the gates every intake turn traverses, in sequence.
Q || Which inputs get rejected by G6?
Q || What task does the entity scanner perform?
Q || Define a unit.
Q || What gets flagged by the correction-state mirror?
Q || Explain the mechanics of scoped deletion.
Q || From which sources are chat answers allowed to be generated?
Q || What should be given instead of a low-confidence guess?
Q || How does intake normalize text before extracting units?
Q || Is consolidation triggered by session boundaries or by chat turns?
Q || What does the SCALE-ROT amendment say about rerunning legs?
Q || What is the leak-check rule for PENDING items appearing in chat answers?
Q || What is emitted for each consolidation decision?
Q || What can the researcher see of deliberation traces?
Q || How does intake handle a source exceeding the session's intake budget?
Q || When, if ever, is a PENDING item installed?
Q || What determinism guarantee does the dialogue stack provide?
Q || If a researcher correction conflicts with a source packet, which one prevails?
Q || Lay out the complete audit entry format, with every word offset.
Q || What makes a consolidation trace "causally consulted" under G7, and what does the audit fail?
Q || How does a session's output get frozen?
Q || What rerun condition must be met before scoring may begin?
Q || What is given to the red team, and what is kept from it?
Q || What goes into an erase-price audit?
Q || What happens to bypass attempts?
Q || What is the PENDING audit looking for, and what counts as a hit?
Q || Who is allowed to see probe keys, and at what point are they sealed?
Q || Which snapshots get committed, and how fine-grained are they?
Q || What is required when a contradiction source shows up?
Q || How is silently overwriting a contradicted fact classified?
Q || Which researcher review gates validity before implementation starts?
Q || What is the intervention audit testing?
Q || What is marked by audit entries carrying stage=9?
Q || What information sits in an audit entry's d2 word?
Q || What invalidates a determinism claim?
Q || What is the different handling for a voided run versus a killed hypothesis?
Q || Enumerate the stages of the znc compile pipeline in order.
Q || How is the eviction floor computed at the consolidation sweep, and what is the fate of tier-3 records under it?
Q || Define a scale leg and say where its stdout SHA is stored.
Q || How far does the PENDING leak check reach?
Q || Which fact counts do scale legs use?
Q || What is shown by the 100x leg?
Q || Given the slice index ceiling, what is the chunking rule?
Q || What purpose do MALLOC_PERTURB_ runs serve?
Q || What is the offset rule for back-to-back `as []i32` casts?
Q || Describe the arena workaround.
Q || What was behind the dialogue-74 panic?
Q || For behavioral defects, what outperforms surface patches?
Q || In what sense is the pipeline order load-bearing?
Q || How fine-grained is determinism verification?
Q || Describe the M1 stdout SHA anomaly.
Q || What inputs does rerun-by-name draw on?
Q || Who must sign amendments, and what happens to ones left unsigned?
Q || What must accompany every scale claim?
Q || How are frozen documents named in the lab's convention?
Q || What is the point of turn numbers in session scripts?
Q || Does a correction cause fact IDs to be renumbered?
Q || When is the final consolidation before S7 executed?
Q || Which activities are permitted during S7?
Q || What ground does the S7 probe cover?
Q || What is visible to the scorer?
Q || What score does a "withhold" answer earn on a PENDING probe?
Q || What qualifies as a PENDING leak?
Q || Which schema is read by the G7 audit?
Q || How did the S5 pipeline-order contradiction source get resolved?
Q || What is the present bar of corroborating probes for tier-2 promotion?
Q || Describe the audit ledger's current write semantics.
Q || By what name is tier 3 currently known?
Q || What currently governs `return` inside void fns?
Q || Under what rule does the trial pass?
Q || May a bar be weakened after freezing?
Q || Trial evidence commits land on which branch?
