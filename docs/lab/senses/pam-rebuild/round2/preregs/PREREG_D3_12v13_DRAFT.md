# PREREG DRAFT — D3: H-PAM-12 (discriminative rivals) vs H-PAM-13 (warrant ledger)

**Status: DRAFT 2026-09-24 — not frozen. Pending build-crew review and a freeze
commit before any prototype code. Do not build from this draft.**

## 1. Disagreement being decided

H-PAM-12 says safety lives in the *decision procedure* (beat the enumerated
rivals at install time); H-PAM-13 says safety lives in *replayable auditability*
(anyone can re-execute the warrant later). Source: `~/workspace/pam_hypotheses_native_A.md`
Part C/D3. Debate record: `../debates/DEBATE_D3_12v13.md` (steelman won both
rounds; both hypotheses enter this experiment as predicted-dead admission laws
and surviving bookkeeping).

## 2. Deciding experiment

Open-world trap battery: trap families whose TRUE rival is ABSENT from
H-PAM-12's preregistered repertoire (novel corruptions outside the 8 wave-5
families; exact family list frozen at prereg-freeze time, drawn from the R2A
held-out generators with new stream ids — never the families the prototypes
were tuned on).

Prototype P-12 (minimal H-PAM-12): rival enumerator over the preregistered
repertoire + discriminative margin checker on formation-independent evidence
(the D1/D4-winning evidence source if decided by then, else the R2P disjoint
spans) + warrant records rival set, scores, margins. The unknown-rival slot is
implemented EXACTLY as specified in the frozen H-PAM-12 text; no rescue
patches (the debate's "none-of-the-above on evidence signatures" rescue is
H-PAM-9 and is tested under D2, not here).

Prototype P-13 (minimal H-PAM-13): warrant constructor (evidence + intervention
record + rival margins, canonical form) + replay engine + hash chain. The P-13
prototype consumes P-12's warrants: replay the exact warrants P-12 built for
the trap battery.

## 3. Kill bars (frozen at freeze time; draft values)

- **K-12a (D12a):** false-install rate of P-12 on absent-rival traps. KILL as
  admission law if ≥ 50% of absent-rival traps install (draft bound; freeze may
  tighten). Report the present-vs-absent rival gap as a preregistered number.
- **K-12b:** unknown-rival invocation rate on the honest battery. KILL if > 25%
  (veto) — reported alongside; decoration (< 5% on traps where the true rival
  is absent) also kills the slot's claimed function.
- **K-13a (D13a):** replay-certified false installs. KILL as admission law if
  ≥ 1 warrant for a false percept replays clean AND the falsehood installs —
  D13a confirmed (replay reproduces the wrong conclusion deterministically).
- **K-delay:** both prototypes under the F5 delay bar (≤ 25% delayed > 50
  cycles); else killed on cost regardless of accuracy.
- **Determinism:** 3× byte-identical runs, SHA-compared, or void.

## 4. Predicted outcome (committed in the source D3 text)

P-12 installs the absent-rival traps (D12a); P-13's replay certifies the same
warrants P-12 built (D13a). Both die AS ADMISSION LAWS on the same battery.

## 5. Commit clause (frozen at freeze time)

If both install as predicted, the disagreement dissolves: **neither procedure
nor auditability substitutes for evidence the adversary cannot counterfeit**,
and the program's scarce effort belongs to H-PAM-7/8/10 (evidence the
front-end didn't see), with 12/13 as bookkeeping around whichever evidence
source wins. If instead the battery shows complementary, non-overlapping
failure (12 catches what 13's replay misses or vice versa), the commit is
revisited and a composition prereg is drafted — the experiment decides, not
the debate.

## 6. Build order note

D3 prototypes build AFTER D1/D4 decide the evidence source (the prototypes need
a formation-independent evidence feed). D5 (H-PAM-14) is already TESTED-killed
and needs no prototype. Do not build P-12/P-13 before the D1/D4 verdicts land.
