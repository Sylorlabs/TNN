# CREW HOLD NOTICE — LI mode trials

**Date:** 2026-09-23. **Issued by:** LI modes debate coordinator.

## Fork crews: DO NOT EXECUTE until the prereg freeze is committed

The hypotheses prereg for the LI mode trials
(`mode_trials/PREREG_MODES_FROZEN.md`) is written and is being committed to
`sylorlabs/TNN` branch `tnn-native-lab` now, together with:

- `mode_trials/DEBATES_LI_MODES.md` — the full debate record (13 takes)
- `mode_trials/HYPOTHESES_LI_MODES.md` — derived hypotheses with kill bars
- this notice

**Any fork test run (V-SCOUT, V-PARA, V-QUAR, V-PROV, V-QUOTA) started before
the freeze commit lands is VOID per §6 of the prereg.** Do not build variants,
do not run batteries, do not touch `webg.zag`.

**Permitted now:** building the C2 novel-facts fixture (≥200 URLs, novelty
claim per fact with primary-source citations, quantitative/qualitative split
tracked). Fixture building is NOT a fork test.

**How you know the hold is lifted:** this notice is superseded by a
`HOLD_LIFTED.md` in this directory naming the freeze commit SHA, OR the
coordinator (or parent orchestrator) tells you directly with the commit SHA.
Until then, wait.
