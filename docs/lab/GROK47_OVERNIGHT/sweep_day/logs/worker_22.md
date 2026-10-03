# worker_22 log — chunk_22 sweep (50 rows)
Date: 2026-09-22. Method: native review; znc spot-compiles (pinned toolchain), python JSON parse, byte-diff; no grok-4.7 calls (all evaluable natively).

## Group 1: jsonl fragments (34 rows)

### battery1x (v1) — 11 non-empty parse as single METRIC_JSON line, schema "metrics-v1"
- m1-1x-code: PASS. recall 100.0, boundary 100.0, 148678 code units, id probe PASS.
- m1-1x-prose: PASS. recall 100.0, boundary 100.0, 84731 prose units, id probe PASS.
- m3-1x: PASS. freeze FROZEN-UNDER-PRESSURE, fresh recall 100.0, 9067 mgmt entries, weaken_handled 0, valuable 1000.
- m4-1x-code / m4-1x-prose: PASS. rev boundary/content 100.0, kill_rate 0.0, killsub false → no kill-bar trip.
- m5-1x: PASS. spent 233409 < budget 298761, store_fail 0, recall_fail 0 (500 probes), slot_table 12452292B, content 14938062B.
- m5-baseline: PASS. 1168 ns/log.
- memctrl-c2p-1x: PASS. memorizer control: in-domain 27.4, transfer 82.2, drop -54.8. NOTE the asymmetry (transfer > in-domain) — control-baseline data point, not a claim; no bar.
- memctrl-p2c-1x: PASS. in-domain 82.2, transfer 27.4, drop 54.8 (mirror of c2p).

### battery1x (v1) — 8 empty (0 bytes), not evaluable
m2-t1-code, m2-t1-prose, m2-t2-code, m2-t2-prose, m2-t3-1x, m6-c2p-1x, m6-p2c-1x, m7-1x (8 rows, all size 0). v1 battery produced no outputs for M2/M6/M7 legs; v2 fills all of them. Verdict "review: 0-byte fragment".

### battery1x_v2 — 7 byte-identical to v1 → dup
m1-1x-code, m1-1x-prose, m3-1x, m4-1x-code, m4-1x-prose, memctrl-c2p-1x, memctrl-p2c-1x — byte-identical (cmp) to v1 counterparts; verdict dup:<v1 path>. v1 taken as canonical (older name).

### battery1x_v2 — 8 distinct, all parse, PASS
- m2-t1-code/prose, m2-t2-code/prose: episodes 1, censored false, ep0 0.0 → final recall/boundary 100.0.
- m2-t3-1x: same + m9 curve fields: shape fast-then-flat, takeoff ep 1, steepness 100.0, late gain 0.0.
- m5-1x: extended vs v1 (budget 238077, slot_table 12531232, units_learned 233409, ledger_bytes 14939200, ledger_entries 233425, corpus_buffer 14938062); within budget, 0 fails.
- m5-baseline: baseline ready, cap 308145, baseline_ledger_bytes 15514176 (v1 fragment was the 127B stub).
- m6-c2p-1x: 200/200 kill probes blocked, leak 0, phaseA/B 99.8, rev 100.0, tax 100.0.
- m6-p2c-1x: same, phaseA/B 99.7.
- m7-1x: hit 100.0, reuse 3.05%, dedup 50.00%, cell PASS, round2 revised 848.

## Group 2: zag files (16 rows)

### R33_NATIVE_SHA256_V2.zag (b3c substrate) — PASS
- `znc check`: "OK — all capability claims proven" (1 analyzer note, benign).
- RFC6234 constants loaded from hex-text literals via ns_load_words with length checks (not magic arrays). No RNG anywhere. No `as []i32/[]u32/[]u16` casts, no `slice as *u8`, no annotated slice-let off a local struct. Uses `_zag_malloc(N) as *i64` + `[0..N]` slicing (pointer, not the ZNC-007 aliasing pattern).

### b5b_1 / b5b_2 / b5b_3.zag — L1 arm ("Absolute position IDs") trial binaries
- Header: one binary, argv[1] selects mode (ARM_INTERFACE.md §3); zero-RNG claim verified — grep found only benign "rng" hits: line-6 comment + `rng:[]u8=s.*.r_new_seg` variable name + the CONFLICT NOTE about the brief's random-ID mention.
- CONFLICT NOTE (lines 8–16): crew logged per RULE-9 that the task brief's L1 description (random-ID control, BPE-native, M5 tax) does not exist in frozen PREREG_FREEZE.md §3 / ALPHABET_G-L.md / briefs/L1.json; built the frozen L1 literally. Proper procedure — no stale-claim flag on the file itself (it self-reports).
- Frozen §3 kill criteria referenced in comments: (i) 3x-K1 store cost, (ii) position-ID eternity, (iii) fragmentation. These are source-level references only — nothing to evaluate mechanically from source (no verdict numbers embedded); no kill bar trips.
- Miscompile patterns: zero `as []i32`/`[]u32`/`[]u16` casts; zero `as *u8` reads; zero chained `s.field.subfield`; all 30–32 annotated slice-lets alias through `.*.` of *L1 fn params (the proven-good pattern). BUT t_m8 (and t_m1/t_m5/t_m6 families) create `let s:L1=l_new();` LOCALS and then do annotated slice-lets touching them.
- SPOT BUILD of b5b_3: FAILS — "error in t_m8 (line 1566): native: aggregate let needs an aggregate initializer". Root cause identified: line 1740 `let chain2:[]u8=halloc(&s,((s.led_n+1048575)/1048576+1)*32);` — annotated slice-let off a LOCAL L1 value (ZNC-004/010 class: scalar-on-local is legal per ZNC-004, but the enclosing annotated-let with `&s` + `s.led_n` fails). b5b_1 line 1737 and b5b_2 line 1745 have the identical line. This is a KNOWN compiler-bug class, not a TNN mechanism flaw — the source pattern matches the characterized bugs exactly.
- Near-duplicates: md5 all differ; diffs vs b5b_1 confined to the CUT region (~line 1340): b5b_2 adds a zero-fill block, b5b_3 adds CUT3 print. These are bisection artifacts, not independent builds.
- Remediation note (for parent): the fix per AGENTS.md ZNC-010 is to hoist the local-field read out of the annotated let (e.g. `let ln:i32=s.led_n;` then `let chain2:[]u8=halloc(&s,((ln+1048575)/1048576+1)*32);`) or move the block into a helper taking `*L1`.

### bisect_A / bisect_B / bisect_C.zag — L1-arm bisection variants
- SPOT BUILD of bisect_A: FAILS — "error in t_m5b (line 1334)" and "error in t_m6 (line 1375)": same ZNC-004/010 class. t_m5b CUT block line 1340: `let s:L1=l_new(); l_init(&s,...); let p1:[]u8=s.*.pids; ... p8` — aliasing fields of a LOCAL L1 value, exactly the m16-series bug shape.
- bisect_B / bisect_C: same t_m5b CUT block at ~1340 (verified textually); differ from b5b_1 by ~142/~130 diff-lines at the CUT region; do NOT contain the chain2 line. Not separately compile-checked (same proven class).
- Zero RNG in decision paths in all three.

### micro/m1..m16_2.zag — compiler-characterization reproducers
- m1: PASS. Builds and RUNS (n=8 = cap 7 + 1). Struct forward-ref probe. 1 analyzer warning (string buffer not freed — benign for probe).
- m10: PASS as negative probe. `fn mkbuf(s:*L1,n:i32) []u8 { let b:[]u8=s.*.a; ...` — field `a` does not exist in L1; fails with misattributed "aggregate let needs an aggregate initializer" (intentional negative case).
- m11: PASS as negative probe variant (alias-in-helper, nonexistent `a`).
- m12: PASS as negative probe (local-value `s.*.a`, nonexistent `a`).
- m13: PASS. Aliases valid field pids through *L1 param (the legal pattern the big files' helpers use).
- m14: PASS. Scalar-field-on-local (`s.led_n`) — the legal-per-ZNC-004 pattern that b5b t_m8's chain2 line nests inside an annotated let.
- m15: PASS. 8-way alias storm on local L1 value (`s.*.pids` ×8) — stress variant of the bug shape.
- m16_1: PASS as reproducer. Single `let p1:[]u8=s.*.pids;` on local → build fails "aggregate let needs an aggregate initializer" — reproduces known ZNC-004/010 as expected.
- m16_2: PASS. Double-alias variant (p1,p2), same class.

## Kill bars
No file referenced a preregistered kill bar with an evaluable triggering condition. m4 fragments (kill_rate 0.0, killsub false) show no trip. The frozen §3 kill criteria cited in b5b headers are arm-level criteria, not numerically present in these files.

## Findings (for parent)
1. KNOWN-BUG CONFIRMATION (no new bug): b5b_1/2/3 and bisect_A/B/C all fail native compile on the ZNC-004/010 "aggregate let needs an aggregate initializer" class — trigger is annotated slice-lets aliasing fields of a LOCAL L1 struct value (t_m8 chain2 line in b5b_3 at 1740; t_m5b CUT block at ~1340 in bisect_*). Micro probes m1–m16_2 are the bisection evidence set; m16_1/m10 reproduced the exact error on this toolchain. Remediation = hoist scalar reads out of annotated lets or move aliasing into *L1-param helpers.
2. Zero RNG found in any decision path across all 16 zag files (all "rand" hits benign: comments, CONFLICT NOTE, or variable name `rng` = r_new_seg slice).
3. No ZNC-007 (consecutive same-size `as []i32/[]u32/[]u16`) casts, no `slice as *u8`, no chained `s.field.subfield` in any big file.
4. Duplicate fragments: 7 v2 fragments byte-identical to v1 (dups logged with canonical v1 paths).
5. 8 v1 fragments are 0 bytes (M2/M6/M7 legs never emitted in v1; v2 fills them) — not evaluable as results.
6. memctrl asymmetry: memorizer control c2p shows transfer (82.2) > in-domain (27.4); p2c is the mirror. Control data, not a claim; flagged as observation only.
7. No stale claims; b5b headers self-document their CONFLICT NOTE per RULE-9.
8. m10/m11/m12/m16_1/m16_2 intentionally fail compile (negative probes) — not a defect of the repo.
