# FORK-BASE MANIFEST — LI Wave-2 starting point (2026-09-23)

Working base (this VM): `~/workspace/scratch-li-forkbase/`
Committed mirror: `docs/lab/knowledge/web_guides/live_ingest/forkbase/`
(byte-identical to the working base at commit time: `run_forkbase.py`,
`BUILD.sh`, `README.md`).

## Contents and identities

| file | SHA-256 / identity |
|---|---|
| `webg.zag` | FROZEN source, md5 `c1ea3e71a93205dd6facf61667c3f442`; single `@import("R33_NATIVE_IO_V1.zag")`. NOT committed (already canonical on the branch); never modified. |
| `R33_NATIVE_IO_V1.zag` | the sole import |
| `guides/g1_query.txt` … `g7_bad.txt` | frozen guides (canonical on branch) |
| `run_forkbase.py` | minimal driver (Python glue; all reasoning is the Zag instrument; zero RNG) |
| `fixtures_novel/` | 60-cluster novel-facts fixture corpus: `manifest_fixtures.txt`, 120 snapshot pages under `snap/` (+ `manifest_fetch_status.txt`, `snapshot_fidelity.txt`), `beacon_ledger.txt`, `ground_truth.md`, `absence_proof.md`, `absence_probes.txt` |
| `expected/` | frozen measurement reference: `knowledge_ledger.txt` (SHA-256 `a5988c819f7eae8e283cfb78a935b174c02f8268480108ec50942376716271cf`), `refusal_ledger.txt` (`7c733cabe3bf4c7442dd89a20f0042136fc8d6f3827bbe2373d39360564b7909`), `run_li.log` (`81f408822c7268cced42f4200df1e627016066f4e2fb9d249d6c7b24420876eb`) |
| `BUILD.sh` | pinned-toolchain build + fidelity proof |
| `README.md` | exact build/run commands + Wave-2 forking contract |

## Proven by BUILD.sh (2026-09-23, this VM)

1. `znc_linux_x86_64_abed8aa1 webg.zag -o webg` → compiled binary
   **byte-identical** (`cmp` clean) to the frozen instrument binary
   `~/workspace/tnn-lab/knowledge/web_guides/webg`.
2. Minimal driver, two passes over `fixtures_novel/`: both emitted
   `DONE|clusters=60|installed=28|withheld=32|` with log/knowledge/refusal
   SHAs exactly `81f40882…` / `a5988c81…` / `7c733cab…`.
3. `cmp` clean: pass1 vs `expected/` (all three files), pass1 vs pass2
   (all three files).

The minimal driver is therefore proven output-equivalent to the frozen
branch driver on the fixture corpus, and deterministic across runs.

## Frozen baseline numbers (from MEASUREMENT_NF.md)

- 60 clusters: 28 installed, 32 withheld.
- Novel INSTALL-worthy installed: 20/44 (Type A 20/20, Type B 0/24).
- Realistic paraphrase coverage installs: 0/24 — the throughput gap.
- Expected integrity holes on the frozen instrument: 8 false installs
  (C5–C12: same-host sockpuppet, distinct-host collusion).
- Injection pages (C13–C16): all flagged, all withheld.
- Prereg `PREREG_LI_NF.md` predictions P1–P6: all HOLD.

## Wave-2 forking contract

- `webg.zag` stays frozen in place; variants are new files compiled with the
  same pinned toolchain.
- Beat the baseline: ≥ 20/20 Type-A, Type-B installs > 0, zero installs on
  C1–C16.
- Keep byte-identical determinism (`cmp` clean across two runs).
