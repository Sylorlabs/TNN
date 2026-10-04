# Fork D: Write-Once Evidence Partition — Final Report

**Date:** 2026-09-27 | **Branch:** `tnn-native-lab` | **Crew:** D production drive, Crew C

## What was built

Fork D's trust root was a text label. Every store line ended with `|EXT`
or `|GEN`, and the checker believed the label: change `GEN` to `EXT` on a
generator-authored fiction and fork D installed it as fact. The red team
proved this with the M5L-001 laundering probe — "The zorp is a qux"
went from generator fiction to installed belief with a one-word edit.

We replaced the label with physics. There are now two append-only
partitions per corpus:

- **EXT partition** — the evidence partition. Each entry carries a
  WOTS one-time signature (w=16, 67 hash chains) over the atom plus a
  hash chain linking it to the previous entry. The first entry's key is
  pinned in the verifier binary (`genesis.zag`). Only the independent
  channel, holding its private seed outside the repo, can mint a valid
  entry.
- **GEN partition** — the generator's partition. Hash-chained for
  tamper evidence, but unsigned and always distrusted. The generator can
  write here freely; nothing in GEN can ever become EXT.

The fork-D discipline kernel (prover + deliberation checker) was rewired
to consume **verified partition membership** instead of parsing the
sixth field. `prover.zag` builds closures directly from attested atom
lists; `delib.zag` checks exact membership in the attested EXT set. The
`PROV` label no longer exists anywhere in the pipeline. If either
partition fails attestation, the whole battery fails closed: every draft
withholds with the atoms marked `EXT_UNVERIFIED` / `GEN_UNVERIFIED`.

Everything is pure Zag compiled with the pinned toolchain
(`znc_linux_x86_64_abed8aa1`), zero RNG, deterministic. The channel tool
(`channel.py`) signs offline with an externally held seed (Amendment 02);
no seed is committed anywhere.

## Measured results vs the preregistered bars

| Bar | Requirement | Result |
|-----|-------------|--------|
| B1 | All laundering/forgery/tamper cases fail closed | **PASS** — 4/4: forged zorp append (`sig-invalid`), bit-flipped signature (`sig-invalid`), reordered entries (`prev-mismatch`), fully forged attacker chain (`genesis` reject). The M5L-001 laundering case: old world INSTALLs "The zorp is a qux", new world WITHHOLDs. |
| B2 | 100% per-case verdict agreement with original fork D (non-launder) | **PASS** — 652/652 cases agree (c1 140, c2 140, c3 130, c4 60, c5 60, c6 40, m2a 25, m2b 25, m4 24, m5 8). |
| B3 | Genuine generator-authored recursion still withholds (`GEN_ONLY`) | **PASS** — m5: 8/8 WITHHOLD. |
| B4 | Byte-identical full reruns; no RNG | **PASS** — all 12 corpora byte-identical across two full runs; `grep` for `rand\|rng\|clock\|time(\|getrandom` across all Zag sources: zero hits. |

Additional measured facts:

- M2 meaning-flip pairs: m2a 25/25 INSTALL on base drafts, m2b 25/25 WITHHOLD on flipped drafts — the partition preserves the paraphrase/meaning distinction exactly.
- M4 trace alibis: 24/24 WITHHOLD (unchanged).
- c2 has 5 cases where both old and new implementations WITHHOLD against an `INSTALL` expectation in the manifest (M2-108/109/110/113/116). This is a pre-existing corpus property, not a regression — the two implementations agree 140/140.
- The pure-Zag WOTS verifier and the Python channel mirror agree on every tamper case, including the exact failure reason (`sig-invalid`, `prev-mismatch`, `bad-hexlen`, `genesis`).
- Attestation cost: ~2s CPU per 72-entry partition (one-time per battery); per-case kernel work unchanged from the original.

## What remains open

1. **Key custody is the channel's problem.** This experiment proves the
   wiring is possible and behavior-preserving; it does not make the
   external seed unstealable. Production use needs a real custody story.
2. **WOTS is one-time per index.** The chained-key construction handles
   this, but a production system would want a proper stateful scheme or
   hash-based signatures with a formal proof.
3. **The 5 c2 expectation mismatches** (pre-existing, both worlds agree)
   suggest the c2 manifest's expectations need a dated correction, but
   that is outside this experiment's scope.
4. **Performance.** Pure-Zag WOTS verification is ~2s per 72-entry
   partition — fine for batteries, but a production verifier would want
   the signature check in the substrate or a faster hash path.

## Verdict

**The wiring is possible, and it is done.** Fork D's discipline now runs
over partition membership instead of a forgeable label, with zero
measured change in verdicts across 652 cases and fail-closed behavior
under every forgery in the red-team family. No impossibility proof was
needed — the mechanism works.

## Score summary

```
B1: 4 attack cases — WITHHOLD: 4/4
B2: per-case agreement new-vs-original: 652/652
B3: m5 genuine recursion WITHHOLD: 8/8
total checks: 1316
ALL BARS PASS
```

## Artifacts (all committed)

- `docs/lab/senses/pam-rebuild/selfpam/r2/forkD/AMENDMENT_02_SEED.md`
  (frozen, committed alone as `fcfbb9be`)
- `docs/lab/senses/pam-rebuild/selfpam/r2/forkD/forkd2/` — full
  evidence tree: Zag sources, `channel.py` (no seed), `genesis.zag`,
  signed partitions, manifests, both battery runs, digests, scores
- This report
