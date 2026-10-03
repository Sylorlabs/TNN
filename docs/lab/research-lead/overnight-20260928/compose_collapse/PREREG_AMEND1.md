# PREREG AMENDMENT 1 (transparent): P3 Y-teaching fact geometry

Date: 2026-10-02. Status of battery: H1 arm run 1 complete; P1/P2a/P2b match
frozen predictions; P3 run exposed the inconsistency below. No kill bar is
changed; all K1-K8 predictions stand as written.

## The inconsistency

PREREG.md Section 5 (P3) lists Y-teaching facts
(50,82,51),(51,82,52),(52,82,53) and (60,82,61),(61,82,62),(62,82,63),(63,82,64)
(chain geometry, transcribed from the canonical H2 world) while simultaneously
stating the frozen teaching expectations "Y 50->3, 60->4 (1->2)".

Under this battery's count semantics (count_rel counts same-subject facts, the
canonical H1 "count targets of node N" semantics that the sealed Z relies on:
(34,82,35),(34,82,36) -> 2), the listed chain facts yield count_rel(50,82)=1
and count_rel(60,82)=1, so teach() records NO observations for Y (nobs=0,
verified by census dump). The fact list contradicts the prereg's own stated
teaching expectations. The world as listed cannot produce the frozen K4
predictions, which were computed from the intended world (Y sig NODE->NUM).

## The fix (facts only; expectations, bars, predictions unchanged)

Replace the P3 Y-teaching facts with star geometry, matching the canonical H1
world ("count targets of node N" as same-subject stars) and the prereg's stated
expectations:

- (50,82,51),(50,82,52),(50,82,53)
- (60,82,61),(60,82,62),(60,82,63),(60,82,64)

With these, teach(A,1,50,3) and teach(A,1,60,4) succeed, Y records n=2
observations (in NODE, out NUM), sig(Y)=NODE->NUM, exactly as the frozen
prereg states. No other problem, arm, kill bar, or predicted number is
affected (verified: P1/P2a/P2b/P5 worlds and all arm logic are untouched).

## Governance

This amendment is recorded BEFORE the corrected implementation runs. The
original P3 H1 run (with the inconsistent world) is discarded as a
world-construction error, not a mechanism result; it is reported here, not
hidden. The frozen hypothesis (Section 3), the operational collapse definition
(Section 4), and kill bars K1-K8 are unchanged. No bar is weakened.
