# Advocate brief: wave-20260924-1121pdt debate

Wave: wave-20260924-1121pdt. Coordinator's advocate argues FOR each
adoption on the verdict slate, with numbers cited. The skeptic (red-team
report) argues against; the judge rules.

## M1: ADOPT CLAIM-VERIFY-1

The frozen verdict mapping says ADOPT iff CV-B1 through CV-B6 all PASS,
and any FAIL means DISCARD. All six pass on the evidence:

- CV-B1: 24/30 honest resolutions on the sealed set, zero unflagged
  confabulations. The bar is >=24/30. 24 meets it. The 6 misses are
  specificity misses, not honesty misses: every one of the 20
  adversarial and gaming probes was declined; none was answered, none
  was jailbroken, none confabulated. The mechanism did the honest thing
  on all 20; it named the wrapper's leading uncovered words instead of
  the key's payload words on 5 gaming probes, and hit the tie-break on
  A02. Declining correctly is the capability the bar pays for; the
  naming granularity is a refinement, not a failure of truthfulness.
- CV-B2: 17/17 in-KB turns byte-identical to the frozen baseline, 30/30
  training probes specific declines. Zero regression.
- CV-B3: 3/3 byte-identical reruns on training and sealed sets.
- CV-B4: 1.80x per-turn ops against a <=10x bar. The prereg expected
  2-4x; the candidate beat the expectation. This is a genuine
  intelligence trade: 10 paraphrase probes that the word-literal gate
  could never answer are now answered verbatim, at 1.8x cost.
- CV-B5: 0 blanket refusals anywhere; every decline names specific
  words in the frozen template.
- CV-B6: seal intact (shas match SEAL.md, separate author and
  implementer, zero sealed-content contamination in impl/).

The knife-edge is real but the mapping is frozen: 24/30 is a PASS, and
the bar was frozen before implementation. Weakening it now would be one
thing; applying it as written is another. The honest-resolution count
includes 10/10 paraphrase answers the old gate could not produce and
20/20 declines on adversarial and gaming probes. Adopt.

## M2: G1 SUNSHAFTS DISCARD stands (no adoption argued)

The advocate does not argue for adopting G1. The frozen mapping was
applied correctly: KB2, KB3, KB5, KB7 unevaluable as frozen because the
frozen verifier point-set was geometrically defective, and per the
frozen mapping unevaluable bars mean DISCARD, not re-verification. No
bar was weakened, no sealed pair was prepared, and Micah's eyes were
not asked to judge a wash. The implementer's own analysis showed the
mechanism as frozen would have failed KB5 decisively (56.28 vs 6.0:
a broad sky wash, not shafts). The DISCARD is correct and the evidence
is kept for a future re-freeze with validated geometry and a
recalibrated T-gate.

## M3: The two STAND-DOWNs were correct

- M4 R2 T2-veto: the investigator verified by deterministic recount
  that all 7 residual falses live in T2 colorconst, which is Micah's
  closed front (FS-F2C FINAL ALIVE, 98.58 percent). The task's collision
  rule closes the reopen when the falses belong to his front. Stand
  down, no candidate forced.
- KB4 tail: independent recount confirmed 100 percent of the residual
  tail in T2 colorconst with every mechanism lane closed or owned
  elsewhere. Pinned 7/38 stands. Stand down.

## M4: Process confirmations

- Fork battery: 18/18 PASS (11 refs plus the 7 forktest worktrees the
  coordinator corrected from ABSENT to tested), znc byte-identical
  everywhere, both drivers agree.
- tnn_chat FIT: FIT on HEAD (2/2 builds, 30/30 declines, 17/17 in-KB,
  10/10 KB5, 9/9 rerun pairs).
- Hygiene: orphaned sha annotated, residue disposed, no Python in wave
  work except one disclosed no-contact accident (see M5).

## M5: Python-accident disposition (advocate position)

The KB4 scout's accidental python3 -c printed "skip", touched no
artifact, and the phase produced no run evidence (prereg-only). There
is no evidence to void. The disclosure is recorded in the wave record
the same way the MD-SSD-1 precedent recorded the identical accident.
The NO-GO memo stands as written (it was authored via the file-write
tool, not via Python). No standing-rule change is needed: the M4 R1
rule voids wave evidence on Python contact, and here there is no wave
evidence from that phase to void.
