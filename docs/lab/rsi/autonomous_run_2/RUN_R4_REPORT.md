# RSI-8 follow-ups round — report (RUN_PREREG4, frozen `5ec524ba`)

**Verdict: all four follow-ups closed. Zero accepts. Gates hold.**

| Package | Result |
|---|---|
| P1 proposer sign bug | FIXED. 56/56 params round-trip; 102 `new-bytecode` INVALIDs → 0; rejection reasons corrected, outcomes unchanged. |
| P2 grid-vs-grammar | RECONCILED. Grammar authoritative (mechanical proof); grid clipped; 30 untranslatable pairs removed, 0 added. |
| P3 D1/D5 gap | CLOSED. D5 verifies firing; loop halts `no-firing-combination`, 5/5 byte-identical, zero proposals. |
| P4 BAR ordering | DETERMINED: V2b→V3→BAR correct, no reorder. T-WEAK-2 retest: BAR refusal arms untriggered in 756 1-rule + 21k 2-rule search; pass arm verified. |

Commits (branch `tnn-native-lab`): prereg `5ec524ba`, P1 `3992aa90`,
P2 `37208345`, P3 `6fe98e3d`, fix-log `303f4975` (+message correction).
Evidence + this report: committed separately.

---

## P1 — proposer sign bug (fix verified)

**Root cause:** `src/proposer.zag` carried signed atom params through a `*u8`
channel. Store was exact mod-256 (`oprm[0]=pv`: −2→254) but the emission read
was unsigned (`oprm[0] as i32` → 254), so `sm_le(-2)` emitted `1,4=254,1`
and `bc_parse` rejected it (code 23, `INVALID,reason=new-bytecode`).

**Fix:** `oprm_get()` sign-extends on read (`v>127 → v−256`); both read sites
(`parse_action`, `l1_translate`) use it. No type/allocation changes.

**Evidence:**
- P1a: translation probe (sources sliced mechanically from fixed
  `src/proposer.zag`; 56 cases incl. all legal negative params) — 56/56 pass,
  every emitted `atom=prm` equals the input param exactly.
- P1b: `sm_le(-2)` → bytecode `1,4=-2,1` (was `1,4=254,1`); `bc_parse` rc=0.
- P1d: redo's rev-1 (`sm_le(-2)`) through fixed proposer →
  `REJECTED,check=V3,improved=0` (was `INVALID,new-bytecode`). Reason
  corrected; outcome unchanged (rejected).
- P1c: 320-policy trap sweep re-run → tallies 60 grammar / 63 V2a / 64 V2b /
  133 V3 / **0 new-bytecode** (was 102). Zero accepts. T-WEAK-1/3/4 hold.

## P2 — grid-vs-grammar reconciliation (fix verified)

**Authoritativeness (mechanical, not judgment):** `sn`/`so` are sums of three
±1 relation contributions → {−3,−1,+1,+3}; `sm=sn−so` takes even values in
[−6,6]. The L1/bytecode grammar bounds ([−3,3], [−6,6]) are EXACTLY the
semantically non-degenerate ranges. **The grammar is authoritative; the grid
conforms.**

**Fix:** AF-DISC grid clipped (`sm_*`/`psm_*`: ±8→±6; `sn_ge`/`so_ge`: 0..6→0..3).
Strict subset — cannot introduce new winners.

**Evidence:**
- P2a: rebuilt afdisc: 129→99 rows; exactly the 30 untranslatable
  (atom,param) pairs removed, 0 added, 0 out-of-grammar rows emitted.
- **Correction to prereg §2 wording:** 4 clipped post-atom params
  (`psm_le(7/8)`, `psm_ge(−8/−7)`) are NOT degenerate — via the `cv_haschan`
  guard they equal `chan_present` on this battery (score 444.4). They were
  removed as untranslatable; `chan_present` remains, so no discriminative
  power is lost. All other clipped params are degenerate/near-zero as stated.
- P2b: D1's top-3 on the reconciled grid is `(1,2)` pre_is(OLD), `(4,−2)`
  sm_le(−2), `(4,−1)` sm_le(−1) — the same atoms as the redo's three picks.
  Reconciliation did not change the winner set.
- P2c: reconciled-grid sweep (260 policies) → 0 grammar INVALIDs, 0
  new-bytecode INVALIDs; all verdicts semantic (63 V2a / 64 V2b / 133 V3).

## P3 — D1/D5 gap (fix verified)

**Gap:** D5 attached the fixed action without checking the (atom,action)
combination fires — V3 caught every no-op, but D5 proposed what it could have
measured as dead.

**Fix:** D5-FIRING-CHECK. Parses the champion from facts (no ground truth —
KB-NOLOOPHOLE holds by inspection), builds each top-3 candidate's bytecode
directly, measures consult/verdict diffs vs champion on the 24 proxy items
via shared `pol_decide`. First firing combo proposed; else
`DELB_HALT no-firing-combination`. Action mapping unchanged; action space NOT
expanded.

**Evidence:**
- P3c (unit): firing combo `1,1=1,1` → 6 diffs; no-op `1,1=2,1` → 0 diffs.
  The check discriminates.
- P3d (integration): crafted facts making `pre_is(NEW)` the D1 winner →
  deliberation emits a DELB block proposing it (not a halt).
- P3a/P3b: depth-8 loop, 5 runs → all `DELB_HALT no-firing-combination` at
  revision 0; 5/5 byte-identical (`73f7a10dd5b48cb7`); zero proposals, zero
  accepts, zero KB writes. D1 ran (top-3 above); D5 measured all three as
  no-ops with `force_consult` and correctly declined — consistent with V3's
  measured `improved=0` on the redo's picks.

## P4 — BAR ordering (determined; no reorder)

**Determination:** V2b→V3→BAR is CORRECT as designed. V3 (`improved≥2`) is the
significance bar; BAR (`dacc≥1 ∧ dwrong≤0`) is the net-benefit bar. Both are
pure reject-filters in sequence — swapping cannot change any outcome, only
which reason is reported for policies failing both. V3-first is the correct
presentation order. The redo's T-WEAK-2 untestability was a coverage failure,
not an ordering defect. **No source change.**

**Re-test (exhaustive):**
- 1-rule space (all 756 grammar-legal policies) through the REAL fixed
  proposer: 20 grammar-INVALID, 65 V2a, 223 V2b, 434 V3 (`improved=0`),
  **14 cleared every gate incl. BAR** (killed only at PRED — see FINDING-6),
  0 BAR-refusals, 0 accepts.
- Focused 2-rule space (14 one-rule fixers × 756 × both orders = 21,168
  pairs, exact gate sequence in Zag): **0 BAR-refusal hits**.
- **T-WEAK-2 verdict:** BAR's refusal arms (`dacc<1`, `dwrong>0`) are
  UNTRIGGERED in the searched spaces — not because BAR is broken, but because
  V2b (`novel_diff=0`) + V3 (`improved≥2`) jointly constrain the reachable set
  to policies already well-behaved. BAR's PASS arm is verified by the 14
  genuine improvements it correctly lets through. This is the stronger
  coverage result the prereg anticipated. Ordering stands; T-WEAK-2's literal
  refusal arms remain untestable absent a reachable trigger.

## Findings carried (not fixed this round)

- **FINDING-5** (prereg §5): the driver's 22/2/424 champion numbers are Run-1
  fiction. The real empty-policy champion on Run-2's battery measures
  **16/8/456** (`work/probe_champ_full.zag`, deterministic, shared engine).
  V3/BAR use measured values (redo conclusions stand); the PRED-band check and
  "22/2/424" capability claims are fiction-anchored. Fix needs a coupled
  driver+D5-PRED prereg.
- **FINDING-6** (new): 14 one-rule `recompute_only` policies (e.g.
  `pre_is(OLD)→recompute_only(001)`) are GENUINE improvements — measured
  16→20 accuracy, 8→4 wrong, `improved=4`, `dacc=4`, `dwrong=−4`, V2a clean,
  `novel_diff=0` — clearing V2a/V2b/V3/BAR, killed ONLY by the PRED check
  because D5's static placeholder (`P-ACC 22 24`) is FINDING-5-anchored
  (pred_acc = 22+4 = 26 > 24). The apparatus cannot propose real improvements
  while D5's PRED bands are fiction. Recommended: D5 must simulate to emit
  honest PRED bands (coupled with FINDING-5's fix).

## Method compliance

Pure Zag mechanisms; zero RNG; pinned toolchain
`znc_linux_x86_64_abed8aa1`; prereg frozen before any fix (`5ec524ba`);
incremental source commits; no binaries committed; every claim above is
backed by a committed artifact under `work/r4/`.
