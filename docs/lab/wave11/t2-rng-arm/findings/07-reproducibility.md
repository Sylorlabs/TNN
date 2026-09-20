# Slice 07 — Reproducibility from logged state (Arm B, fenced seeded RNG)

## Slice
Arm B reproducibility contract: "RNG" never means unrepeatable — the seed schedule is logged
state, so input + logged state (incl. seeds) replays Arm B byte-identically.

## Falsifiable claim
Across 50 replay passes of every Arm B trial episode (fixed binary, identical input,
identical logged seed schedule), all outputs, audit entries, and ledger contents are
byte-identical to the original run. If any replay pass diverges on any byte, the
reproducibility claim is dead for that trial — the trial's B-vs-C comparison is void.

## Design
**Seed schedule.** One master seed per trial, logged once at trial start. Every draw site
prereg-enumerated by the fence gets a deterministic stream: `stream_seed = splitmix64(master_seed ⊕ site_id ⊕ episode_idx)`.
No draw may consume from any other stream; no stream is shared between sites. PRNG is a fixed
xorshift128+ implementation vendored in the repo (never libc `rand`, never OS entropy).

**Seed log format.** One append-only JSONL file per trial, `seedlog.jsonl`, plus a SHA-256
hash-chain field per line (each line hashes the previous line's hash + its own payload):
```
{ "seq": 0, "event": "master_seed", "value": "u64 hex", "hash": "..." }
{ "seq": k, "event": "draw", "site": "<fence-enumerated site id>", "episode": i,
  "draw_idx": j, "stream_seed": "u64 hex", "value": "u64 hex", "hash": "..." }
{ "seq": m, "event": "trial_end", "total_draws": D, "hash": "..." }
```
The ledger cross-references `total_draws` so a missing or truncated seed log is detectable
without opening it.

**Replay procedure.** The replayer: (1) reads input trace + full logged state + seedlog;
(2) verifies the hash chain and that every draw site in the fence manifest has matching
entries; (3) re-executes: before each draw, reseeds the site's xorshift128+ stream to the
logged `stream_seed`, performs exactly the logged number of draws, and asserts each drawn
value equals the logged `value` before the value may influence execution; (4) byte-compares
final outputs, audit trail, and ledger against the original artifacts. Replay is a pure
function of (input, logged state, seedlog) — it never calls the OS for entropy.

**Test.** 50 replay passes per trial (the N=50 from the claim): original run + 49 replays
across at least two machines where feasible. Byte-compare all artifacts every pass.
Additionally, replay episodes in shuffled order to catch cross-episode stream leakage.

## Kill bar
- K1 (fatal): any replay pass produces any byte of divergence in outputs, audit, or ledger.
- K2 (fatal): any draw consumed at runtime with no corresponding seedlog entry, or any
  seedlog entry for a site not on the fence manifest — the fence leaked.
- K3 (fatal): any replay failure of any kind in Arm B → that trial's B-vs-C comparison is
  **void, not lost**: Arm B is scored as INVALID for the trial, Arm C keeps its score, and
  the trial is reported as a non-result for B-vs-C. No salvage by re-averaging.
- K4 (advisory): replay succeeds but requires ≥1 manual intervention per pass (missing
  artifacts, undocumented steps) — the contract is not machine-checkable.

## Honesty notes
- This contract assumes the xorshift128+ implementation is bit-stable across compilers and
  platforms; if a platform's codegen alters bit behavior, that is a toolchain defect, not a
  vindication of RNG-in-the-mind — K1 still fires and the trial is void.
- The seed log is a *claim* about what happened, not an independent witness: a logging bug
  that writes fabricated seeds which then "replay" correctly would pass the byte-compare but
  be detected only by the draw-assert step (value must be re-derivable, not just equal).
  Keeping the assert inside the execution loop, not post-hoc, is load-bearing.
- OS entropy (rdtsc, gettimeofday, /dev/urandom, address-space layout) can sneak in via
  third-party code: the fence manifest must be enforced by a syscall audit (seccomp-style
  allowlist review), not by convention.
- We do NOT claim Arm B is *as good* as Arm C; this slice only secures the comparison's
  validity. A reproducible loss is a clean loss.

## Next build step
Build the minimal fenced draw-site harness: vendored xorshift128+, the JSONL hash-chained
seed logger, the reseeding replayer with per-draw asserts, and the byte-compare test over
a 100-episode synthetic trial with 3 prereg-enumerated draw sites — then run the full
50-replay protocol once end-to-end before any real Arm B experiment consumes it.
