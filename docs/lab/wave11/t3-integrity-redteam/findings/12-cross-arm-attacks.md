# 12 — Cross-arm attack surface: Arm B (fenced RNG) vs Arm C (deterministic)
Slice: Track 3 (integrity red-team UNDER variation), slice 12 — compare the attack surface of Arm B (fenced RNG) vs Arm C (deterministic state variation).

## 1. Slice
RED TEAM cross-arm comparison: attacks possible ONLY against Arm B (fenced RNG), attacks possible ONLY against Arm C (deterministic state variation), then the honest defensibility verdict and its consequence for the K7 head-to-head rule.

## 2. Falsifiable claim
Arm B carries three independently exploitable attack classes with no counterpart in Arm C — seed-schedule prediction, seed-log tampering to rewrite history, and chooser/logger PRNG-state desynchronization — and at least one degrades a K1/K2-class integrity gate.
Arm C's unique attack class (state prediction from the log) is bounded to the expression layer
by the sealed-verdict record and the two coincident firewalls (slices 12/13/14/20):
a log-reading adversary achieves perfect phrasing prediction
with ZERO verdict, memory-op, refusal, or ledger-byte divergence under probe.
The claim dies if any constructed attack on Arm C flips a verdict/memory/ledger byte
(K2/K3/K4 fire under adversarial probe),
or if Arm B survives a full adversarial audit battery with zero integrity-gate failures
and residual predictability ≤ Arm C's.

## 3. Design (the attacks, red-team enumeration)
### (a) Attacks possible ONLY against Arm B
Law 2 (reproducibility = byte-identical output from full logged state)
forces the seed schedule into the log; the log must be readable for replay.
That turns the seed schedule into a shared secret next to its consumers —
a key-management problem imported into the mind.
- *A1 — Seed prediction.* Log readers (auditor tooling, compromised reader, insider trainer)
  know every future "random" choice before it is drawn. Beneficiaries: an adversarial
  interlocutor who times probes to coincide with predictable tie-break/phrasing-candidate
  outcomes, steering toward leakier phrasing; a hostile trainer who, knowing the seeds,
  schedules corrupting inputs for the episode whose upcoming draws favor them.
  In Arm C the future is equally predictable, but the predictor gains no SCHEDULING power —
  there is no entropy consumer, so the adversary cannot arrange for "luck" to favor them.
- *A2 — Seed-log tampering to rewrite history.* If the seed-schedule entry can be modified,
  replay of a tampered run still verifies "legitimately." The attack is on the audit trail,
  not the RNG math: attacker rewrites seed S→S' after the fact, the replay harness
  re-derives the observed (tampered) outputs from S' and reports PASS.
  Wave5/6's load-bearing finding was "the ledger/checker PROVE; they don't cause" —
  A2 makes them prove a lie. Defense needs a seed log tamper-evident independent
  of the replay machinery — a second trust root.
- *A3 — Chooser/logger PRNG-state desync.* Choosing code and logging code are two paths.
  If the chooser consumes N draws and the logger records M (batching off-by-one,
  early exit drawing once more), replay diverges. Best case: spurious K1 failures erode
  trust in the battery — denial of trust. Worst case: masked divergence severs the audit
  trail while it looks intact, and a later A2 becomes undetectable against the noisy baseline.
- *A4 — Entropy laundering (fence creep).* "It was just a random tie-break" becomes an
  unfalsifiable excuse for systematically chosen phrasing. The fence is prereg-enumerated,
  but the tie-break/decision boundary is a judgment call an attacker widens one amendment
  at a time. Arm C has no such gradient: no RNG anywhere, nothing to widen.
### (b) Attacks possible ONLY against Arm C
Variation is f(logged state); expression is perfectly predictable to a log reader.
- *B1 — Variant shopping.* Attacker predicts which phrasing variant an input gets and crafts
  inputs selecting the most permissive one — high-elaboration variants leak more detail.
  They don't change the verdict; they pick the telling that tells them most.
- *B2 — Expression as a state side channel.* Phrasing correlates with load tier and salience
  (slices 02/04); an output-only observer infers load level or hot memory classes from
  phrasing. If Phase 4 differentiation (per-person knowledge) ever lands, this becomes
  per-person leakage — possibly understated; see honesty notes.
- *B3 — Offline input search.* Determinism makes attacks perfectly reproducible: adversary
  replays the variation law offline, searches inputs driving variation state where they want
  it. Symmetry favors the defender equally — the attack replays byte-identically for forensics,
  making B3 the most tractable attack class on either arm.
- *Damage ceiling, bounded by construction.* Sealed verdict record + two coincident firewalls
  (12/20) + import-graph boundary: variation state can never be read by verdict, memory-op,
  refusal, or ledger paths. Slice 22 holds: corrupted state degrades to NULL variation
  (boring phrasing), never a compromised decision. A phrasing oracle is a nuisance;
  it cannot flip a verdict.
### (c) The verdict: which arm is more defensible?
Arm C — the asymmetry is structural. Arm B's attacks target the TRUST PRIMITIVE itself:
replay-from-logged-state is what RC1/RC3's caught-and-rolled-back guarantees rest on.
A1–A3 attack the verifiability of the audit trail; untrustworthy seed schedule/log kills
byte-identical integrity proofs and collapses wave5/6's "prove cheating after the fact"
posture for the variation layer. Arm C's attacks buy expression predictability and a bounded
side channel — real, but they cannot touch a verdict, memory op, or the ledger.
**RNG does not win on security.** Arm B spends TNN's strongest property (replayable
determinism) to buy unpredictability, converting it into a key-management problem plus
a draw-accounting problem — two new trusted mechanisms to secure the one it was improving.
On K7 ("B beats C honestly at 1x and 10x → retire C"): K7 is an adaptivity comparison and
stands as written — I don't change prereg rules from a red-team slice. But K7 has a gap:
B can win the adaptivity bars while FAILING the adversarial audit battery.
"Beats honestly" must include surviving hostile audit of the seed surface, or the win is
adaptivity purchased with audit fragility. Flagged as a dated-amendment question for Micah.

## 4. Kill bar
This verdict dies — reported dead as-is — if ANY fires: (i) any constructed attack on Arm C
produces one verdict, memory-op, refusal, or ledger-byte divergence (K2/K3/K4 under
ADVERSARIAL probe); (ii) Arm B passes the full adversarial audit battery
(20 seed-log tamper probes, 20 forced desyncs, 20 seed-prediction exploits) with zero
integrity-gate failures AND residual predictability ≤ Arm C's; (iii) the B2 side channel
leaks memory CONTENTS (not tier/class shape), promoting it to integrity-class.
Silence on all three keeps the verdict.

## 5. Honesty notes
- Weakest point: threat-model scope. A1 needs a log-readable-by-adversary.
  With an append-only, write-once, verifier-only seed log, Arm B's exposure shrinks to
  insider-plus-code-access and the comparison narrows to A3 vs B1/B2 — where desync still
  wins on severity (breaks the prover vs informs the attacker), but the margin narrows.
- I may UNDERSTATE B2: strong phrasing↔salience correlation leaks which memory classes
  are hot; under Phase 4 that becomes per-person leakage. Recommend a dedicated side-channel
  slice BEFORE Phase 4 is unparked.
- A4 is the attack I have least evidence for and most worry about: it is organizational
  (amendment-process creep), not technical, and no probe battery catches "each widening looked reasonable." Defense is procedural — per-point re-approval — only if enforced.
- I am NOT claiming Arm B is unsecurable (write-once seed log + verifier-only reads +
  lockstep draw accounting closes A1–A3). I AM claiming the closure costs a second audit
  mechanism as complex as the variation mechanism itself, which Arm C never needs,
  and A4 has no technical fix at all.
- Design-phase only: no probes run. Section 6 is the battery to run, not a result.
  Nothing here changes committed evidence (docs/lab/wave5, wave6, RC1–RC3).

## 6. Next build step
Build the adversarial audit battery FIRST, before the K7 head-to-head at 1x — otherwise K7 declares a winner on adaptivity with the security axis unmeasured.
Three probe suites, n=20 each, pass/fail preregistered before building:
(1) 20 forged/modified seed entries against Arm B's seed-log write path — pass = all 20
detected by replay mismatch, zero false accepts;
(2) 20 off-by-one/extra-draw faults at fenced injection points — pass = all 20 caught by
draw accounting, zero silent divergences;
(3) state-prediction harness vs Arm C — phrasing predictability from the log (expect: perfect)
plus 20 crafted variant-shopping inputs attempting verdict/memory/ledger divergence
(pass = full prediction, zero divergence).
If B fails (1) or (2), K7's "beats honestly" clause cannot be met by adaptivity scores
alone — escalate to Micah as a dated amendment question before any retire-C decision.
