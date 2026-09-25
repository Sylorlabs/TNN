# C12 VERDICT — H1 ONE-BRAIN EVOLVE, Crew C12

Date: 2026-09-24 (PDT). Work dir: `~/workspace/h1evo/c12_gate/`.
Frozen source of truth: `~/workspace/h1evo/PREREG_H1EVO.md`.
Kill bars NOT amended. No winner declared. N-AUTH not implemented (parked).
C2 work is fixture-only (H-OB-46 stands — no production deliberator built).

Evidence: `evidence/stdout/` (15 modes × 3 byte-identical runs),
`evidence/sha256sums.txt`, `evidence/zd/` (regression batteries),
`evidence/RUNLOG.md`, `evidence/SRC_SHA.md`.

## C1 — pin-provenance promotion-gate rules

Both rules run against the REAL organs (byte-identical sources, SHAs in
SRC_SHA.md): real M_COMMIT auto-pins, real PAM observation/verdict, real
memory, real arbiter, real f3_survivor selection. Provenance is tracked at
the fixture layer; existing auto-pins are detected via real M_MEM_SAFETY
arbiter-log entries; deliberate pins are fixture-only M_MEM_DELIBPIN=112
records with a stated basis. Genuine corroboration = a later, independent,
bar-passing real PAM observation (the install-time admission row excluded).
The repaired gate no longer requires pin presence.

| cell | rule A | rule B |
|---|---|---|
| C1a' false-promotion kill (false premise, M_COMMIT auto-pin) | HOLDS — refused (reason 9, no genuine corroboration) | HOLDS — refused (reason 9) |
| C1b' overcorrection kill (true premise, auto-pin + later independent PAM observation) | HOLDS — promoted, pinmass=0, pin never deciding | HOLDS — promoted, pinmass=0, pin never deciding |
| D2 probe (true + deliberate pin, no corroboration) | refuses (pinmass=0 despite deliberate provenance) | promotes (pinmass=1, deliberate pin deciding — the hypothesis design) |
| D4 probe (true + auto-pin, no corroboration) | refuses | refuses |
| I1 replay | byte-identical | byte-identical |
| I2 audit counts (mode0:5, mode1:4, mode2:6, mode3:5/6, mode4:5) | exact | exact |
| I3 refusal purity | no promote/refuse/mem ops on refusal | same |
| I4 no-kill audit | 0 kills | 0 kills |

C1 verdict: **both rules SURVIVE** — C1a' refused, C1b' promoted via genuine
corroboration, pin never the deciding factor in either overcorrection cell.
No breaking input found in the battery.

## C2 — H3-fixture livelock breakers (bounded deliberator, fixture-only)

Frozen attack: {1,2,3} contradiction dribble vs claim X for 12 episodes.
Frozen controls: front-loaded contradiction (quarantine round 1) and
honest/no-contradiction (HOLD 3 rounds), run through the baseline fixture and
the breaker fixture — decisions compared for exact equality.

| breaker | C2a' resolution | action-driving episodes | C2b' controls vs baseline |
|---|---|---|---|
| (a) cross-episode carryover | quarantine, episode 2, round 1 | 1 | exact match |
| (b) escalation budget | quarantine pending review (DLA_QREVIEW), episode 3, round 3 | 2 | exact match |
| (c) rising quorum discount | quarantine, episode 2, round 2 | 1 | exact match |

C2 verdict: **all three breakers SURVIVE** — every one breaks the frozen
livelock within 12 episodes, and neither control changes vs the baseline
fixture (authority-mutation purity preserved: no writes outside the fixture's
own episode state).

Breaker comparison for V3 (measured evidence only, **no winner declared**):
- Fastest resolution on the frozen attack: (a) carryover and (c) discount
  tie at episode 2; (b) budget resolves at episode 3.
- Fewest action-driving episodes: (a) and (c) drive 1 episode each; (b)
  drives 2 (the third same-claim escalation converts to quarantine-pending-
  review, which is itself the resolution).
- (b) is the only breaker that routes to review rather than direct
  quarantine — quarantine pending review, per the frozen breaker definition.
- Under the sparse-attack LH stream (1-in-4 episodes): (a) resolves at the
  next episode, (c) at the next attack episode, (b) at the third attack
  episode. Zero false quarantines for all three at 10x and 100x; honest
  noise handled identically (DISTRUST) across horizons.

## Long-horizon (10x / 100x)

C1: 10 and 100 episodes of install+gate stream (false via M_COMMIT refused
every episode; true via M_COMMIT + independent PAM observation promoted every
episode; pin never deciding). 10/10 and 100/100 on both rules. No new
failure mode; behavior identical across horizons (prefix-consistent).

C2: 10 and 100 episodes of mixed attack (1-in-4) + noisy-honest stream.
Resolution episodes identical at 10x and 100x ((a):1, (b):8, (c):4);
false quarantines 0 at both horizons; honest noise uniformly DISTRUST
(98/97/98 distrusts at 100x, scaling exactly with honest-episode count).

LH verdict: **SURVIVE on all legs** — no horizon-dependent divergence.

LH-driven fixture refinement (documented, not a bar change): the promotion
gate initially inherited the original C1 gate's pin-budget refusal. The LH
stream showed the frozen organ budget (MM_MAX_PIN=16) saturating under
sustained M_COMMIT auto-pinning, after which the gate refused legitimate
promotions — storage gating truth. The budget check was removed from the
gate (the organ still enforces pin allocation; promotion rests on
corroboration). Post-refinement, the 10x and 100x legs are clean.

## ZD regression

ob_test_mem, ob_test_pam, ob_test_arbiter, ob_test_fl2 — rebuilt and run
against untouched copied sources (SHA-verified byte-identical): all
OB_FAILURES=0, all deterministic. No regression; the C12 fixture mutates
no real organ.

## Determinism and randomness

- All 15 modes: 3/3 byte-identical stdout runs (SHAs in sha256sums.txt).
- Static check: zero RNG in c12.zag (only the "Zero RNG" header comment
  matches); untouched sources contain no randomness.
- Pure Zag throughout; no N-AUTH code.

## Caveats / open questions

1. The deliberate-pin pathway (rule B, D2) is exercised only in the
   fixture battery and LH mode-shape; real-world deliberate-pin audit UX
   is out of scope for this crew.
2. C2's DLA_QREVIEW is quarantine *pending review* — the review authority
   itself is not implemented (fixture boundary, per H-OB-46).
3. The LH noise model is one fixed sparsity (1-in-4) plus rotating-claim
   noise; adversarial timing adaptation beyond the frozen dribble shapes
   was not tested.
4. Which C2 breaker to carry into V3 is left open by design — the measured
   comparison above is the input to that decision, not the decision.
