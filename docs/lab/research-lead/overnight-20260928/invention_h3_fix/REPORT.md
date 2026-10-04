# REPORT.md -- Invention H3 Repair

## Verdict: INVENTION-H3-FIX-COMPLETE

**Attack 1 re-run: SURVIVE. Attack 5 re-run: SURVIVE.**

The three concrete red-team defects are repaired in the unfrozen
`fix_mech.zag`: the search continues after verify-fail and selects among
all verifying chains by a documented deterministic tie-break policy;
`first_lit` is enforced by the search itself; teach order no longer
decides the invented form. No-regression checks pass: Attack 2 still
terminates on contradiction, and the three exact H3 worlds produce the
identical answers, checks, and MAP ids as the frozen mechanism.
Attack 3 (search scaling) is not addressed: it needs redesign, not
repair (documented below). Kill bars were not weakened: attack worlds
and constraints are identical to the red-team driver.

## What was repaired

### FIX-1: continued search after verify-fail (Attack 1)

The old `invent_try` stopped at the first constraint-satisfying sequence
and returned -2 when that single candidate failed `t2_try_verify`, even
when a verifying chain existed later in the enumeration. The new
`invent_dfs` performs full enumeration: every satisfying sequence is
assembled in a scratch workspace copy (the real workspace is never
polluted by trial assemblies) and verified. Verification failure
backtracks into the search instead of ending it. The winner is selected
among the verifying sequences, not the satisfying ones.

Evidence (A1b, chains ending 2000/2001/2002/2003, expected=2002):
- Mirror: nseq=4, verifying=1 of 4.
- Old behavior: INVENT-FAIL, ans=-2.
- New: `INVENT-OK plen=3 map=27 seq=4 vok=1 repeats=0`,
  `A1b invent_try ans=2002`, winner vals=[1000,1102,1202,2002],
  `A1b CONTINUED-SEARCH-OK`.

### FIX-2: first_lit enforced by the search (Attack 5)

The old `invent_dfs` never read C[20]; only the external `invent_check`
harness enforced `first_lit`, so a violating chain could be constructed,
verified, and promoted. The new `invent_dfs` reads C[20]. The chain value
v[0] is fixed to the query subject s by construction, so enforcement is
an entry check: first_lit>=0 and first_lit!=s means the constrained space
is empty and the search returns -1 immediately (documented in the source
header).

Evidence (A5b, first_lit=9999, s=1000):
- Old behavior: ans=2000, check=0, degenerate chain promoted in
  violation of first_lit.
- New: `INVENT-FAIL`, `A5b ... invent_try ans=-2 check=0`, no MAP
  promoted (rt_find_map returns -1), `A5b FIRSTLIT-ENFORCED-OK`.

### FIX-3: deterministic tie-break policy (Attacks 1 and 5)

Among the verifying sequences the mechanism now applies this documented
policy instead of first-hit-wins in teach (node id) order:
1. fewest repeated values (non-redundancy): a chain that revisits a
   value, e.g. a stuttering 2-cycle detour, loses to one that does not.
   This is a form-quality criterion, not a hard filter: a degenerate
   chain remains promotable when it is the only verifying candidate.
2. lexicographically smallest value sequence: independent of teach
   order, so the same fact set taught in any order yields the same
   winner.
3. residual full tie (identical value sequences, e.g. duplicate facts):
   first verifying encounter in DFS order, deterministic.

Evidence (A1a forward teach order vs A1r reverse teach order, 4 parallel
plen-3 chains, all verifying):
- Old behavior: A1a promoted chain 0 (facts [2,3,4]), A1r promoted
  chain 3 (vals=[1000,1103,1203,2000]); teach order decided the form.
- New: both promote vals=[1000,1100,1200,2000] (A1a facts [2,3,4], A1r
  facts [11,12,13]: the lexicographic-min chain, which in reverse order
  has the HIGHEST node ids). `A1a TIEBREAK-POLICY-OK`,
  `A1r TEACH-ORDER-INDEPENDENT-OK`. Teach order no longer decides.

Evidence (A5a, poison stuttering chain taught first, clean chain second;
both satisfy constraints and verify):
- Old behavior: degenerate chain vals=[1000,1005,1006,1005,2000]
  promoted with check=1.
- New: `INVENT-OK plen=4 map=27 seq=2 vok=2 repeats=0`, winner
  vals=[1000,1010,1020,1030,2000], relseq=[3,7,5,7], facts [6,7,8,9],
  check=1. The non-redundant form wins the tie-break; the degenerate
  form is not promoted. `A5a NONREDUNDANT-WINNER-OK`.

## Re-run verdicts

**Attack 1: SURVIVE.** All three sub-defects are gone: (i) the first DFS
hit is no longer taken blindly, every satisfying sequence is verified
and the winner is selected by policy (A1a seq=4 vok=4); (ii) teach order
no longer decides the form (A1a and A1r promote the identical value
chain); (iii) verify-fail no longer ends the search (A1b finds the
verifying chain and returns 2002).

**Attack 5: SURVIVE.** (i) The degenerate stuttering chain is no longer
promoted when a non-degenerate verifying alternative exists
(non-redundancy tie-break); (ii) `first_lit` is search-enforced, so a
violating constraint now yields INVENT-FAIL instead of a violating
promotion.

## No-regression checks

- Attack 2 (contradictory constraints): all four probes still terminate
  cleanly with -2 (A2a unreachable count, A2b first/last clash, A2c
  impossible first_rel, A2d plen=8 hard cap).
  `A2 TERMINATION-REGRESSION-OK`.
- H3 worlds P1/P2/P3 (exact rebuilds): ans=90/150/300, check=1 on all
  three, with the SAME promoted MAP ids as the frozen mechanism
  (32, 27, 35) and nseq=1/vok=1 each. The original
  INVENTION-CONSTRAINT-COMPLETE behavior is preserved bit for bit on
  singleton solution spaces. `H3 NO-REGRESSION-OK`.
- Determinism: 3/3 byte-identical transcripts (SHA-256
  afcfd91479c20f9fdfee95263116afca7b8b66a10e5ceeb9934053af608d085b).
  Stdout numbers cross-checked against the red-team's known-good
  outputs for the same worlds (mirror counts, fact ids, value
  sequences all match).

## Not addressed

- **Attack 3 (search scaling): BOUND stands, by design.** Full
  enumeration with per-candidate scratch verification is strictly more
  work per query than first-hit stop; the exponential
  visits = b*(b^P-1)/(b-1) law and the plen-7 ceiling are unchanged.
  This repair deliberately does not touch scaling: that needs a
  redesigned search (memoization, heuristic ordering, iterative
  deepening), not a patch. Any claim beyond plen 7 still requires the
  redesign the red team recommended.
- **Attack 4 (constraint smuggling): BOUND stands.** The repair does not
  change what the constraints determine: on singleton solution spaces
  (all three H3 worlds: nseq=1) the repaired mechanism behaves
  identically to the frozen one. The constraint-authorship question is
  unaffected by this repair.

## Honest limitations of the repair

1. The tie-break is a quality ORDERING over verifying candidates, not a
   filter: a degenerate chain that alone verifies is still promoted.
   The mechanism now prefers non-degenerate forms; it does not forbid
   degenerate ones.
2. Lexicographic-minimum is deterministic and teach-order independent,
   but it is not derived from the goal: under genuine
   underdetermination it picks a principled default, not a
   goal-justified optimum. The red team's deeper point (a goal that does
   not know the answer cannot write form-selecting constraints) is not
   resolved by a tie-break; it is bounded, not killed.
3. first_lit enforcement is an entry check because v[0] is fixed to s;
   it cannot prune mid-search. That is the honest search-visible
   semantics of the constraint as defined.

## Method

- Toolchain guard Step 0 PASS (zero forbidden executables; pure Zag).
- Base is a byte-identical frozen reference copy (SHA-256 in
  NAMECHECK.md); frozen mechanism never modified (frozen, read-only).
- One binary (pinned znc), 3/3 byte-identical runs. Build log shows
  warnings only, same analyzer class as the H3 and red-team builds.
- Attack worlds and constraints are identical to the red-team driver
  (helpers copied verbatim); only expectations changed where a defect
  was repaired. Kill bars not weakened.

## Files

- `NAMECHECK.md`: toolchain guard, identity, provenance, outputs
- `REPORT.md`: this file
- `fix_base.zag`: frozen base reference copy (unmodified)
- `fix_mech.zag`: repaired mechanism (new, unfrozen)
- `fix_driver.zag`: verification driver (new)
- `fix_full.zag`: assembled source
- `fix_bin`: binary (pinned znc)
- `fix_compile.txt`: build log
- `fix_run1.txt`, `fix_run2.txt`, `fix_run3.txt`: transcripts, 3/3
  byte-identical

Architecture accounting: mechanism diff is confined to `fix_mech.zag`
(invent_dfs rewrite + two small helpers + INVENT-OK line extension);
0 new modes, 0 new bridges, 0 new handlers, 0 new semantic cases.
Pure Zag. Paper untouched. Nothing pushed.
