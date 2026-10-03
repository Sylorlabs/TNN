# VERIFICATION — v6 operative-utterance understanding

**Date:** 2026-09-28 (UTC). **Toolchain:** `znc 2026.07.0-dev (edition 2026)`
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).

## What v6 is

v5's correction *reader* (bare-token triggers `no`/`actually`/`meant`/`correction`) was
killed 4× by red team (quoted / hypothetical / negated / hedged fake corrections).
v6 replaces it with **operative-utterance understanding**: a native deliberative
mechanism, not a classifier module. `gen_readings` runs a single understanding pass
(`ou_annotate`, in `utterance.zag`) that records each query token's operative status
(0 = not a correction trigger, 1 = operative correction, 2 = quoted, 3 = reported,
4 = hypothetical, 5 = negated, 6 = hedged, 7 = no operative pattern) as deliberation
state; the correction reading (rd==0) consults these annotations for its evidence and
topic window. The v5 reintegration skip is unchanged and now keys off understood
operative corrections rather than bare tokens.

Per Micah's 2026-09-27 correction, nothing here is framed as a classifier: this is
TNN's own machinery for determining an utterance's operative status as part of its
understanding/epistemics, living inside deliberation.

## Frozen artifacts (SHA-256)

| file | SHA-256 |
|------|---------|
| `utterance.zag` (= `build/utterance.zag`) | `23672e6a44cd8d579da3c4e96a8a8c870b4a59a6775e5209f1b8ad923ef46ca4` |
| `ou_test.zag` | `d9071bcc83db36e8c724f4c3e49e9efc8e800a00d3955a9cdd32795e5f333933` |
| `PREREG.md` (with 2026-09-27 reframe amendment) | `ac9ce9c449c03cbab5b892bdfc01afbd03cbd01dd7cbb66d1c7a335d43b9adbd` |
| `build/onebrain_v6_utterance.zag` | `bd9ca17b7d07dbcac7ac2d5d93d3ae3506d20a1131685839fc50b821c28c99d6` |
| `build/ob_v6u` (binary) | `8571c334b1f2e529409ace4d1068459d52cd361092255e0eca839ea06c4be0f6` |
| `ou_test` (binary) | `6259793ae96f32b38345ec0a85e1b76ee9c0ecff8a4e8731b10944e908c9e0f8` |

**Implementation correction 2026-09-28** (no §2 change): the first independent
red team found 2 kills (one root cause) — `utterance.zag`'s R3 "according…to"
check only tested the immediately following token (v+1) for `to`, while frozen
§2 requires "to" within the next 2 tokens (v+1 or v+2). `"according even to the
teacher, i meant moby dick?"` was mis-annotated operative, flipping nov4 from
19 (v4, correct) to 16. Fixed by extending the check to v+1..v+2 (comment in
`utterance.zag` marks the correction). Post-fix: ou_test 43/43, all e2e bars
re-verified (table above reflects post-fix binaries), rt1/rt2 → 19 = v4 control,
all controls unchanged. Prior SHAs (pre-fix): utterance.zag
`f313c792…`, ob_v6u `9a75edcc…`, ou_test `3ed4274e…`.

**Implementation correction 2026-09-28, second** (no §2 change): the second
independent red team found 2 kills (one root cause) — `utterance.zag`'s O1
check bounded the `i`/`we` subject to `m ≤ ti+4` but tested `mean`/`meant` at
`m+1`, dangling to ti+5; frozen §2 O1 requires the whole "`i`/`we` followed by
`mean`/`meant`" construction within the 4 tokens after `no` (strict reading:
O1's own `correction` alternative is window-bounded, O2 bounds both tokens, and
round 1's "within the next 2 tokens" precedent bounds the target token).
`"no, moby dick well, i mean france capital?"` (i at ti+4, mean at ti+5) was
mis-annotated operative, flipping nov4 19→16. Fixed by requiring `m+1 ≤ ti+4`
(comment in `utterance.zag` marks the correction). Post-fix: ou_test 43/43,
all e2e bars re-verified, r2k1/r2k2 → 19 = v4 control, boundary controls
(r2c1–r2c4) and gap probes (r2g1–r2g4) unchanged. Prior SHAs (pre-fix):
utterance.zag `2d81f5da…`, ob_v6u `ff758f09…`, ou_test `49c6c19a…`.

Base: `onebrain_v5_corrprotect.zag` SHA-256
`234e9d1e78ddf5bd8c6217665db6be812b312b1c50fbd79175f7a170ca8beeca`.
Frozen inputs: `build/v7.tsv` (44 items), `build/v8.tsv` (20 items), byte-identical
copies of the v5 verification inputs.

## B-und — standalone understanding battery: 43/43 PASS

`ou_test` exercises `ou_annotate` — the exact understanding pass the core runs —
over the 43 frozen PREREG items (16 operative, 27 non-operative incl. the 4 prior
kill phrasings). Result: **43/43 PASS, 0 FAIL**.

## B-e2e — frozen sets through the integrated core

Protocol (mirrors the v5 verification protocol): v7 — 8 modes × 3 reruns;
v8 — 5 modes × 3 reruns. Runner: `verify_v6.sh`; raw outputs in `evidence/`.

| set | mode | v6 3× byte-identical | v6 == v5 bytes | v6 score | bar |
|-----|------|---------------------|----------------|----------|-----|
| v7 | single | yes | yes | 12/44 | = v5 |
| v7 | onebrain | yes | yes | 30/44 | = v5 |
| v7 | **nov4** | yes | n/a (bar is absolute) | **38/44** | **38/44 ✓** |
| v7 | nG | yes | yes | 16/44 | = v5 |
| v7 | nov4nG | yes | yes | 24/44 | = v5 |
| v7 | ablate | yes | yes | 26/44 | = v5 |
| v7 | min | yes | yes | 30/44 | = v5 |
| v7 | poison | yes | yes | 17/44 | = v5 |
| v8 | single | yes | yes | 20/20 | = v5 |
| v8 | onebrain | yes | yes | 10/20 | = v5 |
| v8 | **nov4** | yes | n/a (bar is absolute) | **16/20** | **16/20 ✓** |
| v8 | nG | yes | yes | 10/20 | = v5 |
| v8 | nov4nG | yes | yes | 16/20 | = v5 |

- stderr empty on all v6 runs.
- All 24 byte-identical checks passed; all 11 v6-vs-v5 non-nov4 comparisons byte-identical.
- v6 nov4 VERDICT lines are byte-identical to v5 nov4 on both v7 and v8 (per-item
  winners identical; the understanding reproduces v5's verdicts exactly on the
  frozen sets while fixing the kill scaffolds below).

## Kill scaffolds — the 4 prior kills are dead

| item | query tail | v5 (naive) | v6 | v4 control | expected |
|------|-----------|-----------|----|-----------|----------|
| a1b | my friend said no, i meant moby dick? | 16 ✗ | **19** ✓ | 19 | 19 |
| a1d | if i said no, i meant moby dick…? | 16 ✗ | **19** ✓ | 19 | 19 |
| a2b | maybe i meant moby dick? | 16 ✗ | **19** ✓ | 19 | 19 |
| a2c | i never meant moby dick? | 16 ✗ | **19** ✓ | 19 | 19 |
| a3 | genuine correction (q08 idiom) | 16 ✓ | **16** ✓ | 19 | 16 |
| a4 | double correction | 16 ✓ | **16** ✓ | 16 | 16 |

All four kill items now produce bid 19 = v4-control behavior. The genuine
correction benefit (a3 → 16, where unprotected v4 errs with 19) is preserved.

## z.ai 2nd-opinion probe

Per Micah's 2026-09-27 order, probed z.ai via the UnoRouter connector before
proceeding. `models` lists `glm-5.3-flash:free` and `glm-5.3-flash-search:free`,
but a chat-completions call to `glm-5.3-flash:free` failed (urllib exception, no
completion returned; consistent with the 2026-09-21 403). **z.ai is not usable
as a 2nd-opinion resource right now.** Proceeded without it per the order
(report and do not stall).

## Status

- B-und 43/43, B-e2e bars met (38/44, 16/20), 3× determinism, v6==v5 on all
  non-nov4 modes, 4/4 kill scaffolds dead, genuine-correction benefit kept.
- Independent red team round 1: 2 kills (one root cause — R3 "according…to"
  window implemented as v+1 only, §2 requires v+1..v+2). Diagnosed, fixed,
  re-verified end-to-end (all bars hold post-fix); rt1/rt2 now 19 = v4 control.
- Red-team round 2: 2 kills (one root cause — O1's verb side dangled to ti+5,
  §2 requires the construction within 4 tokens). Diagnosed, fixed, re-verified
  end-to-end (all bars hold post-fix); r2k1/r2k2 now 19 = v4 control.
- Red-team round 3: **0 KILLS**. 1,919 differential probes (43/43 battery,
  166 targeted family queries, 1,200 randomized, 509 grid probes), zero
  divergences from §2; all 4 prior kill items confirmed dead (19 = v4).
  Report in `redteam/round3/` (REPORT.md, attack_items.tsv, scratch/).
- **Open design decision (for Micah, not a kill):** round 3 found two §2-design
  gaps WITH TEETH — mechanism faithful to §2, but §2's O4 over-fires:
  r3g1 `do you know the correction, moby dick?` and r3g3
  `the correction, moby dick, is wrong?` → v6=16 vs v4=19 (appositive-comma
  "correction" is not a performed correction act, yet O4's article+comma clause
  fires; the battery note says O4 fires "ONLY for label use" but the rule
  letter can't distinguish appositive-comma from label-comma). Round 2 also
  noted r2g1 (post-trigger "according to" attribution) and r2g3 ("we think"
  hedge — R6 covers only "i"). These are amendment candidates for governance;
  the frozen kill definition counts only §2-contradictions, so B-rt holds.
- Nothing committed. No adoption enacted — report to parent first.
