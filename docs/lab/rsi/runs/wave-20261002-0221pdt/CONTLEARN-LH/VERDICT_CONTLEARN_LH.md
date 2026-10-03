# VERDICT_CONTLEARN_LH: longer-horizon delayed reuse under sustained interference

Wave: wave-20261002-0221pdt. Lane: CONTLEARN-LH. Date: 2026-10-02.
Frozen prereg: PREREG_CONTLEARN_LH.md (commit 8d43c6e55), transparently
amended by PREREG_CONTLEARN_LH_AMEND1.md (commit 32bfea311;
pre-implementation event-count correction 358 to 356, no design change).
Implementation commit (see RUN_LOG.md); merge-base ancestry of both
prereg commits verified (K0).

## Per-bar results

| Bar | Result | Evidence |
|-----|--------|----------|
| CP-LH1 ordering maintained 8/8, 0 skips | PASS | 8 PROPOSAL / 8 MACHINERY / 0 MACHINERY_SKIPPED on all 3 TREAT reps; per-(s,r) line check with matching prop node ids (6 NOVEL + 2 LATE-NOVEL at longest horizon); PROPC_FINAL==8 |
| CP-LH2 integration under proposal-first | PASS | STORE_OK 6/6, STORE_PROP_CITE 6/6; LATE_STORE_OK 2/2, LATE_PROP_CITE 2/2 |
| CP-LH3 retention curve | FAIL | REUSE_A 12/12 at V=52; REUSE_B 10/12 at V=152; REUSE_C 8/12 at V=276. Misses are exactly the chains whose licensing facts were deliberately conflicted (2, then 4). Root cause in SEALED_EVAL.md |
| CP-LH4 conflict/correction/retention | PASS | CONFLICT1/2/3_OK 1/1, CORRECT1/2/3_OK 1/1, RETENTION_OK 12/12 |
| CP-LH5 determinism | PASS | 3/3 byte-identical stdout per binary (TREAT 644ba03f..., CONTROL 3ac5697a...); FNV equal across reps; rc=0; 0 stderr bytes; no PID/timestamps/paths |
| CP-LH6 control, machinery-first | ANOMALY (reported, not VOID) | Control reproduces the TREAT curve exactly (12/12, 10/12, 8/12) with zero PROPOSAL occurrences; the degradation is instrument-independent (frozen-core revision semantics). Prereg anomaly clause applied with root-cause analysis |
| K0 commit order | PASS | Prereg 8d43c6e55 and amendment 32bfea311 both strict ancestors of the implementation commit |
| K1a one learner, no reset | PASS | 6 processes (2 binaries x 3 reps), one per 356-event run; pid_leak_check=0 |
| K1b builds logged | PASS | znc_invocations_lh.log: exactly 2 entries (pre-run builds), 0 new during runs |
| K1c audit, no task labels | PASS | AUDIT_PASS 356/356 on all 6 runs; kinds in {1,2,3}; MQUERY expected=-2, flags=1; OBSERVE is the frozen counterexample protocol; empty argv/env |
| K2a frozen ISA boundary | PASS | tnn2.zag SHA-256 a29972ca... before builds and after runs; nomain derivation 26b455e7... verified before builds; lane cores byte copies (hashes match); frozen path never written |
| K2b driver audit | PASS | 0 cognition functions; 0 structural writes; 0 new tags/edges/opcodes/modes/bridges; 0 switch/match |
| K2c source delta | PASS | Frozen path 0/0/0; lane cores 0-line delta (byte copies of recorded CONTLEARN files); driver is a lane-dir fixture; 0 new modes/bridges/handlers/tags/edges/opcodes/state formats; ONE-SYSTEM RULE checked explicitly |
| K2d pure Zag | PASS | Zero Python/C/JS/Rust in research logic; `which python3` empty under safebin PATH (NAMECHECK.md Step 0); one self-disclosed non-incident (stray probe, nothing resolved or ran) |
| K3 no regression | PASS | Committed 2321pdt lo_driver 3x read-only (stdin "TREAT"); stdout SHA-256 1ff527fa... on all 3 reps; rc=0; 0 stderr bytes |

## Verdict

**LH-DEGRADED.** Per the frozen decision rule, CP-LH3 fails while
CP-LH2 passes: retention of the original chain values degrades with the
interference horizon (12/12 at V=52, 10/12 at V=152, 8/12 at V=276).
The bar is not weakened retroactively; the numbers stand as the measured
curve.

The informative content of the degradation (established by post-hoc
read-only diagnostic, deterministic 3/3, identical on both instruments):
unrelated-domain interference at three growing volumes caused ZERO
degradation (REUSE_A 12/12; unconflicted chains and the sanity family
intact through V=276 with 264 interfering facts). The 12 to 10 to 8
curve counts exactly the chains whose licensing facts were deliberately
conflicted. The DEP-cited MAP structure survived all 356 events intact
(all citations live); the frozen revision operator revised the composed
answers downstream LIVE at contradiction time (new integrated facts with
the contradictory values) but did not re-propagate on correction, so the
composed answers froze at the contradicted values while the underlying
facts moved on to the resolved values. Single-propagation revision: a
precise, reproducible property of the frozen core, not of the
proposal-gate instrument.

## Claim bound (binding, carried over from CONTLEARN3)

The proposal content (mech=TRY_CHAIN) is a fixed researcher template;
no learner authorship of proposal content, no learner scheduling of
proposal initiation, no learner agency in the causal sense, no L3, no
generality. The instrument is a measurement instrument, not a proposed
architecture. The battery is disclosed, not sealed adversarial.
Citation form stays machinery-enabled.

## Build status

**BUILD-FAIL** for the as-frozen sustained-retention claim
(LH-DEGRADED). The failure is the informative kind and localizes to
revision-propagation semantics, not to capacity, ordering, citation
integrity, or the instrument.

## Follow-ups for the coordinator

- Recommended next hypothesis: correction-propagation (does a second
  downstream revision fire when the contradicted node is itself
  superseded?), tested against the same frozen oracles, with no new
  modes, bridges, or handlers. Per the no-patch-treadmill rule this
  needs root-cause clustering first; the diagnostic here is the start.
- Queued from CONTLEARN3, still open: empirical exercise of the gate's
  refusal branch (0 MACHINERY_SKIPPED again this lane).
- The CP-LH3 oracle's demand (original values after deliberate
  conflicting evidence) was the least defensible of the three candidate
  correct behaviors; a future prereg should decide the expected composed
  answer under conflict-then-correction BEFORE freezing the bar.
