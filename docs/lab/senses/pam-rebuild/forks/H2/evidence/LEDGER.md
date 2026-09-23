# H2 Ledger — SHA-256 Hash Chain

The H2 memory contract (`memgate.zag`) appends one hash-chained link per
trial to an append-only ledger. The ledger binds every percept program to
its disposition and to all prior trials.

## Link construction

For trial `i` (0-indexed, in memgate feed order):

- `prev`: 32-byte previous link (genesis: 32 zero bytes).
- `record`: the full input record line:
  `seq|tcode|fixture|prog|jcode|judgment|confidence|pred|measure|phash|truth`
- `disp`: the disposition assigned by the contract (e.g. `PERMANENT_INSTALL`).
- `detail`: disposition detail (e.g. `corroborated`, `neg`, `reversed_old=42`).
- `canonical = record + "|DISP=" + disp + "|DETAIL=" + detail`
- `link_i = SHA-256(prev_raw32 || canonical_bytes)`

The ledger file contains one line per trial:
`<prev_hex>|<link_hex>|<canonical>`

Where `prev_hex` and `link_hex` are lowercase hex of the 32-byte values.

## Independent verification

The ledger is verified by recomputing every link with Python `hashlib`:

```python
prev = "00" * 64
for line in open("ledger.txt"):
    p, h, canon = line.rstrip("\n").split("|", 2)
    assert p == prev
    assert hashlib.sha256(bytes.fromhex(p) + canon.encode()).hexdigest() == h
    prev = h
```

The eval harness (`eval_h2.py`) performs this verification automatically
and reports `ledger_verified` in `metrics.json`.

## Properties

- **Tamper-evident**: changing any record, disposition, or prior link
  invalidates all subsequent links.
- **Deterministic**: the same record stream always produces the same
  ledger (byte-identical).
- **Bound to programs**: the `phash` field in each record is the SHA-256
  of the full `program=` text emitted by `sense_h2`, binding the ledger
  to the actual percept program bytes.
- **Truth is pass-through**: the `truth` field is copied to the ledger
  for scoring but is NEVER used in any gate rule (the contract does not
  see the future).

## B6 replay

60 frozen-primary fixtures (10 per task) were run three times each
through `sense_h2`. All 180 outputs were byte-identical. The ledger
links for those trials were independently recomputed and verified.

## Verification records (2026-09-23)

### B6 determinism ledger (60 records)

- 3 runs of `memgate` over the 60-record determinism set: byte-identical
  (16,528 bytes each).
- Independent Python `hashlib` recomputation: 60/60 links valid.
- Ledger SHA-256:
  `f4be66fbfeca3a9cd2d8506a1ffeeafdc9ab6302b2a779f2091ba57a9a4fa223`
- The same SHA was produced by the pre-fix memgate binary and by the
  binary rebuilt from the committed (post-fix) `memgate.zag` — the fixture
  buffer fix changes no ledger bytes on this record set.
- Artifacts (scratch): `evidence/_evalwork/det_records.txt`,
  `det_ledger_0/1/2.txt`.

### Full 10,000-trial ledger

- 10,000 valid links; independent full-chain recomputation: PASS.
- Ledger SHA-256:
  `a1a8b21fb4d65df6f1f02572a687168f5b17898608ef5f39d77e90d65acd8847`
- Ledger bytes: 2,917,419.
- The binary rebuilt from the committed (post-fix) `memgate.zag` produces a
  byte-identical ledger and identical dispositions (0/10,000 differ) to the
  pre-fix binary — the fixture-buffer fix changes no ledger content.

### KB1 tamper/malformed probes

- 10 tampered ledgers (edited link payload): 10/10 detected at the edited link.
- 10 malformed ledgers: 10/10 rejected.
- Result: 20/20 caught.
