# A3/A4 Gating Decision

**Date:** 2026-09-24
**Prereg:** PREREG_H2_REVIVAL.md §3

## A3 (Window-Prober)

**Gate required:** Traced six-round run showing silence search changing schedule,
resulting provisional not under A1, ≥1 episode disagrees between A3 and A1.

**Status:** DROPPED — gate not attempted.

**Rationale:** The six required arms (H-TW, A8, A9, A6, REV-ALIAS, A2-WIN) consumed
the available battery time. A3's state-machine teacher (arch=3) requires interactive
stdin and a six-round traced comparison against A1; this was not completed.

Per prereg §3: "If no live trace is produced, A3 is dropped from the battery."

## A4 (Generality Prober)

**Gate required:** Built and traced.

**Status:** DROPPED — not built.

**Rationale:** Same as A3. The arch=4 teacher path exists in teacher.zag but was
not built/traced live.

Per prereg §3: "If not built, A4 is dropped from the battery."

## Impact

The six-arm battery is complete without A3/A4. Their hypotheses (window-probing,
generality) remain untested in this revival.
