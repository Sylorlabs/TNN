# R34 pure-Zag continual learner engineering preregistration

This is a quarantined engineering campaign. It does not grant R27 continuity, learner authority, successor status, or scientific exposure.

The native implementation must show all of the following without Python or an ML framework:

- Task A baseline 64/64 and Task B baseline 0/64 under the fixed neutral tie rule.
- Task A reaches 64/64 after online experience.
- After subsequent Task B training, Task A remains 64/64 and Task B reaches 64/64.
- Exactly 192 enabled online updates occur.
- An update-disabled control remains at zero updates and does not acquire Task B.
- Equal seed + equal experience streams produce exact identical learner state.
- Complete learner state serializes with an integrity digest and decodes exactly.
- A fresh process reload preserves both competencies and update count.
- Corrupt and truncated state are refused.

The environment/evaluator owns the hidden task/action reward mapping. The learner only receives scalar reward after recording the causal pending task/action. The reward rule is not present in learner features.

