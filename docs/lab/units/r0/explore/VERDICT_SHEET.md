# EXPLORE VERDICT SHEET — R0 crew EXPLORE (non-binding track)

**Date:** 2026-09-21
**Status: EXPLORATORY / NON-BINDING.** Per PREREG_FREEZE.md §14 ("be more wide"):
findings may PROPOSE future amendments but CANNOT change frozen bars (R-1..R-9,
B-T1..B-T5, K-R1..K-R10, A-1..A-58, M-1..M-57, T-1..T-16 — all PROPOSED, none
touched). Every proposal below names the exact frozen bar it would amend.

**Artifacts** (all in `docs/lab/units/r0/explore/` after commit):
- `01_EXTRA_CORPORA.md` — license-clean corpus survey + ranked proposals
- `02_ADVERSARIAL_PROBES.md` — three executed pure-Zag probes + four further designs
- `03_R23_ANCESTRY.md` — R23 teaching-experiment analysis from recovered source
- `04_CACHE_LAYER_DESIGN.md` — content-addressed ID / invalidation / ghost-ID sketch
- `probe_rep.zag` / `probe_id.zag` / `probe_pressure.zag` (+ `_run1.log` each)

All probe code: pure Zag, zero RNG in any decision path, N=2 runs byte-identical.

---

## Ranking — most likely to matter

### 1. Adversarial probes (02)
The only probe family that produced *binding-shaped* evidence while staying
non-binding: (a) the giant-span exploit fires at span length 2 under a naive
gain bar — R-2 is load-bearing, quantified; (b) the use-inflation ambush takes
pure-LFU from 8/8 to **0/8** valuable survival — the G1 threat model made
quantitative, and it fires below occupancy thresholds; (c) the tombstone/generation
tension gives Micah's A-4 ID-width decision a concrete input (pure content-hash
cannot satisfy "tombstoned IDs never reused"). Would amend: R-2, A-16, M-14,
A-24, A-47, A-4.

### 2. R23 ancestry (03)
Recovered a genuine *prediction* from the exact R23 source, not just context:
uncertainty-first peer teaching beat fixed-curriculum master teaching
(`PASS_BOUNDED`), and the mechanism was *selection*, not authority — with teacher
testimony always discounted below direct consequence (1.0 / 0.75 / 0.6). This
bears directly on Track B's unset verdict weights (T-14) and on whether the
teacher track has R23's heaviest channel (an independent `'DIRECT_WORLD'`). Would
amend: T-14, T-11, T-8, A-33/arm-O sub-bars (+ proposed T-17).

### 3. Cache-layer sketch (04)
Needed before the K-arms and D can be built coherently: the
`(content_hash, generation)` ID, the revise→tombstone→re-key invalidation
protocol, and the four ghost-ID rules are all probe-validated at small scale.
Its sharpest point is a negative: K1-as-pure-content-hash is incompatible with
A-47 as written. Would amend: A-4, A-24, A-47, M-32 (dedup accounting for
remix-minted IDs).

### 4. Extra corpora (01)
Useful but downstream: corpora discriminate mechanisms, they don't validate
them. The ranked proposals (multilingual UTF-8 as a correctness gate, NASA logs
for M7/K-arms, minified JS as the honest C-W pricer, FASTA DNA as the degeneracy
discriminator) are ready when Micah signs M-5's third-corpus choice. Would amend:
M-5, M-1 (byte legality), M-28, R-1 (DNA grounding).

---

## Most surprising finding

**Pure content-addressed IDs are incompatible with "tombstoned IDs never
reused" — and the probe caught the implementation violating it before the
write-up did.**

The first version of `probe_id.zag` implemented the textbook content-hash store
("same bytes → same ID"). Its own ghost-ID test then demonstrated the violation:
re-adding the original bytes after a tombstone silently re-issued the tombstoned
ID to a live slot — a resurrection the design forbids. The fix (deterministic
tombstone-remix, i.e. a generation stamp: `ID = (content_hash, generation)`)
is what all 13 checks now validate. The surprise is structural, not a bug in
one probe: **K1's core promise and arm D's tombstone law cannot both hold for
the same ID.** One of them must yield to the K3-hybrid direction, and that is
now a dated, evidenced input to Micah's A-4 unification decision rather than an
argument.

Runner-up surprise (apparatus): the pinned znc's ZNC-2026-09-19-001 defect was
independently re-derived in the first hour (3+ sequential `[]i32` stores corrupt;
`[]u8` stores are fully reliable) — the probes now document a working
`[]u8`-backed cell pattern for the core/harness crews in `r0/impl/`.

---

## What was NOT done (honest gaps)

- The four further attack designs in 02 (split/merge oscillation, cross-TNN ID
  spoof, teacher-wire smuggling, ledger flooding) are designs only — no code.
- No corpus was actually downloaded or hashed (M-30 stays with the frozen track).
- The R23 verdict constant is `PASS_BOUNDED` from recovered source; the numeric
  margins were not re-derived (the Python source needs torch; re-running it is
  the frozen track's business, not this one).
- The `ghost#1` Google Doc flagged in ARCHAEOLOGY_R31.md ("vocabulary" match,
  needs the Docs skill) was not read — flagged, not blocking, per the archaeology sheet.
