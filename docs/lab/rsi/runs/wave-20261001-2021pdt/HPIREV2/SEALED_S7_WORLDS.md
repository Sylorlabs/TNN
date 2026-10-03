# SEALED S7 WORLDS: independent adversary manifest (HPIREV2 step 7, wave-20261001-2021pdt)

Status: SEALED. Written by the independent step-7 adversary (HPIREV2-S7-ADV)
before any execution. This file is the pre-run hash manifest required by the
frozen prereg (the ADVERSARY_WORLD_HASHES.md role): the executor verifies
these sha256 hashes at load time. The builder never sees world contents
before or during the run. RW files are held from the revision machinery
until after the revision completes, per the prereg.

World files live in sealed_s7/ (20 files: 5 per family). Pair notation
matches the frozen fixtures ("abc"->"ccc"), one pair per line.

Byte key used below: h=104 i=105 j=106 k=107 l=108 m=109 n=110 o=111 p=112
s=115 t=116 u=117 v=118 z=122. Frozen alphabet
A_frozen = {97,98,99,100,101,102,103,113,114,119,120,121}.

## sha256 (pre-run, sealed)

A_TW.txt        fbde6ea7969707a0264d6aea8ae0656b5d472b7350f95b882d7e29a3598021e1
A_FW.txt       96622a1b36f424c58ffa77fe75197223c241adc3d3225d2225189c966844abf4
A_RW.txt       0a19e534c3af08629566b2e219c2b21296d86a427d2ff2004ffc0752e6dddca5
A_CONFLICT.txt ac15de3ce2d04ef501c51cfe21873b3c1dba3c9d3bceea60e80a646e59746e69
A_EW.txt       87465c09e14aad83b661f5c6135e3c9c13ad331bdec69689ca5a0d87d2f9fa5e
B_TW.txt       fbde6ea7969707a0264d6aea8ae0656b5d472b7350f95b882d7e29a3598021e1
B_FW.txt       12d1d3f04cb64591d87478e211eaa426363738c5df09c46eecba547438ec35b6
B_RW.txt       0f8913082a08a9ec98be659b495957963efa39c63c58b38cf8080fb4693721af
B_CONFLICT.txt e10046aa3d933803d2ed6d5ef367badab544a67dbfb5ba5a09f645df8db48f20
B_EW.txt       6fbe264da70716878d6985d9a2548edb2e8c4db2a95cb84a7264414f17102e2d
C_TW.txt       00b4ace14f221f371dd9e9bbe1b3def5f6dc50108cb0c2175584207e58b1fc63
C_FW.txt       8d6f3362dc476447f1e07402e97958a654fe76558114adcad4ef40bd3fbf8
C_RW.txt       f183843c8218d48b5ded3585052afc14cc45378f290bc19d330bf51a8093088b
C_CONFLICT.txt 4631bc1ecfc90d907a2f2f749d27175a9066265ddd0f1c56b0c7cd423ba4e42c
C_EW.txt       d96689e044f951e2c9d96d4b9d390fa567b1fde8f37ea37b339288239c0a7e07
D_TW.txt       932c63fb7660c4c651bfb70e52292efb8e78073d9241551a23c665ccb3eb150d
D_FW.txt       934e7ca66063a7629a5927fd0a6264e4a8de5b20b02bb0abda3b99254f10b6da
D_RW.txt       d5be5d8ef4216fbd2280b95313ab1b59f6a60914a33b363b3d3e169d0f25112b
D_CONFLICT.txt de31ab6f386adceaef8f5e25db2eb6a951a9aebb88b02b5b7ed09ff1c6271dad
D_EW.txt       c02e30dd71c0ec4895f448faa8e571e5ad54b9804a5a4bf83de24798bcb8e648

Note: A_TW.txt and B_TW.txt are intentionally identical (same base
regularity, different conflict regimes); their hashes match.

## Family A: novel conflict alphabet and position

Requirement check: single conflict {(2,118)}; every TW/FW/RW input byte is
disjoint from A_frozen (TW uses 104-112, FW/RW use 115-118/122); declared
conflict position 2 is not 0; all input lengths <= 4 (3,2,4 / 4 / 4).

- TW: "hij"->"jjj", "kl"->"ll", "mnop"->"pppp" (base: repeat last byte).
- FW: "stvz"->"vvvv".
- RW: "suvz"->"vvvv".
- R_w: input[2]==118 maps to 118 repeated to input length, else base.
- EW: the 3 TW pairs unchanged (no TW input has 118 at position 2),
  plus FW and RW.

Intended solution: v1w is benum index 38 (repeat last byte; same structural
first fit as the frozen TW). The frozen diagnosis selects (0,115) by
position-ascending rank; the first dsearch fit on FW alone is C2 (benum
index 4), so the frozen construction builds IF(byte-equality(0,115), C2,
v_old). Predicted check outputs: "jjj", "ll", "pppp", "vvvv", "vvvv":
fails=0 is achievable. The novel position 2 is exercised in the consequent
(repeat input[2]) and in the declared rule; the novel alphabet (115, 116,
118, 122) rules out byte-114/120 hardcoding: a mechanism branching on a
hardcoded 114 or 120 would miss FW and fail W1.

Validity notes for the red team (V0-V4): V0 first fit is index 38 with
fails-on-TW=0 (structurally identical to the frozen TW). V1: FW input bytes
{115,116,118,122} are disjoint from TW input bytes {104-112}; {118} is a
subset of FW input bytes; RW input bytes {115,117,118,122} are disjoint
from TW input bytes except 118; RW matches (2,118). V2: v1w("stvz") =
"zzzz", a genuine misprediction. V3: TW needs f(k,4)=3 while FW needs
f(k,4)=2, so no benum program fits the union: first_fit=-1. V4: EW equals
R_w applied to the 5 check inputs; R_w is the parametric conflict-rule
form.

## Family B: multi-conflict

Requirement check: FW "stvz" presents two simultaneous distinct (pos,byte)
conflicts, (0,115) and (2,118); all input lengths <= 4.

- TW: "hij"->"jjj", "kl"->"ll", "mnop"->"pppp" (base: repeat last byte).
- FW: "stvz"->"ssss" (matches the first declared conflict).
- RW: "uzvz"->"vvvv" (matches only the second declared conflict).
- R_w: input[0]==115 maps to 115 repeated; else input[2]==118 maps to 118
  repeated; else base. Declaration order is the precedence rule (FW matches
  both, so the first declared conflict decides).
- EW: the 3 TW pairs unchanged, plus FW "ssss" and RW "vvvv".

Intended solution: v1w is benum index 38. The frozen revision creates one
branch: diagnosis (0,115), alt = first dsearch fit on FW alone = C0 (benum
index 2), revised form IF(byte-equality(0,115), C0, v_old). TW and FW are
then predicted correctly ("jjj","ll","pppp","ssss"), but RW "uzvz" matches
only the second conflict: RW[0]=117 is not 115 and RW's last byte 122 is
not 118, so the mechanism applies the base program and predicts "zzzz"
against expected "vvvv". Expected honest outcome: W1 fails on RW, which per
the frozen bounding matrix bounds the claim to single-conflict revision if
families A, C, D pass. This is the family's required discrimination, not an
engineered pass via base-program coincidence.

Validity notes for the red team: V0 first fit index 38, fails-on-TW=0. V1:
FW bytes disjoint from TW bytes; {115,118} subset of FW bytes; RW bytes
{117,122,118} disjoint from TW bytes except 118; RW matches (2,118) and
does not match (0,115). V2: v1w("stvz")="zzzz" vs "ssss". V3: TW needs
f(k,4)=3, FW needs f(k,4)=0: first_fit=-1. V4: EW equals R_w applied to the
5 check inputs; R_w with stated precedence is the prereg's family-B rule
made deterministic.

## Family C: longer inputs

Requirement check: single conflict {(0,115)}; every TW/FW/RW input has
length >= 8 (TW 8/10/12, FW 8, RW 8).

- TW: "hijklmno"->"oooooooo", "hijklmnoph"->"hhhhhhhhhh",
  "hijklmnophij"->"jjjjjjjjjjjj" (base: repeat last byte).
- FW: "stuvztuv"->"ssssssss".
- RW: "szzzzzzz"->"ssssssss".
- R_w: input[0]==115 maps to 115 repeated to input length, else base.
- EW: the 3 TW pairs unchanged (no TW input contains byte 115), plus FW
  and RW.

Intended solution: v1w is benum index 38. Diagnosis (0,115); first dsearch
fit on FW alone is C0 (benum index 2; byte 115 occurs exactly once in the
FW input, at position 0); revised form IF(byte-equality(0,115), C0, v_old).
All 5 check outputs are achievable with fails=0. The world isolates whether
revision accuracy holds and revision-eval cost stays bounded as length
grows past the frozen regime.

Validity notes for the red team: V0 first fit index 38, fails-on-TW=0. V1:
FW bytes {115,116,117,118,122} disjoint from TW bytes {104-112}; {115}
subset of FW bytes; RW bytes {115,122} disjoint from TW bytes; RW matches
(0,115). V2: v1w("stuvztuv")="uuuuuuuu" vs "ssssssss". V3: TW needs
f(k,8)=7, FW needs f(k,8)=0: first_fit=-1. V4: EW equals R_w applied to the
5 check inputs; R_w is the parametric conflict-rule form.

## Family D: novel template shape

Requirement check: intended structure S_w declared below; differs
structurally from S_frozen while expressible by the frozen construction
operators.

- TW: "hij"->"hhh", "kl"->"kk", "mnop"->"mmmm" (base: repeat FIRST byte).
- FW: "tuvz"->"vvvv".
- RW: "tsvz"->"vvvv".
- R_w: input[2]==118 maps to 118 repeated to input length, else the base
  program (repeat first byte) applies. This is a structural generalization
  of the frozen conflict-rule form: same match-to-repeated-byte shape with
  a different base program in the else position.
- S_w: IF(byte-equality(0,116), C2, v_old), where v_old is the dsearch
  first fit on TW (benum index 2, repeat-first-byte) and C2 is the dsearch
  first fit on FW alone (benum index 4, constant position 2; byte 118
  occurs exactly once in the FW input, at position 2).
- EW: the 3 TW pairs unchanged (no TW input has 118 at position 2), plus
  FW and RW.

Structural difference from
S_frozen = IF(byte-equality(0,114), C0, IF(byte-equality(0,120), C0,
v_old=repeat-last-byte)): (1) branch count 1 versus 2; (2) then-branch
program C2 versus C0; (3) else-branch program repeat-first-byte versus
repeat-last-byte. Expressibility: the single IF byte-equality wrapping is
exactly what the frozen specialize builds per revision event; alt=C2 is a
benum program selected by frozen dsearch on F alone; v_old=C0 is the frozen
dsearch first fit on TW embedded in the else position. No new operators.

Intended solution: v1w is benum index 2 (C0). Diagnosis selects (0,116);
revised form IF(byte-equality(0,116), C2, v_old=index-2). Predicted check
outputs "hhh","kk","mmmm","vvvv","vvvv": fails=0 is achievable. RW matches
both the declared conflict (2,118) and the diagnosed branch condition
(0,116); no TW input contains byte 116, so no record is spuriously
superseded. The world tests whether the conflict rule composes with a
template shape beyond the authored frozen solution shape (different base
regularity, different then-branch program, single branch).

Validity notes for the red team: V0 first fit index 2, fails-on-TW=0. V1:
FW bytes {116,117,118,122} disjoint from TW bytes {104-112}; {118} subset
of FW bytes; RW bytes {116,115,118,122} disjoint from TW bytes except 118;
RW matches (2,118). V2: v1w("tuvz")="tttt" vs "vvvv". V3: TW needs
f(k,4)=0, FW needs f(k,4)=2: first_fit=-1. V4: EW equals R_w applied to the
5 check inputs; R_w is a structural generalization of the frozen form; S_w
differs structurally from S_frozen as listed and is expressible as listed.

## Cross-family design observations (for the red team and scorer)

1. Diagnosis rank bias. The frozen diagnose ranks candidate (pos,byte)
   pairs by position ascending, so on every single-counterexample world it
   selects (0, FW[0]) regardless of the declared conflict position. For
   families A and D (declared position 2), the RW inputs were therefore
   designed to match both the declared conflict and the diagnosed branch
   condition; otherwise the worlds would manufacture a deterministic W1
   fail from the rank bias rather than measuring byte/consequent/shape
   generalization. This is documented per world, not hidden.
2. Family A still exercises a novel position: the consequent alt=C2
   repeats input[2], and the declared rule is stated at position 2. A
   mechanism hardcoding the consequent to position 0, or the conflict byte
   to 114/120, fails here.
3. Family B is the one world where the expected honest outcome is a W1
   fail on RW: one branch cannot cover two simultaneous conflicts. The
   bounding matrix converts this into the single-conflict bound if A, C,
   D pass. RW was deliberately not engineered for base-program
   coincidence (RW[0]!=115, last byte !=118).
4. alt indices are low in every world (A:4, B:2, C:2, D:4), keeping the
   revision cheap and inside the K-OOD-W2 ceiling by construction.
5. extract_seq uniqueness was verified by hand for every FW pair: the
   conflict output byte occurs exactly once in its FW input (A: 118 at
   pos 2 of "stvz"; B: 115 at pos 0 of "stvz"; C: 115 at pos 0 of
   "stuvztuv"; D: 118 at pos 2 of "tuvz"). A repeated conflict byte would
   make dsearch degenerate (first fit index 0) and void V3.
6. No world was executed. All validity arguments above are static
   analyses from the frozen source; the executor's mechanical V0-V3 and
   the red team's V1-V4 certification are still required pre-run. Any
   precheck failure voids that world per the prereg; it must never be
   laundered into a FAIL.

No em-dashes or en-dashes appear in this file or in sealed_s7/.
