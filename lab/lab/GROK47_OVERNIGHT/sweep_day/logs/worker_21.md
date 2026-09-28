# Sweep worker_21 log — chunk_21 (50 rows)

**Date:** 2026-09-22 (PDT) · **Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Rows:** 50/50 done. **Verdicts:** PASS 30, review 11, dup 9. No randomness found in any TNN decision path. No kill bars tripped.

## Method
- All 27 .zag files: grep-scanned for randomness tokens, ZNC-007 (`as []i32/u32/u16` — zero hits anywhere), ZNC-002 (`slice as *u8` — only malloc-result casts in R33_NATIVE_IO_V1, which are raw-pointer casts, not the bug pattern), chained `s.field.subfield` (arm.zag uses `s.*.pids` off a *Tw param — the ZNC-010-safe form).
- Spot compile checks: `cl/common.zag` (impl), `main.zag` (impl, pulls all 9 organ modules), `trust_tiers.zag` (68KB), `work/l1/b3b/cl/arm.zag` (69KB). All compile; warnings only (benign analyzer leak/ignored-return notes; E0102 multiply-by-0 in trust_tiers.zag:510,738 is cosmetic `0*32+slot` source-0 indexing, not a bug).
- Replicated check_c5redesign.py's static-scan logic (checks 7–8) on impl sources: 0 RNG hits, exactly 1 `o4_compose` call site inside `seam4_compose` (G0b). All three .py files py_compile clean; not executed (evidence dirs / GitHub writes would be needed).
- SHA-verified every substrate file against RUN_REPORT's final-binary manifest: all match (trust_tiers.zag `9e95d533`, st_memory_core `474ac0bb`, common `8aec83cb`, IO `e6379ddb`, SHA `9824f6db`).

## Findings (7 notes, none blocking)

1. **Byte-identical substrate twins (dup verdicts):** impl/substrate ↔ trust-tiers/substrate R33 IO, R33 SHA256, cl/common are byte-identical (SHAs above). No git repo present locally, so "already-committed" status could not be verified; flagged as dup against each other with SHAs so the parent can dedupe at merge.
2. **arm-battery substrate variants differ from wave9 copies:** b3/b3b/b3c `R33_NATIVE_IO_V1.zag` (sha `c39bfaf6`) and `R33_NATIVE_SHA256_V2.zag` (sha `87bd3ede`) differ from the wave9 copies — same filename, different content; intentional arm-battery variants, not corruption.
3. **Dead debug stubs in arm.zag:** `t_m5b` in b3/b3b/b3c returns immediately after printing CUT1/CUT2/CUT3 markers. b3b added an explicit zero-init loop before the marker; b3c dropped it back. Dead code in all three — no behavioral difference (function does nothing), but the stubs are leftover scaffolding worth cleaning.
4. **L1 conflict note is healthy process:** b3/b3b/b3c arm.zag headers document a crew-brief vs frozen-prereg conflict (random-ID-control/BPE-native/M5-tax kill criterion absent from frozen §3) resolved per RULE-9 with the frozen prereg winning. Documented, not hidden.
5. **Minor reporting arithmetic in trust-tiers RESULTS.md:** headline "paired byte-identity 792+12+216 cells ×2" omits the 108 gate pairs (CHECK_REPORT §0 covers the full 1128); ST_AUDIT monotonicity reported on 1008 logs; M1 latency "3/5/8 by T0-lag variant (2/5/8)" off-by-one at lag 2. Numbers internally consistent, headline presentation slightly loose.
6. **Honest checker artifacts in CHECK_REPORT_REDESIGN.md:** §11 M1 latency grep hit `evidence/s1/` instead of `evidence/mm/` (n=0/−nan, openly visible in output); §7 vs §14 N0-flagged counts differ by metric definition; A.10 in the prose report openly discloses the checker's fixed-seed `shuf` spot-check. All visible, verdict-unaffecting.
7. **BUILD_NOTES quirk #2 is pre-amendment smoke note:** "A5/T corrupts LOUDLY (needs verification)" is the pre-redesign observation — answered by the amended rerun (A5/T 36/36 held). Not stale; it's the evidence trail that led to REDESIGN. Quirk #1 (TT_RING≥356 znc slice-index panic, 355 bisected-safe) is a real toolchain quirk worth keeping.

## Kill bars (all applied mechanically, all silent)
- Trust-tiers §8 bars: per CHECK_REPORT — SRR 93.75% ≥90%, SRR A1–A6 91.7% (at the amendment's honest 91.7% ceiling), A1/A1-MS 100%, FCR 0%, zero silent corruption, BLIND 0 observable, denial 0% ≤5%, genuine-flagged 0/36 ≤10% (attack-free baseline, A.7), A6 maxstr 50 <80, ledger/determinism clean → NO §8 TRIGGER → NOT RETIRED. (Prior REDESIGN verdict preserved in CHECK_REPORT_REDESIGN_PROSE.md.)
- Position-brief falsification bars: no trial rerun exists for INT-1 C5 redesign; briefs' bars are prospective. Nothing to trip.
- No file contradicted KNOWN OUTCOMES (MA3→MA4 lesson, teacher championship source-independence, strength ruling-1, RC1 40/40, swe banned, hy3 dropped, GLM forgotten, LH LCG remediated).

## Not evaluable
- Full execution of any checker/run script (evidence dirs + GitHub writes out of scope for this worker).
- Exact duplicate-of-committed determination: no local git repo (`git ls-files` fails, not a repo); dup verdicts keyed on byte-identity within the tree with SHAs.

## Output files
- `GROK47_OVERNIGHT/sweep_day/fragments/worker_21.tsv` — 50 rows, status=done
