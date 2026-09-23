# Note — sweep `nev` self-check correction

The sweep harness (`eval/eval_h1.py cmd_sweep`) embeds an inline validator that
asserted `nev == <count of ev: lines>`. That validator predates the frozen
`nev` semantics (PREREG_H1.md §4: `nev = 1 + number of alternatives`, i.e.
event lines + alternative lines) and is therefore stale: it emits strings
like `nev=13 but 5 ev lines` into the run JSONLs' `errors` field.

What was verified:

1. A 72-fixture stratified re-parse audit (all 6 tasks × 3 variants,
   incl. misleading fixtures) recomputed `nev` from the raw stdout text as
   `ev-lines + alt-lines` and matched the reported `nev` in **72/72**.
2. No non-`nev` errors occur in any H1 run (all rc=0).
3. stdout hashes are unaffected: the stale strings live in the test-glue
   JSONL wrapper, not in the binary's stdout.

Metrics handling: `cmd_metrics` ignores `errors` entries beginning with
`nev=` (the stale self-check only) and treats any other error as fatal.
rc!=0 records are excluded from scoring exactly as the frozen harness does
(`run.py` files them under "errors"; the only such record is the harness's
own known A error on shapetrans/adversarial/p042.img, reproduced identically).
