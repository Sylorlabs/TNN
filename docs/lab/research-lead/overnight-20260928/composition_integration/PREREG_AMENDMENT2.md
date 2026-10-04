# PREREG AMENDMENT 2: training relation fix

Status: FROZEN 2026-10-02. Committed before the redesigned
implementation is run.

Amendment 1 specified training as ev_teach(11,70,12),(12,70,13),
(13,70,14) then ev_query_adapt(W,11,70,14,0). Probe revealed this
is broken: activate(11,70) shortcut-fires on the training fact
(11,70,12) itself, returning 12 without ever trialing, so MAP_X is
never promoted.

Corrected training (frozen): ev_teach(11,70,12),(12,70,13),
(13,70,14), then ev_query_adapt(W,11,71,14,0). The query relation
(71) differs from the fact relation (70), so no shortcut fires and
the trial promotes MAP_X with relseq [70,70,70] (field 4 = 71).

Consequences for the Amendment 1 derivations:
- The training FACT is (11,71,14), not (11,70,14). In I2/I6
  specialize scans it appears as an r=71 != 70 alternative at j=0,
  creating an inert 1-link [71] MAP (terminal 14). It never
  terminates the DFS (wrong terminal) and is never selected.
- lv_predict's MAP-execute fallback (field 4 == query r) does not
  fire for MAP_X (71 != 70/72/74). I4 withholds with nobasis as
  preregistered.
- All other Amendment 1 derivations stand unchanged.
