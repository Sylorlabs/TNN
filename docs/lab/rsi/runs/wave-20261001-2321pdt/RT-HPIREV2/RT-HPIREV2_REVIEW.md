# RT-HPIREV2 REVIEW: H-PI-REV2 narrowed single-conflict claim
## (wave-20261001-2321pdt; independent red-team second opinion + adversarial family)

Reviewer: RT-HPIREV2. Pure Zag throughout (NAMECHECK.md Step 0:
safebin active, `which python3` and `which python` both exit 1).
READ-ONLY toward the HPIREV2 lane: all lane artifacts were extracted
with git show from the recorded commits; nothing in the lane dir was
modified. No em-dashes in this documentation.

---

## PART 1: SECOND OPINION ON THE LANE'S BUILD-PASS

### Verdict: QUALIFY

The BUILD-PASS verdict stands on the five tested worlds under the
frozen bars as written: every mechanical check I re-ran confirms
the lane's reported numbers. Two qualifications are load-bearing
and must travel with the verdict.

### What I independently verified (cited evidence)

1. Commit order (prereg before implementation):
   `git merge-base --is-ancestor 00b31af53 ec52cf1ca` returns true
   (ANCESTOR-OK). `git log --format=%H -- <prereg path>` shows
   exactly one commit. `git show --stat 00b31af53` contains ONLY
   PREREG_PI_REV2_NARROWED.md (344 insertions, 1 file). Exactly one
   lane-dir commit exists between prereg and implementation (the
   implementation commit ec52cf1ca itself). The commit-order
   self-check HOLDS.

2. Binary hash: `git show ec52cf1ca:.../s8_exec_bin | sha256sum`
   = aee1b6f21a4b5309a3c93e9f66d9c38553bd75db926feeba123207373117ddbc,
   matching the prereg record, the exec record, and the working
   tree. Match.

3. Frozen mechanism hash: proc_revise2.zag at 847a8f10f =
   dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12,
   matching the prereg. K-ARCH1 (zero cognition source delta)
   corroborated.

4. Machinery prefix: first 606 lines of s8_exec.zag at ec52cf1ca
   hash to 8d2b16ab31184758b2b724e19cb1fa9f96d5ff008a0674b6c95c1da8e227f712,
   identical to the same prefix of proc_revise2.zag. The
   byte-verbatim machinery claim HOLDS.

5. World files: 24 of 25 sealed world files at ec52cf1ca match
   the prereg-frozen hashes byte for byte (verified with
   sha256sum -c against hashes extracted mechanically from the
   prereg). See qualification Q1 for the 25th.

6. Transcripts: all 15 run transcripts 3/3 byte-identical per
   world; per-run sha256 values match the JUDGE_BRIEF exactly
   (A2 a4c05e04..., B1 f1092c1b..., B2 0e5208fd..., C2 9d4e66a0...,
   D2 8a3ac2a9...). All 18 .err files are 0 bytes. K-SC-W4
   corroborated.

7. Metric values read directly from the committed transcripts:
   fails_total=0 on all five worlds (5/5 EW pairs [ok] each);
   revision_evals 6/6/6/11/6 (all <= 25); reuse_correct=1 with
   zero new DIAGNOSIS/PRIMITIVE-CONSTRUCTED/VERSION lines after
   the W3 marker on all 15 runs; first fits, diagnosis winners,
   and alt indices match the prereg predictions exactly.
   K-SC-W1/W2/W3 corroborated against the frozen bars verbatim
   (no bar was weakened: the bars in the prereg are identical to
   the bars evaluated).

8. Bound-trip regression: 3/3 bound_b transcripts byte-identical
   to each other; S1 w_fails_total=1 (`PREDICT uzvz -> zzzz
   [MISMATCH want vvvv]`); S2 COUNTEREXAMPLE_DETECTED at the W3
   reuse probe; S3 zero new revision lines after the W3 marker.
   K-SC-B corroborated.

9. Docs purity: zero em-dash and zero en-dash bytes in all lane
   .md/.zag files (byte scan). K-SC-W5 docs half corroborated.

### Qualification Q1: D2_FW.txt frozen-hash transcription error

The prereg's frozen hash line for D2_FW.txt reads
`2d5083a3c47f0f41fc5f44d3a9e66e02f520db072e74755c6eddc27fa57`
(62 hex chars; two chars dropped). The actual file at ec52cf1ca
hashes to
2d5083a3c47f0f41fc5f44d3a9e66e02f520db072e74755c6eddc7eddc27fa57
(64 chars; the 60-char common prefix confirms a transcription
typo, not a file substitution; the file content `"PQRS"->"SSSS"`
is consistent with every transcript that stages it). Consequences:

- The exec record's claim "25/25 sealed world files verified
  against the frozen prereg hashes (24 via sha256sum -c, the 25th
  D2_TW.txt verified manually against the prereg line; all
  match)" is not literally true: the malformed line is
  D2_FW.txt, not D2_TW.txt, so the parenthetical misidentifies
  the anomaly, and no well-formed frozen hash exists for
  D2_FW.txt in the prereg to verify against. The load-time
  verification was not performed as described, or was described
  sloppily.
- Corrective: anchor D2_FW.txt to its true hash above; treat the
  prereg line as an erratum. The experimental evidence itself is
  unaffected (same file committed, staged byte-exact, and run).

This is a certification defect, not an experimental one. It does
not change any measured value, but the "25/25 verified, all
match" sentence should not be repeated without the erratum.

### Qualification Q2: the rank-bias accommodation in all five worlds

The frozen diagnose ranks (pos,byte) candidates by position
ascending and, on a single failing FW record, always selects
(0, FW[0]). Every lane world accommodates this: A2 declares
(1,84) but diagnoses (0,81); B1 declares (0,33), diagnoses
(0,33); B2 declares (2,58), diagnoses (0,47); C2 declares (0,59),
diagnoses (0,59); D2 declares (3,83) but diagnoses (0,80), with
the design note explicitly stating RW was chosen to match BOTH
the declared conflict and the diagnosed condition "so W1
measures composition with the novel shape rather than the rank
bias". The accommodation is disclosed, which is honest, but it
means the five worlds never test whether the procedure recovers
a conflict the rank bias does not select. The narrowed claim as
literally stated ("revises correctly and cheaply on every sealed
world with at most one conflict") is therefore stronger than the
evidence: Part 2 (ADV-S4) shows a valid single-conflict world
the procedure fails. The claim needs an explicit
rank-diagnosability qualifier: it holds for single-conflict
worlds whose conflict coincides with the rank-1 diagnosis.

### Attacks mounted and their outcomes (Part 1)

- Hash re-verification of every artifact: found Q1; all else
  matched.
- Commit-ordering attack: held (prereg alone, strict ancestor).
- Bar-weakening attack (diffing prereg bars against evaluated
  bars): no weakening found; all bars evaluated verbatim.
- Metric-gaming attack on revision_evals (frozen formula
  candidates+1+1, ceiling 25): values 6-11 are far from the
  ceiling on the tested worlds; the formula is frozen from
  step-5 and applied uniformly; no gaming detected on this
  evidence. (The metric scales with FW length by construction;
  C2 at length 9 already exercises this.)
- Knowledge-vs-architecture confound attack: the worlds'
  EW sets are consistent with the mechanism's single-branch
  form by V4 construction, which is legitimate for a bounded-L2
  claim and disclosed; the substantive confound is the rank-bias
  accommodation (Q2), which Part 2 tests directly.

### Part 1 bottom line

EVIDENCE-HOLDS on the five worlds under the frozen bars, with
Q1 (certification erratum) and Q2 (rank-diagnosability
qualifier) attached. Neither qualification alters a measured
value; Q2 is confirmed as load-bearing by the adversarial
result below.

---

## PART 2: INDEPENDENT ADVERSARIAL FAMILY (POST-FREEZE)

Seal: ADV_SEAL.md (original 8b86b27d2 committed alone before any
adversarial implementation; erratum amendment 1c40232af; 30/30
hashes verified pre-execution). Executor: rt_adv_exec_bin
(da58510e0a20d1a2956dc7556dfd5546870cd8e269b945d5a0d01b884f5e1e23),
frozen machinery byte-verbatim (8d2b16ab...), cognition delta 0.
Full record: ADV_EXEC_RECORD.md. 18 runs, 3/3 byte-identical per
world, exit 0, zero stderr. (Note: the lane binary s8_exec_bin
hardcodes its five fixtures, so it cannot be pointed at new
worlds; the adversarial runs execute the frozen mechanism itself,
byte-verbatim, which is the artifact the claim is about.)

### Per-world results

| world | structure (materially new vs A2/B1/B2/C2/D2) | fails_total | revision_evals | reuse | outcome vs adversarial prediction |
|---|---|---|---|---|---|
| ADV-S1 | base = 5-node reversal map (608); consequent repeat-input[0] | 0 | 6 | correct | PASS (predicted pass; bound generalizes) |
| ADV-S2 | base = identity (0); consequent = reversal (608); FW len 6 | 0 | 8 | correct | PASS (predicted pass; bound generalizes) |
| ADV-S3 | base = repeat-input[1]; consequent = reversal (608) | 0 | 8 | correct | PASS (predicted pass; bound generalizes) |
| ADV-S4 | true trigger (2,66); diagnosed (0,120) | 1 | 6 | mispredict flagged at W3 | BREAK CONFIRMED (predicted fail): `PREDICT p!Br -> rrrr [MISMATCH want pppp]` |
| ADV-M1 | two conflicts; RW carries both (conflict 1 fires first) | 0 | 6 | correct, zero detection | SILENT SUCCESS CONFIRMED (predicted): uncovered conflict 2 never flagged |
| ADV-M2 | two conflicts; RW carries only conflict 2 | 1 | 6 | mispredict flagged at W3 | EXPLICIT TRIP CONFIRMED (predicted): `PREDICT p!Br -> rrrr [MISMATCH want !!!!]`, COUNTEREXAMPLE_DETECTED at W3, no post-W3 re-revision |

### Did the bound survive?

Partially, and the pattern is informative:

1. The single-conflict bound GENERALIZES across materially new
   structures (novel base programs including a 5-node arithmetic
   index map, novel consequents including reversal, longer
   candidate lists): S1/S2/S3 all pass with margin (evals 6-8
   vs ceiling 25). The procedure is not overfitted to the
   lane's four dimensions.

2. The single-conflict bound BREAKS on ADV-S4: a valid
   single-conflict world (V0-V3 all pass) whose true trigger
   (2,66) is not the rank-1 diagnosis (0,120). The mechanism
   fails loudly (fails_total=1, flagged at W3), so the "never
   silent" half holds, but the "revises correctly on every
   single-conflict world" half is falsified as literally
   stated. This confirms Q2: the narrowed claim requires the
   rank-diagnosability qualifier.

3. The bound-trip detector is PROBE-DEPENDENT, not a general
   property of multi-conflict worlds. ADV-M1 (masked second
   conflict) yields fails_total=0 with zero detection: the run
   claims success while the learned rule mispredicts unprobed
   inputs carrying only the second conflict. ADV-M2 (probed
   second conflict) trips explicitly exactly like the lane's
   K-SC-B. The "flags the uncovered conflict explicitly rather
   than converging silently to a wrong solution" half of the
   narrowed claim therefore holds only when the uncovered
   conflict is independently probed; when it is masked, the
   mechanism converges silently to an incomplete solution and
   reports success.

### Strongest attack mounted and whether it held

The strongest attack was ADV-S4: a single-conflict world
satisfying every stated validity precheck, with a true conflict
trigger the frozen rank-biased diagnosis cannot select. It
HELD (the mechanism failed, fails_total=1 on the held-out RW
pair). The second-strongest was ADV-M1, which HELD: the
bound-trip signal stayed silent on a genuinely two-conflict
world. The fair-structure attacks (S1/S2/S3) did NOT break the
claim; the procedure handled novel base programs and
consequents correctly and cheaply, which is genuine positive
evidence for the narrowed bound within its (now qualified)
scope.

### Recommended claim restatement

"The frozen revision procedure revises correctly and cheaply on
sealed single-conflict worlds whose conflict coincides with the
frozen rank-1 diagnosis (position-ascending (pos,byte)), across
novel base programs, consequents, bytes, positions, and lengths;
on multi-conflict worlds it flags the uncovered conflict
explicitly when that conflict is independently probed, but can
report silent success when the uncovered conflict is masked in
all probed pairs."

### Evidence paths

- Part 1 lane record: docs/lab/rsi/runs/wave-20261001-2321pdt/HPIREV2/
  (prereg commit 00b31af53, implementation commit ec52cf1ca)
- This review: docs/lab/rsi/runs/wave-20261001-2321pdt/RT-HPIREV2/
  - NAMECHECK.md (Step 0 toolchain guard)
  - ADV_SEAL.md (frozen adversarial worlds + hashes; seal
    8b86b27d2, erratum amendment 1c40232af)
  - adv_sealed/ (30 sealed world files)
  - rt_adv_design.zag / rt_adv_exec.zag (pure-Zag validator and
    executor; frozen machinery prefix hash-verified)
  - rt_adv_exec_bin (da58510e...)
  - adv_{S1,S2,S3,S4,M1,M2}_run{1,2,3}.{txt,err} (18 transcripts)
  - ADV_EXEC_RECORD.md (full sealed execution record)

No em-dashes or en-dashes appear in this file.
