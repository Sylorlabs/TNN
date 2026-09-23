# CAST AUDIT — lab-wide `as []i32 / []u32 / []u16` sweep (KB-AUDIT)

**Date:** 2026-09-21 (PDT) · **Crew:** CERTIFIER-REBUILD · **Scope:** `~/workspace/tnn-lab`, all `*.zag`, excluding `.zag-cache`
**Pattern:** `as []i32|as []u32|as []u16` (the ZNC-2026-09-21-007 trigger types; `as []i64`/`as []u64` probed clean)

## Real code hits (indexed tables through the trigger types)

| File | Hits | Consecutive same-size? | Indexed? | Blast radius / disposition |
|---|---|---|---|---|
| `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 30 | YES (multiple groups) | YES | **REBUILT by this crew** (`rngscan_v3_rb.zag`, u8 arenas + `t_put32`/`t_get32`) |
| `wave12/step1a-v2/thin-certifier/certifier/thincert.zag` | 9 | YES (multiple groups) | YES | **REBUILT by this crew** (`thincert_rb.zag`) |
| `wave12/step1a-v2/armc-rerun-2026-09-21/thincert/builds/certsrc/thincert.zag` | 9 | YES | YES | Byte-identical copy of the thincert source above — covered by the same rebuild |
| `wave12/step1a-v2/checker/rngscan_v2.zag` | 23 | YES — lines 613–617 (5× 512B), 824–830 (6× 256B after one 800004B), 831–837 (7× 2048B), 838–839 (2× 4B) | YES (all 23 tables indexed) | **LIVE PATTERN, NOT REBUILT.** This is the v2 checker kept as the *informational* `tripwire_v2` in thincert attestations. v2 was killed by its own red team and is not a gate; its tripwire readings are untrusted until rebuilt. Recommendation: rebuild with the same workaround or retire the tripwire — do not promote it. |
| `units/arms/V/cl/arm.zag` | 2 (lines 111, 224) | NO — both are single casts, no consecutive same-size partner | YES (`toks[i]`; `tokbuf` via `out:[]i32` param) | Not triggerable under the proven scope (single `as []i32` probed clean). Residual risk only if the bug's scope is wider than proven. Recommend converting to arenas on next touch. |

## Comment-only mentions (already on the workaround — no code change needed)

These files contain the pattern only inside `//` comments documenting ZNC-2026-09-21-007 and the arena convention:

- `units/teachers/harness/harness.zag` (the wave-12 teacher harness — its 33 former casts are already gone)
- `units/teachers/arm1/teacher.zag`, `units/teachers/arm3/varB/teacher.zag`, `units/teachers/arm3/varC/teacher.zag`
- `prose-learning/src/prose_learn.zag`, `prose-learning/v2/src/prose_learn2.zag`, `prose-learning/v3/src/prose_learn2.zag`, `prose-learning/v3/src/prose_learn3.zag` (+ docs copy at `docs/lab/prose-learning/v3/src/prose_learn3.zag`)
- `senses/rebuild/a_raw/sense.zag`, `htd-1/builds/comp/comp.zag`, `dialogue/dialogue.zag`
- `units/arms/T/work/bbattery/batt.zag` (comment says "never `as []i32`")

## Audit conclusion

Every live instance of the trigger pattern in certification/gate code is now rebuilt (v3 checker, thin certifier). The one remaining live instance with the full trigger shape is the **retired v2 checker's informational tripwire** — flagged, not a gate. Two single-cast instances in `arm.zag` are outside the proven trigger scope. No `as []u32` / `as []u16` indexed tables exist anywhere in the lab.
