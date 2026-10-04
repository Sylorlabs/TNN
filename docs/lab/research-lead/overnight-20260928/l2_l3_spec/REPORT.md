# REPORT: L2-L3 Specialize Combination (ORCHARD)

Worker: L2-L3 Specialize Worker (subagent, 2026-10-02).
Prereg: `l2_l3_spec/PREREG.md`, frozen alone at commit 74499703f
before any implementation existed, then transparently amended (A1)
at commit 839c701a2, still before any implementation commit. The
amendment fixed an arithmetic error in the v1 ARM-L3-ONLY pairing
proof (v1 kind-2 train episodes had singleton (k,a) groups, so
[CPY R0,R1] reached 5/8); the mechanism was sound, the world table
was flawed. A1 moved kind 2's signal pair from (a,b) to (b,c) so
`a` is constant across train and every (k,a) group is exactly half
pick / half skip. No other amendments.

## Verdict

**L2-L3-SPEC-COMPLETE.** All six kill bars PASS, no falsifier fired,
3/3 byte-identical.

## What was built

A standalone pure-Zag learner (`learner.zag`) plus experiment side
(`world.zag`, `driver.zag`), assembled as
`cat learner.zag world.zag driver.zag > spec_full.zag` (854 lines)
and compiled with the pinned znc to `spec_bin`. The learner holds:
X episode recall with a learned replay length (L=6) and learned
per-kind informative slot masks (MASK_K1=48, MASK_K2=12, from
per-kind slot variance across old episodes, frozen timing: once
after phase-0), the L2 SPECIALIZE standing rule (replay exactly the
queried episode's kind informative slots in ascending order, firing
on the kind tag plus learned masks, never researcher-selected per
problem), Y threshold decide on scalars (t=6 from prior experience),
and the L3 greedy constructor over the frozen op basis
{CPY,ADD,SUB,MAX,MIN} on 2 registers with first-2 loading (20
candidates/round, first-max tie-breaking, ascending threshold
sweeps). ADAPT_ON is a driver-set causal-control flag (the
composition_l2 adapt_on precedent), never written by the learner.

The hidden world rule (driver side only): PICK iff the kind's
signal pair sums >= 10, kind 1 using (d,e), kind 2 using (b,c).
The fixed-capacity 2-register consumer loads the first 2 replayed
readings, so X's general full replay [k,a,b,c,d,e] saturates the
registers with the kind tag and `a`; the signal pair never reaches
them without SPECIALIZE, which canonicalizes kind 1 to [d,e] and
kind 2 to [b,c].

## Kill-bar results (from spec_run1.txt, reproduced in runs 2 and 3)

- K-CB-1 (both required): L2-ONLY 0/4, L3-ONLY 0/4, FULL 4/4. PASS.
- K-CB-2 (L2-only fails): Z-L2ONLY 0/4 with ADAPT-STAT spec=8.
  Adaptation genuinely fired (Z lines show 2-reading replays
  [5,8],[3,2],[7,6],[2,3]) but decide is -1 without the novel
  intermediate. PASS.
- K-CB-3 (L3-only fails): Z-L3ONLY 0/4 with spec=0 and constructed M
  n=0. Construction trace: `C-ROUND 1 base=4 eval=20 stop`. The
  amended pairing proof holds: all train episodes have a=0, so the
  (k,a) groups (1,0) and (2,0) are each exactly half pick / half
  skip, and any deterministic program on (k,a) scores exactly 4/8 =
  the empty baseline. PASS.
- K-CB-4 (combined succeeds with provenance): Z-FULL 4/4,
  ADAPT-STAT-FULL spec=344, M-STATE n=1 t=6
  prog=1,0,1,0,0,0,... printed from learner state, and every Z line
  shows a 2-reading replayed sequence (adapted X' in the trace:
  s=13/5/13/5, dec=1/0/1/0, all ok). The invented intermediate is
  M = [ADD R0,R1], t=6, train 8/8. Construction trace matches the
  frozen hand derivation exactly: round 1 base=6, win=1,0,1 gain=2
  score=8 t=6 (first 8/8 in candidate order; later 8/8s from MAX and
  MIN lose the tie-break); round 2 stop. Y-PRIOR t=6 and T-AGREE
  y=6 m=6 (genuine agreement). PASS.
- K-CB-5 (M not in source): all 10 frozen grep patterns return 0
  hits on learner.zag (`d+e`, `b+c`, `ADD R0,R1`, `1,0,1`,
  `100049`, `1,0,0,0,4,9`, `orchard`, `threshold.*=.*6`, `_MODE`,
  case-insensitive `bridge`). PASS.
- K-CB-6 (determinism): spec_run1/2/3.txt sha256 identical
  (76495902b74a56bdcb01c0d8b64db7703059e479e7f7ac440aa9e93e54f3e78f).
  PASS.

No falsifier fired: F-NO-CREATE, F-NO-SPEC, F-L2-SUFFICIENT,
F-L3-SUFFICIENT, F-FRESH-PASS (Z-FRESH 0/4), F-OP-EXPAND, F-AUDIT,
F-NONDET, F-PYTHON all silent.

## Why this is L2 and L3 together

- L2: X's standing replay was the general fixed full replay, too
  general for a kind-heterogeneous world. From old episodes X learned
  per-kind informative slot masks (variance-based, tag excluded).
  On new episodes the SPECIALIZE standing rule adapts the replay
  (X -> X') purely on the structural preconditions of kind tag plus
  learned mask, canonicalizing the kind's signal pair into (R0,R1).
  The ARM-L2-ONLY arm proves the adaptation is real (spec=8,
  2-reading replays in the trace) and proves it is not enough (0/4,
  decide -1 without M).
- L3: M = [ADD R0,R1] was not in source (K-CB-5 audit clean), was
  constructed after experience through the white-box greedy trace,
  and is causally necessary (removing M in ARM-L2-ONLY collapses Z
  to 0/4). The ARM-L3-ONLY arm proves the invention cannot happen
  without the adapted X' (pairing proof: the generic replay's
  (k,a) view is label-uninformative, construction halts with n=0).
- The SPECIALIZE signature: unlike EXTEND (which exposed a hidden
  slot) and TRUNCATE (which removed displacing phantoms),
  SPECIALIZE canonicalizes a heterogeneous input into one canonical
  view, so the invented intermediate is minimal (one instruction).
  The L2 adaptation does the kind-conditioned routing; the L3
  construction does the value-level reduction; neither subsumes the
  other.

## Files

All under `docs/lab/research-lead/overnight-20260928/l2_l3_spec/`:

- PREREG.md (frozen, committed alone at 74499703f; amended
  transparently at 839c701a2, still prereg-only)
- NAMECHECK.md (toolchain guard Step 0 record, development notes)
- REPORT.md (this file)
- learner.zag (generic learner: X recall + SPECIALIZE, Y decide, L3
  constructor; 0 modes/handlers/semantic cases)
- world.zag (hidden rule + episode tables; experiment side only)
- driver.zag (four arms + kill-bar evaluation)
- spec_full.zag (assembled 854-line build input)
- spec_bin (compiled binary)
- spec_compile.txt (build log; exit 0; only benign zagd notice and
  three A0101 heuristic warnings, all provably in-bounds)
- spec_run1.txt, spec_run2.txt, spec_run3.txt (3/3 byte-identical
  outputs, 105 lines, 3357 bytes, 0 NUL bytes)

## Non-claims and bounds

- One world family (ORCHARD kind-tagged aggregation). No generality
  claim beyond the four demonstrated arms.
- Does not claim Micah's full 12-criterion L3 bar; targets the six
  frozen spec bars.
- The hidden world rule was builder-designed, not adversary-designed.
  Sealed-adversary generality is open future work.
- The op basis, 2-register first-2 consumer, greedy policy,
  variance mask learning, and SPECIALIZE rule are disclosed
  researcher-supplied generic machinery. The claims are: (a)
  SPECIALIZE fires on structural preconditions without per-problem
  researcher selection; (b) M's final form is source-underdetermined
  and history-determined.
- Pure Zag, safebin toolchain, zero forbidden executables. Paper
  untouched. Nothing pushed. Commits local on tnn-native-lab.
