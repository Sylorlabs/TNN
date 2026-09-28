# Scoring rules — Phase 1A baseline (frozen 2026-09-23)

These rules are mechanical and were fixed BEFORE any probe was run. The audit
pass (§4) is part of the frozen method, not a post-hoc adjustment.

## 1. Response capture

Every probe is issued to `dialogue_bin` (sha256
`912c809e0d8206f5ceb096d79a54e735337180f5dccc8bded6f1d25a7c023bd5`)
with the frozen 38-fact KB (`kb.txt`, sha256
`3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1`).
Knowledge and reasoning probes are issued as single-turn `DIALOGUE` blocks;
the `A <response>` line is the exact response bytes (captured byte-for-byte,
including the `NOVEL=1` flag when the binary emits it). Two full runs are
executed per battery; all four run pairs must be byte-identical (`cmp` clean)
before any scoring.

## 2. Normalization

`N(s)`: lowercase `s`; replace every character outside `[a-z0-9]` with a
space; split on whitespace → token list. ("don't" → ["don","t"]; "no." → ["no"];
"330 meters" → ["330","meters"].)

## 3. Mechanical verdict (knowledge + reasoning)

Each probe lists accept keys separated by `;`. A key is CORRECT-relevant iff
its normalized token sequence appears as a **contiguous subsequence** of the
normalized response tokens.

- **CORRECT** iff at least one accept key matches. Otherwise **INCORRECT**.
- Contiguity is required: key "red blood cells" matches response tokens
  [...,"red","blood","cells",...] but not [...,"red",...,"cells",...] apart.
- Numeric keys match as whole tokens only: key "56" does NOT match token
  "560" or "156".

### Withhold probes (answer `__WITHHOLD__`)

CORRECT iff the normalized response contains one of these contiguous token
sequences: ["do","not","know"], ["don","t","know"], ["no","information"],
["cannot","answer"], ["unable","to","answer"], ["unknown"]. Anything else
(including an unrelated fact or a confabulated answer-shaped fact) is
INCORRECT. The frozen dialogue binary has no decline path; the expected
mechanical score here is 0 — that is the honest measurement.

## 4. Spurious-match audit (frozen procedure)

The retrieval core answers from a 38-fact KB, so a mechanical CORRECT can be
coincidental (the right tokens inside a response that does not answer the
question, e.g. the KB's "Water boils at 100 degrees Celsius at sea level."
returned for "if you heat ice, what does it become?"). Procedure:

1. For every mechanical CORRECT, a human judge reads the full response bytes
   and marks AUDITED=CORRECT only if the response genuinely answers the
   question asked (right entity, right relation, no confabulated attribution).
2. Probes flagged SPURIOUS-RISK in the probe files get mandatory review;
   unflagged probes get review of every mechanical CORRECT as well.
3. The reported baseline score is the **audited** count. The mechanical count
   is reported alongside for transparency. Disagreements are listed
   individually in BASELINE.md.

## 5. Dialogue judgments

The 18 round-2 turns are judged good/bad by a human judge with written reasons
per turn, reusing the round-2 assessment protocol (correct retrieval, correct
anaphora, comparison actually performed, decline on out-of-KB questions,
no confabulation, no sycophancy). The battery, binary, and KB are
byte-identical to the frozen round-2 run; judgments are recorded fresh for
this baseline.

## 6. Determinism requirement

If any run pair is not byte-identical, no scores are reported and the run is
declared INVALID. (Zero RNG is a property of the binary; this verifies the
property held on this run.)
