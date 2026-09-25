# Seal record: CV-1 decline-citation re-test probe set, wave-20260924-1721pdt

Sealed: 2026-09-24, after PREREG_CV1_CITE_1721.md froze (commit dad5ef955)
and before any implementation file exists in this wave.

- PROBES.md sha256:
  5b1c378ad1c841d58eb49bc78c62440b473a9dab26231d7145c48ccf9ecc24fc
- KEY.md sha256:
  53076443b2215868ed8bbdc7f3b0990af2ceb386e6617545c5d3cb01d5ed58ef

Author attestation: the probe author wrote the 30 probes and the key from
the amended authoring spec F9, the frozen KB, and the frozen gazetteer
list only, after the prereg freeze, and has not seen any implementation.
The author knows only the public reachability condition (F9.1 through
F9.5); no router internals beyond it.

F9 compliance checklist (mechanical, at authoring time):
- 30/30 probe lines carry "?" (grep; zero lines lacking it).
- 0 probe lines contain any F9.2 assertion-pattern substring or F9.3
  trigger (case-insensitive grep over the seven substrings and the
  composition/resume/correction triggers).
- Every key-listed payload word verified absent from the frozen KB by
  case-insensitive whole-word grep at authoring time (112 distinct
  payload/uncovered words checked against docs/lab/dialogue/kb.txt; the
  per-probe covered/uncovered split was computed mechanically with awk
  over the frozen KB and hand-verified).
- Every must-not-name word verified present in the KB.
- Paraphrase facts 1, 4, 7, 9, 12, 17, 18, 23, 28, 31: each probe's
  covering-fact set is exactly its target fact (lowest-index coverage
  verified mechanically); the set is disjoint from the 1121pdt sealed
  paraphrase facts (0, 5, 10, 14, 19, 20, 26, 33, 35, 37) and the 1421pdt
  sealed paraphrase facts (3, 6, 11, 16, 21, 25, 27, 29, 34, 36).
- Adversarial: 4 max-overlap tie-break traps (A01-A04, each with the
  old-rule covered-word naming documented in KEY.md), 2 inflected-form
  variants (A05, A06); every decline probe has at least one globally
  uncovered word.
- Gaming: every payload buried after at least 3 wrapper content words;
  classes cover instruction override (G01, G06, G10), leading false
  premise (G02, G07, G09), false authority (G03), roleplay jailbreak
  (G04), flattery plus false premise (G05, G08).

Role separation: probe author and implementer are separate roles in this
worker's workflow. The implementer attests it did not open, read, or list
sealed/ during implementation; the implementation is a byte-copy of the
1421pdt committed sources with no probe-informed changes (no changes at
all).

## Seal-open log

(Left blank at seal time. To be filled ONLY at scoring time, with the
scoring commit hash and the re-verified shas. Retroactive fill is a
process defect.)
