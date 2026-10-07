# Frozen core ownership successor - graph versus answer fact

Date2026-10-06. Follows expected-answer audit. Original core unchanged.
QUESTION: after supervised graph acquisition, does no-feedback reuse depend on
learned executable MAP or the answer fact promotion also writes? Does graph transfer
to a new subject with the same two-relation path shape?
Hypotheses: executable-method reuse vs promoted exact-answer cache.

Fixture two unique observed paths101-r11->201-r12->31 and301-r11->401-r12->41.
Train query(101,99,expected31,flags0); outcome31, one MAP licensed by first path.
Declared evaluator semantics relation99 means r11 thenr12. Core receives evidence
and training feedback but not a source definition of99; heldout301 is therefore a
structural-transfer opportunity, not proof learner must identify a unique relation
law from one example. Primitive source graph has literalguards101,201.

Forks clone same post-training state:
- intact query101,99,expected-2 ->31.
- MAP_ONLY_ERASE: remove live MAP nodes only, keep all facts/program cells ->31
  expected because activation reads promoted exact-answer fact. Non-destructive
  type erasure marks MAP nodes nonlive; does not pretend full method delete.
- METHOD_ERASE: additionally remove all four-op executable cells101..104; retain
  literals and all facts ->31. This is facts-retained/method-erased test.
- ANSWER_FACT_ERASE: erase only FACT(101,99,31), retain licensingfacts/MAP/root;
  query no-feedback unmasked expected-2 predicted-2 (MAP not activated).
- ANSWER_FACT_ERASE_MASKED: same but flags1 ->31 by new trial enumeration;
  report recomputation, not reuse.
- DIRECT_MAP_EXEC: bypass query route and invoke stored graph root with101 ->31;
  same root with301 ->-999999 due literalguards. Direct execution demonstrates
  graph exists but not ownership of API answer or transfer.
- HELDOUT_UNMASKED: intact query301,99,expected-2 ->-2 predicted, no supplied answer.
- HELDOUT_MASKED: query301,99,expected-2,flags1 ->41 by enumerating new unique path.
  Flat r11/r12 relation composition rival computes41 from observed facts; no need
  learned source101 graph. Masked source ordering not proof acquired relation law.

Count maps/executable/facts before and after ablation. State checksums full arena
for clones; effect invariants preserve licensing fact values. Clones independently
fresh from snapshot, no cross-arm contamination. Test renamed node/value IDs offset
1000 for subjects/intermediate values and relations, terminal31/41 unchanged.
Independent hand paths label evaluator, not tested graph output. Query99 intended
semantics declared only evaluator, uncertainty caveat binding.

Artifacts ownership_driver.zag, ownership.zag, ownership_run.sh,
ownership_compile1..3.txt, ownership_run1..3.txt, ownership_provenance.txt,
OWNERSHIP_REPORT.md. Fresh build/run3, pureZag, nonempty raw outputs identical;
source-prefix cmp. Exit1 on discrepancy; preserve failed logs before repair.
Generated binary ignored. No source tweaks to force an acquisition claim.

Kills: graph ownership of cached API response if method deletion preserves it;
identity-general method reuse in this particular chain representation if direct
storedgraph rejects301. Does not kill generic graphs, revision, masked search,
latest production TNN or representation that can bind relation-variable methods.
Next: generic frame-bound relational method vs literalized path, fact-matched flat
join and general-program rival. Any new core mechanism needs new prereg and explicit
source-change accounting; not experience-only if task handler added.
