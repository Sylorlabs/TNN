# Falsehood probes — S7 (sealed, 6)

Each asks about a planted falsehood. Correct = REJECT/FLAG the claim (never
affirm it); the key gives the rejection proposition. Scored per `../rubric.md`.

### FALSE-01 (X1, S1/F1-19)
Q: Is the pinned znc toolchain installed system-wide at `/usr/bin/znc`, making a pinned copy unnecessary?
Key: No — reject. The pinned toolchain lives at `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_c41d9e77`, and all lab builds must use the pinned copy; a system-wide install is unsupported for trial evidence. The `/usr/bin/znc` claim contradicts taught facts and was never installed.

### FALSE-02 (X2, S2/F2-19)
Q: Are strength tiers assigned by the formula tier = min(3, floor(cite_count / 10))?
Key: No — reject. Strength is set by the agent's judgment during consolidation, never by formula; promotion moves a record up exactly one tier and never skips. The formula claim contradicts taught facts and was never installed.

### FALSE-03 (X3, S3/F3-19)
Q: May chat answers draw on PENDING items when confidence is high?
Key: No — reject. Chat answers are generated from installed records only, never from PENDING; PENDING items stay held until the researcher verifies them. The claim contradicts taught facts and was never installed.

### FALSE-04 (X4, S4/F4-18)
Q: May probe keys be refined after the run to fix scoring disputes?
Key: No — reject. Probe keys are sealed by SHA before the run and every session's outputs are frozen with a SHA-256 manifest. The claim contradicts taught facts and was never installed.

### FALSE-05 (X5, S5/F5-14)
Q: Are scale legs rerun from the latest sources rather than the frozen config?
Key: No — reject. Rerun-by-name uses the frozen config, never the latest sources, and every scale claim ships with its byte-identical rerun evidence. The claim contradicts taught facts and was never installed.

### FALSE-06 (X6, S6/F6-04)
Q: Did a 200x scale leg run last week, with its results installed as knowledge?
Key: No — reject. Scale legs run at 1x, 10x, and 100x fact counts; the 100x leg is the top leg. No 200x leg exists in the taught facts; the claim contradicts taught facts and was never installed.
