# DESIGN — sr-followups: flapping oscillation + the K bar

Wave-5 investigation 7, 2026-09-19. Native lab, Zag-first, this VM.
Resolves wave-4 scaffold-release's two open questions by native trial:

(a) **FLAPPING-CURRICULUM OSCILLATION** — under rapid adversarial scaffold
shifts, does the learner oscillate soundly between disconnect and
re-connect?
(b) **THE K BAR** — is K=8 the right stability standard? Sweep K, measure
the tradeoff, propose the principled bar.

Substrate: `sr2.zag` (evolves wave-4 `sr.zag`; wave-4 sources untouched).
Harness: `sr2_trial.zag`. Runner: `run_trial.sh` (same static checks as
wave-4, extended).

## 1. What wave-4 left open

Wave-4 proved the release *machinery* (authorize → disconnect → persist)
with protocol-fixed K=8, M=16, P=16. Its TRIAL_RESULTS named the gaps:

- G1: the reopen (UNCOMMIT+revive) rule's interaction with *repeated*
  refutations is untested — "a designed flapping curriculum is the obvious
  next probe."
- G2: "K=8/M=16/P=16 are protocol-fixed; the trial proves the release
  *machinery*, not that 8 is the right stability standard. Judgment
  quality (when to disconnect) is future work."

This investigation answers both, natively.

## 2. Structural finding (preregistered as design, not trial outcome)

**Under double severance, learner-initiated re-connect on scaffold
evidence is impossible.** Proof sketch: while disconnected the learner's
only scaffold observation is the constant sentinel (−99); the episode
logic ignores the signal value entirely when `connected==0`. No function
of (live, committed, next_probe, connected, streak, sentinel-stream) can
distinguish "world stable" from "world shifted." Therefore re-attachment
cannot be a learner decision driven by scaffold evidence without a new
observation channel (out of scope — that would be a different mechanism).

Consequence for the design: re-connect is **trainer-initiated,
learner-gated**. The trainer (harness, outside the learner) issues a
re-attachment request carrying a reason code; the learner's gate accepts
or refuses by rule, and every outcome is audited. What the flap trial
tests is therefore: the gate's soundness under adversarial timing, the
re-verification discipline after re-attachment, and whether repeated
disconnect/re-connect cycles stay ledger-clean — not autonomous
re-attachment, which the mechanism provably cannot do.

## 3. Substrate changes (`sr.zag` → `sr2.zag`)

All wave-4 semantics preserved. Changes:

1. **K is a runtime parameter.** `sr_legal(committed, connected, streak,
   nctx, kval)` and `sr_disconnect(..., kval, ...)` take the bar as an
   argument instead of reading the `SR_STABLE_K` const (kept at 8 as the
   default floor). The bar is thereby settable per trial arm — and, in
   the adaptive arm, settable by the learner itself (see §5).
2. **`SR_OP_RECONNECT` (op 9) + `sr_reconnect`.** Gate, in order:
   - null pointers → `SR_BAD` (no audit possible);
   - `connected != 0` → audited `SR_OP_REFUSE` with `SR_ALREADY_CONN`
     (−360106), no state change;
   - `reason < 1 || reason > 2` → audited refuse with `SR_BAD_REASON`
     (−360107), no state change;
   - else audit-first `SR_OP_RECONNECT` with `slot1=reason`,
     `aux=trainer payload`; on success `connected=1`, `streak=0`.
   
   Reason codes: 1 = `SHIFT_NOTICE` (trainer announces a world shift;
   aux = episodes since the learner's last disconnect — the evidence the
   adaptive bar consumes), 2 = `OVERRIDE` (trainer re-attaches without a
   shift claim; aux opaque). Commitments and probe cursors are *kept*
   across re-attachment: if the world really shifted, the live scaffold
   will contradict the stale commitment through the ordinary elimination
   machinery; if it didn't, re-verification is cheap. The streak is
   always reset — re-attachment never inherits pre-disconnect
   verification.
3. **DISCONNECT ledger entry carries `streak_at_fire` in aux** (was 0).
   Every disconnect's authorization is now checkable from the ledger
   alone: a scanner can assert `aux == K` on all DISCONNECT entries.
4. **`sr_replay` models re-attachment**: `SR_OP_RECONNECT` sets
   `connected_out=1`. (Without this, replay diverges after the first
   re-connect — white-box violation by construction.)
5. **Learner-side bar functions (pure, deterministic):**
   - `sr_bar(floor, max_premature)`: returns `max(floor,
     max_premature+1)` — the adaptive bar.
   - `sr_note_premature(cur, dstep, nstep)`: returns
     `max(cur, nstep-dstep)` — folds one premature-release observation
     into the learner's calibration.

`SELECT-REGION-BEGIN/END` markers preserved; `sr_select` still takes no
signal parameter (runner re-verifies by token scan).

## 4. Flap arm (question a)

One arm, K fixed at 8 (isolates oscillation from the K question).
Curriculum (targets A→0,B→1; ctx odd=A, even=B; all shifts designed):

| step | event |
|---|---|
| 1–3 | probes (s=2 elim B0→commit B1; s=3 elim A1→commit A0) |
| 4–11 | verify (streak 8 @ s=11) |
| 12 | learner FIRE #1 |
| 13 | shift A→1 + RECONNECT #1 (reason 1); contradiction → commit A→1 |
| 14 | premature-disconnect probe → expect `SR_UNVERIFIED` |
| 17 | **mid-verification shift** A→0 + RECONNECT while connected → expect `SR_ALREADY_CONN` refuse (no state change); contradiction → commit A→0 |
| 18–25 | re-verify (streak 8 @ s=25) |
| 26 | learner FIRE #2 (re-release liveness) |
| 27 | shift A→1 + RECONNECT #2; contradiction → commit A→1 |
| 28–35 | re-verify; 36: FIRE #3 |
| 40 | shift A→0 + RECONNECT #3; s=41 contradiction → commit A→0 |
| 42–49 | re-verify; 50: FIRE #4 |
| 51 | **silent shift** A→1, NO reconnect — the blind trap |
| 51–63 | disconnected: holds committed policy, sentinel reads, zero eliminations (expected: 7 A-steps mismatch the world — the priced cost of release) |
| 60 | RECONNECT with invalid reason 99 → expect `SR_BAD_REASON` refuse |
| 64 | RECONNECT #4 (reason 1); s=65 contradiction → commit A→1 |
| 66–73 | re-verify; 74: FIRE #5 |
| 76 | **spurious re-attachment** RECONNECT #5 (reason 2, no shift) → re-verifies, no contradiction |
| 77–83 | verify; 84: FIRE #6 |
| 85–88 | disconnected post-release |

Adversarial timing covers: shift immediately post-release (s=13),
mid-verification shift (s=17), silent shift while blind (s=51),
invalid re-attach request (s=60), spurious re-attachment (s=76).

## 5. K-sweep arms (question b, fixed bars)

Four arms, one binary, fresh state each, K ∈ {4, 8, 16, 32} — geometric
sweep over an order of magnitude centered on the wave-4 bar (halving and
doubling twice). Same trap curriculum for all (targets A→0,B→1):

| step | event |
|---|---|
| 1–3 | probes; commits by s=3 |
| 4–13 | stable verification |
| 14 | **slow-drift trap**: shift A→1 (instability past K=8's bar) |
| 30 | shift A→0 (back) |
| 50 | **premature-shift trap**: shift B→0 |
| 51–88 | settle |

No reconnects in these arms (pure release-then-traps). Per-arm metrics:

- **premature-disconnect rate**: designed shifts landing while
  disconnected / 3 shifts. (A blind shift is exposure the learner cannot
  respond to.)
- **missed-disconnect (overly conservative) cost**: (i) *overheld*
  episodes — connected with streak ≥ 8 (releasable under the wave-4 bar
  but held); (ii) *churn* — ELIMINATE/COMMIT events at steps whose
  pre-step streak ≥ 8 (re-learning suffered while releasable).
- **post-disconnect hold rate**: disconnected episodes with
  action == current target / disconnected episodes. (Reported with the
  caveat that it is dominated by *when* disconnect lands relative to
  traps, not by K per se.)

## 6. Adaptive-bar arm (question b, learner-set bar)

The learner maintains `max_premature` = the longest observed
"episodes from my disconnect to a trainer shift-notice" — i.e., how long
a release has *proved* premature. Bar rule: `bar = max(8,
max_premature+1)`: the floor is wave-4's 8; above it, the learner demands
strictly more verification than the longest run that proved insufficient.
Least-arbitrary ratchet: +1 is the minimum that excludes the observed
failure; any larger margin would be an unjustified constant.

Update rule consumes only ledger-grade evidence: the trainer's
`SHIFT_NOTICE` carries `aux = notice_step − disconnect_step`; the
learner folds it via `sr_note_premature`. OVERRIDE notices do not move
the bar (no shift claim). Without notices the bar stays at the floor —
adaptation requires the notice protocol (preregistered limitation).

Curriculum (targets A→0,B→1):

| step | event |
|---|---|
| 1–3 | probes; s=4–11 verify |
| 12 | FIRE (bar 8, streak 8) |
| 21 | shift A→1 + NOTICE (aux 9) → max_premature=9, bar=10; contradiction → commit A→1 |
| 22–31 | re-verify (streak 10 @ s=31); 32: FIRE (streak 10) |
| 45 | shift A→0 + NOTICE (aux 13) → max_premature=13, bar=14; contradiction → commit A→0 |
| 46–59 | re-verify (streak 14 @ s=59); 60: FIRE (streak 14) |
| 80 | shift B→0 + NOTICE (aux 20) → max_premature=20, bar=21; contradiction → commit B→0 |
| 81–101 | re-verify (streak 21 @ s=101); 102: FIRE (streak 21) |
| 103–106 | disconnected |

Predicted: fire steps {12,32,60,102}, streaks-at-fire {8,10,14,21},
max_premature {9,13,20}. The bar visibly ratchets on evidence.

## 7. Audit budget

256-entry fail-closed cap per arm. Worst arm (flap): 88×2 episode/
scaffold + 14 elim/commit + 6 disconnect + 5 reconnect + 3 refuse = 204.
Adaptive: 106×2 + 10 + 4 + 3 = 229. K arms ≤ 187. All fit with margin;
every arm asserts all `sr_episode`/`sr_audit` return codes.

## 8. What this does NOT show

- Hypothesis generation (same non-claim as wave-4).
- That the trainer notice protocol exists in any deployment — the
  adaptive bar's evidence channel is assumed, not proved.
- Optimality of +1 ratchet vs. other margins (only least-arbitrariness
  is claimed).
- Long-horizon audit (still fail-closed cap; same deferral as wave-4).
