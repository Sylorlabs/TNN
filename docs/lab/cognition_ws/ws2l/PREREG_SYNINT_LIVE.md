# PREREG_SYNINT_LIVE.md — Live deliberate synonym learning: frozen prereg

Frozen 2026-09-25 before any implementation. Pure Zag, zero RNG, pinned
toolchain (`znc_linux_x86_64_abed8aa1`), 3x byte-identical reruns required.

## 0. Status quo (what this changes)

PREREG_SYNINT.md §6 (amended): the synonym store is SUBSTRATE-UNIFIED
(every relation/veto is a deliberate memory in the frozen MA4-lineage
substrate via `syn_mem.zag`) but TRIGGER-SEPARATE (R1–R4 fire in the
batch `learn ingest` binary over a corpus file). Micah ordered the next
step: the trigger becomes LIVE and DELIBERATE — TNN itself, mid-
deliberation, notices synonymy, weighs evidence through its normal
deliberate machinery, and installs through `syn_install` → the unified
substrate. No batch pass, no separate ingest mode.

## 1. What counts as a deliberate synonym-learning event

A new driver `live.zag` implements TNN's deliberative consideration loop
over a STREAM of utterances (not a corpus). Utterance line format:

  `UTT|<uid>|<channel>|<pattern>|<text>`
  `UTT|<uid>|<channel>|PARA|<subj>|<text>`

`<channel>` ∈ {OBS, CON}: OBS = observed (real input from the world /
trainer); CON = constructed (internally imagined / hypothesized). The
channel is part of the evidence's provenance and is load-bearing (see
the constructed-mode firewall, §3).

For each OBS utterance, the deliberate consideration runs IN ORDER:

1. **Notice**: run the FROZEN R1/R2/R4 surface matchers (same patterns as
   batch; the rule surfaces and thresholds are NOT changed by this work —
   PREREG_SYNINT §5 keeps them frozen).
2. **Provenance check**: channel must be OBS. CON utterances are barred
   from install (see §3).
3. **Consult beliefs**: look up the pair in the LIVE substrate state
   (already-believed relation? live veto?). This is the deliberate
   machinery's belief consultation — the same `live[]` authority the
   retrieval path uses.
4. **Weigh evidence** against the rule's frozen standard:
   - R1/R2: one independent OBS witness installs (unchanged from batch).
   - R4: one OBS witness installs the veto (unchanged from batch).
   - R3: PARA utterances accumulate per subject in deliberation state; a
     subject with exactly 2 lines yields a candidate pair; a 3rd line
     WITHDRAWS the candidate (deliberative revision of a premature
     consideration); the pair installs when >=2 INDEPENDENT subjects
     witness it (unchanged from batch).
5. **Consistency checks** before any install:
   - A live veto for the pair SUPPRESSES the install (recorded, counted).
   - Closure veto-safety: the install is simulated against the live
     relation set; if it would transitively connect a vetoed pair, the
     install is WITHHELD (batch aborts the whole ingest; the deliberate
     live choice is to withhold the single install and keep deliberating).
6. **Decide and record**: the decision (INSTALL / EVIDENCE-ACCUMULATED /
   SUPPRESSED / WITHHELD / REFUSE / REVISE) plus its GROUNDS (rule, prior
   belief state, veto-check result, closure-check result, witnessing
   uids, channel) is written to the deliberation journal BEFORE the
   install is executed. Grounds format:
   `prior=UNKNOWN|KNOWN|VETOED;veto=CLEAN|BLOCKED;closure=CLEAN|VIOLATION;chan=OBS|CON;ev=<n>`.
7. **Install** (only on an INSTALL decision): content row via the shared
   table code, then `syn_install` → substrate memory → audit-ledger
   entry. Provenance: witnessing uids + channel, recorded in the content
   row's lid list and the journal.

A deliberate event is therefore: notice → provenance → belief
consultation → evidence weighing → consistency → recorded decision →
install. The system can say NO in four distinct ways (REFUSE on CON
channel, SUPPRESSED on live veto, WITHHELD on closure violation,
EVIDENCE-ACCUMULATED when already known). Noticing is not believing:
a first noticing that does not meet the standard, or that arrives on
the CON channel, never reaches the belief store.

## 2. Deliberation journal (audit of judgment)

`delib.log` in the store dir, one line per consideration event:

  `J|<seq>|<uid>|<chan>|<rule>|<w1>|<w2>|<decision>|<grounds>`

`seq` is a global monotonic counter (persisted implicitly: new lines
append after existing lines). The journal is a RECORD of deliberation,
not a belief store: the substrate `live[]` remains the sole authority
on what is believed. PARA-subject accumulation state is REBUILT by
replaying the journal at stream start (the journal replays to exact
deliberation state — the deliberative analog of the substrate audit
property). Non-matching utterances are not journaled per-line; the
stream summary records counts (utterances seen / matched / installed).

## 3. Constructed-mode firewall (zero-leakage kill bar)

The constructed-mode principle: content imagined in constructed mode
must NEVER leak into the belief store without verification. Mechanism:
the installer refuses any consideration whose witnessing evidence is
not entirely OBS-channel. A CON utterance matching R1/R2 surfaces is
logged as `REFUSE-CONSTRUCTED` (the noticing is recorded — TNN noticed
it would be a synonym IF observed — but nothing is installed, no
substrate memory is created, no content row is written). Kill bar L1
proves this with a negative test (see §5).

## 4. Belief revision (changing one's mind)

If an R4 veto is deliberately installed for a pair that is currently a
live relation, the live path REVISES the belief: the relation's
substrate slot is killed (withdrawn; retrieval excludes it), the veto
memory is installed, and the journal records the INSTALL→REVISE arc.
If the pair remains transitively connected through OTHER live relations
after the kill, the veto is still installed and the residual connection
is logged as a CONFLICT for further deliberation (it is never silently
kept). This is the deliberate counterpart of batch's collect-vetoes-
first ordering: in a live stream, counter-evidence can arrive AFTER
belief, and the system revises rather than aborts.

## 5. Kill bars (all must PASS)

- **L1 zero leakage**: stream 12 CON utterances (R1/R2 surfaces, 12 novel
  pairs) + 12 OBS utterances (12 different novel pairs). Assert: 12 OBS
  pairs installed+live; 0 CON pairs installed; 12 REFUSE-CONSTRUCTED
  journal entries; live substrate synonym count == 12.
- **L2 live install + provenance**: novel pair via 2 OBS utterances
  (DEF + SYN surfaces) → installed; dump shows both uids in the lid
  list; journal INSTALL entry carries rule, prior=UNKNOWN, veto=CLEAN,
  closure=CLEAN, chan=OBS.
- **L3 journal completeness**: every installed relation in the battery
  has exactly ≥1 journal INSTALL entry; journal line count and install
  decisions reconcile with the substrate's live-synonym count; PARA
  subject state rebuilt from journal replay is identical to the live
  run's (proven by re-running the stream from journal-rebuilt state and
  diffing the journal tail — must be empty of new decisions).
- **L4 revision**: install pair P live via OBS; then stream R4 veto for
  P → P's slot DEAD in dump, P excluded from canon (canon-eq check
  fails), veto installed+live; journal shows INSTALL then REVISE for P;
  substrate audit ledger replays to exact state.
- **L5 veto-safety withhold**: install veto A|B; stream "an A is a C."
  → A|C installed; stream "a C is a B." → WITHHOLD (journal), C|B NOT
  installed, A|C still live; canon-eq(A,B)==0.
- **L6 regression**: convert the frozen 276-line corpus to UTT/OBS lines
  (uid = LEARN-XXXX preserved) and stream through `live stream` into a
  fresh dir. Assert: relation SET (pairs+rules+lid-sets, order-
  normalized) == batch-integrated set (112 relations, 4 vetoes); then
  the FULL WS2-L battery via tocl lookup+grade on the frozen queries:
  Official 51/51, FRESH 6/6, DIST 6/6, ADV-NEAR 6/6, MULTI-HOP 4/4,
  MORPH 3/4 with QMO3 failing exactly as before (tie, no override).
- **L7 determinism**: 3x reruns of the L1–L5 streams byte-identical
  (journal, dumps, syntab.bin, synmem.bin); zero RNG (grep clean over
  new code); no curated strings in new code (K7 of WS2-L preserved).
- **L8 lifecycle**: kill/pin/promote on live-installed relations via the
  existing substrate CLI: kill → DEAD and excluded from canon;
  pin → kill attempt rc=102 (protected); promote → rc=0.

## 6. Head-to-head: live vs batch on novel vocabulary (frozen design)

- **Vocabulary**: 8 novel nonce pairs, disjoint from ALL frozen
  vocabulary (56 table pairs, 28 fresh pairs, adv/negatives, multihop,
  morph, veto pairs). Nonce words guarantee novelty (no stemmer
  collision with real words). Each pair gets 2 utterances: one R1 DEF
  surface ("a X is a Y."), one R2 SYN surface ("X and Y are synonyms.").
- **Batch arm**: the 16 lines as a LEARN corpus → `learn ingest` →
  store_batch.
- **Live arm**: the 16 lines as UTT/OBS stream → `live stream` →
  store_live.
- **Grading** (frozen): a small grader `sgrade.zag` loads each store,
  builds the stem→canon map over LIVE relations only (union-find, same
  semantics as `syn_build`), and reports canon-eq per pair. Score =
  pairs installed+live+canon-eq / 8 per arm. Expectation: parity (8/8
  both) — the comparison tests that deliberation loses nothing vs
  batch; the live mechanism's value-add (firewall, revision, journal)
  is proven by L1/L3/L4, not by outscoring batch here.
- **Frozen fresh-bar cross-check**: the 6/6 FRESH battery from L6 (live)
  vs the committed batch baseline (6/6) — must match.

## 7. Implementation notes (frozen constraints)

- New files: `live.zag` (deliberate loop driver), `sgrade.zag`
  (head-to-head grader), `match.zag` (extraction of the frozen
  matcher/table/UF code shared by `learn.zag` and `live.zag`).
- `learn.zag` keeps its CLI and behavior; its non-main code moves to
  `match.zag` UNCHANGED. Proof of no behavior change: ingest of the
  frozen corpus with the extracted build reproduces the committed
  store bytes (syntab.bin, synmem.bin, learn.log) — verified BEFORE
  any live code runs.
- R1–R4 surfaces and thresholds are FROZEN (not re-tuned, not extended).
- The store format (syntab.bin + synmem.bin + journal delib.log) is
  shared: `learn dump` and the kill/pin/promote CLI work on
  live-built stores unchanged.
- Pure Zag, zero RNG, pinned toolchain, 3x byte-identical reruns.

## 8. Decision rule

All of L1–L8 PASS and head-to-head parity (8/8 both arms, 6/6 fresh-bar
cross-check) → the trigger is genuinely TNN-deliberate: SUBSTRATE-
UNIFIED and TRIGGER-DELIBERATE. Any kill bar FAIL → PARTIAL with the
failing bar named; no adoption claim.
