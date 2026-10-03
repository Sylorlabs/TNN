# L3C-ADVERSARY Phase 1: Independent Reproduction Report

Date: 2026-09-30. Lane: L3C adversary (reproduction + attack).
Target: L3C-FORM-PASS, result commit e663864f5, prereg dc9a91501.
Compiler: znc 2026.07.0-dev (edition 2026), pinned at
~/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc.

## Method

Rebuilt from committed source ONLY. No copied binaries. The committed
binary l3c_form_bin from e663864f5 was never executed or copied.

- Extracted l3c_form.zag from e663864f5 via `git show` into this
  directory as l3c_form_src.zag.
- Source sha256 661454ca78cd7040585a7c4b3a394fea19ea9157aa5b2f45c17bae3c02bd4f64
  matches the committed blob byte for byte.
- `znc check l3c_form_src.zag --strict --no-zagd`: OK.
- Built fresh binary l3c_repro_bin from that source.
- Ran `./l3c_repro_bin 1` three times and `./l3c_repro_bin 0` once.
- Compared with `cmp` against the committed run1.txt, run2.txt,
  run3.txt, run_abl.txt extracted from e663864f5.

## Outcome

- run1: BYTE-IDENTICAL to committed run1.txt
- run2: BYTE-IDENTICAL to committed run2.txt
- run3: BYTE-IDENTICAL to committed run3.txt
- run_abl: BYTE-IDENTICAL to committed run_abl.txt

Zero discrepancies. Phase-1 reproduction: PASS.

## Notes

- The znc analyzer emits 15 non-fatal warnings (dead `+ 0` additions,
  discarded return values of observe/construct). These are style notes;
  the build succeeds and the outputs are byte-identical, so behavior is
  unaffected.
- This report is committed BEFORE any Phase-2 attack file exists
  (kill bar K1). The attack source and attack prereg follow in a
  separate commit.

## Verdict (Phase 1)

REPRO-PASS. The L3C-FORM-PASS result reproduces byte-identically from
committed source with an independent rebuild.
