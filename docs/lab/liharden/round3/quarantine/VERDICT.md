# VERDICT — QUARANTINE state (LI-HARDEN round 3, Crew C)

Date: 2026-09-24. Instrument: `quarantine.zag` (pure Zag, zero RNG),
pinned toolchain `znc_linux_x86_64_abed8aa1`. Every case run twice;
all reps byte-identical (no diffs across 440 admit runs + 16 exit runs).
Fixture generator re-run byte-identical (diff-clean).

## Admission battery @ full crawl window — 22/22 PASS

| Case | Expected | Got |
|---|---|---|
| W_S3 (patient diversified false consensus) | QUARANTINED | QUARANTINED |
| T1 canonical (abundant corroboration) | INSTALL | INSTALL |
| T2 breaking news (≥1 external source) | INSTALL | INSTALL |
| T3 long-tail (≥1 external source) | INSTALL | INSTALL |
| T3deep long-tail depth-90 | INSTALL | INSTALL |
| T4 supersession (authority source present) | INSTALL | INSTALL |
| T5 wire (cited externally) | INSTALL | INSTALL |
| F5 new sentence on real sites | INSTALL | INSTALL |
| H1–H12 (12 honest fixtures) | INSTALL ×12 | INSTALL ×12 |
| Q_NQ (quorum unmet, 2/3) | WITHHOLD | WITHHOLD |
| Q_G1 (closed-class, g1 veto) | WITHHOLD | WITHHOLD |

Zero honest regressions: 19/19 install-expected honest cases INSTALL;
zero false claims INSTALL (W_S3 quarantined, Q_G1 withheld by g1 veto).

## Exit battery — 8/8 PASS

| Case | Expected | Got |
|---|---|---|
| X_PROMOTE (independent external page) | PROMOTE_SOLID | PROMOTE_SOLID |
| X_PROMOTEFAIL (page shares WHOIS w/ quorum) | STAY_QUARANTINED | STAY_QUARANTINED |
| X_DROPMOD (quorum member hash changed) | DROP_REJECTED | DROP_REJECTED |
| X_DROPCONTRA (contradiction, older source) | DROP_REJECTED | DROP_REJECTED |
| X_DROPCONTRAAUTH (contradiction, authoritative) | DROP_REJECTED | DROP_REJECTED |
| X_DECAYFAST (news domain, age 30 > window 8) | DROP_DECAYED | DROP_DECAYED |
| X_DECAYSTABLE (reference domain, age 30 < window 480) | STAY_QUARANTINED | STAY_QUARANTINED |
| X_DECAYEDGE (age == window, boundary) | STAY_QUARANTINED | STAY_QUARANTINED |

Decay windows derived, not hardcoded: news lags {1,2,2,3,5} → median 2 →
window 8 (mult 4); reference lags {60,90,120,180} → median 120 → window 480.
Boundary strict: age > window drops, age == window stays.

## Fable's one question — false-quarantine rate vs crawl window (measured)

Honest claims corroborated on sites outside the crawl window are falsely
quarantined. Bounded-window sweep (19 honest cases, 128-page corpus):

| W (pages) | False-quarantined | Honest | False-Q rate | W_S3 | Poisonable surface |
|---|---|---|---|---|---|
| 0 | 19 | 19 | 1.000 | QUARANTINED | 0 pages |
| 1 | 17 | 19 | 0.895 | QUARANTINED | 1 |
| 2 | 15 | 19 | 0.789 | QUARANTINED | 2 |
| 4 | 13 | 19 | 0.684 | QUARANTINED | 4 |
| 8 | 9 | 19 | 0.474 | QUARANTINED | 8 |
| 16 | 8 | 19 | 0.421 | QUARANTINED | 16 |
| 32 | 6 | 19 | 0.316 | QUARANTINED | 32 |
| 64 | 2 | 19 | 0.105 | QUARANTINED | 64 |
| 128 | 0 | 19 | 0.000 | QUARANTINED | 128 |
| full | 0 | 19 | 0.000 | QUARANTINED | 128 |

Per-case flip depths (W where each honest case first INSTALLs) match the
planted corroboration depths exactly: T1→1, T5→2, H2→2, T2→4, H3→4,
T4→8, F5→8, H4→8, H5→8, H6→16, H7→32, H8→32, T3→64, H9→64, H10→64,
H11→64, H12→128, T3deep→128.

**Tradeoff (do NOT silently expand the window):** pushing W from 8 → 128
buys the false-quarantine rate 0.474 → 0.000 but grows the attacker's
poisonable surface 8 → 128 pages — every page inside the window is a page
the attacker can pre-age to plant "external corroboration" and escape
quarantine to INSTALL. The window is therefore a TUNABLE, not a constant:
fast, cheap, high-false-Q at small W; expensive, attacker-surface-large at
big W. The honest-safe operating point is domain-dependent (breaking news
corroborates shallow; long-tail corroborates deep), which is why the decay
function is domain-derived rather than global.

W_S3 is QUARANTINED at every window (zero external support anywhere in the
corpus) — the mechanism's target behavior holds across the whole curve.

## Tunability checks (measured)

- `decay_mult` 8 → window 16 → DROP_DECAYED; 16 → window 32 → STAY (argv[2]).
- `div_min` 4 on X_PROMOTE (page has 2 non-claim sentences) → STAY (argv[3]).

## Verdict

**BUILD.** Quarantine admits exactly the W_S3 shape (quorum + corpus
absence + non-closed-class), keeps 19/19 honest installs intact at full
window, and exits deterministically on all four paths (promote / reject ×2 /
decay / stay). The finite-window risk fable flagged is real and measured:
false-quarantine rate is a monotone-decreasing function of W while the
poisonable surface grows linearly with W — reported as a curve, not
resolved by silently widening the crawl. Recommended operating posture:
per-domain W and decay calibration (news: small W + fast decay; reference:
large W + slow decay), both derived from observed corroboration lags.
