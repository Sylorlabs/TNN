# Amendment 2026-09-27 — A6: Align pilot P0 with prereg (full battery uses frozen numbers)

**Status: APPROVED by Micah, 2026-09-27** (~15:21 PDT; recorded in the
governance bundle `SIGNATURE_SHEET.md`, item 1 fix 6). Enacted 2026-09-27.
The frozen prereg text is left byte-intact; this dated amendment governs.

## What it changes

The pilot ran P0 as 6 probes per part at ≥5/6 over tok 6–11; the frozen
prereg specifies 8 probes at ≥7/8 over tok 6–13. The pilot's version was
fine for validating the instrument and was documented openly — but it is a
weaker gate (one lucky guess carries further), and the full battery must not
inherit it by accident. The gate's whole job — especially after A2 closes
the Caesar-shift hole — is to certify that parts were genuinely learned.

## Frozen text reference

`PREREG.md` (frozen 2026-09-27, commit `6ca9e042110ca`), §3 P0:

> - **P0 — mastery gate:** 8 held-out probes per part. <7/8 → part excluded,
>   items needing it classified (a).

And §4: "disjoint index ranges per phase (train 0–5, **P0 6–13**, P2 14–61,
P3 62–69)."

## Enacted change

Add to §9 (Full-battery execution):

> The pilot's P0 implementation (6 probes per part at ≥5/6, tok 6–11) is a
> documented pilot-only deviation. The full battery implements the frozen
> §3/§4 numbers: 8 held-out probes per part at ≥7/8, tok 6–13.

No bar, threshold, or design change — this locks in the frozen numbers for
the full battery and closes the documented deviation. The pilot report stands
as written.

## Evidence

- `pilot/PILOT_REPORT.md`: "the pilot implements P0 as 6 probes at ≥5/6 over
  tok 6–11; the frozen prereg specifies 8 probes at ≥7/8 over tok 6–13. The
  full battery implements the prereg's numbers."
- `pilot/REDTEAM_REPORT.md`, final section: "P0 implements 6 probes at ≥5/6
  over tok 6–11; the frozen prereg requires 8 probes at ≥7/8 over tok 6–13
  (§2, §3, §4)."

## Effect

- The full battery builds P0 as 8 probes per part, ≥7/8 to pass, over tok
  6–13 — exactly the frozen spec. Nothing else changes.
