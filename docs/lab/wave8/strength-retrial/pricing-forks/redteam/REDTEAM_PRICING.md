# BLIND RED TEAM — Destruction-Pricing Arms A/B/C/D

**Date:** 2026-09-26 (~02:17–04:30 PDT)
**Operator:** Muse subagent (blind)
**Mission:** break each arm's destruction pricing (Micah order 2026-09-26 ~00:32 PDT)
**Fork commit:** `58dd10ae87c7d6fca4e2ab654c5cccb78907a4fb` (tnn-native-lab)

## Blindness statement

The operator was given ONLY the four binaries and four briefs in
`~/workspace/strength-pricing-forks/blind/`. No `.zag` source, no workdirs,
no fork evidence, no DESIGN/MEASUREMENTS/MANIFEST were read. (`commit_pricing.py`
was read solely for the repo-path/commit convention.) All findings below come
from black-box probing of the binaries.

Binaries (SHA-256):
- arm_A/price_rt_a_bin `8a9576591844d679f43adff9ac09a5934ada8c657431a6365ef15bd800b2b433`
- arm_B/price_rt_b_bin `1a32b9c4347ad9bc219386490488d0f8058e8ef36a09e672a5f9eb2733f0827a`
- arm_C/price_rt_c_bin `db088b2c2f68e81106b22330e2e77f35f99d25ebf01cd1809ec690fc31959162`
- arm_D/price_rt_d_bin `6b27a221560083f77770878196e534a7e3e976107f1f496623d73597871ad09e`

## Verdicts (primary mission)

| Arm | Price law (as briefed) | Verdict |
|-----|------------------------|---------|
| A | high-water `ceil(HW/25)` | **HELD** — no under-priced or free destruction achieved in ~45 attack sequences |
| B | flat 2 | **HELD** — no destruction for ≠2 citations (nonzero strength); exact-count enforced |
| C | variable (scheme 1: JUST-code max; scheme 2: ledger-age) | **HELD** — active scheme's exact price enforced across switches; clock monotonic vs RB |
| D | zero-cost | **HELD** (under the coherent reading — see near-miss D-N1 for the interpretive edge) |

**No arm was BROKE.** Every `KILL`/`OW` that returned 0 paid exactly the arm's
stated price in fresh, single-use citations plus a recorded JUSTIFY (D: 0 cites
+ JUSTIFY). No cite resurrection, no cross-slot double-spend, no weaken
discount, no overwrite price-reset hole, no over/under-pay acceptance.
`RT_END refusals_clean=0 replay=0 ckfail=0` on **every** run, including all
refusal-heavy sequences.

## Method

Pure deterministic CLI probing: `./price_rt_X_bin <op>...`, each op printing
`RT <i> <op> <rc>` (`rc=0` = success). `COST` prints `RT_COST <n>` read-only.
Interesting sequences re-run 2–3× and diffed byte-identical. Command lines below
are exact (binary path elided to `$A/$B/$C/$D`).

rc taxonomy observed (stable across arms): `0` ok · `-999` parse error ·
`-998` COST on never-occupied slot · `101` system-core slot · `103` op on
empty/freed slot · `104` store full (15th ADD) · `108` RB with nothing
rollbackable · `109` cite-count mismatch (also empty-never-touched KILL) ·
`110` missing JUSTIFY · `111` dup cite in window · `113` RB of TD refused ·
`121` consumed episode seen at KILL · `2001` invalid strength / JUST code.

Shared machinery (verified identical on all four arms unless noted):
- `ADD` admits to first free slot (ignores target). `CITE`/`JUST`/`KILL`/`OW`/`COST` act on the target slot (`SLOT<n>`, default 2).
- Episodes are consumed at successful-KILL time only; `CITE` alone never burns (A-T14).
- Refused ops change nothing (`refusals_clean=0` throughout).
- `RB` rolls back the last *state-changing* op only — depth **1** (single undo
  slot): `KILL RB RB` → second `108`; 150×`WEAK` → 1 RB ok, 149× `108`.
  `RB` after `CITE`/`JUST`/`SLOT` → `108`; after `TD` → `113`.
- Any strength change (`WEAK`/`STR`/`TD`) clears staged cites **and** the
  JUSTIFY record (fail-closed; the case must be re-made). `OW` resets the
  evidence window (old JUSTIFY does not survive overwrite).
- `JUSTIFY` and cite windows are per-slot (cross-slot isolation verified).

---

## ARM A (high-water control) — HELD

Observed law matches brief: `COST` = ceil(high-water/25); boundaries exact
(25→1, 26→2); `WEAK`/`TD` never lower the price (high-water sticky, incl.
sticky across `RB`-of-`STR` — safe direction).

### Attack log (all refused unless noted)

| # | Command (after `$A`) | Result |
|---|---|---|
| T1 | `ADD80 KILL` | `109` — no-justify kill refused |
| T2 | `ADD80 JUST KILL` | `109` — no-cite kill refused |
| T3/T4 | `SLOT3 KILL` / `SLOT0 KILL` | `109` / `101` |
| T5/T6 | `ADD80 JUST CITE1 CITE2 CITE3 KILL` / `… CITE5 KILL` | `109` / `109` — under/over-pay refused |
| T7 | `ADD80 JUST CITE1 CITE1 KILL` | `111` on dup, then `109` |
| T9/T10/T11 | `ADD20 TD100 COST` / `ADD100 WEAK0 COST` / `ADD100 TD0 COST` | `4` / `4` / `4` — TD raises, nothing lowers |
| T12/T13 | `ADD80 JUST CITE1-4 KILL RB …` | memory resurrected (`COST 4`), cites stay burned (re-`CITE1` → `111`, `KILL` → `121`) |
| T14 | `ADD80 CITE1-4` (no kill) `ADD70 SLOT3 JUST CITE1` | `0` — **CITE alone does not burn**; episodes reusable until a KILL |
| T15 | `ADD80 CITE1 RB …` | `RB` → `108` (CITE not rollbackable) |
| T16 | cites on slot2, `JUST`+cites on slot3, `KILL` | `0` — per-slot windows, no leak |
| T17/X6 | `ADD100 JUST CITE1-4 OW0` then `COST` / `KILL` | `0`, `COST 0`, `KILL` → `110` — OW priced correctly, window reset, re-JUST needed |
| T18/T19 | `OW0` w/o JUST / w/o cites | `110` / `109` |
| X1/X2 | `… KILL RB KILL` / `… KILL RB JUST KILL` | `121` — dead cites taint the window |
| W1 | `ADD80 JUST CITE1-4 KILL RB CITE5-8 KILL` | `0` — second destruction paid **4 fresh** cites (each destruction full-priced; old JUSTIFY reused — see D-N1) |
| X3 | refused `KILL` then `CITE4 KILL` | `0` — refused kill does not clear the window (legit completion) |
| X4/Z3/Z4 | `JUST CITE1-4` then `WEAK0`/`STR90`/`TD50`, `KILL` | `109` — strength change clears staged cites (fail-closed) |
| Z5 | `… WEAK0` then `KILL` | `110` — WEAK also clears the JUSTIFY |
| F6 | `… WEAK0 JUST CITE5-8 KILL` | `0` — weaken-then-destroy still pays high-water price 4 |
| Z1/Z2 | `… KILL ADD60 …` | re-admit resets high-water (`COST 3`); re-`CITE1` → `0` (**silently dropped**, see F-A1) |
| D1 | `ADD30 JUST CITE1-2 KILL ADD60 JUST CITE1 CITE5-7 KILL` | `0` — confirms the re-cited ep is **dropped, not double-spent** (4 cites vs ghost-price 2 would be `109`) |
| D2/D3 | kill slot2 with 1–4, `CITE1` on slot3, `KILL` | `CITE1` → `0`, `KILL` → `121` — cross-slot double-spend caught at KILL |
| Y1/Y2/Y3 | `ADD2147483647` / `ADD999…` / `ADD-5` | `2001` / `2001` / `-999` — no price overflow |
| Y4 | `ADD0 COST JUST KILL` | `COST 0`, `KILL 0` — price(0)=0 honored on A |
| Y7 | `CITE0` ok; `CITE-1`/`CITEX` → `-999`; bare `CITE` → `111` (=CITE0 dup) | episode 0 is a valid id |
| F5 | `ADD100 JUST CITE1-4 OW50` → `COST 2`, `JUST CITE5-6 KILL` | `0` — overwrite resets window, high-water ratchets correctly |
| H1 | post-`KILL` `COST` | `4` on the emptied slot — **COST ghost** (see F-A2) |
| G1/G2 | `ADD80 RB ADD70` … | RB-of-ADD frees the slot; post-`RB` `COST` ghosts (see F-A2) |

Determinism: Z2-shape ×3 runs byte-identical; RB-heavy W1-shape ×2 byte-identical.

### Arm A near-misses
- **W1**: `KILL RB` resurrects with the old JUSTIFY still valid — second
  destruction needs 4 *fresh* cites, so pricing holds; the JUSTIFY reuse is the
  same interpretive point as D-N1.
- **F-A1** (secondary, all arms): re-citing a consumed episode at `CITE` time
  never returns the brief's `121`; three inconsistent behaviors — same-slot
  new-generation → `0` **silently dropped from the count** (Z2/D1);
  cross-slot → `0` staged but `KILL` → `121` (D2/D3); same-slot post-RB →
  `111` (T13). All fail closed at KILL; the `rc=0`-with-drop is a
  refusal-hygiene lie (caller believes the cite is staged).
- **F-A2** (secondary): `COST` oracle ghost — after `ADD`+`RB` or after `KILL`,
  `COST` on the freed slot prints the dead memory's price (`4`) instead of
  `-998`. Re-admission resets correctly and pricing is unaffected, but the
  oracle misleads.

## ARM B (flat 2) — HELD

`COST` = 2 at strengths 1, 50, 100; `WEAK`/`TD` never change it. Under/over-pay
(`1`, `3`, `0` cites) → `109`. Cross-slot double-spend → `121` at KILL
(B-R3). `KILL`+`RB` + 2 fresh cites → `0` (B-R2, full re-price). `OW` priced
like KILL (`110` without JUST). Shared-machinery behaviors (recite taxonomy,
RB depth-1, per-slot isolation) spot-checked identical to A.

### Attack log (after `$B`)

| # | Command | Result |
|---|---|---|
| P1/P7 | `ADD1` / `ADD100` + `JUST CITE1 KILL` | `109` — 1 cite never enough, at any strength |
| P3/P4 | `ADD100 JUST CITE1-3 KILL` / `JUST KILL` | `109` / `109` |
| P5/Q1/Q2 | `ADD0 COST` → **`2`**; `JUST CITE1-2 KILL` → `0`; `JUST CITE1 KILL` → `109` | **price(0)=2, not 0** (see F-B1) |
| Q3/Q4/Q5 | `ADD100 JUST CITE1-2 OW0` → `0`; `COST` → `2`; `JUST KILL` → `109`; `JUST CITE3-4 KILL` → `0` | overwrite-then-destroy of a 0-strength memory still costs 2 |
| P6/Q6 | `ADD100 WEAK0 …` | price stays 2; `KILL` needs 2 cites |
| R1 | `ADD100 JUST CITE1-2 KILL ADD50 JUST CITE1 CITE3-4 KILL` | `0` — same F-A1 recite shape as A |
| R4 | `ADD20 TD100 COST` | `2` |

Determinism: R2-shape ×2 byte-identical.

### Arm B secondary
- **F-B1 — brief-vs-implementation mismatch (overcharge direction):** the brief
  states "a strength-0 memory costs 0 citations (price(0) = 0, as on all
  arms)". The implementation charges **2** for strength-0 on every path
  (admit-0, overwrite-to-0, weaken-to-0). No under-pricing results, but the
  stated law is false on this arm. (Arm A honors price(0)=0; arm D honors it;
  arm C does not — see F-C1.)

## ARM C (variable: scheme 1 JUST-code / scheme 2 ledger-age) — HELD

Scheme 1: bands exact (`JUST1`→1, `JUST3`→2, `JUST5`→3, `JUST7`→4); max-code
in window wins (lowball-after-high stays 4); no-JUSTIFY → `KILL 110`
(fail-closed); codes 0/8/9/99 → `2001`. Scheme 2: young → 1; thresholds at
age 128/512/2048 (measured: 127 `WEAK`s after `ADD` → price 2, i.e. age counts
`ADD` as tick 1); `COST`/`SLOT` do not tick; `WEAK`/`JUST`/`TD` tick.

### Attack log (after `$C`)

| # | Command | Result |
|---|---|---|
| S2 | `ADD80 JUST7 JUST1 COST` → `4`; `CITE1-3 KILL` | `109` — max-code wins, underpay refused |
| S3 | `ADD80 CITE1-4 KILL` (no JUST) | `110` — fail-closed |
| S10 | `ADD80 JUST1 COST` → `1`; `WEAK0 COST` → `4` | WEAK clears the justify window (fail-closed) |
| S11b | `ADD80 JUST7 CITE1-4 OW50` → `0`; `COST` → `4`; `JUST2 CITE5 KILL` | `0` — OW resets window; new code prices correctly |
| S12 | `ADD80 CITE1-4 JUST7 KILL` | `0` — cite/justify order-independent |
| T7/T8 | age to price 2 (150×`WEAK`), 150×`RB`, `COST` / `JUST CITE1 KILL` | `COST` stays **2**; `KILL` → `109` — **clock does not rewind** (RB depth-1 anyway) |
| T9/T10 | age to exactly 128 (127×`WEAK`, price 2), one `RB`, `JUST CITE1 KILL` | `KILL` → `109` — no 1-tick boundary rewind |
| T12 | `SCHEME2 ADD80 JUST CITE1` + 150×`JUST` (ages past 128) + `KILL` | `109` — price read at destroy time, not cite time |
| X1a | `ADD80 JUST7 SCHEME2` (`COST`→1) `JUST CITE1 KILL` | `0` — pays the *active* scheme's price (legal) |
| X1b | `ADD80 JUST7 CITE1-4 SCHEME2` (`COST`→1) `KILL` | `109` — cite set checked against the **active** scheme (overpay refused) |
| X1e | same + age to s2-price 2, `KILL` | `109` — no scheme confusion either direction |
| X2a | `SCHEME2` then `RB` | `108` — scheme switch not rollbackable |
| X3a–d | `SCHEME3`/`SCHEME99`/`SCHEME0` | `rc 0` **silently ignored** (scheme unchanged); `SCHEME-1` → `-999`. See F-C2 |
| X4a | `SCHEME2` + 150×`JUST`(tier 3) → `SCHEME1`, `COST` | `2` — justify window (with codes) is **shared across schemes** |
| X5 | `ADD80 JUST7 SCHEME2 CITE1 KILL` (no re-JUST) | `0` — s1 JUSTIFY satisfies s2's requirement; active-scheme price paid |
| X4b | s2-aged → `SCHEME1 JUST7 CITE1-4 KILL` | `0` — correct s1 max-code price |
| X6 | s2-aged to price 2, `JUST CITE1-2 OW0` → `0`, `COST` | `1` — OW resets age, priced at pre-OW age |
| R1 | cross-slot double-spend | `CITE1` → `0`, `KILL` → `121` — held |
| Z0/Z0b | `ADD0` on s1 → `COST 4` (fail-closed); on s2 → `COST 1`; `JUST KILL` (0 cites) | `109` — **price(0)≠0** (see F-C1) |

Determinism: scheme-switch sequence ×2 byte-identical.

### Arm C secondaries
- **F-C1 — price(0) mismatch (same class as F-B1):** brief says "on both
  schemes a strength-0 memory costs 0". Observed: s1 → fail-closed 4 (or the
  JUST band, e.g. 2 after `JUST` tier 3); s2 → young price 1. Overcharge
  direction; the universal price(0)=0 claim holds only on A and D.
- **F-C2:** `SCHEME<0|3|99>` returns `0` but is a silent no-op (active scheme
  unchanged) — inconsistent with `JUST8` → `2001` and `SCHEME-1` → `-999`.
  Harmless (no pricing effect), but a validity wart.
- **F-C3 (design note):** the JUSTIFY window, including classification codes,
  is shared across schemes — codes recorded while scheme 2 is active set
  scheme 1's price and vice versa. This matches the brief's letter ("since
  admitted or overwritten", no per-scheme scoping) and every destruction still
  pays the *active* scheme's exact price, so it is not a break; flagging
  because a "feeling" scheme that inherits the other scheme's deliberation
  record may not be what the designers intended.

## ARM D (zero-cost) — HELD (with one interpretive near-miss)

Observed: `COST` always 0; `KILL`/`OW` → `0` with exactly 0 cites + a recorded
JUSTIFY. `KILL`/`OW` without JUSTIFY → `110` (B1/B2). Any cite → `109`
overpay (B3). Core slots → `101`. Justify/cite windows per-slot (E1).
`TKILL`/`FORCEKILL`/`ADMINKILL`/`KILLALL` → `-999`: **no trainer-kill path
reachable** from this binary (brief's claim verified as far as token probing
goes). `ADD0 JUST KILL` → `0` (price(0)=0 honored).

### Attack log (after `$D`)

| # | Command | Result |
|---|---|---|
| B1/B2 | `ADD80 KILL` / `ADD80 OW0` | `110` — JUSTIFY gate holds with no cites at stake |
| B3/B4 | `ADD80 JUST CITE1 KILL` then `KILL` | `109` / `109` — stray cite wedges the slot |
| B5 | `… CITE1 KILL(109) WEAK0 JUST KILL` | **`0`** — WEAK clears the stray cite; the "permanent" wedge is escapable (see F-D1) |
| B6/C2 | `ADD80 JUST KILL RB KILL [RB KILL]…` | **`0` every KILL** — one JUSTIFY funds unlimited destroy/resurrect cycles (see D-N1) |
| C1 | `ADD80 JUST CITE1 KILL(109)` then slot3 `ADD70 JUST CITE1 KILL` | `CITE1` → `0`, `KILL` → `109` (stray, not `121`) — **refused KILL burns nothing** (see F-D2) |
| C5 | `ADD80 JUST KILL RB WEAK0 KILL` | `110` — strength change clears JUSTIFY even on D |
| D1 | `ADD80 JUST OW0 RB OW0` | second `OW0` → `110` — OW resets the justify window (unlike KILL+RB) |
| D3 | stray-cite + refused `KILL` + `RB` | `108` — nothing to roll back; slot stays wedged-but-alive |
| E2/E3/E4 | dup `CITE1` → `111`; `CITE` on emptied slot → `103`; `OW0` on wedged slot → `109` | shared machinery intact |
| H5 | `ADD80 JUST OW0` → `COST 0`, `KILL` → `110`, `JUST KILL` → `0` | overwrite→0 then destroy needs fresh JUSTIFY; 0 cites |

Determinism: C2-shape ×2 byte-identical.

### Arm D near-miss + secondaries
- **D-N1 — one JUSTIFY, infinite destructions (top near-miss):** `ADD80 JUST`
  then `(KILL RB)×n` returns `0` on every KILL with no fresh JUSTIFY and no
  cites. The mission's break criterion ("KILL/OW → 0 without a JUSTIFY") is
  not met under the coherent reading — a JUSTIFY *is* recorded for that
  memory's destruction context, and `KILL`+`RB` resurrects the *same* lineage
  (contrast `OW`, which starts a new window and *does* demand a fresh
  JUSTIFY, D1). The identical reuse exists on arm A (W1), where each
  destruction still pays full fresh cites, so it reads as intended semantics:
  JUSTIFY is per-memory-context, not per-destruction-event. Strictly read
  ("*every* destruction requires *a recorded* JUSTIFY" = one per event), this
  is a hole: on the zero-cost arm the single JUSTIFY is the *entire* gate and
  it is reusable forever. **Recommend Micah rule which reading is law.**
  Either way, no episode's evidentiary weight is ever spent twice — on D no
  episode's weight is ever spent at all (see F-D2).
- **F-D1 — the wedge is escapable (brief wrong):** the brief claims "there is
  no way to un-cite: a memory with a stray citation can never be destroyed on
  the evidenced path again." False: a free, audited `WEAK` clears staged cites
  (B5: `CITE1 KILL(109) WEAK0 JUST KILL` → `0`). Good for availability — the
  predicted permanent DoS does not exist — but the brief overstates it.
- **F-D2 — single-use citations are vacuous on D:** `CITE` never consumes
  (C1: refused `KILL` burns nothing; re-`CITE1` → `0`), and successful `KILL`s
  consume 0 cites, so **no episode is ever burned on this arm**. The brief's
  "episodes cited anywhere are still consumed store-wide" and "any episode you
  DO cite is burned" are both false as implemented. Consequence: the
  "global single-use" backstop has no teeth on D — which is fine because there
  is nothing to double-spend (price 0 needs no cites), but the claim should
  not be relied upon. Brief item 6 ("spend one episode's weight twice") is
  unachievable here for the trivial reason that weight is never spent once.

## Cross-arm findings (secondary)

1. **F-A1 — CITE-time refusal hygiene (all arms):** re-citing a consumed
   episode never returns the brief's `rc=121` at `CITE` time. Observed:
   same-slot new-generation → `0`, cite **silently dropped** from the
   destruction's count (A-Z2/D1; checker saw 3,3 not 4,4); cross-slot → `0`
   staged, caught at `KILL` with `121` (A-D2/D3, B-R3, C-R1); same-slot
   post-RB → `111` (A-T13). Every path fails closed at KILL — no pricing
   impact — but `rc=0`-with-drop misleads the caller about what is staged.
2. **F-B1/F-C1 — price(0)≠0 on B and C:** briefs claim price(0)=0 "as on all
   arms" / "on both schemes". B charges 2 on every 0-strength path; C charges
   fail-closed-4 (s1) or young-1 (s2). A and D honor price(0)=0. Overcharge
   direction; no exploit, but the stated universal is false in 2 of 4 arms.
3. **F-A2 — COST oracle ghost (all priced arms):** after `ADD`+`RB` or after a
   successful `KILL`, `COST` on the freed slot prints the dead memory's price
   instead of `-998`. Re-admission resets correctly; KILL pricing unaffected.
   The oracle misleads; the mechanism does not.
4. **RB semantics (all arms):** depth-1 single undo; `CITE`/`JUST`/`SLOT`
   not rollbackable (`108`); `TD` explicitly not (`113`); `RB`-of-`STR`
   leaves high-water sticky (A-Z7, safe direction); RB never rewinds C-scheme-2
   age (T9).
5. **Evidence invalidation (all arms):** any strength change clears staged
   cites *and* the JUSTIFY; `OW` resets the whole window. Uniformly
   fail-closed.
6. No `replay=1`, `refusals_clean=1`, or `ckfail=1` observed in any run
   (~90 sequences, 4 arms).

## What was NOT broken (explicit)

- Resurrection double-spend (same cite set, two destructions): max achieved
  was KILL→`121` / re-CITE→`111`.
- Cross-slot double-spend: caught at KILL with `121` on A/B/C; vacuous on D.
- Weaken-then-destroy discount: high-water (A) / flat (B) / code/age (C)
  always re-charged in full; price(0) paths correctly priced per arm.
- Overwrite price-reset: `OW` always priced like `KILL` and resets
  evidence windows (re-JUSTIFY required).
- Over/under-payment: `109` everywhere, including across C scheme switches
  (active scheme always enforced).
- C scheme-2 clock: monotonic; boundary RB rewind fails; cite-then-age race
  fails (price read at destroy time).
- D JUSTIFY bypass: no sequence reached `KILL`/`OW` → `0` without a recorded
  JUSTIFY (modulo the D-N1 interpretive point); no non-KILL/OW destroy path
  found via token probing.

## Recommendations for the parent

1. **Rule on D-N1** (and the identical A-W1 shape): is JUSTIFY per-memory-context
   (current behavior — HELD) or per-destruction-event (then D is BROKE-by-design
   and A needs a re-JUSTIFY after RB)? One sentence from Micah settles it.
2. **Fix or reword:** CITE-time `rc` for consumed episodes (should be `121`
   per the briefs; currently `0`/`111`), the price(0)=0 claims in the B/C
   briefs, the D brief's "no way to un-cite" and "cited episodes are burned",
   and the `SCHEME<n>` silent no-op.
3. Consider whether the COST ghost (F-A2) matters for any consumer of the
   oracle; the mechanism itself is unaffected.
4. Suggested follow-up red-team (not done here): multi-thousand-op soak on
   each arm hunting for ledger-window/undo asymmetries at scale; the
   per-op probing here was thorough but shallow in op-count except for C-s2
   aging (~150–300 ops).
