# ERROR_INVENTORY.md — grok-4.6 English championship source

corpus: `corpus/corpus.json` (model=grok-4.6, temperature=0, seed=42)
dump rows: 240, teach rows: 240
retries: [] (mechanical parse failures only, max 2)

Trainer-supplied claim = facts.json `value` (authoritative for the learner).
True value = ground_truth_notes.md (== supplied for the 228 non-false ids).

## Counts
- E_dump (dump value != supplied): n=7 ids=[88, 89, 90, 91, 92, 93, 94]
- E_obs (obs_value != supplied): n=0 ids=[]
- E_prb (probe_value != supplied): n=0 ids=[]
- inconsistent (obs_value != probe_value): n=0 ids=[]
- distract_value != obs_value: n=240
- E_format (withheld rows, withhold ruling 2026-09-21): n=0 ids=[]

## Integer/text agreement (value appears as a token in its text)
- dump sentence: 240/240 live rows agree; disagree ids=[]
- observation: 240/240 live rows agree; disagree ids=[]
- distractor: 240/240 live rows agree; disagree ids=[]

## The 12 false ids: per-field status
(supplied(false) = reproduced the trainer's false claim; true(corrected) = emitted the true value; other = neither)
- id 3 [alpha-pos] supplied=5 true=4: dump=supplied(false) obs=supplied(false) dis=true(corrected) prb=supplied(false)
- id 29 [alpha-pos] supplied=6 true=4: dump=supplied(false) obs=supplied(false) dis=true(corrected) prb=supplied(false)
- id 55 [word-len] supplied=7 true=8: dump=supplied(false) obs=supplied(false) dis=true(corrected) prb=supplied(false)
- id 71 [word-len] supplied=21 true=20: dump=supplied(false) obs=supplied(false) dis=other(22) prb=supplied(false)
- id 80 [word-len] supplied=8 true=9: dump=supplied(false) obs=supplied(false) dis=true(corrected) prb=supplied(false)
- id 103 [pub-year] supplied=1688 true=1678: dump=supplied(false) obs=supplied(false) dis=true(corrected) prb=supplied(false)
- id 117 [pub-year] supplied=1851 true=1850: dump=supplied(false) obs=supplied(false) dis=true(corrected) prb=supplied(false)
- id 139 [pub-year] supplied=1896 true=1895: dump=supplied(false) obs=supplied(false) dis=true(corrected) prb=supplied(false)
- id 163 [count-fact] supplied=4 true=3: dump=supplied(false) obs=supplied(false) dis=true(corrected) prb=supplied(false)
- id 178 [count-fact] supplied=10 true=9: dump=supplied(false) obs=supplied(false) dis=true(corrected) prb=supplied(false)
- id 205 [count-fact] supplied=38 true=37: dump=supplied(false) obs=supplied(false) dis=true(corrected) prb=supplied(false)
- id 231 [count-fact] supplied=7 true=8: dump=supplied(false) obs=supplied(false) dis=true(corrected) prb=supplied(false)

## Detail: E_obs ids (obs_value vs supplied vs true)

## Detail: E_prb ids

## Detail: inconsistent ids (obs vs probe)
