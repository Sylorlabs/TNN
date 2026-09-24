# Fork C Driver Addendum (Retrospective)

**Status:** RETROSPECTIVE — committed after blind execution. This discloses a
process deviation.

**Deviation:** The attack prereg requires fork-specific driver addenda to be
committed BEFORE blind execution. The C addendum was NOT committed before
C's blind runs. This is a sequencing violation. It is disclosed here
retrospectively rather than concealed or backdated.

**Adapter actually used:** `~/workspace/selfpam_r2/attacks/adapt_c.py`

**Summary of adapter:**
- Reads frozen battery TSVs (CONF, GOLD, ALIBI, RECUR, SMUGGLE, CALIB, UTYPE,
  POINTER, pairs_flip, pairs_sm).
- Emits C fixtures in C's manifest format (1,024-line cap, split by metric).
- M1: CONF (catch) + GOLD (accept). M2: FLIP pairs (diverge). M3: SM pairs
  (stable, expected value `SAME`). M4: ALIBI (reject). M5: RECUR (reject).
  M6: GOLD (accept).
- Extensions: SMUGGLE, CALIB, UTYPE, POINTER as CONFAB.

**Determinism:** All M1–M6 outputs byte-identical ×2. Zero RNG.

**Date:** 2026-09-24
