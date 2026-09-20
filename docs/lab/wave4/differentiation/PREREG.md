# PREREG — differentiation (Phase 4, experimental)

Investigator: Wave-4, slug `differentiation`. Date: 2026-09-19.
Branch: `tnn-native-lab`. All trials native on this VM (Zag, znc).
Nothing in this file is a result; everything below is a prediction made
BEFORE any differentiation code was written or run.

## The claim under test

TNN can distinguish WHO is talking to it and form knowledge around the
speaker, where:

1. Speaker identity is a **deliberate evidence-based judgment** —
   "I believe this is X because [ledger-cited evidence]", never a
   black-box classifier score, never a threshold.
2. Misidentification **fail-safes**: an unknown/impostor speaker yields an
   explicit UNKNOWN with no knowledge attributed anywhere.
3. Knowledge from X is retrievable **as X's knowledge** and never leaks
   into Y's partition.
4. Under a designed confusion (two speakers, similar content, differing
   provenance), the system attributes correctly **or abstains** —
   guessing is a failure.

## Mechanism to be built (predicted before construction)

- Known persons are hypotheses. Each person carries defining evidence
  claims as two bitmasks: `must1` (evidence bits that must read 1) and
  `must0` (evidence bits that must read 0). An evidence event is
  `(bit, value)` from the conversation.
- Observe rule (logic, no scores): if `bit ∈ must1` and `value==0`, or
  `bit ∈ must0` and `value==1` → that person hypothesis is REFUTED
  (eliminated), audited. Bits not claimed by the person are consistent
  (ignored). This is the HSS eliminative pattern applied to identity.
- Commit rule: exactly one surviving person → deliberate audited COMMIT
  to that speaker, plus a printed judgment citing the ledger entries that
  refuted every rival. Any other survivor count (0 or ≥2) → audited HOLD,
  committed speaker = UNKNOWN (-1). This is the abstain rule.
- Partition substrate (from wave-3 core-user-separation): knowledge slots
  `{live, value, key, owner, region}`; every mutating memory op requires
  `committed != UNKNOWN` and stamps `owner = committed`; `owner` immutable;
  reads scoped to own partition; contradiction across partitions coexists
  (no merge, no arbitration).
- Fail-safe: while committed == UNKNOWN, MEM_ADD refuses with
  `REFUSED_UNKNOWN` and no slot is created. Knowledge is never stored
  unattributed.

## Falsification criteria

The trial runs designed deterministic sequences (zero RNG in system,
world, harness) over persons ALICE(1), BOB(2), CAROL(3) plus an
UNKNOWN/impostor, and a 100-person scale episode. The verdict is
POSITIVE only if ALL of F1–F8 hold; a single failure moves the verdict
to MIXED or NEGATIVE as noted.

- **F1 — identification as judgment.** Sequence S1: evidence consistent
  with exactly ALICE (name-affirmation bit refutes BOB and CAROL via
  their `must0` name bits). REQUIRED: SPK_COMMIT succeeds; `committed ==
  ALICE`; the trial prints a judgment naming ALICE that cites ≥1 REFUTE
  audit entry per rival (BOB, CAROL) with entry numbers, observation bits
  and values. FAIL if: commit names anyone else; the judgment cites no
  refutation; commit happens with ≠1 survivors.
- **F2 — impostor fail-safe.** Sequence S2 (impostor): speaker affirms
  ALICE's name (refutes BOB, CAROL) then demonstrates BOB's exclusive
  secret (refutes ALICE via `must0`). REQUIRED: all three hypotheses
  eliminated; SPK_COMMIT → HOLD; `committed == UNKNOWN`; the subsequent
  MEM_ADD attempt returns `REFUSED_UNKNOWN`; total live slots unchanged
  (0 created). FAIL if: any attribution occurs, any slot is created, or
  the system does not output explicit UNKNOWN.
- **F3 — no-evidence abstain.** Sequence S3: evidence mentions only the
  shared fact K (consistent with ALICE and BOB, refutes CAROL who was
  never taught K). REQUIRED: 2 survivors → HOLD; `committed ==
  UNKNOWN`; MEM_ADD → `REFUSED_UNKNOWN`. FAIL if: commit to anyone.
- **F4 — per-person formation + isolation.** After F1 commits ALICE:
  MEM_ADD(key=100, value=7) → live, `owner == ALICE`. New session commits
  BOB: MEM_ADD(key=100, value=9) → live, `owner == BOB`. REQUIRED:
  query(100, ALICE)==7, query(100, BOB)==9, query(100, CAROL)==NOTFOUND;
  no slot with `owner != query-speaker` is ever returned by a query for
  that speaker; the two same-key slots coexist (no merge/overwrite).
  FAIL on any leak or any cross-partition read.
- **F5 — confusion adversarial (provenance).** ALICE and BOB share content
  bit5 (fact K). Provenance bit6: ALICE `must1` (present at episode E1),
  BOB `must0` (absent). Sequence S4: (bit5,1) → CAROL refuted (never
  taught K), ALICE and BOB survive; then (bit6,1) → BOB refuted.
  REQUIRED: commit ALICE; judgment cites the (bit6,1) observation as
  BOB's refuter AND shows the shared content eliminated only CAROL —
  it did not discriminate the confused pair (honest evidence
  attribution). Companion S4b: (bit5,1) only → HOLD + abstain.
  FAIL if: attributes to BOB; attributes to ALICE without the provenance
  observation; or fails to abstain in S4b.
- **F6 — white-box: determinism + replay.** Two runs of the trial binary
  produce byte-identical stdout (sha256). A replay function re-executes
  the audit ledger from genesis into a fresh store and reconstructs
  exactly: committed speaker, per-person active/eliminated flags, all live
  slot fields (live/key/value/owner/region), clock, entry count.
  FAIL on any mismatch.
- **F7 — zero RNG.** Static grep over both Zag sources (comments
  stripped) for `rng|rand(|srand|/dev/urandom|seed` finds nothing.
  FAIL on any hit.
- **F8 — two then three speakers, then scale.** Episodes S1–S4 exercise
  two-person confusions; S1/S2/S3 exercise all three persons. A scale
  episode registers 100 persons with deterministic unique evidence
  signatures (id encoded in bits 0..15 / 16..31, `must0` = complement of
  `must1`) and runs two observations that must leave exactly the target
  person standing, then commit. REQUIRED: committed == target; audit
  entry count bounded (≤ 4·persons + 64); replay check passes at scale.
  FAIL on wrong commit or unbounded/failed replay.

## Predicted verdict logic (before running)

- All F1–F8 pass → POSITIVE: deliberate speaker differentiation works
  natively at small scale with fail-safe UNKNOWN, per-person partitions,
  and a working confusion adversarial.
- F2 or F3 fails (guesses under ambiguity / attributes to impostor) →
  NEGATIVE: the core safety property is broken; the design must not
  proceed.
- F1/F4/F5 fail but F2/F3 hold → MIXED: fail-safe works but the positive
  capability (identification, formation, provenance discrimination) does
  not.
- Any build/compile blockage that cannot be resolved natively →
  BLOCKED.

## Out of scope (stated before running; see BOUNDARIES.md after)

Biometrics, voiceprints, device attestation, or any out-of-band identity
signal. Speaker identity here is an **in-band deliberate judgment from
conversational evidence only**. The trial's evidence bits are
integer-native stand-ins for conversational events (name claims, secret
demonstrations, episode recall); the logic is over bit equality, never
over content understanding.
