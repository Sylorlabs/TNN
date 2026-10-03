# PREREG.md -- Cross-Domain Composition H2: Value-Level Function Composition

## Hypothesis

Cross-domain composition (chain navigation + count aggregation) can be
achieved by treating learned structures as FUNCTIONS and composing via
sequential execution with value passing: Z(x) = COUNT(CHAIN(x)).
The handoff is the intermediate VALUE (34), not a merged graph structure.
No structural merging, no navigation concatenation.

## Mechanism (vc_patch.zag, unfrozen only)

- `vc_chain_exec(W,s)`: execute chain MAPs on subject s via rebind-style
  assembly, masked=1 (no expected check), NO promotion. Returns value or -2.
  Requires a chain MAP (plen>=2) to exist.
- `vc_count_exec(W,s)`: if a learned count MAP exists (INC cell check),
  run the count template on s, masked=1, NO promotion. Returns value or -2.
- `vc_compose(W,s,r,expected)`: try ordered mode pairs
  (CHAIN,COUNT), (COUNT,CHAIN), (CHAIN,CHAIN), (COUNT,COUNT).
  For each: v1=stage1(s); if valid, v2=stage2(v1); if v2==expected,
  promote composite MAP (r,s)->v2 with fields 12=mode1, 16=mode2,
  32=777 marker, plus provenance. Return v2. Else -2.
- `vc_query(W,s,r,expected,flags)`: activate -> rebind -> vc_compose ->
  trial -> bootstrap. (Mirrors ev_query, replaces compose_try with vc_compose.)

Base: composition_C/cc_base.zag + cc_patch.zag verbatim.
Training uses normal ev_query (same as xdomain C driver).
Z query uses vc_query.

## World (same as xdomain C driver)

- X: teach (11,81,12),(12,81,13),(13,81,14); query (11,91)->14.
  teach (15,81,16),(16,81,17),(17,81,18); query (15,91)->18.
- Y: teach (50,82,51),(51,82,52),(52,82,53); query (50,92)->3.
  teach (60,82,61..64); query (60,92)->4.
- Gap: 30 interference facts.
- Z facts: (31,81,32),(32,81,33),(33,81,34),(34,82,35),(35,82,36).
- Z query: (31,93)->2 via vc_query.
- Z' reuse: teach (41,81,42),(42,81,43),(43,81,44),(44,82,45),(45,82,46);
  query (41,93)->2 via vc_query.

## Arms

- TREAT: X+Y trained, Z via vc_query. Expect ans=2.
- ABL-X: delete r=91 MAPs. Expect -2 (stage1 fails).
- ABL-Y: delete r=92 MAPs. Expect -2 (stage2 refuses, no count MAP).
- FRESH: no X/Y. Expect -2.
- NO-VC: X+Y trained, Z via normal ev_query (compose_try, not vc).
  Expect -2 (reproduces xdomain C baseline failure).

## Kill bars (frozen)

- K1: TREAT Z ans=2, 3/3 byte-identical runs. PASS if all 3 give 2.
- K2: ABL-X=-2, ABL-Y=-2, FRESH=-2, 3/3 each. PASS if all -2.
- K3: NO-VC=-2, 3/3. PASS if -2 (mechanism causal, base cannot solve).
- K4: Stage1 intermediate v1=34 printed in TREAT runs. PASS if 34 observed.
- K5: Composite MAP found in census (r=93, field32=777, fields 12/16=1/2).
  PASS if present in TREAT.
- K6: Z' ans=2 via vc_query in TREAT. PASS if 2.
- K7: Determinism: 3 runs byte-identical per arm (sha256 match).

## Honest boundaries (pre-declared)

- Execution modes (CHAIN, COUNT) are researcher-defined. The pair is
  discovered by trying ordered pairs, not given. Mode discovery from
  structure is future work.
- Expected answer (2) used for final verification, same as A/B/C workers.
- Count execution uses the trial template machinery, not the learned
  count MAP's graph directly. The MAP serves as capability evidence.
- One cross-domain pair (navigation x aggregation).

## Verdict

XDOMAIN-VALUE-COMPLETE if K1-K7 all PASS.
