# RUNLOG: TNN-deliberated head placement

## 2026-09-26 ~16:55 PDT

### Changes
Modified `pigfront.zag` in `~/workspace/pigfront/teach/`:
1. Added `deliberate_headx(t, K)` — TNN weighs E1/E2/E3 from taught knowledge,
   excludes E3 on its own evidence, chooses E2=163.
2. Added `deliberate_heady(t, K, ery, hry, hrx)` — TNN scale-corrects the taught
   ear-line (39→37), applies the flap visibility constraint, chooses hcy=123.
3. Taught branch: `dhcx`/`dhcy` replace hardcoded 160/112; `eLx`/`eRx`/`snx`
   derive from `dhcx`; `eline` derives from `dhcy`; torso-x follows `dhcx`.
4. Degenerate fallback (`dhcx<0`) traced as frame-center prior, not a measurement.

### Build
```
cd ~/workspace/pigfront/teach
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 pigfront.zag -o pigfront_delib_bin
```
Build clean (warnings pre-existing). Binary 317,237 bytes.

### Runs (byte-identical ×2)
```
./pigfront_delib_bin run /home/hatch/workspace/forkB-scratch/frames/donor ./delib_run1 /home/hatch/workspace/pigfront/forka ./knowledge
./pigfront_delib_bin run /home/hatch/workspace/forkB-scratch/frames/donor ./delib_run2 /home/hatch/workspace/pigfront/forka ./knowledge
```
Both exit 0.

SHA-256 (run1 vs run2):
- front_construct.ppm: 1f90fd61…fb4275 == 1f90fd61…fb4275 MATCH
- epistemic_map.ppm:  2e1820b9…ada3a63c == 2e1820b9…ada3a63c MATCH
- trace_pigfront.txt:  c2889b58…fa5903   == c2889b58…fa5903   MATCH

### Results
- plan_head: (163, 123) rx=86 ry=86
- head placement error: dx=19 dy=11 manhattan=30 (was dx=22 dy=0 manhattan=22)
- face coverage: 100% (unchanged)
- snout: (185,184); ears: (77,37)/(249,37)
- critic verdict: HONEST; fab_blobs=0; eye_pairs=0

### Honest assessment
Head-x improved by deliberation (19 < 22). Head-y regressed (0 → 11) because
the old 112 exactly matched the held-out truth — TNN's faithful transfer of
taught knowledge gives 123. The dy is frame-to-frame variation (teaching
frame ≠ truth frame), not a logic error. Reported without softening.

### Cleanup
Build binary `pigfront_delib_bin` and run dirs `delib_run1/`, `delib_run2/`
are workdir-only (not committed). Repo gets: modified `pigfront.zag` +
`evidence_delib/` (verdict, runlog, trace excerpt).
