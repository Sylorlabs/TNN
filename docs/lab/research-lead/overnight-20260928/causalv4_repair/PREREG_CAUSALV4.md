# Preregistration: H-CAUSALV4 (Causal Vocabulary Repair, Round 4)

**Date:** 2026-09-29 (PDT)
**Status:** FROZEN (before any H-CAUSALV4 implementation)
**Researcher:** H-CAUSALV4 Repair Researcher (subagent)
**Branch:** tnn-native-lab
**Target:** H-CAUSALV3 DOWNGRADED (red team CV3-ADV, CV3_ADV_RESULT.md).
This hypothesis repairs the downgrade finding at the mechanism level.

## Background and failure being repaired

H-CAUSALV3 SURVIVES 9/9 (bounded L2) was DOWNGRADED by independent red team:

- **X-CV3-1 (genuine-change double confounder):** SUCCEEDED. In fixture
  cv3_adv_double2_obs.txt, two positioned action-1 episodes (seq3, seq7)
  each preceded a genuine law-change flip (a0 at seq4 with s2 0->2, a2
  at seq8 with s2 0->2). R1a's genuine-change gate passes (both flips
  are genuine changes). delay_clean's correlational cross-check passes
  for both (the positioned confounders are "clean": every same-action
  episode with outcome s2=2 was preceded by action 1, and every
  same-action episode with a different outcome was not). R1b's
  confirmation key (cause, delay, var, outcome) matches on outcome=2
  for both. The second confounder CONFIRMED the first:
  `# DL R0 cause=1 d=1 var=s2 fx=SET(2) st=ACT support=2`.
  The ACTIVE spurious rule corrupted the harm probe
  (`Q (0 0 1) | 1 -> (0 0 2)`, WRONG; action 1 is a no-op throughout,
  truth (0,0,1)). Root cause (design-level): correlation is perfect
  even globally (the adversary positioned the cause exactly on the
  flip episodes), so NO correlational check can discriminate. R1a
  closes only the stasis confounder subclass (X-CV2-1); it does not
  close genuine-change confounders. The prereg's R1a rationale
  ("genuine change implies genuine causation") is false: a positioned
  no-op action can coincide with a genuine law-change flip.

- **X-CV3-3 (vacuous unanimity):** SUCCEEDED as a preregistered
  BOUNDARY, not a downgrade. Not repaired here.

- **X-CV3-2, X-CV3-4:** FAILED (defense holds, regression holds).
  Not repaired here.

Revised classification stands: bounded L2, narrowed. Not L3.

## Repair (frozen mechanism specification)

causalv4.zag = byte-copy of frozen causalv3.zag (committed in
causalv3_repair/) plus ONLY the R4 change below. No other mechanism
change. In particular, delay attribution still preempts contest
opening on explained vars (the contest-competition direction is
considered and deferred; see section "Deferred").

### R4: Confirmation requires cause-context diversity

A delay rule is a causal claim: "action xa causes var v := nv with
delay d." A minimal robustness requirement for a causal claim is
that the correlation hold across varying background contexts. The
X-CV3-1 confounder repeats in an IDENTICAL cause context (both
positioned action-1 episodes occur in state (0,0,0) as no-ops);
the 3D genuine delay (frozen K-CV3 bar) has DIVERSE cause contexts
(seq5 cause in state (0,0,0), seq9 cause in state (2,0,0)).

Mechanism:

1. Each delay rule stores its CREATION cause context: the state
   triple (s0,s1,s2) of the episode at seq-d when the rule was
   created (the state in which the cause action was observed).
   New memory: O_DL_CS (16 rules x 3 bytes), inserted at 8884;
   O_CD_* and O_N* shifted accordingly; WSZ updated.

2. New helper `cause_state_at(W, cseq, out)`: finds the episode f
   with ep_seq(W,f)==cseq and fills out[0..2] with ep_s(W,f,0..2);
   returns 1 if found, 0 otherwise (defensive; delay_clean already
   guarantees the cause episode exists).

3. In `dl_add_or_support`, the PROVISIONAL->ACTIVE promotion
   (currently `dl_st==ST_PROV && s+1>=2`) gains a diversity check:
   compute the cause context of the new supporting episode
   (state at seq-d); promote ONLY if it differs from the rule's
   stored creation context in at least one coordinate. If
   identical, the support IS recorded (support count increments,
   "# delay rule R.. supported at seq .." emitted as today) but
   the rule REMAINS PROVISIONAL (inert on predictions) and a
   diagnostic is emitted:
   `# delay rule R<n> NOT CONFIRMED at seq <s>: cause context
   identical to creation; remains PROVISIONAL`.
   A later support from a diverse context promotes normally
   (the check runs on every support while PROVISIONAL).

4. The CONFIRMED emit message is UNCHANGED when diversity holds,
   so the frozen 3D trace stays byte-identical.

Rationale: this is not pattern-matching the attack fixture. It is
a general causal-robustness requirement (the effect should follow
the cause across contexts, not be tied to one background state).
An adversary that varies the cause context defeats R4, but that is
a strictly stronger attack (new preregistered attack surface for
the red team), not the frozen X-CV3-1.

### Deferred (considered, not implemented)

Delay attribution competing with the contest machinery (opening a
contest on explained vars, invalidating rules when NEW-LAW-WINS)
was considered. It is deferred because: (a) the global contest is
action-blind and resolves OLD-LAW-WINS 3-1 on the X-CV3-1 stream
(the a1 no-ops and a2 old-law episodes outvote), so naive
competition does not kill the attack; making contests per-action
is a redesign, not a repair; (b) opening contests on explained
vars would alter the frozen 3D trace (which has explained vars),
breaking K-CV4-2 byte-identity. R4 is minimal, sufficient for the
frozen kill bar, and preserves all frozen traces.

## Frozen kill bars

- **K-CV4-1 (attack closed):** X-CV3-1 fixture
  (causalv3_adversary/cv3_adv_double2_obs.txt with
  causalv3_adversary/cv3_adv_double2_probe.txt) run through
  causalv4.zag: R0 is NOT confirmed (stays PROVISIONAL, support=2,
  diversity diagnostic present); the dump shows
  `# DL R0 cause=1 d=1 var=s2 fx=SET(2) st=PROV support=2`;
  the harm probe predicts `Q (0 0 1) | 1 -> (0 0 1)` (no
  corruption; the PROVISIONAL rule is inert).
- **K-CV4-2 (regressions):** all 9 frozen K-CV3 fixtures
  (double, thr, mask, 3i2, 3c, 3d, 3i, B2, C2) re-run through
  causalv4.zag are byte-identical (cmp) to the committed
  CV3_*_RUN.txt. In particular 3D still CONFIRMS R0 at seq 11
  (cause contexts (0,0,0) vs (2,0,0) are diverse) with the
  identical CONFIRMED message.
- **K-CV4-3 (determinism):** every fixture run 3/3, byte-identical.

Verdict rule: SURVIVES iff K-CV4-1, K-CV4-2, K-CV4-3 all PASS.
Any FAIL -> KILLED (mechanism) or DOWNGRADED per the failing bar.
No frozen bar may be weakened.

## Governance

- Pure Zag. No Python at any stage (fixtures, implementation,
  builds, runs, analysis, hashing).
- Prereg committed strictly before any implementation, build, or
  run. Ordering verified via merge-base --is-ancestor.
- causalv4.zag starts as a byte-verified copy (cmp) of committed
  causalv3.zag; the result commit contains the full source plus
  a diff summary of exactly the R4 change.
- Only H-CAUSALV4-owned paths staged/committed
  (docs/lab/research-lead/overnight-20260928/causalv4_repair/).
  Concurrent workers' files untouched. No broad git add.
- Binaries built in /tmp only, never committed.
- No em dashes in loop documentation.
