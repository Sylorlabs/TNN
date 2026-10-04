# AUDIT: hell-hole v3 verifier — external dependence enumeration

**Crew:** C1 (AUDIT), hell-hole V4 campaign
**Date:** 2026-09-23
**Target:** hell-hole v3 trial (commit `51e944390`, `sylorlabs/TNN`, branch `tnn-native-lab`)
**Scope:** every external or online logic/source dependence in the v3 verifier, so the rebuild crew can eliminate them.
**Method:** read-only. All cited files fetched from the repo at `ref=tnn-native-lab` via the github skill and cross-checked against local copies. No files modified, nothing committed.
**Repo base path below:** `docs/lab/senses/web-search/internet-trial/phase3/`

**Classifications used:**
- **EXTERNAL-SOURCE** — evidence provenance problem: the data came from outside (live web, hand normalization) with no replayable capture, or a human supplied data the trial treats as observed.
- **EXTERNAL-JUDGMENT** — a human or external tool made a *decision* (label, verdict, tier, query, rule design) that the trial treats as TNN's reasoning.

---

## Summary verdict

The v3 pipeline's **code is native** (r12.zag, g_intent6.zag, v3_trial.zag, r3/r4/r5/r6.zag, compose.zag — all pure Zag, file-IO-only syscalls, zero RNG — verified §A). But the pipeline's **judgments are not TNN's**: the R6 "logic verdicts" were hand-written into the course JSON and hand-transcribed into the trial inputs (F1); the R3 gate column was hand-transcribed from hand-assigned claim types (F2); the R4 queries were hand-written, bypassing r4.zag (F3); all 51 V3 domain tiers are human judgments (F6); the helper's observations and joke intents are hand-written (F7, F8); and both classifiers' "knowledge" (negation/endorsement rules, joke phrase tables) was authored by the crew in Python and baked in (F10, F11). The evidence itself is hand-normalized with no raw captures (F4). The trial's byte-identical reruns prove **deterministic replay of human artifacts, not TNN derivation** (F14). M-LOGIC=1.0 / K-LOGIC CLEAR measure transcription fidelity, not logic.

---

## Findings

### F1. R6 "logic verdicts" are hand-seeded, hand-transcribed — the core violation (EXTERNAL-JUDGMENT)

- **What:** `course/v3_course.json`, items V3-20–V3-24: `mechanistic.logic_verdict = "CONTRADICTS"`, with hand-authored `component_facts` and `composition_steps` (verified by parsing the JSON). V3-14's verdict comes from a human-authored course note: `"the R6 mechanistic verdict also CONTRADICTS"` (`notes` field).
- **Transcription:** `trial_v3/evidence/candidates.tsv`, column 3 (`logic`): rows V3-14, V3-20, V3-21, V3-22, V3-23, V3-24 = `2` — set by hand from the JSON. No program performed this mapping; no mapping script is committed.
- **Consumption:** `trial_v3/src/v3_trial.zag:254-256` — `if(logic==2){ ... "CONTRADICTS: seeded mechanistic logic (component facts + composition steps)" }` → REJECT. The driver *says* "seeded" in its own ledger string.
- **The native R6 was never invoked:** `repairs/src/r6.zag:18-27` — `r6_logic()` hardcodes exactly one verdict: phase-2 `"C16"` → CONTRADICTS. It returns UNKNOWN for every V3 ID. No component extraction, no fact lookup, no CAUSES/PREVENTS/CONTAINS/IS-A evaluation exists in any committed Zag: the PREREG §2 composition schema was documented in prose, never implemented.
- **Why it matters:** PREREG.md §1-R6 requires *"For EVERY candidate, TNN composes a logic verdict from taught component facts."* The trial substituted a human verdict. M-LOGIC=1.0 and K-LOGIC CLEAR therefore score the human's transcription, not TNN's logic. This is the exact dependence Micah's directive targets.
- **Rebuild must:** implement native composition at trial time — component extraction from the claim, lookup against taught component facts, relation evaluation (CAUSES/PREVENTS/CONTAINS/IS-A with polarity) → CONTRADICTS/SUPPORTS/UNKNOWN. No verdict may enter via JSON or any precomputed column.

### F2. R3 gate column hand-transcribed from hand-assigned claim types (EXTERNAL-JUDGMENT)

- **What:** `course/v3_course.json` `claim_type` per item is hand-assigned (CONTESTED/EVOLVED/SKEPTICISM/JOKE-FAMILY/SETTLED). `trial_v3/evidence/candidates.tsv`, column 2 (`gated`): `1` for V3-10, V3-11, V3-12, V3-13, V3-18, V3-19 — transcribed by hand from `claim_type`.
- **Consumption:** `trial_v3/src/v3_trial.zag:248` — `if(gated!=0){ disp=4; attrib="R3" ... }` (terminal WITHHOLD).
- **The native R3 was never invoked:** `repairs/src/r3.zag:11,19` — `r3_gated()` knows only phase-2 IDs C5, C6, C8, C11, C12, C13; returns 0 for every V3 ID.
- **Rebuild must:** assign claim type natively (a TNN claim-type classifier or deliberated typing) *pre-search*, per PREREG §1-R3. Remove the `gated` column as a human input; the driver should call the native gate.

### F3. R4 queries hand-written; r4.zag's generator bypassed (EXTERNAL-JUDGMENT)

- **What:** `trial_v3/evidence/v3_queries.tsv:1-9` (header) documents it explicitly: *"natural disconfirmation phrasings are used instead of r4.zag's literal `"evidence against: <claim>"` prefix form, because the literal form returns junk on a live search engine."* All 48 query strings (24 neutral + 24 disconfirm) are human-written.
- **Bypassed code:** `repairs/src/r4.zag` `r4_disconfirm()` — deterministic, native, but its output was judged unusable and replaced by human phrasing via a documented design decision.
- **Rebuild must:** generate queries natively — fix the template or teach phrasing natively so the generator's output works on live search. No hand-written query ledger.

### F4. Evidence hand-normalized from live search; no raw captures, no transport hashes (EXTERNAL-SOURCE)

- **What:** `trial_v3/evidence/v3_search_results.tsv` — 72 rows (9 candidates × 2 queries × 4 results), hand-normalized from live `browser_search` results on 2026-09-23.
- **No raw captures:** TRIAL.md §d states it plainly: *"This is not the phase-2 sense-v2 envelope format (raw bodies, transport hashes not preserved). The trial's determinism rests on the frozen normalized TSV, not on replayable raw captures."*
- **Undocumented selection:** no evidence-collection log exists for the trial search (the committed `course/collection_log.md` covers *course discovery/verification*, a different step). Whether the 4 results per query are verbatim top-4 or human-curated is unrecorded.
- **Rebuild must:** capture raw page bodies + transport hashes at collection time (phase-2 sense-v2 envelope format) and replay the trial from raw evidence, not from a hand-normalized TSV. Log the result-selection rule.

### F5. Stance column is human annotation — verified inert, but a latent hazard (EXTERNAL-JUDGMENT, contained)

- **What:** `trial_v3/evidence/v3_search_results.tsv`, column 9 (`stance`): the author's collection-time annotation (SUPPORT/REFUTE/etc.).
- **Verified NOT in any decision path:** `trial_v3/evidence/r12_input.tsv` carries only `(rowid, claim, title, snippet)` — the local copy is byte-identical to the repo copy (diff-verified). The 72 vote rows derive from native r12 tags × tier weights (spot-verified: V3-01 weights 16/16/8 = T2/T2/T1 per the tier maps; the two weight-1 rows are exactly the two tier −1 domains, `rxiv.org` and `greentricks.me`). No committed or scratch v3 script reads column 9 (`gen_input.py`'s stance references are phase-2-only; `mk382.py`/`predict.py`/`proto_r12.py` never mention stance). TRIAL.md §1 confirms: *"the classifier's tags (not my manual ones) drive the trial."*
- **Rebuild must:** drop the stance column from all decision-path inputs entirely, so a future join cannot silently ingest human stances as TNN's.

### F6. All tier values are human domain-reputation judgments (EXTERNAL-JUDGMENT)

- **What:** `trial_v3/evidence/v3_tier_additions.tsv` — 51 rows; every `rationale` is literally the string `"blind domain-reputation assignment"`. Each tier is a human call (e.g. `science.nasa.gov→3`, `answers.com→0`, `greentricks.me→-1`, `rxiv.org→-1`). `repairs/evidence/tier_map.tsv` (frozen phase-2 base map) is likewise crew-built (explicit domain lists + suffix rules; cf. `repairs/tools/gen_input.py` `tier_of_domain`).
- **What's mechanical:** the tier→weight map (T3=32, T2=16, T1=8, T0=4, T−1=1) in `repairs/src/r5.zag`, and the tag×weight join into `solo_votes.tsv`/`helper_votes.tsv` (72 and 81 rows; verified consistent). The unknown-domain default tier 1 (per `compose.zag` header) is itself a human design choice.
- **Rebuild must:** replace hand tiering with a TNN-native source-reliability mechanism (or an explicit rubric *applied by TNN machinery*, not by the trial author). No human tier column.

### F7. Helper observations hand-written (EXTERNAL-JUDGMENT)

- **What:** `trial_v3/evidence/helper_obs.tsv` — 9 texts, hand-written by the trial author (*"written blind from claim text alone"*, TRIAL.md §f; also §d/Files). They are classified by the native r12 (mechanical — including its negation failures, e.g. V3-04 "Bats are not blind" → AFFIRM) and enter `helper_votes.tsv` as 9 extra rows at tier 0 / weight 4 (the tier-0-for-helper rule follows the `compose.zag:8-9` convention — itself a human design decision).
- **Rebuild must:** the helper arm must be TNN machinery (or the arm goes). No hand-written helper texts.

### F8. Helper joke intents + markers hand-written (EXTERNAL-JUDGMENT)

- **What:** `trial_v3/evidence/helper_jokes.tsv` — 4 rows, hand-written *"frozen blind"* intents and markers: V3-14 → `2` / `non-toxic glue`; V3-15 → `3` / `one small rock`; V3-16 → `3` / `microwave oven`; V3-17 → `5` / `directly at the sun`. These feed the helper rule in `v3_trial.zag:267-290` (AGREE / ADOPT_HELPER / KEEP_CLASSIFIER) via `jokes_helper.tsv` columns 3–4.
- **Rebuild must:** same as F7 — helper judgments must come from TNN machinery or the helper arm is removed.

### F9. The asymmetric helper rule is human safety design (EXTERNAL-JUDGMENT, frozen in code)

- **What:** `jokes/GATE_SPEC.md` §"Helper combination rule (frozen — the deadpan-fooled repair)" + `trial_v3/src/v3_trial.zag:23-24,267-290`. The asymmetry — helper may add non-sincere flags (2/3), never manufacture sincerity; marker-substring test — is a human-designed safety invariant, mechanically executed.
- **Rebuild must:** keep the mechanism (it is native code), but either derive/justify the rule natively or keep it as an explicitly frozen, Micah-signed safety law — not as something TNN "decided."

### F10. r12's linguistic knowledge was authored by the crew in Python (EXTERNAL-JUDGMENT, baked in)

- **What:** `repairs/src/r12.zag:1-4` header: *"Ports tools/proto_r12.py EXACTLY (byte-identical tags on the frozen course)."* The negation lexicon, endorsement-evidence rules, clause-scoped negation, and the R1 "no fallthrough-to-AFFIRM" policy were designed in Python by the crew; the Zag is a port. The classifier is native at runtime (§A), but its *knowledge of what counts as negation/endorsement* is crew-authored, not TNN-taught or TNN-learned. (This is also where the systematic V3 failures live — TRIAL.md §5a.)
- **Rebuild must:** move linguistic knowledge into TNN-taught/learned knowledge with provenance, per Micah's "proper knowledge" principle — not crew-authored lexicons baked into the binary.

### F11. Joke classifier's phrase/pattern KB is crew-built, with held-out test-set influence (EXTERNAL-JUDGMENT, baked in)

- **What:** `jokes/round2/src/g_intent6.zag:1-4`: *"GENERATED by round2/work/gen_gate_r6.py — config 6; do not hand-edit. Config 6: 32 active patterns, 321 phrases."* Generated from crew-built JSONs (`work/patterns_r2.json`, `work/phrases_r2.json`, `work/phrases_r4.json`, `work/vocab_r6.json`) plus the crew-written ROUND2.md §4 component-fact schema.
- **Test-set influence:** `jokes/round2/work/PROVENANCE.md` flags **48 phrases (H)** — occurring in held-out test texts, never in training — i.e. the classifier's vocabulary was shaped by the test set. *"SINCERE(1)/DECEPTIVE(4) never emitted"* is true by human construction, not by TNN judgment.
- **Already acknowledged:** PREREG.md §3 invention note: *"crew-built marker machinery is test scaffolding, not TNN inventing humor understanding."*
- **Rebuild must:** TNN-native joke/intent understanding; purge held-out-influenced phrases; nothing about the intent taxonomy may be unreachable-by-construction human fiat unless explicitly signed as a safety law.

### F12. Evidence-derivation chain has no committed generator (EXTERNAL-SOURCE, provenance gap)

- **What:** `trial_v3/` contains only `TRIAL.md`, `digests.txt`, `evidence/`, `ledgers/`, `src/v3_trial.zag`. No script shows how `v3_search_results.tsv → r12_input.tsv → r12 run → solo_votes.tsv/helper_votes.tsv`, or `jokes_input.tsv → g_intent6 run → jokes_solo.tsv/jokes_helper.tsv`, were derived. (Note `g_intent6.zag` has no `main` and no syscalls — it is a library; whatever driver ran it over the joke inputs is uncommitted.) The joins spot-check as mechanical (F5/F6), but they are not re-derivable from the repo.
- **Rebuild must:** commit the full derivation chain as runnable native code; zero uncommitted scratch steps between frozen evidence and the trial driver.

### F13. Oracle labels are human ground truth — correctly scoring-only (EXTERNAL-JUDGMENT, properly contained)

- **What:** `course/v3_course.json` `oracle_label` per item (TRUE/FALSE/CONTESTED/JOKE/SKEPTICISM/EVOLVED), frozen pre-run per `course/collection_log.md`. Used only for scoring (M1/K1/M-LOGIC/etc.), never enters the decision path. This containment is correct and must be preserved — ground truth has to come from somewhere; the violation would be letting it steer dispositions.

### F14. Determinism-scope caveat (cross-cutting)

- The 3× byte-identical reruns (TRIAL.md Determinism section) prove the *pipeline* is deterministic given frozen inputs. The frozen inputs are the human artifacts in F1–F8. **Deterministic replay of human judgments is not TNN derivation.** The rebuild's determinism bar must apply to a pipeline whose judgments are all native.

---

## §A. Verified ALREADY NATIVE — no replacement needed

Each item verified at source level (extern list + syscall numbers) against the repo copy at `ref=tnn-native-lab`:

| Component | File | Verification |
|---|---|---|
| Stance classifier | `repairs/src/r12.zag` | Pure native Zag. Externs: only `_zag_arg`, `_zag_malloc`/`_zag_free`, `_zag_print`/`_zag_println`, `_zag_raw_syscall`, `_zag_slice_ptr`. Syscalls: 0 (read), 2 (open), 3 (close) only — file IO, no network. Zero RNG, no time/PID. SHA-256 `a867c3be…` matches TRIAL.md's frozen hash; repo copy byte-identical to the local frozen copy (diff-verified). |
| Joke intent classifier | `jokes/round2/src/g_intent6.zag` | Pure native Zag **library**: zero `_zag_raw_syscall` (no IO at all), no `_zag_arg`, no `main`. Zero external calls of any kind; zero RNG. (Its baked-in phrase KB is the issue — F11 — not the code.) |
| Trial driver | `trial_v3/src/v3_trial.zag` | Pure native Zag. Pipeline order R3 gate → R6 → joke → R5 vote implemented mechanically (`:248`, `:254`, `:267-290`, R5 vote block). Externs: arg/alloc/print/file-IO only; syscalls 0/2/3 only. No network, no RNG, no time/PID. |
| R3/R4/R5/R6 repairs, composer | `repairs/src/r3.zag`, `r4.zag`, `r5.zag`, `r6.zag`, `compose.zag` | Pure native Zag, file-IO-only or no syscalls. **Caveat:** `r3_gated`/`r6_logic` hardcode phase-2 IDs and were bypassed in v3 (F1/F2); `r4_disconfirm`'s template was bypassed (F3). Native code, but not the operative mechanism — the rebuild must make them (or successors) operative, not replace their nativeness. |
| R5 weighting, R3-persistence, helper-rule evaluation, vote joins | in the above | All mechanical integer arithmetic in native code; spot-verified against evidence TSVs. |

---

## Rebuild checklist (numbered, in dependency order)

1. **Native R6 composition.** Implement component extraction → taught-fact lookup → CAUSES/PREVENTS/CONTAINS/IS-A polarity evaluation → CONTRADICTS/SUPPORTS/UNKNOWN in native Zag, run at trial time per candidate. Delete the `logic` column as a human input; delete seeded `logic_verdict`s from the course format (keep component *facts* as taught knowledge, never verdicts). (Resolves F1; satisfies PREREG §1-R6/§2.)
2. **Native claim typing.** Assign claim type (SETTLED/CONTESTED/AMBIGUOUS/EVOLVED/SKEPTICISM/JOKE-FAMILY) via TNN machinery pre-search. Delete the `gated` column as a human input; wire the driver to the native gate. (Resolves F2.)
3. **Native query generation.** Ship an R4 generator whose output works on live search (fix/replace the `"evidence against:"` template or teach phrasing natively). Delete the hand-written query ledger. (Resolves F3.)
4. **Raw evidence capture.** Collect raw page bodies + transport hashes at search time (sense-v2 envelope format); replay from raw evidence; log the result-selection rule. (Resolves F4.)
5. **Purge human annotation columns.** No stance or verdict columns in any decision-path input. (Resolves F5.)
6. **Native source reliability.** Replace hand tiering with TNN-native reliability assessment; remove the human tier column and the default-tier-1 fiat (or sign it as an explicit law). (Resolves F6.)
7. **Helper arm.** Helper observations, intents, and markers must be produced by TNN machinery, or the helper arm is removed. (Resolves F7, F8.)
8. **Helper rule provenance.** Keep the asymmetric rule as native code; record whether it is TNN-derived or a Micah-signed safety law. (Resolves F9.)
9. **TNN-owned linguistic knowledge.** Move negation/endorsement knowledge out of crew-authored Python ports into TNN-taught/learned knowledge with provenance. (Resolves F10 — and is where the §5a classifier failures must actually be fixed.)
10. **TNN-owned joke understanding.** Rebuild intent classification on native understanding; purge the 48 held-out-influenced phrases; no unreachable-by-construction intent codes unless signed as safety law. (Resolves F11.)
11. **Committed derivation chain.** Every step from raw evidence to trial inputs is committed, runnable native code. No scratch gaps. (Resolves F12.)
12. **Oracle containment.** Keep oracle labels strictly scoring-only; assert mechanically that no oracle field is readable from the decision path. (Locks in F13.)
13. **Re-verify nativeness after every change.** Extern audit (arg/alloc/print/file-IO only; syscalls 0=open-excluded… i.e. read/open/close only), zero RNG, byte-identical reruns, SHA-pin every frozen source. (Locks in §A; guards F14.)

## Audit caveats (what was NOT verified)

- Sources were audited, not executed: no binaries were re-run; the extern/syscall surface is source-level.
- The joke-gate round-6 training corpus and gate evidence were summarized from `PROVENANCE.md`/`GATE_SPEC.md`, not fully re-audited.
- Whether the 4-results-per-query are verbatim top-4 or curated is unrecorded (F4).
- The hash-chaining step that produced `trial_v3/ledgers/` was not traced to a committed script (related to F12).
- The v3 verdict's correctness claims (M1/K1 margins, §5a classifier failures) were taken from TRIAL.md as reported; only the external-dependence surface was independently verified.
