# T2-SCALEDOWN replication — RUNLOG

Crew: T2-SCALEDOWN (subagent session 556eeaf3-8e53-400b-96c3-941462ecde76),
Wave 2 Tier 2 cross-reference program, authorized by Micah's 2026-09-22
"run everything" ruling. Type A (full independent rerun).

## Frozen pins (recorded BEFORE running)

| Item | Pin |
|---|---|
| Cross-ref prereg (SCOPE.md + PREREG_TIER2.md) | commit `7b2100d09911c5c10252c5756c7def288e70bd1f` (branch tnn-native-lab; SCOPE/PREREG_TIER2 read from this commit via raw.githubusercontent.com; note: `docs/lab/crossref/` does not exist at the evidence commit, it was added later) |
| Scale-down evidence + claims | commit `2d367807d806fac7a23e26375b32c5dea0600ebe` ("scale: few-shot / scale-down verdict — no floor; one-shot learning works (docs/lab/scale/fewshot/)", 2026-09-22T02:20:29Z) — matches the expected `2d367807d806` prefix ✓ |
| znc toolchain | `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned lab build) |
| Driver source | `docs/lab/scale/fewshot/driver/fewshot_learner.zag` @ 2d36780, md5 `a9d3aa95c842605bdcd18df6d693cda2` |
| Cross-ref oracle | `docs/lab/scale/fewshot/runs/identity.txt` @ 2d36780 (md5 of the 5 concatenated timing-stripped logs per leg) + the 70 committed `runs/n*_r{0..4}.log` |

## Clean environment

- Fresh sparse checkout at `~/workspace/scratch-crossref/T2/SCALEDOWN/clean/`
  (`git init` + `git fetch --depth 1 --filter=blob:none origin 2d36780...`
  + sparse `docs/lab/scale`, `docs/lab/crossref`; `git rev-parse HEAD`
  = `2d367807d806fac7a23e26375b32c5dea0600ebe`). No files from any other
  crew's directories; nothing copied except the single `.zag` source.
- Run/build dir: `~/workspace/scratch-crossref/T2/SCALEDOWN/crew/` (scratch,
  never `/tmp`; `TMPDIR=~/workspace/tmp_commit`).
- Binary rebuilt from source with the pinned znc:
  `znc fewshot_learner.zag -o fewshot_learner --no-analyze`
  → `fewshot_learner` (124328 bytes, native x86-64 ELF). No `.zagd` or
  binary copies from anywhere.

## Corpus reconstruction (inputs not committed — byte-verified)

At 2d36780 the corpus runtime inputs are NOT committed: `texts/text_<t>.txt`
(10 Gutenberg texts), `texts/index_<t>.tnix` (frozen binary indexes), and
`texts/meta.json` are absent from the tree (only FACTSPEC.md, MANIFEST.json,
NORMALIZE.md, SHA256SUMS.txt are committed). The driver's `sc_corpus_init`
requires all three at runtime.

Reconstruction path (documented, deterministic, zero RNG):
1. Downloaded the 10 texts from the exact `source_url`s in the committed
   MANIFEST.json (gutenberg.org; server repeatedly reset connections
   mid-transfer — curl rc=18 — so resume+retry until complete).
   Gate: sha256 of every file matches the pinned MANIFEST.json sha256 —
   **10/10 MATCH** (text sizes 151191–1234613 bytes).
2. Re-derived `index_<t>.tnix` with an independent Python implementation of
   the frozen NORMALIZE.md §§0–7 (`crew/build_tnix.py`): UTF-8 strict decode,
   ASCII-only lowercase, maximal `[a-z]+` words, single-pass `[.?!]`-run
   sentences, blank-line paragraphs, word_sent/word_para/sent_para maps
   (incl. the §7 forward-scan refinement), then the §6 binary layout
   (magic `TNIX0001`, u64 LE counts, u32 LE arrays).
   Gate: sha256 of every produced `.tnix` vs the committed
   `docs/lab/scale/corpus/SHA256SUMS.txt` — **10/10 BYTE-IDENTICAL**.
   Word counts also match MANIFEST.json exactly
   (128577/219066/75340/27439/108924/138502/163413/162111/189616/119380).
   Note: NORMALIZE.md §7's worked example is internally inconsistent
   (claims N=11 for a 13-char string); the implementation follows the
   literal §3/§4 algorithms, and the committed sha256s confirm it exactly.
3. Synthesized `texts/meta.json` from the committed MANIFEST.json
   (10 × {pub_year, title_words}; title_words = whitespace-separated tokens
   of the catalog title, per FACTSPEC.md §3 c23). The driver's parser only
   scans `"pub_year"`/`"title_words"` keys, so this is behavior-identical
   provided the values match the original — verified downstream by the
   byte-identical run digests (categories 22/23 are taught at N=192).

## Runs

Adapted the committed `driver/run_ladder.sh` to the crew dir (same argv
convention `./fewshot_learner eval N C M P rep TEXTS OFF`, P=1), 6 legs:

| leg | N | C | M | off |
|---|---|---|---|---|
| n192 | 192 | 24 | 8 | 0 |
| n008 | 8 | 8 | 1 | 0 |
| n002 | 2 | 2 | 1 | 0 |
| n001 | 1 | 1 | 1 | 0 |
| n001_plant | 1 | 1 | 1 | 6 |
| n002_mixed | 2 | 2 | 1 | 5 |

5 reps per leg (30 runs), each log kept at `crew/runs/<lbl>_r<r>.log`.

## Results vs committed claims (commit 2d367807d806)

Byte-identity: all 30 run logs are byte-identical (log minus the wall-clock
`SCALE_RECALL_TIMING` line) to the 70 committed logs — 0 diffs in 30/30
rep-vs-committed-r0 comparisons. `SCALE_DIGEST` fnv1a matches the committed
value at all 6 legs. The committed `runs/identity.txt` md5s (computed over
the 5 concatenated timing-stripped logs) reproduce EXACTLY when the original
crew's absolute run-dir path (`/home/hatch/workspace/scale-fewshot/runs/`,
embedded by grep's multi-file `filename:` prefixes) is simulated —
explaining why a naive re-run of their script in a different directory
yields different hashes. (Minor note: their `nhash` computation always
prints `nhash=1` since it md5s the concatenation once; the real check is
the hash value itself.)

| leg | clean mastery | all-fact | absorption | flaw | ops/fact | B/fact | digest | verdict claim |
|---|---|---|---|---|---|---|---|---|
| n192 | 179/179 = 1.0000 | 0.9323 | 13/13 | 96/96 | 4.005 | 92 | match | match |
| n008 | 7/7 = 1.0000 | 0.8750 | 1/1 | 96/96 | 4.125 | 100 | match | match |
| n002 | 2/2 = 1.0000 | 1.0000 | N/A (no plant) | 96/96* | 4.500 | 124 | match | match |
| n001 | 1/1 = 1.0000 | 1.0000 | N/A (no plant) | 96/96* | 5.000 | 156 | match | match |
| n001_plant | 0/0 (fact is the plant) | 0.0000 | 1/1 | 96/96* | 5.000 | 156 | match | match |
| n002_mixed | 1/1 = 1.0000 | 0.5000 | 1/1 | 96/96* | 4.500 | 124 | match | match |

\* Flaw battery degenerates below N=96 (probe ids collide) — the committed
caveat reproduces as-is (e.g. N=1: 4 families × 24 repeated probes of the
single fact).

- One-shot: N=1 clean HELD 1/1; N=1 plant ABSORBED 1/1 as supplied;
  N=2 mixed BOTH correct (clean 1/1 as truth, plant 1/1 as supplied). ✓
- N=240 validation (P=3, 3 reps, the fewshot PREREG's gate config):
  3/3 byte-identical (stripped); clean 226/226, all-fact 0.9417,
  absorption 14/14, flaw 96/96 — all match the scale-up VERDICT N=240 row.
  (The gate's literal target, byte-identity with `run240_r0.log`, cannot be
  checked: that file is referenced in the fewshot PREREG but was never
  committed at 2d36780 — a gap in the committed record, not a divergence.)
- Recall latency (min-of-N estimator, wall-clock, same in-driver
  microbenchmark: 2000 sweeps × n `sc_recall`, CLOCK_MONOTONIC):

| leg | reps | min ns/probe | committed min |
|---|---|---|---|
| n192 | 10 | 376.9 | 205 |
| n008 | 14 | 279.7 | 179 |
| n002 | 10 | 173.4 | 171 |
| n001 | 5 | 173.2 | 178 |
| n001_plant | 5 | 173.2 | 179 |
| n002_mixed | 5 | 185.6 | 175 |

Range 173–377 ns (0.17–0.38 µs), vs committed 171–412 ns. Constant in N:
no monotonic N-dependence (n008's min < n192's min); the spread mirrors the
committed data's own 2.4× spread. 10–20× faster than install holds
(4.2 µs / 0.17–0.38 µs ≈ 11–24×). Caveat: this VM was heavily contended
during the runs (load average 15–24 on 2 vCPUs from other live
workstreams); early n008/n002 samples were inflated 5–10× and only quiet
moments (extra reps) reached the true floor — the original verdict's own
"wall-clock on a shared VM; treat as measured, not byte-identical" caveat
applies verbatim.

## identity.txt cross-check (finding)

The committed `runs/identity.txt` hashes did NOT reproduce with a naive
re-run of the ladder script in a different directory — because the script's
hash is `md5(grep -v SCALE_RECALL_TIMING "$RDIR/${LBL}_r"*.log)`, and GNU
grep with multiple files prefixes every line with the filename **as given
on the command line**, i.e. the original crew's absolute
`/home/hatch/workspace/scale-fewshot/runs/...` path is hashed into the
value. Simulating those exact prefixes over my byte-identical logs
reproduces all six committed md5s exactly
(n192 `2362189517ee23b95bd8f763e0096687`,
n008 `a1e60e4f0b8a7d3dc1988048610519c0`,
n002 `afafacab3bb71c294fd22983187d0eb9`,
n001 `b71a40c3101f8b1c67452f654fceeb0a`,
n001_plant `933674898ccc55f054028b586e1d5b6f`,
n002_mixed `39e05fe1552f8cedce61694f16f563fa`).
Side note: the script's `nhash` always prints 1 (single md5 of the
concatenation) — the hash value is the real check, not `nhash`.
Proper per-file verification was done instead: 30/30 stripped logs diff
clean against the committed logs.

## N=24000 large-N leg

`runs24k/n24k_r{0..4}.log`: `./fewshot_learner eval 24000 24 1000 1 <r>
corpus/texts 0` — 5/5 byte-identical (stripped), clean 22841/22841 = 1.0000,
all-fact 0.9517, absorption 1159/1159, flaw 96/96, ops 4.000/fact,
92 B/fact (slot_chunks=6, idx_chunks=6, audit_chunks=4 — chunked ledgers
all under the 2^25 slice limit), digest `8e6238911bb7cef0`.
Byte-identical (stripped) to committed `docs/lab/scale/runs/s2_r0.log`
except the `SCALE_CFG` line, where the fewshot fork adds `,off=0` —
confirming off=0 behavior-identity with the frozen scale driver.

## Pure-Zag verdict verifier

`make_verdict_facts.py` (glue) extracts per-leg clean/absorption/min-latency
into `verdict_facts.txt`; `verdict_check.zag` (built with the pinned znc)
applies the decision rule in Zag: mastery legs num==den, one-shot
absorption 1/1 on n001_plant and n002_mixed (+clean 1/1 on n002_mixed),
latency min of every leg within 0.1–2.0 µs/probe and max/min ≤ 4.
Output (`verdict_check.out`): `VERDICT=REPRODUCED`. Zero RNG anywhere.

## Large-N limit (stated)

The committed 6,585,360-fact endpoint was NOT independently re-run: at
4.2 µs/fact install it needs ~8h sustained CPU on this shared 2-vCPU VM,
which would disturb the live workstreams (past-RAM, compression, T1N,
PAM, audio/imagination forks) and violate the non-interference rule.
N=24,000 is the large-N leg of this replication (125× above the ladder's
N=192 top, 100× above the N=240 anchor).

## Environment notes

- VM was heavily contended throughout (load avg 15–24 on 2 vCPUs); the VM
  also rebooted once mid-task (~05:52) — background runs survived and all
  logs verified afterward.
- No binaries or `.zagd` files were committed anywhere (nothing was
  committed at all — this is a scratch replication; the two binaries in
  `crew/` are build artifacts of the pinned znc, never copied).
- No interference with the listed live workstreams; no files touched
  outside `~/workspace/scratch-crossref/T2/SCALEDOWN/` and
  `~/workspace/tmp_commit`.
