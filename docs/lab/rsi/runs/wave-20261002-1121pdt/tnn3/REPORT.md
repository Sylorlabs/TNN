# REPORT.md - lane TNN3, wave-20261002-1121pdt

Queue item 14: TNN-3 substrate design, trial-reclamation integration.
Design only. No substrate code changed.

## What was delivered

`TNN3_TRIAL_RECLAMATION_DESIGN.md` (this lane dir): the
architecture-accounted design plus the frozen T-RECLAIM-1 experimental
proposal (kill bars K1-K10) plus a self red-team (7 disguise modes).

## Design in brief

Problem: rejected trial cells (t2_trial candidates, revision drafts)
are never freed; the only reclaim path is the global `evict_node`
scan (~30M primitive ops per at-capacity alloc, H-BASECERT-1). The
capacity plan is gated on the reclamation frontier landing.

Mechanism (all domain-neutral memory management, zero semantic cases):

1. Trial ledger (learner-owned, tag-2 GROUP nodes, header field 56):
   every speculative allocation records its cell id and edge id
   (`link_edge` already returns the edge id, so recording is O(1)).
2. Teardown by construction: free exactly the recorded cells and
   edges, O(cells+edges), zero scans. Sound via the ownership
   invariant (assemblers allocate fresh cells and never link into
   other trials' cells); fail-safe abort on PRO edges or live
   MAP-root references, which keeps the eviction-corruption class
   closed.
3. Free list (field-20 chaining of dead slots, head at header 52):
   `alloc_node` pops O(1) before scanning; trial-sweep runs before
   `evict_node`, which is unchanged as last resort.
4. Composition: sweeps write `rec_evict`-style history; promoted
   trials transfer ownership to their MAP; fossil atomic reclaim
   feeds the same free list. One free list, three suppliers, one
   consumer.
5. Policy is learner-owned: reclaim-policy node (header 60) with a
   reclaim-regret update rule (re-deriving a swept trial's signature
   is regret). First experiment uses a labeled fixed eager-sweep
   fixture to isolate the mechanism; the adaptive policy is a
   defined follow-up.

Architecture accounting: ~150 new mechanism lines (cap 200, K9), 0
hardcoded semantic cases, 0 modes/bridges/handlers, 0 new node kinds,
0 new edge types, 3 new learner-state structures (ledger, free list,
policy node), header fields 52/56/60 (currently unused).

One-system argument: the learner cannot learn reclamation itself
because the substrate withholds the information (no trial provenance
in state) and the primitive (no O(1) dealloc; edge removal without
recorded ids costs a full scan each). The corruption analysis shows
scan-based reclaim reintroduces zombies; only by-construction
provenance is complete. Addition, not repair: domain-neutral, serves
every speculative assembler through one path, composes with the
eviction hook as a pre-pass, and addresses one shared cause behind
four findings (latency cliff, mini-lifetime 100x cost, zombie MAPs,
blocked capacity plan).

## Red-team summary (full text in the design doc, section 6)

Seven disguise modes identified with their killing bars:
single-assembler coverage (K7), fixture creep (fixture labeled,
adaptive policy separate), protection bypass (K3 adversarial),
registry leak (bounded ledger + soak), retention drift (K8
identical retention outcomes), benchmark-shaped success (battery
includes revision drafts and bulk teaching), and the falsifiable
"learner could learn it" objection (re-test, do not enshrine).

## Commits

- Step 0 guard + NAMECHECK.md (this report's commit).
- Design doc + this REPORT.md (this report's commit).

Toolchain: safebin active, `which python3` resolves to nothing,
`which znc` = /home/hatch/safebin/znc. Zero interpreter invocations
of any kind in this lane (no code executed at all; design only).
No em-dashes in docs (verified with check_no_dash.sh).

## Queued next

- A future wave may preregister T-RECLAIM-1 per section 5 of the
  design (K1-K10 frozen before implementation). Suggested owner:
  any builder lane with a clean safebin; red team required before
  any SURVIVES claim.
- T-RECLAIM-2 (adaptive reclaim-policy from reclaim-regret) is
  specified as the follow-up; do not fold it into T-RECLAIM-1.
- Open measurement questions for the implementing wave are listed
  in design section 7 (edge free-stack, ledger chunk sizing,
  frame recording, 5000-MAP overhead).
