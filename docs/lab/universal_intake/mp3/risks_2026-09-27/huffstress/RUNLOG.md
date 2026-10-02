# RUNLOG — MP3 RISK 3: MAX-HUFFMAN-VALUE STRESS

Workdir: `~/workspace/mp3_risks/huffstress/`
Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
Decoder source: `~/workspace/selfpam_run/tnn-lab/docs/lab/universal_intake/mp3/zag_full/mp3dec.zag`
Oracle: `~/workspace/selfpam_run/tnn-lab/docs/lab/universal_intake/mp3/ref/mp3ref.py`
Pure Zag, zero RNG, fully deterministic. Nothing committed (parent commits).

## 1. Baseline: fresh decoder build + fixture regression (2026-09-27 UTC)

```
cd ~/workspace/selfpam_run/tnn-lab/docs/lab/universal_intake/mp3/zag_full
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 mp3dec.zag -o /tmp/mp3dec_ref
cd ~/workspace/selfpam_run/tnn-lab/docs/lab/universal_intake/mp3/fixtures
for f in t_128cbr t_vbr t_128js; do /tmp/mp3dec_ref $f.mp3 /tmp/$f.pcm && sha256sum /tmp/$f.pcm; done
```

Result — all three match BUILD.md exactly:
- `t_128cbr`: `f72aca836ff4ddc69e6a084e302302243750e0857a7bc0a36de533a8b10bb467`
- `t_vbr`: `7abcd3cb239f530cbc583ff9427738f2a2276bb47a14ae885551d7be63e4c6d5`
- `t_128js`: `711f0f067397f1439f62f18275b88e0e25df86875936e11f27be0d65318209b0`

## 2. pow_43_z full-domain sweep

Linbits table (from `mp3tab64.zag`): tables 16–23 → `1,2,3,4,6,8,10,13`;
tables 24–31 → `4,5,6,7,8,9,11,13`. Max reachable lsb = 15 + (2^13−1) = 8206.

```
cd ~/workspace/mp3_risks/huffstress
cp ~/workspace/selfpam_run/tnn-lab/docs/lab/universal_intake/mp3/zag_full/common.zag \
   ~/workspace/selfpam_run/tnn-lab/docs/lab/universal_intake/mp3/zag_full/mp3tab64.zag .
python3 gen_sweep.py          # extracts pow_43_z byte-verbatim -> sweep.zag
                             # extracted fn SHA-256: c47f8ce8f12a3e92e852e3a7772b73627a73881d72e7be5e6b820540ba0ca3bc
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 sweep.zag -o sweep
./sweep                      # dumps 8207 f64 LE -> sweep.bin
python3 cmp_sweep.py         # vs strict Python float(x)**(4/3)
```

Sweep results (all 8207 x in [0,8206]):
- NaN: 0, +inf: 0, negative: 0
- max rel err vs strict `x**(4/3)`: 1.319428e-06 at x=1055 (quadratic-approx interior error)
- region maxima: 0..128 → 7.555282e-08 (x=2); 129..1023 → 1.297733e-06 (x=132);
  1024..8206 → 1.319428e-06 (x=1055)
- boundaries: x=128 → 645.07958984375 (rel 1.906e-08); x=129 → 651.80791835652462 (4.229e-08);
  x=1023 → 10307.83646674123 (1.902e-08); x=1024 → 10321.2734375 (1.906e-08);
  x=8206 → 165516.77860819467 (strict 165516.77541216419, rel 1.931e-08)

## 3. Table-representation analysis

```
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 dump_tab.zag -o dump_tab
./dump_tab                   # exact f64s as the decoder loads t_pow43b() -> pow43tab.bin
python3 analyze_table_noise.py
```

Findings:
- Zag loads `t_pow43b()` as exact f32 bit patterns widened to f64; the oracle's
  `mp3_tables.json` holds rounded decimal f64s. 136/145 entries differ in bits;
  max rel table discrepancy 5.574e-08.
- Pure-Python poly using the EXACT Zag table vs `sweep.bin`: 0 bit mismatches
  over all 8207 → arithmetic/codegen bit-identical given identical constants.
  Stock-oracle bit differences come from table serialization, not `pow_43_z`.

## 4. Huffman-code inversion

```
python3 sim_ones.py          # 0xFF payload simulation
python3 invert_tables.py     # (15,15) escape codeword per linbits table, verified by re-decode
```

Findings:
- Literal 0xFF bytes decode (0,0) repeatedly (1-bit codewords tables 16–23,
  4-bit codewords tables 24–31) — they do NOT reach max linbits values.
- (15,15) escape codewords: tables 16–23 → `00000011` (8 bits);
  tables 24–31 → `0011` (4 bits). All 16 verified by independent re-decode.
- True max payload per pair: [escape cw][linbits ones][sign][linbits ones][sign]
  → lsb = 15 + (2^linbits − 1). (First attempt wrongly emitted one codeword per
  VALUE instead of per PAIR; caught because the Zag driver decoded lsb=142 for
  value 1 instead of 8206 — the DECODER was correct, the test payload was
  malformed. Fixed in `gen_huffdrv.py`, verified via `dbg_payload.py`.)

## 5. B1 differential drivers (all 16 linbits tables)

```
python3 gen_huffdrv.py       # 34 drivers: 16 tables x {escape,ones} + t23 maxgain/maxscf
                             # extracts pow_43_z,huffman,gr_get,hr_init,hr_peek,hr_flush,
                             # hr_check,zalloc64,zallocf byte-verbatim (asserted)
for t in <34 tags>; do
  ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 huffdrv_$t.zag -o huffdrv_$t
  ./huffdrv_$t               # -> b1_$t.bin (262144 f64 LE) + w_$t.bin (sfb widths)
done
python3 cmp_b1.py            # vs stock oracle AND vs faithful pure-Python port
                             # (oracle huffman source-transformed to use exact Zag table)
```

Driver inputs per run: buf = payload + 2048 zero bytes; gri = [big_values=288,
table_select=[T,T,T], region_count=[7,7], count1_table=0, block_type=0];
scf = 40 x SCF_VAL; sfb widths = scf_long_get(5*23+k); layer3gr_limit = 8*len(buf).

(MAX_ONE analysis: `one = ldexp_q2(gain, iscf<<scf_shift)` ATTENUATES with
scalefactor, so the true max `one` is global_gain=255, scalefactors=0:
1217.7480856579155. The task's "scalefactors at max → max one" is inverted;
both variants tested: maxgain=1217.7480856579155, maxscf=0.004645340294497282.)

Results — vs FAITHFUL port (exact Zag table): ALL 34 runs BIT-EXACT
(262144/262144 f64 bit patterns, symbols match).
Results — vs STOCK oracle: escape runs differ only by table noise
(max rel 1.84e-08 for linbits-13 tables, ≤9.1e-09 for 11/10); ones runs
BIT-EXACT (maxlsb=0 → 0.0 exactly). No NaN/inf in any run.
Max lsb confirmed: 8206 (tables 23,31), 2062 (table 30), 1038 (table 22).
Max product: 1217.7480856579155 * 165516.77860819467 ≈ 2.0156e8 — no overflow.

Determinism: `./huffdrv_t23_esc_std` rerun → SHA-256 identical
(54b3913e0d238def5dd9d397028db1806853750f712d6a4fd6760792569930ea).

## 6. PCM-level stress (all 16 tables + maxscf)

```
python3 gen_pcm_frames.py    # 33 synthetic mono frames (MPEG-1 L3, 320kbps, 44.1kHz)
                             # side info: table T all regions, big_values=96,
                             # global_gain=255, scalefac_compress=0 (maxscf frame: 15)
                             # frame parse verified via oracle read_side_info
cd ~/workspace/selfpam_run/tnn-lab/docs/lab/universal_intake/mp3/zag_full
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 mp3dec.zag -o ~/workspace/mp3_risks/huffstress/mp3dec_full
cd ~/workspace/mp3_risks/huffstress
for f in frames/pcm_*.mp3; do ./mp3dec_full $f pcm/$(basename $f .mp3).pcm; done
python3 cmp_pcm.py           # vs oracle MP3Ref full-decode PCM
```

Findings:
- All 33 frames decode without crash/hang; 1152 samples each.
- Extreme spectra clip at ±32767/±32768 via scale_pcm (correct behavior).
- vs oracle PCM: escape frames 1152/1152 bit-exact (clipping erases the 2e-8
  B1 differences); ones frames 1149/1152, max abs diff 1 LSB (rounding at
  clip/round boundaries). t25_esc 1151/1152, diff 1.
- All 16 ones frames produce IDENTICAL PCM (SHA 5f449decdcb11a6b) — confirms
  0xFF decodes (0,0) pairs on every table; count1's all-zero codeword decodes
  (±1,±1,±1,0), so the ones frames are not silent (deterministic, both sides agree).

## 7. Determinism reruns

```
./sweep && sha256sum sweep.bin   # 60c6fc2e408d44a41446f014dfec3b0254e17583e26aa51ddab80b2f7eacb751 (x2 identical)
./huffdrv_t23_esc_std            # rerun -> identical SHA (see §5)
```

## 8. Final fixture regression (decoder source unchanged)

```
cd ~/workspace/selfpam_run/tnn-lab/docs/lab/universal_intake/mp3/fixtures
for f in t_128cbr t_vbr t_128js; do ~/workspace/mp3_risks/huffstress/mp3dec_full $f.mp3 /tmp/$f.pcm && sha256sum /tmp/$f.pcm; done
```

(Decoder source was NOT modified — no defect found; regression confirms the
build used for PCM stress reproduces the committed fixture SHAs.)

## 9. Notes / deviations

- No MPEG table has linbits=12 (linbits values present: 1,2,3,4,5,6,7,8,9,10,11,13).
  Covered both linbits-13 tables (23,31), linbits-11 (30), linbits-10 (22) at B1.
- `cmp_b1.py` builds its faithful port by source-transforming `mp3ref.huffman`
  (replacing `G_POW43`→exact Zag table, `pow_43`→pure-Python `pow_43_z` port),
  so the reference logic cannot drift from the oracle.
- B1 drivers dump 262144 f64 values (upper bound on writes: 576 + 4*total_bits
  < 262144 for all payloads); comparison covers all of them.
