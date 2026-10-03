# SEALED_EVAL: CLH2 longer-horizon delayed rebind

Wave: wave-20261002-0521pdt. Lane: CONTLEARN (CLH2). Date: 2026-10-02.
Frozen prereg: PREREG_CLH.md (commit aa47999f7, alone). Implementation
commit ef9b80200; K0 merge-base ancestry verified before verdict.

"Sealed" in this lane (per prereg section 1): the battery was frozen
before implementation, all ids/relations fresh and verified unused, all
oracles content-identified, no post-result tuning. The battery is
disclosed and prereg-frozen, NOT adversary-designed; no generality claim
follows.

## Runs

3 binaries x 3 reps = 9 learner processes, one process per full script,
empty argv, empty env, rc=0 on all 9, 0 stderr bytes on all 9.

- clh2_treat (treat core + full driver, 166 events): stdout SHA-256
  2f03c4af4d857b617ea6074ce4a24730d37190bba476ed9fb3d8dcefd2d29b00
  on all 3 reps; FNV 1491595695 on all 3.
- clh2_control (control core + full driver, 166 events): stdout SHA-256
  d53258f7efac4f9c62ee97c6bfbba243631876b8af4ca222eada06907199dcd
  on all 3 reps; FNV -1746384548 on all 3.
- clh2_nophase (treat core + nophase driver, 142 events): stdout SHA-256
  9e6b86812e6d925f19097ee38b915269e3be53c310aad3e21af0216442eb2756
  on all 3 reps; FNV 275619593 on all 3.

No PID, timestamp, or path bytes in any transcript (verified by the
byte-identical hashes plus grep for digit-run anomalies; the only
varying-looking tokens are deterministic node ids).

## Per-bar results

| Bar | Result | Evidence |
|-----|--------|----------|
| CP-R0 ordering (TREAT) | PASS | 24 PROPOSAL / 24 MACHINERY / 0 MACHINERY_SKIPPED on all 3 reps; 12/12 rebind (s,r) pairs with PROPOSAL line-number < MACHINERY line-number and matching prop node ids (tail 97001..97006/863, head 97101..97106/866) |
| CP-R1 rebind (TREAT) | PASS | REBIND_OK 12/12 on all 3 reps: answers 96201+i (tail) / 96101+i (head), serve_ok via the promoted facts, new MAPs with alive DEP edges to the phase-A chain facts AND the anchor facts |
| CP-R1 proposal cite | measured | REBIND_PROP_CITE 12/12 on TREAT, 0/12 on CONTROL (no proposals exist there) |
| CP-R2 survival (TREAT) | PASS | SURVIVE_OK 6/6 (phase-A MAPs live, DEP citations to both licensing facts live); SURVIVE_ANSFACT 6/6 |
| CP-R3 retention (TREAT) | PASS | RETAIN_OK 6/6 |
| CP-R4 interference (TREAT) | PASS | PRESSURE_OK 96/96; INT2_OK 1/1 (96601 superseded, 96603 live, probe 96603); STORE3_OK 6/6 |
| CP-R5 discriminator (NOPHASE) | PASS | NOPHASE_OK 12/12 (all rebind answers == 1, the frozen count-branch prediction); NOPHASE_NOA 1/1 (phase-A facts absent); integrity STORE3_OK 6/6, PRESSURE_OK 96/96, INT2_OK 1/1 |
| CP-R6 determinism | PASS | 3/3 byte-identical per binary (hashes above); FNV equal; rc=0; 0 stderr |
| CP-R7 control | PASS, no anomaly | CONTROL: REBIND_OK 12/12, SURVIVE_OK 6/6, RETAIN_OK 6/6, zero PROPOSAL occurrences; reproduces TREAT on every rebind bar |
| K0 commit order | PASS | prereg aa47999f7 and NAMECHECK c927915b3 both strict ancestors of impl ef9b80200 |
| K1a one learner, no reset | PASS | 9 processes (3 binaries x 3 reps), one per full run; pid_leak_check=0 (PIDs only in harness_clh2.log) |
| K1b builds logged | PASS | znc_invocations_clh2.log: exactly 3 entries (pre-run builds), 0 new during runs |
| K1c audit, no task labels | PASS | AUDIT_PASS 166/166 (FULL) and 142/142 (NOPHASE) on all 9 runs; kinds in {1,2,3}; MQUERY expected=-2, flags=1; OBSERVE is the frozen counterexample protocol; empty argv/env |
| K2a frozen ISA boundary | PASS | tnn2.zag a29972ca... before builds and after runs; nomain derivation 26b455e7... before builds; clh2_core_control.zag hashes 26b455e7... (byte copy); clh2_core_treat.zag hashes 627af6eb... (byte copy); frozen path never written |
| K2b driver audit | PASS | Both drivers: 0 cognition functions (clh_-prefixed fixture fns only: event emission, read-only oracles, census, prints); ns(/link_edge(/alloc_node( count 0; 0 new tags/edges/opcodes/modes/bridges/routers/handlers; switch/match count 0 |
| K2c source delta | PASS | Frozen path 0/0/0; lane cores 0-line delta (cmp byte-identical to recorded 0221pdt sources); drivers are lane fixtures (full 317 lines, nophase 236 lines); 0 new modes/bridges/handlers/tags/edges/opcodes/state formats; ONE-SYSTEM RULE checked explicitly (one 110656-byte arena, proposals as tag-1 POLICY_ROOT-space nodes, no independent state format) |
| K2d pure Zag | PASS | Zero Python/C/JS/Rust; `which python3` empty under safebin PATH (NAMECHECK.md Step 0, recorded before any research operation) |
| K3 no regression | PASS | lo_driver 3x with stdin TREAT: stdout SHA-256 1ff527fa97b36da25fd8163299773680e53ae47fba521fc2227b0bf7c39394d9 on all 3; rc=0; 0 stderr |
| Capacity guard | PASS (no trip) | CAPGUARD nodes=426 edges=421 at REBIND (caps 1024/4096); no eviction possible |

## Census trace (TREAT rep 1, selected phases)

- CAP: MAPC=6 PROPC=6 (6 novel integrations)
- INT1: N1 grows by 96 pressure facts, MAPC unchanged
- INT3: MAPC=12 (second family integrated; phase-A MAPs intact)
- ANCHOR: MAPC=12, 12 anchor facts added
- REBIND: MAPC=24 PROPC=24 DEPC=120 UNC=0 GUIDEC=0 N1=183 Eall=421

The 12 rebind MAPs are new structures (MAPC 12 -> 24); the 6 phase-A
MAPs are untouched (SURVIVE_OK 6/6). UNC=0/GUIDEC=0 throughout: every
novel query verified through the trial path, so miss_inquire never
fired; no true misses occurred in any run.

## Verdict

**REBIND-DEMONSTRATED.** All frozen bars pass. See VERDICT_CLH2.md for
the claim bound and REDTEAM_SELF.md for the adversarial review.
