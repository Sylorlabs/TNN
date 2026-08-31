# R32 E51M — Calibration Dose × Capacity Curve Result

Date executed: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Status

`INVALID_EXPERIMENT_INTEGRITY_FAILURE — SEED_NAMESPACE EXHAUSTED`

E51M compiled and executed successfully in full native Zag v2, but the preregistered fresh-partition integrity contract failed before any scientific dose/capacity conclusion could be accepted.

## Native authority

- GitHub Actions run: `33343784134`
- source head: `2288224147569a434965353b5873c913df9d8d4c`
- artifact id: `9741423490`
- artifact digest: `sha256:467462a89d22f95b44da95800fdbc10e2e005e2b4d15dae0994e5a6814ee249a`
- assembled native source SHA256: `a2fbcdb694d3c91b56aeb8125ca85963a17bbe666bfed318d0ed0b4aa43cc5e2`
- frozen core SHA256: `6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0`
- native binary SHA256: `b344dbce057360fd2df0c60a4b1817c0e3c75ef553d49c46d126cab6b7cb3bed`
- two native builds byte-identical: PASS
- native exit code: 0
- native experiment runtime: 293 s

## Integrity

Parent E50 integrity passed:

- seed preflight: PASS
- batch statistics: PASS
- forward/reverse batch identity: PASS
- convergence: PASS
- auxiliary frozen-state gate: PASS

E51M learner-side invariants also passed:

- native Zag v2 only: yes
- evaluator truth exposed to learner: no
- ambiguity label exposed: no
- validation membership exposed: no
- UNKNOWN positive target: none
- topology change: none
- graph privilege: none
- base UNKNOWN target nonzero: 0
- base UNKNOWN parameter nonzero: 0
- base terminal fit identity: PASS
- scalar forward/reverse identity: PASS
- hinge forward/reverse identity: PASS

But partition integrity failed:

- requested/emitted partition assignments: 29,160
- seed assignment failures: **2,440**
- overall E51M integrity gate: **FAIL**
- sealed confirmation executed: 0

The failure repeats the finite global substream-state exhaustion seen in the earlier E51C lineage. The old allocator requires one base candidate to simultaneously avoid occupied raw, truth/evidence, history, passive, active, and resource states in a roughly one-million-state namespace. That contract no longer scales to the required developmental dose.

## Non-authoritative diagnostic output

The program completed the grid after the seed gate failed. Those rows are retained only for debugging and MUST NOT be used as scientific evidence, model selection, or a basis for promotion. In particular, printed `dose_signal=1` and `capacity_signal=1` are non-authoritative because 2,440 requested worlds were assigned invalid fallback seeds.

For traceability, the invalid-run base reachability was 4,199 / 4,200 known and 1,124 / 1,200 no-unique UNKNOWN. The best printed no-unique number was 1,162 / 1,200, but it is not a valid validation result.

## Causal diagnosis

This is evaluator infrastructure exhaustion, not evidence for or against TNN's scalar calibration architecture. E51M does not justify a topology change, a graph mechanism, more learner features, or a larger cognitive model.

The next binding experiment is an evaluator-only seed/world-domain repair that:

1. preserves the same learner-visible state and grounded utility semantics;
2. gives truth/history/passive/active/resource randomness independent domain identities rather than treating all substream RNG states as one globally shared namespace;
3. uses a much larger deterministic world identity space;
4. proves zero duplicate world identities and zero train/validation/confirmation overlap;
5. keeps all seed/domain/stage identifiers evaluator-only;
6. reruns the exact E51M dose × capacity contract only after that integrity layer passes.

No E51M result promotes R32 or establishes AGI.
