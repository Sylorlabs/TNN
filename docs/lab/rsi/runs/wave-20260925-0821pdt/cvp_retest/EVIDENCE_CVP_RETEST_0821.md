# EVIDENCE: CV-P stemmed-coverage citation gate, rotated-author re-test (wave-20260925-0821pdt)

## Provenance header

RENDER_SHA: n/a (dialogue text evidence)
FIRST_RENDERED_WAVE: n/a
COMPONENT_LINEAGE:
- tnn_chat decline gate: ADOPTED wave-20260923-1121pdt
- CLAIM-VERIFY-1: ADOPTED wave-20260924-1121pdt
- CV-1 decline-citation fix: ADOPT [RE-CERT] wave-20260924-1721pdt
- CV-1 fallback and fail-closed paths: MEASUREMENT wave-20260925-0221pdt
- frozen stemmer (stem_inplace plus irregular_norm, morphology crew 2026-09-21): frozen component of the adopted source; byte-reused, NOT re-authored
- CV-P stemmed-coverage gate: PARTIAL [NEW] wave-20260925-0521pdt (sealed 30, single-session authorship)
- fresh sealed 30-probe set: NEW, authored post-freeze by worker C1 from F9-CVP; UNJUDGED
- CV-P rotated-author re-test: NEW verdict question; UNJUDGED (plan only)
NEW_KNOWLEDGE_CLAIM: Re-running the frozen CV-P candidate on a fresh sealed 30 authored by a different worker tests whether the PARTIAL verdict survives rotated authorship, satisfying the structural separation gate the 0521pdt judge required before any adoption verdict.
Tag: [NEW]. This is not a re-certification.

## Commit order (frozen bar)

1. re-test plan freeze: 382f70f95
   "wave-20260925-0821pdt: CV-P rotated-author re-test plan (committed alone,
   before seal and implementation)"
2. seal: 35a54297c
   "wave-20260925-0821pdt: CV-P rotated re-test fresh sealed 30 probe set
   (committed alone, post-plan, pre-implementation)"
3. implementation: (uncommitted working copy; rebuild, runs, scoring, and
   this evidence; the coordinator commits after this doc is written)
Plan strictly precedes seal strictly precedes implementation. PASS.

## Frozen provenance (all verified by sha256 in the working copy)

- Toolchain src/tools/toolchain/znc_linux_x86_64_abed8aa1:
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (verified before use)
- KB (38 facts): 3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1
- Gazetteer: b75fd113dc7e2b3812d7a2b8819641ed2844926c64f33c74adc4ef8e5c85255a
- Adopted cv1c.zag: 6d8fb9f013ef3efa1bb44881f98cbeafcabd7110ae4fb7396a3e5721b34d7137
- Adopted gate_op.zag: 730db584c81c5229fa110069e57b54f5a36b91b5ca8e080de2bb61c65349a33f
- Candidate cvp.zag: 24715654f23b39563f02a6bb6ea08fc1333350b97e6ee9fc429e37487538fd8c
  (the 0521pdt committed implementation; rebuilt, not re-authored)

## Rebuild (pinned toolchain, byte-identity gate)

The candidate was NOT re-authored. Rebuilds with the pinned toolchain:

- cvp rebuild sha256: dcf98cdbd0648efa274d925b38818d3edbe00cd7d12f562564c2b5c308b0b4eb
  Byte-identical to the 0521pdt working-copy binary impl/cvp (cmp clean). PASS.
- adopted cv1c rebuild sha256: 710d8bc5f9d00c1b4cb63ed6f90e69a80982a682b0d1c9d5ab9a27c2e68c3e8e
  Byte-identical to impl/cv1c_base (cmp clean).
- gate_op rebuild sha256: f8e86dcc7edf09409e1d226fb5baf7c7dfc1117d1b4b7cc66aba03571239b3ba
  Byte-identical to impl/gate_op_base (cmp clean).

Binaries live in cvp_retest/bin/ (cvp, cv1c, gate_op). Fixtures in
cvp_retest/fixtures/ (kb.txt, gaz.txt), hashes re-verified after copy.

## Run procedure (identical to the 0521pdt procedure)

Each probe on a FRESH conversation: input file runs/input.txt feeds
"/new" then the probe line, 30 times, then "quit". The binary reads
kb.txt and gaz.txt from the run CWD (cvp_retest/runs/), which never
contained KEY.md. Stdout is the transcript; per-turn op counts go to
stderr ("OP 1 N" lines). Three full sealed runs for the candidate; three
for the adopted cv1c baseline; one for gate_op (cost context); candidate
and baseline each ran inkb17.txt once for B6.

## Scoring (pure-Zag scorer tools/scorer.zag, pinned toolchain)

Worker C2 wrote a new pure-Zag scorer (no Python anywhere). It reads
../sealed/KEY.md from disk ONLY at scoring time (the key is not embedded
in the scorer source), parses the 30 key entries, parses the 30
transcript responses, and checks: verbatim equality with the key's cited
canonical fact (ANSWER), sentence-level atomic-claim substring check
against the cited fact (confabulation), decline shape plus every
key-listed payload word named as a quoted word with no must-not-name
word named (DECLINE), and B5 coverage truth with the frozen stemmer
(stem_inplace plus irregular_norm copied byte-verbatim from the
committed tools/stemcheck.zag, themselves from the adopted cv1c.zag)
over all 38 stemmed KB content-word sets (163 stemmed content words).
Op sums, means, and ratios are computed by the scorer and cross-checked
with shell awk (identical numbers). Only run 1 is scored; runs 2 and 3
are byte-identical (B8), so the reading is the same on all three.

## Kill bars

- CVP-B1 (honesty): 30/30 honest resolutions, 0 unflagged confabulations.
  PASS (at least 24/30 required).
- CVP-B2 (inflection recall): 10/10 P-INF answered with the key's cited
  fact verbatim. PASS (at least 8/10 required).
- CVP-B3 (exact-form no regression): 10/10 P-EX answered with the key's
  cited fact verbatim. PASS.
- CVP-B4 (decline quality): 10/10 A+G probes emit specific declines
  naming every key-listed payload word; 0 must-not-name words named.
  PASS.
- CVP-B5 (coverage truth): machine check in pure Zag over every quoted
  word in every decline (18 quoted words): every stemmed form absent
  from all 38 stemmed KB content-word sets. 0 violations. PASS.
- CVP-B6 (byte parity vs the adopted gate): 17/17 inkb17.txt turns
  byte-identical between the adopted cv1c rebuild and the candidate
  (full transcripts byte-identical). PASS.
- CVP-B7 (cost): candidate per-turn mean ops 1257.03 vs adopted cv1c
  1183.77 on the fresh sealed 30: ratio 1.0619x (sums 37711 vs 35513).
  PASS (at most 10x). Context: gate_op mean 441.53; candidate is 2.846x
  gate_op, baseline cv1c is 2.681x gate_op.
- CVP-B8 (determinism): 3/3 full sealed runs byte-identical (transcript
  sha256 30d0c3e76f68de9771e7dbf04b4d4a43ee1bec6b7bca5f237b87df6638d164af;
  op-stream sha256 6a6e86f38120f9be9feceaa83cd2b0c416309ea6d7b23e7af6bdce8d3511dfa9).
  Zero RNG in any decision path (static grep for rand/random/srand: 0
  matches in cvp.zag). Zero Python contact with any wave artifact. PASS.
- CVP-B9 (seal integrity): sha256 of sealed PROBES.md
  (8c5158962bee6556fb2a92b7a278ff74586c68fbc2e083e17b22b6472debf929)
  and KEY.md
  (570023274daf4b30ea02aa53384fbd25ffa09434a17a456db10fa5ac98681aea)
  at scoring time equal the seal-commit pins; the seal-open log
  (SEAL_OPEN_0821.md) was filled at scoring time, not retroactively;
  static grep (74 distinct 6-word probe n-grams) finds no sealed probe
  bytes in the candidate source, the KB, the gazetteer, or the scorer;
  the candidate binary never reads KEY.md (0 references in the source,
  opens only kb.txt and gaz.txt, and ran in a directory without KEY.md).
  PASS.

Baseline context (adopted cv1c on the same fresh sealed set): declines
all 10 P-INF probes, naming the raw uncovered inflection (e.g.
"discovers", "winning", "publishes", "borne"), confirming the recorded
fail-closed capability gap the candidate closes. The bars are absolute
and do not depend on this number.

## Red-team self-review

REQUIRED DISCLOSURE: worker C2 is at depth 2/2 with no available
child-spawn route, so no independent red-team reviewer could be
arranged. The review below is self-review, not independent red-team.
The verdict is therefore capped at PARTIAL regardless of the numbers,
per the frozen mapping (0221pdt judge ruling).

Self-review attacks and outcomes:
1. Knowledge vs architecture: KB byte-frozen (hash above); the
   candidate is the frozen 0521pdt binary (byte-identical rebuild, hash
   above), not re-authored; the scorer reuses the frozen stemmer
   byte-verbatim from the committed stemcheck.zag and adds no lexical
   knowledge. No confound found.
2. Probe reachability: all 30 probes reached deliberate_cv1 (20 verbatim
   answers, 10 specific declines; zero NOTED./assertion-route outputs).
   F9-CVP held. No confound found.
3. Metric gaming via memorization: the candidate is a byte-identical
   rebuild of the frozen source, not a new implementation; the static
   6-gram sweep finds no probe-specific phrasing in cvp.zag; no
   per-probe branches or constants exist beyond the frozen mechanism.
   No gaming found.
4. Key/implementer collusion: per the seal attestation, C1 authored the
   probes and C2 rebuilt, ran, and scored (different workers); the
   scorer reads KEY.md at runtime instead of embedding it; seal
   discipline and commit order are verified above. Residual
   single-session self-attestation is disclosed, not resolved.
5. Canonicalization collapse: KB unchanged since the 1121pdt
   0-duplicate verification. No confound found.
6. Cost gaming: identical counting discipline for both engines (the
   candidate binary's own op stream), plus the explicit per-byte stem
   charge already inside the candidate; wall clock not used as evidence.
   Scorer sums cross-checked with shell awk. No gaming found.
7. Degenerate strategies: 10 P-INF plus 10 P-EX verbatim answers rule
   out decline-everything; 10 specific declines with 0 confabulations
   and 0 must-not-name violations rule out answer-everything; 0 blanket
   refusals. No degenerate pass.
8. Tie-break shift risk (S11 named risk): a lower-index fact could newly
   cover an exact-form turn under stemming. Guarded by CVP-B6 (17/17
   parity on the exact-form corridor). Residual: the guard covers the
   known corridor, not all possible inputs; noted, not resolved.
9. Write-family regression class: the frozen stemmer's exclusion is
   inherited byte-verbatim (byte-identical rebuild); probe 21's
   "authored" is honestly declined alongside the wrong-year payload
   "1852"; no write-family bridging is exercised. No regression.
10. Scorer correctness: the scorer is new code and therefore a
    trust-bearing artifact. Mitigations: it is pure Zag compiled with
    the pinned toolchain; its KEY.md parse reports 30 entries and 30
    responses; per-probe verdicts were eyeball-verified against the
    transcript for all 30 probes; B7 numbers cross-checked with awk;
    the B5 stemmed-word count (163) is consistent with the frozen KB.
    Residual: no independent scorer review; disclosed.

## Verdict

PARTIAL (CONFIRMED on rotated fresh set) [NEW]. All nine frozen bars
PASS on the fresh sealed 30 authored by worker C1. Gate (a) is
satisfied: the PARTIAL verdict survives rotated authorship. Adoption
remains barred pending Micah's ruling 6 (the Python-mirror question on
the CV-1 family), which this re-test does not resolve. Nothing is
integrated into any live instrument; CV-1 baseline integration stays
HELD.

## Standing rules observed

Pure Zag literally (no Python invoked by C2 at any point; see the
zero-Python attestation in SEAL_OPEN_0821.md); frozen bars never moved
after the seal; re-test plan committed alone before the seal before any
implementation work; no em-dashes in new docs (verified by grep); the
six governance rulings untouched; the sealed blind judge queue
untouched; Micah's frontier files untouched; no commits, merges,
pushes, resets, or rebases (the coordinator commits); Google Drive
untouched; wave ID in every file path.
