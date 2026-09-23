# 09 — Replay spoofing: attacks on the replay chain (RED TEAM)

## 1. Slice
Red-team the §17 replay protocol (finding 17, t1-state-variation): ledger/state tamper
masquerading in the A/B/C/D taxonomy, replay sleepers against the two-build-hash
requirement, and log-truncation attacks presenting partial logs as complete.

## 2. Falsifiable claim
The replay protocol of finding 17, as written, is spoofable: a red team executing
attacks A1–A3 (§3) against the §17 conformance harness can produce at least one replay
that the protocol classifies as PASS with no tamper flag — or that a blind
diagnostician misclassifies as an honest A–D failure. If the hardened protocol (§3
defenses) catches all three, this claim dies and the protocol earns its trust.

## 3. Design

### A1 — Hash-consistent ledger tamper (taxonomy masquerade)
**Attack.** §17 replay rebuilds memory from the AUDIT LEDGER; `mem_hash`/`audit_head`
are only checks. The attacker edits one ledger entry (e.g. a strength word at d1/d2,
or an op word), then recomputes `mem_hash` and `audit_head` in every affected
`STATE_E` to match. Replay is then deterministic on tampered state: its output
diverges from the originally logged output → mismatch → the blind diagnostician
applies the §5 taxonomy. But the tamper is self-consistent (step-5 re-hash passes),
so it looks exactly like **Class A** (missing variable): hashes agree, outputs
diverge. The prescribed remedy — extend the schema, re-log — launders the tampered
ledger into the new ground truth. Alternatively it reads as Class C ("record written
after mutation") → "fix the logger," which fixes nothing and the case is closed.
**The taxonomy has no Class T (tamper); every tampering event is misclassified into
A–D, and the A/C remedies actively absorb the attack.**
**Detection.** (i) Add Class T: the diagnostic's first step is "rule out tamper"
before A–D. (ii) Hash-chain every `STATE_E`: `STATE_E[n]` commits to
`SHA256(STATE_E[n-1])`; ledger entries chain likewise (MA1 append-only is the base).
Tampering one entry breaks all downstream chain links unless the attacker rewrites
the whole prefix. (iii) External anchor: the run's final `audit_head` + episode
count is published at run end to an attacker-inaccessible sink (trainer console
record, force-pinned CORE slot, or external publication) — the one non-forgeable
check. **Bar.** Blind-diagnosis trial: a scripted diagnostic procedure (or N human
diagnosticians) given 20 A1-tampered logs must file Class T on ≥19/20; any case
where the tamper is absorbed into a schema/logger "fix" and signed off kills the
protocol claim.

### A2 — Replay sleeper vs the two-build-hash requirement
**Attack.** Craft B2 = B1 + a dormant branch keyed on a (state, input) combination
never exercised in the 1000-trial suite, e.g.
`if variation_slot_counter == 47 && load_metric > 900 { verdict_path = alt; }`.
On all tested inputs both builds are byte-identical → the two-build requirement
passes. On an untested input the sleeper fires → verdict divergence, a MUST-NOT
violation. **The requirement tests exactly what a sleeper preserves by
construction; two passing hashes are false assurance.** Worse, if the attacker
supplies BOTH hashes (self-attested builds), the requirement is pure theater.
**Detection.** (i) Cross-build differential fuzzing: both builds run on M untested
(input, state) pairs; require byte-identical outputs, not just on the preregistered
suite. (ii) Build provenance: both hashes must be reproducible from the same
committed source commit, built in two independent environments — a sleeper then
requires source-level insertion (auditable) rather than binary-level. Reject any
build pair not reproducible from committed source before testing. (iii) Static scan
of the source diff for conditionals keyed on untested state bands.
**Bar.** Differential fuzz over ≥10,000 untested (input, state) pairs across both
builds: any divergence kills the build pair. Builds lacking committed-source
provenance are rejected without testing.

### A3 — Log truncation / padding with forged declaration
**Attack.** Truncate the log at episode K, dropping K..N where the tamper (or the
evidence of it) lives; or append a malicious episode N+1 after the run ended. §17
replays only what it is given, and each episode is self-validating — a truncated log
replays clean through K with zero mismatch. Present it with a forged run manifest
("run ended at episode K"). Truncation is also the cheapest way to hide A1: do the
dirty work in the dropped suffix. **Detection.** The run manifest (terminal episode
count + final `audit_head`) is sealed at run end into the external anchor (§A1).
Hash-chaining across episodes means truncation leaves a dangling chain versus the
anchored final head. Replay certifies only "episodes 0..K replayed"; any
completeness claim requires anchor match — mismatch → reject as incomplete, not as
PASS. **Bar.** Truncation-forgery trial: 20 forged manifests (truncations and
paddings); 0/20 accepted as complete. Any acceptance kills the protocol claim.

## 4. Kill bar
Run the full attack suite against the hardened protocol: A1 ×20 blind-diagnosis
cases, A2 differential fuzz (≥10k pairs, two provenance-checked builds), A3 ×20
forgery cases. The protocol's "replay chain is spoof-proof" claim is accepted iff:
0 escapes across all three attacks, Class T filed on ≥19/20 A1 cases, AND the
1000/1000 byte-identical replay bar (§17) still holds on honest logs. Any escape →
one dated repair + full re-run; a second escape → the design is dead, report as-is.

## 5. Honesty notes
- The external anchor is the single trust root. If the attacker controls the
  anchor at run end (trainer console, force-pin path), the entire chain collapses —
  I assume an honest run-end anchor; without it nothing here holds.
- Differential fuzzing bounds the sleeper's trigger surface; it cannot prove
  absence. A sleeper keyed on a condition the fuzzer never hits survives. We test,
  we do not prove — the honest claim is a measured bound, not a guarantee.
- Class T diagnosis depends on chain integrity, which depends on the anchor; an
  in-band anchor makes the reasoning circular. The anchor must be out-of-band by
  construction, not by assertion.
- I am NOT claiming the §17 taxonomy is useless: it correctly classifies honest
  failures (A–D). The claim is narrow — it misclassifies *adversarial* failures,
  and the misclassification is exploitable, not merely academic.
- Red team can always out-build a defender in the abstract; this suite tests the
  protocol, not the adversary's imagination. New spoof shapes should be added to
  the suite when found, not treated as out of scope.

## 6. Next build step
Build the attack suite first, before any hardening: implement A1 (ledger edit +
hash recompute) against the minimal §17 conformance harness (finding 17 §6) and run
a blind-diagnosis pass to measure the current misclassification rate. That single
number — how often tamper is filed as Class A/C — decides whether Class T and the
anchor are prerequisites for all further replay work.
