# R2-9 human-verdict package — WITHHELD (fork DEAD on B5)

**Status: NOT DELIVERED to Micah. Fork R2-9 died on B5 (false permanent installs 719/10,000 = 7.19% > 3% kill threshold) on the full 10,000-trial battery, 2026-09-23.**

Per the frozen prereg §5(7): a human verdict cannot rescue a mechanical-bar failure. The mechanical battery is decisive; this package was assembled by the earlier crew before the battery completed and is superseded. Parent may route nothing from it.

## Artifact labels (KB-E3/KB-E4, had the fork lived)

- All 151 visual trial artifacts (trials/J000..J150): **NEW** — none were shown to Micah. The package was assembled 2026-09-23 and never routed (prior verdict: "awaiting parent routing").
- The 49 audio trials (pitchdisc/timbredisc): **NOT INCLUDED** — gate-blocked (audio_gate_blocked.tsv). The frozen protocol requires a full waveform gate calibrated against real field recordings; only a partial gate exists.
- No artifacts are **PREVIOUSLY SHOWN** or **REFERENCE** (no Micah verdicts were ever collected on this fork).

## Package contents (as assembled by the earlier crew, unchanged)

- `manifest.tsv` — 151 visual trials in randomized double-blind order (J000..J150), mapped to human_sample_manifest sample indices
- `brief.md` — judge brief (note: its KB-E4 wording ("beauty") is the earlier crew's phrasing; the frozen prereg defines KB-E4 as spoof-catch)
- `trials/J###/` — source + emission + claim.txt per trial
- `audio_gate_blocked.tsv` — 49 audio trials blocked from the package
