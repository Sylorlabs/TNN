# PREREG_AMENDMENT1: operator firing semantics (pre-implementation)

Date: 2026-10-02. Status: FROZEN. No implementation exists at this
commit; no results exist. This amendment resolves an ambiguity in
PREREG.md section 2, it does not change any frozen number, kill
bar, or falsifier.

Ambiguity: section 2 says "Each operator fires at most once per
query (the composition_adapt firing precedent)." Section 4's frozen
NO-SUB hand derivation requires t16=3: one truncation (t1->m) plus
two extensions (e_d->d, e1->t1).

Resolution (frozen): TRUNCATE-ONE fires on the FIRST stale MAP in
node-id order only (targeted repair of one stale MAP per query).
EXTEND-ONE applies to EACH eligible MAP in the extend sub-pass
(one link per MAP; "ONE" refers to one link, matching the
composition_adapt EXTEND-ONE pass structure, which likewise
iterates over MAPs). The frozen NO-SUB expectation t16=3 stands
unchanged, as do all kill bars K1-K10 and all falsifiers.

No other section of PREREG.md is altered.
