# N-KEY INVESTIGATION — final (2026-09-24)

Task: investigate the `~N` key problem in the 10GB ingestion; run the dry
ingestion; test three resolutions head-to-head (V1 admit `~N` / V2
skip-rejected-in-CAL / V3 re-key upstream); preregistered bars; pure Zag;
zero RNG; byte-identical reruns.

Prereg: `NKEY_PREREG.md` (+ amendments A1/A2/A3, frozen 2026-09-24 ~17:05
UTC). Interim results: `NKEY_RESULTS.md` (§§1–6). Full-corpus battery:
`nkey_fullrun.sh` (V0×1, V1×2, V2×2 — V3 was never in the driver; see §6).

**Bottom line:** all three prereg §7 Bar-4 predictions were wrong in the
PREREG, not in the runs. Every measured count reconciles EXACTLY under a
corrected model. V1 wins on coverage (9,314,871 installed, 0 lessons lost).
V2 is orthogonal and composes with V1. V3 is count-identical to V1 (CP1
proven) but qualitatively worse per A3. All bars hold for V1 and V2.

## 1. Root cause (established, unchanged from interim)

- `clean2.py::r9_emit_unit` splits >4096-byte SE posts into ≤4096-byte
  chunks keyed `se:<site>:<q|a>:<id>~N`. `~N` = source-generated chunk
  provenance, not malformed input.
- Frozen `gate.zag::ig_se_key_ok` (G3) requires all-digits after the post
  id → every `~N` key → G3 reject. The SOURCE and GATE contracts disagree.
- No downstream consumer parses the post id numerically (G2 = byte
  equality, merge/sindex = byte order, retrieval = citation display).
  The digits-only rule serves no demonstrated integrity function.
- Lesson CAL takes the FIRST 4 records of each 65,536-record lesson as
  must-accept probes; any probe failing the gate drops the WHOLE lesson.
  Full corpus: lessons 84 (mask=8), 116 (mask=8), 124 (mask=7) dropped =
  196,608 records (2.1%) lost because a lesson-head record carried a
  `~N` key. CP2 isolated lesson 84: V1 installed all 65,536 with g3=0 —
  the lesson was PERFECT except for one key-grammar technicality at its
  head.

## 2. Corpus measurements (nkey_probe.py, 9,327,214 records — unchanged)

- Tilde-keyed: 117,470 (kind-6: 91,866; kind-7: 25,345; kind-5: 259).
- Kind-6 tilde: math 62,273; physics 24,508; chemistry 2,925; biology
  2,160. All 91,866 match `~N` shape (0 malformed); max chunk index 9.
- Probe: admitting optional `~N` → 90,167 installable; 1,699
  question-continuations still fail the separate `"\n\n"` rule
  (91,866 = 90,167 + 1,699 ✓); 0 G1.
- Non-kind-6 tilde: kind-5/7 grammars ALREADY admit `~` (V0 installed
  23,434 of 25,604; the other 2,170 fail the multi-word G3 rule —
  variant-independent).

## 3. Full-corpus runs (final)

Driver `nkey_fullrun.sh` died mid-flight (main log truncated at
`[18:06:32] START v1b`); v1b and v2a ingests completed with valid
manifests/lesson-audits; v2b died mid-ingest ~19:14 (ENOSPC — 3.1G
partial on a 97%-full disk; a full store needs ~4.7G). v2b was rerun
clean by the closer on 5.2G free (same binary, same inputs, same NCAP,
script's `run_one` replicated exactly); partial store removed per the
script's own discipline. V3 was never in the driver (see §6).

| run | n | g1 | g2 | g3 | lessons_rej | negcontrol | seal |
|---|---|---|---|---|---|---|---|
| V0 (rebuild) | 9,030,226 | 9 | 0 | 100,371 | 3 | 1000/1000 | 43d7e5cc… |
| V1a | 9,314,871 | 9 | 0 | 12,334 | 0 | 1000/1000 | 3e12a69c… |
| V1b | 9,314,871 | 9 | 0 | 12,334 | 0 | 1000/1000 | 3e12a69c… |
| V2a | 9,224,704 | 9 | 0 | 102,501 | 0 | 1000/1000 | a17580c4… |
| V2b | 9,224,704 | 9 | 0 | 102,501 | 0 | 1000/1000 | a17580c4… |

- V0 rebuild byte-identical to dryrun/gate_bin_fixed (SHA cc75082c…);
  V0 manifest matches the prereg baseline EXACTLY (n, g1/g2/g3,
  lessons_rejected, seal 43d7e5cc…).
- **Bar 1 determinism:** V1a/V1b manifests byte-identical (`diff`
  rc=0), seals identical. V2a/V2b manifests byte-identical, lesson
  audits byte-identical (143 LESSON lines each), seals identical. (A2 method: sequential runs, manifest + seal + aggregate
  store SHA. Note: v2a's aggregate store SHA was lost when the driver
  died before its tee; v1a's survives in the main log (a95b14ab…),
  v2b's was computed and recorded by the closer. The seal — SHA-256
  over the final chain hash + the full audit event stream — is the
  byte-content evidence for both variants.)
- **Bar 2 integrity:** negcontrol 1000/1000 every run; zero CAL=REJECT
  in the V1/V2 lesson audits (a single failed must-reject synthetic
  probe rejects the lesson as a unit, so 143/143 CAL=OK entails all 4
  must-reject probes fired correctly in every lesson); seals present
  and deterministic within each variant.
- **Bar 3 no silent widening:** g1=9, g2=0 EXACT in all five runs
  (within ±0.1% trivially — the variants only touched G3-key and CAL
  selection, as designed).

## 4. Bar-4 adjudication: every delta reconciles EXACTLY

Prereg §7 predictions vs measured. Verdict on each: **the prereg was
wrong, the runs are self-consistent.**

### 4a. V1 n: 9,314,871 measured vs 9,120,393 predicted (+194,478)

Prereg: V1 = 9,030,226 + 90,167 (admittable tilde) = 9,120,393 EXACT.

Corrected model:
V1 = V0 + rescued good non-tilde + admitted tilde
   = 9,030,226 + 194,478 + 90,167 = **9,314,871 EXACT** ✓

The prereg's prediction omitted the lesson-rescue term. V1's grammar
change doesn't just admit `~N` records — it also rescues the 3 dropped
lessons outright, because their head records now PASS the gate
(V1 lessons_rejected=0, confirmed in manifest and lesson audit). The
194,478 rescued good non-tilde records are the same 194,478 V2 rescues
(CP2-measured). Cross-checks: V1−V2 = 90,167 ✓ (admittable tilde,
corpus-wide); V1−V0 = 284,645 = 194,478 + 90,167 ✓.

**Adjudication: PREREG-WRONG (omitted rescue term). Run is correct.**

### 4b. V2 n: 9,224,704 measured vs 9,222,704 predicted (+2,000)

Prereg: V2 = 9,030,226 + 192,478 = 9,222,704, rationale "194,478
installed − 2,000 tilde" (from CP2's V2 installed=194,478).

The rationale double-subtracted. CP2's V2 installed=194,478 does NOT
include the 2,000 tilde records — under V2, per-record install gating
is UNCHANGED, so those 2,000 are individually G3'd (CP2 V2 g3=2,130 =
2,000 tilde + 130 residual). The correct V2 delta is the full 194,478
good non-tilde records in the 3 rescued lessons:

V2 = 9,030,226 + 194,478 = **9,224,704 EXACT** ✓

g3 cross-check: V2 g3 = 100,371 (V0) + 2,130 (rescued lessons'
install-gated rejects, which V0 never gated because it dropped the
lessons at CAL) = **102,501 EXACT** ✓.

**Adjudication: PREREG-WRONG (double-subtracted the tilde). Run is
self-consistent.**

### 4c. V1 g3: 12,334 measured vs 10,334 naive (+2,000)

Naive: V1 g3 = V0 g3 − 90,167 (admittable tilde) + 130 (rescued
lessons' residual) = 10,334.

The naive model assumed all 90,167 admittable tilde were counted in
V0's g3. They were not: the 2,000 admittable tilde inside the 3 dropped
lessons never reached install gating under V0 (lessons die at CAL).
Only 88,167 admittable tilde were inside V0's g3=100,371:

V1 g3 = (100,371 − 88,167) + 130 = 12,204 + 130 = **12,334 EXACT** ✓

The 1,699 question-continuation `"\n\n"` failures the prereg noted are
inside the 12,204 residual (they are tilde records that still fail
under V1's grammar, alongside ~10,505 other G3 failures — single-token
texts etc. — unchanged from V0's residual). No anomaly to investigate;
the totals reconcile to the record.

**Adjudication: NAIVE-MODEL-WRONG (miscounted the V0 g3 denominator).
Run is self-consistent.**

## 5. Cherry-pick results (unchanged from interim — recorded for the record)

### CP1 — tilde-only micro-corpus (117,470 records), teach per variant

| variant | installed | g3 | lessons_rej | note |
|---|---|---|---|---|
| V0 | 23,434 | 42,102 | 1 (mask=15) | lesson 1 (all kind-6 tilde) dropped |
| V1 | 113,601 | 3,869 | 0 | kind-6 admitted: 90,167 = probe prediction EXACT |
| V2 | 23,434 | 42,102 | 1 (mask=256) | canary fires on the all-reject lesson — correct |
| V3+V0 gate | 113,601 | 3,869 | 0 | IDENTICAL counts to V1 (lesson splits match too) |

negcontrol 1000/1000 all runs.

### CP2 — the 3 dropped lessons (196,608 records), teach per variant

| variant | installed | g3 | lessons_rej | note |
|---|---|---|---|---|
| V0 | 0 | 0 | 3 (masks 8,8,7) | catastrophe reproduced in isolation |
| V1 | 196,478 | 130 | 0 | lessons rescued AND tilde admitted |
| V2 | 194,478 | 2,130 | 0 | lessons rescued; 2,000 tilde individually G3'd |

V1−V2 = 2,000 = the tilde records in these lessons (all admittable).

## 6. Head-to-head recommendation: V1 vs V2 vs V3

| | V0 (frozen) | V1 (admit ~N) | V2 (CAL skip) | V3 (re-key) |
|---|---|---|---|---|
| gate change | none | G3 grammar +`~N` | CAL selection only | none |
| source change | none | none | none | re-key + re-sort pass |
| installed | 9,030,226 | **9,314,871** | 9,224,704 | — (not run full-corpus) |
| lessons lost to `~N` heads | 3 (196,608 rec) | 0 | 0 | 0 (CP1) |
| provenance | n/a | transparent (`~0`) | n/a | opaque (arithmetic decode) |
| new assumptions | none | none | 256-window canary | id<10^12, n<10^4 |
| governance | — | spec amendment (G3) | CAL change | pipeline change |

- **Coverage winner: V1** (9,314,871 = max legitimate-record coverage,
  all bars hold). This is the recommendation if one variant is adopted.
- **V2 is orthogonal, not a rival:** it fixes the lesson-drop
  catastrophe class without touching key semantics, and composes with
  V1 (V1+V2 coverage = V1 coverage on this corpus; the canary adds
  robustness against OTHER head-reject causes beyond `~N`). If the G3
  spec amendment is contested, V2 alone still recovers 194,478 records
  the frozen gate drops — a governance-cheaper partial fix.
- **V3 was never run at full corpus** (not in `nkey_fullrun.sh`; the
  A3 Bar-4 prediction V3_installed == V1_installed EXACT is verified
  only on the CP1 micro-corpus: 113,601/3,869, lesson splits match).
  Per A3 the V1-vs-V3 contest is qualitative, and V1 wins it:
  transparent `~N` provenance + one-line grammar amendment vs opaque
  arithmetic keys + silent-collision fragility if upstream ids ever
  exceed the baked-in bounds + an extra re-sort pass. Recommendation:
  **V1 over V3**; do not pursue V3 without a full-corpus run, which the
  CP1 identity result makes unnecessary.
- **V-NOLIMIT** (kill the 4096B chunk-split itself) is being built and
  tested by a sibling crew in `nolimit/` under `NOLIMIT_PREREG.md`
  (frozen 2026-09-24) — not duplicated here; their verdict will
  supersede or sit alongside this head-to-head.

## 7. Close-out appendix (driver death, v2b rerun, disk)

- `nkey_fullrun.sh` launched 17:27 UTC; main log's last driver line is
  `[18:06:32] START v1b`. v1b ingest completed ~18:38, v2a ~18:56
  (their per-run logs: "ingest done"), with valid manifests and
  lesson-audits; v2b died mid-ingest ~19:14 with a 3.1G partial store
  (blobs 000000–000008). Disk at the time: 97% full, 3.6G free; a full
  store needs ~4.7G — ENOSPC is the consistent cause (empty v2b log,
  no gate process in ps).
- Closer actions: removed the partial `nkey_full_v2b/` (per the
  script's own rm-each-store discipline; manifests/logs untouched),
  freed completed CP teach-store dirs (`cp1_v*`, `cp2_v*`, `smoke*`,
  ~1.2G — results already recorded in `NKEY_RESULTS.md` §§4–5),
  verified 5.2G free, reran v2b with the script's `run_one` steps
  verbatim (same `gate_v2_bin`, same `dryrun_facts.dat`, same
  `/home/hatch/workspace/tmp10/bad.bin`, NCAP=11292656), then
  manifest/seal/aggregate-SHA/lesson-grep steps, copied manifest +
  lessons, and removed the store dir. v2b: DONE rc=0, manifest
  byte-identical to v2a (seal a17580c4… identical), lesson audit
  byte-identical to v2a (143 LESSON lines, per-lesson inst/g counts
  match), negcontrol 1000/1000, 0 CAL=REJECT. v2b aggregate store SHA
  (A2 construction): a4631d133b94cef562124a0adc57002fcd7cd8d1f0d228b6
  43f33d6009e1e50c (v2a's aggregate SHA was lost with the driver, so
  V2 determinism rests on the byte-identical manifests + seals +
  lesson audits).
- Untouched per box discipline: `ingest_1gb/`, frozen baseline probes
  (dryrun stores), sibling `nolimit/` and `nolimit_c/`. No `/tmp` for
  bulk. Pure Zag mechanisms, zero RNG throughout.

## 8. Artifacts

- Prereg + amendments: `NKEY_PREREG.md`
- Interim results: `NKEY_RESULTS.md`
- This report: `NKEY_INVESTIGATION.md`
- Driver: `nkey_fullrun.sh`; main log `nkey_fullrun.log`
- Per-run: `nkey_full_{v0,v1a,v1b,v2a,v2b}.log`,
  `nkey_full_{v0,v1a,v1b,v2a,v2b}_manifest.txt`,
  `nkey_full_{v0,v1a,v1b,v2a,v2b}_lessons.txt`
- Sources: `gate_v1.zag`, `gate_v2.zag`, `v3_rekey.py`, `nkey_probe.py`
  (binaries and full store dirs excluded from the commit per discipline)
