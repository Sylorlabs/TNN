# ADV_SEAL: RT-HPIREV2 independent adversarial world seal (FROZEN)

Status: FROZEN. Committed ALONE before any adversarial executor
source, binary, transcript, or build log exists. The 30 world files
under adv_sealed/ are bound by the sha256 hashes below; the sealed
executor verifies them at load time and aborts on any mismatch.
No world may be tuned after this freeze; any amendment is
transparent and re-frozen. No em-dashes in this documentation.

## Adversary and independence

These worlds were designed by RT-HPIREV2, the independent red-team
reviewer for wave-20261001-2321pdt, with no access to the HPIREV2
lane's design process beyond its frozen public record. The lane
disclosed non-independent world design; this family is the
independent adversarial counterpart required by the C0-C mandate.
Design-time mechanical validation used only the frozen machinery
(lines 1-606 of proc_revise2.zag at 847a8f10f, hash-verified) inside
rt_adv_design.zag; three design slips were found and fixed
pre-freeze (S2 FW/TW byte overlap, S2 RW transcription length, S3
TW/FW byte overlap) and are disclosed here. The seal binds
post-freeze.

## Family

Six worlds, materially different from the lane's A2/B1/B2/C2/D2:

- ADV-S1: base program is the 5-node reversal index map (benum 608);
  consequent repeat-input[0] (benum 2); trigger (0,81).
- ADV-S2: base program identity (benum 0); consequent reversal
  (benum 608); trigger (0,81); FW length 6.
- ADV-S3: base program repeat-input[1] (benum 3); consequent
  reversal (benum 608); trigger (0,81).
- ADV-S4 (RANK-BIAS BREAKER): single conflict whose true trigger is
  (2,66) while the frozen rank-biased diagnosis selects (0,120);
  adversarial prediction is mechanism FAIL (fails_total=1).
- ADV-M1 (MASKED SECOND CONFLICT): two-conflict true rule; the
  held-out RW pair carries both conflicts with conflict 1 firing
  first, so all EW pairs agree with the single-branch revision;
  adversarial prediction is silent success claim (fails_total=0,
  no detection) despite the uncovered second conflict.
- ADV-M2 (PROBED SECOND CONFLICT): same two-conflict true rule as
  M1, but the held-out RW pair carries only conflict 2;
  adversarial prediction is explicit trip (fails_total=1,
  COUNTEREXAMPLE_DETECTED at W3, no post-W3 re-revision).

Predicted sealed-execution values (from pre-freeze validation):
S1: V0=608, DIAG (0,81), ALT=2, revision_evals=6, fails_total=0.
S2: V0=0, DIAG (0,81), ALT=608, revision_evals=8, fails_total=0.
S3: V0=3, DIAG (0,81), ALT=608, revision_evals=8, fails_total=0.
S4: V0=38, DIAG (0,120), ALT=2, revision_evals=6, fails_total=1
(predicted adversarial break of the narrowed claim).
M1: V0=38, DIAG (0,81), ALT=2, revision_evals=6, fails_total=0,
reuse_correct=1, no detection (predicted silent success).
M2: V0=38, DIAG (0,81), ALT=2, revision_evals=6, fails_total=1,
COUNTEREXAMPLE_DETECTED at W3 (predicted explicit trip).

Adversarial bars for the sealed run (not kill bars on the lane;
they score the attempt to break the claim):
- A-S1/S2/S3: fails_total==0, revision_evals<=25, reuse correct,
  3/3 byte-identical, exit 0, zero stderr. A pass means the
  single-conflict bound generalizes to the novel structure.
- A-S4: report fails_total exactly; fails_total=1 with the RW
  pair the mismatch CONFIRMS the rank-bias break; fails_total=0
  would mean the claim survived the strongest single-conflict
  attack mounted.
- A-M1: report fails_total and detection lines exactly; the
  predicted silent success (fails_total=0, zero detection)
  demonstrates the bound-trip signal is probe-dependent.
- A-M2: report S1-S3 style trip conjuncts exactly.

## Frozen sha256 hashes (30 files)


## ERRATUM (transparent amendment; no execution preceded it)

The original seal commit 8b86b27d2 contained three hand-transcription
errors in the frozen hash listing, caught by the mandatory
pre-execution load-time verification (sha256sum -c) before any
adversarial executor run, binary execution, or transcript existed:

- M2_FW.txt: hash line had 63 hex chars (truncated).
- S4_EW.txt: hash line had 63 hex chars (truncated).
- S4_RW.txt: hash line had 64 chars but one wrong char
  ("d2e" for "d3e" at one position).

No world file was created, modified, or tuned after the original
seal; the files are byte-identical to the pre-freeze validated
designs. This amendment corrects only the hash listing, regenerated
mechanically with sha256sum (no hand transcription), and re-freezes
it. The 27 unaffected lines are unchanged. The pre-execution
verification that caught the errors is recorded in
ADV_EXEC_RECORD.md.

## Frozen sha256 hashes (30 files, mechanically generated)
M1_CONFLICT.txt 3ea59280273d06623987af467fc56e4752aef12da546f83bdc1549081dc468ac
M1_EW.txt 773e6b42f1f717d0379462bf1c8347f036273d4485109879a096302379d03dc3
M1_FW.txt 75d204d9f8ac92369bdc170f2ad3a6fe06c513f25749c9a00db7abdc288b97c1
M1_RW.txt c4e386324f77369bba40acb72444ba80162e46a6e7995c4dd5b9b0b3671c8d1c
M1_TW.txt d24126846cec9896a9c95324cc913f51f8bce9d718ceb01db3285239187c5455
M2_CONFLICT.txt e699c095c7e67a2737125ed4903f704b01bcf2c08647885837cffa89986f0e0d
M2_EW.txt 371b980e172f4927374493057d37bb9bd95d4ec6bad09d2b2fbdb111def3c613
M2_FW.txt 57fe58a837a64b2ea06b879b0fecd48d9ef346995e8a1c9327aaefafbd612ca3
M2_RW.txt 9c57f6e2371f264bd5c7a3859f3810ec4ac4e74cab96fb8bb2f80f96baf54dd5
M2_TW.txt d24126846cec9896a9c95324cc913f51f8bce9d718ceb01db3285239187c5455
S1_CONFLICT.txt a31d03771e32974e1c1ae0bbd8d6441ce16874af2e6ba0bd3d845bbd5c9dcc3b
S1_EW.txt e6dba8a21f07e9d09f662ed49e4ab0c0736a6516f589771caabb62c6f4a72c52
S1_FW.txt 75d204d9f8ac92369bdc170f2ad3a6fe06c513f25749c9a00db7abdc288b97c1
S1_RW.txt 22faf9f8d7a2e075fc58da1429a56351595849bf14fe3fe441363c497ceb0207
S1_TW.txt 1d9b10746944a4e0062c7f896ed5c9ca26904ea837fd8b66ae0f3c4a50ad0ff3
S2_CONFLICT.txt 2f0681030a803b233f30420156cea48c52f538ed3fbda937e3c8a29866eaac07
S2_EW.txt 11b602d95c1d19b0a2d011ef2d6a7ddafce5e39f1f036e0c7f31aba4ac265380
S2_FW.txt 33c4cd667f9b54f5bc6c6106d8b18ad9174ab868d1a133847cb26d1940b00c3a
S2_RW.txt ded5c17e41e1084fbd4a7968613b66e4c109225ce06025e2cc930a9582af4797
S2_TW.txt 8628f421c83ca4874e3e7566909490060d7446846e05939c0f0b24d407640875
S3_CONFLICT.txt e318681afbb76e9bb5df71054ee75b9bec556178b82cf3fafd43b4c69bcb1704
S3_EW.txt 4f0f0216e91231569387ab3d0ba583dc8dd095853453a34325ad751293426af5
S3_FW.txt 33c4cd667f9b54f5bc6c6106d8b18ad9174ab868d1a133847cb26d1940b00c3a
S3_RW.txt af01c6e22069d82da01258a6d1631c99af5af20275b8a8556208a8c6ee1cf7fd
S3_TW.txt 7fb0bcf58ebc732deabff55d9cdbb445764ae382a0de8e7a93b7f79daa274a6a
S4_CONFLICT.txt 18bfe3973c600fef3d6f239d32d8c7b5a6b3ece63054e439da123090f1f28b42
S4_EW.txt b745a5a6a82485676b35d45afbb3aae5d1b4807777536499f9c99c5bd0f5c4b3
S4_FW.txt 6bf6b251ec71548ee214d6a27f5d3ad7886990f2529e1ee9c2bfe87ce0096a59
S4_RW.txt 7e88b2a8f0cee59657b25096b5495686d2a95b42f6d3eafd213cbf2125b263e6
S4_TW.txt d24126846cec9896a9c95324cc913f51f8bce9d718ceb01db3285239187c5455

No em-dashes in this documentation.
