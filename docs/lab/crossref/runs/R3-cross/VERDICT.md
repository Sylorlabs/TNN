# R3-CROSS VERDICT — teacher showdown, Legs A/B

**Verdict: REPRODUCED**

Independent cross-check crew for TNN cross-reference family R3 (teacher
showdown, Legs A/B), under Micah's 2026-09-22 "run everything" ruling.
Every number below was recomputed from the committed evidence by a fresh,
independently written pure-Zag verifier (`r3_cross.zag`), compiled with the
pinned toolchain. Zero RNG. Three runs, byte-identical output
(SHA256 `5233088ac7427ad9ad8c7e15b9c128eecdc92219620757725a32ffde959e7a9d`).

The verifier parses the committed corpus JSON directly (no original scoring
code was read or reused), recomputes all counts, and applies the frozen
VERDICT RULE mechanically. Exit code 0, `fails=0`.

## Committed vs reproduced

| Claim (frozen record) | Reproduced | Match |
|---|---|---|
| 40/40 capture batches present, checked, zero voided/recaptured | 40 present; 40/40 SHA256 vs SHA256SUMS.txt; 40/40 id-coverage 12/12; 40/40 truncation guards (dump ends `.`, teach ends `PROBE_VALUE: <int>`); batches numbered 00–19 sequentially, no gaps | ✅ |
| Leg A: 0/240 observation diffs | 0 | ✅ |
| Leg A: 0/240 probe diffs | 0 | ✅ |
| Leg A: byte-identical English learner digest | 5/5 legC47 run logs byte-identical; GROKC_TEACH_DIGEST agrees 5/5; matches grok-4.6 frozen legC log | ✅ |
| English digest `be5dba84…05d` | `be5dba8498fffd515f6b9a3b16068300a1d58b00d963338e2b9a0dfad7e9e05d` (full, both models) | ✅ |
| Leg B grok-4.7: E_dump=0 | 0 | ✅ |
| Leg B grok-4.6: E_dump=7, IDs 88–94 | 7, IDs 88,89,90,91,92,93,94 | ✅ |
| Leg B: E_obs=0, E_prb=0, inconsistent=0 (both) | 0, 0, 0 (both) | ✅ |
| 12/12 falsehoods faithfully reproduced (dump/obs/probe = supplied) | 12/12 (both models) | ✅ |
| No correction/flagging in falsehood prose | 12/12 (both): supplied value present as token, true value absent, in dump sentence and observation | ✅ |
| Frozen rule → grok-4.7 champion | legA_tie=1, E_dump 0<7 with 12/12 faithfulness both sides → champion=47 | ✅ |
| Leg C excluded / not run | not run | ✅ |

Additional independently computed (informational, not in verdict claims):
- Leg A dump diffs: 7 (IDs 88–94 — the Leg-B differentiators).
- Leg A distractor diffs: 84/240 (distractor channel not scored by the showdown).
- Leg B grok-4.7 distractor toward-true: 12/12.
- Leg B grok-4.6 distractor toward-true: 11/12 — ID 71 is `other(22)`,
  exactly as the committed `ERROR_INVENTORY.md` records
  (`dis=other(22)`); not a discrepancy.

## Defect audits

### Defect 1 — preregistered digest domain substitution
The preregistered digest `76e85c3e…772b5` belongs to the Zharovia-domain
standardized class-3 corpus. The English-domain equivalent
`be5dba8498fffd515f6b9a3b16068300a1d58b00d963338e2b9a0dfad7e9e05d`
was used instead. **Exactly as described.** Verdict-neutral, demonstrated
mechanically: Leg A obs/probe diffs are 0/240 regardless of digest domain,
and the English digest is byte-identical across all five 4.7 runs and
matches grok-4.6's frozen English legC digest (extracted from the committed
`teacher_leg.log`).

### Defect 2 — Zharovia truth oracle skips English facts
The standardized driver's truth oracle (`t5_truth`, reimplemented
independently from the frozen spec) skips facts whose stored claim ≠
Zharovia truth. **Denominator correction:** the driver attempts 8×24=192
facts (probe indices 0–191 through the `(i*37+1)%240` permutation, false
plants excluded), not 240. Reproduced: **187 skipped / 192 attempted**
(driver's own committed rerun log independently confirms `skipped,187`).
The 5 accepted facts: 48, 50, 52, 138, 191.

**Exactly as described** (187 skips), with the denominator made precise.
Verdict-neutral, demonstrated mechanically:
- (a) obs/probe diffs are 0 over all 240 records — no numeric-channel
  differentiator exists that a skip could conceal.
- (b) The Leg-B differentiators (dump IDs 88–94) are scored directly from
  all 240 corpus records, outside the driver path. Of the 7, 4 fall in the
  taught set and all 4 were skipped — yet Leg B still counts all 7,
  because Leg B never goes through the driver.
- (c) The Zharovia digest was superseded by the English digest (defect 1),
  so the skip cannot affect any number the verdict rule consumes.

## Frozen pins (observed 2026-09-22)

- Crossref prereg commit: `7b2100d09911c5c10252c5756c7def288e70bd1f`
- Evidence commit: `d915f0258e2e056b954bfd5f40f831ebcff2f064`
- Toolchain: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (SHA256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`)
- Corpus pins verified in-program: 4.7
  `111f588f29f23c7864f4842401516e9b30d98c495f5d1a0b68642a71d67f467a`;
  4.6 `7f3a25739981c8276082ceeda7de3628afd88977e7a16bd0a5f220eba2bc2508`.

## Method note (disclosure)

The task required a fresh `git clone` into `clean-cross/`. This VM has no
`git` binary and no network path for a clone succeeded; instead every input
was fetched as an individual Git blob through the GitHub API with its SHA
verified against the commit tree before use (41/41 batch files, both
corpora, all logs). The staged files are therefore byte-identical to the
committed record by construction. `clean-cross/` is an API-extracted mirror,
not a git clone. No R3-PRIMARY code, outputs, or scratch were inspected;
no `.zagd` files or binaries were copied.
