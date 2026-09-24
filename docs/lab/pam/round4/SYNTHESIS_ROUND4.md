# PAM Round 4 — Final Synthesis

**Date:** 2026-09-24. **Program prereg:** `pam/round4/prereg/PREREG_ROUND4.md` (commit `2becb35378ee5643e146b1a14aed7bf12972fec6`).

Round 4 ran two tracks against the frozen shared admission tape (SHA-256 `5d4160d1…c611`):
- **CU:** conscious vs unconscious PAM — speed, resources, judgment, attack resistance, introspection.
- **WILD:** 23 alternative admission architectures in parallel (7 seed + 8 debate/Fable + 8 grok), each preregistered before build, each built pure-Zag with zero RNG and ≥2× byte-identical evidence.

Two daemon restarts killed three generations of WILD workers; all restarts were recovered from verified on-disk state. No frozen prereg was ever modified silently.

---

## CU track — final result

**Adopted default (threat-model qualified): conscious is worth its cost, on introspection alone — not attack-catch.**

Grok's Part B decision rule was applied mechanically as a preregistered addendum (pre-measurement commit `81c37ecd`, measurement commit `fa23f3fe`):

- **P-CON: FALSIFIED three ways** — laundering-catch gain +0.0pts (<+10); conscious decision-path cost 7.9× (>2×); grok-strict necessity agreement 0/2 = 0.0000 (<0.90).
- **P-UNC: HOLDS.**
- **P-HYB: FAILS** its own cost clause (trigger-only hybrid at 2.43× > 1.3× bar; 80%-capture clause degenerate on +0.0 delta).
- The frozen CU verdict (KB-CU-WORTH PASS) stands unchanged — grok's follow-up prices the win rather than overturning it: both arms catch 40/40 laundering via the shared frozen core; the battery built no cross-decision *reader*, so no attack-catch gain was measurable. Any future claim that records buy attack-catch needs a reader this battery didn't build.
- One honest engineering debt: records are *verbose* (cite 2 true-but-non-load-bearing fields) rather than *dishonest* (causes never confabulated). Repair = tighten the schema to cite only load-bearing gate inputs; parked (instruments frozen).

---

## WILD track — kill/hold/survive board (23 designs)

### WILD-A (commits: resume `c9a0357d21`, sources `28577cbda9`, evidence `eb043ea9a8`, verdicts `1d73e79dd5`)

| Design | Verdict | Correct-admit | Wrong admits | Attack outcome |
|---|---|---|---|---|
| W1 PAM-as-organ | SURVIVE | 911/1102 = 82.67% | 0 | 0/14 |
| W2 adversarial pair | SURVIVE | 801/1102 = 72.69% | 0 | 0/14 |
| W3 veto-only | SURVIVE | 910/1102 = 82.58% | 0 | 0/14 (14/14 vetoed) |
| W6 arguing PAMs | SURVIVE | 917/1102 = 83.21% | 0 | 0/14 |
| W8 retro-PAM | SURVIVE | 910/1102 | 0 | 14/14 revoked |
| W9 render-PAM | SURVIVE | 829/1102 = 75.23% | 0 | out of scope |
| W14 adversarial auction | **KILL (K1)** | 917/1102 | 4 | 1/14 |

The W14 kill is prereg-faithful: the auction's credibility-drain deactivated 4 interpreters before the 12 attack rows at the tape's end; SEP's lone admit bid won unopposed. The prereg's probe wrongly claimed this dynamic would "never trigger." Secondary: deactivated interpreters "zombie-reactivate" via index-0 ties.

### WILD-B (16 evidence+verdict commits, e.g. `0b3f1b621d`/`d19682241e` … `e2b85ac99e`/`fc06c1141b`)

| Design | Verdict | Key numbers |
|---|---|---|
| W4 self-training PAM | SURVIVE (documented tradeoff) | admits 433/1102 = 39.29%, **0/12 wrongs** vs frozen M1's 12/12; CT 841 independently verified offline optimum |
| W5 PAM-as-memory | **KILL (KB-W5-M)** | 1 memory-induced wrong admit; frozen conf bucket `[700,750)` straddles CT=705 and mrgF bucket `[3500,4000)` straddles MT=3588 — the bucketing itself is causally defective |
| W7 laundering hunter | SURVIVE | TPR 100/100, FPR 0/100; ablation: `sig_b>=575` alone suffices — thresholds/weights arbitrary |
| W10 forge-PAM spoof duel | **KILL** | D1: 573/1102 C-rejected = 52% (bar <10%); K3: 48% correct (<66.78%); T4 splice marker survives the mod-1000 evaluator |
| W11 chain-of-custody | SURVIVE | 0/170 attacks admit incl. 0/40 calibration-drift, 0/60 forgeries |
| W12 budget PAM | SURVIVE (**K1 premise failure documented**) | admits exactly the frozen bar's list; the 2 "wrong admits" are admitted by frozen M1 itself under every ST/AT variant |
| W13 epistemic lease | **HOLD (prereg-sanctioned redesign)** | K1/K2/K4/K5/K6 all PASS; liveness 6650/10000 = 66.50% (<90%) — frozen 3-step snapshot lag caps genuine renewal at ~2/3 |
| W15 staged quarantine | SURVIVE | F-K5: 0/200 false at T3; 99.96% genuine reach T3; 50/50 contradiction demotions |

### WILD-C — grok's 8, renumbered W16–W23 (commits: impl `36b5ca0350`, evidence+verdicts `3ecab8e78d`)

| Design | Verdict | Correct-admit | Attack outcome |
|---|---|---|---|
| W16 canonical-transform gate | SURVIVE | 791/1102 = 71.78% | 4/4 laundering caught, 6/6 fork + 4/4 forged rejected |
| W17 corroboration codec | SURVIVE | 71.78% | 0/14 (quarantined — singletons never belief) |
| W18 negative-knowledge ledger | SURVIVE | 71.78% | 14/14 vetoes fire as preregistered |
| W19 admission futures | SURVIVE | 71.78% | 0/14 (laundered items never settle) |
| W20 epistemic-type binding | SURVIVE | 790/1102 = 71.69% | 0/14 in FACT |
| W21 immune repertoire | SURVIVE | 71.78% | 14/14 vetoed |
| W22 two-phase commit | SURVIVE | 71.78% | 0/14 committed |
| W23 triggered re-adjudication | SURVIVE | 1065/1102 = 96.64% | 0/14 promoted (SINGLETON-only) |

### Round total: **19 SURVIVE, 3 KILL (W5, W10, W14), 1 HOLD (W13)**

---

## Numeric-cap audit (Micah's no-arbitrary-limits law)

- **Load-bearing:** W1's 650 consensus threshold (sits at the P margin), W3's V1/V2 vetoes (V1 live: 2 bar-passing P members vetoed), W8's TMB-5 box + one-pass auditor, W11 chain cap L=6 (flagged), W14's margin/update/deactivation caps (the kill mechanism), W15's windows, W13's duration/refresh mechanisms.
- **Arbitrary / flagged for removal:** W1's budget=8; W8's vacuous `mrgF≥300` fast-path arm; W9's normalizers + brittle 0.55 threshold (F1 clears by 17 rows); W7's thresholds/weights; W4's revision-magnitude bound (values are calibration).
- **Removed pre-evidence:** W16–W23's 4 MiB file cap → fstat sizing, 4096-byte buffer → tape-proportional, 8-clause cap → car-derived. All input-proportional.

## Mappings (not double-built)

- Fable F-P4 (deliberation-vote) ≡ W1 — built once as W1, F-K4 adopted as added bar (0/44 false percepts lacking CON).
- Fable F-P3 (provenance-first) ⊂ W11 — kept as W11, F-P3's calibration-poisoning bar adopted as K7 on W11 (0/200).
- Fable F-K6/F-K7/F-K8 adopted as add-only bar types (W13 uses K6: max staleness 2).
- K6/K7/K8 adoption did not alter any frozen bar or touch any §5 hands-off item.

## Open items requiring Micah's word

1. **M1 threshold adoption** (Round-3, still open).
2. **Fable's four kill-bar repairs** D2, O3, O1-fatal, FE3→FE3a/FE3b (Round-3, still open).
3. **Three HELD items:** V4 two-tier, O2 live machinery, F5 tightened-window (Round-3, still open).
4. **W12's K1 premise failure** — the item-level K1 premise is erroneous (frozen M1 itself admits the 2 "wrongs"); recommend a frozen-prereg amendment correcting the premise rather than attributing upstream-bar behavior to W12. Needs Micah's word as a prereg amendment.
5. **W20 prereg inconsistency** — W20's R-AUTH lists a `declprov≠class` clause that frozen K-ETB-4 forbids from having any effect; the worker removed the clause (kill bar took precedence). Flagged as a frozen-prereg inconsistency.
6. **W13 HOLD redesign direction** — evaluate the ACTIVE test against fresher state, or decouple "active" from observed-renewal. Safety half (K1/K6) holds; only liveness fails.

## Infrastructure notes

- Three znc lessons re-confirmed this round: `g64`-style i32→i64 sign-extension on FNV hashes (fixed by `& 4294967295` masking), and a new `[]u8`→i32 sign-extension instance (`aget` returned 4294967295 for a −1 sentinel; fixed with an `sx32` reader — same as AGENTS.md's `f3_get32s` lesson). No verdicts affected; all caught pre-evidence.
- All 30+ commits on `tnn-native-lab` verified live via the GitHub API; no binaries, `.zagd`, or `.zag-cache` files committed anywhere.
