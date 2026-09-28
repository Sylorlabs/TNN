# PATH_MECHANICS.md — how dialogue natively generates

**Path:** dialogue / text generation
**Native source:** `~/workspace/tnn-lab/dialogue/dialogue.zag` (pure Zag, pinned toolchain, zero RNG)
**Entry point:** `do_compose` at `dialogue.zag:1302`; the full turn pipeline is `do_turn` at `dialogue.zag:1538`; driven by `main` at `dialogue.zag:1785`.

## 1. The generation pipeline (do_turn, :1538–1761)

A turn is a 5-branch deterministic dispatch on the current utterance, in fixed priority order:

1. **Correction** (`:1544–1614`): if the utterance is a correction (`is_correction`, :1438) and the previous turn was a retrieval (`pkind==0`), strip the correction marker, rebuild the query, and call `retrieve` **excluding the previous answer fid and its primary entity** (`retrieve(fm,keya,kid,plen,pans,excl_eid,fea,-1)` at :1592). The old output is *excluded from candidacy* — never consulted, never arbitrated with.
2. **Topic resume** (`:1616–1635`): `is_resume` (:1448); pops/pushes the topic stack (`top_pop_to`, `top_push`, :844–864) and emits a general fact for the topic entity via `general_fact` (:981).
3. **Composition** (`:1637–1644`): `do_compose` (:1302). Four frozen pattern branches — "was the author of … before …" (:1303), "which is taller" (:1324), "did … write" (:1356), "birth year" (:1405, morphology crew repair). Each resolves entity/year ids from KB tables and assembles the response from fixed template literals (`"yes."`, `"no."`, `" is taller."`) plus copied KB strings.
4. **User assertion / contradiction** (`:1646–1692`): if the utterance is not a question, `extract_assert` (:1021) parses a (subject, relation, value) claim, stores it in the user-claim store via `uclaim_check` (`uc`, :1189), and either emits `"NOTED."` or `"CONTRADICTION: turn N said X."` when it conflicts with an *earlier user claim* — note: earlier *user* claims, not earlier system outputs.
5. **Default retrieval** (`:1694–1759`): resolve pronouns/ellipsis against the salience stack (`build_resolved`, :728; `use_ellip`, :1701), parse to keyword ids (`proc_sentence`, :390), score all KB facts by cross-multiplied Jaccard (`retrieve`, :936; `jscore`, :463), emit the winner verbatim via `emit_fact` (:1481).

**Emission itself is byte-copy, not generation.** `rclr` (:866) zeroes the response length; `rput` (:867) appends bytes. `emit_fact` (:1481–1498) copies frozen KB fact text into the response verbatim, or emits the sentinel `"UNCERTAIN."` if no fact matched. There is no word loop, no token sampling, no sequential unit-by-unit rendering of any kind. The "cursor" is append-only and **never re-read during generation**.

## 2. What the "plan" is

The dialogue plan has four parts, all fixed before a response is assembled:

| Component | Source | Mutability |
|---|---|---|
| **KB facts** (38) | `kb.txt`, installed once at boot by `kb_install` (`:892`) | write-once; never written during turns |
| **Entity gazetteer** | `gaz.txt`, `gaz_install` (`:578`) | frozen |
| **Parsed utterance** | keyword-id set from `proc_sentence` (`:390`): tokenizer → stemmer (`stem_inplace`, :270) → irregular-norm (:305) → vocab intern (`v_intern`, :529) | per-turn input |
| **Discourse state** | salience stack `sal` (:804), topic stack `top` (:824), prev-turn vector `pv` (ans/eid/peid/qraw/q/kind@28, :1536), prev-query bytes `pqb`, user-claim store `uc` (:1189), history log `hist`/`histb` (:1523) | carried across turns, **all input-side** |

Crucial: every carried structure records *what the user said, which entities were mentioned, which facts were emitted* (as integer ids) — it is **memory of the conversation**, not generated output feeding back into generation. The KB itself is never written by any turn.

## 3. Carried-state inventory: is ANY of it output state?

Walked every read of every cross-turn structure inside the generation path:

- `sal` (salience): entity ids pushed by `push_ents`/`sal_push` (`:1455`, `:804`) from *utterance* scans and *fact* entity lists (integer ids, plan-side). Read by `build_resolved` (:728) for anaphora and by the no-entity fallback (:1719). Never holds response text.
- `top` (topic stack): entity ids only. Read by resume branch. Never text.
- `pv`: fact/entity ids + byte *offsets of the user's query* in `pqb`. Read by correction (:1549–1590) and ellipsis (:1704–1729). The query bytes are *user* bytes, not system output.
- `uc`: (subject, relation, value, turn) tuples extracted from *user assertions*. Read by `uclaim_check`. User-side provenance, labeled by turn.
- `hist`/`histb`: the append-only turn log. Written by `hist_add` in `main` (`:1860`, `:1863`) — utterance bytes (kind 0) and response bytes (kind 1). **Read exactly once** in the generation path: `novelty_ok` (`:1500`), which checks the composed response is not a substring of any KB fact or prior turn, then sets a flag (`novelf`) that `main` prints as `NOVEL=1` (`:1867`). It is a **post-hoc measurement**. It does not alter the response, does not feed any generation decision, and does not write to any plan structure.
- `last_fid`: the fact id emitted last turn, passed to `retrieve` as `tbfid` (`:1751`). Used at `retrieve` (`:973`): on an **exact Jaccard tie** (`lhs==rhs && rhs>0`), prefer the previously-emitted fact. This is the single place where a value derived from a prior turn enters a generation decision — and it is a *plan-side integer id* used as a continuity tie-break, not emitted text, and it cannot override a strictly better score.

**Verdict: zero carried *output* state.** No byte of generated text is ever read as generation input. The response buffer `resp` is cleared at the start of every branch and never re-read within a turn (the only read, `novelty_ok`, is measurement-only).

## 4. The classification question — answered explicitly

The survey (`~/workspace/bytegen/survey/FINDINGS.md`) classifies `do_compose` as **OTHER (template slot-fill)**:
> "Rule-based: pattern-match question type, copy fact strings into response via `rput` (e.g. lines 1317-1319, 1347-1349). Response is a fixed function of matched KB facts; whole utterance assembled from the plan; cursor is append-only. No byte-level feedback, no generative loop at all."

This re-verification **confirms** the classification, and sharpens it: it is not merely that dialogue isn't PAR or AR — **the PAR-vs-AR-vs-hybrid question does not apply to dialogue at all, because dialogue is not byte rendering.** The question presupposes a sequential unit-by-unit rendering process (samples, pixels, tokens) where "feedback" means "later units conditioned on earlier units." Dialogue has no units and no sequence: a response is a single atomic assembly `response = D(utterance, KB, discourse_state)`, computed whole by branch dispatch, emitted by memcopy. There is no `n` at which unit `n` could read units `0..n−1`, because there are no units.

The only coherent translations of "output feedback" into dialogue mechanics are:

- **(a) Reading emitted text to choose subsequent text** (the LLM way the audio report explicitly rejects): structurally absent — there is no subsequent text; the response is complete when the branch returns.
- **(b) A repair loop over the composed response** (generate → detect fault → re-render): structurally absent — no detection pass exists, and no re-render path exists.
- **(c) Prior-output-derived values biasing the next turn** (`last_fid` tie-break): present but plan-side (integer fact id, exact-tie only), and user-claim memory (`uc`): present but explicitly *user*-side provenance.

Dialogue is a **different kind of generation entirely**: plan-absolute symbolic assembly with integer-id discourse memory. It is the path where the audio bytegen debate's vocabulary (loops, servos, latches, contraction maps) has no referent — and that fact itself is the load-bearing finding of this report (see UNIVERSAL_VS_PERPATH.md).
