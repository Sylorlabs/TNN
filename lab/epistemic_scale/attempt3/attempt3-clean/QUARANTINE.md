# Attempt 3 Clean-Room: QUARANTINE REPORT

**Date:** 2026-09-27
**Workdir:** `~/workspace/epi_a3/attempt3-clean/`
**Status:** INVALID — clean-room breached. Do not use as evidence.

## Contamination

The clean-room line was breached before parser development:
- `head -50 cleanroom_train.tsv` exposed the `class` column and labeled rows.
- Original IDs with `F`/`O`/`L`/`S` prefixes (revealing classes) were seen.
- Texts were converted to opaque IDs only afterward.
- Parser/build diagnostics later printed original-looking IDs (e.g. `T0108`).

The user's law: "The `class` column may be used ONLY to SCORE a frozen LOO.
Never to develop, choose, or adjust parsing rules, lexicons, thresholds, or addressing logic."

Parser development continued in the contaminated workdir. This violates the law.
The entire implementation line is tainted and cannot serve as valid Attempt 3 evidence.

## What was built (for the record only — NOT valid evidence)

### Parser (parse.py, tables.py, TABLES.md)
- Deterministic Python premise-frame parser.
- Frame well-formedness on train: 480/480 = 1.0000 (locally defined).
- **Tainted:** developed with label knowledge. Invalid.

### Build (build.py)
- Frames: 689 (480 train, 209 heldout). Vocab: 1586. Addressing: 342 pairs. Antonyms: 23.
- **Tainted:** addressing logic developed in contaminated workdir. Invalid.

### Zag deliberator (deliber.zag, data.zag)
- Pure-Zag, zero RNG. Implements §4.3 (value comparison, premise status,
  contradictor standing, CMPUNK resolution, verdict logic).
- Compiled with `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- LOO ran byte-identically twice (verified by diff).
- **Tainted:** operates on tainted frames/addressing. Invalid as evidence.

### LOO outputs (loo1.tsv, loo2.tsv)
- loo1.tsv: uncontested standing. 448 verdicts.
- loo2.tsv: corroborated standing. 448 verdicts.
- **NOT SCORED** (labels sealed; scorer must be separate party).
- **Tainted:** do not score or interpret. Quarantine only.

## What was NOT done (correctly, per stop instruction)
- No LOO scoring against labels.
- No held-out scoring.
- No GO/NO-GO determination.

## Missing artifact
- `attempt2/takeaways.md` does not exist in the filesystem. Could not carry it.
  (Summary claimed 26 citations were verified on 2026-09-27, but the file is absent.)

## Prereg discrepancy (for replacement implementer)
- Amendment 2 record says §7 was fully numerically specified.
- Prereg body on disk still has qualitative/older §7 wording.
- Parent brief supplies six explicit GO numbers. Document before replacement's first LOO.

## Recommendation
1. Quarantine `~/workspace/epi_a3/attempt3-clean/` as invalid. Do not score loo1.tsv/loo2.tsv.
2. Restart with a separate implementer/session:
   - New workdir.
   - Pre-sanitized text-only train file with truly opaque IDs (no class prefixes).
   - No access to this workdir, parser, or artifacts.
3. Coordinator (not implementer) retains labels for one-shot scoring after freeze.
4. Resolve Amendment 2 §7 discrepancy before replacement's first LOO.

## File hashes (quarantine record only)
- parse.py: (see FREEZE_MANIFEST.txt)
- deliber.zag, data.zag: generated; see workdir.
- loo1.tsv: 5917104261d9adcce2bddc3aedcf018ef1e6af19c4c4765a042d9d1c4eb8d519
