# NO-STUPID-LIMITS Crew C — L9 + L5 experiment results (2026-09-24)

Prereg: `~/workspace/scratch_10gb_work/LIMITS_AUDIT.md`.
Scratch dir: `~/workspace/scratch_10gb_work/nolimit_c/`.
Committed `gate.zag` untouched. Baseline rebuilt with the pinned toolchain
(`znc_linux_x86_64_abed8aa1`) → **SHA-identical to frozen
`dryrun/gate_bin_fixed`** (`cc75082c55a966ad8f2005d5f634c90b42fc76ca1cc13b4baea2724827c4ac97`).

Corpus for both: `l5_clean.dat` — 300,000 consecutive gate-passing records
from `dryrun_facts.dat` in stream order (73 G3 `~N` records skipped; Python
mirror of `ig_gate` predicted exactly 300,000 passes; the gate installed
exactly 300,000 with g1=g2=g3=0, lessons_rejected=0 — mirror validated
end-to-end). Zero lesson drops by construction, so installed-set differences
can only come from the variable under test.

## L9 — growable store: KILL the ncap pre-declared capacity

Variant: `gate_grow.zag` = frozen gate + `sc_store_grow()` (doubles the chunk
table: chunk_ptrs, chain, widths, clkbase; only hard stop is i32 overflow of
the chunk count — physical, load-bearing). The two `id>=ncap → -1` aborts
(gate.zag L1229/L1260) now grow instead. `sc_add`'s own `n>=cap` check can no
longer trigger (growth precedes it). Growth appends only EMPTY chunk slots;
sealed chunks, chain, events, seal are content-determined.

Runs on `l5_clean.dat` (300k records):
| run | binary | ncap | inst | seal |
|---|---|---|---|---|
| pre-sized | gate_base_bin (frozen) | 300000 | 300000 | b198622dfc9cf8608404f684b98746a665fcfc1e657c738c85aacdca57927e9f |
| grown | gate_grow_bin | 1000 → grown 9 doublings to cap=524288 | 300000 | b198622dfc9cf8608404f684b98746a665fcfc1e657c738c85aacdca57927e9f |
| grown ×2 | gate_grow_bin | 1000 | 300000 | b198622dfc9cf8608404f684b98746a665fcfc1e657c738c85aacdca57927e9f |

Kill bars:
- **Ledger identical**: blob_*.dat byte-identical (3/3 SHAs match),
  manifest.txt byte-identical (incl. seal), audit.log byte-identical.
  store.dat identical in every content field (sealed chunks, chain, events,
  seal, clock, n, nsealed); differs ONLY in capacity metadata: cap
  524288 vs 300000, nchunks 128 vs 74, trailing zero widths padding.
- **Determinism ×2**: grown vs grown-rerun `diff -r` rc=0 (byte-identical).
- **Negative control**: frozen gate with ncap=100 on a 5k-record probe
  aborts ("lesson error", rc=1) — proves the comparison exercised growth,
  not an irrelevant ncap. The 5k probe also showed grown-vs-presized
  byte-identical blobs/manifest/audit with seal 4c20055f… matching.

**Verdict: KILL L9.** A real KB grows; geometric growth yields a
byte-identical ledger modulo capacity metadata. The `ncap` abort is dead.

## L5 — lesson-size invariance: 65536 is NOT load-bearing

Variants: single-const diffs of frozen gate (`IG_LESSON` 16384 / 262144;
65536 arm = frozen `gate_base_bin`). Binaries same size (290,307 B);
diff confirms only line 34 differs.

Runs on `l5_clean.dat` (300k records, ncap=300000):
| IG_LESSON | inst | g1/g2/g3 | lessons | clock | seal |
|---|---|---|---|---|---|
| 16384 | 300000 | 0/0/0 | 19 | 19 | e0a3d690a6d932be0f1693268e4e447fd344ca81bbf53af1c23c938a649bfa27 |
| 65536 | 300000 | 0/0/0 | 5 | 5 | b198622dfc9cf8608404f684b98746a665fcfc1e657c738c85aacdca57927e9f |
| 262144 | 300000 | 0/0/0 | 2 | 2 | 199831ff3508280b0868e3cd8b6d1720d7a07c058744c120449664fb7bbe7a42 |

Kill bar — installed set identical:
- **blob_000000/1/2.dat byte-identical across all three sizes**
  (02b593369d7697a33d447b88e2fe21e35c2aba5c1ad18120c6420be35c3d2de9,
   69570db1ffaa65d7c7fc9e34243ab54dca0f67a69f2aca0241a5798f225a4336,
   ed8866855d0ce997de53f054b4a29aaeef7aacc0a905b248705767a4ed38b63c).
  Same records, same ids, same order.
- Manifests identical except lessons=/clock=/seal= lines.
- negcontrol 1000/1000 all runs; lessons_rejected=0 all runs.

Expected (prereg "modulo lesson-index audit lines"): seals differ because
`sc_seal_final` commits to the events ledger, which carries per-lesson
episode tags (lesson_idx), and per-slot clock_delta meta ticks once per
lesson. These are audit artifacts, not knowledge — the knowledge (blobs)
is byte-identical.

**Verdict: KILL L5.** Lesson size is pure batching/accounting granularity
with zero effect on what gets installed. 65536 carries no semantics.

## L7 — text lower bound A/B: in progress

Corpus `l7_corpus.dat` (200k records, deterministic truncations: 40k→10B,
22.9k→60B, rest full). Variants built: `gate_l7_1_bin` (bound 1),
`gate_base_bin` (bound 20, control), `gate_l7_100_bin` (bound 100 + CAL
must-reject R2/R4 probe texts padded to ≥100 chars so they still reach
G2/G3 — probe purpose preserved). `bad_l7.bin` (1000 recs, all texts ≥100)
keeps the frozen negcontrol expectation (500/250/250/0) valid at all three
bounds. 300 corpus-derived probe questions generated
(150 long / 75 medium / 75 short). Ingests running; panswer + scoring next.
