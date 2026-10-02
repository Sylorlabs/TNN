# PREREG AMENDMENT 1 (pre-implementation, committed before any code)

## Correction to predicted try counts

Trace-through of the H1 `solve_z` logic (unmodified from xt.zag)
against the designed distractors reveals corrected try counts.
The mechanism logic and all kill-bar intents are unchanged.

### Distractor D2 design (clarified)

D2 = identity, taught on (1->1), (2->2). Signature 1->1.
(X: 1->2, Y: 2->2, D1: 1->2, D2: 1->1.)

### H1 TREAT trace for (1, 93) -> 17, kin = 1, kout = 2

Singles (sig_in == 1 and sig_out == 2):
- m0 = X: X(1) = 16 != 17. Try 1.
- m1 = Y: sig_in = 2, skipped.
- m2 = D1: D1(1) = 7 != 17. Try 2.
- m3 = D2: sig_out = 1, skipped.

Pairs (a: sig_in == kin; b: sig_in == sig_out(a), sig_out == kout):
- a = 0 (X, 1->2): b = 0 (X): sig_in = 1 != 2, skip. b = 1 (Y):
  sig_in = 2, sig_out = 2. Try 3: mid = X(1) = 16, r = Y(16) = 17
  == target. SOLVE. Z-COMP z = 4 a = 0 b = 1.

Total: 3 tries (not 4 as originally predicted). D2 is never reached:
as b it is type-incompatible (sig_in = 1 != 2); as a the solver stops
at (X, Y) first.

### H1 NOTYPE trace (type_on = 0)

Singles: X(1) = 16, Y(1) = 2, D1(1) = 7, D2(1) = 1. 4 tries, all wrong.
Pairs in order: (X, X): X(16) = -1 (no r = 71 fact from 16; find_obj
returns -1)... 

Correction: X(16): find_obj(16, 71) scans facts for subject 16, rel
71. No such fact. Returns -1. So (X, X): mid = -1, r = X(-1) = -1.
Not 17. Try 5. (X, Y): mid = 16, r = 17. SOLVE. Try 6.

Total: 6 tries > 3. K3 (contract prunes) holds.

### H1 Z2 trace for (2, 93) -> 9

After TREAT, z = 4 exists (behav 4, comp_a = 0, comp_b = 1,
sig 1->2). kin = probe_kind(2) = 1, kout = probe_kind(9) = 2.

Singles: m0 = X: X(2) = 8 != 9. Try 1. m1 = Y: skipped. m2 = D1:
D1(2) = 5 != 9. Try 2. m3 = D2: skipped. m4 = Z: sig 1->2. Try 3:
Z(2) = Y(X(2)) = Y(8) = 9. SOLVE via Z-SINGLE.

Total: 3 tries <= 4. K4 holds.

### Amended kill bars

- K1 H1-SOLVE: PASS iff Z-COMP z = 4 a = 0 b = 1 and tries = 3.
- K4 H1-REUSE: PASS iff Z2 solves via Z direct with tries = 3.

All other bars unchanged. The substantive predictions (correct
composite, causal ablations, contract pruning, reuse, determinism,
no template, toolchain) are unaffected.
