# SELF MODEL — TNN's conflict-resolution machinery (2026-09-22)

Machine-readable inventory of the subject engine (`subject.zag`, faithful
copy of the frozen R4C trial binary). The proposer reasons over this.

## Decision stack (askfirst = current champion, mode 4)

```
PRE:  so,sn = coherence scores vs pre-channel anchors (+1/-1 per relation)
      c = NEW if sn>so | OLD if so>sn | WITHHOLD(tie)
CONSULT TRIGGER: consult=1 iff c != NEW        # <-- C1/C2 modify this
POST (if consult): so2,sn2 = scores vs post-channel anchors
      v = NEW if sn2>so2 | OLD if so2>sn2 | WITHHOLD(tie)
NO-CONSULT: v = NEW                            # c==NEW here
COST: 7 ops/item base; +16 if consulted (10 channel + 6 recompute)
```

## Frozen measured state (VERDICT_R4C.md, commit 0c12d717)

| arm | acc | wrong | cost |
|---|---|---|---|
| askfirst (champion) | 22/24 | 2/24 | 424 |
| coherence | 20/24 | 4/24 | 168 |
| recency | 8/24 | 16/24 | 48 |
| base | 8/24 | 0/24 | 0 |

Distractors: RECALL 10000 (must hold), COST-quiet 200 (must hold).
Determinism: 5/5 byte-identical per mode. Separation: no gt in binary.

## Known residual gaps (from VERDICT_R4C.md — the proposer's diagnosis targets)

- GAP-1: ask-first's 2 misses are ADV-OLD items where recency and
  coherence WRONGLY AGREE on NEW pre-channel, so no consult fires.
  Root cause: correlated-wrong agreement; the consult trigger
  (c != NEW) is blind to it. The ONLY pre-channel signal distinguishing
  these items: a channel packet is present (cidx != -1).
- GAP-2: coherence fooled on 4 ADV items (stale corroboration) —
  already fixed by ask-first's consult; not the champion's gap.
- GAP-3: cost. ask-first spends 424 ops vs coherence's 168. The consult
  recompute re-evaluates all 3 relations; only the corrected one changed.
- GAP-4 (process, out of scope): KB3 champion rule was unsatisfiable
  against the degenerate baseline — a drafting defect, not machinery.
