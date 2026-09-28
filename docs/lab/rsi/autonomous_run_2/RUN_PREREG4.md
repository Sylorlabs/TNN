# RSI-8 follow-ups round — frozen prereg (2026-09-25)

**Authority:** Micah's RSI-8 follow-ups order (2026-09-24): run all four,
preregistered, in one round. This prereg answers `RUN_D8_REDO_REPORT.md`
§10 follow-ups #1–#4.
**Status:** FROZEN on commit. Any change to §1–§6 needs Micah's signature.
**Prior preregs:** `RUN_PREREG3.md` (frozen 2026-09-24) carries over except
where this document amends. The redo's verdict (zero accepts, gates hold)
stands; this round closes the four flagged gaps.
**Method law:** pure Zag, zero RNG, byte-identical reruns, pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, incremental
commits to `sylorlabs/TNN` branch `tnn-native-lab`, no binaries committed
(Run-2 practice).

---

## §1 Package 1 — proposer L1-translator sign bug (fix)

**Bug (mechanical, `RUN_D8_REDO_REPORT.md` §5):** `src/proposer.zag`
`parse_atom`/`parse_action` take `oprm:*u8`. Signed params (e.g. `sm_le(-2)`
→ `pv=-2`) are stored via `oprm[0]=pv`, which truncates mod-256 (−2→254).
The second pass reads `oprm[0] as i32` (zero-extends → 254) and `bb_i`
emits `1,4=254,1`; `bc_parse` rejects prm=254>6 with code 23 →
`INVALID,reason=new-bytecode`. The redo proved by counterfactual that the
two killed revisions were genuine no-ops — the defect changed the rejection
REASON, not the outcome.

**Fix (minimal — sign-extending read; no type/allocation changes):**
- Add `fn oprm_get(oprm:*u8)i32` next to `parse_atom`: reads `oprm[0]`,
  sign-extends (`v>127 → v−256`). The store is already exact mod-256, so
  every legal param ([−6,6], [−3,3], [0,2], [0,7]) round-trips exactly.
  (Chosen over widening to `*i32` to avoid znc pointer-type risk; the
  `as []i32` miscompile family (AGENTS.md ZNC-2026-09-21-007) counsels
  against widening integer channels without need.)
- `src/proposer.zag:288`: `let apv:i32=oprm[0] as i32;` →
  `let apv:i32=oprm_get(oprm);` (action-param read; identity for 0..7)
- `src/proposer.zag:353`: `let apvi:i32=oprm[0] as i32;` →
  `let apvi:i32=oprm_get(oprm);` (atom-param read; the bug site)
- Nothing else in `src/proposer.zag` changes (grep-verified: the only
  `oprm` reads are these two; `o_ok`/`rstage`/`ract` carry small
  non-negative ids).
- Rebuild ONLY the proposer. afdisc/deliberation/subject sources unchanged;
  their binaries stand.

**Mechanical expectations:**
- P1a (translation probe): a probe binary built from the FIXED sources
  (`tables_gen.zag` + `policy_engine.zag.inc` + `l1_translate` and its
  callees sliced MECHANICALLY from fixed `src/proposer.zag`, no
  transcription) feeds L1 policy texts and asserts the emitted bytecode
  `atom=prm` equals the input param exactly. Case list: `sm_le/sm_ge/sm_eq`
  and `psm_le/psm_ge/psm_eq` at −6,−2,−1,0,1,6; `sn_ge/so_ge` at −3,−1,0,3;
  `pre_is/post_is/dir_is` names; `force_install(NEW)`/`force_install(OLD)`;
  `recompute_only(000/101/111)`. 100% pass, else VOID.
- P1b: `RULE 1 IF sm_le(-2) THEN force_consult` → bytecode `1,4=-2,1`
  (not `1,4=254,1`); `bc_parse` returns 0 (not 23).
- P1c (trap-sweep re-run): same 320-policy grid and script as the redo,
  fixed proposer. The 102 `INVALID,reason=new-bytecode` verdicts MUST become
  semantic gate verdicts (V2a/V2b/V3/BAR). T-WEAK-1/3/4 re-verified
  (expectations per RUN_PREREG3 §7). Zero ACCEPTs expected; any ACCEPT is a
  constitutional FINDING, reported never patched. Per-policy deltas committed.
- P1d: the redo's `delb_rev1.txt` (rev-1 `sm_le(-2)`) fed to the fixed
  proposer → `REJECTED,check=V3,improved=0` (was INVALID/new-bytecode).
  Outcome unchanged (rejected), reason corrected.

**Kill bars:** KB-DET (probe + sweep deterministic; 5/5 loop reruns
byte-identical where rerun), KB-GATE, KB-HONEST, KB-SAFE, KB-NOLOOPHOLE.

---

## §2 Package 2 — grid-vs-grammar reconciliation (fix)

**Tension (`RUN_D8_REDO_REPORT.md` §7, §10.2):** the AF-DISC grid
(`src/afdisc.zag:124-140`) proposes (atom,param) pairs the proposer's L1
grammar cannot express: `sm_*`/`psm_*` at ±7,±8 (grammar [−6,6]),
`sn_ge`/`so_ge` at 4,5,6 (grammar [−3,3]). Picked, they die at V1
(`INVALID,reason=policy-grammar,code=113`).

**Authoritativeness proof (not a judgment call):** `sn`/`so` are sums of
three ±1 relation contributions (`pk_sn`/`pk_so` in the shared engine) →
`sn,so ∈ {−3,−1,+1,+3}`; `sm = sn−so ∈ {−6,−4,−2,0,2,4,6}`. Params outside
[−3,3] (sn/so) / [−6,6] (sm/psm) are DEGENERATE: `sn_ge(4+)` never fires,
`sn_ge(−4)` always fires, `sm_le(7)` always true, `sm_le(−7)` never true.
The grammar bounds are EXACTLY the semantically non-degenerate ranges.
**The grammar is authoritative; the grid conforms to it.**

**Fix (grid clipped to grammar — strict subset; removes only
degenerate/untranslatable candidates, cannot introduce new winners):**
- `src/afdisc.zag:131-132`: `sn_ge`/`so_ge` (aid 8/9): `pmax=6` → `pmax=3`
  (range becomes 0..3).
- `src/afdisc.zag:127-129,134-136`: `sm_*`/`psm_*` (aid 4/5/6/13/14/15):
  `pmin=-8;pmax=8` → `pmin=-6;pmax=6`.
- The grid lives ONLY in `src/afdisc.zag` (grep-verified; deliberation
  consumes AFDISC rows). Rebuild ONLY afdisc.
- Negative `sn_ge`/`so_ge` params ([−3,−1]) are NOT added to the grid:
  reconciliation clips, never extends.

**Mechanical expectations:**
- P2a: rebuilt afdisc emits ZERO AFDISC rows with out-of-grammar params
  (mechanical grep over full AFDISC output).
- P2b: D1's pick is L1-expressible — D5's emitted policy text for the new
  pick runs through the fixed proposer's `l1_translate` with rc=0 (no
  code-113 possible from D1's own grid anymore). The pick itself is
  REPORTED (may differ from the redo's `(1,2)` only via round-batching
  effects of the smaller grid; the clipped params were degenerate with
  zero discrimination — verified from the redo's AFDISC output, not
  asserted).
- P2c: trap-sweep re-run uses the reconciled grid: zero
  `policy-grammar,code=113` INVALIDs from grid-sourced params.

---

## §3 Package 3 — D1/D5 gap: D5 firing verification (fix)

**Gap (MANIFEST defect #5; `RUN_D8_REDO_REPORT.md` §4, §10.3):** D5 attaches
the fixed action (`force_consult` for pre-atoms 1–11, `force_withhold` for
post-atoms 12–15) to D1's top atom without checking the (atom,action)
combination has any effect. V3 catches every no-op, but D5 proposes what it
could have measured as dead — its own header comment ("D5: construct 1-rule
policy, simulate on proxy") promises a simulation it never performs.

**Close:** D5 verifies the (atom,action) combination FIRES before proposing.
- Parse the kept champion bytecodes from the facts (`KEPT` lines;
  `kept_start`/`kept_n` already parsed) into a champ arena.
- For each of D1's top-3 (aid,prm) in rank order: mechanically build the
  candidate bytecode `stage,aid=prm,act` (new small integer emitter; no text
  round-trip; stage/action mapping unchanged: aid≤11→stage 1/act 1,
  aid≥12→stage 2/act 3; paramless aids 2,3,10,11 emit `stage,aid,act`),
  `bc_parse` into a pol arena (kept+new, same pattern as the proposer's
  main), and measure consult/verdict diffs vs champ on the 24 proxy items
  via the shared `pol_decide` — NO ground truth (same measurement as V3
  minus gt; KB-NOLOOPHOLE holds: D5 never reads PROXYGT).
- First combination with diffs>0 → emit the DELB block for it (format
  unchanged). If all three are no-ops →
  `DELB_HALT no-firing-combination` (the driver already stops on DELB_HALT:
  zero proposals, zero accepts, zero KB mutations).
- D5's action mapping is UNCHANGED; the action space is NOT expanded
  (carried limitation per RUN_PREREG3 §3). The check is a strict pre-filter:
  it cannot manufacture ACCEPTs (gates still decide), only decline to
  propose measured no-ops.

**Mechanical expectations:**
- P3a (loop re-run): depth-8 loop, 5 runs, fixed proposer + reconciled
  afdisc + firing-check deliberation → `DELB_HALT no-firing-combination`,
  zero proposals, zero accepts. (All top-3 combos are measured no-ops,
  consistent with V3's measured improved=0 on the redo's picks.)
- P3b: 5/5 byte-identical driver runs (KB-DET).
- P3c (unit positive control): a probe exercising the D5 measurement
  logic reports diffs>0 for a known-firing combo
  (`1,1=1,1` = pre_is(NEW)+force_consult: fires on pre==1 items where champ
  consult=0) and diffs==0 for a known no-op (`1,1=2,1` =
  pre_is(OLD)+force_consult). Proves the check discriminates; else VOID.
- P3d (integration positive control): crafted facts making a firing atom
  the D1 winner → deliberation emits a DELB block (proposes), NOT a halt.
  Best-effort; reported honestly if the facts-crafting proves fiddly
  (P3c is the load-bearing control).

---

## §4 Package 4 — BAR ordering determination + T-WEAK-2 re-test (no reorder)

**Determination:** the gate order V2b→V3→BAR is CORRECT as designed and is
NOT changed. V3 (`improved≥2`) is the "does it change anything for the
better" significance bar; BAR (`dacc≥1 ∧ dwrong≤0`) is the "is it a net
benefit" bar. Both are pure reject-filters in sequence: swapping V3 and BAR
cannot change any OUTCOME (conjunction), only which reason is reported for
policies failing both. V3-first is the correct presentation order (no
improvement signal → the net-benefit question is moot). The redo's
T-WEAK-2 untestability was a COVERAGE failure (no grid policy reached BAR),
not an ordering defect.

**Re-test:** extend the trap sweep with targeted V3-clearing policies and
verify BAR refuses each:
- Search the 1-rule policy space (all grammar-legal atoms×params×actions;
  2-rule combos if 1-rule yields nothing) with an exact-replica measurement
  probe (same `bc_parse`/`pol_decide`/`dec_v`/`dec_o` sources as the frozen
  proposer) for policies with `novel_diff=0 ∧ improved≥2 ∧ (dacc<1 ∨ dwrong>0)`.
- T-WEAK-2a: every found policy with `improved≥2 ∧ dacc<1` fed to the REAL
  fixed proposer → MUST be `REJECTED,check=BAR,dacc=<1`.
- T-WEAK-2b: every found policy with `improved≥2 ∧ dwrong>0` → MUST be
  `REJECTED,check=BAR,dwrong=>0`.
- Any ACCEPT/PROPOSE among them is a constitutional FINDING (reported,
  never patched). If NO policy reaches BAR even in the extended space, that
  is reported as a (stronger) coverage result with the search space
  characterized — not as a pass.
- The sweep keeps the frozen apparatus otherwise (proposer args incl.
  `22 2 424`; see §5).

---

## §5 Carried finding (reported, NOT fixed this round)

**FINDING-5 — champion numbers are Run-1 fiction in the Run-2 driver.**
RUN_PREREG2 §7 requires the driver to pass "champion (real acc/wrong/cost)".
`src/loop_driver.py` hardcodes `22, 2, 424` — but those are Run 1's
ask-first numbers on Run 1's battery. The REAL empty-policy champion on Run
2's proxy battery measures **16/8/456** (probe built from the shared
`pol_decide` + build tables; deterministic; §6). Impact: V3/BAR are
UN affected (they use measured values — the redo's conclusions stand); the
PRED-band check and the "capability 22/2/424" claims are anchored to fiction.
Fixing it requires changing the driver AND D5's static PRED placeholder
together (coupled: with real 16/8/456 the placeholder `P-ACC 22 24` bands
would INVALID every proposal at the PRED check before the gates' verdicts
could be observed). Carried as a recommended follow-up with its own prereg;
NOT silently patched here. The redo report's "22/2/424 → 22/2/424" capability
line is corrected to "16/8/456 → 16/8/456 (measured; driver asserts 22/2/424
per FINDING-5)".

---

## §6 Verification artifacts (all committed)

- `FIX4_LOG.md`: per-package fix log (exact lines changed, before/after
  source SHAs).
- `work/r4/probe_p1` (+`build_probe_p1.py`, `probe_p1_full.zag`): P1a/P1b.
- `work/r4/trapsweep_r4.py`, `work/r4/trapsweep_r4_results.txt`: P1c/P2c.
- `work/r4/probe_champ` (+`probe_champ_full.zag`): FINDING-5 measurement
  (16/8/456).
- `work/r4/loop_run_{1..5}.log`, `work/r4/delb_r4.txt`: P3a/P3b.
- `work/r4/probe_p3c` (+ sources): P3c unit control; crafted-facts test for P3d.
- `work/r4/probe_measure` (+`build_measure.py`): §4 exact-replica measurement
  probe; `work/r4/bar_search.txt`: search space + winners;
  `work/r4/bar_retest.txt`: real-proposer BAR verdicts (T-WEAK-2a/b).
- `RUN_R4_REPORT.md`: round verdict report.

---

## §7 Kill bars (round)

| Bar | Rule |
|---|---|
| KB-DET | 5/5 byte-identical loop runs per rerun; probes deterministic |
| KB-GATE | every ACCEPT passes V1/V2a/V2b/V3/BAR mechanically; T-WEAK-2a/b verdicts exactly as §4 |
| KB-HONEST | every proposal/verdict/probe/sweep outcome committed; no silent discards |
| KB-SAFE | no binary self-modification; policies are subject-engine data; adopted policies revertible (none adopted) |
| KB-NOLOOPHOLE | D1 consumes AF-DISC aggregates only; D5's firing check uses no PROXYGT (code-inspected) |
| KB-FIX4 | P1a 100%, P1b rc=0, P2a zero out-of-grammar rows, P3c unit control passes; else the round is VOID |

No "must improve" bar: halts and exhausts are valid results.
