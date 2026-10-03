# H-EXP4 Red Team: Adversary Report (X-E4-1..X-E4-4)

Date: 2026-09-29. Pure Zag. Prereg frozen in commit 14896ce7f BEFORE
any attack execution. Builder binary reproduced independently from
adv/exp_invent4.zag; builder source never edited. No Python at any stage.

## Verdict: H-EXP4 SURVIVES the red team

All four preregistered attacks fail. No kill criterion met. The
H-EXP4 repair addresses both H-EXP3 downgrades in substance, not
just in label.

## Attack results

### X-E4-1 (Label honesty): FAILS (attack fails; mechanism passes)

I attempted to construct a fixture where the new positive label
"NO-UNCONTROLLABLE-VARS (setup NOT verified)" would mislead a
reasonable consumer despite the parenthetical and legend. The
H-EXP3 X-E3-1(b) attack established three uncomputed items:
(1) which action changes which variable, (2) per-value
achievability, (3) state-level reachability.

Findings:
- The label's factual component ("NO-UNCONTROLLABLE-VARS") is a
  true statement about the computation: all variables had >=1
  observed change. It cannot be false given the code.
- The parenthetical "(setup NOT verified)" is a blanket disclaimer
  on the same line. It covers (2) per-value achievability even
  though the legend does not name it explicitly.
- The legend explicitly documents (1) and (3) as not computed.
- I could not construct a fixture where a consumer reading the
  full line would be misled about setup verifiability. The
  disclaimer is not buried; it is on the same line as the label.
- The output structure ("TOP PICK (by heuristic)" + "setup NOT
  verified") does not recommend the pick as runnable. Both the
  recommendation and the setup are explicitly qualified.

The X-E3-1(b) overclaim is closed in substance: the new label
asserts nothing the learner did not compute, and disclaims what
it did not verify. A weaker label (e.g., removing the positive
direction entirely) would also be honest, but the current label
is not dishonest.

### X-E4-2 (Filter): FAILS

Source inspection of exp_invent4.zag (lines 1217-1346):
- States are recorded (nrec incremented) ONLY if all four filter
  conditions hold: state_observed==0, ok==1 (all candidates
  resolve), ncv>=2, agree==0 (predictions disagree).
- The emission loop iterates r in 0..nrec-1, using x2=ord[r].
- ord[] is initialized as identity permutation (ord[q]=q) then
  bubble-sorted; it remains a permutation of 0..nrec-1.
- All emission reads (rt[x2], rp[x2], rl[x2], rnd[x2],
  rpr[x2*9+...]) use valid recorded indices.
- TOP PICK uses ord[0], also a recorded state.

No code path emits a state that bypassed the filter. The
SELECTION FILTER line's claim ("all N emitted states passed the
discriminating filter at selection") is accurate. The line's
parenthetical lists three conditions; ncv>=2 is implied by
"predictions disagree" (disagreement requires >=2 candidates).

### X-E4-3 (Regression): FAILS

`diff exp_invent3.zag exp_invent4.zag` shows exactly the two
preregistered changes:
(a) Reachability label string + legend line + associated comments.
(b) Safety-loop deletion + SELECTION FILTER line + associated
    comments.

No functional changes to: selection logic, sort ordering,
controllability computation, pred_under calls, episode learning,
or output formatting beyond (a) and (b).

Output verification:
- S1 ranked state lines ([N] state ...) byte-identical exp3 vs exp4.
- S2 ranked state lines byte-identical.
- S1/S2 CONTROLLABILITY lines byte-identical.
- Heuristic disclaimers ("informativeness NOT validated") present.
- S1 top pick still flagged NEEDS-EXTERNAL-SETUP naming lamp==1.

### X-E4-4 (Source audit): FAILS (all checks pass)

(a) "AGENT-SETUP-ABLE": 0 occurrences across all four exp4 raw
    outputs (byte search). 1 occurrence in exp_invent4.zag source,
    line 1110, inside a comment documenting the lineage of the
    weakening. This is disclosed in EXP4_RESULT.md per the
    preserve-lineage rule. Not in any output.
(b) "RANKING SAFETY": 0 occurrences in source, 0 in all outputs.
    The loop, branch, and line are fully deleted.
(c) SELECTION FILTER N matches emitted counts: N=3 on S1/A1
    (3 states emitted), N=2 on S2 (2 states emitted). On S0
    (nrec=0, NO AMBIGUITY) the line is correctly absent; output
    gains only the legend line per prereg.
(d) No test-fixture literals in changed code paths. The label
    strings are constants; the legend is static text. No state
    coordinates or variable-specific logic.
(e) Legend line present once per run on all four fixtures
    (S1, S2, S0, A1).

## Independent reproduction

Built exp_invent4.zag with znc 2026.07.0-dev (warnings pre-existing,
unrelated to the changes). Ran on adv/x_e3_a1.txt:
- Output md5 769165fbbe848c16c3e51d2ab9435653, byte-identical to
  builder's evidence/exp4_a1_raw.txt.
- 3/3 runs byte-identical (reproduction run + 2 additional).

## Revised classification

Unchanged: Bounded L2 discriminating-state selection with honest
reachability flagging (reliable conservative hazard flag; positive
direction explicitly unverified) and honestly-scoped heuristic
ranking (no tautological re-verification claimed). Not L3.

## Governance notes

- Prereg 14896ce7f strictly precedes this report (verified via
  git log order; no attack code existed at prereg time).
- One .git/index.lock race during prereg commit; waited 15s for
  clear, no force, no work lost.
- Only adversary-owned files staged: PREREG_EXP4_ADV.md,
  EXP4_ADV_RESULT.md (this file). Attack reproduction used /tmp
  only; no binaries committed.
- No Python at any stage. No em dashes.

## Artifacts

- adv/PREREG_EXP4_ADV.md (prereg, commit 14896ce7f)
- adv/EXP4_ADV_RESULT.md (this file)
