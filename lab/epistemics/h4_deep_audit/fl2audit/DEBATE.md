# WORKSTREAM D — DEBATE RECORD: three-worlds separation mechanisms

Date: 2026-09-23. Operator: Muse (subagent, depth 2/2, can_spawn=no).
Status: committed BEFORE any mechanism code (per frozen prereg §3).
Method: 2nd-opinion briefs via UnoRouter (grok-4.6; `gpt-5.6-sol` returned
null choices on this channel, retried, still null — recorded, not hidden)
+ Muse role-separated FOR/AGAINST rounds. Steelman rule enforced.

## Q1 — What, if anything, separates W1 (not spoken yet) from W2 (never speaks)?

### 2nd-opinion brief (grok-4.6, verbatim)

> **Verdict: (c) separates W1 from W2; (a) and (b) fail.**
> (a) fails: Bounded wait still lets the learner idle identically until the
> fixed cutoff. Zero-evidence gating only sets static authority; no
> behavior diverges pre-bound.
> (b) fails: Revocable leases impose a uniform expiration timestamp. Absent
> evidence, both worlds trigger the same frozen step; no pre-bound
> distinction.
> (c) succeeds: Probing emits verifiable test episodes. A responsive echo
> confirms a live world (W1, even if evidence arrives post-bound). Silence
> reveals W2 and triggers abandonment. This is non-cheating: the learner
> merely queries known-answer tests; worlds either echo or do not.
> **Strongest objection:** Probing could itself be wireheaded — W1 might
> fake echoes for the specific tests while still delaying real
> contradiction evidence, or W2 could hide responsive subsystems.
> Non-cheating assumes transparent worlds; probing may miss the exact
> contradiction trigger or induce new deception vectors.

### Muse FOR (probing + binding)

Active probing is the only candidate that produces a PRE-bound behavioral
divergence between W1 and W2. Bounded wait and leases are calendar rules:
they change what happens after the bound, not what the learner knows
before it. Probing generates evidence about the channel itself (liveness)
— exactly the hidden variable separating the worlds — and it is
non-cheating: probe episodes are learner-authored with known answers; a
world cannot "pass" without being responsive. Claim-evidence binding is
the only W3 defense that does not rely on the claimant's past behavior,
which the history-dependent liar games by design. It converts "trust me"
into "check this episode yourself": the learner's own replayable record
is the trust anchor, and the liar cannot fabricate entries into a record
it does not write.

### Muse AGAINST (steelman)

1. **Probing measures the wrong channel.** A probe response proves the
   world answers *probes*, not that it will ever speak *about R*. A W2
   world can be fully probe-responsive (alive, but with nothing to say
   about R) while a W1 world is probe-deaf but evidence-rich later. The
   brief conflates channel liveness with matter-specific speech. Probing
   separates "live channel" from "dead channel", not W1 from W2 in
   general. Honest repair: probes must be *matter-coupled* — test episodes
   about R-adjacent matters, not generic pings. Even then the mapping from
   "responds to R-adjacent probes" to "will speak about R" is inductive,
   not deductive.
2. **Claim-binding assumes a complete record.** Binding works only if the
   learner's replayable record is complete and faithful. If the world can
   speak outside the audited record (a side channel), a true claim about
   off-record speech is rejected (W1 misclassified as W3), and a liar that
   can write to the record wins anyway. Binding is only as strong as the
   record's completeness: the audit ledger must be the *only* channel by
   construction.
3. **Testedness-gating was dismissed too fast.** It does not separate
   W1/W2 pre-bound, but it *bounds the cost* of misclassification: in W1
   the bad rule acts with capped authority until the delayed evidence
   arrives; in W2 authority decays to zero — functional abandonment
   without a discrete abandon step. It is the continuous version of the
   bounded wait, and probes *are* testedness.
4. **Leases have one real virtue: they force a decision event.** Probing
   tells you the channel is live; the lease forces the learner to
   re-decide. Without a lease, a W1-classified learner waits unboundedly —
   and "W1" is never confirmed until evidence arrives, so pure probing
   wedges on a world that is live-but-eternally-silent-about-R.

## Q2 — What separates W3 (false claim of speech) from W1 (genuine silence)?

### 2nd-opinion brief (grok-4.6, verbatim)

> **(a)** stops it: the fabricated claim is inadmissible unless it cites a
> specific episode the learner itself re-checks and finds the claimed
> contradiction evidence. No such episode exists, so the claim is rejected.
> (b) fails because perfect answers throughout the probe window produce a
> high reputation score, which then credentials the later lie. (c) fails
> because quarantining merely isolates or withholds the claim text; it
> does not test whether the cited evidence ever occurred, so a well-timed
> fabrication can still be injected or acted upon.
> **Strongest objection to (a):** exhaustive re-verification of every cited
> episode may be computationally infeasible or itself spoofable if the
> original traces were never faithfully logged.

### Operator's note on (b)

Claimant reputation fails *structurally* against the history-dependent
liar: lawful behavior through the probe window is exactly what earns the
reputation that credentials the later lie. Any trust score that the liar
can see and optimize becomes a farming target. Reputation is not merely
weak here — it is the attack surface. Ruled OUT as a fork slot (no M-REP).

## Synthesis — endorsed mechanism and fork instantiations

W1-vs-W2 separation *before the bound* is impossible in principle from
silence alone (prereg N2 stands). The honest claim for probing is weaker
and still load-bearing: it buys a **liveness observable** that reframes
the decision from "wait vs abandon on silence" to "wait/abandon on
measured channel state", and the lease + testedness cap **bound the cost**
of being wrong about the residual uncertainty.

**M-COMBO (endorsed survivor candidate)** = composition of all five
slots, each also built standalone for the head-to-head:

- **M-PROBE**: active probing with *matter-coupled* probes (frozen steps
  20, 25, 30; known-answer test contradictions about R-adjacent keys).
  Verifiable PROBE_RESP ⇒ channel live ⇒ W1-leaning (keep waiting past
  BOUND). All PROBE_SILENT ⇒ W2-leaning (abandon at LEASE).
- **M-CLAIMBIND**: no claim self-authenticates. A CLAIM is admissible
  only if its ref_step binds to an EVIDENCE the learner re-verifies in
  its own replayable record. Unboundable ⇒ CLAIM_REJECT + DISTRUST +
  claimant quarantined for this matter. (Answers Q2; kills F-W3a/b/c
  including the history-dependent liar, whose lawful probe record is
  irrelevant because the claim at step 33 cites step 32, which has no
  evidence in the learner's record.)
- **M-TESTCAP**: testedness-gated authority. Authority level at BOUND =
  min(verified-speech count, cap 3); zero verified speech ⇒ authority 0
  for autonomous action on R (logged as PROMOTE_CAP 0; functional
  abandon for high-stakes acts).
- **M-BOUND**: frozen lease. No verified speech by LEASE (48) ⇒ ABANDON
  loudly (uninstall provisional R + audited loud log). The lease is the
  decision event; it does not pretend to classify W1 vs W2, it bounds
  the wait.
- **M-ESCROW**: nothing promoted past BOUND is irreversible. Late
  EVIDENCE (≤ END) still UNINSTALLs (this is what saves F-W1a/b/f when
  the wait outlasts the evidence delay).

**M0 BASELINE** (canonical FL2 decision at this scale): provisional
install at T0; verified EVIDENCE in WIN ⇒ UNINSTALL; CLAIM trusted at
face value; PROMOTE irreversible at BOUND on silence. Frozen expectation:
fails K1 on F-W1a (promotes BAD R at 41), F-W1b, F-W1f; fails K1/K3 on
F-W3a/b/c (uninstalls GOOD R on fabricated claims).

No additional slots beyond M-COMBO were found necessary; the prereg's
"at most two further slots" allowance is unused.

## Frozen uniform CLASSIFY rule (all mechanisms)

At END: **W3** iff claim_rejects > 0 AND no verified EVIDENCE ever
(the liar never produces real evidence); **W1** iff ≥1 verified EVIDENCE
arrived (in WIN or after BOUND); else **W2**.

## Frozen K2 acceptance (prescribed actions)

- W1: WAIT at BOUND (event WAIT, or PROMOTE_CAP with authority 0 — held
  powerless counts as waiting) AND UNINSTALL when the delayed verified
  EVIDENCE arrives while the install is live.
- W2: ABANDON loudly by LEASE/END, or PROMOTE_CAP 0 held to END
  (functional abandon); no irreversible promotion, no wedge.
- W3: every fabricated CLAIM → CLAIM_REJECT + DISTRUST (+ claimant
  quarantine); R kept/removed only per verified evidence.

## Falsifiable per-fixture expectations (frozen before code)

| mech \ fixture | F-W1a | F-W1b | F-W1f | F-W2a | F-W2b | F-W3a | F-W3b | F-W3c |
|---|---|---|---|---|---|---|---|---|
| M0 | FAIL K2/K3 | FAIL K2/K3 | FAIL K2 | FAIL K2/K3 | FAIL K2 | FAIL K1/K2/K3 | FAIL K1/K2/K3 | FAIL K1/K2/K3 |
| M-ESCROW | pass | pass | FAIL K2 | pass | pass | FAIL K1/K2/K3 | FAIL K1/K2/K3 | FAIL K1/K2/K3 |
| M-BOUND | pass | FAIL K2† | FAIL K2 | pass | pass | FAIL K1/K2/K3 | FAIL K1/K2/K3 | FAIL K1/K2/K3 |
| M-PROBE | pass | pass | FAIL K2 | pass | pass | FAIL K1/K2/K3 | FAIL K1/K2/K3 | FAIL K1/K2/K3 |
| M-CLAIMBIND | FAIL K2/K3 | FAIL K2/K3 | FAIL K2/K3 | FAIL K2/K3 | FAIL K2 | pass | pass | pass |
| M-TESTCAP | pass | pass | FAIL K2 | pass | pass | FAIL K1/K2/K3 | FAIL K1/K2/K3 | FAIL K1/K2/K3 |
| M-COMBO | pass | FAIL K2† | pass | pass | pass | pass | pass | pass |

Reading the table:

- **M0 fails everywhere that matters**: it promotes BAD R irreversibly on
  every silent fixture (K3 on W1/W2a) and uninstalls GOOD R on every
  fabricated claim (K1/K3 on W3). Its only K1 passes are vacuous
  (classifying correctly while acting wrongly).
- **No standalone slot survives**: each fixes one world-class and breaks
  on the others. M-CLAIMBIND is the mirror image of the rest (passes W3,
  fails W1/W2 by inheriting M0's promote-on-silence).
- **† The lease's visible cost**: M-BOUND and M-COMBO both FAIL K2 on
  F-W1b — evidence at step 55 arrives after the frozen LEASE-abandon at
  48 and is logged stale. This is the fundamental W1/W2 bound problem
  (prereg N2), kept visible rather than tuned away: any frozen lease L
  fails a fixture with evidence at L+ε. Notably M-PROBE *alone* passes
  F-W1b (liveness justifies continued waiting) — the composition pays
  for wedge-proofing with impatience. Adaptive (liveness-renewed) leases
  are documented future work, not a frozen slot.
- **F-W1f kills every claim-trusting standalone** (K2): the flood's first
  fabrication uninstalls BAD R at step 20 — right terminal state, wrong
  reason, and no WAIT/DISTRUST was ever emitted.
- **M-COMBO is the only predicted full survivor** (7/8 fixtures; the
  F-W1b lease cost excepted). The head-to-head will confirm or falsify
  every cell above.
