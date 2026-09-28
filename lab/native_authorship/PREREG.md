# PREREG — Native-authorship conversion trial 1: chunker choice rule

**Program:** TNN native-authorship (Micah's vision: TNN itself authors its choices)
**Trial:** convert the text-intake chunking choice rule from frozen lookup to runtime deliberation
**Status:** FROZEN (bars below are final; any change needs Micah's re-approval)
**Date:** 2026-09-27

## §1 Goal and honest scope

The production text intake (`docs/lab/mg_chunking_promote/intake.zag`, entry
`tnn_intake`, promoted 2026-09-26 commit `e74271015`, regression gate 57/57)
chooses its chunking policy via `policy_winner(kind, shape)` — a frozen
if-chain mapping (question-kind, text-shape) to one of 9 candidates. The
decoration audit classifies this GENUINE mechanism / CREW-SCAFFOLDED authorship:
the choice rule was derived offline from measured results (57 questions x 9
chunkers) and frozen. On 26 never-seen traps it scored 13/25 with 12 misses and
1 panic — "nothing shows runtime invention of chunking."

This trial converts the **choice rule only**: classify→lookup→execute becomes
classify→deliberate→execute. The 9 candidates (CHAR, WORD, WORD>CHAR,
WORD?CHARSCAN, REV_WORD, BOTH_ENDS, SPAN3, SPAN5, END_DIRECT) are FIXED. The
classifier (`classify`, kinds 0–17) and `text_shape` are FIXED and may be used
as *evidence*, never as lookup keys. What must be TNN-native is the **choice**,
made at runtime from input-derived evidence by an eliminative deliberation
stage — not the machinery (the deliberation stage itself is crew-built, as all
TNN machinery is; the audit's authorship boundary is about the choice rule).

What this trial does NOT claim: new chunkers, a new classifier, or unification
with the dialogue/deliberation line (that line is mid-repair on fork divergence;
coupling this trial to it would confound both. A later trial may port a passing
chooser into the deliberation line.)

## §2 Arms

- **Arm L (control, frozen):** current production `tnn_intake` byte-identical
  from commit `e74271015`. Classify → `policy_winner` lookup → execute winner.
- **Arm D (treatment):** same classifier, same 9 candidates, same executor —
  but the choice is made by the deliberative chooser (§3). `policy_winner` must
  not be called, linked, or inlined on D's path (broker verifies by symbol/grep).

## §3 The deliberative chooser — required properties

The implementer may design freely within these constraints:

1. **Inputs:** `(qid, question bytes, text bytes)` ONLY. Never the expected
   answer, never oracle data, never the battery.
2. **Candidate consideration:** per input, at least **2** of the 9 candidates
   must be explicitly considered, each with ≥1 input-specific evidence item
   recorded (a fact about *this* question/text, e.g. addressing level,
   anchor position, text length class — not the kind label alone).
3. **Elimination:** candidates are eliminated by stated criteria against the
   evidence; the trace records elimination order and reasons. The survivor is
   executed.
4. **Trace:** every choice emits a machine-readable trace: candidates
   considered, evidence cited per candidate, elimination steps, final choice.
5. **Determinism:** zero RNG anywhere on the choice path. Byte-identical reruns.
6. **No disguised lookup:** the chooser must not implement a kind→candidate
   (or (kind,shape)→candidate) mapping by another name. K4 audits this.

## §4 Battery protocol

- **Fresh trap battery, N=26**, authored by a SEPARATE battery-generator agent
  working from this prereg only. Trap families must target the lookup's known
  weaknesses (next-wall verdict): novel parser vocabulary (sentences/lines,
  spelled ordinals, relative addressing), multi-level addressing, longer texts,
  edge text shapes, degenerate inputs (empty text must refuse cleanly — the
  W25 panic class).
- **Oracles fixed by the generator before the first run**, committed as a
  SHA-256 manifest BEFORE the implementer finishes. The implementer must never
  see the traps or oracles; it develops against the frozen 57-question
  production battery only.
- **Oracle ceiling:** the honest broker runs all 9 candidates per trap question
  and takes the best per question. This bounds what any choice rule can score.

## §5 Kill bars (all must pass; any failure kills the trial — no ship)

| Bar | Statement |
|---|---|
| K1 — beats the lookup | D_correct − L_correct ≥ **5** on the 26-trap battery |
| K2 — choice quality | D_correct ≥ ceil(0.8 × oracle_ceiling) |
| K3 — causality | (a) feature-scramble: replacing the chooser's input features with fixed constants changes ≥80% of its choices; (b) choice-matters: forcing D's choices to the fixed default (candidate 3) changes D's battery score by ≥3 |
| K4 — no disguised lookup | ≥90% of trap questions show ≥2 candidates with input-specific evidence in the trace; independent audit of 10 random traces finds none reducible to a kind→candidate mapping |
| K5 — no regressions | D scores **57/57** on the frozen 57-question production battery |
| K6 — determinism | two runs byte-identical + rebuild-from-source reproduction; zero RNG on the choice path |
| K7 — no oracle leakage | the D binary contains no oracle bytes (broker greps); oracle manifest committed before implementation completed (commit timestamps) |

**Void-for-battery (not a kill):** if L_correct > oracle_ceiling − 5 on the fresh
battery, the battery lacks headroom to test the direction — the trial is VOID
and the generator must produce a harder battery. A void is reported, not
counted as a kill.

## §6 Neuter probes (broker runs; §5 K3 is the bar, these are the methods)

- P-feat: constant-fold every input feature the chooser reads → count choice flips.
- P-def: override every choice to candidate 3 post-deliberation → score delta.
- P-trace: blank the trace emitter → choices must be unchanged (trace is
  instrumentation, must not steer the choice).

## §7 Red team (independent, only after broker GO on K1–K7)

Six families, from committed source: (1) reversal (negated addressing);
(2) disguised-lookup traps (same kind, different optimal candidate — deliberation
must win where mapping fails); (3) feature-adversarial (kind suggests X, text
demands Y); (4) degenerate (empty/short/pathological texts — clean refusal, no
panic); (5) long-text scaling; (6) trace-forgery (does the trace correspond to
the computation? cross-check trace claims against neuter behavior).

## §8 Phase gates

- **P0** (coordinator): this prereg frozen + committed. No implementation before.
- **P1a** (battery generator): 26 traps + sealed oracle manifest, committed.
- **P1b** (implementer, parallel with P1a): builds Arm D from this prereg;
  verifies K5/K6 on the 57Q battery; hard stop before the fresh battery; never
  sees traps/oracles.
- **P2** (honest broker, fresh eyes): builds L and D from committed source,
  runs both on the sealed battery, measures oracle ceiling, scores K1–K7,
  verifies K7 by inspection. Delivers GO/NO-GO per bar.
- **P3** (independent red team): only on broker GO. Six families (§7).
- **P4** (coordinator): ALL bars + red team pass → Arm D's chooser replaces
  `policy_winner` as the live choice rule in `intake.zag` (production promotion
  #2, with the 57Q gate re-run). Any failure → honest kill, report, no ship.

## §9 Evidence and commit rules

Pure Zag. Zero RNG. Byte-identical reruns. No binaries/`.zagd`/caches/derived
files in the repo. Commits via API replay (fetch origin, rebase onto current
head, verify SHAs, parent = current origin head; raw urllib fallback).
Disk at 99%: keep workdirs lean, clean staging after commit.
