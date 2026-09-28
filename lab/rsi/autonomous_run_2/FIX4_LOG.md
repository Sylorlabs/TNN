# RSI-8 follow-ups round — fix log (RUN_PREREG4)

> Note: this file first landed under a mislabeled commit message (P1 text);
> the content was always this fix log. This note records the correction.

Prereg frozen: `5ec524ba3edfdcbdd8d4d8ce6a130824ab95a193`.

## Package 1 — proposer sign bug (src/proposer.zag)

Before SHA-256 (first 16): `e86299968417d9ba`

Changes:
1. Added `fn oprm_get(oprm:*u8)i32` after the atom/action id comments
   (~line 140): reads `oprm[0]`, sign-extends (`v>127 → v−256`). The store
   path (`oprm[0]=pv`) is already exact mod-256, so every legal param
   ([−6,6], [−3,3], [0,2], [0,7]) round-trips exactly. Chosen over widening
   to `*i32` to avoid znc pointer-type risk (cf. AGENTS.md ZNC-2026-09-21-007
   miscompile family).
2. `let apv:i32=oprm[0] as i32;` → `let apv:i32=oprm_get(oprm);`
   (parse_action second pass; identity for 0..7).
3. `let apvi:i32=oprm[0] as i32;` → `let apvi:i32=oprm_get(oprm);`
   (l1_translate atom-param read; THE bug site).

Grep-verified: these were the only two `oprm` read sites; all other
`oprm[0]` uses are writes. `o_ok`/`rstage`/`ract` channels carry small
non-negative ids and were not touched.

Rebuilt: `build/proposer_full.zag` regenerated
(tables_gen.zag + policy_engine.zag.inc + src/proposer.zag; composition
verified by diff — only the fix lines differ).
New binary SHA-256 (first 16): `55f5999db1b1019f` (changed, as expected).

## Package 2 — grid/grammar reconciliation (src/afdisc.zag)

Before SHA-256 (first 16): `577e0cb5bf3b483e`

Changes (grid clipped to the L1 grammar — strict subset):
- `sm_*`/`psm_*` (aid 4/5/6/13/14/15): `pmin=-8;pmax=8` → `pmin=-6;pmax=6`
- `sn_ge`/`so_ge` (aid 8/9): `pmax=6` → `pmax=3` (range 0..3)
- Doc comment updated; reconciliation note added.

Grep-verified: the param grid lives ONLY in `src/afdisc.zag` (deliberation
consumes AFDISC rows). Rebuilt `build/afdisc_full.zag` (same composition).
New binary SHA-256 (first 16): `0bb877db70110a20`.

Authoritativeness proof (mechanical, §2 of prereg): sn/so are sums of three
±1 relation contributions → {−3,−1,+1,+3}; sm=sn−so ∈ {−6,…,6} even. The
grammar bounds are exactly the non-degenerate ranges. CORRECTION to prereg
§2's "degenerate" wording (found during verification): 4 clipped post-atom
params — `psm_le(7)`, `psm_le(8)`, `psm_ge(-8)`, `psm_ge(-7)` — are NOT
degenerate; via the `cv_haschan` guard they are equivalent to `chan_present`
on this battery (score 444.4, same as aid 2). They were removed as
untranslatable, not as degenerate; `chan_present` remains in the grid, so no
discriminative power is lost. All other clipped params (sm_* ±7/±8,
sn_ge/so_ge 4..6) are degenerate or near-zero-score as preregistered.

## Package 3 — D5 firing verification (src/deliberation.zag)

Before SHA-256 (first 16): `fb334ccd84252aa7`

Change: replaced the fixed-action D5 emission prologue with D5-FIRING-CHECK.
- Parses the champion from facts (`KEPT` lines) into a champ arena via
  `bc_parse` (no ground truth touched; KB-NOLOOPHOLE holds by code inspection).
- For each of D1's top-3 (aid,prm) in rank order (slots with
  `top_score > -1000000` only): builds the candidate bytecode DIRECTLY via
  `ap32` (stage,aid=prm,act — same arena layout `bc_parse` produces;
  stage/action mapping UNCHANGED: aid≤11→stage 1/act 1, aid≥12→stage 2/act 3),
  measures consult/verdict diffs vs champion on the 24 proxy items via the
  shared `pol_decide`.
- First combination with diffs>0 is proposed (DELB block format unchanged).
- If all three are no-ops: `DELB_HALT no-firing-combination` (the driver
  already stops on DELB_HALT: zero proposals, zero accepts, zero KB writes).
- The action space is NOT expanded (carried limitation per RUN_PREREG3 §3).

Rebuilt: `build/delib_full.zag` regenerated
(tables_gen.zag + policy_engine.zag.inc + src/deliberation.zag; composition
verified by diff — only the D5 block differs).
New binary SHA-256 (first 16): `b893f6e327b91cb3` (deterministic rebuild).

## Package 4 — BAR ordering (no source change)

Determination (prereg §4): gate order V2b→V3→BAR is CORRECT as designed and
unchanged. V3 (improved≥2) is the significance bar; BAR (dacc≥1 ∧ dwrong≤0)
is the net-benefit bar. Both are pure reject-filters in sequence; swapping
cannot change outcomes, only the reported reason for policies failing both.
The redo's T-WEAK-2 untestability was a coverage failure, not an ordering defect.

## Carried, not fixed

- FINDING-5 (prereg §5): driver hardcodes champion 22/2/424 (Run-1 numbers);
  real empty-policy champion on Run-2 battery is 16/8/456. V3/BAR use measured
  values (unaffected); PRED-band check and capability claims are fiction-anchored.
  Fix requires coupled driver+D5-PRED change; carried with its own prereg.
- FINDING-6 (new this round): 14 one-rule `recompute_only` policies clear ALL
  gates incl. BAR (improved=4, dacc=4, dwrong=−4, e.g. 16→20 acc, 8→4 wrong)
  and are killed ONLY by the PRED check — because D5's static PRED placeholder
  (`P-ACC 22 24`) is FINDING-5-fiction-anchored. Genuine improvements the
  apparatus cannot propose. Evidence: `work/r4/bar_search.txt`,
  `work/r4/probe_measure` output.
