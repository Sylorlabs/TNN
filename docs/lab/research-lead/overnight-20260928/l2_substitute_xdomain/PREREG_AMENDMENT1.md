# PREREG_AMENDMENT1: fold-discovery valrel skip + corrected FULL counts

Status: PRE-IMPLEMENTATION amendment to PREREG.md (frozen at
6bed092c3). No implementation exists at this commit. The design
intent is unchanged; this corrects two mechanical details found
while translating the frozen design into implementation
pseudocode (same category as l2_substitute/PREREG_AMENDMENT1.md:
operator semantics clarified before any code exists).

## A1. Fold-walk discovery skips the descriptor's valrel

The frozen PREREG says fold-1 discovers (s1,s2) as "rels of
first live facts with sub==u then sub==a". Applied literally,
the U-chain candidate (entry 17, u=70) breaks: fold-1 finds
f1=(15,70,60), then the first live fact with sub==60 is the VAL
fact (60,2,20) [fid 16], so s2=2 and the walk dies at the next
hop. The correct grounding would be unreachable, which is not
the frozen intent (the prereg hand-derivation assumed the chain
fact (60,16,71) is found).

Correction: fold discovery skips facts whose rel equals the
source descriptor's d_valrel. Rationale (principled, generic):
d_valrel identifies the value-annotation relation (discovered at
teach time from the source MAP, never hardcoded); value
annotations are not structural hops, so structural fold search
skips them. Folds 2..nf are unaffected (they already require
rel==s1/rel==s2, which excludes valrel facts by mismatch).

Recounted FULL adapt cost with the skip (counting rules
unchanged: +1 per fact id examined):
- steps-MAP search: 3; capsearch: 2; entry scan fids 0..20: 21.
- (7,51): 13+16+38 = 67 (unchanged).
- (8,60): fold1 s1scan 0..22=23 (fid 16 skipped as valrel,
  s1=16 at fid 22), s2scan 0..23=24 (s2=15); fold2 25+26;
  fold3 27+38 (fail at last hop) = 163.
- (17,64) decoy: folds 29+30+31+32+33+34=189 (unchanged);
  arity two-phase: VALs 35+36+37=108, LINK 38 fail = 146.
- (17,70): fold1 22+23; fold2 24+25; fold3 26+27 = 147;
  arity: VALs 17+18+19=54, LINKs 14+15+16=45 = 99.
- verify VALscan (2,73): 28.
- FULL A_SEARCH = 3+2+21+67+163+(189+146)+(147+99)+28 = 865.
- FULL A_EXEC = 3 (collect + verify + deliver), unchanged.

## A2. Arity check is two-phase, as traced

Confirming the frozen trace: phase 1 VALscans all addends
(records addvals), phase 2 LINKscans all addends (uniform-rel
requirement, records cost_rel). The frozen trace line
`XA-ARITY u=64 addvals=1,2,3 LINK-FAIL` stands as written.

## A3. Corrected frozen expectations

- FULL: A_SEARCH=865 (was 671), A_EXEC=3 (unchanged).
  F-COUNT now reads: FULL A_SEARCH != 865 or A_EXEC != 3.
- Informational (not bars): NOADAPT A_SEARCH=552, A_EXEC=2;
  ABLATE-Y A_SEARCH=684.

All kill bars K1-K8, all other frozen expectations, and the
audit spec are unchanged.
