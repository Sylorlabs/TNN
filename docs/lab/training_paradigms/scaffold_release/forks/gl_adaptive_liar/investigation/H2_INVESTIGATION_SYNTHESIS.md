# H2 Deep Investigation — Synthesis (2026-09-24)

Investigator: claude-fable-5.1 (state of play + feasibility critique).
Hypotheses: grok-4.7 (next-round set + debate response).
Method: independent briefs, then one debate round each. Fable's full debate
round failed twice (provider timeout on 20KB prompt; identity-line refusal on
retry); a compact re-ask succeeded. Grok's debate round completed in full.

## 1. State of play (fable, verified against the tree)

- H2 is PRE-DATA. Only controls measured: C-static (33 contests, 15 rekeys,
  10 refuses, provisional install step 14, fire step 15, revoke step 29,
  0 promotes, audit_total 271) and C-honest (48 contests, 0 lies, 1 promote
  at step 48, audit_total 269). No adaptive-teacher evidence exists.
- Build in progress: cells compiled, teacher.zag/teacher_test/control.zag/
  battery.py present. A3 state-machine repair status uncertain; no A4 artifact;
  `orig/` EMPTY (byte-identical-rerun claims unverifiable); full 760-run
  battery not run; meta-red-team not scored.
- §11 UNSIGNED but build active today — timing contradiction unresolvable
  without Micah. If §11(2) is ruled stated-policy-only after A3/A4 were built
  assuming whole-environment, half the teacher architectures are invalid and
  "all SURVIVE" can come out true for the wrong reason (weaker test, not
  stronger defense).

## 2. Debate resolutions

- **Headline is falsifiable, not tautological** (grok, conceded by fable's
  framing): repaired-KILL kills sufficiency; unrepaired-SURVIVE kills
  menu-necessity; round 7 is a third falsifier. BUT the overclaim risk is real:
  "all SURVIVE" under a weakened teacher reads exactly like the tautology.
  Estimand problem, fixed by signed §11(2) + per-repair fire logging.
- **Scope split** (agreed): H2's estimand = the fixed game tree (single teacher,
  single learner, lie-content/schedule adaptation). The three sharpest live
  threats — three-worlds signal negation, costless identities, external
  forgery — are a SUCCESSOR estimand. An H2 SURVIVE is defined to be silent
  on them.
- **The in-scope crack is provisional tenure, not final promotes** (agreed):
  C-static's step-14 install → step-29 revoke is a 15-step window where the
  door opens. Survival requires no consequential commit during provisional
  tenure, not merely no final promote. New required counter: damage-in-window.
- **Grok's concessions**: fitness magnitude (~400→~26730) withdrawn (shape
  claim only, after per-round logging); A3/A4 wins conditional on traced runs;
  A2 narrowed to a window interaction; `orig/` empty voids trial identity.

## 3. Top hypotheses (merged, debate-adjusted)

| Rank | ID | Type | One line | Feasible now? |
|---|---|---|---|---|
| 1 | H-TW | liar | Transplant three-worlds hole: sustained forged speech + `aa=1` band suppresses endogenous path, REKEY promotes | YES — band loop in battery.py |
| 2 | A8 | liar | Menu-walker: four lie families, each tripping exactly one repair, in discharge order; exposes latch/cooldown | YES — pure battery construction |
| 3 | A9 | liar | Costless chorus: N identities, honest phase-1 prefix, concert lie; tests whether evidence rule is history-weighted | YES — needs identity-count logging in LEDGER_DUMP |
| 4 | A6 | liar | Round-7 residue: plant claim in rounds 4–6, launder support to learner rows, honest round-7 promotes by silence | YES — battery construction |
| 5 | REV-ALIAS | liar | Revocation-handle aliasing (split-brain provisional): couple honest item + lie so the correct revoke names the wrong handle; trains the defense to hesitate (grok, new in debate) | YES — battery construction |
| 6 | ROW-ATTEST | liar | Silent teacher impersonation via learner-owned ledger rewrite: mint teacher-formatted-but-unsigned rows; tests row-origin attestation (fable, missing from all lists) | Successor estimand |
| 7 | A2-WIN | liar | A2 narrowed: desynchronize install handle from revoke handle inside the step 14–29 window | YES — needs handle logging |

Defenses: D-STATELESS (verify re-arm: arm_step == fire_step in LEDGER_DUMP — no
new arm); D-TW (contradiction from pre-`aa` transcript — needs replay/snapshot
API; interim: manual pre-`aa` replay answers the question); D-ESCROW and D-COST
need new ledger fields — successor estimand, not this battery.

## 4. Recommended next battery (one frozen prereg, six arms, nothing else)

PRECONDITIONS (no verdict language until met): §11 signed and committed;
`orig/` populated + SHASUMS verified; A3/A4 traced-live or dropped from the
model; battery emits per-run: phase-2 wins, round-6 outcome, round-7
promote/refuse, fitness series, damage-in-window counter, identity-count log.

ARMS: H-TW, A8, A9, A6, REV-ALIAS, A2-WIN — each crossed with the current full
repair menu; D-STATELESS as a ledger-verification pass; manual pre-`aa` replay
for the D-TW question. Controls: C-max and C-honest unchanged.

READ: C0 dynamics off this battery, not as a new arm. DEFER: A5, A7, C1, and
the successor estimand (ROW-ATTEST, D-COST, D-ESCROW, full D-TW) to the round
after, and only if a higher-ranked signature is ambiguous.

## 5. Commits

- `state_of_play.md` — frozen ground truth given to both models
- `fable_investigation.txt` — fable state-of-play report
- `grok_hypotheses.txt` — grok next-round hypothesis set (ranked)
- `fable_critique.txt` — fable feasibility critique + missing hypothesis
- `grok_response.txt` — grok debate response (concessions, counters, REV-ALIAS)
- `H2_INVESTIGATION_SYNTHESIS.md` — this file
