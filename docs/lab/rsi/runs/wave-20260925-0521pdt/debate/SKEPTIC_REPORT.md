# Skeptic Report, wave-20260925-0521pdt

Wave: wave-20260925-0521pdt
Debate group, depth 2/2. Role 2 of 3: SKEPTIC.
Job: attack gaming, confounds, weak bars, cost, and taint. A verdict can
be overturned only with cited evidence, never rhetoric.

## The provenance probe, answered per item (verbatim):

"What is the provenance of the artifacts under judgment, and what exactly
is new versus inherited?"

### Item 1: Fork battery

Provenance: FORK_RESULTS_0521.md in the working tree at
docs/lab/rsi/runs/wave-20260925-0521pdt/forks/FORK_RESULTS_0521.md.
New: the 0521pdt run itself, fresh enumeration via `git branch -a` and
`git worktree list`, the new local-archive-wave-0221pdt branch, the
run-start tip entry at 4050b1097. Inherited: the harness source
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738 from
the 2321pdt archive branch, the shell driver adapted from the frozen
0221pdt driver, and 26 fixture forks whose SHAs are unchanged.

Attack surface I checked:

1. The results file is UNCOMMITTED (git status shows `??` on the forks
   directory). The verdict CONFIRM rests on a working-tree file the
   coordinator has not yet committed. If the coordinator fails to
   commit it, the re-cert has no durable evidence. The confirmation
   must be conditioned on the commit.

2. Two of the 28 are named duplicates (origin-tnn-native-lab-runstart-tip
   duplicates origin/tnn-native-lab; local-archive-wave-0221pdt
   duplicates the local run-start tip). The 28/28 count therefore
   covers 26 unique commits. The duplicates are disclosed and named,
   which is honest, but 28/28 is a test count, not a unique-fork count.
   Nothing is hidden, but the framing should say 28 tests, 26 unique.

3. The brief-listed remote heads (origin/fs-gr1, origin/main,
   origin/r2-7, origin/reorg/phase-0-1, origin/wg-freeze) are not
   remote-tracking refs in this clone; they were fetched read only into
   FETCH_HEAD and extracted via `git show FETCH_HEAD:<path>`. The SHAs
   (e.g. origin-main 6e621178038f5e0dd61dafa7c70df1e9eca9eb3e) are
   reported as "unchanged since last wave" on the worker's word alone.
   Sequential FETCH_HEAD reuse is fragile: a second fetch overwrites
   FETCH_HEAD, so ordering discipline matters. No failure occurred this
   wave, and the reported SHAs are consistent, so this is a residual,
   not an overturn.

4. Mode drift (100644 vs 100755 on extracted znc copies) is asserted as
   metadata-only with every sha256 matching. Acceptable: byte equality
   of the executed copies is the operative fact, and it is reported per
   fork.

Verdict attack result: no overturn. 28/28 PASS stands, subject to the
commit caveat.

### Item 2: ST-1 STEREO FIELD

Provenance probe answer. "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?"

- New this wave: st1_stereo.zag (1387 lines, 42-stem world-panned
  renderer), st1_verify.zag (374 lines, the pure-Zag verifier), the
  WAVs st1_r1/r2/r3.wav, the traces, and EVIDENCE_ST1.md, all committed
  in 40c632bea. FIRST_RENDERED_WAVE: wave-20260925-0521pdt.
- Inherited: sub/synth_base.zag (vendored D-AUD-3 baseline; first 1065
  lines of st1_stereo.zag byte-identical, diff-verified), the D-AUD-3
  data source, the pinned znc 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
- Not stacked: S11-AUD (QUEUED-UNJUDGED) explicitly not stacked; no
  b_alpha contact.

Attack surface:

1. THE TAINT. The worker's own evidence discloses: "Python was briefly
   used for a text edit on st1_verify.zag, then reverted via backup and
   redone with a proper edit tool." Under the 1121pdt standing rule,
   any Python touch of a wave artifact voids that artifact's wave
   evidence. The operative condition is contact, and contact happened:
   st1_verify.zag was the artifact, Python touched it, the revert is
   self-attested with no byte-level proof (no pre-touch hash recorded,
   no diff of the revert). The committed blob is
   90c4d47e9ab79246f43b1b610d11f3846fff460d, and nothing in git can
   show whether those bytes were ever under Python's fingers.

2. Every KB verdict rests on the void verifier. The verifier audits the
   42 trace entries and computes KB2, KB4, KB6, KB7. KB1 (3/3
   byte-identical, 4e9ea742...) is a sha256 of WAVs produced by bin_st1,
   but the claim of three independent renders and the equality check
   were performed by the same tainted tooling chain. The crest ratio
   1.203907 (+1.61 dB) that kills the candidate is an output of the
   Python-touched verifier. The DEAD verdict therefore rests on void
   evidence. A verdict without citable evidence is not a verdict.

3. The advocate's escape hatch (the crest ratio is a pure function of
   the committed WAVs and is independently re-checkable) is true but
   unexercised. No pristine verifier has recomputed the numbers. A
   judge cannot cite a re-check that has not happened.

4. The honest-refusal narrative (worker refused post-hoc
   re-interpretation to the total-energy reading) is admirable but
   irrelevant to taint: refusing to game the bar does not un-touch the
   verifier.

5. Addendum A1: "conceived after implementation existed but before any
   implementation commit and before seeing energy numbers." The
   numeric bar did not change (plus/minus 0.5 dB), and the
   implementation commits after the addendum (12:57:39 UTC vs
   13:22:11 UTC), so commit order passes. But the timeline shows the
   implementation existed before the addendum was frozen, which narrows
   the meaning of "prereg strictly precedes implementation" to commit
   order only. Under the governance-tightened commit-order rule that is
   formally satisfied. Residual, not an overturn on its own.

6. Verifier segfault (bad _zag_free on slice pointers, frees removed).
   Disclosed. The segfault was at exit after printing results; results
   unaffected. Acceptable disclosure, but it adds to the
   trust-this-verifier stack: the tool that measured the killing number
   both segfaulted and was Python-touched.

Attack result: the DEAD verdict is OVERTURNED in form. Not because the
numbers are wrong (they may well be right), but because the evidence
they rest on is void under the standing rule. The correct disposition
is UNVERIFIABLE: the candidate is quarantined, the WAVs and traces
remain committed, and a future wave must re-verify from the committed
artifacts with a pristine verifier (written and run with zero Python
contact) before any verdict, including DEAD, can be rendered. The KB7
+1.61 dB reading is recorded as an untested hypothesis, not a finding.

### Item 3: CV-P stemmed-coverage gate

Provenance probe answer. "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?"

- New this wave: cvp.zag (the 108-line stemmed-coverage change),
  tools/score.zag, the sealed 30 probe set (63cef111d), the evidence
  and seal-open logs. FIRST_RENDERED_WAVE: wave-20260925-0521pdt.
- Inherited: adopted cv1c.zag (sha256
  6d8fb9f013ef3efa1bb44881f98cbeafcabd7110ae4fb7396a3e5721b34d7137),
  adopted gate_op.zag (730db584c81c5229fa110069e57b54f5a36b91b5ca8e080de2bb61c65349a33f),
  the frozen KB (3ef27296...), the frozen stemmer reused byte-verbatim
  (stem_inplace/irregular_norm untouched, including the write-family
  exclusion), the F8 atomic-claim check on raw canonical text.
- Note: CV-P builds on adopted CV-1 logic whose baseline integration
  is HELD pending Micah's Python-mirror ruling (sixth governance
  ruling). The lineage is tainted by an unresolved governance question,
  not by Python contact in this wave.

Attack surface:

1. Independent red-team: none was possible (depth 2/2). The evidence
   doc admits this and caps the verdict at PARTIAL per the frozen
   mapping. The self-review ran 9 structured attacks, but a self-review
   cannot see its own blind spots. Residuals: single-session authorship
   (author and implementer are the same worker), and the tie-break
   guard covers the known corridor only. This does not overturn
   PARTIAL; it is exactly why the verdict cannot be better than
   PARTIAL.

2. The empty Python invocation: `python3 - <<EOF / EOF` executed an
   empty program and touched no artifact. Under the 1121pdt M5
   precedent, the operative condition is contact with a wave artifact.
   An empty program that opened, read, and wrote nothing made no
   contact. There is no taint. Disclosed and clean.

3. Stacked-judgment risk: CV-P is a CV-1-family derivative, and the
   0221pdt judge ruling requires structural different-worker
   author/implementer separation before any CV-1-family adoption, which
   is unmeetable in one session. The worker does not claim adoption;
   the verdict is PARTIAL and the disposition is a rotated-author
   re-test. The one session's authorship is disclosed. No judgment is
   being stacked: nothing is integrated, CV-1 integration stays HELD,
   and this wave's result does not resolve the Python-mirror ruling.

4. Seal hygiene: PREREG (397a97c7a, 12:49:54 UTC, alone) strictly
   precedes seal (63cef111d, 13:09:05 UTC, alone) strictly precedes
   implementation (358a8013c, 13:29:24 UTC) precedes evidence
   (7d845b53a, 13:29:33 UTC) precedes seal-open log (5a7d6402f,
   13:30:22 UTC). Static grep finds no sealed probe bytes in cvp.zag;
   the candidate never reads KEY.md. The probe set was sealed before
   the implementation existed. Seal discipline is clean.

5. Gaming checks: diff is 108 lines in frozen scope; no probe-specific
   constants or per-probe branches; decline text still cites raw words;
   B5 machine check (0 covered-as-uncovered) is computed in Zag;
   degenerate strategies are ruled out by the 10/10 P-INF answers and
   the 10 specific declines with 0 confabulations. Cost 1.0626x is
   measured with identical counting discipline plus the explicit
   per-byte stem charge; wall clock not used. No gaming found.

6. Determinism: 3/3 runs byte-identical (transcripts sha256 c3e47587...,
   ops 57080df9...); zero RNG (static grep: 0 matches for rand). The
   byte parity B6 (17/17 INKB-17 turns identical to the adopted cv1c
   rebuild) guards the exact-form corridor; the residual (guard covers
   the known corridor only) is disclosed.

Attack result: no overturn. PARTIAL is the correct ceiling and the
correct floor. The queued disposition (rotated-author re-test on a
fresh sealed set before any adoption verdict) is confirmed, with one
precision: the queue entry must also record that CV-P's adoption chain
is doubly gated, by the rotated-author re-test AND by Micah's pending
Python-mirror ruling on the CV-1 family, and that a rotated-author
re-test cannot be run until a different worker exists to run it.

## Cross-item observations for the judge

1. The two taint incidents are materially different and must not be
   conflated: ST-1's was contact with a wave artifact (voids evidence);
   CV-P's was an empty program with no contact (no taint).

2. Self-attestation is the theme of this wave's weaknesses: the
   Python revert (ST-1), the harness rebuild, and the self-review
   (CV-P) all rest on the worker's word. The fork battery is the one
   item with no self-attestation gap that matters, because every number
   in FORK_RESULTS_0521.md is re-checkable from committed SHAs. That is
   the standard to hold the other items to.

3. No narrowing was requested or adopted in this debate. Frozen bars
   are untouched: KB7 stays plus/minus 1.5 dB for ST-1; CV-P's nine
   bars stay frozen; the pure-Zag rule is applied as written (contact
   is the operative condition).
