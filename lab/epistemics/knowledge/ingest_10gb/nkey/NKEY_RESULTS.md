# N-KEY INVESTIGATION — results (interim, 2026-09-24)

Task: investigate the `~N` key problem; run the dry ingestion; test three
resolutions head-to-head (admit `~N` / skip rejected in CAL / re-key upstream);
cherry-picked subsets; preregistered bars; pure Zag; byte-identical reruns.
Prereg: `NKEY_PREREG.md` (+ amendments A1/A2/A3, 2026-09-24 ~17:05 UTC).

## 1. Root cause (established)

- `clean2.py::r9_emit_unit` splits >4096-byte Stack Exchange posts into
  ≤4096-byte chunks keyed `se:<site>:<q|a>:<id>~N`. `~N` = source-generated
  chunk provenance, not malformed input.
- `gate.zag::ig_se_key_ok` (frozen G3) requires all-digits after the post
  id → every `~N` key → G3 reject. Spec-compliant rejection; the SOURCE and
  GATE contracts disagree.
- No downstream consumer parses the post id numerically (G2 = byte equality,
  merge/sindex = byte order, retrieval = citation display). The digits-only
  rule serves no demonstrated integrity function.
- Lesson CAL takes the FIRST 4 records of each 65,536-record lesson as
  must-accept probes; any probe failing the gate drops the WHOLE lesson.
  Dry run: 3 lessons (84, 116, 124) dropped = 196,608 records (2.1%) lost
  because a lesson-head record carried a `~N` key. CP2 isolated lesson 84
  (cp2 lesson 0): V1 installed all 65,536 with g3=0 — the lesson was
  PERFECT except for one key-grammar technicality at its head.

## 2. Corpus measurements (nkey_probe.py, full 9,327,214-record corpus)

- Tilde-keyed records: 117,470 (kind 6: 91,866; kind 7: 25,345; kind 5: 259).
- Kind-6 tilde concentration: math 62,273; physics 24,508; chemistry 2,925;
  biology 2,160. All 91,866 fail current `ig_se_key_ok`; all match `~N`
  shape (0 malformed); max chunk index 9.
- Probe prediction: admitting optional `~N` → 90,167 installable;
  1,699 question-continuations still fail the separate `"\n\n"` rule; 0 G1.
- Non-kind-6 tilde: kind-5/7 grammars ALREADY admit `~` (V0 installed
  23,434 of 25,604; the other 2,170 are single-token texts failing the
  multi-word G3 rule — variant-independent).

## 3. Variants (all scratch-only; committed gate.zag untouched)

- **V0**: rebuilt committed gate.zag, pinned znc; byte-identical to
  dryrun/gate_bin_fixed (SHA cc75082c…).
- **V1** (`gate_v1.zag`): `ig_se_key_ok` admits one `~N` (N=1+ digits).
  Malformed `~` still rejected. Smoke-tested.
- **V2** (`gate_v2.zag`): lesson-CAL uses a 256-record peek window with a
  local prev-chain copy; lesson proceeds iff ≥4 window records pass the
  gate (stuck-gate canary; reject mask bit 8 = 256+nacc). Final partial
  lesson keeps V0 semantics. Must-reject probes unchanged. Per-record
  install gating UNCHANGED (`~N` still individually G3'd). Smoke-tested:
  V0 dropped a 10-record lesson (mask=3), V2 installed 6 / G3'd 4.
- **V3** (upstream re-key, no gate change): kind-6
  `se:<site>:<q|a>:<id>~<n>` → `se:<site>:<q|a>:<10^12+id*10000+n>`
  (injective for id<10^12, n<10000; corpus max id 4,890,949, max n 9).
  Provenance arithmetically recoverable. One streaming pass re-sorts
  (chunks sort after genuine records in their (site,q/a) group).

## 4. Cherry-pick results

### CP1 — tilde-only micro-corpus (117,470 records), teach per variant

| variant | installed | g3 | lessons_rej | note |
|---|---|---|---|---|
| V0 | 23,434 | 42,102 | 1 (mask=15) | lesson 1 (all kind-6 tilde) dropped |
| V1 | 113,601 | 3,869 | 0 | kind-6 admitted: 90,167 = probe prediction EXACT |
| V2 | 23,434 | 42,102 | 1 (mask=256) | canary fires on the all-reject lesson — correct |
| V3+V0 gate | 113,601 | 3,869 | 0 | IDENTICAL counts to V1 (lesson splits match too) |

negcontrol 1000/1000 all runs. V1's kind-6 installs (90,167) match the
probe prediction to the record.

### CP2 — the 3 dropped lessons (196,608 records), teach per variant

| variant | installed | g3 | lessons_rej | note |
|---|---|---|---|---|
| V0 | 0 | 0 | 3 (masks 8,8,7) | catastrophe reproduced in isolation |
| V1 | 196,478 | 130 | 0 | lessons rescued AND tilde admitted |
| V2 | 194,478 | 2,130 | 0 | lessons rescued; 2,000 tilde records individually G3'd |

V1−V2 = 2,000 = the tilde records in these lessons (all admittable).
V2 rescues 194,478 good records the frozen gate drops.

## 5. Head-to-head (interim)

| | V0 (frozen) | V1 (admit ~N) | V2 (CAL skip) | V3 (re-key) |
|---|---|---|---|---|
| gate change | none | G3 grammar +`~N` | CAL selection only | none |
| source change | none | none | none | re-key + re-sort pass |
| tilde records installed | 0 (kind-6) | 90,167 | 0 (kind-6) | 90,167 |
| lessons lost to `~N` heads | 3 (196,608 rec) | 0 | 0 | 0 |
| provenance | n/a | transparent (`~0`) | n/a | opaque (arithmetic decode) |
| new assumptions | none | none | 256-window canary | id<10^12, n<10^4 |
| governance | — | spec amendment | CAL change | pipeline change |

V1 vs V3 is the real contest: identical coverage (proven on CP1), and the
choice reduces to transparent-provenance + spec amendment (V1) vs
opaque-keys + silent-collision fragility if upstream ids ever exceed the
bounds (V3). V2 is orthogonal: it fixes the LESSON-DROP catastrophe
without touching key semantics (and composes with V1).

## 6. Pending

- Full-corpus teaches: V0×1 (rebuild validation), V1×2, V2×2, V3×1
  (background job `nkey_fullrun.sh`, started 17:27 UTC; ~4h on contended box).
- Determinism: manifest + aggregate-SHA comparison per A2.
- Bar 4 exact-match checks against probe predictions.
- Final NKEY_INVESTIGATION.md + commit (docs/sources only).

## 7. Preregistered full-corpus predictions (locked before runs land)

Baseline (dry run, V0): n=9,030,226, g1=9, g2=0, g3=100,371,
lessons_rejected=3, seal=43d7e5cc262755a837b2984858db309560eaadcc2339e7e8481a0a51d44542fd.

- V1: n = 9,030,226 + 90,167 = **9,120,393** EXACT
  (90,167 = probe-predicted admittable kind-6 tilde; kind-5/7 unchanged).
- V2: n = 9,030,226 + 192,478 = **9,222,704** EXACT
  (192,478 = CP2-measured good non-tilde records in the 3 rescued lessons:
  194,478 installed − 2,000 tilde).
- V3: n = V1 n = **9,120,393** EXACT (same admitted set, re-keyed).
- lessons_rejected: V1=0, V2=0, V3=0 (V0=3).
- G1/G2 within ±0.1% of V0 (g1=9, g2=0) for all variants.
- negcontrol 1000/1000 every run.
