# PREREG_AMENDMENT2: FULL A_SEARCH hand-derivation correction

Date: 2026-10-02. Status: FROZEN. This amendment is written after
the first build but BEFORE any verdict is drawn; it corrects an
arithmetic slip in PREREG.md section 4's hand derivation, not a
kill-bar threshold. The 5x ratio threshold in K2a/K3 is unchanged.

Slip: section 4 derives FULL A_SEARCH=9 by counting a MAP2/d
header examination in the piece search. The frozen counting rules
(section 3) and the frozen first-match rule (section 2: "First
match wins (node-id order, no researcher selection)") together
give A_SEARCH=8: stale-detect ascan MAP0 (1), piece search
MAP0 self-skip (2), MAP1 header (3), MAP1 fact-3 live-check (4),
MAP1 fact-4 live-check (5) then MATCH, dedup ascan MAP0/1/2
(6,7,8). MAP2 is never examined because the search stops at the
first MATCH, exactly as the frozen rule requires. The
implementation follows the frozen rules; the hand derivation
double-counted.

Corrected frozen numbers: FULL A_SEARCH=8, A_EXEC=3.
K2a product: 5*A_SEARCH(FULL)=40 (measured ABLATE-N 76 >= 40).
K3 product: 5*A_SEARCH(FULL)=40 (measured FRESH 72 >= 40).
All other frozen numbers, kill bars K1-K10, and falsifiers stand
unchanged.
