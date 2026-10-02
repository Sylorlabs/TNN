# DEVANG4 Build Log (wave-20261002-0221pdt)

## File creation order
1. `NAMECHECK.md`: Step 0 (safebin, toolchain verification) + Step 0c
   near-miss disclosure.
2. `PREREG_DEVANG4.md`: frozen prereg. Committed ALONE at c768b02be
   (with NAMECHECK.md, per 2321pdt precedent; no implementation).
3. `baseline/familyd_utt.txt`, `baseline/familyd_eps.txt`: prereg-frozen
   Family D inputs (6 utterances / 6 episodes).
4. Baseline measurement (post-freeze, pre-implementation; frozen binaries):
   - 2321pdt `devang3` (sha 36f5047d...) `segb` on Family D utterances,
     3/3 runs: exit 0, zero stderr, byte-identical
     (sha 8b00ffebb76979d8c982a9d33dbff54f0dd9b184af9a015ab0c8e3f79e932327).
     Output: all six shatter to `3,6,8` ([tak][X][yy][Z]). Score 0/6.
     K_DISC premise (<= 2/6) HOLDS.
   - 2021pdt `devang3` (sha 7006ce4d...) `segb`, 3/3 byte-identical
     (sha afd728b3ea0bb2151aaf6d0ca0a2819687fd80ef34d90bf5c5965366c1648e09).
     Output: four `3,6` ([tak][X][yyZ] merges) + two `3,6,8` shatters.
     Score 0/6. Secondary baseline confirms the family discriminates
     against both prior builds.
5. `devang4.zag`: copied from 2321pdt `devang3.zag`; COSEG implementation
   (see IMPLEMENTATION.md).
6. `devang4`: built binary via pinned znc.
7. (pending) dev Family A test logs.
8. (pending) `genseal4.zag`, sealed4/ package, sealed runs.

## Paper analysis recorded at prereg time (per-probe lexicon arithmetic)

Nominal post-training counts: tak 100, not 16, red 28, blu 26, grn 14,
bal 37, sph 8, cub 26, tri 24, big 10, biger 16, smal 6.
Seen score = ilog(c)*10-30+ilog(L+1)*5 (minus 40 if L==1);
novel score = -50-L (2321pdt linear penalty).
sc(tak)=40, sc(bal)=30, sc(red)=20, sc(blu)=20, sc(cub)=20, sc(tri)=20,
sc(grn)=10, sc(sph)=10.
- D1 takbaltagrn: shatter [tak][bal][ta][grn] = 40+30-52+10 = 28;
  whole [tak][balta][grn] = 40-55+10 = -5. Gap 33 -> shatter.
- D2 takredbogrn: shatter 40+20-52+10 = 18; whole -5. Gap 23.
- D3 takblupabal: shatter 40+20-52+30 = 38; whole 40-55+30 = 15. Gap 23.
- D4 takcublagrn: shatter 40+20-52+10 = 18; whole -5. Gap 23.
- D5 tak trixobal: shatter 40+20-52+30 = 38; whole 15. Gap 23.
- D6 taksphlagrn: shatter 40+10-52+10 = 8; whole -5. Gap 13.
Baseline run confirms: 2321pdt picks the shatter on all six (0/6).
COSEG design: whole has margin 2 (50 coherence) vs shatter margin 0;
50 + 5 (seg parsimony) > max gap 33 -> whole wins on all six.
