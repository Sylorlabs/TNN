# REDTEAM: CV-1 decline-citation re-test (wave-20260924-1421pdt)

Role: independent red-team reviewer. I did not implement the candidate.
Every number below was recomputed independently with shell coreutils only
(sha256sum, md5sum, grep, awk, cmp, diff, git). No Python was used in this
review. No em-dashes appear in this document.

## Independent verdict: CONFIRM DISCARD

The worker's DISCARD recommendation is correct under the frozen verdict
mapping (ADOPT iff CVC-B1 through CVC-B8 all PASS; three bars fail). The
causal story is also correct in substance: the 10 misses never reached the
decline-citation mechanism. I refine the story, correct two misreported
evidence statements, and add one finding the worker missed that changes the
recommended F9 amendment.

## Recomputed evidence

### Commit order: PASS

- 963f872ae prereg freeze, 2026-09-24 21:48:54 UTC, PREREG_CV1_CITE_1421.md
  committed alone.
- de1cd2c42 seal, 21:52:26 UTC, probes_sealed/ (PROBES.md, KEY.md, SEAL.md)
  committed alone.
- 5c53da6ba implementation and evidence, 22:07:22 UTC.
- git merge-base confirms 963f872ae is an ancestor of de1cd2c42 which is an
  ancestor of 5c53da6ba. Only two commits in the repo touch
  candidates/cv1_cite/**, in this order. No cv1_cite file was committed
  before the prereg freeze. No UNVERIFIABLE ORDERING.

### Seal integrity: PASS on substance, one process defect

- Recomputed: PROBES.md
  1ea86906d404861144264fca4fabcb14ec31a45b5a8fca47b3ad2beb32af61bb,
  KEY.md
  8b4b6a89d99c262ad9af1d8b79c2b2011d4480fd38d7ab26e96c1cbfd15de115.
  Both match the SEAL.md pins and the seal-commit blobs byte for byte.
- Fresh set confirmed: the 1121pdt sealed shas are
  cf2f3293f0dd8fa23cbdaf07a5df95290f692af22c4dc1506636ce953b55db06
  (probes) and
  371cd2823f73ca64aaa8e0de8a12bf3834855a4eae03ccae1db4a12ee8f2992e
  (key). Different content, not a re-certified set.
- Process defect: the SEAL.md seal-open log was never filled in (still
  reads "to be filled at scoring time"). CVC-B8 asks for the seal-open to
  be logged by commit hash. The attestation exists in EVIDENCE section 7,
  but the log itself is blank. See also the undocumented-diagnostics
  finding below.

### Contamination: B8 scope clean; worker's grep statement misreported

- My grep of the CVC-B8 scope (cv1c.zag, gate_op.zag, R33_NATIVE_IO_V1.zag,
  R33_NATIVE_SHA256_V2.zag, runs/kb.txt, runs/gaz.txt) for the worker's
  16-word list returns 0 hits. No KEY.md or probes_sealed read exists in
  the candidate source (the single "sealed set" mention is a code comment
  on a defensive path). CVC-B8 passes on its frozen terms.
- Correction: the EVIDENCE section 5 claim "grep over impl/ for 16
  sealed-distinctive words ... 0 hits" is false as written. My grep over
  impl/ with the same list hits runs/adv30.txt, runs/cand_adv30.txt,
  runs/qmark.txt, runs/named_words.txt, and EVIDENCE_CV1_CITE.md itself.
  These are training inputs and scoring transcripts, not mechanism
  artifacts, so this is an evidence-accuracy defect, not a seal breach.
  The evidence sentence should be corrected to the B8 scope.
- Related: ADV-30 training inputs share distinctive vocabulary with the
  sealed set ("mona lisa"/"da vinci" in adv30.txt line 3 vs sealed A05/G07;
  "cipher" in adv30.txt line 33 vs sealed A07/G05). The training set was
  authored pre-seal and the mechanism is general (see diff finding), so
  this is topical overlap, not leakage. It slightly weakens the
  training-battery independence narrative. CVC-B5 is a no-regression
  battery, so its result stands.
- Diff of cv1c.zag against the adopted 1121pdt cv1.zag: 78 changed lines,
  all the prereg-specified rule edits (3-word cap removed, anyhit
  coverage flags added, best-fact selection removed, full uncovered list
  cited, fail-closed and empty-uncovered fallback texts). Zero sealed
  probe words in the diff. No per-probe branches. The mechanism is
  general, as attested.

### The 10 misses: confirmed NOTED from the frozen path-4 handler

- PROBES.md contains zero "?" characters (grep count 0). Confirmed.
- The 10 misses (P01, P03, P04, P05, P09, P10, A04, A06, G05, G09) emit
  "tnn> NOTED." in sealed_r1.txt at exactly the expected positions.
- The NOTED output lines are byte-identical between candidate and frozen
  baseline: md5 e6478a2671d9f178e8c9e8402ebc3e22 for both (this resolves
  the EVIDENCE number; it is the md5 of the 10 transcript NOTED lines).
  The two-probe NOTED test transcripts are md5
  ce6198484b4429389d661fc0a525d684 across candidate, baseline, and the
  1121pdt binary. Frozen behavior, not a regression, not a citation-rule
  defect.
- Refinement (new): I executed the committed cv1c binary on the worker's
  undocumented runs/qmark.txt. Results: P01 assertion form gives NOTED;
  the P01 interrogative form ("moby dick was written by herman
  melville?") gives the fact-3 answer verbatim; A01 assertion form gives
  the same correct decline as the sealed run. And runs/noted2.txt (two
  interrogative-form probes containing assertion fragments) gives NOTED
  twice. So routing is frozen extract_assert pattern plus gazetteer
  entity matching, not "?"-absence alone: interrogative form is necessary
  but not sufficient. All 10 misses match assertion patterns with
  gazetteer entities (" was written by ", " was born in ", " is in ",
  " is the capital of ", " meters tall ", " wrote "). A01 has
  " was written by " but "bradbury" is not a gazetteer entity, so it
  reached the mechanism and passed.

### The 20 path-5 probes: 20/20 confirmed from the raw transcript

- I graded every line of scoring/sealed_r1.txt against KEY.md directly:
  16 declines each name every key-listed payload word and no other quoted
  words outside the key's uncovered list; 4 answers (P02, P06, P07, P08)
  are the cited facts verbatim (each confirmed present in kb.txt).
- Independent CVC-B3 machine check: 92 unique quoted words across all
  declines, 0 found in kb.txt (case-insensitive whole-word). No covered
  word named. The A02/martian class is absent on all tested probes.
- Zero unflagged confabulations; no false coverage claim in any decline
  (declines emit only the frozen template; the fail-closed and
  empty-uncovered fallbacks never fired on the sealed set).
- Caveat: 20/20 is conditional on reaching path 5. The subset is not
  random; it is exactly the non-assertion-pattern probes. "Mechanism
  vindicated" is accurate only in this conditional sense and must not be
  promoted to a bar pass.

### Bar mapping: confirmed as the worker reports

- CVC-B1: 20/30 vs bar 24/30, 0 confabulations. FAIL.
- CVC-B2: 16/20 vs bar 100 percent. FAIL.
- CVC-B3: 0 covered-as-uncovered, machine-checked. PASS.
- CVC-B4: 4/10 paraphrases answered (FAIL on part i); decline text clean
  (part ii holds). Overall FAIL.
- CVC-B5: 17/17 INKB byte-identical, sha256
  db6b707550865331666a2cf52d3c930a359c1d114ddf41f11a84656dbef4e7d5
  for both transcripts; 30/30 ADV-30 specific declines, 0 blanket
  refusals. PASS.
- CVC-B6: candidate mean 1338.07 vs baseline mean 833.90 ops/turn from the
  committed op streams, ratio 1.6046, inside the 10x budget. PASS.
- CVC-B7: sealed_r1/r2/r3 byte-identical, md5
  0c6fc375bfeb60a6f023c3384cd6005f; op streams identical. PASS.
- CVC-B8: PASS on substance (shas match; source/KB/build/scorer clean);
  seal-open log blank (process defect noted above).

## Rulings

### Q1. DISCARD confirmed; framing is probe-form defect rooted in a prereg-spec gap

DISCARD is the correct verdict. The frozen verdict mapping is unambiguous
and the bars are evaluable: the grading rules define exactly what a miss
is, and the 10 NOTED probes are real misses under them. "Unevaluable" is
the wrong frame because it would imply the mapping should not fire; it
does and it did.

The causal attribution is also correct with two amendments. First, it is
not only a probe-authoring slip: F9 never specified interrogative form,
and the prereg's confound list never considered path-4 interception (its
F9 guarantee addressed the empty-uncovered fallback, the wrong failure
mode). The misses are therefore a prereg-spec gap realized through the
probe author's literal F9 compliance. Second, the precise routing cause is
assertion-pattern plus gazetteer matching, not mere "?"-absence, per the
noted2 finding.

On evasion: NOTED is not decline-shaped gaming. It scores as a miss under
every frozen grading rule, so no bar is gamed by it.

On the worker's recommendation: re-authoring a fresh sealed set for a new
wave against the unchanged implementation is sound, but the F9 amendment
must require interrogative forms AND exclude frozen assertion-pattern
fragments with gazetteer entities. Requiring "?" alone is insufficient;
the noted2 interrogative probes still route to NOTED. The worker missed
this. The 20/20 conditional result supports re-running the unchanged
implementation, framed as a new evaluation, not a continuation.

### Q2. Python contact: no evidence void

The disclosed contact was one accidental `python3 -c` computing the cost
ratio from two literal numbers typed on the command line. It touched no
wave artifact, read no file, wrote no file, and its output was not used as
evidence. The ratio stands on the committed op streams: I recomputed
1338.07 / 833.90 = 1.6046 independently. Under the 0521pdt prospective
rule ("any Python contact with a wave artifact voids the evidence") the
operative condition is contact with an artifact; there was none, so no
evidence is void. The 1121pdt M5 precedent (accidental python3 -c,
no artifact touched, disclosure recorded, memo stood) applies squarely.
Ruling: nothing is void; the disclosure is adequate; the cost number is
independently reproducible from committed artifacts. Nit: the EVIDENCE
does not record the awk command itself, but the op streams are committed
and recomputable, which is sufficient.

### Q3. No bar moved, no metric gaming; four evidence-quality findings

No frozen bar was moved after the fact: the prereg's CVC-B1 through CVC-B8
match the verdict application exactly. No metric gaming found: NOTED
cannot inflate any bar, the cost discipline is identical for both engines,
and determinism is byte-verified.

New findings (evidence quality, not verdict-changing):

1. Contamination grep misreported: "0 hits over impl/" is false; hits
   exist in training inputs and scoring transcripts. CVC-B8's frozen scope
   is clean, so B8 stands, but the evidence sentence must be corrected.
2. Training/sealed topical overlap ("mona lisa"/"da vinci", "cipher")
   weakens the training-battery independence narrative slightly. Not a
   breach; CVC-B5 unaffected.
3. Undocumented diagnostics: runs/qmark.txt and runs/noted2.txt were
   committed in the impl commit, are never mentioned in EVIDENCE or
   VERDICT, and qmark.txt contains sealed probe verbatims (P01, A01).
   File timestamps (21:57 to 21:58, after the 21:55 binary build and the
   21:52 seal) plus the clean source diff exonerate pre-implementation
   contamination, and I used these files to independently confirm the
   root-cause story. But combined with the blank seal-open log, the
   author/implementer separation attestation is not fully auditable from
   the record. Next wave should fill the seal-open log at scoring time
   and document every diagnostic input and output.
4. The worker's recommended F9 fix (require "?") is insufficient per the
   noted2 runs: interrogative probes containing assertion fragments still
   hit path-4. The F9 amendment must also exclude frozen assertion
   patterns with gazetteer entities.

## Bottom line

CONFIRM DISCARD. Killing evidence: 10 of 30 sealed probes were intercepted
by the frozen path-4 assertion handler (F9 form defect: no interrogative
requirement, no assertion-pattern exclusion), yielding CVC-B1 20/30,
CVC-B2 16/20, CVC-B4 4/10 against frozen bars. Exonerating evidence: on
the 20 probes that reached the mechanism, 20/20 (16/16 declines name every
payload word, 0 covered words named by independent machine check, 4/4
answers verbatim), cost 1.60x, determinism 3/3, no regression. The citation
rule is not implicated; the next wave should amend F9 as specified above
and re-run this unchanged implementation against a fresh sealed set.
