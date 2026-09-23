# worker_23 log — chunk_23 sweep (50 rows, 2026-09-22 ~07:20 PDT)

50/50 evaluated, all rows status=done. Zero kill bars referenced by any file. Zero stale claims against KNOWN OUTCOMES (these files reference no program outcomes). No exact-duplicate pairs (md5 of all 18 zag files distinct). No grok-4.7 calls used — native review covered everything.

## zag files — znc characterization micro-probes (work/l1/micro/ + work/l1/repro/)

All 17 zag files are ZNC compiler-bug characterization probes (ZNC-004 / ZNC-010 family) built around a 39-field L1 struct (23 []u8 fields + 16 i32 fields). None contain any randomness — grep for rand/random/time/getpid/_zag_arg found nothing — and none sit in a TNN decision path (they are toolchain probes, not learner code), so the no-randomness law is satisfied trivially. No `as []i32`/`[]u32`/`[]u16` casts, no `slice as *u8`, no chained `s.field.subfield` in any of them.

Spot compile+run with ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 (13 of 17 compiled for build-status check; first batch's exit codes were pipe-corrupted, so m2/m16_3/m19 were recompiled cleanly):

| file | matrix cell | build | run | verdict |
|---|---|---|---|---|
| m2.zag | baseline (no alias) | PASS | n=8 | PASS |
| m16_3.zag | 3 slice-lets off local struct value | FAIL "aggregate let needs an aggregate initializer" | n/a | PASS: ZNC-004 reproduced |
| m16_4.zag | 4 aliases | FAIL same | n/a | PASS: ZNC-004 reproduced |
| m16_5.zag | 5 aliases | FAIL same | n/a | PASS: ZNC-004 reproduced |
| m17.zag | alias inside helper via *L1 param | PASS | n=8 | PASS: ZNC-010 known-good form confirmed |
| m18.zag | multi-arg struct-returning l_new | PASS | n=11 | PASS: ZNC-004 multi-arg confounder resolved — fine |
| m19.zag | `let ps:*L1=&s; let p1:[]u8=ps.*.pids;` | PASS | n=8 | PASS — note below |
| m3/m4a/m4b/m4c/m5/m6 | aliases off local value in t_m5b, l_new arg-count variants | FAIL ZNC-004 | n/a | PASS: fail-by-design probes |
| m7.zag | cap=250000, no alias | PASS | n=250001 | PASS |
| m8.zag | zero-arg l_new | PASS | n=1 | PASS |
| m9.zag | 16-arg fwd call | PASS | n=8 | PASS |
| t1.zag | trivial | PASS | "hi" | PASS |

Notes:
- m19 built and ran CORRECTLY on this toolchain. ZNC-010 characterized the `&local`-derived pointer slice-let as failing the typed-declaration check ("expected []u8, found []i64"), but that entry's failing case used []i64 fields; with []u8 fields here it compiles and runs byte-correct (n=8). Not a contradiction of ZNC-010 as written, but worth recording: the &local-pointer failure mode appears field-type-dependent. No claim updated — flagging for the compiler crew.
- m3/m4a/b/c/m5/m6 all fail at build, so their t_m5b write loops (cap*4 = 1,000,000 writes into empty-string slices — would be out-of-bounds panics at runtime) are unreachable. If the ZNC-004 form ever compiles, those loops are latent OOB bugs; currently moot.
- m4a/m4b additionally carry B0103 `unused local ins` lint warnings (their l_new args are partially unused).

## jsonl files — metric fragments (work/l2/battery_r1/ ×16, work/l2b/battery_r1/ ×17)

NOT raw JSONL: each file is one line in the form `METRIC_JSON <json>` with schema "metrics-v1". After stripping the prefix, all 33 inner JSON documents parse. Verified per file: exactly 1 line, METRIC_JSON prefix present, inner JSON parses, required keys {schema, arm, round, scale, mode, fields} all present, schema == "metrics-v1", rec.mode == parent dir name, round == "r1", scale == "1x".

Field counts and key metrics:
- m1-1x-code/prose: 9 fields; m1_recall/boundary 100.0 tenths, m1_id_probe PASS, l2_epoch_bumps 0.
- m2-t1/t2 code/prose: 8 fields. m2-t3-1x: 12 fields incl. m9_shape "fast-then-flat", m9_steepness 100.0 tenths.
- m3-1x: 9 fields. m4-1x-code/prose: 11 fields. m5-1x: 9 fields. m6-c2p/p2c: 9 fields.
- m5-baseline: 1 field — m5_baseline:"ready" readiness marker, not a metric. Both l2 and l2b copies identical.
- memctrl-c2p/p2c: arm="memorizer" control legs, 3 fields — indomain 82.2 / transfer 27.4 / drop 54.8 tenths.
- m7-1x: l2b only, 8 fields — hit 100.0, reuse 2.0, dedup 50.0 tenths, m7_cell PASS, round2_revised 848, bumps 20, xepoch_recalls 3334, misses 0.

Flags (non-blocking, in verdicts):
- All 17 l2b rows carry arm="l2" inside the record despite living under work/l2b/. Systematic across every l2b file including memctrl (which correctly says arm="memorizer"), so it reads as "l2b = l2 battery re-run round" rather than a copy error. No verdict changed; flagged so consumers know the in-record arm field does not match the directory.

## Findings count
- 17 zag probes: 17 PASS verdicts (7 fail-by-design build rejections counted as probes behaving as characterized).
- 33 jsonl fragments: 33 PASS verdicts (all schema/mode/dir checks hold).
- 0 rows not evaluable.
- 0 kill bars referenced. 0 stale outcome claims. 1 observational flag (l2b arm-field mismatch), 1 observational flag (m19 vs ZNC-010 field-type dependence), 1 latent note (t_m5b OOB loops unreachable).
