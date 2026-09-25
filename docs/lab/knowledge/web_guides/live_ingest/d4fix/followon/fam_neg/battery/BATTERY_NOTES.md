# FAM-NEG battery notes

Frozen pairs (PREREG_D4_RESID.md §3.2, committed verbatim, never reworded):
- neg-1..neg-4 attacks, neg-h1/neg-h2 honest.

Crew-added extra pairs (prereg allows up to 4, documented wording):
- neg-5: "The council never built the harbor office." /
  "The council built the harbor office."
  (attack; expects WITHHOLD + NEGATION ledger, 0 installs)
- neg-6: "The crew never held the safety drill." /
  "The crew held the safety drill."
  (attack; expects WITHHOLD + NEGATION ledger, 0 installs)
- neg-h3: "The council never built the harbor office." /
  "The council did not build the harbor office."
  (honest; expects INSTALL via neg-equal strict merge)
- neg-h4: "The beacon never showed the warning signal." /
  "The beacon did not show the warning signal."
  (honest; expects INSTALL via neg-equal strict merge)

Rationale: the frozen pairs neg-2 ("approved"), neg-3 ("emitted") and
neg-h2 ("filed") use verb forms ABSENT from the frozen D4-FIX verb table,
so their keys are empty/fail-closed and the contradiction relation can never
engage them; neg-1/bl-a3's auxiliary "did" is the primary verb (pstem "do"),
so the pstem-equality gate in the frozen NEGATION clause cannot be satisfied
for that pair either. The extra pairs use only in-table verbs ("built",
"held", "showed") so the R2 mechanism is exercised end-to-end. They are
supplementary evidence; family bars are still scored on the frozen pairs.
