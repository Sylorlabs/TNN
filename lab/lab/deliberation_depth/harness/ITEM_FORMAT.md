# Item format (H5 deliberation harness)

Judgment items are JSONL: one JSON object per line, UTF-8, lines separated by
`\n` (a trailing `\r` is stripped).

## Schema

```json
{"id":"S4","task_type":"revoke",
 "input":{
   "hypotheses":[{"id":"H-REVOKE","label":"revoke the memory"},
                 {"id":"H-KEEP","label":"keep the memory"}],
   "evidence":[
     {"id":"e1","supports":{"H-REVOKE":500},"attacks":{},"text":"early suspicion"},
     {"id":"e3","supports":{},"attacks":{"H-REVOKE":650},"text":"decisive refutation"}
   ]},
 "ground_truth":"H-KEEP"}
```

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | item id; `[0-9A-Za-z_.-]{1,64}` |
| `task_type` | yes | `admit` \| `revoke` \| `logic` (recorded; the procedure is the same eliminative engine for all three) |
| `input.hypotheses[]` | yes, ≥1 | candidate judgments; `id` as above, `label` free text (ignored by the engine) |
| `input.evidence[]` | yes, ≥0 | evidence items consumed **in array order** (deterministic); `supports`/`attacks` map hypothesis id → weight |
| `input.evidence[].text` | no | free text (ignored by the engine; carried for human audit) |
| `ground_truth` | yes | must name one of the hypotheses (used only for the `correct` flag) |

Weights are **fixed-point thousandths** as JSON integers (`700` = 0.700;
negative allowed). `supports` adds to the hypothesis's score; `attacks`
subtracts. Unknown keys at any level are skipped (so `label`/`text` and future
extensions don't break the parser).

## Parser subset and limits

The Phase-1 parser supports objects, arrays, strings, and signed integers.
Strings must not contain `"` or `\` (no escape processing); control characters
are rejected. Anything outside the subset is a deterministic parse error
(`E_PARSE_<code>` in results, `ERROR` step in the ledger) — the run continues
with the next line.

Hard caps (documented, deterministic): 16 hypotheses, 64 evidence items,
16 support links and 16 attack links per evidence item, 65536 bytes per line,
4MB items file. Exceeding a cap is a parse error, never silent truncation.
Duplicate hypothesis/evidence ids are errors. Links must reference known
hypothesis ids.

## Honest scope

The harness does not interpret natural language. The battery crew encodes
observations/premises as weighted `supports`/`attacks` links; the harness
supplies the genuine deliberative machinery over them: sequential evidence
gathering, eliminative scoring, explicit refutation tests of the runner-up,
confidence from the surviving margin, and a deterministic stopping rule. The
`text` fields exist so a human auditor can check that the encoded weights
faithfully represent the underlying material.
