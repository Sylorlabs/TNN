# PREREG_AMENDMENT2: corrected FULL A_SEARCH 865 -> 941

Status: PRE-VERDICT amendment to PREREG.md (frozen 6bed092c3) as
amended by PREREG_AMENDMENT1.md (frozen d6d8e01ee). Implementation
exists and runs; this corrects a pure arithmetic slip in the
hand-derived FULL A_SEARCH expectation. No design, algorithm, or
counting-rule change (same category as
l2_substitute/PREREG_AMENDMENT2.md: arithmetic correction only).

## The slip

The hand derivation assumed the arity check's LINK phase stops
at the first failing addend (38 ticks for the decoy). The frozen
counting rules say "+1 per fact id examined", and the
implementation examines every addend (no early exit in the LINK
loop). For the decoy candidate (17,64): LINK scans run for all
three addends (74, 75, 76), each a full 38-fact scan with no
match: 3x38 = 114, not 38.

## Corrected FULL derivation

- steps-MAP search: 3; capsearch: 2; entry scan fids 0..20: 21.
- (7,51): 13+16+38 = 67.
- (8,60): 23+24+25+26+27+38 = 163.
- (17,64) decoy: folds 189 + VALs (35+36+37)=108 + LINKs
  114 = 411.
- (17,70): folds 147 + VALs (17+18+19)=54 + LINKs
  (14+15+16)=45 = 246.
- verify VALscan (2,73): 28.
- FULL A_SEARCH = 3+2+21+67+163+411+246+28 = 941.
- FULL A_EXEC = 3 (unchanged).

F-COUNT now reads: FULL A_SEARCH != 941 or A_EXEC != 3.

The implementation's F-COUNT check is updated from 865 to 941
to match; this is the arithmetic correction, not a weakening
(the bar is exact-equality either way). All kill bars K1-K8,
all other frozen expectations, and the audit spec are
unchanged.
