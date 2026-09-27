# BUILD5 — v8 construction log (2026-09-27)

## Phase A: mechanism probes (NOT in v8; excluded per PREREG5 §6 disclosure)
A1–A4, B1–B2, C1–C4 ran all modes during rule discovery. Established: V4 denial target rule (rel, dep), bid22 shield, duel pre-emption, margin gate. None of these queries appear in v8.

## v8 draft (20 items)
Drafted from §4 design rules. Single-mode structural validation only.

### HELP (E01–E04)
All four accepted first-try: readings {0,2}, inter(challenge)=4 > inter(correction)=2, bid22 grd=0 in correction fact, margin=9.
- E02 original (`...capital of france...eiffel tower...`) dragged fid11 (3rd fact). Replaced with `no, i meant moby dick; really, herman melville is greater? herman melville is finer?` → clean 2-fact, margin=9. Original discarded.

### HARM (E05–E08)
All four accepted first-try: readings {2,6}, inter tied at 2, bid22 grd=2 in challenge fact, margin=12. E07 has fid11 drag (inter=1) — harmless (denied first, outcome unchanged).

### DUEL-PREEMPT (E09–E12)
All four accepted first-try: readings {2,6}, forget target spaced, margin=10.

### INERT-MARGIN (E13–E16)
All four accepted first-try: readings {0,7}/{6,7}, margins 18/21/18/21.

### NEAR-MARGIN (E17–E20)
Required margin spread. Tested 19 candidates (single-mode only):
- N1 (12), N2 (11) ✓, N3 (12), N4 (12), N5 (12), N6 (12), N7 (12), N8 (13) ✓
- M1 (11, degenerate: forget target had no keywords), M2 (12), M3 (14) ✓, M4 (12), M5 (11), M6 (11)
- P1 (12) ✓, P2 (12), P3 (12), P4 (13), P5 (12)
- Selected: E17=N2 (11), E18=P1 (12), E19=N8 (13), E20=M3 (14). Discarded the rest.

## Freeze
v8.tsv SHA-256: 9b8c80b7af5a8f55e4e6252c011c96280d824ddae36415c4a990ae2e76cecb88
FREEZE5.txt: 2026-09-27T23:23:45Z. PREDICTIONS5.md written before freeze.

## Red team (rt.tsv, 7 items)
R1a–c: forget+correction (help-seeking). R2a–b: correction+challenge with inter(correction)>inter(challenge) (outcome-irrelevance). R3a: 3-reading (preemption-break); R3b: duel-preempt control.
Predictions in redteam/predictions_rt.md (R1 prediction updated for the forget+correction design before running).
