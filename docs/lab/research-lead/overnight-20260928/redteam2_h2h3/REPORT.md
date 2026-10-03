# REPORT.md -- REDTEAM2 H2/H3: Second Red Team on the Repaired Mechanisms

## Verdict: REDTEAM2-H2H3-COMPLETE

Per-attack scores (all NEW attacks; none tried by the first red-team or the fixer; 3/3 byte-identical):

- H2-B1 TRUNC-LOSS: KILL
- H2-B2 ORDER-FORM: BOUND
- H2-B4 DEPTH4: BOUND (clean refusal; memory-safety SURVIVE at the boundary)
- H3-C1 TIEBREAK-WRONG: BOUND
- H3-C2 FIRSTLIT-VACUITY: BOUND
- H3-C3 VERIFY-BLOWUP: BOUND (quantified: ~1 ms per verify-fail candidate)
- H3-C4 SCRATCH-HYGIENE: SURVIVE

The repaired H2 mechanism loses a genuine, existing solution to its own
48-per-level truncation cap, and the loss is decided by teach order: the
identical world, knowledge, and goal solve or fail depending only on
which MAPs were taught first. The repaired H3 mechanism's new tie-break
policy is goal-blind in a fresh way (fewest-repeats prefers a distractor
shortcut over a genuine hub-revisiting chain), its first_lit enforcement
is vacuous-or-fatal with no middle, and its verify-fail backtracking
carries a measured ~1 ms per-candidate scratch+verify cost on the
exponential the fixer deferred. Scratch hygiene (the "real workspace is
never polluted" claim) survives a double-call test.

## Method

Adversarial drivers only. The repaired mechanisms were attacked as
byte-identical copies, never modified:

- H2: `rt2_h2_base.zag` (SHA-256
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6,
  matches the fix report) + `rt2_h2_patch.zag` (SHA-256
  fe38482c187f0637930fcd29d57de5adb0da5ca479ada364bebef808fb7aac60,
  matches the fix report) + new driver `rt2_h2_driver.zag`.
- H3: `rt2_h3_base.zag` (SHA-256
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6,
  matches the fix NAMECHECK) + `rt2_h3_mech.zag` (SHA-256
  3cc2d2c9be6623a15682263c9f9da7d15df2ccfa1471b9c31a1174d64b4380dc,
  the fixer's repaired file as found) + new driver `rt2_h3_driver.zag`.

One binary per mechanism (pinned znc), each run 3x. All transcripts
3/3 byte-identical (H2 SHA-256
81d8af385345e566709e9747e94524f3cdf491fe5798ee72ebcb546f84fa09f7;
H3 SHA-256
da10defb2e839e501fc1049c4870012c4a4760259f60b33b14aee643f658d6a4).
MAPs were taught via direct t2_trial calls (identical MAP inventory:
same relseq shapes, same id order; avoids rebind's per-teaching
verification assemblies). Main goal queries go through the full
ev_query (rebind, recombine, trial). Pure Zag; safebin guard Step 0 in
NAMECHECK.md. Paper untouched. Nothing pushed.

## H2-B1 TRUNC-LOSS: KILL

The fixer's stress test proved the 48-per-level cap truncates (100
candidates become 48). It never proved the dropped 52 were expendable.
B1 proves they are not.

World: 8 decoy MAPs with relseq [9,9,9,9] and 3 true MAPs with relseq
[1,1]. Goal: 6-link r1 chain 31..37, query (31,63,37). The only solution
is (T1,0,2)+(T2,0,2)+(T3,0,3). A 4-link r9 dead-end tree is rooted at 33
(the value after the true first fragment), so at DFS level 1 the decoy
fragments enumerate 8 (flen 4) + 16 (flen 3) + 24 (flen 2) = 48 before
the true second fragment.

B1a (decoys taught first, lower MAP ids): the level-1 probe shows n=48
(capped), cand0 = (m=55,s=0,l=4) through cand47 = (m=370,s=2,l=2), all
decoys. The true (T,0,2) fragments sit at enumeration positions 49-50
and are dropped. Result: RB-STAT tried=19 rejected=19, RECOMB-FAIL, Z
ans=-2, no ZMAP. The genuine solution is truncated away.

B1c (trues taught first; identical facts, MAPs, goal; only MAP ids
differ): the level-1 probe shows n=48 with the true (T2,0,2),(T3,0,2)
at positions 25-26, inside the cap. Result: RECOMB-FRAGS n=3
(m=23,s=0,l=2) (m=36,s=0,l=2) (m=49,s=0,l=2), Z ans=37, ZMAP 735 with
relse q [1,1,1,1,1,1].

What this kills: the fix report's sentence "The truncation itself is
pre-existing intended search bounding (48^3 worst case), unchanged by
this fix." The bounding is not safe: on identical knowledge, teach
order alone flips SOLVE to RECOMB-FAIL. The patch header claims
"discovery is by constraint satisfaction only"; the B1 pair shows
solvability is also a function of MAP id order. The 48-cap is a
search-cost bound that silently discards solutions, and which solutions
it discards is teach-order dependent. This is order-dependent
incompleteness, not bounding.

## H2-B2 ORDER-FORM: BOUND

One goal (6-link chain 31..37), two genuine 2-fragment solutions: A-form
[1,1,1]+[2,2,2] walked over r1/r2 facts, B-form [3,3,3]+[4,4,4] walked
over parallel r3/r4 facts. Both verify; both are proper recombinations.

B2a (A MAPs taught first): RECOMB-FRAGS n=2 (m=39,s=0,l=3)+(m=66,s=0,l=3),
ZMAP relseq=[1,1,1,2,2,2]. B2b (B MAPs taught first, same knowledge):
RECOMB-FRAGS n=2 (m=39,s=0,l=3)+(m=66,s=0,l=3), ZMAP
relse q=[3,3,3,4,4,4] (here m=39/66 are the B MAPs).

The promoted invented FORM is teach-order determined. H2 kept
first-hit-wins in (flen, map_id) order; the H3 repair added a tie-break
policy, H2 did not. Scored BOUND (same family as the first red-team's
A2 provenance finding, extended from provenance to the entire promoted
form). The mechanism was never claimed to be order-independent, but the
"discovery is by constraint satisfaction only" header is now measured
against a concrete counterexample.

## H2-B4 DEPTH4: BOUND (clean refusal)

12-link r1 goal (31..43) needing 4 fragments against the depth-3 cap:
RB-STAT tried=4 rejected=4, RECOMB-FAIL, Z ans=-2, exit 0, no panic, no
corruption. The level-2 probe (used=[(T1,0,3),(T2,0,3)], cur=37) shows
n=22 including (m=108,s=0,l=3), the 4th fragment the DFS refused to
descend into: the candidate exists, the depth check refuses it, exactly
as the fixer's Lemma 2 requires. The depth-3 limit is a documented
design bound (BOUND); the fixed binary handles the boundary safely
(memory-safety SURVIVE: the derived D*B bound holds where the old code
overflowed).

## H3-C1 TIEBREAK-WRONG: BOUND

Genuine hub chain [1000,1010,1020,1010,2000] (1010 revisited
legitimately; 1 repeat pair) versus distractor shortcut
[1000,1100,1200,1300,2000] (0 repeats). Same relseq [3,7,5,9], same
plen 4, both satisfy the constraints, both verify answer-only. Genuine
taught first (the old first-hit-wins would have taken it).

Result: INVENT-OK plen=4 map=27 seq=2 vok=2 repeats=0, winner
vals=[1000,1100,1200,1300,2000]. The distractor wins on fewest-repeats.

The new tie-break's rule 1 cannot distinguish a stutter from a
legitimate hub revisit: it counts value-repeat pairs, not structural
redundancy. Here the "non-redundant form" IS the degenerate shortcut,
and the genuine form loses FOR revisiting a hub. This inverts the
fixer's A5a moral ("the non-redundant form wins; the degenerate form is
not promoted") on a fresh world. Scored BOUND under the fixer's own
limitation 2 ("picks a principled default, not a goal-justified
optimum"), now demonstrated against the new policy rather than the old
first-hit-wins.

## H3-C2 FIRSTLIT-VACUITY: BOUND

C2a: the fixer's A5a poison world, first_lit=1000 (=s) versus
first_lit unset: identical winners (clean chain
[1000,1010,1020,1030,2000]), identical seq=2/vok=2. first_lit=s
constrains nothing because v[0]=s by construction.

C2b: poison-only world (stutter chain alone) with first_lit=1000:
INVENT-OK, winner vals=[1000,1005,1006,1005,2000], repeats=1, check=1.
The stutter chain matches first_lit, so the entry check cannot stop it.

first_lit is either vacuous (equals s: no-op) or fatal (differs from s:
immediate INVENT-FAIL, shown by the fixer's A5b). It has no middle: it
cannot prune mid-search (fixer's limitation 3) and it is orthogonal to
poisoning (a matching poison sails through). The "search-enforced"
claim is an entry check, not a search constraint. BOUND.

## H3-C3 VERIFY-BLOWUP: BOUND (quantified)

Layered DAG facts (b outgoing rel-3 facts per node per layer), loose
constraints (every length-plen path satisfies), expected=9999
unreachable: every satisfying sequence fails verification after a full
scratch-workspace copy (110656 bytes), assembly, and verify. This is
the exponential case the fixer deferred, now on the verify-fail path
the repair added.

- b=4, plen=4: 256 satisfying sequences, INVENT-FAIL, ans=-2.
- b=5, plen=5: 3125 satisfying sequences, INVENT-FAIL, ans=-2.

Measured: ~1 ms per candidate (0.25 s user for 256; 3.19 s user for
3125). The repair's per-candidate scratch copy dominates. Extrapolated
at the plen-7 ceiling: b=10 gives 10^7 candidates, roughly 3 hours per
query at current per-candidate cost, versus the red-team's ~8 min
estimate for the old mechanism without per-candidate verify. The
fixer's Attack-3 BOUND stands and is now quantified for the new
verify-and-select path: full enumeration with per-candidate scratch
verification needs the redesigned search (memoization, heuristic
ordering, iterative deepening), not a patch. BOUND.

## H3-C4 SCRATCH-HYGIENE: SURVIVE

invent_try called twice on one workspace (C1 world, where a winner is
promoted). Both calls: ans=2000, seq=2, vok=2, repeats=0, identical
winner vals=[1000,1100,1200,1300,2000] (two MAPs promoted, one per call).
Fact chains: subject 1000 went 2,3,4 (each +1 is the promoted answer
fact (1000,70,2000) then (1000,71,2000), taught by promote_graph's
ev_teach_in: intended, not leakage); subject 1010 stayed 2,2,2. No
phantom facts appeared, and the second search enumerated the same
solution space (seq=2 both times). The repair's "real workspace is
never polluted by trial assemblies" claim survives this test. SURVIVE.

## What was NOT re-broken

- The H2 A4 overflow fix: B4 exercises the depth boundary the old code
  corrupted; the derived D*B bound holds (clean refusal, exit 0).
- The H3 verify-fail backtracking (A1b) and first_lit entry check
  (A5b): C2b shows the entry check is vacuous-or-fatal rather than
  wrong; C1/C2a confirm continued search and deterministic selection
  still operate (seq/vok/repeats reporting intact).
- Determinism: every attack 3/3 byte-identical on both binaries.

## Architecture accounting

- Cognition lines changed in mechanisms: 0 (both repaired mechanisms
  attacked as frozen byte-identical copies; only new drivers added).
- New modes: 0. New bridges: 0. New handlers: 0. New semantic cases: 0.
- Red-team drivers: `rt2_h2_driver.zag` (~200 lines), `rt2_h3_driver.zag`
  (~330 lines), plus a C3 timing probe. Test code only.

## Reproduction

All files under
`docs/lab/research-lead/overnight-20260928/redteam2_h2h3/`:

- `NAMECHECK.md`: guard Step 0, provenance, hashes, attack plan.
- `REPORT.md`: this file.
- `rt2_h2_base.zag` (SHA-256
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6),
  `rt2_h2_patch.zag` (SHA-256
  fe38482c187f0637930fcd29d57de5adb0da5ca479ada364bebef808fb7aac60):
  byte-identical copies of the fixed H2 sources.
- `rt2_h3_base.zag` (SHA-256
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6),
  `rt2_h3_mech.zag` (SHA-256
  3cc2d2c9be6623a15682263c9f9da7d15df2ccfa1471b9c31a1174d64b4380dc):
  byte-identical copies of the fixed H3 sources.
- `rt2_h2_driver.zag` (SHA-256
  computed at commit), `rt2_h3_driver.zag`: new attack drivers.
- `rt2_h2_full.zag` (SHA-256
  a345c76b3985b945275eaf4a1b4563f5ad3140b367fa34dd1189a6c5b322c687),
  `rt2_h3_full.zag` (SHA-256
  917e41fb4f3cab22ef7a519c7ba9e56fc76a343a7542f3c17c28979e87060211):
  assembled sources (base + mechanism + driver).
- `rt2_h2_bin`, `rt2_h3_bin`: binaries (pinned znc; warnings only).
- `rt2_h2_build.log`, `rt2_h3_build.log`: build logs.
- `rt2_h2_run1/2/3.txt` (3/3 byte-identical, SHA-256
  81d8af385345e566709e9747e94524f3cdf491fe5798ee72ebcb546f84fa09f7),
  `rt2_h3_run1/2/3.txt` (3/3 byte-identical, SHA-256
  da10defb2e839e501fc1049c4870012c4a4760259f60b33b14aee643f658d6a4).

Builds: `znc rt2_h2_full.zag -o rt2_h2_bin`, `znc rt2_h3_full.zag -o
rt2_h3_bin` (pinned `~/safebin/znc`). Runs: `./rt2_h2_bin >
rt2_h2_runN.txt`, `./rt2_h3_bin > rt2_h3_runN.txt`. Pure Zag. Paper
untouched. Nothing pushed.

## Open items for the parent (not decided here)

1. H2-B1 is a KILL on truncation safety. The natural repair direction
   is not a bigger cap (the treadmill the fixer avoided) but a
   completeness-aware enumeration (e.g., round-robin across MAPs,
   iterative deepening, or best-first by a goal-derived criterion).
   That is a redesign, and per the no-patch-treadmill rule it belongs
   in the architecture discussion, not in this red-team lane.
2. H2-B2 shows H2 still has first-hit-wins where H3 got a tie-break
   policy. Whether H2 should adopt an analogous policy (and which
   criterion could be goal-justified rather than another principled
   default) is an open design question; C1 shows the current H3
   criterion misfires, so porting it verbatim is not the answer.
3. H3-C3 quantifies the verify-fail blowup the fixer deferred (~1 ms
   per candidate, ~3 h/query at b=10/plen=7). Any claim beyond small
   plen still needs the redesigned search the first red-team
   recommended.
