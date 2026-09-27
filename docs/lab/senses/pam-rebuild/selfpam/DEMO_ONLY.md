# Self-PAM gate — FORMAL SCOPE: DEMO ONLY

Issued 2026-09-27 by the fix-or-kill executor (decoration-audit P2 #7).
This document is binding on how the Self-PAM composition may be described
and used until every blocker in §4 is cleared with committed evidence.

## 1. Scope declaration

**The Self-PAM gate composition in `selfpam/src/` is DEMO ONLY.**

It sits on **no live TNN decision path**. No TNN utterance, memory install,
or speech act is admitted, withheld, or modified by this gate. The
`main_smoke.zag` (11-step) and `main_g1probe.zag` drivers are test
harnesses, not live consumers: a smoke driver exercising all 9
dispositions is not a TNN decision path, and must never be presented as
one. The decoration audit (2026-09-27) verified zero callers of
`sp_init`/`admit_claim`/`corr_observe` outside Self-PAM's own drivers.

## 2. What is genuine (and stays claimed)

The internal mechanism is honestly built and honestly tested:

- `src==1` (attested independent channel) is consulted at both install
  dispositions (`admit_claim.zag` `sp_step`); unattested re-observation
  stays provisional (disp 1/8); evidence-hash mismatch fails closed
  (disp 0, margin unknown).
- Pure Zag, zero RNG, deterministic given state; 16-check verifier
  (`verify.py`) including two-run byte-identical comparison.
- Standing blockers were documented in `src/README.md`, not hidden.

Nothing in this document retracts the above. Demo-only scoping concerns
*deployment status*, not mechanism honesty.

## 3. Adoption-status correction

- The 2026-09-24/25 program notes mentioning Self-PAM "adoption" have **no
  adopted integration document**. Nothing is adopted.
- R2 fork adjudication stands: **Fork C was killed as theater**
  (licenses deliberation's say-so without store validation);
  **Fork D (discipline) survives red-team** (24/24 trace-alibi rejection,
  8/8 confabulations, 4/4 held-out, 12/12 utterance-type smuggling) **but
  is unwired and unintegrated** (`r2/SYNTHESIS.md`).
- The G1 registration (`src/G1_REGISTRATION.md`: candidate gate id 2
  behind the R2-3 admission instrument) is **planned, not applied**:
  `round2/forks/R2-3/src/sense.zag` on the current branch still accepts
  only `gate_id` 0/1.

## 4. Complete blocker list for live integration

Every item must be cleared with committed evidence before the gate may
leave demo-only scope. Items marked (Micah) require his explicit sign-off;
items marked (prereg) require a committed prereg amendment per the
frozen-PREREG amendment rule.

- **B1 — Real live consumer.** A TNN decision path that calls
  `admit_claim`/`corr_observe` on draft claims before speech. None is
  designed; none is built. Designing one is a research/architecture task,
  not a wiring task.
- **B2 — CC1 correlated-corroborator guard, verified in Zag (DEPLOY
  BLOCKER, PREREG §3.5).** The contradiction-matrix verdict stands: two
  correlated-wrong high-conf PASSes agreeing within tolerance defeat the
  install rule (CC1 seqs 10983/10992 → REVISED_INSTALL false permanent).
  The guard's Zag verification is its own experiment; this build does not
  clear it and must not be cited as clearing it.
- **B3 — §8 pre-build amendment blockers (prereg) (Micah).** KB threshold
  sign-off (Micah); frozen probe charter (licensed-inference-step set);
  FACT-type tolerance table; marked-emission format (exact frozen wording
  for passing emissions); sealed corpus manifests (CELL-C1/C2/C3/W/P/D/R).
  All open. The current build runs against §8 *starting bids* only.
- **B4 — Fork D trust root: write-once evidence partition.** Per
  `r2/SYNTHESIS.md`, D discriminates on the PROV *label*, not on
  authorship itself; the M5L-001 probe demonstrates provenance
  laundering (relabel GEN as EXT → INSTALL). "A write-once evidence
  partition the generator cannot author ... remains unbuilt and is the
  explicit next experiment: D's discipline + a tamper-evident provenance
  substrate would move the trust root from labels to physics." Until
  built, D's trust root is labels.
- **B5 — Production channel-key ceremony.** The frozen C1 channel test
  key `SELF-PAM-C1-REG-CHANNEL-2026-09-23` is a test key; production
  replaces it with a channel-key ceremony. Only the mechanism
  (gate-verifies / forger-cannot-sign) is frozen, per IE amendment R2.

## 5. What un-scopes demo-only

B1–B5 cleared, each with committed evidence; prereg amendments committed
BEFORE any affected measurement runs (frozen-PREREG amendment rule);
Micah's sign-offs where marked. Partial clearance un-scopes nothing —
a gate with a live consumer but no CC1 guard is a live unguarded gate,
not a demo.

## 6. Red-team note

The mechanism's internal honesty (attestation consulted, provisionality
preserved, fail-closed on hash mismatch) was re-verified by the
program-wide decoration audit on 2026-09-27; no new behavioral claim is
made here. The audit's verdict on this component: **OPEN (built,
unwired)** — this document is the formalization of that verdict into a
binding scope.
