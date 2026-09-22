# GOAL-B trial table

B5: 3 fresh-process reruns byte-identical (cmp rep1/rep2/rep3). B4: kb.txt sha256 unchanged; 0/16 stories share a >=16-byte substring with kb.txt; composer source has no write path to kb.txt (O_RDONLY reads only).

| trial | set | variant | B1 words | B2 sol | B2 native* | B3 novel |
|---|---|---|---|---|---|---|
| T01 | S1 | POS | PASS | 2 | 2 | PASS |
| T02 | S1 | DEL | PASS | 3 | 3 | PASS |
| T03 | S2 | POS | PASS | 2 | 2 | PASS |
| T04 | S2 | DEL | PASS | 4 | 4 | PASS |
| T05 | S3 | POS | PASS | 2 | 2 | PASS |
| T06 | S3 | DEL | PASS | 3 | 3 | PASS |
| T07 | S4 | POS | PASS | 2 | 2 | PASS |
| T08 | S4 | DEL | PASS | 5 | 3 | PASS |
| T09 | S5 | POS | PASS | 2 | 2 | PASS |
| T10 | S5 | DEL | PASS | 4 | 4 | PASS |
| T11 | S6 | POS | PASS | 2 | 2 | PASS |
| T12 | S6 | DEL | PASS | 4 | 3 | PASS |
| T13 | S7 | POS | PASS | 2 | 2 | PASS |
| T14 | S7 | DEL | PASS | 4 | 3 | PASS |
| T15 | S8 | POS | PASS | 2 | 2 | PASS |
| T16 | S8 | DEL | PASS | 5 | 3 | PASS |

*B2 native = non-blind experimenter supplementary rating (evidence/b2_native_supplementary.md), NOT bar evidence. Second blind LLM judge unevaluated (APIs hard-down); two-judge bar not met.
Positive control T17: sol=5 (bar >=4.0 single-judge; second judge pending API recovery)
