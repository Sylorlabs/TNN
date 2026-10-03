# CERT_S7_V1V4: independent red-team certification of step-7 sealed worlds

Lane: HPIREV2-S7-RT (analysis only; the mechanism was NOT run on the sealed worlds)
Certifier: independent red-team certifier, depth-2 subagent
Date: 2026-10-01
Scope: 20 world files in sealed_s7/ (5 per family), frozen prereg
PREREG_PI_REV2_STEP7.md (committed alone at 201ed5a05), adversary manifest
SEALED_S7_WORLDS.md (committed at dea2694d1)

## Method

Read-only static certification. No execution of the revision mechanism, no
build, no forbidden executables (safebin toolchain guard recorded in
NAMECHECK_S7_RT.md; `which python3` printed nothing).

1. Verified all 20 file hashes against the adversary manifest: 19/20 OK;
   C_FW.txt manifest line is malformed (see Erratum 1). The file itself is
   intact; its true sha256 is recorded below.
2. Wrote a mechanical byte-level checker (/tmp/s7_cert.awk, mawk, safebin)
   that parses every pair, checks notation, lengths, byte sets, disjointness,
   declared-conflict matching, extract_seq uniqueness, v1w fit/mispredict,
   EW == R_w on the 5 check inputs, and the intended revised form vs EW.
   Result: 0 failures on every check that encodes a prereg requirement,
   for all 4 families.
3. Read the frozen source docs/lab/rsi/runs/wave-20260929-2321pdt/pi_rev2/
   proc_revise2.zag (committed 847a8f10f) to verify the static claims it
   supports: benum term order (index 0=K, 1=N, 2=C0, 3=C1, 4=C2),
   eval semantics (program returns input index f(k,n) for output position k
   of n), extract_seq (requires each output byte to occur exactly once in
   the input), dsearch (first fit in index order), diagnose ranking
   (position ascending, then byte ascending).

Static proofs established from the frozen source (no execution needed):

- benum index 2 = C0 = repeat input[0] = repeat-first-byte.
- benum index 4 = C2 = repeat input[2].
- benum index 38 = SUB(N, C1) = n-1 = repeat-last-byte. Exhaustive case
  analysis of all 50 size-3 programs (binops of two terms from
  {K,N,C0,C1,C2} with ADD/SUB): any k-involving program varies with k and
  cannot match the constant-per-n sequences; among k-free programs only
  n-1 matches (n=3->2, n=2->1, n=4->3); all constant combos fail across n.
  No index below 38 fits the A/B/C TW sets, so dsearch first fit = 38.
- dsearch first fit on D_TW = index 2 (indices 0, 1 fail on "hij"->"hhh").
- dsearch first fit on FW alone: A -> 4, B -> 2, C -> 2, D -> 4
  (verified against extract_seq outputs [2,2,2,2], [0,0,0,0], [0]*8,
  [2,2,2,2]).
- Diagnose on a single-counterexample world selects (0, FW[0]) by the
  frozen position-ascending rank: A -> (0,115), B -> (0,115),
  C -> (0,115), D -> (0,116). Matches the adversary's design notes.
- Prereg V3 impossibility (B1 over TW+FW, first_fit=-1) holds by a clean
  static argument, stronger than enumeration: eval_prog sees only (k, n).
  A: TW "mnop"->"pppp" and FW "stvz"->"vvvv" share the identical (k,n)
  domain (k in 0..3, n=4) but require f=3 and f=2 respectively: no program
  can satisfy both. B: same n=4 domain requires 3 vs 0. C: n=8 domain
  requires 7 vs 0. D: n=4 domain requires 0 vs 2. Hence first_fit=-1 on
  TW+FW for every family, mechanically.

## Per-family certification

### Family A (novel conflict alphabet and position): CERTIFY

V1 (family requirements): PASS on every clause. Declared conflict set is
the single pair {(2,118)}; position 2 is not 0. Every TW/FW/RW input byte
is disjoint from A_frozen = {97,98,99,100,101,102,103,113,114,119,120,121}
(TW uses 104-112, FW uses {115,116,118,122}, RW uses {115,117,118,122}).
Declared byte 118 is a subset of FW input bytes. FW input bytes are
disjoint from TW input bytes. RW input bytes intersect TW input bytes in
the empty set, which satisfies "disjoint except for declared conflict
bytes". RW matches the declared conflict (RW[2]==118). All input lengths
(3,2,4 / 4 / 4) are <= 4.

V2 (validity): PASS. All 10 pairs use valid "abc"->"ccc" notation, one per
line; every pair has inlen == outlen >= 2 (no degenerate inputs). FW
extract_seq uniqueness holds: byte 118 occurs exactly once in "stvz"
(at position 2).

V3 (non-triviality): PASS. v1w = benum index 38 (repeat-last-byte) fits all
3 TW pairs (proven first fit by the size-3 case analysis above) and
mispredicts FW: v1w("stvz") = "zzzz" vs expected "vvvv", a genuine
counterexample. Plain re-search over TW+FW is impossible (the (k,n)-domain
contradiction at n=4: 3 vs 2). Solvable in principle by the frozen
mechanism: diagnose (0,115) by frozen rank, alt = C2 (index 4, first fit on
FW alone), revised form IF(byte-equality(0,115), C2, v_old) predicts all 5
EW pairs correctly (mechanically verified: TW inputs never have 115 at
position 0, so no spurious branch; FW/RW fire the branch and repeat
input[2]=118).

V4 (no designed kill / rank-bias mitigation): PASS. The declared conflict
(2,118) differs from the diagnosed branch (0,115), and the adversary
mitigated the rank bias by designing RW ("suvz") to match both the declared
conflict and the diagnosed branch condition. The world therefore measures
novel-byte generalization (115 vs the frozen 114/120: a mechanism with the
conflict byte hardcoded to 114 or 120 branches on (0,114)/(0,120), misses
FW[0]=115, and fails W1) and novel consequent position (alt=C2 repeats
input[2]), not the rank bias. The intended revised form achieves 5/5, so no
deterministic failure is manufactured.

### Family B (multi-conflict): CERTIFY

V1 (family requirements): PASS on every clause. FW "stvz" presents two
simultaneous distinct declared (pos,byte) conflicts, (0,115) and (2,118):
FW[0]==115 and FW[2]==118. RW "uzvz" matches the second only: RW[0]=117
is not 115, RW[2]==118. All input lengths (3,2,4 / 4 / 4) are <= 4.
{115,118} is a subset of FW input bytes; FW bytes are disjoint from TW
bytes; RW bytes intersect TW bytes in the empty set. No TW input matches
either declared conflict, so the EW TW part is stable under R_w.

Note: the prereg's family-B rule ("an input matching either declared
conflict maps to the matched byte repeated") is ambiguous when an input
matches both; the adversary's CONFLICT.txt completes it with
declaration-order precedence (first declared conflict decides), stated
pre-run in both CONFLICT.txt and SEALED_S7_WORLDS.md. This is a disclosed
deterministic disambiguation, not a deviation: FW matches both and maps to
"ssss" per the precedence rule.

V2 (validity): PASS. Valid notation on all 10 pairs; inlen == outlen >= 2
throughout. FW extract_seq uniqueness holds: byte 115 occurs exactly once
in "stvz" (at position 0).

V3 (non-triviality): PASS. v1w = index 38 fits all 3 TW pairs and
mispredicts FW: v1w("stvz") = "zzzz" vs expected "ssss". Re-search over
TW+FW is impossible (n=4 domain requires 3 vs 0). The intended honest
outcome is a W1 fail confined to RW: the frozen revision builds exactly
one branch, IF(byte-equality(0,115), C0, v_old), which predicts TW and FW
correctly but applies the base program to RW ("uzvz": branch does not
fire since RW[0]=117, base predicts "zzzz" vs expected "vvvv").
Mechanically verified: revised-form mismatches on RW only. This is the
family's required single-vs-multi-conflict discrimination, and the
adversary deliberately avoided base-program coincidence (RW[0]!=115, RW
last byte 122 != 118). Per the frozen bounding matrix, a B-only fail
bounds the claim to single-conflict revision; that is a measurement, not
a world defect.

V4 (no designed kill / rank-bias mitigation): PASS. The diagnosed
(0,115) is the first declared conflict, consistent with the precedence
rule; no rank-bias exploitation. The expected fail comes from the
one-branch-per-revision-event structural limit the family is designed to
probe, which is honest discrimination rather than a manufactured
deterministic failure.

### Family C (longer inputs): CERTIFY

V1 (family requirements): PASS on every clause. Single declared conflict
{(0,115)}: FW[0]==115, RW[0]==115, 115 in FW input bytes. Every TW/FW/RW
input has length >= 8 (TW 8/10/12, FW 8, RW 8). FW bytes are disjoint from
TW bytes; RW bytes intersect TW bytes in the empty set. No TW input
contains byte 115, so the branch never fires spuriously.

V2 (validity): PASS. Valid notation on all 10 pairs; inlen == outlen >= 2
throughout. FW extract_seq uniqueness holds: byte 115 occurs exactly once
in "stuvztuv" (at position 0).

V3 (non-triviality): PASS. v1w = index 38 fits all 3 TW pairs (same
case-analysis proof with n in {8,10,12}) and mispredicts FW:
v1w("stuvztuv") = "vvvvvvvv" vs expected "ssssssss" (see Erratum 2: the
adversary doc wrote "uuuuuuuu"; the misprediction conclusion is
unaffected). Re-search over TW+FW is impossible (n=8 domain requires 7
vs 0). Solvable in principle: diagnose (0,115), alt = C0 (index 2, first
fit on FW alone), revised form IF(byte-equality(0,115), C0, v_old)
predicts all 5 EW pairs correctly (mechanically verified).

V4 (no designed kill / rank-bias mitigation): PASS. Declared conflict
equals diagnosed branch ((0,115)); no rank-bias issue arises. The world
isolates length scaling of revision accuracy and cost, as required.

### Family D (novel template shape): CERTIFY

V1 (family requirements): PASS. Intended structure
S_w = IF(byte-equality(0,116), C2, v_old) with v_old = benum index 2
(repeat-first-byte) and C2 = benum index 4 (repeat input[2]).

V2 (validity): PASS. Valid notation on all 10 pairs; inlen == outlen >= 2
throughout. FW extract_seq uniqueness holds: byte 118 occurs exactly once
in "tuvz" (at position 2). Declared byte 118 is a subset of FW input
bytes; FW bytes are disjoint from TW bytes; RW bytes intersect TW bytes in
the empty set; RW matches the declared conflict (RW[2]==118).

V3 (non-triviality): PASS. v1w = benum index 2 (repeat-first-byte; proven
first fit: indices 0 and 1 fail on "hij"->"hhh") fits all 3 TW pairs and
mispredicts FW: v1w("tuvz") = "tttt" vs expected "vvvv". Re-search over
TW+FW is impossible (n=4 domain requires 0 vs 2). Solvable in principle:
diagnose (0,116) by frozen rank, alt = C2 (index 4), revised form
IF(byte-equality(0,116), C2, v_old) predicts all 5 EW pairs correctly
(mechanically verified: no TW input has 116 at position 0; FW/RW fire the
branch and repeat input[2]=118).

V4 (expressibility, no designed kill): PASS. S_w differs structurally from
S_frozen = IF(byte-equality(0,114), C0, IF(byte-equality(0,120), C0,
v_old=repeat-last-byte)) in three respects, where the prereg requires at
least one: (1) branch count 1 versus 2; (2) then-branch program C2 versus
C0; (3) else-branch program repeat-first-byte versus repeat-last-byte.
S_w is expressible by the frozen construction operators: the single IF
byte-equality wrapping is exactly what the frozen specialize builds per
revision event; the branch condition (0,116) is exactly what the frozen
diagnose produces on this world; alt=C2 is the frozen dsearch first fit on
FW alone (index 4, verified above); v_old is the frozen dsearch first fit
on TW embedded in the else position (index 2, verified above). No new
operators, no disjunctions, no researcher-authored branch conditions.
Because S_w is precisely the structure the frozen construction would
build, this world cannot be a designed kill; it is the composition-
generality question the prereg requires. Rank-bias mitigation holds as in
family A: RW ("tsvz") matches both the declared (2,118) and the diagnosed
(0,116), and the intended form achieves 5/5.

## Errata (documentation defects, not world defects; neither voids any world)

Erratum 1 (manifest typo, pre-run correction required): SEALED_S7_WORLDS.md
records the C_FW.txt sha256 as
8d6f3362dc476447f1e07402e97958a654fe76558114adcad4ef40bd3fbf8
(61 hex characters; "7a" dropped). The actual file hash is
8d6f3362dc476447f1e07402e97958a654fe76558114adcad4ef7af40bd3fbf8
(64 hex characters, verified). The file is intact; 19/20 manifest lines
verify cleanly. The executor's load-time hash check will reject the
malformed line, so the manifest needs a transparent one-line correction
before execution. This does not void world C: the sealed bytes are
unchanged and the true hash is now independently recorded by the red team.

Erratum 2 (adversary note typo, conclusion unaffected): the Family C
validity note in SEALED_S7_WORLDS.md states v1w("stuvztuv")="uuuuuuuu".
The last byte of "stuvztuv" is v (118), so repeat-last-byte predicts
"vvvvvvvv", not "uuuuuuuu". The V2 conclusion (genuine misprediction vs
expected "ssssssss") is unchanged.

## Residual scope note

This certification is static analysis of the committed world files against
the frozen prereg's family requirements and validity criteria. The
prereg's mechanical executor prechecks (V0/V1/V2/V3 run with frozen
baseline code) remain required pre-run; the static proofs above
(first-fit indices by case analysis, V3 impossibility by (k,n)-domain
contradiction, EW consistency by direct computation) cover the same
ground and predict the mechanical outcomes, but they do not replace the
executor's run.

## Verdicts

- Family A: CERTIFY (V1 PASS, V2 PASS, V3 PASS, V4 PASS)
- Family B: CERTIFY (V1 PASS, V2 PASS, V3 PASS, V4 PASS; expected honest
  outcome is a W1 fail on RW, which per the frozen bounding matrix bounds
  the claim to single-conflict revision rather than voiding the world)
- Family C: CERTIFY (V1 PASS, V2 PASS, V3 PASS, V4 PASS)
- Family D: CERTIFY (V1 PASS, V2 PASS, V3 PASS, V4 PASS)

No world is voided. No em-dashes or en-dashes appear in this file; the 20
world files were byte-checked clean (0 em/en-dash bytes).
