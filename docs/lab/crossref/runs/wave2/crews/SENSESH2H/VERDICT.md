# T2-SENSESH2H — VERDICT (replication crew, replacement)

**Trial:** senses rebuild head-to-head — Approach A (LLM-style raw values) vs Approach B (human-style qualitative percepts).
**Type:** A — full rerun from committed sources in a clean checkout.
**Crew:** T2-SENSESH2H (REPLACEMENT — predecessor killed mid-run by runtime daemon restart; full fresh rerun, no inherited results).
**Date:** 2026-09-23.

## Frozen prereg (authoritative — quoted verbatim, extracted from commit 7b2100d09911c5c10252c5756c7def288e70bd1f, docs/lab/crossref/PREREG_TIER2.md)

> ## T2-SENSESH2H — senses rebuild head-to-head: raw values win, both fail memory (Type A)
>
> **Claims:** commit `84df6dc24483`: raw-values (LLM-style) viability 72.6% PASS vs qualitative percepts (human-style) 54.0% FAIL — 18.6pp win, percept approach killed by its own bar; both 60/60 byte-identical; both FAILED memory integration (false installs 59.0% vs 55.0%); shared install rule failed against high-confidence wrong percepts (79/134 false installs A, 72/131 B) — backs 'truthful but sensor-deceivable'.
> **Method:** rerun the head-to-head from committed sources in clean checkout; ≥3 byte-identical.
> **Rule:** REPRODUCED if 72.6% vs 54.0%, 60/60 byte-identical, both fail memory integration at ~59%/55%, install-rule failure counts match; NOT REPRODUCED if percepts cross 60% or either passes memory integration.

## Pins (frozen before any run)

| Item | Value |
|---|---|
| Frozen prereg commit | `7b2100d09911c5c10252c5756c7def288e70bd1f` (branch tnn-native-lab) |
| Trial commit (pin) | `84df6dc244836848decdf3d76d9796cd60f91269` — detached HEAD, `git status` clean, `git fsck` clean |
| znc | `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` |
| Build flags (frozen) | `znc <src> --no-zagd --no-analyze --no-foreground-cache -o <bin>` |

## Verdict: **REPRODUCED**

Every claimed figure re-derived from a clean-checkout rerun. The replicated metrics.json is deeply identical
(field-by-field, float-exact) to the committed `harness/results/metrics.json` — zero mismatches across all
per-task accuracies, ops counts, robustness figures, memory streams, and determinism records.

## Claims checklist — claimed vs measured

| # | Frozen claim | Measured (rerun) | Check |
|---|---|---|---|
| 1 | A viability 72.6% PASS (KB1 ≥ 60%) | 72.6389% → **72.6% PASS** | ✓ |
| 2 | B viability 54.0% FAIL (KB1) | 54.0278% → **54.0% FAIL** — percept approach killed by its own bar | ✓ |
| 3 | 18.6pp win (KB2, no tie) | 72.6389 − 54.0278 = **18.611pp → 18.6pp** | ✓ |
| 4 | Both 60/60 byte-identical (KB5) | A 60/60, B 60/60 stdout-identical ×3 runs; 3 full pipeline runs byte-identical (raw_results.json SHA-256 equal) | ✓ |
| 5 | A memory integration FAIL: 59.0% false installs | 79/134 = **58.955% → 59.0% FAIL** (560 withholds) | ✓ |
| 6 | B memory integration FAIL: 55.0% false installs | 72/131 = **54.962% → 55.0% FAIL** (440 withholds) | ✓ |
| 7 | Install-rule failure counts: 79/134 A, 72/131 B | **79/134 A, 72/131 B** exactly | ✓ |
| 8 | NOT-REPRODUCED triggers: percepts cross 60% / either passes memory integration | B at 54.0% (6.0pp below bar); neither passes KB4 (both > 10% bar by ~45–49pp) | not triggered |

Kill decisions re-derive: **B KILLED (KB1)**; **A WINS head-to-head (KB2), not fragile (KB3: A adv drop 20.9pp ≤ 25pp; B 8.3pp), but FAILS KB4** — A not cleared for direct deliberate-memory wiring. The 'truthful but sensor-deceivable' qualifier is backed: the shared install rule withholds heavily (560/440) yet cannot stop high-confidence wrong percepts.

## Supporting figures (measured, all matching committed metrics.json)

Per-task primary accuracy (A / B): colordisc 48.3/40.0, colorconst 87.5/62.5, shapetrans 100/40.0,
pitchdisc 83.3/78.3, timbredisc 75.0/75.0 (tie), motiondir 41.7/28.3.
Ops totals: A 1,034,699,124 (~1.03B), B 428,070,933 (~428M) — B 2.42× cheaper, does not overcome KB1.
Noise accuracy: A 71.7%, B 53.8%. Adversarial accuracy: A 51.7%, B 45.7%.
Known runner error re-observed: A exited 1 (`task_failed`) on `t3_shapetrans/adversarial/p042.img` (truth=TRIANGLE) — same as the original run's honest caveat; A's shape-adv n=44.

## Replication method (Type A)

1. Clean clone (blob:none) of sylorlabs/TNN at pin 84df6dc, sparse to `docs/lab/senses/rebuild/`; status clean, fsck clean.
2. Sources copied to scratch and sha256-verified byte-identical to committed blobs; rebuilt with frozen flags
   (cwd = source dir per znc's cwd-relative `@import`; B's `../../tnn-lab/toolchain/R33_NATIVE_IO_V1.zag` resolved
   against a mirror of the committed copy, byte-identical to the live toolchain file the original crew used).
   - `sense_a`: 88191 bytes main — exact size match to A BUILD_LOG.
   - `sense_b`: 94129 bytes main, md5 `e6c98d091bbb0f90f54936b46bf849d8` — **exact md5 match** to B BUILD_LOG.
   - Rebuilds of both byte-identical (deterministic compiler). B boundary proof `znc check percept.zag` → OK.
3. Fixtures regenerated via committed `gen.py` (master seed 20260921); 170 picsum photos verified against committed
   `MANIFEST.sha256` (all 170 OK — 6 seeds serve small-but-valid JPEGs under gen.py's 2000-byte guard; each hashes
   exactly to the manifest). **All 2020 manifest entries (925 fixtures + 925 truths + 170 photos) verify OK** —
   the end-to-end regeneration the original VERDICT left unverified now IS verified byte-identical.
4. `run.py --no-wait` + `score.py` (committed, sha256-verified copies) with SENSE_A/SENSE_B; compared to committed metrics.json.
5. Pure Zag for all reasoning/verification; zero RNG anywhere; no binaries or .zagd committed; TMPDIR under workspace, never /tmp.

## Byte-identity evidence (≥3 runs)

| Run | raw_results.json SHA-256 |
|---|---|
| 1 | `aa91f3a1af0ee42de5229b93a371c5d8efb5ffd5c99bc8b28398bdefd9a2fc0a` |
| 2 | `aa91f3a1af0ee42de5229b93a371c5d8efb5ffd5c99bc8b28398bdefd9a2fc0a` |
| 3 | `aa91f3a1af0ee42de5229b93a371c5d8efb5ffd5c99bc8b28398bdefd9a2fc0a` |

Three full pipeline runs byte-identical. (Plus the runner's internal KB5 sample: 60 fixtures × 3 runs each, both approaches.)

## Incidents (recorded, none hidden)

1. Predecessor's full-tree checkout died mid-fetch (git-remote-https SIGKILLed, OOM) and the `clean/repo` dir was found
   deleted; cause undetermined. Recovered with a fresh blob:none clone + sparse checkout of the trial subtree; all
   pins and integrity re-verified. No results were inherited (predecessor left none).
2. gen.py's photo-fetch `> 2000`-byte guard rejects 6 picsum seeds' small-but-valid JPEGs; each downloaded directly
   and verified against the committed manifest (all 6 exact matches). No fixture drift.
3. A concurrent unrelated workstream (`~/workspace/h3work`, timbredisc) shares the VM; no interference either way.

## Deliverables

- `~/workspace/scratch-crossref/T2/SENSESH2H/crew/VERDICT.md` (this file)
- `~/workspace/scratch-crossref/T2/SENSESH2H/crew/RUNLOG.md`
- Evidence in crew dir: `build/` (rebuilt binaries + verified source mirrors), `harness/` (byte-verified script copies,
  regenerated fixtures, results incl. `raw_results_run{1,2,3}.json`, `metrics_run{1,2,3}.json`, per-run SHA-256 log).
