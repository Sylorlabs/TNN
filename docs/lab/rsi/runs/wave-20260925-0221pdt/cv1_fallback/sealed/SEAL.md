# Seal record: CV-1 fallback and fail-closed sealed probe set, wave-20260925-0221pdt

Sealed: 2026-09-25, after PREREG_CV1_FALLBACK_0221.md froze and before
scoring. Intended commit order: prereg commit strictly before this seal
commit strictly before the scoring commit (the coordinator commits; the
worker wrote the files in this order).

- PROBES.md sha256:
  56fbc9b821f24be9ce6b144d57692e9f57a125073639fe0267f5c2e8b0d86b9b
- KEY.md sha256:
  77716c0fa1acecd725b40f9d821ca884ff618be224ed1b52e77c90aa2447416c

Author attestation: the probe author (Worker 4, author role) wrote the
24 probes and the key from the frozen authoring spec G1 through G6, the
frozen KB, and the frozen gazetteer list only, after the prereg freeze,
and did not modify the implementation. The implementation is
byte-inherited from the committed wave-20260924-1721pdt sources
(cv1c.zag sha256
6d8fb9f013ef3efa1bb44881f98cbeafcabd7110ae4fb7396a3e5721b34d7137;
rebuilt binary verified byte-identical to the adopted binary, sha256
710d8bc5f9d00c1b4cb63ed6f90e69a80982a682b0d1c9d5ab9a27c1e68c3e8e).
The author knows only the public reachability condition (G1); no router
internals beyond it. Separation is self-attested (single worker
session), disclosed per the 1721pdt addendum (c) convention.

G1 through G6 compliance checklist (mechanical, at authoring time):
- 24/24 probe lines carry "?" (grep; zero lines lacking it).
- 0 probe lines contain any frozen assertion-pattern substring
  (case-insensitive grep over the seven substrings; one draft probe
  caught with " meters tall" and reworded before sealing).
- 0 probe lines contain any G1 trigger (composition/resume/correction;
  case-insensitive grep).
- Class A (A01-A08): every content word verified KB-covered by
  case-insensitive whole-word grep; per-probe mechanical coverage check
  (awk over the frozen KB) confirms 0 uncovered words and 0 covering
  facts for all 8 probes.
- Class B1 (B01-B04): zero content words after F7 stopword removal
  (mechanical check), all four probes.
- Class B2 (C01-C08): at least one uncovered word per probe (8 to 10
  uncovered each); all 21 payload words verified KB-absent
  (case-insensitive whole-word grep); all must-not-name words
  (degrees, discovered, new, big, ben, 96, meters) verified KB-present.
- Class D (D01-D04): covering-fact sets exactly the cited facts
  (33, 35, 15, 26), verified mechanically; disjoint from the 1721pdt
  sealed paraphrase facts and the draft control.
- Pre-freeze draft reachability probes (8 unsealed scratch probes in
  /tmp, disjoint in text from the sealed set) validated that
  composition-shaped, degenerate, adversarial, and in-KB probe shapes
  reach the mechanism and hit the fallback, guard, specific-decline,
  and answer paths respectively. No sealed probe byte touched any
  binary before this seal.

Static contamination check (at seal time): grep over the candidate
source (cv1c.zag), KB, gazetteer, build scripts, and scorer finds zero
sealed probe bytes (the sealed probe texts were authored after the
sources were frozen and never executed before scoring).

## Seal-open log

Seal opened for scoring 2026-09-25 (after the seal commit): PROBES.md
and KEY.md shas re-verified against the pins above at scoring time
(both match); the implementation sources remain sha256-identical to
the 1721pdt committed blobs; the scoring binary is the byte-identical
rebuild. Filled at scoring time in the scoring commit, not
retroactively.
