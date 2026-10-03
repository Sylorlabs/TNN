# SHA256SUMS record-defect repair: wave-20260927-0821pdt (lane 1)

## What was wrong

The wave-20260927-0521pdt verdicts recorded a record defect:
docs/lab/rsi/fit_authority/SHA256SUMS did not exist. The frozen pins lived
only as prose in fit_authority/README.md, so a third party could not verify
the authority path with a single standard command (sha256sum -c). The repair
was assigned to this wave's lane 1.

## What was written

Created docs/lab/rsi/fit_authority/SHA256SUMS, following the same convention
as other SHA256SUMS files in this repo (plain sha256sum output, paths
relative to the directory holding the file, header comment documenting scope
and the verification command).

It covers all nine files currently in the authority path:

- tnn_chat.zag (baseline probe instrument source)
- tnn_chat_decline.zag (decline-gate probe instrument source)
- kb.txt (canonical 38-fact closed-book knowledge base)
- gaz.txt (gazetteer)
- fixtures/kb1_out30.txt (KB1 probe fixture, 30 adversarial out-of-KB turns)
- fixtures/kb2_inkb.txt (KB2 probe fixture, 17 in-KB turns)
- fixtures/kb5_nogame.txt (KB5 probe fixture, 10 in-KB turns)
- README.md (the authority record itself)
- AUTHORITY_MANIFEST.md (the manifest itself)

Before writing, every file's sha was verified byte-exact against the frozen
pins in README.md and AUTHORITY_MANIFEST.md: all matched. The fixture shas
were additionally verified against the FIT_1421.md evidence record: all
matched. One correction was made during drafting: the initial draft carried
invented placeholder shas for README.md and AUTHORITY_MANIFEST.md; they were
recomputed with sha256sum and corrected before the file was committed. No
placeholder values remain.

## Verification by a third party

From the repo root:

  cd docs/lab/rsi/fit_authority && sha256sum -c SHA256SUMS

Result at commit time: all nine files OK. Any future mismatch fails loudly
through the standard tool, which is exactly what the record defect was
missing.

Note: the frozen built-binary pins (1ada2fae... baseline,
20273a99... decline) and the pinned toolchain pin (498abcb5...) remain in
README.md prose because those files do not live under this directory; this
wave's FIT re-run independently re-verified all of them (rebuilt binaries
byte-identical to the binary pins, znc sha verified on
src/tools/toolchain/znc_linux_x86_64_abed8aa1).

## Python-contact statement

Zero Python. The file was written and verified with sha256sum only.

## Caveats

SHA256SUMS covers the authority path files only. It does not certify the
R33 support sources, the toolchain, or any candidate work. It certifies the
38-fact closed-book probe chain only.
