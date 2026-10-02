## 2026-09-27 ~12:02 PDT — P1 COMPLETE
- impl_p1/azgen_p1.zag: C3 + argv(3)=="force" pins PLANE everywhere; without flag byte-identical to C3.
- Determinism: bridge SHA fea34201b7821c0e… ×2 + env -i, identical.
- Force verified: 45/45 C3-PLANE bridge regions render byte-identical under P1.
- Sanity: bridge P1 19.86 (+0.12 vs C3 19.74); sky byte-identical to C3 (C3 chose PLANE 31/31 there).
- Early signal: deliberation premium ≈ 0 on bridge/sky — full battery adjudicates per prereg.
## 2026-09-27 ~12:03 PDT — SEALED COMPLETE: 10 images
- sealed/: 10 JPEGs (768px wide, PIL-LANCZOS downscale of Commons originals, q90), 1.2MB total.
- Categories: texture x2, smooth x2, people x1, object x2, animal x2, mixed x1.
- Licenses: CC BY 3.0 x1, CC BY-SA 3.0 x3, CC BY-SA 4.0 x5, CC0 x1. MANIFEST.json + SEALED_SHASUMS.txt.
- Exclusion check: 10 SHAs vs 14 exclusion SHAs — zero matches; subjects disjoint from exclusion list.
## 2026-09-27 ~12:04 PDT — P3 COMPLETE
- impl_p3/azgen_p3.zag (SHA b77fe3ee…): base=PLANE/MEAN ladder; op=3 PLANE+ATOM residual iff licensed AND sse_atom < sse_base on observed pixels (g_resid_check, exact integer arithmetic).
- Determinism: bridge SHA 937b7fdb… x2 + env -i identical.
- Sanity: bridge 19.63 (C3 19.74), sky 23.84 (C3 23.89). Residual path: 0/48 bridge (3 licensed, all 3 rejected by honest check), 0/31 sky.
- Positive control: synthetic indir → 4/4 op=3, Python oracle recomputed 12,288 pixels byte-exact. Render path verified.
- Early signal: on bridge/sky no atom earned its place on real pixels.
## 2026-09-27 ~12:05 PDT — P2 COMPLETE
- VOC3 dry-run PASS. VOC3 SHA e43cfebf… (VOC2 + 240-byte u8 src table, NULL->255). src: brick_wall 101, lake_water 132, foliage 2, stone_wall 0.
- azgen_p2.zag (SHA d1620a96…): pristine baseline + lineage restriction (si=0 full vocab; finer scales same-src only; NULL/empty -> full vocab).
- Determinism: bridge 655afed6… x3 identical. Baseline rebuild reproduces committed SHAs.
- Sanity: bridge 18.40 (-0.07), sky 22.75 (0.00). Restriction binds (128 restricted blocks bridge; output SHAs differ from baseline).
- Analysis mode: bridge plane-render 19.20 vs P2-atom 18.40 → +0.80 dB for planes on identical geometry (abandonment-bar input).
## 2026-09-27 ~12:06 PDT — P4 COMPLETE + BATTERY DISPATCHED
- impl_p4/azgen_p4.zag (SHA 8ed57695…): C1 gate byte-identical, unlicensed -> PLANE fallback. Licensed path verified (C1 vs P4 byte-identical outputs; gate licensed 0 takes on bridge/sky so fallback untested there — sealed battery is the real test).
- Sanity: P4 bridge 20.00 / sky 26.27 (== C1). Bicubic column (P4 crew, PIL): bridge 25.89, sky 33.20 — far above all arms.
- Battery crew dispatched: BAR 0 gate, 8 configs x dev(11) + 7 x sealed(10), bicubic column, 2x determinism + perturbation spot checks.
## 2026-09-27 ~12:25 PDT — BATTERY round 1 done; sealed_04 panic; REPAIR dispatched
- Round-1 battery: BAR 0 PASS, 151/151 determinism, 32/32 perturbations. Sealed_04 (768x576) panics frozen LINES code on all 7 sealed configs.
- 9-image readings: P1 within +/-0.10 of C3 (decorative/harmful); P2 abandonment bar FIRES (-0.654); floor clause violated by most arms (sealed_07 -0.99 etc.); PIL bicubic far above all arms on every image.
- Prereg has no panic clause; repair (capacity, not tuning) authorized per standing orders. Repair crew: diagnose OOB, identical fix in 6 sources, neutrality guard = byte-identical SHAs on all 11 dev images vs unrepaired, then full 10-image rerun + BAR 1 adjudication.
## 2026-09-27 ~13:05 PDT — REPAIR COMPLETE, BAR 1 adjudicated; red team + gallery dispatched
- Root cause: LINES take buffer hardcoded 16384 rows; sealed_04 needs 16847. Fix: w*h*7*8, identical in 6 sources. C1 untouched.
- Neutrality: 77/77 dev SHAs byte-identical vs unrepaired. Full rerun: 158/158 sha_match, 30/30 perturbations.
- BAR 1 (10 sealed): P2plane PASS (+0.539, 10/10, floor +0.00); C3/P1/P3/P4 FAIL (floor); P2 FAIL (mean -0.094).
- P2 abandonment bar FIRES (-0.633) — vocabulary retired as rendering; NOTE: P2plane's take GEOMETRY still vocabulary-decided.
- P1 reading: +0.080 within +/-0.10 -> deliberation decorative/harmful.
- Red team (5 attacks incl. R3 killer traps) + eyes gallery (5 texture images, data-URI) dispatched in parallel.
