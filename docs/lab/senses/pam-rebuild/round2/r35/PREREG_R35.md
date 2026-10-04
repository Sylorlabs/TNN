# PREREG_R35 — Repair: full-64-bit capability tag binding for H-PAM-35 vs J-35

**Crew:** R-35 (PAM round-2 swarm, repair crew)
**Date:** 2026-09-24
**Status:** FROZEN (committed alone before code; this document governs the repair battery)

## §1. Target and kill being repaired

H-PAM-35 (capability-typed inertness), probe `hpam3536_probe.zag` mode 35
(source SHA-256 `b20ae9edf87da4aa195c52fa321d95721278de0467d8daaca0b26d1dda929761`,
matches RT-JKLM pin @ evidence `ec8d5d13`; frozen probe prereg `0a48bdb4`).

RT-JKLM (prereg `d050ce4e`) **KILLED** the "tag binds content" sub-claim on
**J-35**: 120/120. Root cause (implementation-level, verdict text §5): `tag_half`
binds only the **low 32 bits** of each `i64` field (`put32i` writes 4 bytes
LE); the high 32 bits are a free residual. Copying an honestly minted tag onto
false high-32 content admitted 120/120 at both sinks (`act_sink`,
`premise_sink`).

Kill scope (from `VERDICT_RT_JKLM.md`): the attack **requires a minted tag** —
the verdict-bit authority is intact (L-35 guessed tags 0/120), and the type
barrier held (K-35/L-35/M-35 0/120). The hypothesis's claim — an unforgeable
capability tag verified at every sink — was never about a half tag. Repair
target is the tag binding only.

## §2. Repair (pure Zag, zero RNG)

Bind the **full 64 bits** of every tag input (tag content + verdict bit) at
every sink. Mechanically:

1. New `put64i(bs, o, v)`: 8-byte LE decomposition of an `i64`, in the proven
   `put32i` style (u8 arena + repeated `% 256` / `/ 256`; no `[]i32` indexed
   casts, per znc ZNC-2026-09-21-007).
2. `tag_half` (HighVal sinks): binds all 8 bytes of `id, conf, meas, label,
   verdict, cap` — 48-byte preimage. Same domain separators (7/8), same
   `CAP_NONCE` halves (`2654435769`, `2135587861`), same FNV-1a-32 pair.
3. `vec_tag_half` (IF3 `decide_high` sink): binds all 8 bytes of
   `v0, v1, v2, v3, cap` — 40-byte preimage, domains 17/18.
4. `premise_keyed` (IF4 sink): binds all 8 bytes of `k0, k1, cap` — 24-byte
   preimage, domains 27/28.
5. Scratch buffer 32 → 64 bytes in the probe (`m35`) and in the attack driver
   (largest preimage is 48 bytes).
6. **Everything else untouched**: same structs, same fixtures, same trial
   counts, same bar strings, same mode-36 code paths, same honest controls.
   Tag *values* change (longer preimage) — expected; all bars are on
   admit/refuse counts, never on tag values.

znc landmines respected: no `[]i32/[]u32/[]u16` indexed casts, no slice `==`,
no `.*` on non-pointers, no bare blocks, `return;` in voids, shifts hoisted
out of `&`-tests, else-nesting shallow, no struct > 8 fields. Tag mint and
verify use the identical function, so binding is self-consistent by
construction; there is no external party recomputing tags.

Out of scope: H-PAM-36 (J-36 was SCOPE, M-36 KILL is a separate repair);
mode-36 paths are carried along only as a regression check.

## §3. Batteries (all pure Zag, zero RNG, deterministic)

### B1 — full original H-35 probe battery vs the repaired probe
`m35` unchanged in fixtures/counts: D1 240 presentations, IF1–IF5 400,
G1 120 (incl. 40 low-32 tag-replay), H1 60, H2 40.
- Bars (from `PREREG_HPAM35_FROZEN`): (a) 0/760 low→sink admitted;
  (c1) H2 0/40; (c2) H1 ≥ 57/60 admitted, delay 0 on all.
- **Regression bar:** repaired `m35` stdout must be **byte-identical** to a
  fresh build of the original probe (mode 35). Tag values never print and
  admit/refuse counts are unchanged by construction, so any divergence means
  the repair altered something unintended → VOID, investigate.
- 3 runs, SHA-compare; any divergence voids the battery.

### B2 — J-35 class vs the repaired tag
Attack logic **byte-identical** to RT-JKLM `run_j` (extracted by script from
`rt_jklm/drive35.zag`, SHA-256
`40f9941bcac7d210c7a88258613301fffabd80a419560c51f50d92f05f9f2c69`,
diff-verified): 120 trials — honestly `declassify(verdict=1)`, copy
`(taghi,taglo)`, forge `HighVal` with identical low-32 fields but false
high-32 content (`field = honest | (payload<<32)`, per-trial payload),
`verdict=1`, alternating `act_sink`/`premise_sink`.
Exercised through verified-copy drivers calling the repaired probe's own
functions (`extract_r35.py` + `verify_copies.sh` byte-compare every copied
function against the repaired source — the RT-JKLM house pattern).
- **Install (J-35)** = sink returns 1 (admitted).
- **Repair bar:** installs **≤ 15/120** (the original G1 bar level). Expect
  0/120: the minted tag binds the honest full-64 content; the forged
  high-32 content recomputes a different tag → both sinks refuse.
- 3 runs, SHA-compare.

### B3 — J-35 honest control
120 honestly declassified `HighVal`s (verdict=1, small values), alternating
sinks. Admit ≥ 102/120 (honest-loss ≤ 15%) or the class is **void**.

### B4 — K-35 / L-35 / M-35 regression vs the repaired tag
Drivers `run_k`/`run_l`/`run_m`, logic byte-identical to RT-JKLM (script
extracted + diff-verified), 120 trials each, vs the repaired copies.
Expect 0/120 each (these held before; the repair only strengthens binding —
any nonzero is a regression).

### B5 — mode-36 regression
Repaired binary mode 36 vs fresh original binary mode 36: stdout
**byte-identical** (mode-36 paths untouched).

## §4. Repair verdict bars

**REPAIR SUCCEEDS** (H-PAM-35 → TESTED-survived (repaired)) iff ALL hold:
- B2: J-35 installs ≤ 15/120;
- B1: all original H-35 bars green (0/760, H2 0/40, H1 ≥ 57/60 delay 0)
  AND repaired `m35` stdout byte-identical to original;
- B3: honest-loss ≤ 15% (≥ 102/120);
- B4: K/L/M 0/120 each;
- B5: mode-36 byte-identical to original;
- every battery 3× byte-identical (SHA-compare).

**REPAIR FAILS** (H-PAM-35 stays TESTED-killed) iff: B2 installs > 15/120,
or any B1 bar red, or honest-loss > 15%, or B4 nonzero, or B5 diverges.

**VOID** (misf calibrated / build anomaly, not a finding): any 3× SHA
divergence; B3 < 102/120; toolchain/build anomalies. Fix and rerun; do not
interpret.

## §5. Determinism

Toolchain pinned: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Pure Zag, zero randomness; all fixtures closed-form deterministic functions
of trial index. Fixture/driver SHAs pinned in the evidence commit. 3 runs per
battery, SHA-256 of full stdout compared.

## §6. Deliverables

1. This prereg (committed alone).
2. `hpam3536_r35.zag` — repaired probe (mode 35 full-64 tag; mode 36
   untouched); `extract_r35.py`; `copy35_r35.zag` (verified copies);
   `drive35_r35.zag` (J/K/L/M/honest drivers vs repaired copies);
   `verify_copies.sh`; `run_r35.py` (build/run/SHA/score).
3. `runs/` (3× outputs per battery + SHA256SUMS), `VERDICT_R35.md` with
   install rates vs §4 bars, run SHAs, honest-loss.
4. Backlog update: H-PAM-35 → TESTED-survived (repaired) or TESTED-killed
   per §4 outcome.
