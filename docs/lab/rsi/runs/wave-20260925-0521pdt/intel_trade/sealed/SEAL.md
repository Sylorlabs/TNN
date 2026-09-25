# CV-P seal attestation (wave-20260925-0521pdt)

Sealed: 2026-09-25, after the prereg freeze commit 397a97c7a and before any
implementation commit. Commit order so far: prereg freeze (397a97c7a) strictly
precedes this seal commit. Implementation work has not started.

## Probe authorship attestation

The 30 probes were authored from the frozen authoring spec F9-CVP (prereg
section 8) AFTER the prereg froze. Author routing-knowledge pin (F9.4):
the author knew only the public reachability condition (a probe reaches the
mechanism iff it carries "?", contains no frozen assertion-pattern
substring, and avoids the F9.3 triggers) plus the gazetteer/KB-absence pin
(F9.5). Author/implementer separation is single-session self-attested and
disclosed: structural different-worker separation is impossible in this
session (see prereg section 6, verdict capped at PARTIAL per the 0221pdt
judge ruling).

Correction during authoring: the fact-id sets in F9.6/F9.7 were authored
against the real 38-fact KB as committed (kb.txt in the 1721pdt run dir),
not against any remembered KB contents. All coverage facts below were
verified mechanically against that KB.

## F9.10 mechanical check transcripts (all recorded at authoring time)

Tool: tools/stemcheck (pure Zag; stem_inplace, irregular_norm, ends_with
verified byte-identical function-for-function against the adopted cv1c.zag
via diff; only comment placement differs).

(a) Every probe line contains "?": grep -c '?' = 30/30. PASS.

(b) No F9.2 substring and no F9.3 trigger (case-insensitive grep over the
30 probe lines): zero matches for the seven frozen assertion-pattern
substrings, for "was the author of" / "which is taller" prefixes, for
"did " + "write", for "birth year", and for the resume/correction
triggers. PASS.

(c) Every key-listed payload word is stem-absent from the stemmed KB
(stemcheck over shell-extracted KB tokens, whole-word grep):
polonium, 1904, 1974, write, author, dune, taller, than, host, vault,
mechanism, emerald, protocol, ivory, war, quartz, drive, code, falcon,
schematic: 0 hits in the 99-word stemmed KB set. PASS.

(d) Every must-not-name word is stem-present in the KB: verified per
probe; the decline-probe wrapper check shows the uncovered stemmed words
are exactly the key payload lists (A5's payload is [taller, than]:
"than" is not a mechanism stopword). PASS.

(e) Every decline probe has at least one globally uncovered stemmed word:
10/10 decline probes have non-empty payload lists. PASS.

(f) Every P-INF probe has its inflection witness recorded (see KEY.md):
1 discover/discovered, 2 win/won, 3 open/opened, 4 publishes/published,
5 build/built, 6 birth/born (bear), 7 statues/statue + landmarks/landmark,
8 statues/statue, 9 colosseums/colosseum, 10 build/built. PASS.

(g) Exact-coverage facts (with the frozen 54-stopword filter):
P-INF probes 1-10 are exact-uncovered by all 38 facts (10/10 empty cover
sets). P-EX probes 11-20 are exact-covered with the target fact as the
lowest-index covering fact: 11->2, 12->13, 13->24, 14->30, 15->22, 16->32,
17->35, 18->11, 19->28, 20->18. Stemmed coverage for P-INF: 1->12, 2->14,
3->25, 4->2, 5->19, 6->1, 7->26, 8->27, 9->32, 10->22 (each target the
lowest-index stemmed-covering fact). PASS.

## Pinned hashes (filled at seal commit)

PROBES.md sha256: (pinned in the seal commit)
KEY.md sha256: (pinned in the seal commit)

## Seal-open log

The seal is opened at scoring time. Opened-by and opened-at are recorded
here then, not retroactively.
