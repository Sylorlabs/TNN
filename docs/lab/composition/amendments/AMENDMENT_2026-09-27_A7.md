# Amendment 2026-09-27 — A7: D2 build gate — instrument spec required before construction

**Status: APPROVED by Micah, 2026-09-27** (~15:21 PDT; recorded in the
governance bundle `SIGNATURE_SHEET.md`, item 1 fix 7). Enacted 2026-09-27.
The frozen prereg text is left byte-intact; this dated amendment governs.

## What it changes

D1 is specified down to the byte formula; D2 (sim sub-skills) is a paragraph
of intentions — no scenario generator, no scoring rule for action sequences,
no chance arms (what is "identity output" or "apply only the first part" for
a sequence of sim actions?). Building D2 "from the prereg" today would mean
inventing the generator, the scoring, and the baselines on the fly — exactly
the un-preregistered design work the frozen prereg exists to prevent. A D2
battery built without a spec would produce K1–K6 verdicts against bars whose
meaning for action sequences was never defined.

## Frozen text reference

`PREREG.md` (frozen 2026-09-27, commit `6ca9e042110ca`), §2:

> **D2 — sim sub-skills (secondary, reuses TIDELOCK machinery):**
> - S1 forage: efficient mote eating (+30/mote, dormancy respected).
> - S2 ward-build: crystal+crystal→WARD before a storm window.
> - S3 storm-time: shelter during storm windows, forage outside them.
> - Novel scenarios require novel SEQUENCES (e.g., forage-then-ward under a
>   shifted storm schedule the agent never saw). Parts verified mastered in
>   isolation first (same ≥7/8 gate on held-out scenarios).

And §9: "Build order when headroom exists: … (3) D2 sim scenarios …"

## Enacted change

Insert into §9, before the D2 build step:

> **D2 build gate.** The D2 instrument cannot be built from this prereg: it
> specifies no scenario generator, no scoring rule for action sequences, and
> no chance arms. Before any D2 instrument is built, a D2 instrument spec
> must be written and held to the same bar as D1 — specifying: the novel
> scenario generator (deterministic, novelty-verifiable the way §5 does for
> D1); the scoring rule (what counts as a correct novel sequence); the
> chance arms (what NULL and SINGLE-RULE mean for action sequences); the
> P0–P4 phase analogs; and which of the K1–K6 kill bars apply to D2 and how
> they are adjudicated. Writing the spec is a separate build task and is NOT
> part of this amendment — this amendment only imposes the requirement that
> the spec exists and meets the bar before D2 construction begins.

## Evidence

- `pilot/REDTEAM_REPORT.md`, "D2 (sim) gap": "the frozen prereg specifies no
  D2 instrument — no generator, no scoring rule, no chance arms (what is
  NULL/SINGLE-RULE for action sequences?). D2 is currently
  unbuildable-from-prereg; it needs a specified instrument."
- Recommended fix #7: "D2: write the instrument spec before building."

## Effect

- D2 construction is blocked until a D2 instrument spec exists that meets
  the D1 bar (generator, scoring, chance arms, phase analogs, kill-bar
  adjudication).
- The D1 full battery is unaffected and can proceed without D2.
- This amendment does not write the spec and does not approve any spec —
  the spec is its own build task (commissioned alongside this enactment),
  and if it changes frozen bars or design it returns as its own amendment.
