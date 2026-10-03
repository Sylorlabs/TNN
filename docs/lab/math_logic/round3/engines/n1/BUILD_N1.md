# BUILD_N1 — N1 NATIVE-ENTAIL engine build record

Date: 2026-09-25 (PDT)
Crew: MATH R3 native engine N1
Status: **BUILD SUCCESS**

## Sources

- `n1.zag` — single-file pure-Zag engine (~2,350 lines). No other sources.
- Imports (relative to build CWD, per brief):
  - `../../../deliberation_depth/harness/R33_NATIVE_SHA256_V2.zag` (sha256/hex)
  - `../../../deliberation_depth/harness/dlb_util.zag` (arenas, file IO, DOut)

## Toolchain (pinned)

- Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Build CWD: `~/workspace/tnn-lab/math_logic/round3/engines/n1`
  (imports resolve relative to CWD)
- Exact command:
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 n1.zag --no-zagd --no-analyze --no-foreground-cache -o n1_bin`
- Binary SHA-256: `a4b0a33ed4d2fd98ccb3b1d8a148997100de0d8315c98edeec1061974464916d`
- Binary size: 279,318 bytes
- Zero RNG anywhere in the engine (no random calls; all iteration is
  index-ordered; ties broken by license id / state id).
- `n1_bin` was deleted after measurement; only sources are committed.

## Knowledge store (pinned)

Per coordination note 2026-09-25, the build is pinned to the R3 NL store:

- Path: `~/workspace/tnn-lab/math_logic/round3/batteries/knowledge/KNOWLEDGE_STORE_NL.md`
- Local file SHA-256: `910ea9da0989e113587a3856583ba1ec1ea8b4f59258ab3374f1b17b9220084a`
- Repo commit (tnn-native-lab): `db913da907d0` (per coordinator handoff)
- Format: `[KNNN] (kind)` header line + text line(s); 25 items, all 25 parsed.
- The parser also accepts the legacy `KNNN <text>` single-line format
  (fallback `knowledge/KNOWLEDGE_STORE.md`); the NL format above is the
  pinned one. No fallback was used for the smoke runs below.
- Sealed batteries were never read. The startup/input guard returns exit
  code 3 if any of the three CLI paths contains the substring `sealed`
  (tested on all three argument positions; tested with a dummy path —
  `sealed/` contents were never listed or opened).

## Smoke results (P01–P03, public development problems)

Store: the pinned NL store above. Command per problem:
`./n1_bin <problems/P0N.txt> <KNOWLEDGE_STORE_NL.md> <out.trace>`

| Problem | Verdict | States | Licenses | Steps | Trace SHA-256 |
|---|---|---|---|---|---|
| P01 (√2 irrational) | WITHHELD | 53 | 64 | 2000 | `85e9b96e35c2476585e71f771a24ecf35ab188ad8d1654ef68b833e4d0375137` |
| P02 (infinitely many 4k+3 primes) | WITHHELD | 55 | 64 | 2000 | `6c50fc50e8b4b5b872bacc0561bc1be538667acfa95375eb2aa56134e70568f4` |
| P03 (n^5−n divisible by 30) | WITHHELD | 53 | 64 | 2000 | `c634aaa8a499c9753986940c1d47ce4058e1bea76239c788c2aeb44e8a365037` |

- Determinism: 3 external reruns per problem → exactly 1 unique SHA-256
  each (byte-identical). Additionally each invocation runs the engine
  3× in-process on independent arenas and exits 4 on any trace mismatch
  (never triggered).
- Withholding is the honest outcome: the byte-pattern licenses derive
  fragments (definitions, conjunction splits, substitutions) but no chain
  reaches the goal-overlap bar or defeats the contradiction assumption.
- Exit-3 guard: verified on arg1/arg2/arg3 with dummy `sealed` paths.

## Architecture (as built)

- Text-state rewriting over a byte arena (`tx`, 2 MB). State stack holds
  Input (src 0), KnowledgeCite (src 1), Inference (src 2), and
  ContradictionAssumption (src 3) states with premise ids, depth, and
  byte-span hole provenance (state id, hole id, tx offset, length).
- ~20 fixed byte-shape idiom recognizers mint licenses only when their
  anchors occur in a knowledge item's bytes: MP, CONTRA, IMPLIES, LEMMA
  (if C, then Q, ≤3 conjuncts), BICON-F/B, DEF, NEGPAIR, UNIV, CONJ-L/R,
  EXISTS, SUCHTHAT, SUBST, TRANS, IFF-F/B, THEREFORE, HENCE, ASSUME.
  On the NL store 64 licenses mint (cap reached: ASSUME + 63).
- Licenses carry premise byte-patterns (literal segments + hole segments),
  cross-premise byte-equality constraints, and output templates whose
  holes must all resolve to premise spans.
- Honesty: every emitted hole comes from a premise byte span; output words
  (≥4 bytes, non-stop) must occur in a premise or the license's own literal
  pool; >3 bindings for a premise match withholds the candidate.
- Forward chaining, deterministic order (prospective quality desc, then
  license id asc, state id asc); contradiction referee defeats the
  lower-quality side on (shared non-stop word ≥4 bytes + opposing local
  polarity); assumption defeat proves the goal.
- Trace (`N1-TRACE v1`) lists licenses, states with quality/premises/text,
  per-hole byte-span provenance, ranked candidates, and challenge counts.

## Simplifications vs the frozen spec (with mechanism-level reasons)

1. **Assumption quality fixed at 10 (src 3).** The frozen quality
   categories cover input/citation/inference only. The contradiction
   assumption is a deliberate low-trust construct; fixing its quality at 10
   guarantees established evidence (input 1000, citations ~800, inferences
   derived from them) defeats it in the referee, which is the mechanism by
   which proof-by-contradiction succeeds. Without this, a fresh assumption
   could tie or beat the evidence that refutes it.
2. **Byte holes, not variables:** single-letter alpha tokens become holes
   (pure byte-shape rule); multi-letter tokens stay literal. No typed
   scoped variables, no term grammar — the license patterns are byte
   shapes, and binding is byte-span capture.
3. **Fixed quality scale ×10 integers:** Input 1000; citation
   800−100×challenges; inference min(premise)−20×depth; corroboration
   +150 per independent path; uniqueness +50×(distinct bytes/total).
   Integer math only (no floats in the engine).
4. **Hard caps:** 64 licenses, 600 states, 2000 expansion steps, 3 duplicate
   byte-equal states with disjoint premises (corroboration), 20 SUBST
   products/run, depth >10 without corroboration withholds, 4 bindings max
   per premise match (5th sets the ambiguity flag → candidate withheld).
   These are load-bearing (heap arenas are fixed-size), not design limits.
5. **MP license's `=>` connective** is the license's own fixed byte shape,
   not item content; the license mints on the item's "modus ponens (" anchor.
   (The NL store writes "if P then Q", not "P => Q".)
6. **ASSUME license is always minted** (kind 3), not extracted from item
   bytes; its premise provenance cites the input's own byte span in-trace
   ("It is not the case that " + input bytes).
7. **Goal-proof bar:** an established depth≥1 state with goal-word overlap
   ≥ max(2, goal_words/2), or the assumption defeated by an established
   state. No formal entailment — overlap is the native proxy.
8. **Contradiction detector (known limitation):** shared non-stop word
   (≥4 bytes, case-folded stop list incl. store-mined words in ≥5 items)
   with opposing local polarity (±50/−60 byte window for negative markers).
   On P01 this spuriously defeated K004 (Euclid's postulates) and K005
   (rules of inference): the shared words "exactly"/"proof" carry a nearby
   "not" in one item ("a point not on it", "'not P'") but not the other.
   Both are axioms; neither truly contradicts its defeater. The mechanism
   is faithful to the Fable's byte-level rule; the window is crude. The
   licenses minted from those items still fire (licenses are not defeated
   when their citing state is), and the verdicts are unaffected, but this
   false-positive rate is the top candidate for a follow-up tightening
   (narrower window and/or requiring the marker to negate the shared word
   itself rather than its neighborhood).
9. **Stop list:** static list + store-mined words (folded, len≥3, in ≥5
   distinct items). Never split on or cite stop words.
10. **Trace INPUT sha256** covers the whole text arena (input + derived
    states), not the problem file alone; the problem path is printed
    alongside for identification.

## Notes

- Temporary build probes (`hello.zag`, `rec.zag`, binaries) and `n1_bin`
  were removed before commit; no `.zagd` files are committed.
- Debug `znc` findings hit during this build (for the record): passing
  **byte** offsets to `au_get32`/`au_put32` (they take element indices);
  struct locals need full literal initializers; the candidate-count slot
  needs arena element 2000*6 (off-by-one).

## Repair 2026-09-25 (v2 rescore): hole-provenance span emission

- **Defect (found in v1 scoring):** inference states recorded hole offsets as
  premise-relative (`n1_match` runs on the premise's tx slice
  `tx[oN..oN+lN]`), but the trace printer indexed the whole tx arena
  absolutely (`tx[ho..ho+hl]`). Every hole span cited the wrong bytes;
  v1 trace honesty was 8/24 on R3N and 0/12 on the sampled twin traces.
- **Fix (emission only, `n1.zag` ~line 1764):** at the `n1_hm_put` call site
  in `n1_try_add`, convert `ho` to tx-absolute by adding the premise's
  arena base (`po = o0/o1/o2` per `prem`, then `n1_hm_put(c,id,eq,pid2,hid,po+ho,hl)`).
- **Reasoning machinery provably untouched:** the `hm` table is written by
  `n1_try_add` and read only by the trace emitter (`n1_emit`'s hole print
  loop); `mb`, `n1_build_out`, `n1_con_ok`, search, referee, and verdict
  logic are byte-identical (diff vs pre-repair source: 1 comment + 4 lines
  at the single call site).
- **Rebuild:** same pinned toolchain and command (build CWD unchanged).
  Binary SHA-256: `d9a9a4cd57b0868c72963f854da068237ba4003c21c014885e792115e9d92aab`;
  size 283,414 bytes. `n1_bin` and any `.zagd` are excluded from commits.
- **Verification:** re-scored all 146 problems ×3 (byte-identical); repaired
  traces re-audited (see SCORECARD_R3_V2.md).
