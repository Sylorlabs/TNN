# PREREG AMENDMENT 2 (pre-implementation, committed before any .zag exists)

Amends PREREG.md (frozen cb8545cb4) + AMENDMENT1 (2d4e2ca9c). Reason:
worksheet self-review while designing the implementation.

1. GEN Q2 E (section 4): frozen as E=5, correct value is E=4.
   Derivation: pipeline mB0 chain_exec (1) + xs_general steps
   collect (1) + candidate collects mD2, mB0 (2) = 4. There is
   no delivery exec in the general path (it delivers via set_ans
   after the accepted trial; no promotion, no spec_exec). Pure
   arithmetic slip; no algorithmic change. GEN Q2 frozen S=1866
   unchanged. GEN Q2B E=4 was already correct.

2. SAW-SPEC GATE (sections 2, 4): xs_query's pipeline loop now
   records (tick-free, from the already-examined MAP headers)
   whether a live specialized MAP (cap==qcap, dom==qdom,
   d_param==0) was seen. If the pipeline fails AND such a MAP
   was seen, the query fails CLOSED (ANS -2) instead of
   re-running xs_specialize. Rationale (disclosed generic
   machinery): a specialized variant already exists for this
   capability/domain; the query is outside its fixed scope, so
   there is nothing to specialize. Without the gate, FULL Q2D
   would re-run the whole trial sequence (and derive a spurious
   candidate from mS itself). With the gate, FULL Q2D stays
   exactly as frozen: S=815, E=3, ANS -2,-2 via -1. No other
   frozen number changes (the gate reads already-examined
   headers; zero new ticks).

3. STEPS-BACKUP (section 2): build_cands runs xa_collect per
   target-domain MAP, which would clobber the stepset scratch
   (@1408) that adapter_trial's arity check needs. The frozen
   design now specifies: xs_specialize/xs_general snapshot the
   stepset (8 i32s @1408 -> @1600) and NSTEPS right after the
   steps collect, and restore them after build_cands. The copy
   loops cost zero ticks. No frozen S/E number changes; this
   only fixes which stepset the arity LINKscans observe
   (authoritative: the stepsMAP's, i.e. mB0's {50,51,52,53}).

4. PIPE DISPATCH (section 2): pipe_try dispatches on cap, not
   d_param alone: cap==AGG && d_param==1 -> home_exec (taught
   replay); cap==AGG && d_param==0 -> spec_exec (fixed
   re-grounding); else -> chain_exec (plain relseq walk).
   ROUTE MAPs (cap=2) carry d_param=0 from m_teach (descriptor
   extraction is AGG-only) but must chain-walk, not spec-walk.
   This matches the frozen worksheet (QB via chain_exec etc.);
   no numbers change.

No kill-bar thresholds, worlds, queries, or other frozen
numbers change.
