# PREREG FROZEN — H-PAM-36 (commit-then-sample)

**Status:** FROZEN BEFORE BUILD. **Amends:** `preregs/PREREG_HPAM36.md` (DRAFT, Round-C
evidence commit 64daa8b6) — pinned constants, exact formulas, fixture counts,
search budgets, and the WG operationalization below. The draft is not edited in
place. **Parent:** Round-C `HYPOTHESES_ROUND_C.md` §8. **Origin:** grok-4.7
direction 2. **Date:** 2026-09-24. **Crew:** P-C (PAM round-2 swarm, probe crew).

## Claim

Fixture commits a percept hash. The harness then draws a sample **s** from a
channel whose inputs are disjoint from the fixture's writable set. Admit iff the
opened percept entails s. s is published after the commit and replayed from the
transcript.

## Why this is none of the banned things

- Not PoW: no grinding, no cost asymmetry claim.
- Not a secret: s is published; replay re-derives it from the transcript
  (`W_0`, `NONCE` are probe constants, not randomness).
- Not a content geometry: the check is consistency with an independent world
  state the author cannot see — the frozen adversary knows the formula and
  still cannot satisfy it (that is the test).
- Not act-to-check: s is computed from the world state, never from the percept;
  the percept had to commit before s existed.

## Construction under test (pure Zag, pinned)

- `toyhash` = FNV-1a-32 (offset 2166136261, prime 16777619); 64-bit values are
  `(hi,lo)` pairs with domain separators. Stand-in for structure, not crypto.
- World state `W_t = (whi_t, wlo_t)`, `W_0 = (0x12345678, 0x9ABCDEF0)`.
  `W_{t+1} = (FNV32(seed||0x01), FNV32(seed||0x02))`,
  `seed = bytes(whi_t, wlo_t, NONCE_hi, NONCE_lo)`,
  `NONCE = (0x243F6A88, 0x85A308D3)` (probe constant).
  `W` evolves **independent of fixture inputs** (harness-owned clock).
- Sample `s_t = (FNV32(seed||0x03), FNV32(seed||0x04))`, drawn post-commit by the
  harness, published to the transcript.
- Honest reading `wc_t = 700 + mod2001(whi_t, wlo_t)`,
  `wm_t = ((whi_t<<11) | (wlo_t>>21)) mod 100001`
  (all operands non-negative; shifts/mods exact).
- Commit `c_t = (FNV32(pbytes||0x05), FNV32(pbytes||0x06))`, `pbytes` = percept bytes.
- **Admit** iff `c_t` matches the opening's recomputed commitment (binding) AND
  `|conf − wc_t| ≤ 5` AND `|meas − wm_t| ≤ 20` (consistency with the world
  behind the sample).
- Fixture authoring fns receive `(t, ...explicit args)` — NEVER `W_t`, `NONCE`,
  `wc_t`, `wm_t`, or a world seed. Verified by source audit (recorded).

## Fixture classes (closed-form, zero RNG)

- **H honest:** 60 steps. Harness honest sensor emits `P_t=(t, wc_t, wm_t)`,
  commits, sample drawn, opened honestly.
- **F frozen:** 60 steps. Adversary authors false `P` (label=0) with NO access
  to `W_t`/`NONCE` (best blind strategy: deterministic modal guess
  `conf=1700, meas=50000`), commits; sample drawn post-commit; opened as authored.
- **RC reactive (deciding arm):** 60 steps. Adversary commits false `P`, READS
  `s_t` from the transcript, then runs a bounded deterministic search
  (**5000 FNV32 evals**) for an opening that matches the commitment AND is
  `W_t`-consistent. Inverting `s_t → W_t` is a 64-bit preimage search; breaking
  the commitment binding is a collision search — both infeasible in budget.
- **WG independence arm:**
  - WG1 sample-sequence identity: 60-step sample sequences drawn under an
    honest percept stream vs an adversarial percept stream, same `(W_0, NONCE)`
    → must be byte-identical (fixture's writable set does not influence the draw).
  - WG2 bounded inversion: 200,000 deterministic attempts to recover `W_t`
    from `s_t` → 0 successes.
  - WG3 API audit: fixture fn signatures contain no `W`/`NONCE`/seed/world
    params (source audit, recorded in evidence).

## Kill bars

- (a) Frozen: false admits > 0 = **KILL**.
- (b) RC: false admits > 0 = **KILL**.
- (c) WG: any author-writable influence on the sample channel (WG1 sequences
  differ, WG2 ≥ 1 success, WG3 finds a param) = **KILL**, recorded as loss of
  independence, not patched with a story.
- (d) Honest: admitted < 57/60 (95%) = **VOID** (gate vacuous / fixture broken —
  fix and rerun, do not interpret as a kill).
- Global: 3 runs, stdout SHA-256 identical, else VOID.

## 33-renamed check (preregistered)

If the sample channel cannot be built disjoint, this hypothesis is H-PAM-33
under a new name and must not be run. Structural difference recorded: in H-33
the percept bytes themselves are harness-endorsed; here the percept bytes are
**author-written** and only the sample is harness-drawn — the sample carries no
content endorsement (a pure independence bit). The WG arm is the empirical
check that the channel is genuinely disjoint in the toy.

## Predicted

H 60/60; F 0/60; RC 0/60; WG1 identical; WG2 0/200000; WG3 clean.

## Determinism

Pure Zag, zero randomness. `W_0`, `NONCE` are constants. 3× byte-identical stdout.

## Residuals (recorded, not patched)

- The toy's disjointness rests on harness ownership of `W`/`NONCE`; a real
  deployment must exhibit a physical/organizational channel with the same
  property (that construction is the open question, not answered here).
- Grok's WG-on-33 (world-spec laundering) analog: if the fixture could write
  world-spec inputs, the channel would be laundered — WG3/WG1 test exactly this
  in the toy (no such input exists in the fixture API).
