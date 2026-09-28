# Counts and hashes (independent re-runs, 2026-09-26)

Toolchain: znc_linux_x86_64_abed8aa1 (pinned)
Adoption commit: 94625817c6f65e07c4ac99abde5dd533f0e810a5

S1: 160 output files (36 cells x2 + 4 gates x2, pre+post), combined sha256 e4d886233d26d0887d0cc8d25e047ce3b33cbb2d794e053c4786a9329d5654b3
S1 executions: 160 (36 cells x2 pre + 36 cells x2 post + 4 gates x2 pre + 4 gates x2 post), 0 failures
wedge pre_run1.out: 628 lines, WB_VERDICT fail=0, sha256 88c80225c99073c1
wedge post_run1.out: 628 lines, WB_VERDICT fail=0, sha256 88c80225c99073c1
wedge: pre run1 == pre run2, post run1 == post run2, pre run1 == post run1 (byte-identical)
adopt_run1.out: 531 lines, sha256 d6ba675074a52c74
meter_run1.out: 10 lines, sha256 01037fb7302a8b30
adopt_test: 50 ADOPT_PASS / 0 ADOPT_FAIL (x2 byte-identical)
meter_test: 8 METER_PASS / 0 METER_FAIL (x2 byte-identical)

## Fresh red-team (this battery)
r1: RT_R1 total=120 fails=0 holes=0, sha256 0620d35544eb91cc6cc9cd95c29f6a4ff68743b7a0ca7a91a39c4c6b4a63bd46
r2: RT_R2 total=128 fails=0 holes=0, sha256 c82240f4968961172914329a37e9bc2c37bd673b577ea220360482536c3d020d
r3: RT_R3 total=108 fails=0 holes=0, sha256 b090e2c671341f2283c33ecb71a692bff3ff4df85dae34fb340f60fb1b9b9d25
r4: RT_R4 total=105 fails=0 holes=0, sha256 0335e6b923cf540acc7f5e1109417694aa3bccd8ecd04c0a003b38aeeaca6421
r5: RT_R5 total=120 fails=0 holes=0, sha256 0deea2fe3befd2b8db546832025267d88f94376adeb2849ed7ae98fd95bf35dc
r6: RT_R6 total=104 fails=0 holes=0, sha256 59f375152843ed736804c07bd1536c3d749a4fcbf21ce8659986157b24bbd093
TOTAL red-team sequences: 685, failures: 0, holes: 0
Each battery ran twice; run1 == run2 byte-identical (cmp).
