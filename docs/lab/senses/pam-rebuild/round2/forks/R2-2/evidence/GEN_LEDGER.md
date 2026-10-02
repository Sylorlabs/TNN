# R2A generator ledger
generator: src/r2gen.py  master_seed=20260923
streams: normal-ext=400+taskidx adversarial=500+taskidx
generated_at: 2026-09-23T08:24:51
wall_time_s: 1051.5

## counts (per frozen family/task tables)
frozen harness files covered: 2020 (hashes match harness MANIFEST.sha256)
generated normal: 5100  (per-task: {'colordisc': 1080, 'colorconst': 720, 'shapetrans': 1296, 'pitchdisc': 720, 'timbredisc': 720, 'motiondir': 564})
generated adversarial: 5815
signature-targeted subset (B5): 1850 ['R2A-COL-1', 'R2A-MOT-1', 'R2A-SHP-1', 'R2A-SHP-2', 'R2A-TMB-2']
novel-collision probes (kill-3): 1090 ['R2A-CCN-2', 'R2A-MOT-2', 'R2A-PTC-2']
TOTAL generated: 10915   TOTAL suite (frozen+generated): 12935

## frozen-spec arithmetic discrepancy (see r2gen.py header)
spec text says 4,260 normal / 4,815 adversarial / 10,000 trials / 2,000-fixture B5 subset;
the spec's own tables sum to 5100 / 5815 / 11840 / 1850. Tables govern; text flagged.

## truth tallies
('R2A-CCN-1', 'DIFFERENT') 170
('R2A-CCN-1', 'SAME_SURFACE') 170
('R2A-CCN-2', 'SAME_SURFACE') 340
('R2A-COL-1', 'DIFFERENT') 400
('R2A-COL-2', 'SAME') 350
('R2A-COL-3', 'DIFFERENT') 400
('R2A-MOT-1', 'E') 44
('R2A-MOT-1', 'N') 44
('R2A-MOT-1', 'NE') 44
('R2A-MOT-1', 'NW') 44
('R2A-MOT-1', 'S') 44
('R2A-MOT-1', 'SE') 44
('R2A-MOT-1', 'SW') 43
('R2A-MOT-1', 'W') 43
('R2A-MOT-2', 'E') 44
('R2A-MOT-2', 'N') 44
('R2A-MOT-2', 'NE') 44
('R2A-MOT-2', 'NW') 44
('R2A-MOT-2', 'S') 44
('R2A-MOT-2', 'SE') 44
('R2A-MOT-2', 'SW') 43
('R2A-MOT-2', 'W') 43
('R2A-MOT-3', 'E') 33
('R2A-MOT-3', 'N') 33
('R2A-MOT-3', 'NE') 33
('R2A-MOT-3', 'NW') 33
('R2A-MOT-3', 'S') 33
('R2A-MOT-3', 'SE') 33
('R2A-MOT-3', 'STILL') 32
('R2A-MOT-3', 'SW') 33
('R2A-MOT-3', 'W') 32
('R2A-PTC-1', 'HIGHER') 102
('R2A-PTC-1', 'LOWER') 113
('R2A-PTC-1', 'SAME') 135
('R2A-PTC-2', 'HIGHER') 134
('R2A-PTC-2', 'LOWER') 133
('R2A-PTC-2', 'SAME') 133
('R2A-PTC-3', 'HIGHER') 133
('R2A-PTC-3', 'LOWER') 133
('R2A-PTC-3', 'SAME') 134
('R2A-SHP-1', 'CIRCLE') 134
('R2A-SHP-1', 'SQUARE') 133
('R2A-SHP-1', 'TRIANGLE') 133
('R2A-SHP-2', 'CIRCLE') 150
('R2A-SHP-2', 'SQUARE') 150
('R2A-SHP-2', 'TRIANGLE') 150
('R2A-SHP-3', 'CIRCLE') 92
('R2A-SHP-3', 'SQUARE') 106
('R2A-SHP-3', 'TRIANGLE') 102
('R2A-TMB-1', 'BRIGHT') 45
('R2A-TMB-1', 'DARK') 73
('R2A-TMB-1', 'PURE') 49
('R2A-TMB-1', 'RICH') 83
('R2A-TMB-2', 'RICH') 250
('R2A-TMB-3', 'BRIGHT') 48
('R2A-TMB-3', 'DARK') 48
('R2A-TMB-3', 'PURE') 47
('R2A-TMB-3', 'RICH') 47
('normal', 'colorconst', 'DIFFERENT') 360
('normal', 'colorconst', 'SAME_SURFACE') 360
('normal', 'colordisc', 'DIFFERENT') 720
('normal', 'colordisc', 'SAME') 360
('normal', 'motiondir', 'E') 66
('normal', 'motiondir', 'N') 66
('normal', 'motiondir', 'NE') 66
('normal', 'motiondir', 'NW') 66
('normal', 'motiondir', 'S') 65
('normal', 'motiondir', 'SE') 65
('normal', 'motiondir', 'STILL') 40
('normal', 'motiondir', 'SW') 65
('normal', 'motiondir', 'W') 65
('normal', 'pitchdisc', 'HIGHER') 240
('normal', 'pitchdisc', 'LOWER') 240
('normal', 'pitchdisc', 'SAME') 240
('normal', 'shapetrans', 'CIRCLE') 432
('normal', 'shapetrans', 'SQUARE') 432
('normal', 'shapetrans', 'TRIANGLE') 432
('normal', 'timbredisc', 'BRIGHT') 180
('normal', 'timbredisc', 'DARK') 180
('normal', 'timbredisc', 'PURE') 180
('normal', 'timbredisc', 'RICH') 180

## count discrepancy (recorded 2026-09-23)
The R2_FIXTURE_SET.md summary says 5,000 normal + 5,000 adversarial and a 2,000-fixture targeted subset. The granular per-family tables sum to 5,100 normal, 5,815 adversarial, 1,850 targeted, 1,090 novel (PTC-2: 400, CCN-2: 340, MOT-2: 350). Granular tables govern; all percentage bars apply to actual denominators.
