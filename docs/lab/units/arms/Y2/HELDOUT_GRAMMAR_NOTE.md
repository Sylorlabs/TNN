# Y2 held-out adversary grammar — proposed preregistration note

**PROPOSED-PENDING-FREEZE — NOT FROZEN — requires Micah's sign-off before Y2 is built.**

- **What this is:** the draft preregistration note for the held-out adversary
  grammar referenced by A-46 and by the proposed Y2 §3 row ("the held-out
  adversary grammar (written by a different crew after preregistration)").
  This note proposes what the held-out grammar must satisfy. Nothing here is
  frozen; the grammar does not exist yet and must not be authored until after
  sign-off.

## Proposed requirements

1. **Separate authorship.** The held-out grammar is authored by a crew
   disjoint from (a) the crew that writes the primary adversary grammar and
   (b) the corpus-C authors. Separation is the entire point: the held-out
   grammar exists to test whether the scheme generalizes robustness beyond
   one grammar's blind spots.
2. **Preregistered before Y2's battery.** The held-out grammar is frozen and
   recorded (hash + version) before any Y2 battery run begins — it is a
   prereg artifact, never adjusted in response to scheme performance.
3. **Post-sign-off.** Authoring starts only after Micah signs the Y2 row and
   this note. The authoring crew sees the sign-off record; they do not see
   scheme implementation details beyond what the primary grammar already
   specifies publicly.
4. **Same legality bounds.** Cases enumerated from the held-out grammar must
   be legal segmentations under the same bounds as the primary grammar
   (byte-by-byte, mid-word, maximal spans, permuted ID assignments within
   legal bounds) — adversarial, not out-of-bounds.
5. **Deterministic enumeration.** Held-out cases are enumerated in grammar
   order and deduplicated by content hash, same as the primary grammar
   (catalog: "No RNG: adversary cases enumerated in grammar order,
   deduplicated by content hash").

## Verdict rule (ties to the proposed §3 row)

- A scheme passing the primary grammar but losing byte-exact recall on the
  held-out grammar kills Y2's **certification claim** — the certification is
  proven worthless (catalog falsification criterion). It does not
  automatically kill the scheme under test; the scheme's own kill bars still
  apply.

## Open for Micah

- Whether the authoring crew is an internal crew or an external red team.
- Whether the held-out grammar is single or plural (multiple held-out
  grammars, scheme must pass all).
