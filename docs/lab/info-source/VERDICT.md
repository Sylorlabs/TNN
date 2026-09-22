# Info-source richness — VERDICT

Date: 2026-09-22. Frozen prereg: `PREREG.md` (§4 kill bars KB-R0-BASE,
KB-CATCH, KB-CATCH-RATE, KB-CORR-INSTALL, KB-CONTEST, KB-SPOOF-RESIDUAL,
KB-DET). Amendment A1 (F05 distractor 300,000 → 150,000 km/s, pre-score)
recorded in prereg §7; bars unchanged.

Question: does falsehood detection **emerge from richer information**,
given that parameter scaling provably could not buy it (16/19 parameter
configs byte-identical learners, zero truth-detection at any size)?

## Result table

| Arm | Information environment | Falsehood absorption (12 planted) | Falsehoods installed | Catch rate | True corrections installed | Unknown facts (4) | Contested (4) | Spoof residual (2) |
|---|---|---|---|---|---|---|---|---|
| R0 | Facts only, no outside source | **12/12 absorbed** | 12/12 (teacher claims installed verbatim) | 0/12 | 0/12 | 0/4 answered | n/a (no search) | n/a |
| R1 | Facts + search, READ-ONLY | 0/12 | **0/12** (install mechanically refused) | **12/12** | 0/12 (read-only by construction) | 4/4 provisionally answered, 0 installed | 4/4 | provisional-wrong 2/2, **0 installed** |
| R2 | Facts + search, corroboration-gated editable (R-CORR) | 0/12 | **0/12** | 12/12 (every falsehood contradicted by ≥2 domains) | **12/12 true values installed** | **4/4 installed** (Ouagadougou, W, Mariana Trench, Swiss franc) | 4/4 | 2/2 spoofed values installed (expected honest boundary) |

## Kill-bar scorecard

| Bar | Requirement | Result |
|---|---|---|
| KB-R0-BASE | R0 absorbs ≥10/12 | **12/12 → PASS** (baseline reproduced: a closed learner believes its teacher) |
| KB-CATCH | R1 and R2 install 0/12 falsehoods | **0/12 and 0/12 → PASS** |
| KB-CATCH-RATE | R1 catches ≥10/12 | **12/12 → PASS** |
| KB-CORR-INSTALL | R2 installs true value on ≥10/12 falsehoods AND ≥3/4 unknowns | **12/12 and 4/4 → PASS** |
| KB-CONTEST | 4/4 contested dispositions match §2 | **4/4 → PASS** (C1 WITHHOLD 1v1, C2 PROVISIONAL_MAJORITY 2v1, C3 PROVISIONAL 2-agree, C4 WITHHOLD single-source) |
| KB-SPOOF-RESIDUAL | residual reproduces honestly | **Reproduced → PASS**: R1 provisional-wrong + 0 installs; R2 installs 2/2 spoofed values (two "independent" domains agreeing on a fiction defeat R-CORR — the known sensor-deceivable boundary, not hidden) |
| KB-DET | N=5 byte-identical per arm | **PASS** — full-run hash `cda86333…0a81` ×5; per-arm hashes stable ×5 |

## Verdict

**EMERGENCE CONFIRMED.** A learner that absorbed 12/12 planted falsehoods
with facts alone (R0) installs **zero** of them once it can read the web —
and, with corroboration-gated editable installation (R2), it goes further:
it installs the **true** value on all 12 and answers all 4 previously-unknown
facts correctly. Parameter scaling moved cost but never capability; adding a
second information source moved capability. Falsehood detection is a function
of information richness, not parameter count.

## Caveats and limitations

1. **Unanimous-spoof residual is real.** R2 installed both spoofed values
   (Poseidonia, Uo) because two constructed "independent" domains agreed.
   Corroboration gates disagreement, not collusion. This matches the
   program's standing "truthful but sensor-deceivable" qualifier.
2. **C2 is mechanically provisional, semantically ambiguous.** "Tallest
   mountain" genuinely admits Everest (elevation) vs Mauna Kea (base to
   peak); the 2v1 majority rule fired correctly as a mechanism, but the
   answer should carry the ambiguity, not a bare value.
3. **R1's provisional answers are not knowledge.** Read-only mode catches
   falsehoods but installs nothing — its 4/4 unknown "answers" are
   withhold-or-provisional judgments, not installed facts.
4. **Recorded envelopes, not live scoring.** Search results were recorded
   live via SearXNG (`search.lumy.live`, 17 queries × 8 results) and frozen;
   the trial replays them deterministically. Live re-querying would add
   freshness, not change the mechanism verdict.

## Build notes (implementation, not prereg changes)

- **Hash-convention fix (generator bug, caught pre-verdict):** the Zag-side
  tamper check recomputes sha256 over the *unescaped runtime* string, so the
  embedded hash must be computed over the whitespace-collapsed bytes, not the
  backslash-escaped literal bytes. The first build hashed the escaped form
  and tripped tamper=1 on exactly the 5 facts whose snippets contain `"`.
  Fixed in `gen_is.py` (`zc()` = runtime bytes, `zg()` = literal bytes,
  `rhash()` over `zc()`). All 140 result hashes re-verified against the
  Zag-side recomputation (0 tamper flags in final runs).
- **C3 test-data fix:** the first assembly picked two same-domain
  (wikipedia.org) "Paris" results; the mechanism correctly WITHHELD (only
  one distinct domain). Rebuilt to require two *distinct* domains, matching
  prereg §2's "2 domains agree" case.
- F05 A1 amendment was pre-score and is in prereg §7; no bar changed at any
  point after scoring began.

## Reproducibility

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- `src/is_trial.zag` + generated `src/is_cases.zag` (1,061 lines, pure Zag)
- 5/5 full runs byte-identical: `cda86333df6d83b79e6da671227ce64045bd2cacab2fb1b27322bf8f698a0a81`
- Per-arm N=5: R0 `af63c7e0…73862`, R1 `2fe7843e…0c89d2`, R2 `fc57de6b…0510ca`
- Independent verifier `verify_is.py`: ALL EXPECTATIONS HOLD on all 5 runs.
- Live envelopes: `live/*.json` (17 files, recorded 2026-09-22).
