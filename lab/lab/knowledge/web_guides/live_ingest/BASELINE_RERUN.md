# Baseline rerun — pilot run_pass1 byte-identity check

2026-09-23. The pilot-era LI run (`docs/lab/knowledge/web_guides/live_ingest/run_pass1/`)
was re-executed with the era-correct driver to confirm the frozen stack
reproduces the committed pilot ledgers byte-for-byte.

## Setup

- Driver: pilot-era `run_li_pilot.py` from commit `7daba782`
  (`docs/lab/knowledge/web_guides/live_ingest/run_li.py`, pre-fidelity-gating
  version), SHA-256 `d2c728fcdc2cbfea0bff09208086e5134d7fbb82fc827d9429ea191ff79c2823`.
  (The branch HEAD driver adds fidelity gating + exact teach-validation
  wording; the baseline must use the historical driver that produced the
  committed artifacts.)
- Instrument: frozen `webg` binary (byte-identical to pinned-toolchain
  rebuild of frozen `webg.zag` md5 `c1ea3e71a93205dd6facf61667c3f442`).
- Inputs: pilot `urls_pilot.txt` + `corpus_snap/` (19 snapshot files),
  byte-identical copies of the committed inputs.
- Output dir: `rerun_pass1/` (fresh).

## Result

```
DONE|clusters=7|installed=0|withheld=9|sha_log=3156a760c8511fccbf664ca623003817bc7cc653943a8d6ddac96968d3f73741|sha_knowledge=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855|sha_refusal=e21300eb800ad95994c9f0283c8f27ecff531cf9a22aa03449159a289ee7d499
```

Byte comparison against committed `run_pass1/` artifacts:

| file | result |
|---|---|
| `knowledge_ledger.txt` | BYTE-IDENTICAL (`cmp` clean) |
| `refusal_ledger.txt` | BYTE-IDENTICAL (`cmp` clean) |
| `run_li.log` | BYTE-IDENTICAL (`cmp` clean) |

Committed pilot result (7 clusters, 0 installs, 9 withholds: 7×
NO_CORROBORATION + 2× UNSUPPORTED_FETCH) reproduces exactly on the frozen
stack. Baseline verified.
