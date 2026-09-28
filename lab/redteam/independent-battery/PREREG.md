# PREREG — Independent Battery (red-team attacks #2 and #4)

**Frozen:** 2026-09-21 (PDT) · **Crew:** independent-battery · **Status:** FROZEN — no scored run may precede this file's commit.
**Parent mandate:** red-team attacks #2 (test-generation coupling: 156/156 contradiction mechanism dispatches on battery kind labels; disjoint vocabulary measured −25pp) and #4 (no "does it believe true things" instrument exists anywhere in the program).

## Question
Do the champion capabilities survive contact with a stranger's test — a battery sharing no code, templates, schemas, vocabulary, or kind-labels with the learner?

## Independence protocol (the load-bearing part)
1. **Two authors, one wire format.** The battery generator is written by a party that never sees the learner harness; the harness is written from the wire-format shape spec only, before the battery exists. The wire format is the only shared artifact.
2. **Sealed corruption.** The generator chooses a corruption rate (20–35%), seals it in `expected.json`, and discloses it to nobody until scoring. The harness never reads `expected.json` (enforced by construction: the harness opens only `items.jsonl`; the scorer is a separate program).
3. **Disjoint vocabulary.** The generator invents a fresh fictional domain. Lab vocabulary (mammals, platypus, boiling water, Mars, guilds, isles — anything used in any prior battery) is forbidden.
4. **No kind labels on the wire.** `items.jsonl` carries only `id`, `phase` (`teach`|`probe`), and `text`. Capability tags live only in sealed `expected.json`.
5. **Novel compositions.** The generator must include compositions its own inventory never directly produced (transitive chains, principle-mediated conflicts, negated conjunctions), so retrieval cannot reduce to template matching.
6. **Reproducibility.** The generator is deterministic given its sealed seed; `PROTOCOL.md` documents the process so a third party could re-run the independence.

## Wire format (normative — the only shared contract)
- `items.jsonl`: one JSON object per line: `{"id": N, "phase": "teach"|"probe", "text": "..."}`.
- ASCII only, no `"` inside text, single spaces, ≤240 chars.
- Sentence shapes:
  - `D1`: `<Name> <verb> <words>.` — singular fact. Name = single capitalized token.
  - `D2`: `<Name> is a <class>.` — class membership. class = single lowercase token.
  - `D3`: `Every <class> <verb> <words>.` — universal principle.
  - `D4`: `No <class> <verb> <words>.` — exclusion principle.
  - `Q1`: `Is it true that <D1-text>?` — yes/no truth probe.
  - `Q2`: `Which <class> <verb> <words>?` — wh probe; answer is a Name.
  - `Q3`: `First: <D1 A> Second: <D1 B> Do they agree?` — comparison probe.
  - `Q4`: `Which teaching act stated: <D1-text>?` — provenance probe; answer is a teach item id.
- Harness stdout, one line per probe: `V,<id>,<VERDICT>,<detail>` with VERDICT ∈ {AFFIRM, REJECT, ABSTAIN, CONTRA, CITE}; detail = value text | teach id | empty.

## Battery composition (targets; generator has latitude on exact counts)
- Teach: ~48 items (D1/D2/D3/D4), corruption 20–35% sealed. Corruption mix must include principle-violations, inter-claim contradictions, AND smooth lies (no contradiction, no principle violated) — the smooth lies measure the honest boundary.
- Probes: ~72, 12 per capability:
  - `contra` (Q3): genuinely conflicting pairs (one consistent with teaching, one not).
  - `false` (Q1): statements violating a taught D3/D4 principle → expected REJECT.
  - `para` (Q1/Q2): genuine rewordings (word order / synonym / voice changes), true facts → expected AFFIRM.
  - `truth` (Q1): one probe per corrupted-or-true taught fact, stating the taught claim → AFFIRM iff the taught claim was true, REJECT iff corrupted.
  - `abstain` (Q1/Q2): names/classes never taught → expected ABSTAIN.
  - `prov` (Q4): quote a taught D1 → expected CITE with the act id.

## Champion under test
One pure-Zag harness implementing the program's champion mechanisms generically (no kind-label dispatch — shape classification only, which is reading the question, not the answer key):
paraphrase-tolerant BoW/Jaccard retrieval (v1 prose), claim-vs-claim conflict detection (new-mechanisms), principle instantiation → derived-claim arbitration (principle-detection, with principle-priority per RSI T-PRIN-PRIORITY), withhold-on-insufficient-evidence (info-source).

## Coupled headline numbers (what the gap is measured against)
| Capability | Coupled headline | Source |
|---|---|---|
| contra | 1.0000 (156/156) | new-mechanisms conflict-driven deliberation |
| false | 1.0000 (13/13) | principle-detection derivation |
| para | 0.9649 (sol v1 prose) | prose-learning v1 (range 0.83–0.96; champion representative) |
| truth | *none exists* (attack #4 admits it) | new measurement; kill bar vs mirror baseline |
| abstain | *no clean coupled headline* | new measurement; reported absolute |
| prov | *no coupled headline* | new measurement; reported absolute |

## Kill bars (mechanical, adjudicated by `score_indep.py`)
- **KB-GAP:** independence gap = coupled − independent > 0.30 on contra/false/para → that capability's headline is GENERATOR-COUPLED; the headline is revised downward to the independent number in the verdict.
- **KB-TRUTH:** learner truth score (fraction of `truth` probes correct: AFFIRM true-taught, REJECT corrupted-taught) must exceed the mirror baseline (fraction of taught claims that are true — what a perfect copier scores). Else the program's "truthful" qualifier is SUSPENDED pending redesign. (Smooth lies are expected misses; the bar is *beat the mirror*, not perfection.)
- **KB-DET:** 5/5 byte-identical reruns, or the run is void.
- **KB-NOLEAK:** build/source audit confirms the harness never opens `expected.json`; the scorer is the first program to read it.

## Honesty clauses
- The harness author and generator author are both AI agents of the same program; "independent party" means process-separated (no shared code, no shared vocabulary, sealed labels), not a different species. Stated so the claim cannot be overread.
- The wire-format shapes are shared by necessity (a test needs a protocol); independence is about content, not about the English language.
- If the harness fails to parse the generator's sentences, that is a harness-coverage finding, reported as unparseable-rate — not silently dropped.

## Deliverables
`PREREG.md` (this file) · `gen_indep.py` · `PROTOCOL.md` · `items.jsonl` · `expected.json` (sealed) · `indep.zag` · `score_indep.py` · `runs/` (5 logs) · `SHA256SUMS` · `VERDICT.md` → `docs/lab/redteam/independent-battery/`.
