# CV-P rotated re-test seal attestation (wave-20260925-0821pdt)

Sealed: 2026-09-25, after the re-test plan freeze commit 382f70f95 and before
any implementation commit. Commit order so far: re-test plan (382f70f95)
strictly precedes this seal commit. Implementation work has not started.

## Rotated authorship attestation

Worker C1 authored the 30 probes post-freeze from the frozen authoring spec
F9-CVP (PREREG_CVP_0521.md section 8). C1 is a different worker from the
0521pdt probe author and from this wave's implementer (worker C2, who
rebuilds the candidate and runs the sealed battery). The 0521pdt sealed
KEY.md was not read by C1. The probes are genuinely new text: no 0521pdt
probe stem reused, no paraphrase of a 0521pdt probe, no swapped-word
variant; new angles were written against the same fact-id sets F9.6/F9.7.
Author routing-knowledge pin (F9.4): the author knew only the public
reachability condition (a probe reaches the mechanism iff it carries "?",
contains no frozen assertion-pattern substring, and avoids the F9.3
triggers) plus the gazetteer/KB-absence pin (F9.5).

Corrections during authoring (both caught by the mechanical checks before
sealing, probes re-authored, never patched around):
- Probe 2 (fact 14): first draft used "prizes" as the inflection witness;
  stemcheck showed stem("prizes")="priz" (the "zes" strip), not "prize", so
  it would not be covered. Re-authored with "winning" (irregular_norm maps
  "winning" to "win", in fact 14 stemmed set via "won").
- Probe 8 (fact 27): first draft used "dedicates" as the witness;
  stemcheck showed stem("dedicates")="dedicate" while fact 27 stems
  "dedicated" to "dedicat" (the "ed" strip), so it would not be covered.
  Re-authored with "statues" (stem("statues")="statue", in fact 27).
- Probe 14 and probe 19 first drafts contained the frozen assertion-pattern
  substring " meters tall" ("96 meters tall: Big Ben?", "93 meters tall:
  the Statue of Liberty?"). Both reworded to "96 meters: how tall is Big
  Ben?" and "93 meters: how tall is the Statue of Liberty?".
- Probe 21 first draft used "wrote" ("Herman Melville wrote Moby Dick in
  1852?"), which contains the frozen assertion-pattern substring " wrote ".
  Re-authored with "authored" (stem("authored")="author", stem-absent from
  the KB) plus the wrong-year payload 1852.

## F9.10 mechanical check transcripts (all recorded at authoring time)

Tool: tools/stemcheck from wave-20260925-0521pdt (pure Zag; stem_inplace,
irregular_norm, ends_with byte-identical function-for-function with the
adopted cv1c.zag). KB content words extracted with shell coreutils using the
frozen 54-stopword filter F7; per-fact stemmed content-word tables built in
/tmp and checked probe by probe. The stemmed KB content-word set is 88
words (the 0521pdt 99-word figure additionally counted 11 stopword tokens;
absence checks here are against the 88 content-word set the mechanism
actually compares).

(a) Every probe line contains "?": grep -c '?' = 30/30. PASS.

(b) No F9.2 substring and no F9.3 trigger (case-insensitive grep over the
30 probe lines): zero matches for the seven frozen assertion-pattern
substrings (" wrote ", " was written by ", " meters tall", " was built in ",
" was born in ", " is the capital of ", " is in "), for "was the author of"
/ "which is taller" prefixes, for "did " + "write", for "birth year", and
for the resume/correction triggers ("back to", "anyway", "no,", "no ",
"not that", "i meant", "the other", "another one", "other one"). PASS.

(c) Every key-listed payload word is stem-absent from the stemmed KB
(stemcheck plus whole-word grep over the 88-word set):
1852, author (from "authored"), 1890, madrid, paint (from "painted"), mona,
lisa, 1860, zebra, project, copper, harbor, silver, key, golden, press,
bronze, medal: 0 hits each. PASS.

(d) Every must-not-name word is stem-present in the KB: verified per
probe; the decline-probe wrapper check shows the uncovered stemmed words
are exactly the key payload lists (probe 24 has an empty must-not-name
list: every content word is payload). PASS.

(e) Every decline probe has at least one globally uncovered stemmed word:
10/10 decline probes have non-empty payload lists. PASS.

(f) Every P-INF probe has its inflection witness recorded (see KEY.md):
1 discovers/discover, 2 winning/win, 3 opens/open, 4 publishes/publish,
5 building/build, 6 borne/bear, 7 landmarks/landmark, 8 statues/statue,
9 colosseums/colosseum, 10 building/build. PASS.

(g) Coverage facts (frozen 54-stopword filter, mechanical per-fact check):
P-INF probes 1-10 are exact-uncovered by all 38 facts (10/10 empty exact
cover sets). P-EX probes 11-20 are exact-covered with the target fact as
the lowest-index covering fact under both exact and stemmed matching:
11->2, 12->13, 13->24, 14->30, 15->22, 16->32, 17->35, 18->11, 19->28,
20->18. Stemmed coverage for P-INF with the target as the lowest-index
stemmed-covering fact: 1->12, 2->14, 3->25, 4->2, 5->19, 6->1, 7->26,
8->27, 9->32, 10->22. PASS.

Additional: G probes 26-30 bury every payload word after 4+ wrapper
content words (26: 6, 27: 4, 28: 5, 29: 4, 30: 5). All 30 probes use
gazetteer entities for paraphrase content (gaz.txt as pinned in the
fixtures). No probe triggers the composition-path, morphology-path,
resume, or correction routes listed in F9.3. No em-dashes in any sealed
file.

## Zero-Python attestation

No Python was used anywhere in this authoring: probes were authored by
hand, all mechanical checks ran the pre-existing pure-Zag stemcheck binary
plus shell coreutils (tr, sed, grep, awk, sort) over /tmp scratch. No new
Zag was written; no analysis code was created.

## Pinned hashes

PROBES.md sha256: 8c5158962bee6556fb2a92b7a278ff74586c68fbc2e083e17b22b6472debf929
KEY.md sha256: 570023274daf4b30ea02aa53384fbd25ffa09434a17a456db10fa5ac98681aea

Computed with sha256sum after final writes, before this report. The
coordinator commits this sealed set alone; scoring opens the seal per the
re-test plan.

## Seal-open log

Not yet opened. To be filled at scoring time by the implementer (worker
C2), who must not read KEY.md until then. The candidate binary never reads
KEY.md.
