# IMAGINATION — VERDICT SHEET (analysis + red-team)

Worker: native (imagination). Partner: Grok 4.7 (degraded → VOID, then hard-down; see Fallback log).
Date: 2026-09-22. Scope: 39/39 manifest items reviewed (15 P0 full HTRF, 24 P1 review-level).
Rule: no building/modifying imagination mechanisms or sources; reran existing harnesses only.
Item-level results: `ITEMS_DONE.tsv` (same directory).

## 1. CLAIMS ANALYZED (native verification)

All reruns below use the EXISTING committed binaries/logs — no rebuilds.

### Reproduced PASS
| Claim | Native rerun | Result |
|---|---|---|
| Field M1f/M2f/GEN (verify_fields.py) | `python3 verify_fields.py` | ALL PASS; numbers reproduced exactly (M1f v1 175/46=3.80, v2 340/58=5.86, f3 172/32=5.38; M2f 32/32; GEN-1f 12/12, GEN-2f 12/12, GEN-3f 24/24; determinism; M4) |
| Raster crosscheck | clean-room: `f3dump all`+`f3novel`+`f3video` → `crosscheck_raster.py` | CROSSCHECK PASS — 14/14 BMP + 48/48 AVI frames byte-identical |
| AVIs deterministic vs shipped | sha256 of fresh `f3vid1/2.avi` vs `your_files/imagination_video/` | MATCH both |
| Hi-fi bars (verify_hifi.py) | on shipped hi-fi WAVs | ALL PASS (H2 44100/16/mono, H3 no-clip peak 24000, H4 exact 12-TET, H5 bipolar, H5b no-DC) |
| Q1 72/72 (verify_imag.py) | on rep1 logs | 36/36 per mode (bar 26/36) |
| Q3 (verify_imag.py) | on rep1 logs | machine 6/8 MARGINAL, human 4/8; AGREE-2 \|6−4\|=2 NO-DIFFERENTIATION |
| Q1 text-only control | verify_q1_textonly.py | <12/36 per mode — memorization guard holds |
| Q1V 12/12 (verify_q1v.py) | on logs/q1vm_rep1.txt | 12/12 per mode (bar 9/12) |
| GEN-1/GEN-2 (verify_q2_gen.py) | on logs/q2m.txt, q2h.txt | PASS (12/12 mode fidelity) |
| GEN-3 (verify_q2_gen3.py) | on logs/q2m.txt, q2h.txt | 24/24 (bar ≥20/24) |
| scenes_inc.zag 65/65 byte-identical | brace-matched fn extraction vs imagine.zag | 65/65 byte-identical, 0 missing, 0 mismatched |
| emit.zag pitch table | values vs 110·2^(b/12) | all correct; used bins {15,16,17,19,20,22,24,26,27} all covered; gaps {18,21,23,25} never emitted |
| v2 48-freq table (sin_lut.zag) | vs round(110·2^(b/12)) | correct Hz values (no B2 mistuning in v2 path) |

### Reproduced FAIL / measured-against-frozen-bar
| Claim | Native check | Result |
|---|---|---|
| Upgrade M1 (v2 ≥ 2× v1 both axes) | verifier's own m1 code (BIN path fixed only) | v1 3.80/3.83, v2 5.86/4.83 → **1.54×/1.26× FAIL** |
| Upgrade M2 (≥18/24 novels) | verifier's own m2 code (BIN path fixed only) | **17/24 FAIL** (machine novels only; one check hardcoded True) |
| Upgrade M4 (v1 untouched) | via verify_fields.py | PASS |
| imagine.zag SHA256SUMS guard | recorded 7ea9b80b… vs current 949addd6… | **DRIFT — file-level guard broken** (behavioral M4 passes; re-record needed) |

## 2. RED-TEAM ATTACKS + NATIVE ADJUDICATION

Voice key: SOL = gpt-5.6-sol (fallback per 23:16 alert; grok-4.7 outputs VOID — tooling artifact). Adjudications are native (repo evidence + reruns).

### A1. "Two independent implementations" (crosscheck_raster.py)
- **SOL attack:** byte-agreement is a consistency check against a re-rasterizer, not an independent semantic oracle; no evidence of author independence; consuming the binary's own dumps as ground truth means shared-spec/common-mode errors survive.
- **Native adjudication: PARTIALLY SUSTAINED.** The check genuinely guards emitter-level byte bugs (BMP headers, stride, padding, AVI chunk layout, interpolation arithmetic, channel order) — 14/14 + 48/48 reproduced clean-room. But "independent implementations" overstates: no author-independence evidence; the oracle is the binary's own grid dumps. **Correction:** say "independent rasterizer implementation / cross-language renderer consistency check," never end-to-end independent verification. RUN-LOG should record the exact dump composition (`f3dump all` + `f3novel` + `f3video`) — reconstructed, not documented.

### A2. Literal sine-LUT vs "no hardcoding sines"
- **SOL attack:** a literal 256-entry sine table is a hardcoded waveform vocabulary regardless of how variable the per-cell harmonic weights are; ear quality cannot waive the literal mechanism requirement; "sounds equivalent" ≠ mandate compliance.
- **Native adjudication: SUSTAINED.** `src/sin_lut.zag` holds the literal table; both field legacy and hi-fi paths sample it; the fields amendment FROZE the LUT ("reuses the frozen sine LUT") while the generative amendment reinterprets Micah's order as timbre-only ("Basis oscillators remain sines"). The program is honest in its docs ("do not claim fully-generative-audio success until a non-fixed-waveform alternative is tested head-to-head and Micah's ear judges both files") — but the literal mandate is UNSATISFIED. Note: emit.zag's video soundtracks already use runtime Taylor-series sine (no table) — a non-LUT method exists conceptually. Correct claim: native/deterministic additive audio, NOT mandate-compliant generative audio. Phase-3 head-to-head proposed in §4.

### A3. Blind packet leaks track identity
- **SOL attack:** per-item provenance labels ("Zag-native (field.zag...)" vs "Python renderer (pending native Zag re-render)") plus `blind_key.txt` in the same directory make the packet shuffled but not track-blind; expectancy/prestige effects contaminate ratings.
- **Native adjudication: SUSTAINED.** Confirmed in `build_blind_packet.py` (labels injected per item; key written beside the HTML). **Correction:** strip labels, normalize presentation, move key to a separate file, reveal provenance only after ratings.

### A4. Q4 packet: key in same document + inferable mode
- **SOL attack:** footer key ("A=(mode0,brief3)…") with "do not read past this line" is not a control; mode is inferable from description vocabulary (262 Hz vs warm-amber) — systematic unblinding; mode is confounded with description register (raw values vs qualitative percepts impose different cognitive load).
- **Native adjudication: PARTIALLY SUSTAINED.** Both weaknesses confirmed in Q4-PACKET.md (footer key; self-acknowledged inferability). The vocabulary-faithful description was a preregistered design choice, but it means ratings cannot cleanly attribute differences to imagination quality vs description style. **Correction:** separate-key protocol + neutral descriptions (or render-based rating). Additional: prose mislabels handles — 2003 "neutral-gray-blue" (table: LIGHT_GRAY), 1027 "warm-amber" (table: YELLOW-MID).

### A5. Stale distorted audio contaminates ear ratings
- **SOL attack:** packet audio was rendered through buggy synth paths; binding ear judgments on distorted files are invalid for the corrected path.
- **Native adjudication: PARTIALLY SUSTAINED.** Confirmed: field legacy path has B1 (unsigned `f3_get32` mix reads → half-wave rectification; measured min=0, zero-crossings=0, DC 0.42) + B2 (semitone constant 1.06529 vs 2^(1/12), +9.5¢/semitone compounding). The v2 WAV emitter (`j2_emit_wav`) ALSO carries B1 (unsigned `j2_get32`) — so packet audio briefs (v2 + field) are ALL distorted, and fields additionally sound detuned vs v2 (B2) — a systematic disadvantage to the field track in M3f audio ratings. Mechanical M2f 32/32 stands (stroke/grid criteria, not perceptual). **Correction:** replace packet audio + AVI soundtracks with corrected deterministic renders; disclose prior fault; restart blind ratings for affected items. (No duplication of the fidelity track — file as packet dependency.)

### A6. H2 (substrate) exposure-vs-mechanism identification
- **SOL attack (native-led; sol H2 call timed out):** fields differ from v1/v2 in exposure (6 scenes vs 12, one modeless builder vs two mode builders), briefs, units (strokes vs elements), and attribute vocabularies (brightness is field-only) — "populated attrs/unit" favors larger vocabularies; no clean substrate isolation.
- **Native adjudication: H2-SUPPORTED already EXCLUDED by the frozen verdict rule** (needs field ≥ v2 on M1f-density AND M2f AND M3f-lead; M1f density fails: 5.38 < 5.86 attrs/unit). Best possible: H2-PARTIAL (pending v2's M2 and M3f). Interim "UNDECIDED" is acceptable shorthand but the sharpened statement is: SUPPORTED ruled out; PARTIAL possible. Settling test proposed in §4.

### A7. Taste-probe "no simplicity preference"
- **SOL attacks:** (1) the 4 novel pairs were SELECTED for documented complex-preference — 2/4 on n=4 is compatible with any preference, selection-biased; (2) machine 6/8 is only +1 over the always-old baseline (5/8); (3) naming the decisive sub-score term redescribes the programmed taste functions rather than discovering a preference.
- **Native adjudication: PARTIALLY SUSTAINED.** The degenerate single-element scoring IS proven (vacuous harmony 400 + trivial self-mirror balance 300 + max simplicity 300 = 1000 by construction — the Cracker Barrel miss is a math artifact, frozen per Micah's no-debiasing order). The decisive-term distribution (SIMPLICITY decisive in 1/12 human-mode decisions; 3 of 4 human-mode misses had simplicity voting WITH humans) is valid evidence against the bias claim. But: the novel-probe 2/4 must NOT be cited as chance-level evidence (selection-biased, n=4); and the decomposition is explanatory redescription, not an independent discovery. **Correction:** cite the criterion distribution + the proven degenerate case; drop the 2/4 line.

### A8. v2 amendment: the verdict that was never rendered
- **SOL attacks:** (1) the shipped verifier was not operational (wrong line prefix, bad default path, impossible hardcoded note count) and no UPGRADE-RESULTS.md / recorded M1/M2 measurements exist — the preregistered decision procedure never produced a verdict; (2) the independent rerun (paths fixed only) gives M1 1.54×/1.26× and M2 17/24 — both FAIL, so per the frozen rule "M1/M2 fail → H0 survives"; (3) the field track (H2) cannot settle H1/H0 — claiming the "H1 vs H0 verdict stands independently" risks conclusion laundering.
- **Native adjudication: SUSTAINED on all three.** verify_v2.py is inoperable as shipped (confirmed: `parse_D` seeks "D" lines, logs use "E" → ZeroDivisionError; default BIN path nonexistent; `gen()` hardcodes A1m=4 notes vs 3 pitched + 1 room in the dump → IndexError; M2 scores machine novels only; N5 "reverb on" hardcoded True). My rerun of its own m1/m2: M1 FAIL, M2 FAIL. **Filed correction:** per the frozen verdict rule, H1 (mechanism) is NOT SUPPORTED; H0 (exposure load-bearing) survives. This verdict was never written down and must be recorded; the fields amendment's "H1 vs H0 verdict stands independently" is UNSUPPORTED until it is.

### A9. M3f packet composition asymmetries
- **SOL attack:** inconsistent cells (briefs 1–2: five items; 3–4 audio: v2+field only; 5–6: v1+field only) prevent factorial interpretation — aggregates depend on which tracks appear in which briefs.
- **Native adjudication: SUSTAINED.** Confirmed in `build_blind_packet.py`. The fields amendment promised "v1 vs v2 vs field renders"; audio briefs omit v1, struct briefs omit v2. **Correction:** full factorial packet (all three tracks × all briefs) or report per-brief only, never pooled means.

## 3. CORRECTIONS FILED

1. **H1/H0 verdict (upgrade amendment):** H1 NOT SUPPORTED; H0 survives — per frozen rule (M1 1.54×/1.26× FAIL, M2 17/24 FAIL, M4 PASS). Never previously recorded.
2. **verify_v2.py inoperable as shipped:** D/E prefix bug, wrong default BIN path, gen() A1m IndexError, machine-only M2, hardcoded-True N5 check. (Scratch-fixed copies used for analysis only; repo source untouched.)
3. **Raster claim wording:** "independent implementations" → "independent rasterizer / cross-language renderer consistency check."
4. **Generative-audio claim:** native/deterministic additive audio — NOT mandate-compliant until Phase-3 head-to-head.
5. **Blind-packet blindness:** strip per-item provenance labels; move key out of packet dir; repair before any binding M3f rating.
6. **Q4 protocol:** separate-key file; neutral descriptions or render-based rating; fix 2003/1027 prose mislabels.
7. **Stale distorted audio:** v2 WAVs carry B1 rectification; field WAVs carry B1+B2 (B2 systematically disadvantages fields vs v2 in blind audio). Replace all packet audio + AVI soundtracks with corrected renders; restart affected blind ratings.
8. **M3f composition:** audio briefs omit v1; briefs 5–6 omit v2 — not a three-way design as amended. Full factorial or per-brief-only reporting.
9. **Taste-probe citation:** drop the 2/4 novel-probe line (selection-biased); keep the criterion distribution + degenerate-score proof.
10. **SHA256SUMS hygiene:** imagine.zag file hash drift (recorded 7ea9b80b… ≠ current 949addd6…; M4 behavioral guard passes — re-record); f3b1.bmp entries use relative paths that fail `sha256sum -c` (hash correct, path wrong).
11. **RUN-LOG gap:** v2 M1/M2 never recorded; crosscheck dump composition undocumented (reconstructed: `f3dump all` + `f3novel` + `f3video`).
12. **Shell-reproducibility hazard (from earlier in this sweep):** piping verifier output through `tail` masks nonzero exit codes (`echo EXIT=$?` reports the pipeline tail's status). Use `set -o pipefail` or capture status directly.

## 4. HYPOTHESES FOR OTHER TRACKS (preregistered-style, both voices)

### H-v1v2emit: v1/v2 native-emitter equivalence
- **Attacker (sol):** the native emitter (emit.zag) omits gallery text payloads ("TEXT" glyph, "NNN Hz" labels) and invents nothing — but the comparison bar is "zero differing pixels outside documented text regions." If the emitter's Pillow-port has subtle semantic drift (ellipse state machines, ROUND_UP/DOWN edge tables, round-half-to-even color mapping), the zero-pixel bar could fail for reasons unrelated to imagination quality. Preregister the text-region masks AND a pixel-diff budget for known ulp-level risks before running the comparison.
- **Native:** agree; additionally the emitter-dump-vs-logs check (#9) was not re-verified here (no emit binary committed — requires a fresh znc build). Proposed bar: decoded-RGB zero-diff outside pre-registered text bboxes; any residual diffs reported with coordinates, not hidden.

### H-M3repair: repaired blind protocol
- **Attacker (sol):** even with labels stripped, raters may recognize renderer fingerprints (BMP bilinear softness vs Pillow-crisp edges; 8 kHz vs 44.1 kHz audio). Preregister a fingerprint audit: can a held-out rater sort items by renderer above chance from a content-free probe? If yes, renderer is still confounded with track.
- **Native:** agree. Proposed protocol: full factorial (3 tracks × 6 briefs), labels stripped, key in separate file, per-brief reporting, renderer-fingerprint audit first; ratings only bind if fingerprint audit ≤ chance.

### H-H2matched: matched substrate test
- **Attacker (sol):** current H2 comparison confounds substrate with exposure, builder count, and vocabulary size. A fair test needs same briefs, same per-brief builder budget, equivalent output contracts, and normalized complexity before blind human quality.
- **Native:** agree. Proposed: freeze briefs; cap both tracks at equal stroke/element budgets; blind ratings on renders with renderer fingerprinting controlled; cross-over ablation (element builder with field vocabulary size vs field builder with element vocabulary size) to separate vocabulary-size effects from substrate effects.

### H-noLUT: non-fixed-waveform oscillator head-to-head (Phase 3)
- **Attacker (sol):** arms — (1) LUT baseline; (2) procedural breakpoint oscillator (per-cell deterministic control points, integer interp); (3) Karplus–Strong waveguide (integer delay line, seeded excitation). Bars: code audit finds no sine LUT/constants/fixed table in the audio path; waveform params generated per cell; blinded A/B/X noninferiority vs LUT (preregistered bound, e.g. ≤0.25 pts worse on 7-pt scale, ABX 95% CI upper < 55%). "Sounds equivalent" alone does NOT satisfy the literal "no hardcoding sines" order.
- **Native:** agree. Note emit.zag's Taylor-series sine already proves a no-table method is implementable in pure Zag; the Phase-3 question is oscillator *vocabulary* (fixed vs generated), not fidelity. Until this runs and Micah's ear judges, no generative-audio success claim.

## 5. FALLBACK LOG

- 23:16–23:25 PDT: grok-4.7 via stock `experientiallabs/bin/chat.py` returned ~65–72-char truncated completions on 4 consecutive probes (natural prompts). Logged as degradation; substantive work moved to gpt-5.6-sol via UnoRouter, native verification otherwise.
- **VOIDED (correction received 23:34 PDT):** the "truncations" were a TOOLING artifact — stock chat.py hard-codes `"max_tokens": 16`. All conclusions drawn from truncated grok outputs are void. In this worker's case: NO conclusions rested on grok output (all attacks re-sourced to sol or native evidence), so nothing required recapture. The grok fallback instances are reclassified as voided tooling artifacts, not model failures.
- 23:30 PDT: grok-4.7 HARD DOWN — gateway HTTP 429 insufficient_credits, org balance $−0.02. Unusable even for short outputs until Micah tops up. Fixed wrapper `~/workspace/grok47/senses/grokchat.py` noted for when service resumes.
- Sol intermittent failures during this sweep: one `NoneType` response error (retried OK), one 120-s timeout on the H2 prompt (attack completed natively instead).
- EXEMPT from hourly grok re-probe per coordinator (cron-owned).

## 6. OPEN QUESTIONS

1. **Who authorized the sine-LUT reinterpretation?** The generative amendment cites Micah's direct order as authority while reinterpreting "no hardcoding sines" as timbre-only. Was the reinterpretation itself approved, or substituted? Needs Micah's word (structural).
2. **H0-next-step:** per the frozen upgrade rule, M1/M2 fail → "next test studies exposure." No exposure-variation test is preregistered. What is the exposure manipulation?
3. **M3f/M3/Q4 rater:** all blind ratings need Micah (or an outside panel he approves). Nothing here asks him — but the repaired packets cannot bind until rated.
4. **imagine.zag hash drift:** what changed between recorded 7ea9b80b… and current 949addd6…? M4 passes, but the file-level guard needs re-recording or root-causing.
5. **v2 GEN re-runs:** never successfully scored (verifier gen() crashes on real data). "Generation intact" for v2 is unmeasured.
6. **Q1V determinism:** 5-rep byte-identical SHAs claimed in Q1V-RESULTS.md; rep logs exist — spot-verified rep1 only here.
7. **emit.zag check #9** (emitter dump vs logs/q2*.txt byte-identical): not re-verified — no emit binary committed; needs a fresh znc build (build-crew action, not analysis).

---
*Delivered: VERDICT_SHEET.md + ITEMS_DONE.tsv (39/39). Nothing committed (coordinator commits). No imagination sources built or modified; existing harnesses rerun only.*
