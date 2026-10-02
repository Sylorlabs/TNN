# REPORT.md -- H2 Value-Level Function Composition: XDOMAIN-VALUE-COMPLETE

## Verdict: XDOMAIN-VALUE-COMPLETE (K1-K7 all PASS)

Value-level function composition solves the cross-domain Z that
mechanisms A, B, and C all failed. The handoff is the intermediate VALUE
(34), not a merged graph structure. No structural merging, no navigation
concatenation.

## Results (3/3 byte-identical, sha256 `72f4a805...`)

| Arm | Z ans | Expected | Kill bar |
|-----|-------|----------|----------|
| TREAT | 2 | 2 | K1 PASS |
| ABL-X | -2 | -2 | K2 PASS |
| ABL-Y | -2 | -2 | K2 PASS |
| FRESH | -2 | -2 | K2 PASS |
| NO-VC | -2 | -2 | K3 PASS |

- K4: Stage1 intermediate v1=34 observed in TREAT. PASS.
- K5: Composite MAP id=309, m1=1, m2=2, mark=777. PASS.
- K6: ZPRIME ans=2 (new subject 41, pipeline re-executed). PASS.
- K7: 3 runs byte-identical. PASS.

## How it works

`vc_compose` tries ordered mode pairs (CHAIN,COUNT), (COUNT,CHAIN),
(CHAIN,CHAIN), (COUNT,COUNT):

1. Stage1: `vc_chain_exec(31)` assembles chain MAPs on subject 31,
   executes masked (no expected check), returns 34. No promotion.
2. Stage2: `vc_count_exec(34)` checks a learned count MAP exists
   (capability evidence), runs count template on 34, returns 2.
3. Final: 2==expected, promote composite MAP (93,31)->2 with
   fields 12=1, 16=2, 32=777.

The pair (CHAIN,COUNT) is discovered by trying ordered pairs, not given.
Mode definitions (CHAIN, COUNT) are researcher-authored; this is
declared in PREREG.md honest boundaries.

## Why ABL-Y works

`vc_count_exec` refuses if no learned count MAP exists (INC cell scan).
ABL-Y deletes r=92 MAPs, so stage2 returns -2 even though the count
template could technically run. This ties stage2 to learned Y knowledge,
not just general machinery.

## ABL-X trace (informative)

With chain MAPs deleted, stage1 mode=2 (count) fires on subject 31:
count(31)=3 (counts the 81-chain). Stage2 then fails on all modes
(chain(3)=-2, count(3)=-2). The mechanism correctly rejects a valid
but wrong intermediate. This shows the two-stage verification is
load-bearing, not just stage1 luck.

## Comparison with A/B/C failure

- A failed at admission (count MAPs invisible to plen contract).
- B formed cross-domain history but could not assemble (chain-only).
- C failed at admission (INC breaks relseq) and search semantics.
- H2 sidesteps all three: no admission filter on structure shape,
  no chain assembly. It executes each structure as a function and
  passes values.

## Architecture accounting

- Cognition lines added: ~150 (vc_patch.zag) + ~100 (vc_driver.zag).
- Modes / bridges / handlers / new semantic cases: 0 / 0 / 0 / 0.
- Frozen base (cc_base.zag, cc_patch.zag) used verbatim, read-only.
- Researcher-owned: mode definitions, ordered-pair search, expected
  for final verification, world design.
- Learner-owned: X/Y MAPs, intermediate value 34, composite record,
  Z' re-execution.

## Honest boundaries

1. Modes (CHAIN, COUNT) are researcher-defined. The mechanism discovers
   which ordered pair works, but does not discover the modes themselves.
2. Expected answer used for final verification (same as A/B/C).
3. Count execution uses trial template machinery; the learned MAP is
   capability evidence, not the executed graph.
4. One cross-domain pair tested (navigation x aggregation).

## Follow-ups

- H1 (typed contracts) and H3 (dataflow) are sibling workers; compare.
- Mode discovery: can the learner induce CHAIN vs COUNT from structure?
- 3+ stage pipelines.
- Replace expected with learner verification (C181).

## Deliverables

- PREREG.md (frozen as 5b5bb39e8, strictly before implementation)
- NAMECHECK.md (Step 0 guard recorded)
- REPORT.md (this file)
- vc_patch.zag (mechanism, 150 lines)
- vc_driver.zag (driver, 100 lines)
- vc_full.zag (assembled input, 2297 lines)
- vc_bin (pinned znc build)
- vc_compile.txt, vc_run1/2/3.txt (3/3 byte-identical)

Pure Zag. Safebin PATH. Zero em/en dashes (byte-verified).
Paper untouched. Frozen source read-only. Committed locally, nothing pushed.
