# Slice 11 (Track 3 red-team) — Corrupted-state verdict-flipping vs Slice 22

## 1. Slice
Track 3, slice 11: red-team attack on Slice 22's claim that corrupted variation state degrades
to NULL variation and can never flip a verdict, because checks run at the render gate.

## 2. Falsifiable claim
Within Slice 22's own stated threat model (external-input influence, internal bugs, bad
writes — explicitly NOT requiring arbitrary internal write access), there exists at least
one of: (A) a fault injected strictly before the verdict is sealed that changes a verdict,
integrity refusal, memory decision, or ledger byte while the render gate later reports
mask = 0 or its NULL-degradation fires too late to matter; (B) a single crafted fault that
passes checksum AND range AND cross-variable consistency while changing rendered output
vs control; (C) a two-fault pair defeating all three checks where each fault alone is
caught. Any one of A/B/C firing kills Slice 22's "100% detection / worst case is boring
phrasing" claim as specified.

## 3. Design — the attacks
**A1. The upstream window (strongest).** Slice 22's detector runs once, at the render gate,
after verdicts are sealed. But two Track-1 variables are verdict-path by construction:
load L has a *refusal floor* (Track 1 synthesis: "load L integer-only with monotone 4-tier
mapping and refusal floor"), and budget bounds deliberation depth — how long TNN thinks
before deciding. A bit-flip on load (1→4) injected pre-deliberation flips the refusal
decision; the render gate later flags corruption and degrades to NULL variation, but the
refusal already flipped — degradation cannot un-flip it. Worse, Slice 22's `render_gate`
does not even enumerate load: no load check exists in the pseudocode. Either load is
verdict-path (separation invariant false) or load is unprotected (detector incomplete).
Also note the invariant is mis-stated: `variation_read_set ∩ verdict_write_set = ∅`
constrains variation reading verdicts; the needed invariant is
`verdict_read_set ∩ variation_write_set = ∅` — as written it does not protect verdicts.
```
attack_A1(s):  s.load = 4                    // pre-deliberation, single word flip
               run_deliberation()             // refusal floor trips -> REFUSE
               m = render_gate(s, L)          // mask != 0, NULL variation
               assert refusal != control.refusal   // verdict-path change, gate too late
```
**A2. Forged checksum (single fault).** `fnv1a` is 32-bit, non-cryptographic: collisions
are forgeable offline (~2^16 structured variants via birthday search on padding bytes).
Craft segment S' != S with fnv1a(S') = fnv1a(S), values in range, sum-to-1.0 preserved,
watermark fresh. One write passes all three checks and drives non-NULL variation from
attacker-chosen state. The 10,000-trial suite's "checksum-only rewrites" class never tests
collision-forged segments, so its 100% figure is vacuous against this fault.
**A3. Two-fault metadata kill.** The checks are not independent: each check trusts
uncorrupted metadata. Pair (fault-1, fault-2), each caught alone, jointly missed:
(i) freeze the writer (stuck-at old salience) + rewrite `s.updated_ep[i]` to current
clock — checksum valid (genuinely old values), range valid, staleness check passes
(watermark fresh; watermarks are NOT checksummed); (ii) corrupt variable word + corrupt
`VAR_TABLE[i].hi` to match — the table itself is never checksummed; (iii) corrupt
variable + corrupt `L.clock` so the staleness horizon never elapses. Any pair yields
mask = 0 with semantically wrong state driving output.
**A4. Lawful-wrong write (internal bug, single fault).** Slice 22's threat model claims
internal bugs. A bug in the single lawful writer emitting in-range, cross-consistent,
freshly-watermarked but semantically inverted values (e.g., salience sorted ascending)
passes checksum (writer recomputes it), range, and cross-checks — the honesty note
concedes "checksums catch bad writes, not lawful-looking bad values," which concedes
exactly the claimed threat model.
**A5. Post-gate gap.** The honesty note admits corruption after the gate but before
rendering is missed, "which the builder must guarantee, not assume" — a check whose
correctness depends on an un-verified builder guarantee is not a proven mechanism.

## 4. Kill bar
Build the attack harness against the Slice-22 reference gate in Zag and fire the design
if ANY of: **K-RT1** — any pre-seal fault on load/budget/salience changes a verdict,
refusal, memory op, or ledger byte vs the fault-free control (gate mask irrelevant);
**K-RT2** — a collision-forged fnv1a segment passes checksum+range+cross-consistency and
produces non-NULL variation output differing from control; **K-RT3** — any fault pair
from {(frozen writer, forged watermark), (var word, table bound), (var word, clock)}
yields mask = 0 with output differing from control; **K-RT4** — a writer-bug emitting
lawful-looking wrong values passes all checks. One firing = Slice 22's claim dead; the
10,000 single-fault trials do not need re-running to establish this — they test a fault
model that excludes the killing faults by construction.

## 5. Honesty notes
I am NOT claiming an external-input-only attacker can flip verdicts end-to-end today:
A2/A3 need a bad-write or stuck-at primitive, which is the internal-bug half of Slice 22's
own threat model, not the external-input half. A1 is the exception — load/budget are
input-influenced (long inputs push budget; load tracks input complexity), so a crafted
input plausibly nudges load across its refusal floor with zero writes at all; I have not
proven the nudge is reachable, only that the coupling exists by Track 1's own spec. The
fnv1a forgery needs offline compute and a write primitive; I am not claiming it is
remotely triggerable. I am not disputing that NULL-degradation works when the gate
actually fires — I am claiming the gate is misplaced (downstream of verdict use),
mis-stated (wrong invariant), incomplete (load unenumerated), and checkable-only
(fnva32, unchecksummed metadata). Fixing all four is a redesign, not a patch.

## 6. Next build step
Before any builder trusts Slice 22, implement the four attacks as a red-team harness in
Zag against the literal `render_gate` pseudocode: A1 with load 1→4 pre-deliberation and
a refusal-floor assertion vs control; A2 with a real birthday-forged fnv1a collision
segment; A3 with the (frozen-writer, forged-watermark) pair. If any attack fails to fire,
the failure itself is evidence about which coupling to cut — but a harness that cannot
even express these faults is not testing the claim.
