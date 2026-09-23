# VERDICT.md — T2-TRACKA: Representation Track A closeout (replacement crew)

## 0. Frozen prereg (exact, T2-TRACKA section of `docs/lab/crossref/PREREG_TIER2.md`)

> **Claims:** closeout verdict `1706708005a9`: provisional champion Y5 (cross-stream span sets) → tokenizer replacement; 16 killed / 20 pass / 13 provisional / 3 unadjudicated; Y5's blowout restored (7/8 decided, Y5 1.659 vs U 2.902 cost, 74.9% margin); B-family: B-8 retired, B-16/B-64 survive; F-B, R2, I1 killed; G2 KILLED (binding criterion: recall-quality advantage <2 pts over G1); K1 KILLED (kill (ii)); U PASS (binding); T KILLED (degenerates exactly to X); arm R KILLED (`76849610b8` — OR-kill M1 clause; boundary metric beat baseline ≥10 pts on both corpora but M1 recall tied baseline at 100% ceiling); C-W PASS, F-S SURVIVES, H1 COMPLETE (1× M1–M9 double-run byte-identical), I1 SURVIVES, N PASS, R build SUCCESS, C-P PASS; D-family provisional (thesis-critical, no scorecard); V never built; 10× legs blocked by znc 2^25 slice wall; frozen spec actually 52 arms (the '53 ratified' footer was an arithmetic error).
>
> **Method:** Type C — re-derive the verdict sheet from committed arm evidence; verify a sample of kill/pass applications (at least Y5's 7/8, the R kill's M1 clause, G2's <2pt binding, T→X degeneration) with independent Zag checks; confirm D-family provisional status and the 52-arm correction.
>
> **Rule:** REPRODUCED if the body count (16/20/13/3) and sampled applications re-derive; NOT REPRODUCED if any binding kill is misapplied; PARTIAL if provisional arms' status is ambiguous (name them).

## 1. Overall verdict: **REPRODUCED** (with documented corrections)

The body count **16 / 20 / 13 / 3** re-derives textually from the pinned closeout verdict
`1706708005a9`; Y5's **7/8** championship re-derives via an independent Zag check
(3× byte-identical, `VERIFY=PASS`); every sampled kill/pass application (R, G2, T, K1, I1)
is correctly applied per committed evidence; the 52-arm correction verifies; D-family
provisional status is confirmed unambiguous. **No binding kill is misapplied.**

**Corrections to prereg phrasing (do not change the verdict):** the prereg's "I1 SURVIVES"
is stale — final committed evidence says **I1 KILLED** (see §2); "F-S SURVIVES" overstates —
F-S is **PROVISIONAL** (kill (iii) blocked on D); "10× legs blocked" overstates — Y5's 10×
leg is **complete/confirmed** at frozen head (`f225a71f`); Y5 was "provisional" at the pinned
10:05 snapshot but is **CONFIRMED** at frozen head.

## 2. I1 adjudication — resolved from committed evidence (not punted)

**I1 = KILLED.** The prereg contains an internal contradiction ("F-B, R2, I1 killed" vs
"I1 SURVIVES"); committed evidence resolves it decisively:

| Commit | Date (PDT) | I1 status |
|---|---|---|
| `8feb65b` | 2026-09-21 00:09 | survives all kill criteria (early verdict) |
| `3af67c0` | 2026-09-21 03:46 | kill (ii) SURVIVE (512-unit synthetic corpus, L1-only chunks) |
| `1706708` (= `1706708005a9`) | 2026-09-21 10:05 | **PROVISIONAL** (consolidated sheet) |
| **`0741530`** | 2026-09-21 14:05 | **KILLED by binding kill (ii)** — final arm verdict |

Deciding evidence (`0741530`, ancestor of frozen head, file unchanged to frozen head):
prose maintenance-churn audit **24,164 / 109,295 = 22.1%**, exceeding the frozen **20%**
kill bar → kill (ii) fires. The earlier 12.4% "survive" came from a 512-unit synthetic
corpus that formed only L1 chunks; the final verdict explicitly supersedes it. Kill (i)
survived (full hierarchy, 84,731/84,731 byte-exact recall); kill (iii) remained blocked
(no frozen operational definition of "natural breaks") — not needed for the binding verdict.
The prereg's "I1 SURVIVES" matches only the superseded `8feb65b`; the prereg's own
"F-B, R2, I1 killed" is the correct phrase.

## 3. Claim-by-claim vs measured evidence

| Prereg claim | Committed evidence | Assessment |
|---|---|---|
| Body count 16 killed / 20 pass / 13 provisional / 3 unadjudicated | Pinned verdict `1706708` (10:05) textually states 16/20/13/3 | **REPRODUCED** (from pinned source) |
| Y5 provisional champion, 7/8 decided | Independent Zag re-derivation: Y5 wins M1-content, M1-boundary, M2, M3, M4, M6-tax, M7; L1 wins M5 (`VERIFY=PASS`, 3× byte-identical SHA `170d6cee…f68`) | **REPRODUCED** |
| Y5 1.659 vs U 2.902, 74.9% margin | Zag recomputed from raw integers: ((17260−8304)×1024+6563843)/5422721→2.902; ((33724−26236)×1024+1327320)/5422721→1.659; (2.902−1.659)/1.659→74.9% | **REPRODUCED** |
| R KILLED (`76849610b8`, OR-kill M1 clause) | Verdict: boundary +23.1/+16.9 (≥10 both) but M1 recall 100.0 vs 100.0 → clause 2 fires; Zag re-derived kill=TRUE | **REPRODUCED** |
| G2 KILLED (<2pt binding) | G1 100.0 vs G2 100.0, advantage 0.0 < 2 → kill; Zag TRUE | **REPRODUCED** |
| T KILLED (degenerates to X) | B2 T/X = 1.000000 both corpora; 13,000/13,000 sub-episode; beats X 0/4 → criteria (i),(ii),(iv) fire; Zag TRUE | **REPRODUCED** |
| K1 KILLED (kill (ii)) | Chain 20.00>8, latency 9.99×>2× → fires; Zag TRUE | **REPRODUCED** |
| U PASS (binding) | `9c6d938` (2026-09-21 13:27); adjudicated M1 100.0/99.9, M4 93.0/100.0 | **REPRODUCED** |
| F-B, R2 killed | F-B killed `d2c35d7` (within noise of F-S); R2 killed per sheet | **REPRODUCED** |
| I1 SURVIVES | Final verdict `0741530`: **KILLED** (kill ii, 22.1%>20%) | **STALE — corrected to KILLED** |
| F-S SURVIVES | Final verdict: **PROVISIONAL** (kill iii blocked on D) | **OVERSTATED — corrected to PROVISIONAL** |
| H1 COMPLETE (M1–M9 double-run byte-identical) | Sheet §10; scorecard `M8GATE PASS` | **REPRODUCED** |
| C-W PASS / C-P PASS / N PASS / R build SUCCESS | Sheet body counts; N verdict-only PASS (no metrics scorecard) | **REPRODUCED** |
| B-8 retired; B-16/B-64 survive | Sheet B-family rows | **REPRODUCED** |
| D-family provisional, thesis-critical, no scorecard | No D scorecard in closeout dir; D/D-R/D-T provisional per verdicts | **REPRODUCED** (unambiguous, not PARTIAL-triggering) |
| V never built | No V scorecard or verdict | **REPRODUCED** |
| 10× legs blocked by znc 2^25 slice wall | Y5 10× **complete** at `f225a71f` (frozen head); N/others blocked | **PARTIALLY STALE** — Y5 escaped the wall |
| 52 arms (footer arithmetic error) | 49 §3 rows; B→3, C→2 → **52**; footer "48 rows→53" wrong on its own terms | **REPRODUCED** |

Note on later amendments: the frozen-head sheet textually counts 17/21/11/3 (F-B killed later,
N promoted to PASS, Y5 confirmed). The prereg's 16/20/13/3 describes the **pinned**
`1706708005a9` snapshot, from which it re-derives exactly.

## 4. Frozen pins

- Repo/branch: `sylorlabs/TNN`, `tnn-native-lab`
- Frozen commit: `7b2100d09911c5c10252c5756c7def288e70bd1f` (working tree verified clean here)
- Prereg: `docs/lab/crossref/PREREG_TIER2.md`, section T2-TRACKA
- Closeout verdict: `1706708005a9` → `1706708005a9a348cb710f6e2a65427ae700cc1e` (GitHub API: resolves)
- Arm R kill: `76849610b8` → `76849610b897075bfcbc6201c0a7e55f70480f00` (GitHub API: resolves)
- I1 final: `074153044897cdffa2b8971d2ee435057c4a59ab`
- ~~Brief pin `02ffbc1be27a`~~ — **transcription artifact per coordinator PIN CORRECTION; disregarded** (422 "No commit found"; see RUNLOG §1)

## 5. Method note

Type C committed-evidence re-derivation. No batteries executed (not required by method;
evidence already committed). Independent Zag verifier `verify_tracka.zag` (generated by
`gen_verify.py`, glue) re-derived the §7 championship, the M5 harmonization arithmetic,
and five kill applications with pure-Zag logic, zero RNG, 3× byte-identical runs
(SHA-256 `170d6cee8cbafd983e0e5720694952f8de6685a8729675303be98a3f34148f68`).
Toolchain: pinned `znc_linux_x86_64_abed8aa1`. Full provenance in `RUNLOG.md`.
