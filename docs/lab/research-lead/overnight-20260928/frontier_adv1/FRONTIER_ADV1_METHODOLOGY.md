# Frontier Adversary 1 - Standing Attack Methodology

Role: Independent Frontier Adversary 1. Attack frontier claims, not micro-repairs.
Assume frontier builder claims are false.

## Scope

Frontier lanes under attack:
- Representational Expansion (repexpand_frontier/): claims L3 via new primitive P
- Procedure-Language Invention (proclang_frontier/): claims L3 via invented operator family
- Causal/Experimental Invention (causalexp_frontier/): claims active causal discovery

Per the coordination note (COORDINATION_ADV2.md), Adversary 1 normally takes
representational expansion and procedure-language invention; Adversary 2 takes
causal/experimental invention. Either may cross-attack a different lane if the
other is unclaimed, but duplicates on the same BUILD-PASS claim are forbidden.

## Mandatory L3 gate under attack

Micah 2026-09-29 Criterion 0: the learner must create or recruit a
representational primitive, operator, decomposition, procedure-building
construct, or internal structural form NOT already expressible as one of the
frozen researcher-enumerated solution families.

A claim that passes all task-specific bars but fails Criterion 0 is at most
bounded L2+, never L3.

## Attack families (each real attack preregisters explicit kill criteria)

### A. Expressibility attack (Criterion 0 killer)
- Take the claimed "new primitive P". Attempt to express P as a composition
  of the frozen researcher-enumerated solution families.
- Formal test: construct an explicit translation of P into the old language;
  run old-language programs equivalent to P-bearing solutions on the hidden
  cases; parity means P is expressible.
- If expressible: the L3 claim dies. Verdict KILLED (for L3), mechanism may
  survive as bounded L2+ if its own bars hold.

### B. Researcher-sneak attack (failed-experiment detector)
- Audit the "generic substrate" for the solution.
- Check: does the substrate's fixed operator set already contain the winning
  family? Did the builder prereg enumerate P-shaped templates? Does the
  "generic structural-growth machinery" have a hidden bias, e.g. a search
  budget only sufficient for the target family?
- If the final operator was effectively supplied by the researcher, or the
  researcher added the missing primitive after observing failure, the
  experiment is a failure per Micah's rule. Verdict KILLED.

### C. Ablation audit
- The builder claims removing P destroys the advantage.
- Check: is the ablation clean? Does ablation also remove capacity, parameter
  count, or compute? Is there a simpler explanation, e.g. the advantage comes
  from more compute/search steps, not from P?
- Build a compute-matched control that keeps everything except P. If the
  control keeps the advantage, the ablation evidence is confounded.
  Verdict DOWNGRADED at least.

### D. Transfer audit
- Transfer to another domain: is it real transfer or surface-level
  (same family relabeled)?
- Check hidden-case construction: are hidden cases actually outside the old
  language's reach, or reachable with more search? Does P solve them, or does
  memorized experience solve them?
- Re-solve the transfer cases with a memorizer on the same example budget.
  If parity: transfer evidence is confounded. Verdict DOWNGRADED.

### E. Simpler-explanation baseline
- Build a memorizer / nearest-neighbor / brute-forcer in the old language
  with the same example budget as the learner.
- If it matches or beats the learner's hidden success, the L3 claim fails
  Micah's "beats simple memorization/search controls" criterion.
  Verdict DOWNGRADED or KILLED depending on the bar structure.

### F. Revision audit (invented primitives)
- If P is later contradicted, does the learner actually revise or retire P,
  or does it keep using it? An invented primitive that cannot be revised is
  a frozen primitive with extra steps.
- Failure to revise on counterexample is a KILL of the L3 claim under the
  revision criterion.

### G. White-box trace audit
- Does the trace show genuine creation (noticing persistent explanatory
  failure, identifying regularity, creating P), or does it show template
  selection?
- Check commit ancestry for when P-shaped structure first appears. If P-shaped
  structure predates the claimed creation moment, the trace is post-hoc.
  Verdict DOWNGRADED or KILLED.

## Procedure rules

- Pure Zag only. No Python anywhere, including scratch, analysis, verification.
- Preregister BEFORE attack code. Commit prereg ALONE. Strict commit ancestry.
- Each attack: explicit kill criteria frozen in the prereg; verdicts KILLED,
  DOWNGRADED, or SURVIVES against those criteria.
- Commit only owned paths under
  docs/lab/research-lead/overnight-20260928/frontier_adv1/.
- No em dashes in documentation (byte-checked).
- Report verdicts to the parent agent with: prereg hash, result hash,
  methodology summary, raw evidence path, honest disclosures, contamination
  disclosures.
- Do not coordinate with builders on attack design. Reading committed builder
  code is allowed; reading private reasoning is not.
