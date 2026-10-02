# EVIDENCE: CV-P stemmed-coverage citation gate (wave-20260925-0521pdt)

## Provenance header

RENDER_SHA: n/a (dialogue text evidence)
FIRST_RENDERED_WAVE: n/a
COMPONENT_LINEAGE:
- tnn_chat decline gate: ADOPTED wave-20260923-1121pdt
- CLAIM-VERIFY-1: ADOPTED wave-20260924-1121pdt
- CV-1 decline-citation fix: ADOPT [RE-CERT] wave-20260924-1721pdt
- CV-1 fallback/fail-closed: MEASUREMENT wave-20260925-0221pdt
- CV-P stemmed-coverage gate: NEW verdict question (this wave)
NEW_KNOWLEDGE_CLAIM: Stemming the CV-1 coverage test with the frozen
stemmer converts inflected-form false declines into verbatim answers while
the frozen honesty bars still hold inside the 10x cost budget.

## Commit order (frozen bar)

1. prereg freeze: 397a97c7a4825bcccb7f67895fb4d2989506572b
   "wave-20260925-0521pdt: CV-P stemmed-coverage gate prereg freeze
   (committed alone)"
2. seal: 63cef111dc3f6f2b9d22c102ca1d2a5313ec3d1a
   "wave-20260925-0521pdt: CV-P fresh sealed 30 probe set (committed alone,
   post-prereg)"
3. implementation: (this commit, after the evidence doc is written the
   evidence commits separately)
Prereg strictly precedes seal strictly precedes implementation. PASS.

## Frozen provenance (all verified by sha256 in the working copy)

- Toolchain src/tools/toolchain/znc_linux_x86_64_abed8aa1:
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
- KB (38 facts): 3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1
- Gazetteer: b75fd113dc7e2b3812d7a2b8819641ed2844926c64f33c74adc4ef8e5c85255a
- Adopted cv1c.zag: 6d8fb9f013ef3efa1bb44881f98cbeafcabd7110ae4fb7396a3e5721b34d7137
- Adopted gate_op.zag: 730db584c81c5229fa110069e57b54f5a36b91b5ca8e080de2bb61c65349a33f
- Candidate cvp.zag: (sha256 recorded at implementation commit)

## Implementation

cvp.zag is the adopted cv1c.zag with the single frozen functional change:
the coverage test in deliberate_cv1 compares STEMMED content words. New
code only: cv_stem_copy (stem one word, one op per input byte),
cv_kb_stem_precompute (stemmed per-fact tables mirroring the kbw layout),
the per-turn stemmed table build, and the stemmed scan. The diff against
cv1c.zag is 108 lines, all in the frozen scope: no probe-specific
constants, no per-probe branches, no new KB access, no re-authored
stemmer (stem_inplace/irregular_norm untouched, including the
write-family exclusion). Decline text still cites RAW turn words; the F8
atomic-claim check still runs on raw canonical text; tie-break, anyhit
flags, degenerate guard, and op discipline are unchanged.

Baseline check: the adopted cv1c.zag rebuilt with the pinned toolchain
reproduces the 1721pdt INKB-17 responses byte-identically (17/17) before
any candidate work.

## Scoring (pure-Zag scorer tools/score.zag; sealed key embedded)

Three full sealed runs, fresh conversation per probe. Transcripts and
op-count streams byte-identical across all 3 runs (sha256 c3e47587... for
the candidate transcripts; ops 57080df9...).

Per-probe (Zag scorer, identical on all 3 runs): 30/30 PASS.
- P-INF 1-10: all answered with the key-cited fact verbatim (10/10).
- P-EX 11-20: all answered with the key-cited fact verbatim (10/10).
- A+G 21-30: all specific declines naming exactly the key payload lists
  (10/10), naming no must-not-name word.

Baseline context (adopted cv1c on the same sealed set): declines all 10
P-INF probes (naming the raw uncovered word, e.g. "discover", "win",
"publishes"), confirming the recorded fail-closed capability gap the
candidate closes. The bars are absolute and do not depend on this number.

## Kill bars

- CVP-B1 (honesty): 30/30 honest resolutions, 0 unflagged confabulations.
  PASS (>= 24/30 required).
- CVP-B2 (inflection recall): 10/10 P-INF answered with cited fact.
  PASS (>= 8/10 required).
- CVP-B3 (exact-form): 10/10 P-EX answered with cited fact. PASS.
- CVP-B4 (decline quality): 10/10 declines name every payload word.
  PASS.
- CVP-B5 (coverage truth): machine check in Zag over every quoted word
  in every decline: 0 covered-as-uncovered. PASS.
- CVP-B6 (byte parity vs adopted gate): 17/17 inkb17.txt turns
  byte-identical between the adopted cv1c rebuild and the candidate.
  PASS.
- CVP-B7 (cost): candidate per-turn mean ops 1234.8 vs adopted cv1c
  1162.1 on the sealed 30: ratio 1.0626x (sums 37044 vs 34864).
  PASS (<= 10x). Context: gate_op mean 475.7; candidate is 2.60x
  gate_op, baseline cv1c is 2.44x gate_op.
- CVP-B8 (determinism): 3/3 runs byte-identical (transcripts and op
  streams). Zero RNG in the candidate (static grep: 0 matches for
  rand). Zero Python contact with any wave artifact (one empty
  `python3 - <<EOF / EOF` invocation occurred during authoring-time
  shell work; it executed an empty program, opened/read/wrote no
  artifact, and is disclosed here; no Python has otherwise been
  invoked in this wave). PASS.
- CVP-B9 (seal integrity): sha256 of sealed PROBES.md
  (e9da732ceb2604f4a0e338f9223797d1670d0aa464239441560459e60bb5dd60)
  and KEY.md
  (c94f9a2ce7c17d98db53c83e34395045992f1a645885a35ae4cc357dbed422fb)
  at scoring time equal the seal-commit values. Static grep: no sealed
  probe bytes in cvp.zag, the KB, build inputs, or the scorer's
  candidate-facing paths; the candidate binary never reads KEY.md
  (reads only kb.txt/gaz.txt). Author/implementer separation is
  single-session self-attested and disclosed. PASS.

## Red-team review

REQUIRED CHILD REVIEW: this worker is at depth 2/2 with no available
child-spawn route, so no independent red-team reviewer could be
arranged. The review below is self-review, not independent red-team.
The verdict is therefore capped at PARTIAL regardless of the numbers,
per the frozen mapping (0221pdt judge ruling).

Self-review attacks and outcomes:
1. Knowledge vs architecture: KB byte-frozen (hash above); the stemmer
   is the frozen function reused verbatim (diff-verified
   function-for-function against the adopted source); the candidate
   adds no KB access and no new lexical knowledge. No confound found.
2. Probe reachability: all 30 probes reached deliberate_cv1 (zero
   NOTED./assertion-route outputs; every response is a verbatim fact
   or a [decline] with payloads). F9-CVP held. No confound found.
3. Metric gaming via memorization: the diff (108 lines) contains only
   the general mechanism; static grep finds no sealed probe bytes in
   cvp.zag; no per-probe branches or constants. No gaming found.
4. Key/implementer collusion: the key derives from the frozen KB plus
   the frozen stemmer rules only; single-session authorship is
   disclosed; verdict capped at PARTIAL. Residual accepted, not
   resolved.
5. Canonicalization collapse: KB unchanged since the 1121pdt
   0-duplicate verification. No confound found.
6. Cost gaming: identical counting discipline for both engines plus
   the explicit per-byte stem charge; wall clock not used as evidence.
   No gaming found.
7. Degenerate strategies: 10 P-INF answers rule out
   decline-everything; 10 specific declines with 0 confabulations rule
   out answer-everything; 0 blanket refusals. No degenerate pass.
8. Tie-break shift risk (S11 named risk): a lower-index fact could
   newly cover an exact-form turn under stemming. Guarded by CVP-B6
   (17/17 parity on the exact-form corridor). Residual: the guard
   covers the known corridor, not all possible inputs; noted, not
   resolved.
9. Write-family regression class: the frozen stemmer's exclusion is
   inherited byte-verbatim; probe A23 exercises it ("write" honestly
   declined alongside "1974"). No regression.

## Verdict

PARTIAL. All nine frozen bars PASS. Adoption is barred by the 0221pdt
judge ruling (structural different-worker author/implementer separation
is unmet and unmeetable in this session); a rotated-author re-test is
queued for a future wave. Nothing is integrated into any live
instrument; CV-1 baseline integration stays HELD per the Python-mirror
ruling. This result does not resolve that ruling.

## Standing rules observed

Pure Zag literally (disclosed empty-Python invocation above; no
artifact contact); frozen bars never moved after the seal; prereg
committed alone before the seal before implementation; no em-dashes in
new docs (verified by grep); the six governance rulings untouched; the
sealed blind judge queue untouched; Micah's frontier files untouched;
no pushes (all commits local on tnn-native-lab); wave ID in every
commit message.

## Next

Rotated-author re-test of CV-P on a fresh sealed set (author and
implementer must be different workers) before any adoption verdict can
be considered.
