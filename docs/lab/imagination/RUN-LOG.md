# IMAGINATION-DESIGN trial — RUN LOG

Started 2026-09-22. All times PDT. Frozen prereg: `PREREG.md`
(commit `6603e8dd6a025d722c8ede5e607acad6f26f72a3`, branch `tnn-native-lab`).

## 2026-09-22 ~04:50 — Q0 baseline audit

Searched `senses/rebuild/b_percept/` (`percept.zag` 282 lines,
`PERCEPT_DESIGN.md` 150 lines, `sense.zag`, `transducer.zag`):
no scene buffer, no offline simulation partition, no
construct-then-query representation. b_percept = live classification
(fixtures in, handles out). Finding: NONE — mechanism had to be built.
Full file/line evidence: `AUDIT-Q0.md`.

## 2026-09-22 ~04:55 — Build

`src/imagine.zag` (~2000 lines, pure Zag, zero RNG) compiled with
`toolchain/bin/znc_linux_x86_64_abed8aa1 --no-zagd --no-analyze
--no-foreground-cache` → `src/imagine_bin` (205365 bytes after the
2026-09-22 Q3 rebuild; earlier build 191073 bytes). No errors.

## 2026-09-22 ~04:56 — Q1 runs + independent verification

`imagine_bin q1 m all` / `q1 h all`: 38 lines/mode (36 questions; the
farthest-pair question emits 2 lines with one qid in scenes 2 and 4 —
documented, scored as one question each).
`verify_imag.py` (independent Python port, hand-authored from reading
the source, not from running it): **machine 36/36, human 36/36**.
IMAG-1 (≥26/36): **PASS both modes**.

## 2026-09-22 ~05:00 — Signed-sentinel audit

`ig_get32` reads unsigned; stored `-1` rel-targets read as 4294967295.
All sites audited (`AUDIT-Q0.md` Appendix A): `cur < 0` disjuncts are
dead under unsigned reads, but every path is caught by `cur >= n`
guards → deterministic, no hang, no miscompare. No change made
(frozen code); flagged, not silently fixed.
Pitch-handle wording gap flagged (`AUDIT-Q0.md` Appendix B): prereg
says 4000–4047, code stores the ordered bin index (0–47) — disjoint
from machine Hz values, so mode vocabularies stay disjoint.

## 2026-09-22 ~05:05 — Q3 sources verified

All 8 pairs re-verified against public web sources (see `Q3-SOURCES.md`):
pairs 1–5 STRONG (Gap 6-day revert; Tropicana −20% sales; New Coke
79 days; UC 50,000+ petition; Cracker Barrel Aug 2025 revert),
pairs 6–8 MODERATE (Starbucks 2011 still in use, award-winning;
Mastercard 2016 "Logo of the Decade"; Apple 1998 mono among most
recognizable marks).

## 2026-09-22 ~05:06 — Q3 encodings rebuilt

Old `ig_pair` encodings were degenerate (single-element ties, pair 7
identical both sides, pair 8 encoded as audio for a logo pair).
Rebuilt from `Q3-SOURCES.md` facts: 2–6 visual elements per design,
same facts in both codecs, no attribute chosen to push a score toward
the known outcome. Rebuilt binary, ran `q3 m` / `q3 h`.

Q3 scores (documented preference in brackets):

| Pair | Machine s0/s1 (pref) | Human s0/s1 (pref) |
|---|---|---|
| 1 Gap (classic=s1) | 592/630 OK | 491/662 OK |
| 2 Tropicana (orig=s1) | 462/619 OK | 591/625 OK |
| 3 New Coke (classic=s1) | 666/766 OK | 591/712 OK |
| 4 UC (seal=s1) | 414/778 OK | 562/641 OK |
| 5 Cracker Barrel (orig=s1) | 700/539 MISS | 1000/725 MISS |
| 6 Starbucks (2011=s0) | 775/794 MISS | 662/691 MISS |
| 7 Mastercard (2016=s0) | 545/439 OK | 508/528 MISS |
| 8 Apple (mono=s0) | 446/289 OK | 612/642 MISS |

Zero ties (frozen tie rule unused). AGREE-1: machine 6/8 → MARGINAL;
human 4/8 → FAIL; best mode 6/8 → **MARGINAL**. AGREE-2: |6−4|=2 < 3 →
**NO-DIFFERENTIATION**. Secondary: STRONG tier 4/5 both modes;
MODERATE machine 2/3, human 0/3.
Scorer: `verify_imag.py --q3m/--q3h` (preferences from `Q3-SOURCES.md`).

## 2026-09-22 ~05:10 — Q3 determinism

5 reps `q3 m` / `q3 h`: byte-identical.
SHA256: m=`f7f82ae06399720f8da6365545e28876de19399f515277bd3ad9fdc930288f52`,
h=`cfbaecf87186650a494df4ea5b6ec100406197fdb122ccd71b60f5f62dbc0ad2`.
Logs: `logs/q3m_repN.txt`, `logs/q3h_repN.txt`.

## 2026-09-22 ~05:23 — Q1V video battery applied + run

Amendment applied: `PROPOSED-amendment-video-2026-09-22.md` →
`PREREG-amendment-2026-09-22-video.md`, status set to APPLIED 2026-09-22
(approved by Micah's standing test-authorization 2026-09-21 22:20 and his
explicit video-battery order). Battery spec, scenes, and IMAG-V bar
(≥9/12 per mode) unchanged from the proposal.

`src/imagine.zag` extended (additive only): domain=4 VIDEO, one element per
frame (machine: frame,x,y,r,g,b,dx,dy; human: frame,zone,color,
dir-handle 6000–6008, speed-handle 6100–6102, shape tuple), 4 scenes
(V1 ball rolls L→R 3f; V2 bird arch 4f; V3 car accelerates 3f;
V4 pendulum out-and-back 4f), 4 queries (`query_trajectory`,
`query_speed_change`, `query_reentry`, `query_midpoint`), displacement-
consistent edits. Rebuilt with
`toolchain/bin/znc_linux_x86_64_abed8aa1 --no-zagd --no-analyze
--no-foreground-cache` → `src/imagine_bin` (226401 bytes), no errors.

Runs: `imagine_bin q1v m all` / `q1v h all`, 5 reps each, byte-identical.
Independent verifier `verify_q1v.py` (hand-written from the spec, not the
binary): machine **12/12** all reps, human **12/12** all reps.
IMAG-V (≥9/12): **PASS both modes**. Full scene/question/answer tables:
`Q1V-RESULTS.md`. Logs: `logs/q1vm_repN.txt`, `logs/q1vh_repN.txt`.
SHA256: m=`55b26e0579528345ee218668557227d1fe6f3806f2566bd7b76c5fea6a221f40`,
h=`5bb4428240b6591662339150330275548c4a22c6277f7d4d5c84799b1190faa3`
(all in SHA256SUMS).

## Pending (in flight)

- Q2 GEN-1/GEN-2/GEN-3 mechanical verification + text-only Q1 control +
  Q1/Q2 5-rep determinism + Q4 blind packet → delegated subagent,
  results land in `Q2-VERIFY.md` / `Q4-PACKET.md`.
- Q4 human rating: needs Micah (or approved outside panel).
- `VERDICT.md`, commit (after Q2 results land).

## 2026-09-22 — field track: pure-TNN generation mandate + generative audio/video

Micah's hard constraint: every shipped image/WAV/video must be generated by
TNN's own Zag machinery — no Python renderer, PIL, ffmpeg, or external synth
in the generation path (Python is harness-only now).

- Extended `src/field.zag`: `f3_emit_bmp` (integer-bilinear visual /
  heat-ramp spectrogram / hillshaded relief rasterizers → 14 BMPs),
  `f3_emit_avi` (uncompressed 240x240 8fps AVI + PCM audio + idx1, written
  byte-by-byte; new `f3_write_all` via raw write(2) since nio_write_all caps
  at 1 MiB), `f3_emit_wav` (8 WAVs), `f3bmp`/`f3avi`/`f3vidwav` commands,
  `f3novel` extended to scenes 11–18.
- Rebuilt: `src/field_bin` = 196,206 bytes native main, 0 external tools.
- Audio grid now energy + brightness (48x48x2); verifier updated (F3_SLOTS
  brightness counted, GEN-3f q2 sums energy only).
- N17 entire short song + N18 unheard sound built (melody/bass/pad/drums;
  inharmonic partials + crossing sweeps + noise + pulses). Honest caveat
  recorded: synthesis still maps bins through a fixed sine-LUT stack — may
  violate Micah's literal "no hardcoding sines"; ear judgment pending.
- Results (verify_fields.py, full output above): M1f v1 3.80 / v2 5.86 /
  f3 5.38 attrs per unit, units/scene 3.8/4.8/5.3 (H2 still undecided);
  M2f 32/32 (bar ≥24); GEN-1f 12/12; GEN-2f 12/12; GEN-3f 24/24;
  native artifacts clean; determinism PASS; M4 PASS. BARS: PASS.
- Independent verification: `crosscheck_raster.py` (Python reimplementation
  of the integer raster rules) reproduces all 14 BMPs + all 48 AVI video
  frames byte-identically → CROSSCHECK PASS. Independent RIFF/AVI parser:
  RIFF size, avih, 24v+24a chunks, 48 idx1 entries all valid; embedded audio
  == sibling WAV PCM (52,800/52,800 bytes). ffprobe used as verifier only.
- Shipped: 14 BMPs + 8 WAVs to `~/workspace/your_files/imagination_fields/`
  (old Python PNGs retired to `harness_png_superseded/`); 2 AVIs + 4 WAVs to
  `~/workspace/your_files/imagination_video/` (+ README-FIELDS.md).
- Blind packet rebuilt with Zag BMPs + novel-probe section + video section;
  v1/v2 PNGs still Python-rendered (flagged in-packet, native re-render
  pending on the element tracks).
