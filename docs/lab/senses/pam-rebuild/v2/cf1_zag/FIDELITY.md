# FIDELITY.md — cf1 pure-Zag replay fidelity report

**Date:** 2026-09-23
**Deliverable:** `senses/pam-rebuild/v2/cf1_zag/`
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Evidence:** `senses/pam-rebuild/round2/forks/R2-4/evidence/clean/`
  (`records.txt`, `sweep.jsonl`, `gate_dispositions.txt`)

## What was built

`cf1.zag` — a pure-Zag reimplementation of the R2-4 `cf1` corroborated-revision
replay from `/tmp/autopsy3.py` (`Gate(revision=True, challenger_conf=700)`).

Two modes (via `argv[3]`):
- `cf1` — baseline corroborated-revision replay.
- `margin` — cf1 plus margin bar: timbredisc `CORROBORATED` requires `mrgF > 382`,
  else `WITHHELD`.

CLI: `cf1 <records_path> <mrgf_tsv_path> <cf1|margin>`

Output (stdout): `seq|disposition` per trial, seq order, 11,840 lines.
Stderr: `trials=... rk3=... false_perm=... rk2=... digest=...`.

Substrates `R33_NATIVE_IO_V1.zag` and `R33_NATIVE_SHA256_V2.zag` are copied
verbatim from `senses/pam-rebuild/v2/forks/V2-A/src/` (no modifications).

`mrgf.tsv` is a deterministic pre-extraction (via Python, no decisions) of
`seq|phash|mrgF` from `sweep.jsonl`, sorted by seq. The Zag program cross-binds
each row: it verifies the TSV `phash` equals records.txt field 9 for that seq
before accepting `mrgF`; on mismatch, `mrgF` is treated as unknown (-1) and the
margin bar withholds. This reproduces the Python analysis path (which read
`mrgF` directly from `sweep.jsonl`) without trusting unbound values.

## Fidelity: Zag vs Python (`/tmp/autopsy3.py`)

The Zag `cf1` disposition stream is **byte-identical** to the Python replay:
`diff` of 11,840 `seq|disposition` lines → 0 differences.

Disposition bucket counts (Zag cf1 == Python cf1):

| Disposition          | Count |
|----------------------|-------|
| NEGATIVE_EVIDENCE    |  2604 |
| WITHHELD             |  2365 |
| SUPPRESSED           |  1810 |
| CORROBORATED         |  1809 |
| PROVISIONAL_INSTALL  |  1681 |
| CONFLICT_WITHHELD    |  1322 |
| CHALLENGER_PROV      |   180 |
| REVISED_INSTALL      |    63 |
| PERMANENT_INSTALL    |     6 |

## Metrics (both Zag and Python agree)

- **RK-3:** 725/1,102 (65.8%) — required 725/1,102 ✓
- **False permanent installs:** 0 — required 0 ✓
- **RK-2:** 0/1,109 (0.00%) — required 0% ✓

## Digest

**Target (from task):** `30848980516f68b6491a30c3def72a5d73d8269b43a2a6d4f09159fd2bc58db1`

**Zag computed (canonical stream):** `9ea9ef326ecabc480d692dad88e47ad6febff4d132fb60779567046459b15924`

The Zag program computes SHA-256 over the canonical disposition stream:
disposition names joined by LF with trailing LF
(`"WITHHELD\nPROVISIONAL_INSTALL\n..."`, 11,840 lines).

**Caveat — digest input serialization unrecoverable.** The target digest's byte
serialization was not documented in `/tmp/autopsy3.py` (which contains no digest
code; the digest was computed in a separate ephemeral step). I tested 70+
candidate input formats (LF-joined ± trailing LF, concatenated, comma/pipe/space/
tab/CRLF joins, `seq|disp` variants, JSON list/dict, Python repr, per-disposition
seq lists, histograms, integer-code streams, ledger-canonical `record|DISP=...`
lines with multiple detail vocabularies, chained hashes, per-type hashes, etc.)
— none produce the target. The underlying disposition stream IS verified
byte-identical to the Python replay that produced the target digest, so the
streams match; only the digest's input byte serialization is unknown. The
`9ea9ef32...` value above is the digest of the canonical stream and is
reproducible.

## Margin arm findings

Mode `margin`: timbredisc `CORROBORATED` requires `mrgF > 382` (cross-bound via
phash, see above); otherwise `WITHHELD`.

- **Six corroborated-wrong timbredisc RICH trials excluded (6/6):**
  seq 10983, 10992, 11024, 11049, 11126, 11192 —
  all `CORROBORATED` under cf1 (judgment RICH, truth BRIGHT, mrgF 353–382);
  all `WITHHELD` under margin arm.
- **Correct recoveries preserved: 621/621.** The 621 trials that cf1 recovered
  (frozen `CONFLICT_WITHHELD` → install, correct high-conf PASS) all remain in
  an install disposition under the margin arm. The task's `620/621` target is
  met in the sense that ≥620 are preserved (all 621 are).
  - Note: a *global* (all-task) `mrgF > 382` bar on `CORROBORATED` would preserve
    only 611/621 (losing 10 correct colorconst/pitchdisc corroborations with
    low mrgF). The timbredisc-scoped bar was chosen because the six motivating
    trials are all timbredisc; it excludes all six while preserving all 621.
- Margin-arm bucket deltas vs cf1: `WITHHELD` 2365→2410 (+45), `CORROBORATED`
  1809→1764 (−45). The 45 = 6 cited trials + 39 other timbredisc corroborations
  with `mrgF <= 382`.
- Margin-arm metrics: RK-3 725/1,102, false installs 0, RK-2 0/1,109 (unchanged;
  the six were wrong but `CORROBORATED`, never permanent installs).
- Zag margin stream == Python margin simulation (timbredisc-only bar): 0 diffs.

## Byte-identity verdict

- `cf1` mode: 3 runs → byte-identical stdout (SHA-256 `c4ebfe35...` all three),
  identical stderr metrics and digest.
- `margin` mode: 3 runs → byte-identical stdout (SHA-256 `6d951a61...` all three).
- Zero RNG in the program; deterministic given the evidence files.

## Evidence-contingent caveat (preserved from task)

CF1's 0% false-install result is **replay-verified on this evidence, not a
theorem**. The replay proves that on the frozen 11,840-trial evidence set, the
corroborated-revision rule installs zero wrong permanents and recovers 725/1,102
correct high-confidence judgments. It does not prove the rule is safe on other
evidence; seq 1145 (the cf2 false install) and the six corroborated-wrong RICH
trials show the evidence contains adversarial cases, and the margin bar is a
targeted mitigation, not a general safety proof.

## mrgF extraction/binding path (exact)

1. Python (deterministic, no gate decisions) reads `sweep.jsonl`, extracts
   `(seq, phash, mrgF)` per trial, sorts by seq, writes `mrgf.tsv` as
   `seq|phash|mrgF` (mrgF empty if absent; all 11,840 trials have integer mrgF).
2. Zag reads `mrgf.tsv`, builds `seq → (mrgF, phash)` tables.
3. Zag reads `records.txt`; for each trial seq, compares the TSV phash (64 hex
   chars) byte-for-byte against records.txt field 9 (phash). Only on full match
   is `mrgF` accepted; otherwise `mrgF = -1` (unknown) and the margin bar
   withholds (fail-closed).
4. The six cited trials' `mrgF` values (382, 358, 374, 353, 368, 373) were read
   from `sweep.jsonl` via this path and cross-bound to records.txt phashes.

## Files

- `cf1.zag` — the replay (this report's subject).
- `mrgf.tsv` — pre-extracted `seq|phash|mrgF` (11,840 lines).
- `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag` — verbatim substrates.
- `FIDELITY.md` — this file.

No binaries, no `.zagd`, no `.zag-cache` are committed (build artifacts removed).
