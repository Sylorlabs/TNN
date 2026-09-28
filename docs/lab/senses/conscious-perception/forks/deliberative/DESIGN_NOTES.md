# F2 DELIBERATIVE — design notes

Pure-Zag two-pass perception fork. Built 2026-09-24 under frozen
`conscious_perception/preregs/PREREG_FORKS.md` (do not amend).

## The core finding it implements

Both debate sides eliminated "autopilot sensing + conscious gate": once lossy
preprocessing destroys raw evidence, rerunning the same deterministic decoder
cannot recover it. So F2's consciousness chooses sampling **before** irreversible
preprocessing. Pass 1 is not "the old autopilot" — it is a *declared* sampling
policy whose loss bounds are written to the ledger (P1_PLAN) before any sample
is taken. Pass 2 re-samples the *raw stimulus* the plan retained.

## Pass 1 — declared, bit-exact F1

`src/f1.zag` is a bit-exact Zag port of the frozen F1 reference
(`forks/autopilot/gen/ref_f1.py`): identical labels, confidences, detail ints,
and op counts on all 26 shared fixtures (verified by `t1.zag` driver diff).
Pass 1 in F2 is therefore a perfect F1-proxy: any F2-vs-F1 delta is pure
deliberation gain, not an implementation drift.

Declared loss bounds (P1_PLAN, ledgered before sampling):
- PITCH: blind to late-B events (only first 2048 of each 8192 half examined);
  20,000 ppm gate.
- TIMBRE: blind post-sample-2048; hp1000 thresholds 67/82/110.
- COLORDISC: sub-40-unit distances collapse to SAME.
- COLORCONST: single-pixel spike corrupts the white-patch illuminant;
  discount-identical surfaces collide.
- MOTION: global brightness centroid on frames 0,7 only — a large dim
  distractor dominates; a small bright target is invisible.

## Pass 2 — changed evidence only

Selectors per task (ids 10..13; 1=pass-1, 2=background):

- PITCH: LATE_B[14336:16384), MID_B[10240:12288), FULL_B[8192:16384),
  LATE_A[6144:8192) — new windows, same zero-cross decoder.
- TIMBRE: POST[2048:4096), LATE[4096:8192), FULL[0:8192).
- COLORDISC: TOP rows, BOTTOM rows, CENTERBAND x∈[16,48) (new regions,
  same decoder); ALTDEC (same halves, different decoder: per-channel max
  abs diff vs 40).
- COLORCONST: ROBUST (second-max illuminant — spike-immune),
  ABSOLUTE (no discount at all), CONSENSUS (disjunctive).
- MOTION: BRIGHT_TRACK frames 0..7 / 1..6 (different frames AND different
  decoder: bright-cluster tracking vs global centroid).

Same-evidence reruns are structurally impossible: a used-selector bitmask is
checked before every acquisition, and every acquisition's evidence bytes are
SHA-256-hashed into the ledger (P2_ACQ). Re-examining an already-used selector
cannot happen; the loop simply ends.

## Triggers (frozen table, evaluated on the current percept)

1. UNCERTAIN — confidence < 250.
2. COVERAGE — high-stake task (PITCH, MOTION) with zero deliberate
   acquisitions yet.
3. GOAL — MOTION whose evidence is not bright-target tracking.
4. DIVERSITY — COLORCONST without an absolute-decoder acquisition yet.
5. BG — background interrupt (consumed after the first round).

## Budgets and the circuit-breaker (deterministic)

- MAX_ACQ = 6 deliberate acquisitions per trial. The loop condition
  `trigger != NONE && acq < MAX_ACQ` provably terminates.
- Op deadline: per-trial op cap (default 100,000; argv[3]). Before each
  acquisition the estimated cost is checked; exceeding the cap raises BUDGET
  and stops deliberation.
- On exhaustion: CAPTURE is ledgered (`pinned=1, past_budget=0`) and the
  install proceeds as PROVISIONAL — never a refusal, never silence.

## Install-time verification (high stakes: PITCH, MOTION)

After deliberation, if the install is assertive (no provisional flags,
conf ≥ 250), one verification round runs with a FRESH unused selector
(independent evidence), depth-bounded by a counter (MAX_VERIFY_DEPTH = 2;
one round is used in practice). Agreement → VERIFIED. Disagreement, no fresh
selector, or deadline → PROVISIONAL. Low-stake assertive installs are DIRECT.

## Authority tiers

- VERIFIED — high-stake, fresh-evidence confirmation agreed.
- DIRECT — low-stake, assertive, no disagreement.
- PROVISIONAL — any of: uncertainty seen (min conf < 250), decoder
  disagreement, verify skipped/failed, budget/deadline hit. Always installs;
  always flagged.

## Background channel (interrupt-only)

`bg_scan` returns only `(fired, hint, ops)` — its return type carries no
percept label, so it *cannot* install by construction. It is a cheap strided
scan: pitch quarter-frequency spread, timbre late-brightness, colordisc
near-boundary, colorconst max-pixel-count spike check, motion bright-cluster
presence. A fire wakes deliberation (INTERRUPT ledger entry); deliberation
then re-senses with full evidence.

## Objection answers

- **Irreversibility.** The sampling policy and its loss bounds are declared
  in P1_PLAN *before* sampling. Pass 2 samples the raw stimulus — the plan
  retains it — not the destroyed summary. Demonstrated: om_p1/om_p2
  (late-B pitch events invisible to pass 1) recovered via LATE_B windows.
- **Attention capture.** Hard acquisition budget (6) + op deadline +
  used-selector mask; the deliberation loop provably terminates. Measured:
  0 trials pinned past budget at the 100k cap (past_budget=0 everywhere);
  at a 30k cap, 4/26 trials pinned (budget stopped them) — all ledgered as
  CAPTURE with provisional installs. The redteam budget-burners (rt_c1,
  rt_p1) burned 4 acquisitions each and stopped at the mask, not the budget.
- **Verification regress.** Verification depth is machine-bounded (counter,
  max 2). The verifier is the *same deterministic decoder* on *fresh
  evidence* — not a new agent that could itself need verifying. The
  high-rate leg shows verification meeting the deadline at 100k ops, and the
  graceful provisional fallback at 30k/50k caps.

## Known limitation (from the debate, open problem E1)

F2 does not solve all commission-class decoder fooling: inputs engineered to
sit exactly on a decision boundary (rt_c1: distance 39 vs gate 40; rt_p1:
18,181 vs 20,000 ppm) defeat every window/decoder tried. Both misses are
provisional-flagged (min-conf < 250), never assertive. This is the honest
boundary of the design, not a bug.

## Determinism

Zero RNG in any decision path. No timestamps, no pointer-derived values, no
hash-map iteration anywhere in the pipeline. Verdict and ledger bytes are
identical across runs (4/4 battery runs byte-identical; 26/26 ledger hash
chains verify).
