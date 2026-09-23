# worker_01 — chunk_01 manifest sweep log

Worker: cb4ba97b chunk_01 crew. Date 2026-09-22. 50/50 rows evaluated, all evaluable (no skips).
Tooling: pinned `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` for spot compiles;
python3 self-tests for scoring/audit scripts. grok-4.7: not used (native review sufficed).
No commits, no cron, no external contact.

## Kill bars applied mechanically (per file)

| File (arm) | Bar | Measured | Verdict |
|---|---|---|---|
| E/VERDICT.md | stored-bytes ≥2× B-64 at equal M1 (10x) | 2.764×, M1 equal both corpora | FIRES → KILLED ✓ |
| I2/VERDICT.md | record savings <10% OR arbitration error >10% | savings 75.5% PASS; error 55.9% >10% | FIRES (cond 2) → KILLED ✓ |
| K2/VERDICT.md | chain >4 on any corpus run | max chain 1, collisions 0 | no fire → PASS ✓ |
| M/VERDICT.md | merge remap ≥1 bad pointer OR compute >10%; M7 dedup <0.4 | 39.14% >10% (0 bad pointers); dedup 0.00 | FIRES scoped-KILL; M-dedup sub-claim SUPERSEDED (see finding F3) |
| M2/VERDICT.md + DEATH_CERTIFICATE.md | leaf-edit >25% stale OR recompute >10% of recall (10x) | K1 0.003% PASS; K2 26.8/28.8% >10% (10x A/B) | FIRES (K2) → KILLED ✓ |
| P/VERDICT.md | margin <3 pts OR churn >50% | 53.4 pts ≥3; churn 42/90=46.7% <50% | no fire → PASS ✓ |
| R2/VERDICT.md | not beating R by ≥3 (M1) OR ratio doesn't fall | margin 0.0 <3 (ceiling tie); ratio falls both corpora | FIRES (a) → KILLED ✓ |
| Z3/VERDICT.md | cost not ≥20% below best fixed OR half-B drop >15% | 0.6317 ≤0.80; drop 0% | no fire → SURVIVE ✓ |
| B-8/VERDICT.md | size retires on strict M1/M2/M3 dominance; family killed on ≥2× M3 | B-16/B-64 strictly dominate B-8 | B-8 RETIRES; family survives (2× bar arithmetically unreachable at M3 ceiling — flagged to Micah) |
| B-T1 (stage/CLOSEOUT_ADDENDUM.md) | surprise > fw4 > raw_micro AND raw_micro dead last | order holds; raw_micro rank 7/10 | FAILS dead-last → B-T1 FAIL (matches known outcome) |

## Findings (12)

- **F1 — prose_learn3.zag analyzer A0101 (benign).** Off-by-one warning on `while(k2<=le)` at main; read the code: `tb[k2]` is only indexed in the `k2<le` branch, so the warning is a false positive. Binary compiled clean (228KB). Zero RNG; ZNC-007 workaround applied ([]u8 arenas, no `as []i32` casts anywhere).
- **F2 — stale paths in E docs.** ARM_SPEC.md §6 and BUILD_LOG.md reference `~/workspace/docs/lab/units/arms/E/`; canonical is `~/workspace/tnn-lab/docs/lab/units/arms/E/`. Cosmetic; content verified fine.
- **F3 — M/VERDICT.md STALE on M-dedup.** Local copy: "M-dedup claim dies (dedup_barred=0.00 <0.4)". Night-run spot-check (10:20 PDT) found the 0.00 was invalid — dedup path was compiled out (`if(false && ...)` in the evidence binary) — and a corrected evaluation gives dedup_barred 50.01 ≥0.4; coordinator ruling at 17:10 UTC: "M-dedup death superseded (50.01 ≥ 0.4 survives)". DOCUMENTATION_AUDIT notes the repo carries the corrected M-dedup result; the local copy predates the ruling. Headline scoped-KILL (39.14% >10%) unaffected — spot-check reran it byte-identical.
- **F4 — candidate NEW znc bug in M/ARM_SPEC.md §6.** FNV hash accelerator panics with a computed table index but runs with a constant index; labeled "multi-parameter corruption, ZNC-2026-09-21-007 extended". No minimal reproducer exists yet — flagged as needs-reproducer, not yet a numbered ZNC issue. (AGENTS.md §ZNC-2026-09-21-007 lists scope; this would extend it.)
- **F5 — bt1_rank.py line 44 display bug.** `"vocab_probed_code": prose["vocab_probed"]` should read `code["vocab_probed"]`. Display-only: tournament score, ranks, and binding verdict use `capability_composite` only. Self-test on synthetic per-(arm,corpus) JSONs: ranker emits correct PASS/ranks. Self-test on synthetic corpus+SEG: scorer rc=0, two runs byte-identical, composite sane, asserts gate corrupt tilings.
- **F6 — Z3 comparator-cost evidence gap (not verdict-flipping).** Spot-check found: raw logs for b64/b16/b8 total-cost comparators not preserved; `scorecard_raw_shared.json` mislabeled "b64" but holds Z3's own numbers. First-principles sanity check supports asserted b64 (≈14.16M vs 14.34M); flipping prong 1 would need b64 ≤ 11.32M — implausible. Conclusion robust; verdict stands.
- **F7 — new-mechanisms prereg typo (mechanical).** audit_batteries.py confirms construction table lists kind-5 n=24, but kill bar and N=264 total force kind-5=12 (96+36+36+24+24+12+24+12). Verdict numbers use 12 (correct); '24' is a doc typo.
- **F8 — audit_batteries.py wording nit.** Per-conflict line prints "max score 35/36" per pair; BATTERY_HEALTH_AUDIT.md correctly reports the combined max 34/36 (two pairs). Finding itself (CONFIRMED) unaffected.
- **F9 — top-level `scratch/b_t1_closeout/CLOSEOUT_ADDENDUM.md` is a stale draft.** Claims binding bar PASS with "[FILLED AFTER SCORING]" rank table; superseded by `stage/CLOSEOUT_ADDENDUM.md` FAIL (measured rank_table.json: binding_verdict FAIL, raw_micro rank 6/9, dead_last_ok false). Known outcome "B-T1 FAIL stands (artifact-driven, XOR L=7 annihilator)" matches the stage version.
- **F10 — `stage/VERDICT_SHEET.md` is stale.** The 2026-09-21 01:42 PASS sheet's numbers (e.g. 0.6843/0.5995) were not reproduced by the closeout (measured 0.9558/0.8968); provenance unestablished; addendum treats it as unverified claim.
- **F11 — GROUNDED_BUG.md duplicated.** `scratch/b_t1_closeout/GROUNDED_BUG.md` is byte-identical to `stage/GROUNDED_BUG.md` (verified via diff). Finding itself valid: G=min(C,8192) allocation vs candidate indices ge∈[0,C) → heap overflow on inputs >~80KB; grounded_adaptive_mdl excluded from scoring, reported not fixed (no-tune rule).
- **F12 — Z3 BUILD_LOG leg-count wording.** "run_battery.sh (17 legs × 2 runs...)" vs VERDICT's 18/18: first scored run was 17/18 (m2-t2-prose ledger-oversize failure), second scored run 18/18 after the fix. Wording ambiguous but evidence trail resolves it; no inconsistency.

## Per-file notes (condensed)

- prose-learning/v3/src/* (R33_NATIVE_SHA256_V2.zag, prose_learn3.zag, oracle3.py): pure Zag, zero RNG, compiles with pinned toolchain; oracle is deterministic Python cross-check; header contracts (m0/m1/m2, byte-identical run log) documented.
- redteam/battery-design/*: all four claims re-run mechanically (A1 confirmed 2 conflicting pairs; A2 non-issue 50/31; A4 sol corpus 240/240 distinct; A6 envelopes frozen-by-design; kind-5 typo; Sol #1 bat_kind coupling confirmed in code).
- B-8/{AMBIGUITIES-B8,VERDICT}.md: internally consistent; ambiguity A-B8-1 adjudicated on rebuilt evidence (M3 byte-identical); family-kill-bar wording flagged to Micah.
- E/*: KILLED verdict derives cleanly; metric-reading (ledger excluded per prereg §5 M5) disclosed.
- I2/*: KILLED via arbitration error 55.9%; savings 75.5% preserved as evidence; build fixes honest.
- K2/*: PASS; audit-layout fix in BUILD_LOG matches frozen 16-word layout (stage@52, d1@56, d2@60); known limitation #3 (incomplete true-collision chain search) flagged openly.
- M/*: headline scoped-KILL confirmed; F3/F4 above; M4-revision-semantics ambiguity logged, not silently resolved.
- M2/*: KILLED by K2 on 10x double runs; DEATH_CERTIFICATE present; m7-1x pending after accidental kill disclosed.
- P/*: PASS; binding-trial methodology (200-unit subset, LRU eviction, 0/500 baseline vs 267/500 emergent) disclosed with limitations; M5 timeout honest.
- R2/*: KILLED on ceiling-effect tie (mirrors R's own death); hybrid operationalization change from 64B-block (degenerate: 0 proposals) documented with validation; corpus drift note (5,638,480B prose, units 11,871→13,970) disclosed, kill-relevant metrics unchanged.
- Z3/*: SURVIVE; A-53 reward-signal exclusion stated pre-battery in spec §2; F6 evidence gap; 8 implementation fixes parameter-preserving.
- history/*: DO_NOT_REPEAT.md + WHAT_TNN_IS_NOT.md consistent with known outcomes incl. R34 LCG contamination notice/quarantine.
- ops/*: DOCUMENTATION_AUDIT + MORNING_BRIEF consistent (B-T1 FAIL 7/10, Arm C/Track 5/rulings sign-offs pending, ZNC-005..012). NIGHT_RUN coherent; spot-check section also independently re-verified E/I2/K2/M/M2/P/Z3 kill logic (6 confirmed; M partial → F3; Z3 evidence gap → F6).
- scratch/b_t1_closeout/*: F9/F10/F11 above; stage/ dir is the authoritative closeout (rank_table.json on disk, binding_verdict FAIL); readback_mdl.py is the independent MDL reimplementation (12/12 per closeout log); PROBE_MANIFEST documents Python-scorer scope as measurement harness.

## Zag miscompile-pattern sweep (prose-learning/v3 sources)

- Randomness in TNN decision paths: NONE (grep + compile clean).
- ZNC-007 (`as []i32/[]u32/[]u16` consecutive-cast aliasing): NONE — file uses []u8 arenas with explicit put/get32 per the documented workaround.
- ZNC-004 (annotated slice-let off local struct value): NONE found.
- `slice as *u8` garbage reads: NONE.
- Chained `s.field.subfield` through pointer-in-struct-field: NONE.
- Spot compiles: R33_NATIVE_SHA256_V2.zag (lib, no main — expected), prose_learn3.zag → 228KB binary, warnings only.

## Open items for parent/coordinator

1. F3: confirm the corrected M/VERDICT.md (M-dedup supersede) is the committed repo version; decide whether the "corrected evaluation" 50.01 run evidence is preserved anywhere.
2. F4: decide whether the M-crew's suspected multi-parameter znc bug gets a minimal reproducer and a ZNC number.
3. F6: Z3 comparator raw logs — accepted as robust-per-spot-check, or request raw-log preservation?
4. F12-type wording cleanups and F2 stale paths are minor; F5/F7/F8 are one-line fixes any crew can apply.
