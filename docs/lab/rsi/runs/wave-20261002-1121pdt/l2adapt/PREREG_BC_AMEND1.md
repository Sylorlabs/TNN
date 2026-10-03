# PREREG AMENDMENT: candidates B and C (battery length fix)

Date: 2026-10-02. Amends PREREG_BC.md (frozen 770a72afd).

## Flaw discovered during implementation

The PREREG_BC battery specified 3-link (B) and 2-link (C) target walks.
Probe experiments show the ev_query fallback (mp_run/trial) can walk
fact chains up to 4 links without any MAP:
- 3 links: ans=304 (fallback succeeds)
- 4 links: ans=705 (fallback succeeds)
- 5 links: ans=-2 (fallback fails)
- 7 links: ans=-2 (fallback fails)

Consequence: XB-FRESH and XB-ABL (3-link B chain) answered 304 via the
fallback, not via SUBSTITUTE; IC-ABL (2-link goal) answered 54 via the
fallback. The kill bars KB3, KB4, KC4 cannot be met because the battery
does not isolate the adaptation operators. The prereg battery is invalid
as specified.

## Amendment (transparent, re-frozen before implementation)

The hypothesis, operators, variant codes, kill bar structure, and cost
bounds are UNCHANGED. Only the battery chain lengths increase to defeat
the fallback (5+ links required):

### B arms (amended)
- Train XA: (11,1,12),(12,1,13),(13,1,14),(14,1,15),(15,1,16);
  ev_query(11,71,16). MAP_XA relseq [1,1,1,1,1] (5 links).
- Domain B facts: (301,3,302),(302,3,303),(303,3,304),(304,3,305),
  (305,3,306). (5 links, 301->306)
- XB-TREAT: query (301,70,306). Expect 306 via SUBSTITUTE 1->3.
- XB-NOADAPT: adapt_on=0. Expect -2.
- XB-FRESH: no XA, only B facts (5 links). Expect -2 (fallback fails).
- XB-ABL: train XA then kill. Expect -2.
- B-L1REG: unchanged (101,70,107) expect 107.

Kill bars KB1-KB7 unchanged except KB1 expects 306 (not 304).

### C arms (amended)
- Train W: (51,1,52),(52,1,53),(53,1,54),(54,2,55),(55,2,56),(56,2,57),
  (57,2,58); ev_query(51,75,58). MAP_W relseq [1,1,1,2,2,2,2] (7 links).
- IC-TREAT: query (52,70,57). Expect 57 via SUBSEQ [1..5]=[1,1,2,2,2]
  (5 links: 52->53->54->55->56->57). Fallback cannot walk 5 links.
- IC-NOADAPT: adapt_on=0. Expect -2.
- IC-FRESH: no W. Expect -2.
- IC-ABL: train W then kill. Expect -2.

Kill bars KC1-KC6 unchanged except KC1 expects 57 (not 54).

## Rationale

The amendment preserves the scientific content (cross-domain substitution,
interface sub-sequence adaptation) while ensuring the battery actually
tests the operators. A 5-link minimum guarantees the fallback cannot
succeed, so any PASS must come from the adaptation machinery. This is a
battery-strengthening amendment, not a hypothesis change.

No kill bar was weakened. The expected answers changed only because the
chain lengths changed (306 is the 5-link target, 57 is the 5-link
sub-interval target).
