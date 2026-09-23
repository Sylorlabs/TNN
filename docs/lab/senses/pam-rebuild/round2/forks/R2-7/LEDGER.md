# R2-7 Ledger Format

## Format
Each line: `fixture=<id> task=<task> judgment=<j> conf=<c> challenge=<ch>
outcome=<o> disp=<d> ops=<n> hash=<hex>`

- `fixture`: `r2fx_t<task>_i<index>_f<family>` or `legacy_<task>_p<idx>`
- `task`: colordisc, colorconst, shapetrans, pitchdisc, timbredisc, motiondir
- `judgment`: formation claim (e.g. SAME, CIRCLE, N)
- `conf`: confidence 0-990
- `challenge`: CH-COL-1, CH-CCN-1, CH-SHP-1, CH-PTC-1, CH-TMB-1, CH-MOT-1,
  or NONE (legacy)
- `outcome`: challenge outcome code, or UNRESOLVED
- `disp`: INSTALL or WITHHOLD
- `ops`: operation count (integer)
- `hash`: SHA256 hex of (prev_hash_raw || content_bytes)

## Hash chain
Each entry's hash = SHA256(prev_hash_raw_bytes || content_bytes).
Genesis prev = 32 zero bytes. The `audit` mode verifies:
1. Each line parses (9 fields).
2. Each hash recomputes correctly from prev + content.
3. Chain links (prev of entry N+1 == hash of entry N).

## Determinism
Byte-identical reruns: same fixture + fresh ledger → identical stdout
(excl. ledger_seq) and identical ledger hash. Verified in B6.
