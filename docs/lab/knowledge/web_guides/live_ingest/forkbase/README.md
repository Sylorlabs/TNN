# LI fork-base (Wave-2 starting point)

A clean, buildable copy of the live-ingestion driver machinery at the
2026-09-23 freeze, for the Wave-2 fork crews (training-mode / unified-mode /
paraphrase-tolerant variants).

## Contents

| file | what it is |
|---|---|
| `webg.zag` | FROZEN canonical instrument source (md5 `c1ea3e71a93205dd6facf61667c3f442`). Never modify here — fork crews copy and rename. |
| `R33_NATIVE_IO_V1.zag` | the only `@import` of webg.zag |
| `guides/g1_query.txt` … `g7_bad.txt` | frozen guides G1–G7 |
| `run_forkbase.py` | minimal driver: teach → per-cluster query/select/verdict → `knowledge_ledger.txt` / `refusal_ledger.txt` / `run_li.log`. Python glue only; all reasoning is the Zag instrument. Zero RNG. |
| `fixtures_novel/` | the 60-cluster novel-facts fixture corpus (manifest, 120 authored snapshot pages, fetch-status + fidelity manifests, beacon ledger, ground truth, absence proof) |
| `expected/` | frozen measurement artifacts from the 2026-09-23 baseline (pass1) — the byte-identical target |
| `BUILD.sh` | build + fidelity proof |

## Build and run

```bash
cd ~/workspace/scratch-li-forkbase
./BUILD.sh
```

BUILD.sh does exactly five things:

1. Compiles `webg.zag` with the pinned toolchain
   (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
2. Asserts the compiled binary is byte-identical to the frozen instrument
   binary (`~/workspace/tnn-lab/knowledge/web_guides/webg`).
3. Runs the minimal driver twice over the fixture corpus.
4. Asserts pass1's ledgers + log are byte-identical to `expected/`
   (the frozen 2026-09-23 measurement: 60 clusters, 28 installed,
   32 withheld; novel INSTALL-worthy 20/44; realistic paraphrase coverage
   0/24 — the throughput gap Wave-2 must beat).
5. Asserts pass1 == pass2 byte-identically (determinism).

Manual run of the driver alone:

```bash
python3 run_forkbase.py fixtures_novel/manifest_fixtures.txt fixtures_novel/snap my_run
```

Ledger formats: `K|<kid>|<cluster>|<claim>` + `P|<kid>|<page>|<url>` lines
in `knowledge_ledger.txt`; `R|<cluster>|<gate>|<claim>|<reason>|<urls>` lines
in `refusal_ledger.txt`; per-cluster `query.out`/`select.out`/`verdict.out`
under `my_run/work/<cluster>/`.

## Forking contract (Wave-2 crews)

- `webg.zag` is frozen: do not edit it in place. Variants are new files
  (e.g. `webg_training.zag`) compiled with the same pinned toolchain.
- `run_forkbase.py` is the minimal reference driver; forks may extend it,
  but any claimed improvement must be reported against the frozen baseline:
  ≥ 20/20 Type-A installs, Type-B installs > 0, and zero installs on
  C1–C16 (single-source true, sockpuppet false, colluding false, injection).
- Keep the byte-identical reproduction property: your variant must still
  produce identical outputs across two runs (`cmp` clean) — Micah's
  no-randomness law.
