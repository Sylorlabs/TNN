# VERDICT_CONTLEARN: continuing-learner integration experiment

Wave: wave-20261001-2021pdt. Lane: CONTLEARN. Date: 2026-10-01.
Prereg: PREREG_CONTLEARN.md, frozen alone at commit 2ed8fb7d3.
Implementation: `cl_driver` built from the byte-identical frozen core plus
the fixture driver, one logged znc invocation. No H10/H11 implementation,
no new cognitive machinery, no frozen-core edits.

## Per-bar results

| Bar | Result | Evidence |
|-----|--------|----------|
| K0 commit order | PASS | Prereg committed alone at 2ed8fb7d3 (HEAD at implementation start). All implementation files first appear after that commit. `git merge-base --is-ancestor 2ed8fb7d3 HEAD` true. |
| K1a one learner, one process | PASS | 21 spawns total, exactly 3 per mode; each treatment rep is one process for the whole 149-event run. Transcripts contain no PID (pid_leak_check=0). |
| K1b one build | PASS | `znc_invocations.log` holds exactly 1 entry (the pre-run build); 0 new entries during the 21 runs. |
| K1c audit, no task labels | PASS | AUDIT_PASS on all 21 runs (149/24/24/33/18/80/18 events through the choke point). Empty argv; phase-free env (fully empty env via `bash -c 'exec -c'`; `env` is not linked in safebin). Mode letters and PHASE markers driver-side only. |
| K2a frozen ISA boundary | PASS | SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd` verified before implementation, immediately before the build, and after all runs; `git diff f4de7ff46` on the frozen path empty throughout. |
| K2b driver audit | PASS | 0 cognition functions, 0 new node tags, 0 new edge types, 0 new opcodes, 0 modes/bridges/routers/handlers/semantic cases; switch/match count 0. |
| K2c source delta | PASS | Cognition lines added 0, deleted 0, net 0; all learner-state structures in frozen formats, counted by census. |
| K2d pure Zag | PASS | Zero Python/C/JS/Rust at every stage; `which python3` empty under safebin PATH. |
| K3 cross-phase reuse | PASS | R1C 6 >= 4; R2C 3 >= 2 (with \|T\| = 3); R3C 3 = 3; R4C 12 >= 10; R5C 6 >= 4; REUSE_COUNT 30 >= 20. |
| K4a edge census | PASS | E4 = 33 edges at end of P4; 0 missing at end of run. |
| K4b MAP survival | PASS | 6/6 MAPs alive at end of run. |
| K4c fact retention | PASS | R4C 12 >= 10 (0 of 12 P1 facts lost). |
| K4d diagnosability | PASS | Zero lost facts and zero unanswerable chains, so no diagnoses required; the DIAG path is exercised and working (18 lines in C-P6). |
| K5a control parity | PASS | C-P1 12/12, C-P2 6/6 + R1C 6, C-P3 R2C 3 + probes 6/6, C-P4 3/3, C-P5 40/40; each >= the matching treatment phase score (equality throughout). |
| K5b control reuse is 0 | PASS | C-P6 0/18; 0 tag-20 nodes; every tag-1 node field24 == -999. No harness state leak. |
| K6 determinism | PASS | 3/3 byte-identical transcripts per mode (SHA-256 match); FNV-1a checksums equal; exit 0 on all 21 runs; zero stderr bytes; no PID/timestamps/paths in transcripts. |

## Verdict

**INTEGRATION-DEMONSTRATED.** All of K0 through K6 pass.

The exact frozen claim, per the prereg: on this fixed 149-event sequence
(see the erratum below), the frozen TNN-2 core shows 30 white-box
cross-phase citations (R1C 6, R2C 3, R3C 3, R4C 12, R5C 6), every component
floor met or exceeded, with the per-phase-reset negative control scoring
identically on P1-P5 and 0/18 on the cross-phase probe, and 3/3
byte-identical determinism across 21 runs.

What this verdict does NOT claim (per prereg section 7): no L3, no
generality, no architecture claim beyond the stated fixed-script claim.
The event script is disclosed, not a sealed adversarial world. The oracles
measure the frozen core's cross-phase integration baseline, which any H10
implementation must later beat.

## Deviations from the prereg

1. Event count erratum (prereg-internal): section 3 says "P4 (7 events)"
   and "Total: 150 events", but the enumerated frozen tuples give 3 OBSERVE
   + 3 QUERY = 6 P4 events, total 149. The driver implements exactly the
   enumerated tuples (149 events; audit counter confirms). No event was
   invented. No kill bar references the total count, so no bar is affected.
2. Launch mechanism (K1c): the prereg names `env -i plus PATH`; `env` is
   not linked in the safebin PATH, so runs launched via
   `bash -c 'exec -c ./cl_driver'` with a fully empty environment, which
   strictly satisfies the phase-free requirement. Argv carried no arguments.
3. Pre-wrapper scratch builds: 4 direct znc invocations in /tmp for driver
   development (2 trivial mechanism probes, 2 full scratch builds) ran
   before the wrapper existed; their binaries were discarded and never used
   for measurement. The wrapper log holds exactly the 1 official pre-run
   build. Disclosed in DRIVER.md.

## Follow-ups for the coordinator

- None required by this lane. The lane's standing question (what H10 must
  beat) now has a measured baseline: REUSE_COUNT 30/30 on the fixed script,
  0 interference loss under 2x unrelated load, byte-identical determinism.
- Suggested (not authorized here): the sealed post-freeze adversarial
  battery on the three new mechanisms remains the important generality
  test; this battery must not be cited for generality.
