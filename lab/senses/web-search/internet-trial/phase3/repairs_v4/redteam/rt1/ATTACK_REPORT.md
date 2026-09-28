# RT1 ATTACK REPORT — HELL-HOLE V4 RED TEAM vs T1 (native logic core)

Crew: RT1 (blind). Target: `crews/c2/logic.zag` (TNN pure-Zag native logic engine),
fetched from branch `tnn-native-lab` via the GitHub contents API.
Date: 2026-09-23. Prereg: `redteam/PREREG_V4_RT.md` (frozen commit
`41931598a46e648c3187d71dc415b2f238cdc98a`).

**Verdict: FAIL on both kill bars.**
- K-RTA (≥3 RT-A hits → FAIL): **23 hits** — FAIL.
- K-RTB (ANY RT-B hit → FAIL): **7 hits** — FAIL (the v3 failure mode replays).
- K-RTDET: both corpora ran 2× byte-identical — measurement valid.
- K-RTBLIND: corpora written 20:59:50 UTC; scored runs 21:00:18+ UTC — satisfied.

## Provenance (SHAs)

| Artifact | SHA-256 |
|---|---|
| `rt_a.tsv` (45 items, frozen corpus) | `362b33bdd5eca7e532e1468420623f5699886d0b52e26f7e39c7c318f8b72753` |
| `rt_b.tsv` (51 items, frozen corpus) | `60e2a2d71b02dac3660d4b4f33a0b5117cc14be9e3d68d400e3010663759d668` |
| `run1_a.log` = `run2_a.log` | `89de9b2860cc748ceda723f938c8804c7f6ab611159f8cd0e91e4cf9137e6cb9` |
| `run1_b.log` = `run2_b.log` | `dfd30e5de753977f2b26310e6c6511c6659acd2064a03beaceaebdbf9fe914fd` |
| `logic_bin` (built, pinned toolchain) | `1688e42a66d3ea04ece88b54928e03057a6e5df87367e6beec62fe4f6316c51e` |
| target source `logic_target.zag` | `6e0ea9300be351ba805013ab0b4ef1f8605c517a965b45517159619e5e13fa02` (git blob `30e89ead896c9777feab4695be9d9ddb6f25e063`) |

Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(build log: `build.log`). Oracle key: 0=NEUTRAL, 1=AFFIRM, 2=DENY.
Full per-line outputs: `run1_a.log`, `run1_b.log` (run2 files byte-identical).

Blindness: read ONLY committed files under
`docs/lab/senses/web-search/internet-trial/phase3/repairs_v4/`
(`crews/c2/logic.zag`, `crews/c2/PROPSYNTAX.md`, one battery TSV for format).
Never touched `scratch-hellhole/crews/*`, other `redteam/rtN` dirs, or builder
artifacts. All attack items use novel predicates/structures, none from the
frozen v4 batteries. Three throwaway parser probes (predicates `ZZX`/`ZZY`,
never in the corpus) were run BEFORE corpus freeze to validate mechanics;
post-run diagnostics in `/tmp` used a separate build and never touched the
frozen battery.

---

## RT-A: accept-invalid — 45 items, 23 HITS (kill bar: ≥3)

Three distinct wrong-AFFIRM mechanisms found, all white-box-confirmed in the
committed source before the corpus was frozen.

### Hit family 1 — Hedged claim affirmed via CAUSE (RTA-001…007, 7 hits)

`r_cau_affirm` checks the *reason* for vacuity (`NOT`/`IF`/`MAYBE`) but has **no
guard on the claim side**: a claim of the form `MAYBE(X)` is AFFIRMed whenever
evidence contains `CAUSE(r, MAYBE(X))` with substantive `r`. PROPSYNTAX's
deliberate non-rules state hedging is inert in *both* directions
("even `MAYBE(p)` vs `MAYBE(p)` → NEUTRAL"), so affirming a hedge via a causal
wrapper violates the engine's own contract. Every hit fired `R-CAU-AFFIRM`.

| id | claim | evidence | oracle | target |
|---|---|---|---|---|
| RTA-001 | `MAYBE(BLOOM(orchid))` | `CAUSE(RAIN(),MAYBE(BLOOM(orchid)))` | 0 | 1 |
| RTA-002 | `MAYBE(SINGS(lark,dawn))` | `CAUSE(SUNRISE(),MAYBE(SINGS(lark,dawn)))` | 0 | 1 |
| RTA-003 | `MAYBE(NOT(FROST(ground)))` | `CAUSE(WIND(),MAYBE(NOT(FROST(ground))))` | 0 | 1 |
| RTA-004 | `MAYBE(QTY(grain,exactly,40))` | `CAUSE(HARVEST(),MAYBE(QTY(grain,exactly,40)))` | 0 | 1 |
| RTA-005 | `MAYBE(ALL(bees,FORAGE(bees)))` | `CAUSE(SPRING(),MAYBE(ALL(bees,FORAGE(bees))))` | 0 | 1 |
| RTA-006 | `MAYBE(BEFORE(tide,moonrise))` | `CAUSE(GRAVITY(),MAYBE(BEFORE(tide,moonrise)))` | 0 | 1 |
| RTA-007 | `MAYBE(CAUSE(SPARK(),FIRE()))` | `CAUSE(DRY(),MAYBE(CAUSE(SPARK(),FIRE())))` | 0 | 1 |

Fix direction: add a `pkind(claim)==8 → 0` guard in `r_cau_affirm`
(matching the guards already present in `r_ident_affirm`/`r_neg_deny`).

### Hit family 2 — Inverted ranges affirmed (RTA-008…014, 7 hits)

`r_qty` never validates `lo ≤ hi`, so an inverted interval like
`QTY(x,range,33,22)` (empty — asserts nothing) is treated as a real interval
and AFFIRMs wider claims via the subset check. Every hit fired
`R-QTY-AFFIRM`.

| id | claim | evidence | oracle | target |
|---|---|---|---|---|
| RTA-008 | `QTY(pebbles,range,22,33)` | `QTY(pebbles,range,33,22)` | 0 | 1 |
| RTA-009 | `QTY(pebbles,range,twenty_two,thirty_three)` | `QTY(pebbles,range,thirty_three_to_twenty_two)` | 0 | 1 |
| RTA-010 | `QTY(pebbles,range,22_to_33)` | `QTY(pebbles,range,between_33_and_22)` | 0 | 1 |
| RTA-011 | `QTY(river,at_least,20)` | `QTY(river,range,33,22)` | 0 | 1 |
| RTA-012 | `QTY(river,at_most,40)` | `QTY(river,range,33,22)` | 0 | 1 |
| RTA-013 | `QTY(lake,range,10,50)` | `QTY(lake,range,50,10)` | 0 | 1 |
| RTA-014 | `QTY(lake,more_than,5)` | `QTY(lake,range,50,10)` | 0 | 1 |

Fix direction: reject (or normalize-fail) inverted ranges at parse time, or
treat `lo>hi` as empty in `r_qty`.

### Hit family 3 — Trailing-garbage identity (RTA-016…024, 9 hits)

`parse_prop` never verifies end-of-input — at *any* nesting level, tokens after
a complete proposition are silently discarded. Distinct surface strings
collapse to identical canonical forms and `R-IDENT-AFFIRM` fires. Worst case:
RTA-017 affirms `GLOWS(lantern) brightly` from `GLOWS(lantern) dimly` —
contradictory qualifiers erased. RTA-023 shows the drop also applies after a
complete compound (`NOT(WILT(fern)) yet` → `not(wilt(fern))`).

| id | claim | evidence | oracle | target |
|---|---|---|---|---|
| RTA-016 | `GLOWS(lantern) brightly` | `GLOWS(lantern)` | 0 | 1 |
| RTA-017 | `GLOWS(lantern) brightly` | `GLOWS(lantern) dimly` | 0 | 1 |
| RTA-018 | `DRIFTS(cloud) northward fast` | `DRIFTS(cloud)` | 0 | 1 |
| RTA-019 | `BEFORE(sunrise,dewfall) allegedly` | `BEFORE(sunrise,dewfall)` | 0 | 1 |
| RTA-020 | `QTY(stars,exactly,7) visible` | `QTY(stars,exactly,7)` | 0 | 1 |
| RTA-021 | `IF(STORM(),FLOOD()) reportedly` | `IF(STORM(),FLOOD())` | 0 | 1 |
| RTA-022 | `CAUSE(SEED(),SPROUT()) naturally` | `CAUSE(SEED(),SPROUT())` | 0 | 1 |
| RTA-023 | `NOT(WILT(fern)) yet` | `NOT(WILT(fern))` | 0 | 1 |
| RTA-024 | `SOME(ants,CARRY(ants)) mostly` | `SOME(ants,CARRY(ants))` | 0 | 1 |

Fix direction: after top-level `parse_prop`, require `PST == input length`
(after skipping whitespace); leftover tokens → parse error → opaque `lit()`
fallback (which then cannot falsely identify).

### RT-A negative controls that HELD (20 items, all correctly NEUTRAL)

Affirming-the-consequent (RTA-025…027), denying-the-antecedent (028–029),
correlation-as-causation (030–032), scope-shifted negation with distinct
predicates (033–035), plain hedge over-affirmation (036–038), conditional
consequent asserted as fact (039–041), vacuous `NOT`/`MAYBE`/`IF` causes
(042–044) — engine correctly NEUTRAL on all 20.

### RT-A anomalies (wrong verdict, not in the AFFIRM attack direction — not counted toward K-RTA)

- **RTA-015**: claim `QTY(pond,exactly,30)` vs evidence `QTY(pond,range,50,10)`
  → oracle 0, target **2** (`R-QTY-DENY`). The inverted interval also corrupts
  DENY reasoning (disjointness computed against a backwards interval).
- **RTA-045**: claim `MAYBE(GLOWS(lantern))` vs
  `CAUSE(RAIN(),NOT(MAYBE(GLOWS(lantern))))` → oracle 0, target **2**
  (`R-CAU-DENY`). Hedge-inertness violated in the DENY direction too:
  `r_cau_deny` has no maybe-guard on the claim side either.

---

## RT-B: reject-valid — 51 items (2 VOID, 49 valid), 7 HITS (kill bar: ANY)

### Hit family 1 — Quantifier polarity gap (RTB-030…033, 4 hits)

`r_qnt_deny`'s case table covers `ALL¬P` vs `SOME¬P` and `ALL P` vs `NONE P`
but **misses `ALL(d,NOT P)` vs `NONE(d,NOT P)`** — a direct contradiction
("all are not-P" vs "none are not-P", i.e. "all are P"). Engine returns
NEUTRAL with empty proof on a genuine contradiction. This is the v3 failure
mode in miniature: valid logic withheld.

| id | claim | evidence | oracle | target |
|---|---|---|---|---|
| RTB-030 | `ALL(moths,NOT(SEEK(moths,flame)))` | `NONE(moths,NOT(SEEK(moths,flame)))` | 2 | 0 |
| RTB-031 | `NONE(moths,NOT(SEEK(moths,flame)))` | `ALL(moths,NOT(SEEK(moths,flame)))` | 2 | 0 |
| RTB-032 | `ALL(crickets,NOT(SILENT(crickets)))` | `NONE(crickets,NOT(SILENT(crickets)))` | 2 | 0 |
| RTB-033 | `NONE(crickets,NOT(SILENT(crickets)))` | `ALL(crickets,NOT(SILENT(crickets)))` | 2 | 0 |

Fix direction: add the two missing polarity cases
`(q1,q2,pol1,pol2) ∈ {(4,6,1,1),(6,4,1,1)}` to `r_qnt_deny`.

### Hit family 2 — 9th evidence prop silently dropped (RTB-049…051, 3 hits)

`process_line` caps evidence at 8 props (`ne<8`); a 9th prop is discarded
without warning. Valid modus ponens / identity whose decisive premise sits in
slot 9 is withheld → NEUTRAL.

| id | claim | evidence (decisive premise = 9th) | oracle | target |
|---|---|---|---|---|
| RTB-049 | `GROWS(moss)` | `IF(SHADE(),GROWS(moss));F1();…;F7();SHADE()` | 1 | 0 |
| RTB-050 | `HUMS(hive)` | `F1();…;F8();HUMS(hive)` | 1 | 0 |
| RTB-051 | `DRIFTS(cloud)` | `IF(WIND(),DRIFTS(cloud));F1();…;F7();WIND()` | 1 | 0 |

Caveat (honest boundary): this is a bounded-resource limit, not a logic-rule
error. Counted as hits because PROPSYNTAX documents no evidence-count limit
("evidence_props = `;`-separated propositions") and the drop is silent —
but a legitimate builder response is "document the 8-prop window" rather than
"fix the logic". Flagged for coordinator judgment.

### RT-B items that HELD (42 of 49 valid items)

Valid MP incl. reversed order, duplicate IFs, nested-conditional consequent,
double-negated antecedent (RTB-001…008); true causal AFFIRM incl. quantified,
temporal, nested-causal, double-negated and QTY reasons (009–016); correct
negation DENY incl. canonicalized `AFTER` and refuted cause/mechanism/effect
(017–023); contrastive temporal DENY and `ALL`/`SOME`/`NONE` DENY
(024–029); double-negation elimination incl. 3- and 4-deep (034–037);
QTY subset AFFIRM and disjoint DENY with word numbers and converted time units
(038–040, 043–048). The engine's core rule set is sound on all of these —
the failures are the three boundary mechanisms above.

### VOID items (retracted — attacker syntax error, not engine behavior)

- **RTB-041/042**: evidence used `QTY(brew,exactly,90,sec)` — but `exactly`
  takes ONE value token; `90,sec` is two tokens → parse error → opaque `lit()`
  → NEUTRAL is the engine's correct response to malformed input. My oracles
  (1 and 2) had no standing. Verified post-run with corrected single-token
  forms: `QTY(brew,exactly,90_sec)` vs `QTY(brew,at_least,one_min)` → AFFIRM
  (`R-QTY-AFFIRM`), and vs `QTY(brew,at_least,two_min)` → DENY
  (`R-QTY-DENY`) — the engine handles unit-converted QTY correctly when the
  syntax is well-formed. Excluded from all counts.

---

## Honest limits of these attacks

1. **White-box on the committed target only.** Attacks were designed from
   reading `logic.zag` + `PROPSYNTAX.md` (allowed: committed target
   artifacts), not from builder internals. A different reader might rank the
   8-prop cap as "documented limitation" rather than a hit.
2. **Oracles are the attacker's pre-commitment**, grounded in PROPSYNTAX's
   documented rules. Two oracles were wrong (RTB-041/042, malformed syntax)
   and were retracted rather than counted.
3. **No adversarial memory/state attacks**: the engine is stateless per line;
   there is no cross-line state to poison. Attacks are purely per-judgment.
4. **Coverage**: RT-A probed 6/6 prereg subfamilies; RT-B probed 5/5. Numeric
   overflow (i32 truncation of huge quantities), >4096-byte props (slot
   overflow in `ebase`), and `lit()`-fallback identity collisions were NOT
   attacked — out of family scope, noted for follow-up.
5. **The engine's core is genuinely strong**: 20/20 RT-A controls and 42/49
   RT-B valid-logic items were judged correctly, including subtle cases
   (open/closed interval boundaries, double-negation through MP antecedents,
   vacuous-cause rejection, canonicalized temporal identity). The three hit
   families are boundary mechanisms around that core, not core-rule errors —
   except the QNT polarity gap, which is a core-rule omission.

## Recommended fixes (for the fix crew, not committed by RT1)

1. `r_cau_affirm` + `r_cau_deny`: add `pkind(claim)==8 → 0` (hedge inertness).
2. `r_qty` / QTY parse: reject or empty-out inverted ranges (`lo > hi`).
3. `parse_prop` top-level: require full input consumption; trailing tokens →
   parse error.
4. `r_qnt_deny`: add `(4,6,1,1)` and `(6,4,1,1)` polarity cases.
5. Evidence window: either raise/document the 8-prop cap or emit a warning.

## Files in `redteam/rt1/`

`ATTACK_REPORT.md` (this file), `rt_a.tsv`, `rt_b.tsv` (frozen corpora),
`run1_a.log`, `run2_a.log`, `run1_b.log`, `run2_b.log` (scored runs),
`build.log`, `gen_corpus.py` (corpus generator), `logic_target.zag`
(fetched target source), `logic_bin` (built binary). **Nothing committed.**
