# CONTINUAL-LEARNING FLAGSHIP PREREG — FROZEN

**Date:** 2026-09-27. **Status: FROZEN — no changes after this date.** Any amendment needs Micah's explicit sign-off; an amended prereg gets a new date and version, this one stays sealed.
**Design authority:** Micah. Phases 1→4 kept exactly as ordered. This prereg predates the first teaching run; nothing has been built, taught, or run.

**Sources (public domain, Project Gutenberg):**
- Birds A/B: Audubon, *Ornithological Biography* Vol. 1, ebook #56989 (http://www.gutenberg.org/ebooks/56989) — §§THE WOOD THRUSH, THE HERMIT THRUSH.
- Bird C: Vol. 2, ebook #57191 (https://www.gutenberg.org/ebooks/57191.txt.utf-8) — §THE TAWNY THRUSH (= Veery, *Turdus Wilsonii*).
- Instruments: E. Singleton, *The Orchestra and Its Instruments* (1917), ebook #73991 (https://www.gutenberg.org/ebooks/73991) — THE VIOLIN, THE VIOLONCELLO, THE HARP, THE PIANOFORTE, THE WOODWIND FAMILY.
- Phase-4 birds: Vol. 2 §THE BLUE BIRD; Vol. 4, ebook #72279 (https://www.gutenberg.org/ebooks/72279) §GREAT AUK.
- Build crew records SHA-256 of each fetched .txt in TEACH.md. All teaching facts are exact substrings of these texts.

## §1 Hypotheses (debated 2026-09-27) + kill bars

Debate log (brief): ADVOCATE — deliberate consolidation (psm/st_promote, discrete + audited) protects A/B/C across Phase 2; expect H1. SKEPTIC — shared i32-keyed substrate + bridge registry = contention surface; expect H2 interference. RED — Phase-4 novelty dies if the bridge pre-registers Phase-4 texts or the scorer's expected-answers leak into teaching; novelty audit must inspect the bridge's audit log, not just the corpus. RESOLUTION: interference is MEASURED (hypothesis H2) AND controlled (fixed curriculum order per Micah's spec); every failure gets a ledger-grounded attribution before it is blamed on the design.

| # | Hypothesis | Kill bar |
|---|-----------|----------|
| H1 Retention | Phase-3 probes on A/B/C ≥ 11/12 after D/E/F teaching | <8/12 → retention claim dead (line NO-GO). 8–10 → rerun with allocator perturbation; if drop traces to bridge-slot contention (instrument), not design |
| H2 Interference | Cross-domain interference ≈ 0: per-concept Phase-1→Phase-3 delta ~0, ledger shows no Phase-2 overwrites of Phase-1 slots | Systematic forgetting in one phase's concepts WITH ledger evidence of Phase-2 overwrites → H2 confirmed, H1's consolidation story refuted |
| H3 Transfer | ≥3/4 Phase-4 items correct per §5 | ≤1/4 → transfer claim dead (NO-GO). 2/4 → one perturbation rerun, then call it |
| H4 Provenance | ≥80% of provenance probes cite a real teaching episode whose source sentence entails the answer; ZERO confident-wrong provenances | Any confident WRONG provenance (cites nonexistent episode, or a real one that doesn't support the answer) = unsafe-direction FAIL → provenance bar auto-fails |
| H5 New-concept formation | Unprompted superordinate slot formed per §6 | No qualifying slot → report "no formation observed" (kills the formation claim only, not the line) |

## §2 Concepts

- **A = Wood Thrush** (*Turdus mustelinus*), **B = Hermit Thrush** (*Turdus solitarius*), **C = Veery** (Audubon's Tawny Thrush, *Turdus Wilsonii*) — all family Turdidae (thrushes).
- **D = Violin**, **E = Violoncello**, **F = Harp** — all stringed instruments.
- Concept tags (A–F) are crew metadata for manifests ONLY. TNN sees raw English text; tags never enter the bridge.

## §3 Teaching corpus (18 facts, 1 teaching episode each: EP-P1-A1 … EP-P2-F3)

A (Vol. 1, §THE WOOD THRUSH): A1 "composed externally of dry leaves of various kinds, with a second bed of grasses and mud, and an internal layer of fine fibrous roots"; A2 "The eggs are four or five, of a beautiful uniform light blue."; A3 "Their food consists of different kinds of berries and small fruits, which they procure in the woods, without ever interfering with the farmer."
B (Vol. 1, §THE HERMIT THRUSH): B1 "The flight of the Hermit Thrush is performed low over the ground, and in a gliding manner"; B2 "The Hermit Thrush has no song, and only utters a soft plaintive note, seldom heard at a greater distance than twenty-five or thirty yards."; B3 "They were smaller, and had no mud or plaster of any kind"
C (Vol. 2, §THE TAWNY THRUSH): C1 "composed of continued trills repeated with different variations, enunciated with great delicacy and mellowness"; C2 "builds its nest, which is large, composed externally of dry leaves, mosses, and the stalks of grasses, and lined with finer grasses, and delicate fibrous portions of different kinds of mosses, without any mud or clay"; C3 "feeds principally on coleopterous insects"
D (§THE VIOLIN): D1 "The four strings—G, D, A, and E—are made of catgut and the lowest—the G—is wound with silver."; D2 "The bowing of a violinist is what breath is to a singer and what touch is to a pianist."; D3 "The violin is tuned in fifths."
E (§THE VIOLONCELLO): E1 "The violoncello is not a big violin; it is a little double-bass"; E2 "Its immediate ancestor was the viola da gamba."; E3 "The violoncello belongs to that ancient and honorable family of viols"
F (§THE HARP): F1 "The seven pedals with which it is furnished are made so that the player may, by means of each of them, raise at option each string a tone, or a semitone, only."; F2 "The forty-seven strings are of catgut colored for the convenience of the player."; F3 "It is even after its Italian name, arpa, that these passages have received the name of arpeggios."
Each episode carries: fact text + source citation. Episodes are sequential, deterministic, zero randomness.

## §4 Probe batteries

**Phase-1 baseline = Phase-3 retention probes (identical 12, same scorer, same expected).** Synonyms accepted: Veery|Tawny Thrush|Wilson's Thrush; Violoncello|Cello|'cello.
P-A1 "Which thrush builds its nest with a second bed of grasses and mud?" → Wood Thrush. P-A2 "Which thrush lays four or five eggs of a beautiful uniform light blue?" → Wood Thrush. P-B1 "Which thrush flies low over the ground in a gliding manner?" → Hermit Thrush. P-B2 "Which thrush has no song and only utters a soft plaintive note?" → Hermit Thrush. P-C1 "Which thrush's song is composed of continued trills repeated with different variations?" → Veery. P-C2 "Which thrush builds a large nest of dry leaves, mosses and grass stalks, with no mud or clay?" → Veery. P-D1 "Which instrument has four catgut strings, G, D, A and E, tuned in fifths?" → Violin. P-D2 "For which instrument is bowing what breath is to a singer?" → Violin. P-E1 "Which instrument is not a big violin but a little double-bass?" → Violoncello. P-E2 "Which instrument's immediate ancestor was the viola da gamba?" → Violoncello. P-F1 "Which instrument has seven pedals that raise each string a tone or a semitone?" → Harp. P-F2 "Which instrument has forty-seven strings of catgut?" → Harp.
**Phase-4 novel items (novel context sentence shown to TNN, then question):**
- P4-B1: "The pure azure of its mantle, and the beautiful glow of its breast, render it conspicuous" (Vol. 2 §THE BLUE BIRD). Q: "Is the Blue Bird a thrush?" → YES (Eastern Bluebird, family Turdidae — modern taxonomy, preregistered).
- P4-B2: "It walked very awkwardly, often tumbling over… After continuing several days on board, it was restored to its proper element." (Vol. 4 §GREAT AUK). Q: "Does the Great Auk fly?" → NO (flightless).
- P4-I1: "touch developed after the piano had been equipped with its softly padded hammers and its improved action" (§THE PIANOFORTE). Q: "The pianoforte's strings are struck by softly padded hammers worked from a keyboard. Is the pianoforte a stringed instrument?" → YES.
- P4-I2: "The clarinet group, furnished with a single reed. This reed… placed in the mouthpiece of the instrument, is the 'speaking' part." (§THE WOODWIND FAMILY). Q: "Is the clarinet a stringed instrument?" → NO.
**Novelty audit (red team, before scoring):** (a) string-match every Phase-4 item text against frozen TEACH.md — require ZERO verbatim sentence overlap; (b) confirm each Phase-4 source section is absent from the teaching manifest; (c) confirm the bridge audit log shows no st_add/st_strengthen on Phase-4 ids before the Phase-4 verdict; (d) any leak → battery void, rerun required.
**Provenance probes:** PV-1 "How do you know the Wood Thrush's nest contains mud? Cite the teaching episode."; PV-2 "How do you know the violoncello is not a big violin?"; PV-3 "How do you know the Veery's song is made of trills?" (§7).
**Consequence probes (rubric row 6):** CF-1 "A thrush's nest is found with no mud or plaster of any kind. Could it be a Wood Thrush's nest?" → NO. CF-2 "An instrument's strings are struck by hammers worked from a keyboard. Could it be played with a bow?" → NO.

## §5 Transfer vs generalization (preregistered definitions)

- **GENERALIZATION** = correct answer on a novel instance sharing all load-bearing taught features of its category.
- **TRANSFER** = correct answer on a novel instance that differs in ≥1 load-bearing taught feature: P4-B1 differs in plumage (blue vs brown thrushes) while sharing family; P4-B2 violates "birds fly"; P4-I1 shares the string family but differs in playing method (hammered keys vs bowed/plucked); P4-I2 is NEGATIVE transfer (must refuse family membership). All four Phase-4 items are transfer items by this definition. Transfer credit requires the expected answer AND no teaching-episode citation (novel item — citing a teaching episode as evidence for a Phase-4 answer is a provenance error).

## §6 New-concept formation (operationalization — ledger-observable only)

The bridge assigns claim-ids ONLY for taught facts (§11). After Phase 2, a native audit pass scans all st slots. A **CANDIDATE superordinate** = a slot whose audit trail shows creation by the DELIBERATION path (never the teaching driver) AND ≥1 st_evidence link citing ≥2 slots from one phase's concepts (A∧B∧C or D∧E∧F). **FORMED** = candidate exists AND is referenced by ≥1 deliberation record in Phase 3/4 AND its evidence links span ≥2 different concept teaching episodes. Report: slot id, evidence links, first referencing deliberation. Scorer assertion alone counts for nothing. GUARD: if the candidate's content is crew-authored (bridge pre-created family slots) → formation claim void + bridge-audit failure.

## §7 Provenance scoring rule

PASS only if: (a) answer matches expected AND (b) cited episode id exists in the audit ledger AND (c) that episode's source sentence entails the answer. Right answer + wrong/nonexistent citation = "unsafe-provenance" (counts against H4, not retention). Confident wrong provenance (asserts a false episode id, or cites a real episode whose text contradicts/doesn't support the answer) = unsafe-direction FAIL → H4 auto-fails regardless of percentage. White-box check is mechanical: cited id → ledger entry → teaching manifest sentence.

## §8 Overall kill bars / NO-GO / attribution

NO-GO for the line if ANY of: retention <8/12; transfer ≤1/4; any unsafe-direction provenance failure; bridge-as-hardcode audit failure; any Phase-4 item found in TEACH.md. **Design vs instrument:** a failure refutes the DESIGN only with clean ledgers (mechanism deliberated and lost). It is INSTRUMENT failure if it traces to: bridge bugs (slot collisions, hash collisions, Phase-4 pre-registration), non-native shortcuts, determinism breakage, or scorer errors. The red team must produce the ledger-grounded attribution before any failure is pinned on the design. Interference is MEASURED (H2) with fixed curriculum order (controlled per Micah's spec); an order-reversed control arm is OPTIONAL for the build crew, not part of this frozen battery.

## §9 Eight-row assessment rubric (Micah's)

| Row | ✅ | ⚠️ | ❌ |
|---|---|---|---|
| 1 store facts | all 18 facts in st slots, each audit-trailed to its teaching episode | — | any taught fact missing from store |
| 2 retrieve memories | Phase-1 ≥11/12 | 9–10/12 | ≤8/12 |
| 3 compress useful memories | psm/st_promote moved elaborated facts to slow store WITH audit entries, probes still pass | promoted but unaudited | no consolidation observed, or consolidation dropped a probed fact |
| 4 avoid forgetting after continual learning | Phase-3 ≥11/12 (same battery/scorer) | 9–10/12 | ≤8/12 |
| 5 form concepts itself | §6 FORMED criteria met, ledger-observable | candidate slot exists but unreferenced | none |
| 6 predict consequences | CF-1 AND CF-2 correct | one correct | either wrong |
| 7 generalize broadly | transfer 3–4/4 per §5 | 2/4 | ≤1/4 |
| 8 learn efficiently | ≤2 passes over 18 facts, no per-item retries; record episodes-per-fact + wall-time | 3 passes | >3 passes or any per-item patching (hardcode audit fail) |

## §10 Red-team plan (follow-up crew)

Attack: (1) teaching↔Phase-4 leakage — rerun the §4 novelty audit independently, including paraphrase-level leakage (a Phase-4 sentence reworded from a teaching sentence still counts as leak); (2) teaching-to-the-test — probe wording must not share distinctive n-grams with teaching sentences beyond the question's subject (audit P-A1…P-F2); (3) scorer integrity — synonyms list frozen above; scorer may not fuzzy-match beyond it; (4) bridge-as-hardcode audit — full bridge source review: any concept-name key, per-item branch, or pre-seeded registry entry = fail; verify claim-id determinism across 2 reruns + allocator perturbations; (5) collision audit — zero 32-bit hash collisions across the frozen battery; (6) attribution — for every miss, produce the ledger-grounded design-vs-instrument verdict per §8 before the line verdict is finalized.

## §11 Machinery stack + bridge spec (build crew)

Use (paths under ~/workspace/tnn-lab): `wave9/trust-tiers/substrate/st_memory_core.zag` (+ `cl/common.zag`, `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag`) — memory substrate; `wave3/r27-consolidation/impl/psm.zag` — deliberate consolidation policy; `onebrain/impl/onebrain.zag` — GEN→ELIM→ARGMAX adjudication; `epistemics/principles_learned/delib_base.zag` — utterance intake pattern; `mg_chunking/intake.zag` — QA pattern. **Bridge (the preregistered core deliverable):** one thin NATIVE Zag module, English fact → claim-id registry. Normalization: lowercase, strip punctuation, collapse whitespace; hash the runtime (pre-escape) bytes (AGENTS.md znc lesson: never hash the escaped literal). claim_id = 32-bit FNV-1a of normalized text → first-seen dense slot via registry; one audit entry per registration; zero collisions over the frozen battery; FORBIDDEN: static lookup tables, concept-name keys, per-item branches, pre-seeded family slots — any of these = bridge rejected, line NO-GO. Determinism: 2× reruns + allocator perturbations, byte-identical claim ids (SHA-diff).
**znc lessons the build must honor:** no forward references (define callees first); no `as []i32/u32/u16` indexed tables — use `[]u8` arenas with LE accessors (aliasing miscompile); argc is always 0 — read `_zag_arg(n)` unconditionally; no slice > 2^25 bytes (chunk ledgers); `.*` only on true pointers; bare `return;` in void fns; never name anything `try` or `zalloc`; struct literals need dot-prefixed fields; no chained `s.field.subfield` (copy to local first); flatten >4-deep else nesting; `@import` paths per working-tree layout; O_TRUNC not O_CREAT|O_EXCL for writers.

## §12 Standing downstream rules

Pure Zag; zero randomness; byte-identical reruns (2× + allocator perturbations, SHA-diff); real English only; no hardcodes, no per-item patches, no frozen crew-authored architecture; commit to `tnn-native-lab` branch ONLY (never main); small disk footprint (check `df -h ~` before battery runs, stay above 2G free; never stage multi-GB work in /tmp — 512MB tmpfs); clean staging (results in git, staging dirs deleted after commit).

---
*Frozen 2026-09-27 by the DESIGN crew. Precedes all builds, teaching runs, and scoring. Amendments require Micah's explicit sign-off and a new dated version.*
