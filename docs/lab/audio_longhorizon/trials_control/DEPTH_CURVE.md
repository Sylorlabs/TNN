# DEPTH_CURVE — Phase B2b (persistent session depths)

Hit rate by 10-target depth band (r1, frozen scorer).

## Pitch (depths 1–40)

| Band   | Hits | Rate |
|--------|------|------|
| 1–10   | 4/10 | 0.40 |
| 11–20  | 9/10 | 0.90 |
| 21–30  | 9/10 | 0.90 |
| 31–40  | 6/10 | 0.60 |

## Envelope (depths 41–80)

| Band   | Hits | Rate |
|--------|------|------|
| 41–50  | 10/10| 1.00 |
| 51–60  | 10/10| 1.00 |
| 61–70  | 9/10 | 0.90 |
| 71–80  | 10/10| 1.00 |

## Prosody (depths 81–120) — scorer VOID (ANOM-009)

| Band    | Hits | Rate |
|---------|------|------|
| 81–90   | 6/10 | 0.60 |
| 91–100  | 8/10 | 0.80 |
| 101–110 | 9/10 | 0.90 |
| 111–120 | 6/10 | 0.60 |

## Paired repeats (pitch): early vs deep

| Set              | Hits  | Rate | 
|------------------|-------|------|
| Early (1–20)     | 13/20 | 0.65 |
| Deep (141–160)   | 15/20 | 0.75 |
| Drift            |       | +10.0 pp |

**No DRIFT-FAIL**: deep repeats IMPROVED by 10pp over early (bar is drop >5pp).
The persistent history (recalled deltas) benefits repeated targets — the
controller learns from experience within the session.

## Design notes

- Single continuous session per run (r1/r3): depths 1–160, one target per
  depth, 16-entry history ring (consult seeds F0 delta from same-ref history).
- Depth bands confounded by axis — reported as-is, not as a pure depth effect.
- r2 incomplete (159/160, VM reboot); r1≡r3 byte-identical proven.
