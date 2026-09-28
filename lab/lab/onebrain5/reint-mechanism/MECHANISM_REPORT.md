# Reintegration mechanism report — why it helped (+14) and harmed (−3)

**Job 1 of 3, one-brain follow-up. Date: 2026-09-27 (PDT).**
**Question (Micah's order):** white-box WHY reintegration helped on 14 items and harmed on 3 — mechanism per item, proven by intervention. No hand-waving.

## The answer in one paragraph

Reintegration helped and harmed through **the same single ranking step**. The reintegration decision (`reint_better`, `impl/onebrain_v4.zag`) ranks surviving bids by a fixed priority list: grounded-in-a-fact first, then **fact overlap** (`inter` = how many query keywords hit the bid's grounding fact), then fact quality, then branch agreement, then duel history, then evidence class, then raw score. On all 14 fix items **and** all 3 harm items, the fact-overlap step was the decider: it overruled both the raw score order and unanimous branch agreement to pick the bid whose fact had more keyword hits (inter=2) over the bid whose fact had fewer (inter=1). On the 14 fixes the extra keyword hits genuinely marked the right answer; on the 3 harms the extra hits belonged to the *revoked* claim ("really, moby dick… are the ones"), and the rule has no notion of revocation — so it picked the revoked claim's answer over the explicit correction. **Proven by intervention:** disabling the fact-overlap step erases all 14 fixes and all 3 harms (44/44 winners revert to the honest-null's); a surgical variant that protects correction-gated bids from the fact-overlap step erases the 3 harms while all 14 fixes hold (38/44).

## The rule, exactly

`reint_better(led, a, b)` returns whether bid `a` outranks bid `b`, comparing these keys in order (first difference wins):

1. **grounded** — bid grounded in a live gated fact beats a fallback-string bid (bids 22/23/24 always stage fallbacks)
2. **inter** — stronger fact overlap first (count of query keywords intersecting the bid's grounding fact)
3. **qual** — higher fact quality first
4. **agr** — more sub-deliberations left it standing as branch winner
5. **duelwin** — its gating reading won a duel
6. **evc** — substantive trigger evidence over absence-evidence
7. **score** — higher raw bid score
8. **lowest hid** — final tiebreak

Keys 1–6 are all non-score ledger facts; the trace's `nullcase` flag reads 0 on all 17 items below, meaning no decision here reduced to score/hid order.

## The 17 items: identical signature

Every one of the 14 fixes and all 3 harms has the **same ledger signature**:

| | winner | loser |
|---|---|---|
| fact overlap (inter) | **2** | **1** |
| raw score | lower (by exactly 2) | higher |
| branch agreement (agr) | 0 | **2** (both branches agreed on the loser) |
| deciding step | — | **inter** (the trace's `lose` line cites it) |

The fact-overlap step therefore outranks *both* score order and unanimous branch agreement. The only ledger difference between a fix and a harm is the **loser's gating reading**: on harms it is rd=0 (correction); on fixes it is rd∈{1,2,4} (resume/challenge/joke).

### Per-item table

Columns: W = winning bid (action, score, inter, qual, agr, gating reading); L = losing grounded bid (same fields). Deciding step is `inter` in all 17 (trace-verified). V1 = support-strength disabled; V2 = correction-protected.

| item | kind | W (bid/action) | W score/inter/qual/agr/gr | L (bid/action) | L score/inter/qual/agr/gr | deciding step | V1: fix/harm gone? | V2: outcome |
|---|---|---|---|---|---|---|---|---|
| q21 | FIX | 18 compose | 227 / 2 / 22 / 0 / compose | 17 resume | 229 / 1 / 11 / 2 / resume | inter | gone (→17) | fix holds (18) |
| q22 | FIX | 18 compose | 227 / 2 / 22 / 0 / compose | 17 resume | 229 / 1 / 11 / 2 / resume | inter | gone (→17) | fix holds (18) |
| q23 | FIX | 18 compose | 227 / 2 / 22 / 0 / compose | 17 resume | 229 / 1 / 11 / 2 / resume | inter | gone (→17) | fix holds (18) |
| q24 | FIX | 18 compose | 227 / 2 / 22 / 0 / compose | 17 resume | 229 / 1 / 11 / 2 / resume | inter | gone (→17) | fix holds (18) |
| q25 | FIX | 20 provenance | 221 / 2 / 28 / 0 / provenance | 19 challenge | 223 / 1 / 14 / 2 / challenge | inter | gone (→19) | fix holds (20) |
| q26 | FIX | 20 provenance | 221 / 2 / 28 / 0 / provenance | 19 challenge | 223 / 1 / 14 / 2 / challenge | inter | gone (→19) | fix holds (20) |
| q27 | FIX | 20 provenance | 221 / 2 / 28 / 0 / provenance | 19 challenge | 223 / 1 / 14 / 2 / challenge | inter | gone (→19) | fix holds (20) |
| q28 | FIX | 20 provenance | 221 / 2 / 28 / 0 / provenance | 19 challenge | 223 / 1 / 14 / 2 / challenge | inter | gone (→19) | fix holds (20) |
| q29 | FIX | 14 memory | 239 / 2 / 33 / 0 / mem | 13 joke | 241 / 1 / 16 / 2 / joke | inter | gone (→13) | fix holds (14) |
| q31 | FIX | 17 resume | 230 / 2 / 25 / 0 / resume | 13 joke | 241 / 1 / 12 / 2 / joke | inter | gone (→13) | fix holds (17) |
| q33 | FIX | 18 compose | 227 / 2 / 20 / 0 / compose | 17 resume | 229 / 1 / 10 / 2 / resume | inter | gone (→17) | fix holds (18) |
| q34 | FIX | 18 compose | 227 / 2 / 22 / 0 / compose | 17 resume | 229 / 1 / 11 / 2 / resume | inter | gone (→17) | fix holds (18) |
| q35 | FIX | 20 provenance | 221 / 2 / 20 / 0 / provenance | 19 challenge | 223 / 1 / 10 / 2 / challenge | inter | gone (→19) | fix holds (20) |
| q36 | FIX | 20 provenance | 221 / 2 / 25 / 0 / provenance | 19 challenge | 223 / 1 / 12 / 2 / challenge | inter | gone (→19) | fix holds (20) |
| q06 | HARM | 19 challenge | 224 / 2 / 22 / 0 / challenge | 16 correction | 232 / 1 / 11 / 2 / correction | inter | gone (→16) | **harm gone (→16), correct** |
| q07 | HARM | 19 challenge | 224 / 2 / 22 / 0 / challenge | 16 correction | 232 / 1 / 11 / 2 / correction | inter | gone (→16) | **harm gone (→16), correct** |
| q08 | HARM | 19 challenge | 224 / 2 / 22 / 0 / challenge | 16 correction | 232 / 1 / 11 / 2 / correction | inter | gone (→16) | **harm gone (→16), correct** |

(Every item also had a third candidate, bid 22 `clarify`, which loses on the grounded step as a fallback-string bid — it never decides anything here.)

### Why inter=2 marked the right answer on the fixes

`inter` counts query keywords that hit the bid's grounding fact. On the fix items the decoy bid leans on a thin fact and the right bid on a fact the query genuinely engages:

- **q21–q24** ("continue the louvre tale, but compare moby dick with pride and prejudice?"): the resume bid grounds in the thin louvre-tale fact (1 hit); the compose bid grounds in the comparison facts (2 hits). The comparison is the deliverable — the ranking is right.
- **q25–q28** ("prove the louvre story and cite the eiffel tower origin?"): the challenge bid leans on the thin louvre fact (1 hit); the provenance bid grounds in the cited origin fact (2 hits). The citation is the deliverable — right.
- **q29** ("tell me a joke, then remember the eiffel tower tale?"): the joke bid grounds in the thin joke fact ("joke" = 1 hit); the memory bid grounds in the eiffel-tower fact ("eiffel"+"tower" = 2 hits). The remember act is the deliverable — right.
- **q31–q36** (support-quality): same pattern — the wrong reading's trigger is prominent in raw score, but fact support favors the expected bid.

### Why inter=2 marked the wrong answer on the harms (q06–q08)

The queries are self-corrections, e.g. q06: *"really, moby dick and austen's novel are the ones; no, i meant prejudice?"* The correction target ("prejudice") appears **once**, via "i meant X" → inter=1. The **revoked** initial claim ("moby dick") appears twice → inter=2. The fact-overlap step counts keywords with no notion of revocation, so it reads the revoked claim as "better supported" and picks bid 19 (challenge, grounded in the moby-dick fact) over bid 16 (correction, grounded in the prejudice fact) — overruling both a higher score (232 vs 224) and unanimous branch agreement (2–0). **The harm is the fact-overlap step being revocation-blind**, not a different mechanism.

## Intervention proof

Two single-step variants of the frozen source were built with the pinned toolchain (`498abcb5…1357e58ef`), run on the frozen v7 set in `nov4` mode (reintegration on, V4 off), twice each, byte-identical reruns.

- **V1 — support-strength disabled** (`reint_better`: inter and qual forced equal, so ranking falls through to branch agreement → duel → evidence → score → hid).
  - Result: **all 14 fixes gone, all 3 harms gone**; V1 winners match the honest-null (`nov4nG`) winners on **all 44 items**; score 24/44. Nothing else changed anywhere.
  - Trace check (q21): `lose bid18: less branch agreement agr=0 vs 2` — with the step off, branch agreement picks the score-order bid.
  - Nuance found honestly: on all 17 items the inter=2 fact also had higher `qual`, so `qual` agreed with `inter` everywhere — disabling `inter` alone would *not* have removed the effects (qual would have decided identically). The intervention neutralized the whole support-strength step (inter + qual). The trace's `lose` lines cite `inter` because it is the first differing key, but `qual` is a silent co-decider on this set.
- **V2 — correction-protected** (`reint_better`: the inter/qual step is skipped whenever *either* bid is gated by the explicit correction reading, gr=0 "i meant X"; `reint_why` mirrors the skip so traces stay honest).
  - Result: **all 3 harms gone** (q06–q08 now answer 16, the expected correction), **all 14 fixes hold**, and V2 differs from `nov4` on **no other item**; score 38/44.
  - Trace check (q06): `lose bid19: less branch agreement agr=0 vs 2` — with the correction shielded from the overlap count, unanimous branch agreement picks the correction.
  - This proves the fixes and harms, while driven by the same step, are **separable at the step level**: the separator is whether the demoted bid is an explicit user correction. Principle: "i meant X" is an operative act, not a keyword-overlap contest — a correction-grounded bid should not be demotable by raw overlap counts.

## Entanglement verdict

The 14 fixes and 3 harms are **the same mechanism on the same ledger signature** — they cannot be separated by deleting the step (V1 removes both). They **can** be separated by a principled refinement of the step (V2: corrections are exempt from overlap-demotion), proven to remove all 3 harms while preserving all 14 fixes with zero side effects on the other 27 items. V2 is intervention evidence for separability, not an adoption recommendation — that is a governance call.

## What was NOT found

- No fix or harm on this set was decided by any other ranking step (qual, branch agreement, duel-win, evidence class, score, hid). The attribution is complete for v7; whether the inter-first ordering generalizes beyond v7 is not tested here.
- No RNG anywhere in the variant decision paths (source is pure Zag; reruns byte-identical).
- The single `nullcase=1` item (q37, anchor) is pre-existing in baseline `nov4` and unchanged by both variants.

## Evidence

- `INTERVENTIONS.md` — variant definitions, build SHAs, run SHAs, determinism record, full scoring.
- `impl/onebrain_v1_nosupport.zag` (SHA-256 `318c6400…`), `impl/onebrain_v2_corrprotect.zag` (`3a2b7bf9…`) — variant sources; each differs from the frozen source (`bbb1752e…`) only in `reint_better`/`reint_why` plus a `REINT_VARIANT` trace marker.
- `runs/v1_r1.out`, `runs/v1_r2.out` (SHA `7948df1d…`, identical), `runs/v2_r1.out`, `runs/v2_r2.out` (SHA `7fcf3c76…`, identical) — full traces, empty stderr.
- Binaries `impl/ob_v1` (`ebf94b07…`), `impl/ob_v2` (`c9a7b8d8…`) are build artifacts, not committed (repo standard: no binaries).
