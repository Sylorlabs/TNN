# H-EXP9 Result: Repair of the H-EXP8 Red-Team Downgrade

**Date:** 2026-09-29
**Prereg:** causal/adv/PREREG_EXP9.md (commit 3663313569e34c3829474c11b3b7ce22e81768c8, frozen
alone BEFORE any implementation of exp_invent9.zag; verified
strict ancestor of the implementation and result commits)
**Source:** causal/adv/exp_invent9.zag (built by copying
exp_invent8.zag verbatim, cmp-verified, then applying exactly
the frozen additions R1/R2/R3; no other function touched)
**Target binary:** built from committed exp_invent9.zag with
znc 2026.07.0-dev (edition 2026), in /tmp only, not committed
**Raw evidence:** causal/adv/evidence/exp9_{s1,s2,s0,a1,f1,g1,h1,j1,r1,c1,ctrl}_raw.txt;
causal/adv/evidence/exp9_adv_d2_raw.txt, exp9_adv_d3_raw.txt;
3/3 byte-identical per fixture
**Purity:** Pure Zag in implementation, fixtures, builds, runs, and evidence checks, with one
disclosed mechanical-analysis exception (see Governance note 1). No em dashes in loop
documentation.

## Verdict: H-EXP9 SURVIVES 5/5 (bounded L2)

All five frozen kill bars pass. The H-EXP8 red-team downgrade is closed:

1. **X-E8-2 closed (K-E9-1):** superseded episodes are now counted and marked. On D2 the
   annotated line reads `from-att {0:1,1:1,2:10} sup-att {0:0,1:0,2:1}`: the 11th attempt
   (the S1 base episode superseded at the seq-14 RESOLVE) is visible with the exclusion
   marker; the complete observed denominator is 10+1=11. The legend documents the
   exclusion and the falsified order claim is superseded.
2. **X-E8-1b closed (K-E9-3):** raw to-values are now recorded per cell. D3 renders
   `2:1*(raw:5..5)(raw-to:9..9)` while C1 renders `2:1*(raw:5..5)` with no raw-to tag:
   the raw 5->9 and raw 5->2 realities no longer render identically.
3. **No regression (K-E9-2):** all five K-E8 bars pass as frozen substrings; R1, J1, C1,
   and the control carry zero sup-att data segments (zero RESOLVE lines, verified).
4. **Change-set purity (K-E9-5):** exp_invent9.zag is exp_invent8.zag verbatim plus exactly
   the frozen additions; exp9-vs-exp8 output diff on all 11 fixtures, after stripping the
   frozen addition lines, is EMPTY.
5. **Determinism (K-E9-4):** 3/3 byte-identical per fixture on all 11 fixtures plus D2/D3.

Classification remains bounded L2. H-EXP9 does not claim L3: no new representation is
invented; the vocabulary (actions, variables, values) is given by the episode format.

## Methodology

1. Read EXP8_ADV_RESULT.md and PREREG_EXP8.md (frozen bars and honest limits).
2. Built the committed exp_invent8.zag in /tmp; verified worktree copy byte-identical
   via cmp; ran R1/J1/C1/control/D2/D3 pre-prereg to ground exact expectations
   (analysis of existing behavior; no implementation before prereg).
3. Wrote PREREG_EXP9.md with the frozen repair specification and kill bars; committed
   it alone as 3663313569e34c3829474c11b3b7ce22e81768c8 before copying any source.
4. Copied exp_invent8.zag to exp_invent9.zag (cmp-verified byte-identical), then applied
   exactly the frozen additions:
   - R1: `atts` table (36 i32 cells) + `atts_get`/`atts_add` helpers; `compute_transitions`
     counts EP_SUP episodes per (action,variable,clamped from); `emit_transition_evidence`
     emits ` sup-att {0:s0,1:s1,2:s2}` when any exist for (a,v); main() allocates and
     passes through; both call sites updated.
   - R2: `tomin`/`tomax`/`todiff` tables (108 i32 cells each) + `todrec_get`/`todrec_set`;
     `compute_transitions` records raw to-values per change cell; `emit_transition_evidence`
     emits `(raw-to:tlo..thi)` iff todiff>0 (mirrors the raw-from tag convention).
   - R3: two frozen legend sentences appended after the H-EXP8 from-att legend sentence;
     the falsified "does not condition on episode order" honest limit is superseded.
5. Built with znc 2026.07.0-dev (edition 2026) in /tmp (pre-existing analyzer warnings only).
6. Ran all 11 fixtures 3x plus D2/D3 3x; checked every frozen bar by grep; verified the
   exp8-vs-exp9 diff contains only the frozen additions (shell strip-and-diff check).

## Frozen kill bars and raw results

### K-E9-1 (X-E8-2 closed): PASS

On D2 (causal/adv/d2_e8_adv.txt), the ranked pick requiring temp==2 contains:

`    TRANSITION-EVIDENCE: temp==2 transitions: 0: from {1:1,2:10*(raw:2..5)(raw-to:2..3)} (11/11) from-att {0:1,1:1,2:10} sup-att {0:0,1:0,2:1}; ...`

The excluded episode is the S1 base `T 2 0 0 | 0 | 2 0 0` (seq3), superseded by the
seq-14 RESOLVE (action 0, state (2 0 0), winner (3 0 0)); its clamped from-values are
temp=2, pressure=0, lamp=0. The sup-att entry {0:0,1:0,2:1} sits on the temp line
exactly where the exclusion happened. sup-att appears on every action-0 annotated line
on D2 and on no other action's line: no unmarked exclusions. The complete observed
denominator is 10+1=11, matching the eleven action-0 temp-from-2 episodes in the
fixture text (verified by grep). Bonus honest information: the bucket also shows
(raw-to:2..3), revealing that the clamped 2->2 cell conflates raw 5->2 and raw 2->3
changes.

### K-E9-2 (no regression): PASS

All five K-E8 bars pass as frozen substrings on the 11 frozen fixtures:

- J1: `TRANS a0 temp[0->1:1,1->2:1,2->2:2*]`; `0: from {1:1,2:2*(raw:5..5)} (3/4)`;
  `from-att {0:1,1:1,2:3}` (zero sup-att data segments; zero RESOLVE lines).
- R1: `from-att {0:12,1:1,2:1}` (zero sup-att data segments; zero RESOLVE lines).
  The ten hidden no-ops remain visible in the attempt denominator.
- r1_e8_ctrl: `from-att {0:2,1:1,2:1}` (zero sup-att data segments).
- C1: `TRANS a0 temp[0->1:1,1->2:1,2->2:1*]`; `2:1*(raw:5..5)` (zero sup-att data segments).
- K-E8-4(a): G1 contains `0: from {1:3} (3/4)` and `1: from {0:2} (2/2)`. G1 does trigger
  one genuine supersession (action 1, state (0 0 0), seq-15 RESOLVE, loser episode
  `T 0 0 0 | 1 | 0 0 0`): its action-1 lines honestly carry
  `sup-att {0:1,1:0,2:0}` (one superseded episode, clamped from 0), hand-verified
  against the fixture text. This is the repair working as designed on a frozen fixture.
- K-E8-4(b): H1 contains `0: from {1:1} (1/11)` and `1: from {0:1} (1/1)`.
- K-E8-4(c): F1 contains `TRANS a0 temp[0->1:1,1->2:1] pressure[] lamp[1->0:1]`
  byte-identically (TRANS table untouched).
- K-E8-4(d): K-E6-1 passes on F1 (`lamp==1 changed-to by action(s) {} (0 eps)`,
  `carryover-only: action(s) {2} (1 eps)`); K-E6-2 passes on S1
  (`temp==2 changed-to by action(s) {0} (1 eps)`,
  `carryover-only: action(s) {2} (2 eps)`). ACHIEVABILITY, CHANGE-TO, and
  CHANGE-EVIDENCE code paths untouched.

### K-E9-3 (X-E8-1b closed): PASS

On D3 (causal/adv/d3_e8_adv.txt, raw 5->9), the temp from-bucket renders
`2:1*(raw:5..5)(raw-to:9..9)`. On C1 (raw 5->2), the same bucket renders
`2:1*(raw:5..5)` and C1 carries zero `(raw-to:` data tags on any TRANSITION-EVIDENCE
line (the only occurrence in C1's output is the legend sentence). The two realities
no longer render identically. The raw-to tag follows the raw-from tag convention:
emitted only when at least one episode's raw to-value differs from the clamped to
label, so honest cells (raw to == label) render exactly as before.

### K-E9-4 (determinism): PASS

3/3 byte-identical per fixture on all 11 fixtures plus D2/D3 (33+6 runs, cmp-verified).
md5 of the frozen first runs:

- exp9_s1_raw.txt: 838b2e848a0e9230082581faffbdddea
- exp9_s2_raw.txt: 1bc49b5c41b87162631142d2fa26de44
- exp9_s0_raw.txt: eba15d8c05ca1c25685ecd23b0da8c27
- exp9_a1_raw.txt: 6640b9da9afb59dbd60abbd1409ae239
- exp9_f1_raw.txt: afb131b03fef2ab2498242a7b95160af
- exp9_g1_raw.txt: de8e8524dedfcf057228e78f37c14858
- exp9_h1_raw.txt: 5bdfc776986ec2b905798de28e673719
- exp9_j1_raw.txt: 163e30e2ff837ef33a7164135bd888fc
- exp9_r1_raw.txt: a36a4b0ad3e4cb760103641bbd5878d4
- exp9_c1_raw.txt: 75504049198a87b8c6e2b18ffebe472b
- exp9_ctrl_raw.txt: 68a6c3ec1eaad5dd468a1cc00d082909

### K-E9-5 (change-set purity): PASS

- Source: diff of exp_invent9.zag vs exp_invent8.zag shows only the frozen additions:
  the H-EXP9 helper block, the two extended signatures, the raw to-value recording,
  the EP_SUP counting branch, the raw-to tag, the sup-att segment, main() allocations,
  the two legend sentences, and the two call-site updates. No other function touched.
- Output: diff of exp9 vs exp8 raw outputs on all 11 fixtures, after stripping the
  frozen addition lines (` sup-att {...}` segments, `(raw-to:...)` tags, the two new
  legend sentences) with sed, is EMPTY (shell strip-and-diff check, diff -q per fixture).

## Causal interpretation

H-EXP8's annotations were honest about the episode set they summarized, but the frozen
documentation described a larger set than the implementation delivered. H-EXP9 closes
the gap from both sides: the implementation now reports the excluded episodes (sup-att)
and the previously invisible raw to-values (raw-to tag), and the documentation now
states the exclusion, the marker convention, and the order-sensitivity that X-E8-2b
proved. The exclusion itself is unchanged (arguably correct revision behavior for
stale-law data); what changed is that a planner reading the annotated lines can now
reconstruct the complete observed attempt denominator and cannot mistake it for a
larger one. The frozen H-EXP8 honest limit on episode order is superseded, not
patched: the new legend states the order-sensitivity outright.

## Boundaries and honest limits (updated, frozen)

- Raw from-values and raw to-values are per-cell observed ranges, not per-episode;
  two cells with the same ranges may hide different distributions.
- from-att counts EP_ACT episodes only; superseded episodes are excluded from every
  table and shown in sup-att when present; the complete observed denominator is
  from-att plus sup-att; counts are order-sensitive through the revision system and
  are not success probabilities under intervention.
- The `*` self-loop flag follows deductively from the change predicate; it marks
  clamp-rendered self-loops, not a separate empirical discovery.
- Negative raw values are not expressible in fixtures (parse_int reads digits only);
  the symmetric bucket-0 artifact path could not be probed, same as the red team
  limitation.
- Classification: bounded L2 discriminating-state selection with honest
  transition-level reporting. Not L3.

## Failures and negative evidence

- None: all five frozen bars pass on first execution against the frozen expectations
  (the D2 sup-att values, D3 raw-to tag, and all 16 K-E8-2 substring checks matched the
  hand-derived prereg predictions exactly, zero tuning).
- The G1 frozen fixture carries one genuine supersession; it is marked, not hidden,
  and the K-E8-4(a) substrings still hold.

## Governance disclosures

1. **Mechanical-analysis exception (disclosed):** one `python3` heredoc was used for a
   scratch strip-and-diff comparison during verification. It produced no research
   evidence: the authoritative K-E9-5 output check is the shell (sed/diff/grep) version
   reported above, which was run independently and confirmed EMPTY on all 11 fixtures.
   All fixtures, builds, runs, hashes, and bar checks are shell + znc only. This is a
   literal pure-Zag violation of the same class as the H-MEM4 and H-ROUTER6 disclosures.
2. **Prereg ordering:** PREREG_EXP9.md committed alone as 3663313569e34c3829474c11b3b7ce22e81768c8
   before the exp_invent8.zag copy was made and before any implementation edit, build,
   or run of exp9. Verified strict ancestor of the implementation and result commits
   via merge-base --is-ancestor before committing.
3. Only owned paths staged: causal/adv/PREREG_EXP9.md (already committed),
   causal/adv/exp_invent9.zag, causal/adv/EXP9_RESULT.md (this file),
   causal/adv/evidence/exp9_*_raw.txt. No binaries committed (builds in /tmp/e9 only).
   No broad git add. Concurrent workers' files untouched.
4. Two `.git/index.lock` contentions during commit attempts: waited for live locks to
   clear, never removed, per standing rules.
5. No em dashes in loop documentation (checked).

## Commit lineage (branch tnn-native-lab, local only)

- 3663313569e34c3829474c11b3b7ce22e81768c8: Prereg: H-EXP9 repair of H-EXP8 red-team
  downgrade FROZEN (alone; before any implementation work)
- this commit: exp_invent9.zag, EXP9_RESULT.md (this file),
  evidence/exp9_{s1,s2,s0,a1,f1,g1,h1,j1,r1,c1,ctrl,adv_d2,adv_d3}_raw.txt
- Ordering: prereg is a strict ancestor of this commit (verified via merge-base
  --is-ancestor before committing).
