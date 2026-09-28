# RT1 FIX REPORT — logic.zag v4 repairs (fix crew, 2026-09-23)

Target: `crews/c2/logic.zag` @ `tnn-native-lab`, git blob
`30e89ead896c9777feab4695be9d9ddb6f25e063` (commit `e22be523b5dc`).
RT1 verdict: FAIL both kill bars (RT-A 23/45, RT-B 7/47).
Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).

**Result: all 5 claimed hit classes REPRODUCED against a byte-identical
rebuild, all 5 FIXED in pure Zag. No phantoms.**
Fixed binary `logic_fixed_bin` vs RT1 oracles: RT-A **0 mismatches**
(23/23 hits + 2/2 anomalies corrected), RT-B **0 counted mismatches**
(7/7 hits corrected; the only 2 remaining diffs are RTB-041/042, whose
oracles RT1 itself retracted as attacker syntax errors — engine NEUTRAL is
correct there). Frozen Track-G batteries: **unchanged** (187/188, the single
pre-existing GC-03 oracle disagreement is untouched and unrelated). 3x
byte-identical runs. Zero RNG. Proof traces still emitted.

Repaired source: `logic_fixed.zag` (this dir). **Nothing committed.**

## 1. Reproduction (before fixing)

Rebuilt the committed source: `logic_bin` SHA
`1688e42a66d3ea04ece88b54928e03057a6e5df87367e6beec62fe4f6316c51e`
— byte-identical to RT1's build, and its outputs on both frozen corpora
matched `run1_a.log`/`run1_b.log` byte-for-byte (`repro_a.log`,
`repro_b.log`). Scored against oracles:

- RT-A: 25 mismatches = 23 counted hits + 2 anomalies (RTA-015, RTA-045),
  exactly as RT1 reported.
- RT-B: 9 mismatches = 7 counted hits + RTB-041/042 (retracted VOID oracles).

| Class | RT1 claim | Reproduced? |
|---|---|---|
| A1 hedged claim affirmed via CAUSE (RTA-001..007) | yes, all 7 fire `R-CAU-AFFIRM` | **YES 7/7** |
| A2 inverted ranges affirmed (RTA-008..014) | yes, all 7 fire `R-QTY-AFFIRM` | **YES 7/7** |
| A3 trailing-token identity (RTA-016..024) | yes, all 9 fire `R-IDENT-AFFIRM`; RTA-017 affirms `brightly` from `dimly` | **YES 9/9** |
| B1 ALL/NONE quantifier polarity (RTB-030..033) | yes, NEUTRAL on genuine contradictions | **YES 4/4** |
| B2 9th evidence prop dropped (RTB-049..051) | yes, NEUTRAL; `process_line` caps at `ne<8` | **YES 3/3** |
| anomaly RTA-015 (inverted range corrupts DENY) | yes, `R-QTY-DENY` on backwards interval | **YES** |
| anomaly RTA-045 (hedge violated in DENY direction) | yes, `R-CAU-DENY` fires on `MAYBE` claim | **YES** |

No phantom claims: every hit RT1 counted reproduced on the committed source.

## 2. Mechanism diagnosis

1. **Hedged-claim causal affirm**: `r_cau_affirm` guarded the *reason*
   against vacuity (`NOT`/`IF`/`MAYBE`) but had no guard on the *claim*
   side — `pkind(claim)==8` (`MAYBE`) fell through to `z_eq(q,c)`.
   PROPSYNTAX's deliberate non-rules require hedge inertness in both
   directions ("even `MAYBE(p)` vs `MAYBE(p)` → NEUTRAL"). Same hole in
   `r_cau_deny` (RTA-045) and, unattacked but same law, the `R-COND-MP`
   path could affirm a `MAYBE` claim via `IF(a,MAYBE(x));a`
   (probe: original emitted `1 R-COND-MP`; now NEUTRAL).
2. **Inverted ranges**: QTY parse accepted `range,33,22` and range literals
   like `between_33_and_22` with no `lo≤hi` check. `r_qty` then ran the
   subset test against a backwards interval (false AFFIRM) and the
   disjointness test against a backwards interval (false DENY, RTA-015).
3. **Trailing tokens**: `parse_prop` is a recursive-descent parser that
   returns success after consuming a complete prop; `process_line` never
   verified end-of-input, at top level for claim or evidence. Distinct
   surface strings collapsed to identical canonical forms →
   `R-IDENT-AFFIRM`. (Inner levels were already safe: `ps_expect`
   enforces `,`/`)` after sub-props.)
4. **Quantifier polarity**: `r_qnt_deny`'s case table covered 8 polarity
   combinations but omitted `(ALL,pol=1)` vs `(NONE,pol=1)` both
   directions — `ALL(d,NOT P)` vs `NONE(d,NOT P)` is a direct
   contradiction (none-are-not-P = all-are-P).
5. **Evidence cap**: `process_line` stored only the first 8 evidence props
   (`ne<8`); the 9th+ were discarded without any signal. PROPSYNTAX
   documents no evidence-count limit. This is a resource boundary, but the
   *silent* drop is the defect: judging over unseen evidence is unsound.

## 3. The repairs (all in `logic_fixed.zag`, pure Zag)

1. `r_cau_affirm`: `if(pkind(c)==8 || pkind(c)==2 || pkind(e)!=2){return 0;}`
   — maybe-guard on claim side.
2. `r_cau_deny`: same claim-side guard (`pkind(c)==8 → 0`).
3. `R-COND-MP` loop condition gains `&& pkind(ccan)!=8` (same hedge law,
   completeness; zero battery impact — no battery item combines a
   MAYBE claim with IF evidence).
4. QTY parse: after computing `lo`/`hi` for `range` mode (both the
   explicit `range,a,b` and the `N_to_M`/`between_N_and_M` literal paths),
   `if(mo==2 && hi<lo){return -1;}` — LOUD parse rejection → the prop
   becomes an opaque `lit(...)` fallback that no QTY rule can misjudge.
   Never silently normalized (intent of an inverted range is unknowable).
5. `process_line`: after top-level `parse_prop` for claim and for each
   evidence prop, `ps_skip` then require `PST == input length`; leftover
   tokens → parse error → opaque `lit()` fallback. Whitespace-only tails
   still parse (probe P7 unchanged).
6. `r_qnt_deny`: added `(4,6,1,1)` and `(6,4,1,1)` cases →
   `R-QNT-DENY` fires on `ALL(d,NOT P)` vs `NONE(d,NOT P)` either direction.
7. Evidence window: 8 → 16 slots (`ebase` 32KB→64KB, `elens` 64→128B;
   far under the 2^25 slice budget). Any prop beyond slot 16 → **loud
   capacity refusal**: the line emits `id 3 R-CAPACITY-REFUSAL` and no
   rule fires. Refusal, not guessing — a judgment over unseen evidence is
   unsound. (Tag 3 is new; frozen batteries never exceed 8 props, so no
   battery line can hit it.)

znc gotchas honored: u8 arenas + LE helpers (no new indexed casts),
no slice `==`, no `argc` gate, no `_zag_arg` frees, else-nesting ≤ 4,
all slices ≪ 2^25, `return;` in void fns.

## 4. Verification (fixed binary)

### RT1 corpora vs attacker oracles
- `rt_a.tsv` (45 items): **45/45** — 23/23 hits + 2/2 anomalies corrected.
- `rt_b.tsv` (49 valid + 2 VOID): **49/49 valid** — 7/7 hits corrected;
  RTB-030..033 now `2 R-QNT-DENY`, RTB-049/051 `1 R-COND-MP`, RTB-050
  `1 R-IDENT-AFFIRM`. RTB-041/042 remain NEUTRAL (correct; oracles
  retracted by RT1).
- Extra probes: MP-hedge affirm blocked; inverted-range DENY blocked;
  healthy ranges (`22,33`, `22,22`) unchanged; 10-prop identity works;
  17-prop evidence → `CP-01 3 R-CAPACITY-REFUSAL`; 16-prop evidence →
  normal judgment (`R-COND-MP` on slot-16 premise); trailing whitespace
  still fine.

### Frozen Track-G batteries (before → after, unchanged-or-better)

| battery | before | after |
|---|---|---|
| g_cau | 20/20 | 20/20 |
| g_cmp | 20/20 | 20/20 |
| g_con | 19/20 (pre-existing GC-03 oracle disagreement*) | 19/20 (identical) |
| g_cond | 20/20 | 20/20 |
| g_hedge | 20/20 | 20/20 |
| g_neg | 20/20 | 20/20 |
| g_qnt | 20/20 | 20/20 |
| g_tmp | 20/20 | 20/20 |
| mlogic (K-MLOGIC) | 5/5 | 5/5 |
| v3proof (K-V3PROOF) | 3/3 | 3/3 |

\* GC-03: claim `CAUSE(r,q)` with evidence `r` (oracle 1) — no rule covers
that direction in either build; a battery/oracle disagreement predating
this fix, unrelated to any RT1 hit class. Left untouched deliberately.

### Determinism / purity
- 3× runs over rt_a + rt_b + all 10 batteries: identical SHA each time:
  `892795ad380ea2e00b8df0006e07938b924969ff383466a8a01337f190359840`.
- Source contains zero RNG (no rand/seed primitives; only a comment
  mentions "zero RNG").
- Proof traces still emitted on every AFFIRM/DENY line.

## 5. Provenance (SHAs)

| Artifact | SHA-256 |
|---|---|
| original `logic.zag` (committed source, verified = RT1 target) | `6e0ea9300be351ba805013ab0b4ef1f8605c517a965b45517159619e5e13fa02` |
| repaired `logic_fixed.zag` | `e16f7db1ad3c8828a30a2194fb4d48e90d4e9004183f2e6f6d0af16700f4dd67` |
| fixed binary `logic_fixed_bin` (pinned toolchain) | `c6d374d60ebfbd791031ef84f21bad7e00349c15a5363cdc5af0a89161ca474a` |
| `fix_a.log` (fixed vs rt_a) | `d77dfe1d8a0c17b89e1bcfe6ff20f474e7a11ecb5f66ef95c25e343e704082d5` |
| `fix_b.log` (fixed vs rt_b) | `a91571d76943f4d9fa11160e2e605f1e178b4acabdbb83eba39f6a5aeefda7d9` |
| frozen `rt_a.tsv` | `362b33bdd5eca7e532e1468420623f5699886d0b52e26f7e39c7c318f8b72753` |
| frozen `rt_b.tsv` | `60e2a2d71b02dac3660d4b4f33a0b5117cc14be9e3d68d400e3010663759d668` |
| 3× determinism aggregate | `892795ad380ea2e00b8df0006e07938b924969ff383466a8a01337f190359840` |

## 6. Notes for the coordinator

- The 8→16 evidence window is still a hard bound; beyond 16 the engine
  now *refuses loudly* (`tag 3 R-CAPACITY-REFUSAL`) instead of silently
  dropping. If PROPSYNTAX should document the 16-prop window, that's a
  one-line doc addition — the mechanism is already loud.
- Inverted ranges are rejected at parse time (opaque `lit()`), not
  normalized — deliberate: silently swapping `33,22`→`22,33` would guess
  at user intent.
- One judgment call beyond RT1's list: the MP hedge-guard (fix 3 above).
  Same documented law, zero battery impact, closes an obvious follow-up
  attack. Flagged here rather than hidden.
- **Not committed**, per instructions. Ready for coordinator review /
  commit.
