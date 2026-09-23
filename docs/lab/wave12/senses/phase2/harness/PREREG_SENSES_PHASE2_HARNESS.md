# PREREG — Senses Phase 2 Harness/Verifier: cross-cutting sections F–I + counting reporter + independent verification

Date: 2026-09-20. Status: **FROZEN BEFORE BUILD.**
Dir: `docs/lab/wave12/senses/phase2/harness/` (workspace: `~/workspace/tnn-lab/wave12/senses/phase2/harness/`).

## 1. Role

This worker is the HARNESS/VERIFIER for TNN senses phase 2. It implements the
CROSS-CUTTING sections of the proposed qualification bar
(`../PROPOSED_QUALBAR_SENSES_2026-09-20.md` — PROPOSED, UNSIGNED, needs
Micah's approval to become law), counts all 155 checks, and independently
verifies the two modality tracks (audio, vision). It does NOT implement the
modality batteries §A–E — those belong to the sibling workers; their dirs are
read-only to this worker (read to coordinate, never edit).

Measurement language: results are reported as "meets / does not meet the
proposed bar". The word QUALIFIED is never used by this harness.

## 2. Scope

Build (in this dir only):
- `se2_main.zag` — pure-Zag driver with modes `harness` (§H churn + §I
  mid-harness save) and `verify` (fresh-process §I reload checks).
- `run_phase2_harness.sh` — §G static scans, double build + hash compare,
  double harness run + stdout diff, verify run. Emits `se2f-*`/`se2g-*` lines.
- `count_phase2.sh` — counting reporter over all phase-2 logs.
- `VERIFICATION_PHASE2.md` — independent per-track verification verdicts.
- Vendored copies of phase-1 `se_ingress.zag`, `se_memif.zag`, and
  `substrate/` (provenance + deltas in `VENDORING.md`).

Out of scope: modality batteries §A–E (audio: `se2a-*`, vision: `se2v-*`),
live sensors, classifiers, performance.

## 3. Kill bars (carried over from phase 1, binding)

K-SE1 replay mismatch, K-SE2 silent admission, K-SE3 refusal mutation,
K-SE4 aliasing, K-SE5 computed strength, K-SE6 RNG/clock/threads/floats,
K-SE7 save/reload identity, K-SE8 protected kill. A fired bar kills the run;
the witness is committed as evidence and reported honestly as DEAD.

## 4. §F replay (2 checks)

`run_phase2_harness.sh`:
1. Compiles the frozen sources twice with the pinned znc
   (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`) →
   `se2_bin_a`, `se2_bin_b`; compares binary SHA256. Identical → emit
   `CL_CHECK,se2f-build-hash,1,1`; differ → `,0,1` and abort (K-SE1
   build leg).
2. Runs `./se2_bin_a harness` then `./se2_bin_b harness`, each from clean
   state (`rm -rf se2_store` before each); diffs stdout. Empty diff and both
   rc=0 → emit `CL_CHECK,se2f-replay-runs,1,1`; else `,0,1` and abort
   (K-SE1).

"Full battery" = the `harness` mode: fixtures → 24 record admits → 1,000
deterministic OBSERVE/KILL cycles → §H checks → 8 refusal re-probes →
mid-harness save. Stdout contains only `CL_CHECK` lines and fixed markers
(no timestamps, no paths, no pointers).

## 5. §G static (2 checks)

Over ALL phase-2 `.zag` sources (this dir + `../audio/` + `../vision/` when
landed):
- K-SE6: strip full-line and trailing `//` comments; grep for
  `_zag_rand|gettimeofday|clock_gettime|thread_create|pthread_create|`
  `_zag_time`, `\bf32\b`, `\bf64\b`, and float literals `[0-9]\.[0-9]`.
  Zero hits → `CL_CHECK,se2g-no-banned,1,1`; any hit → `,0,1` and abort.
- K-SE5: admit-path scan. Every assignment to a strength store field
  (pattern `\.strength(\[|=)`) must have RHS exactly `<identifier> as u8`
  — i.e. the caller-declared parameter cast, no arithmetic. Mechanical:
  `grep -nE '\.strength(\[|=)'` piped to `grep -vE`
  `=[[:space:]]*[A-Za-z_][A-Za-z0-9_]* as u8;` must be empty →
  `CL_CHECK,se2g-no-computed-strength,1,1`; else `,0,1` and abort.
  Honest boundary (as phase 1): caller discipline + static check + audit;
  the scan covers the admit path (vendored `se_memif.zag` + any phase-2
  admit path).

## 6. §H churn (4 checks)

Driver (`harness` mode): 1,000 deterministic OBSERVE/KILL cycles against the
16-slot store. Fixtures: 8 churn records (PCM16LE 8000 Hz mono, 32 B
payloads, deterministic byte pattern) + 8 audio twin records + 8 vision twin
records (see §7). Cycle `i` (0..999):
- `OBSERVE(rec = i mod 8, judgment = 1 + (i mod 4), strength = 1 + (i*37 mod
  100), region = USER, cite_ep = i)`. Judgments and strengths are
  caller-declared by the driver via a fixed deterministic pattern — this is
  caller discipline, not K-SE5-relevant contract computation (the contract
  copies the declared parameter; §G scan covers the admit path).
- Unless `i mod 100 == 99`: `KILL(slot, evidence = 1 + (i mod 99))`.
  (Every 100th observation is left alive → 10 live slots at end; all kills
  target USER-region unpinned slots with nonzero evidence → all succeed.)

Ops issued: 1000 OBSERVE + 990 KILL = 1990, all expected MI_OK. The driver
records every issued op (op, slot, rc, judgment, strength, region, cite_ep,
rec_id) in a parallel expected-ops array.

Checks (emitted by the driver):
- `se2h-audit-complete`: `audit_n == 1990` AND every audit entry
  (op,slot,rc,j,st,rg,ce,ri) matches the issued-op log entry-by-entry — no
  gaps, no drops, no reordering. (K-SE2-adjacent.)
- `se2h-no-silent-admit`: `mi_audit_scan() == 1` — every live slot traces
  to a successful OBSERVE audit entry. Zero silent admissions.
- `se2h-fresh-state`: a fresh `SeStore`+`MiStore` run through the same
  logical sequence (same 24 admits, same 1,000 cycles) produces
  byte-identical records image, slots image, and audit image. (Non-degradation.)
- `se2h-refusals`: re-probe 8 §B refusal codes, all exact: judgment NONE →
  -7201; judgment 5 → -7201; strength 0 → -7202; strength 101 → -7202;
  region 2 → -7203; cite_ep -1 → -7209; dead rec_id 99 → -7204; fill store
  to 16 then one more → -7205.

Order: churn → H1 → H2 → H3 → H4 (H4's fill probe mutates state and adds 6
audit entries, so it runs last; no later check depends on audit_n).

### Vendoring delta (documented, binding on this build)

The phase-1 skeleton's `se_memif.zag` caps the op audit at 256 entries and
silently stops recording when full. A 1,000-cycle churn issues 1,990 audited
ops, so the literal §H bar ("entry count equals ops issued") is unreachable
on the 256-cap skeleton. This harness therefore vendors `se_memif.zag` with
ONE delta: `MI_AUDIT_CAP` 256 → 2048. Op table, refusal codes, judgment
gate, slot semantics, and all K-SE5/K-SE6 properties are unchanged. Delta
listed in `VENDORING.md` with canonical sha256. Reported to Micah as an open
question: whether the skeleton's audit capacity should change, or the bar be
amended. The audit *semantics* under test (append-only, one entry per op,
complete) are exactly what §H demands.

## 7. §I save/reload (5 checks)

Mid-harness save (end of `harness` mode, after H4): `se_save` + `mi_save`
into `se2_store/` (regenerable; never committed), plus canonical
serializations hashed with SHA256 and written to
`se2_store/se2_expected.sha256`:
- records image: `n[4]` then per record `len[4]+bytes` (same layout as
  records.bin);
- slots image: live+ pinned + region + judgment + strength (16 B each) +
  cite_ep + rec_id (64 B each) + phash (512 B) = 720 B;
- audit image: `audit_n[4] + clock[4] + audit[0..audit_n*32]`.

Fresh-process reload (`verify` mode, run with the OTHER build, cross-build
like phase 1): load from `se2_store/`, re-serialize, re-hash, compare:
- `se2i-records`: records image byte-identical (hash match).
- `se2i-slots`: slots image byte-identical.
- `se2i-audit`: audit image byte-identical.
- `se2i-audio-twins`: for each of 4 audio twin pairs (records 8..15,
  admitted in harness mode): loaded bytes == deterministically re-authored
  fixture bytes, pair bytes differ, payload sha256 differ. All 4 pairs →
  pass. (K-SE7 twin leg.)
- `se2i-vision-twins`: same for 4 vision twin pairs (records 16..23).

Twin fixtures (deterministic, authored in-driver; twin pairs differ in
exactly one controlled item):
- Audio (PCM16LE 8000 Hz mono, 32 B payloads): A1 sample[7] sign flip;
  A2 sample[3] +1 LSB; A3 +1 DC offset all samples; A4 silence vs
  1-LSB dither.
- Vision (RGB8): V1 single-pixel +1; V2 pixel permutation (identical byte
  histogram, different bytes); V3 row swap (2×2); V4 1×1 vs 2×2 geometry.

Note: at prereg time the audio/vision worker dirs have not landed, so their
committed twin fixtures cannot be read yet. §I therefore uses the
in-driver fixtures above; re-validation against the workers' committed twin
fixtures happens in the independent-verification step and is recorded in
`VERIFICATION_PHASE2.md`. If the workers' fixtures are readable as
TNNRAW02 records, they are additionally run through this harness's
admit→save→reload path as a cross-check.

## 8. Counting reporter (`count_phase2.sh`)

- Discovers logs: all `*.txt`/`*.log` files under
  `~/workspace/tnn-lab/wave12/senses/phase2/` (recursively), excluding
  nothing by track — each track writes its own logs dir.
- Parses `CL_CHECK,se2*` lines; maps name prefix to section:
  se2a→A, se2b→B, se2c→C, se2d→D, se2e→E, se2f→F, se2g→G, se2h→H, se2i→I.
- Dedup: identical (name,actual,expected) repeated across logs counts once;
  same name with conflicting values → DOES-NOT-MEET (conflict reported).
- Expected tallies: A32 / B18 / C20 / D48 / E24 / F2 / G2 / H4 / I5 = 155.
- Verdict: `MEETS-PROPOSED-BAR` iff every section's distinct passing-name
  count equals its expected count AND zero checks have actual≠expected AND
  zero conflicts. Else `DOES-NOT-MEET`. The reporter NEVER prints
  QUALIFIED (enforced by construction: the string does not appear in the
  script).

## 9. Independent verification protocol (per track: audio, vision)

Recorded in `VERIFICATION_PHASE2.md`; per-track verdict ENDORSED or
DISCREPANCY-found (with specifics):
1. Re-read their committed sources: real mechanisms, not stubs (stub
   signatures: canned returns ignoring inputs, unimplemented paths
   presented as passing).
2. Re-run their battery from their committed sources with the pinned znc;
   compare output to their committed logs (CL_CHECK lines identical;
   byte-identical stdout preferred).
3. Confirm their reported tallies match their logs (distinct se2a-/se2v-
   names, actual==expected on every line).
4. Run the §G scans over their sources (no banned constructs; no computed
   strength in any admit path they ship).
5. Confirm pure-Zag (no Python/shell in the mechanism path; runner scripts
   are harness, not mechanism).

If a track has not landed at report time, its section records NOT-LANDED —
verification pending, not endorsed.

## 10. Commit discipline

- Commit 1 (this prereg): freeze before any implementation.
- Commit 2: vendored sources + driver + scripts (no binaries, no
  `.zagd.semantic-ready`, no `.zag-cache/`, no regenerable `se2_store/`).
- Commit 3: evidence logs + `VERIFICATION_PHASE2.md`.
- `python3 ~/workspace/commit_to_branch.py tnn-native-lab <msgfile> <paths>`;
  verify commit hashes; report them.

## 11. What this does not claim

No live-sensor qualification, no S2 perception, no classifier admission, no
performance claims. Passing the cross-cutting sections establishes the
mechanical harness only; modality verdicts belong to the tracks and to
Micah's signature on the proposed bar.
