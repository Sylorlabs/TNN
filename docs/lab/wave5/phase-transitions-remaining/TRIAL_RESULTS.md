# TRIAL_RESULTS.md — PT-01 / PT-23 / PT-34: the remaining phase transitions (2026-09-19)

Wave-5 investigation `phase-transitions-remaining`. Native lab, Zag-first,
compiled with `znc_linux_x86_64_abed8aa1`, executed on this Linux VM.

## Verdict: POSITIVE (all three)

All three remaining transitions trial natively as specified, against
their written falsifiers. No falsification criterion triggered in any
prereg (PREREG_01.md F1–F5, PREREG_23.md F1–F7, PREREG_34.md F1–F6).
126 CL_CHECK lines actual==expected across the three binaries; two
consecutive runs byte-identical per trial; RNG grep clean per trial;
every refused transition replay-verified and clean-refusals-verified.

- Trial sources: `trial/trial01.zag`, `trial/trial23.zag`,
  `trial/trial34.zag` (each `@import("memory_core.zag")` — the MA1 core
  copied unmodified from the wave-4 trial — plus `substrate/`).
- Runner: `trial/run_trials.sh`. Passing evidence: the latest
  `trial/EVIDENCE_*/` directory (`summary.txt`: `PT01_FAILURES,0`,
  `PT23_FAILURES,0`, `PT34_FAILURES,0`; `*_run1.stdout` carries every
  `CL_CHECK` and `PT*_STAT` line).

## PT-01: 0→1 Boot → Construction — pure trainer gate. POSITIVE.

The position-paper falsifier — *any unilateral system-side path to
phase 1* — was exercised directly and refused structurally.

- `PT01_STAT,A,1,0,2,3` — full evidence (3 organ verifications at/above
  protocol-fixed thresholds, firewall self-test with KILL refused
  `REFUSED_STAGE`): grant commits, phase=1, stage=MANAGE (firewall
  armed), manifest references the actual verification/self-test entries.
- `PT01_STAT,B,0,211,2,0` — system-side `pt01_self_grant` → refused
  `PT01_REFUSED_NOPATH`, phase stays 0, nothing mutated. The system has
  no write path to phase; the one function it could reach refuses.
- `PT01_STAT,C,0,212,2,1` — trainer grants with only 1 of 3 organs
  evidenced → refused `PT01_REFUSED_NO_EVIDENCE`, phase stays 0. The
  trainer cannot grant by fiat without evidence on record.
- `PT01_STAT,D,0,213,0,3` — all organs verified but no firewall
  self-test → refused `PT01_REFUSED_NO_SELFTEST`, phase stays 0.
- `PT01_STAT,E,0,0,0,0` — trainer never grants: a teaching op (ADD)
  attempted at stage NONE → refused `REFUSED_STAGE`; phase stays 0.
  Teaching is refused until the manifest is complete.
- `PT01_STAT,F,1,214,2,3` — double grant → refused
  `PT01_REFUSED_PHASE`, phase stays 1. No skip path exists (grant only
  writes 1).
- Organ suites are real, run on real cores: O1 replay+clean-refusals
  (2/2), O2 KILL-refused-at-MANAGE with KILL-working-at-KILL shape check
  (1/1), O3 append-only byte-identity (1/1).
- All scenarios: `*_replay,0,0`, `*_clean_refusals,0,0`.

## PT-23: 2→3 Development → Strengthening — system-deliberate + evidence gate, no trainer veto. POSITIVE.

Both position-paper falsifiers were exercised; neither triggered.

- `PT23_STAT,A,3,0,8,4,3` — 8 real judgments (4 promote, 4 consolidate
  on real slots), system derives its own stats and decides deliberately
  (arm=hybrid), commit → phase=3. Strength-set with a judgment citation
  succeeds; **re-set by the system succeeds** (reversibility holds —
  paper falsifier (b) discharged).
- `PT23_STAT,B,2,222,2,1,3` — premature (2 judgments, forced decision)
  → refused `PT23_REFUSED_PREMATURE`, phase stays 2.
- `PT23_STAT,C,2,222,0,0,3` — decision with zero judgment record →
  refused. **Paper falsifier (a) discharged: a system with no Phase-2
  judgment record cannot pass the gate.**
- `PT23_STAT,D,3,0,8,4,3` — strength-set without citation → refused
  `PT23_REFUSED_NO_CITATION` (table untouched); strength-set at phase 2
  → refused `PT23_REFUSED_PHASE`. Judgment provenance is enforced at
  every use, which subsumes the paper's gate pre-check (see
  SPEC_AMENDMENTS.md).
- `PT23_STAT,E,3,0,8,4,3` — trainer veto attempt → refused
  `PT23_REFUSED_NO_VETO`, mutates nothing; the legitimate commit then
  succeeds. **The veto fails structurally and does not block the
  transition.**
- `PT23_STAT,F,3,0,8,4,3` — pre-commit trainer force-pin on slot 0:
  commit proceeds, commit entry records pin=1 visibly; system re-set of
  the pinned slot → refused `PT23_REFUSED_PINNED`; unpinned slot re-set
  → OK. The brake exists, is scoped, is visible — and the phase is
  compatible with a pinned value.
- `PT23_STAT,G,3,0,8,4,3` — system-side pin attempt → refused
  `PT23_REFUSED_NOPATH`; the system's own strength stays re-settable.
  The only true lock is the human pin.
- `PT23_STAT,H,2,223,8,4,3` — spoofed decision (claims 0/0/0 vs derived
  8/4/4) → refused `PT23_REFUSED_CLAIM_MISMATCH`, phase stays 2.
- All scenarios: `*_replay,0,0`, `*_clean_refusals,0,0`.

## PT-34: 3→4 Strengthening → Differentiation — petition + prereg + evidence gate + trainer grant. POSITIVE.

Both position-paper falsifiers were exercised; neither triggered.

- `PT34_STAT,A,4,0,2,1,7` — evidence 2/1 (method 1), partitions declared
  (spk1→0..3, spk2→4..7), in-scope facts, one cross-partition attempt
  refused *at write time* (`PT34_REFUSED_SCOPE` — scope, never
  arbitration), petition with mask 0b111, trainer grant → phase=4.
  Grant entry records the prereg reference (petition index), checks,
  scheme.
- `PT34_STAT,B,3,234,2,2,7` — sybil (speaker 2 cites speaker 1's
  evidence id 102) → refused `PT34_REFUSED_SYBIL`, phase stays 3.
- `PT34_STAT,C,3,235,2,1,7` — adversarial calibration: a
  cross-partition fact appended through the bypass stub (simulating a
  write path the scope check missed) → the gate's ledger scan refuses
  `PT34_REFUSED_LEAKAGE`, phase stays 3. **Paper falsifier (b)
  discharged: no cross-partition write path the gate missed.**
- `PT34_STAT,D,3,236,2,1,7` — spoofed petition (claims 3/3 vs derived
  2/1) → refused `PT34_REFUSED_CLAIM_MISMATCH`, phase stays 3.
- `PT34_STAT,E,3,231,2,1,7` — grant without petition → refused
  `PT34_REFUSED_NO_PETITION`, phase stays 3.
- `PT34_STAT,F,3,232,2,1,0` — prereg with criteria mask=0 → refused
  `PT34_REFUSED_UNMEASURABLE`, phase stays 3. **Paper falsifier (a)
  discharged: no granted 3→4 with an unmeasurable prereg.**
- `PT34_STAT,G,3,233,0,0,7` — petition before any identity evidence →
  refused `PT34_REFUSED_NO_EVIDENCE`, phase stays 3 (no partitioning
  before identity evidence).
- `PT34_STAT,H,4,0,2,1,7` — rollback + re-entry rule: phase 4 →
  `pt34_dissolve` → phase 3 (audited); grant on the stale (pre-dissolve)
  petition → refused `PT34_REFUSED_NO_PETITION`; fresh petition + grant
  → phase=4. The paper's "re-entry requires a fresh petition" is
  structural (freshness = petition index newer than latest dissolve).
- All scenarios: `*_replay,0,0`, `*_clean_refusals,0,0`.

## What the trials do NOT establish (honest negatives)

- The protocol-fixed values (3 organs / pass thresholds; 8 judgments +
  kind coverage; 2 speakers / slot ranges / method 1) are honesty
  boundaries, not derived truths — same as MA1/SM1.
- 0→1: the trainer force-pin halt path (spec §1) is specified, not
  trialed. Tightening transitions (3→2 rollback, 2→1 re-arm) are
  specified, not trialed — except 4→3 dissolve, which is trialed (H).
- 2→3: the graded/uniform/hybrid arms are declared and recorded only;
  the strength experiment's behavioral differences are separate work.
- 3→4: enforcement covers entry structure (measurable prereg,
  isolation, anti-sybil, evidence-before-structure). The surveillance
  failure mode beyond the prereg — whether each fact's content was
  consented-to — is recorded at grant time but cannot be automated;
  the trainer-as-counterparty is the accountability point there.
- Scale: 8 slots, tens of ledger entries per scenario. Gate scans are
  O(ledger window); the 10× scale trial is deferred (same note as
  PT-12's PT2).

## Build notes

- Reused without modification: `trial/memory_core.zag` and
  `trial/substrate/` (copied from the wave-4 PT-12 trial).
- One trial-code fix during the build: PT-01's O1 suite initially
  expected the pressure KILLs to *succeed*; at stage MANAGE they must be
  *refused* (that refusal is the firewall working). Fixed the suite's
  expectations (`ma_kill` must return `MA_REFUSED_STAGE`); no mechanism
  change. The prereg's mechanism description is unaffected.
- Evidence accumulates under `trial/EVIDENCE_<stamp>/`; each contains
  per-trial `rng_grep.txt`, `compile.stdout/stderr`, `run1.stdout/stderr`,
  `run2.stdout`, and `summary.txt`.
- No git pushes (program law). No compiler bugs encountered.

## Next step

PT2-scale trial (deferred from PT-12): 80 slots, 10× curriculum,
assert per-gate cost linear in the ledger window only — extended to
cover the PT-23 judgment scan and PT-34 evidence/partition scans, since
all three gates scan a ledger window. Kill criterion (from PREREG_12):
per-gate cost growing with store capacity.
