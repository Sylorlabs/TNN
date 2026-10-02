# QUEUED-CHECK report: wave-20261001-2321pdt "Queued next" section currency

Lane: QUEUED-CHECK (verification only; no experiments). Safebin Step 0 verified, see NAMECHECK.md. WAVE_RECORD.md not edited; this report is for the coordinator/parent.

Check time: 2026-10-02 ~00:45 PDT. Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.

## Verdict: NOT CURRENT. The section is empty, not stale.

The "## Queued next" section in `docs/lab/rsi/runs/wave-20261001-2321pdt/WAVE_RECORD.md` (lines 81-83) contains nothing but the placeholder `(to be filled)`.

Consequences of that emptiness:

1. **No stale items are listed.** It does NOT list BATTERY-E8, H5R2-SKEPTIC3, or CONTLEARN-OWNED2 as queued. All three have landed (BATTERY-E8 E8-BANDWIDTH, H5R2-SKEPTIC3 SEPARATED, CONTLEARN-OWNED2 MACHINERY-DEPENDENT, all [NEW] per FINAL-COUNT's 47-verdict coherence check), so nothing in the section contradicts the landed verdicts.
2. **Everything that should be queued is missing.** The section carries zero items while at least a dozen legitimate queue items are pending. Filling it is the required action.

## Stale queued items elsewhere (for awareness, not in the record section)

The LOOPSTATE-DRAFT's queued-next line (line 61) IS stale, if the coordinator reads it as the source of truth:

- It lists H5R2-SKEPTIC3 as queued ("two live facts on one key..."). It landed: SEPARATED [NEW]. Remove when refreshing from the draft.
- It lists BATTERY-E8 as "(already running)". It landed: E8-BANDWIDTH [NEW]. Remove when refreshing from the draft.
- It lists "continuing learner integration". This is now actively misleading: CONTLEARN-OWNED and CONTLEARN-OWNED2 (both MACHINERY-DEPENDENT) show the frozen core has no learner-invoked trial/construct machinery, so integration work sits on the researcher side of the control-plane line. DRAFT-CHECK recommends replacing it with: "LEARNER-OWNED mechanism proposal first: root-cause analysis (per the no-patch-treadmill rule) of how learner-created state could initiate structure construction; no new handlers/modes/opcodes until that mechanism is proposed."
- CONTLEARN-OWNED2 must not be re-queued: OWNED-SYNTHESIS section 9 states "No further machinery-disabled replications are needed: the fact is doubly confirmed."

## Items that SHOULD be queued (additions for the section)

Ordered by priority:

1. **SENSORY verdict when it lands, plus RT-SENSE red-team coverage.** The SENSORY lane is still running and progressing normally (H2v1 renders in flight; SENSORY-CHECK re-checked at ~00:41 PDT, verdict expected in roughly 45-60 minutes). Queue the verdict pickup and its RT-SENSE review.
2. **The wave debate itself.** DEBATE-READY's readiness check (00:40 PDT): the debate minimum is present and committed (DEBATE-PREP/DEBATE_BRIEF.md, CLUSTER-FINAL/CLUSTER_FINAL.md, ARENA-SYNTH/ARENA_SYNTHESIS.md). OWNED-SYNTH/OWNED_SYNTHESIS.md, H5R2-SYNTH/H5R2_SYNTHESIS.md, and QUAL-SUMMARY/QUAL_SUMMARY.md are still being written and should be folded in when they land. The Fork bullet is explicitly marked "(debate pending)".
3. **Newest-live-among-all-live gate test: debate decides whether it is the next build.** H5R2-SYNTHESIS names this as the concrete testable next hypothesis after SEPARATED: a provenance filter (live, non-superseded licensing facts) combined with newest-live tie-breaking among all verifying candidates, which must show SEP-NEW 8/8 on the re-teach family, D ok 8/8 on the decoy family, CD ok 8/8 on the chained family, the full baseline five-bar vector, and 46/46 on the built-in battery. The debate should decide whether this is the next build or whether a stronger discriminator comes first.
4. **Bare-prompt abstention test.** RT-ARENA5 QUALIFY plus ARENA-GEN NARROW show DEFRECALL is extensionally a bare-prompt handler (it enumerates on whattime and invent, where it should abstain). Queue: a general default-action candidate must demonstrate abstention on inappropriate bare prompts (whattime/invent test); multi-step tool protocol for C15 is still unimplemented.
5. **LEARNER-OWNED mechanism proposal.** Per CONTLEARN-OWNED/OWNED2 and DRAFT-CHECK suggestion 2: before any future LEARNER-OWNED push, propose a mechanism by which learner-created state initiates structure construction (constitution's learner-authority metric). No new handlers, modes, or opcodes until that mechanism is proposed.
6. **Still-open items from the draft that are NOT stale** (keep, do not drop):
   - F1 repair-time policy experiment (what makes a later burst run to zero vs stall; fresh prereg on relaxed S-prime).
   - C9GEN as a candidate instrument for a future wave's governance decision (frozen arena battery untouched).
   - Arena C9 world-generator fix (randomize candidate order; add real intervention turns; C9 stays a sealed zero until the fix lands).
   - Blind re-examination mandate (debate decides how far it extends across prior construction claims, per BATTERY-E3 reframe).
   - H2R/H6R/H7R re-attempts gated on the substrate-adoption governance decision.
   - Arena work toward 1.0 across all 15 capabilities (remaining sealed zeros: C9 causal, C15 goal tool protocol).
7. **Debate agenda updates** (per DRAFT-CHECK suggestion 4): add a 6th debate item (adjudicate CONTLEARN-OWNED's machinery-dependent finding and the mechanism-first requirement for any future LEARNER-OWNED push); extend debate item 3 (ARENA2 REMAP vs ARENA3 TRX) with the ARENA5 DEFRECALL qualification pair (RT-ARENA5 QUALIFY plus ARENA-GEN NARROW); extend debate item 4 (BATTERY-E3 mandate scope) with E8's refined H2a claim for the record.
8. **Record bookkeeping** (per OWNED-SYNTHESIS section 9): bind the CONTLEARN-OWNED supersession wherever LEARNOWN-DEMONSTRATED is cited (bounded form: "machinery-enabled scope; strong sense measured absent"); fix the SHA-256 typo in LEARNER_MECH_ANALYSIS.md section 1 (correct value in the MECH-VERIFY report).
9. **Record-only consequence, not a queued experiment:** Cluster 2 discrimination program is COMPLETE (H2a refined to the narrow claim that subject-identity content of an actionable guide does not differentiate the emitted action; H2b killed; H2c-sticky confirmed; H2d confirmed as contributing cause by E8-BANDWIDTH).

Explicitly NOT to queue: further machinery-disabled replications (doubly confirmed); Cluster 2 follow-up discriminators (E8 done, program complete).

## Consistency with DRAFT-CHECK section (c) suggestions

- Suggestion 1 (remove BATTERY-E8 as running; add the Cluster 2 COMPLETE consequence; supersede the BATTERY-E2 line's "Remaining within-cluster discriminators: E6, E8"): CONSISTENT. The record section has nothing to remove, but the consequence text above (item 9) should be added.
- Suggestion 2 (replace "continuing learner integration" with the mechanism-first instruction): CONSISTENT. Covered by item 5 above.
- Suggestion 3 (add the bare-prompt abstention test to arena work): CONSISTENT. Covered by item 4 above.
- Suggestion 4 (debate items: 6th item; extend items 3 and 4): CONSISTENT. Covered by item 7 above.
- Suggestion 5 (escalation appends for BATTERY-E3 and staging races; no new escalation items required): NOTED. No queued-next impact; those belong to the escalation section, not this one.

## Summary for the coordinator

The "Queued next" section is NOT current: it is empty. It lists no already-landed items, so there is nothing to remove, but it is missing every pending item. Fill it with items 1-9 above (with the explicit do-not-queue guards). If the coordinator drafts the section from the LOOPSTATE-DRAFT queued-next line, also strip the three stale entries (H5R2-SKEPTIC3, BATTERY-E8, "continuing learner integration") before copying.
