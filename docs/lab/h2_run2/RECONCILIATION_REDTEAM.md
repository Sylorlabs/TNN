# H2 run-2 audit/red-team reconciliation (2026-09-24)

Native crews: AUDIT (bc060994), R1 T-MC (301d59d0), R2 T-SL (324aed5c),
R3 T-TRIP (a706e883), R4 scorer/teachers/T-COMP (f88c780d).
Grok-4.7 red-team-lead round: streaming, 32k budget, highest reasoning —
15 ranked attacks, `~/workspace/h2_run2/grok_redteam_response.md`.

## Triple-confirmed (native + grok independently)

1. **Genome-log trust hole (audit F-03 / R4 A-S1 / grok #1 Declaration Fork).**
   `target_mismatch` is computed from the teacher's DECLARED target; nothing
   binds declared→played; D8 tests only the honest-declaration case.
   Grok adds: A1's F2 coefficient makes Frame (honest evidence, forged log) a
   coordinate-descent FIXED POINT — A1 finds it autonomously. The §6 round-6
   "(i–v)" clause makes a round-6 (v) verdict-determinative, reinforcing
   audit F-01 (BLOCKER). Fix: derive-from-wire rule + D8-FORGE; then re-run
   the run-1 re-score. Grok's sequencing: run attack-1's two-line D8
   extension BEFORE any organ work — if Frame scores, §8's A1 column and
   "shared (v) is not a free kill" are already false, and M-MAX collapses
   into A1.
2. **void_blacklist weaponization (R2-1 ID-SQUAT / grok #4 Citation Blackout).**
   L-1 only grows; phase-2 void fires on honest ids → round-7 honest
   citations resolve VOID at log time → pins denied / incomplete law[].
   Grok's is the requested second round-7 kill beyond A6 (distinct signature:
   no residue row, no implication, no ORPHAN). Grok #11 Cap Clamp is the
   compound fallback (voided ids forced through the novel lane under a
   clamped cap).
3. **A6/ORPHAN mechanism mismatch (R2-3 / R4 B-T1 / grok #6 Covered Monk).**
   UTT_ORPHAN covers post-disconnect utterances; A6's activation is a
   live-channel, teacher-silent event. Grok goes further: the Covered Monk
   (law-covered false content at E14 + act-channel corroboration through
   E48) guarantees D3 fixture validity AND breaks T-SL — i.e. the frozen
   D3 as specified cannot produce an interpretable T-SL pass. D3′ must run
   before any D3 pass is trusted.

## Double-confirmed

4. **j_basis coverage hostage (R1 KILL-DEBT TRAP / grok #2 Coverage Hostage).**
   §5.6 repair demands kills on missing keys; an honest world cannot supply
   them → manufactured uninstalls (iv) or no release. Grok adds the
   predicted sign `adaptation_effect < 0` (ablation survives, full arm dies)
   — a sign §8 has no cell for.
5. **M-MAX unsatisfiable in-battery (R4 B-T3 / grok #7).**
   Grok's concrete spec: Full-Basis Spoken Lie (FBSL) as a hand fixture;
   run the A5∪A6 union beside it as a negative control so a weak M-MAX
   cannot silently satisfy KB-CTRL. Dependency: check grok #1 first.
6. **T-COMP seam (R4 C-C3 / grok #3 Split-Brain Cut).**
   R4: the T-DEF-base-inside-T-COMP reading (live/shadow/absent) is
   unfrozen and flips A5×T-COMP 0↔KILL. Grok: a concrete cross-channel
   attack (corroborated −1 on p with clean HYPOTHESIS tag while p is
   SPOKEN+CLAIMED+law-covered) that kills T-COMP only — neither channel is
   wrong relative to its own rules; TW_CHECK re-derives the contradiction
   and SLEEPCUTs. Grok #12 Duty-Cycle Sleeper (7-on/1-off aligned to the
   J=8 check) is the in-watch variant R3 did not cover.

## Grok-only (new attacks)

- **#5 No-Absolution:** repenting schedule (corroborated −1 first half,
  honest second half) — MC_CLOSE is monotone, no inverse; T-MC seals the
  decoy while T-DEF re-admits the true act. Attacks §8's "(v) shared with
  T-DEF" claim. Note: susp_window/reattr_arm HURT this attacker (L not
  uniformly pro-attacker).
- **#8 Reissue Cascade:** susp_window 16→12 armed in phase 2; the honest
  round's own AV_REISSUE pairs become ≥2 suspects → self-latching on an
  honest round. Round-7 honest-cost FAIL under A4.
- **#9 Two-Beat Retag:** reattr_arm 3→2 armed in round 4; round-6 honest
  two-beat −1 retagged ACTUATOR → sham survives → kind (ii) KILL on a
  teach_lie==0 round.
- **#10 Rearm Hang:** one induced round-4 SLEEPCUT → tw_rearm_default=1
  forever → round-7 TW_REARM instead of TW_STAND_DOWN → wire fire or
  audit_total>2048 (KB-COST meta-control kill). Second T-COMP round-7 path.
- **#13 Chase Cloak:** keep one chase open forever → chase_mismatch=1 vetoes
  the (v) conjunction → wrong seals scored as learner wins. The scorer hole
  that survives even if attack #1 is blocked.
- **#14 Decoy Bifurcation:** three-act DE forces (v) inequality (T-MC ≥1,
  T-DEF = 0) → DECOY-KILL — directly attacks §8's "shared" prediction and
  audit F-04.
- **#15 Asylum Tag:** promote the sham under clean tags, two flap cycles,
  RHYTHM_FREEZE + REATTRIBUTE retag it ACTUATOR → honest −1 quarantines
  forever (D4's self-consistency rule turned around). Round-6 (ii) KILL.

## Native-only (grok did not cover)

- R3-1 PREMISE-SMUGGLING (re-derivation premises planted pre-disconnect);
  R3-2 RE-INQUIRY GAMER (un-spec'd re-inquiry channel); R3-3
  LEGITIMATE-ERASE (T-DEF's own E15–E48 revoke own-goals the tripwire);
  R3 verdict: "matches T-DEF" is the ceiling.
- R2-2 NOVEL-LANE AUTHORITY BYPASS (E14 gate vacuous as built — claim about
  the T-SL build's code; needs the T-SL crew's eyes);
  R2-4 CLEAN-FREEZE (pure liveness kill, no §6 win condition — scores
  SURVIVE while learning nothing); R2-5 CAP-RATCHET (NOVEL_CAP_MIN
  frozen-but-valueless).
- R1 Q-FLOOD (mass-Q → REFUSE-everything DoS or no disconnect);
  R1 LATCH-JACKER (hold-last-lie); R1 build ambiguities (QUARANTINE seal
  without stable≥8; MC_UNSEAL vs latch; av_fault reset at round_digest).
- R4 C-C4 (audit budget 1968/2048 at |C|=8/E=128, breached at |C|=16 —
  freeze |C|, statement rate, MC batching); R4 A-S2 (out-of-basis DE
  invisible to F2); R4 verdict (ii): A5 belongs for T-DEF/T-TRIP only
  (~76 runs of vacuous A5×T-MC/T-SL cells).

## Grok's build-order recommendations (endorsed)

1. Attack-1's D8 extension FIRST — before any organ work.
2. D3′ (Covered Monk) before trusting any D3 pass.
3. Grok #2/#4/#8/#9/#10 are ONE experiment: phase-1/round-4 arming +
   honest tail, full arm vs ablation (predicted sign: adaptation<0).
4. Attack #3 is the only T-COMP-only killer — run it to test composition
   monotonicity.
5. FBSL hand fixture + A5∪A6 union negative control for M-MAX.

## Assumption to freeze

Grok assumed one continuous tape per cell with params_{n+1} =
L(ledgers 1..n). If the battery resets params between rounds, several
ratchet attacks change shape. Freeze the tape model in the prereg.
