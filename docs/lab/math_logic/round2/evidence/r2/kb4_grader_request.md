# Request to Parent: Spawn 3 Independent KB4 Grader Subagents

## Task
Grade 284+ blinded proof-audit trails for circularity and soundness.

## Why parent must spawn
Coordinator is depth 2/2 and cannot spawn children. The three graders must be
independent subagents (not simulated locally) per the frozen protocol.

## Materials
- Blinded packet: `~/workspace/math_r2/eval/kb4_packet.json`
  (will be rebuilt with B5X audits when B5X completes; currently 284 audits)
- Grading instructions are embedded in the packet's "instructions" field.
- Alias key: `~/workspace/math_r2/eval/kb4_key.json` (DO NOT give to graders)

## Grader instructions (for the spawn prompt)
Each grader subagent receives:
1. The packet file path (`kb4_packet.json`)
2. Instruction: "You are an independent grader. Rate each audit 1-5 on circularity, unwarranted steps, and magic knowledge per the embedded instructions. Output JSON. You are blinded: do not attempt to identify the engine. Work independently."

## Output format
Each grader returns a JSON list:
[{"id": "A001", "circularity": 5, "unwarranted": 4, "magic": 5}, ...]

## Coordinator will then
1. Compute Krippendorff's alpha (or pairwise agreement) across the 3 graders.
2. Require alpha > 0.8 or the round fails (per frozen protocol).
3. Unblind and compare mean scores: if ONE's mean is >=1.0 below DUAL's mean, DUAL is falsified as audit-hostile.

## Blinding integrity
- Aliases: Engine A=DUAL-R1, B=NFEE, C=ONE-R1, D=REF-FIRST, E=LEARN-FORM, F=HYB
- Audits stripped of engine names, paths, and identifying strings.
- Graders must not see `kb4_key.json`.
