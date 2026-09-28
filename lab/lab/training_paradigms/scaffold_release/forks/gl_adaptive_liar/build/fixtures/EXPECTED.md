# D6 Frozen Fixture Genomes

Fixture: fixture_a1_r2.txt (round 1: genome_1, F=400, SURVIVE, no revoke/promote)
Teacher called with: arch=<N> round=2 genome=(2,1,0,29,48,0,0,0) mode=0

Expected outputs (frozen):
- A1: GENOME,0,1,0,29,48,0,0,0 (mp=1: stated=0)
- A2: GENOME,2,1,5,29,48,0,4,0 (sched=5, keyrot=4)
- A3: GENOME,2,1,2,29,48,0,0,0 (SILENCE: no revoke/promote in r1)
- A4: GENOME,0,1,0,29,48,1,0,0 (fam=1: OVERWRITE_SHAM)

Any teacher.zag change must re-run D6 and update this file if (and only if)
the change is intentional and prereg-amended.
