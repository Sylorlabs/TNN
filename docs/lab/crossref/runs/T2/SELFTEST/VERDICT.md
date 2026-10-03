# VERDICT.md — T2-SELFTEST replication (Wave 2, Tier 2)

Crew: T2-SELFTEST (REPLACEMENT — predecessor killed mid-run by runtime daemon
restart; no predecessor artifacts were present in the run dir).
Date: 2026-09-22/23. Type A replication (rebuild from committed sources in a
clean checkout; re-run at both scales; re-inject the silent-skip fault).

## 1. Authoritative checklist (quoted verbatim from the frozen prereg)

Source: sylorlabs/TNN, branch `tnn-native-lab`, commit
`7b2100d09911c5c10252c5756c7def288e70bd1f`,
`docs/lab/crossref/PREREG_TIER2.md`, section
"## T2-SELFTEST — self-testing harness at 1× and 10× (Type A)" (lines 131–137).
Extracted by this crew from the frozen commit itself (not from any summary).

> **Claims:** commit `334444eb94d8` (API-verified): one pure-Zag zero-RNG binary executes a frozen battery manifest, adjudicates pass/trip/unrunnable against preregistered bars itself, audits each verdict, structurally refuses completion unless emitted verdict count = manifest count. Independent-oracle fidelity 40/40 at 8 batteries and 400/400 at 80 batteries; byte-identical 5/5 at both scales; orchestration overhead 0.0127× battery ops; fault-injected silent skip blocked by both binary and oracle. Honest limits: manifest compiled in, learner embedded, battery kinds limited, formula-generated data; adoption needs loadable manifests, external learner dispatch, richer/live battery types, multi-config matrices.
> **Method:** rebuild from committed sources in clean checkout; re-run at both scales; re-inject the silent-skip fault.
> **Rule:** REPRODUCED if 40/40, 400/400, 5/5 byte-identical, overhead ≈0.0127×, silent skip blocked; NOT REPRODUCED if the binary completes with a verdict-count mismatch or the fault slips through.

## 2. Verdict: REPRODUCED

Every element of the frozen decision rule holds on the rebuilt binary:

| Frozen claim | Measured (this replication) | Disposition |
|---|---|---|
| 40/40 independent-oracle fidelity, 8 batteries (s1) | oracle: 40/40 verdict lines match obs+verdict+bar; 0 failures; exit 0 | HOLD |
| 400/400 independent-oracle fidelity, 80 batteries (s10) | oracle: 400/400 verdict lines match; 0 failures; exit 0 | HOLD |
| 5/5 byte-identical at both scales | s1: 5/5 md5 `3be14786…`; s10: 5/5 md5 `6ffead66…` | HOLD |
| orchestration overhead ≈0.0127× battery ops | s1: 40/3144 = 0.0127; s10: 400/31440 = 0.0127 | HOLD (exact) |
| fault-injected silent skip blocked by both binary and oracle | binary: `ST_BLOCKED,emitted=7,expected=8`, no ST_DONE; oracle: coverage miss + count 7v8 + ST_DONE missing + ST_BLOCKED present, exit 1 | HOLD |
| NOT: binary completes with verdict-count mismatch | all 10 clean runs emitted ST_DONE with verdict count == manifest count (8 / 80); oracle COUNT check passed on all | absent |
| NOT: fault slips through | fault run blocked at both layers | absent |

Byte-identity against committed evidence: this crew's rebuilt-binary outputs
are md5-identical to the committed run logs in the frozen commit —
`s1` → `3be14786893ae083ed4f3ede9a67024d` (== committed `runs_s1_r0.log`),
`s10` → `6ffead6686871b4191fe6e5927c354ce` (== committed `runs_s10_r0.log`).

Per-battery verdicts (identical at both scales, all 5 reps):
B1 obs=240 bar=236 PASS; B2 obs=12 bar=12 PASS; B3 obs=96 bar=92 PASS;
B4 obs=48 bar=46 PASS; B5 obs=0 UNRUNNABLE; B6 obs=1 PASS;
T1 obs=239 bar=240 TRIP; T4 obs=47 bar=48 TRIP.
Manifest tallies — s1: pass=5 trip=2 unrunnable=1 error=0, bat_ops=3144,
orch_ops=40, audit_records=8; s10: pass=50 trip=20 unrunnable=10 error=0,
bat_ops=31440, orch_ops=400, audit_records=80. (5/2/1 per 8 batteries ×
reps/variants — the oracle recomputed the tallies independently and agreed.)

## 3. Honest caveats (carried, not hidden)

- **B6 GAP (documented in the frozen `SELFTEST_VERDICT.md` at the same
  commit, DOC-SWEEP 2026-09-22, bar-audit abaa5c7b57b6):** the "40/40" and
  "400/400" fidelity figures include B6 verdicts whose digest equality the
  oracle *asserts* rather than recomputes (oracle.py `expected_obs("B6")`
  returns 1 unconditionally). Independently-recomputed coverage: **35/40 at
  s1** (5 B6 lines asserted) and **350/400 at s10** (50 B6 lines asserted).
  This crew measured the same oracle behavior and reports both numbers. The
  frozen decision rule's "40/40, 400/400" is satisfied *as defined by the
  committed oracle's procedure*; the recomputed-subset figures are stated
  here so the verdict does not overclaim.
- **T1 TRIPWIRE (same doc-sweep):** KB-ST-OVERHEAD's bar (≤ 2.0) is
  non-informative — 0.0127 is ~157× under it. The number is exact and
  reproduced; the "cheap/lean" reading inherits the bar's weakness. Recorded
  per the frozen verdict doc; not re-litigated here.
- Honest limits from the prereg confirmed in source: manifest compiled in
  (battery ids hardcoded in `main`'s loop), learner embedded (`ln_*` fns in
  the same binary), 8 fixed battery kinds, closed-form formula data
  (`truth`/`flie` — no RNG, no seeded PRNG anywhere in the source).

## 4. Frozen pins (all verified before running)

- Frozen prereg commit: `7b2100d09911c5c10252c5756c7def288e70bd1f`
  ("crossref: scope + frozen preregs…", 2026-09-22) — present in clean repo.
- Claim/evidence commit: `334444eb94d8388bf79a1c54224c3405a27131a9`
  ("Self-test TNN: the TNN as its own test-runner", 2026-09-21) — verified
  present via GitHub REST API (`GET /repos/sylorlabs/TNN/commits/334444eb…`).
- Code identity: `selftest.zag`, `oracle.py`, `SELFTEST_PREREG.md`, and all
  `runs_*` logs are **byte-identical** between `334444eb94d8` and
  `7b2100d09911c5c10252c5756c7def288e70bd1f` (`git diff` shows only
  `SELFTEST_VERDICT.md` changed — the doc-sweep corrections). Build used the
  frozen commit's sources, which are the claim commit's sources.
- Built source blobs at frozen commit: `selftest.zag`
  `abfe915663590e3e39cd5e923b9909fd9797d6a6`; `oracle.py`
  `16aa10b65177139efe5762674b465f4612d32a1e`; `PREREG_TIER2.md`
  `b1178370036bffbda6eb68ea0989c0e427dc31b7`.
- znc: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`;
  build cmd per source header: `znc_linux_x86_64_abed8aa1 selftest.zag -o selftest --no-analyze`.
- No `.zagd`/binary copies from elsewhere; binaries built fresh in
  `crew/build/` (scratch, never committed).

## 5. Method notes / anomalies

- RESUME: predecessor left an empty `clean/` (bare `git init`, no objects)
  and an empty `crew/`. No partial VERDICT/RUNLOG existed; nothing to resume.
- Infrastructure anomaly (recorded, did not affect validity): the clean
  clone's 463 MB fetch completed at ~05:12, then the entire `clean/`
  directory vanished from the filesystem (~05:21; not in Muse trash; disk
  has 68 GB free — cause unknown, possibly another process). Recovered
  read-only: the T2/TQ crew's local clone held both pins in its object
  store; this crew re-fetched from GitHub with `--depth=110 --filter=blob:none`
  (1.4 MB) and materialized only the needed paths at the frozen commit.
  TQ's repo was never written to. `git fsck` clean on the rebuilt checkout.
- Determinism: rep arg (`<rep>`) is accepted but never printed — output is
  rep-invariant by construction; 5/5 byte-identical confirmed at both scales.
- Fault injection: this crew's own re-injection (guard `if(batt!=5)` around
  the orchestrator's inner loop in a clearly-labeled copy
  `selftest_fault.zag`) reproduces the original fault report exactly:
  `ST_BLOCKED,emitted=7,expected=8`, no ST_DONE, no ST_MANIFEST; oracle
  exit 1 with coverage miss / count 7-vs-8 / ST_DONE missing / ST_BLOCKED
  present. The pristine source was never modified.

## 6. Deliverable paths

- Run dir: `~/workspace/scratch-crossref/T2/SELFTEST/crew/`
  ([VERDICT.md](sandbox://workspace/scratch-crossref/T2/SELFTEST/crew/VERDICT.md),
  RUNLOG.md, `build/` sources+both binaries, `runs/` 10 clean logs + fault log)
- Clean checkout: `~/workspace/scratch-crossref/T2/SELFTEST/clean/`
  (frozen commit `7b2100d0`, needed paths materialized; fsck clean)
