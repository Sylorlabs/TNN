# T2-PROSE replication — RUNLOG (crew: T2-PROSE REPLACEMENT)

## 2026-09-22 ~21:37 PDT — crew start (replacement)

- Predecessor crew killed mid-run by runtime daemon restart (~2026-09-23 04:0x UTC).
  Inherited state in `~/workspace/scratch-crossref/T2/PROSE/`:
  - `clean/` contained an EMPTY git repo (no commits; predecessor's clone never completed).
  - `crew/` was empty. No VERDICT.md / RUNLOG.md inherited.
- RESUME decision: predecessor state was empty/void → re-cloned from scratch.
  (Integrity check: `git fsck` on the empty repo reported "unborn branch, no
  references" — nothing valid to resume.)

## Pins (frozen BEFORE any run)

- Cross-ref frozen commit: `7b2100d09911c5c10252c5756c7def288e70bd1f`
  ("crossref: scope + frozen preregs", 2026-09-22T22:54:44Z, micahcooley).
  Checked out in `~/workspace/scratch-crossref/T2/PROSE/clean/repo`;
  `git rev-parse HEAD` → `7b2100d09911c5c10252c5756c7def288e70bd1f`. ✓
- Battery pin (expected `d4c151c7e39c`): verified via GitHub API —
  full SHA `d4c151c7e39c73c8f05b42697cd8fdc81466c025`,
  "Prose-learning experiment: TNN reads LLM words", 2026-09-22T02:06:00Z, 45 files. ✓
- Grok-4.7 rerun pin (expected `fbecf64f08b6f5f41efbf33ef07384154cd48140`):
  verified via GitHub API — full SHA identical,
  "Grok-4.7 rerun sweep: prose-learning KB-QUALITY 4.7 addendum", 2026-09-22T20:30:02Z. ✓
- znc: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned path exists). ✓

## Fetch method note (documented deviation, same pinned bytes)

- Direct `git clone` / full single-SHA `git fetch` OOM-killed on this VM
  (git-remote-https signal 9; VM load ~26, ~150MB free RAM — other crews'
  heavy workloads concurrent).
- Used instead: `git init` + `git fetch --depth 1 --filter=tree:0 origin
  7b2100d09911c5c10252c5756c7def288e70bd1f` (commit object only, ~3s),
  then cone sparse-checkout `docs/lab/prose-learning docs/lab/crossref`
  + `git checkout` (lazy tree/blob fetch of exactly those subtrees).
- Result: HEAD == frozen SHA; `git status` clean; `git fsck` quiet.
  All bytes are the pinned commit's blobs — no source substitution, transport
  only. TMPDIR=/home/hatch/workspace/tmp_commit throughout; nothing in /tmp.

## Authoritative claims checklist (quoted from frozen PREREG_TIER2.md §T2-PROSE)

> **Claims:** commit `d4c151c7e39c`: all four sources trip the ≥0.98 viability
> bar — sol 220/228 (0.9649, −3.5pp), step 0.8947 (−10.5pp), muse-native 0.8772
> (−12.3pp), grok-4.6 0.8289 (−17.1pp); extraction 240/240 perfect; cause =
> retrieval ties, not extraction; Q=+0.0022 → frozen NO-DIFFERENTIATION; fluent
> lies install 12/12 in prose. Honest scope: bag-of-stemmed-words retrieval.
> **Grok-4.7 rerun:** commit `fbecf64f08b6f5f41efbf33ef07384154cd48140`: on
> frozen prose bars, 4.7 yields Q=+0.0548 → mechanically QUALITY-MATTERS
> (boundary result at +0.05 band edge); prose viability still fails 0.9342 vs
> 0.98; both teachers absorb all 12 falsehoods; direct head-to-head clean
> mastery gain +10.5pp. Five live-4.7 items remain blocked — excluded.
> **Method:** rerun the four-source prose battery on committed corpora (clean
> checkout, ≥3 byte-identical); re-derive the Q statistic for 4.6 and for the
> committed 4.7 corpus with independent Zag code.
> **Rule:** REPRODUCED if all four viability figures match and
> Q(4.6)≈+0.0022/NO-DIFFERENTIATION while Q(4.7)≈+0.0548/QUALITY-MATTERS;
> NOT REPRODUCED if the quality verdict flips for either model.

Cross-check vs original VERDICT.md (battery commit): clean counts —
grok-4.6 189/228, sol 220/228, step 204/228, muse-native 200/228;
full — 197/240, 231/240, 214/240, 211/240; extract 240/240 all; absorb 12/12
all; 5/5 byte-identical. Q(4.6)=mean(189,220)/228−204/228=+0.0022.
Q band: ±0.05 three-bin (doc-sweep correction of prereg's ±0.02; both bands
give the same verdicts for these Q values).
4.7 addendum: clean 213/228 (0.9342), full 223/240, Q(4.7)=+0.0548,
Δclean(4.7−4.6)=+24=+10.5pp, 26 gained/0 lost per-probe.

## Build

- Build mirror: `crew/build/` with sources COPIED from the clean checkout
  (sources only, pinned bytes — sha256 recorded below). CWD-at-build =
  `crew/build/` so `@import("R33_NATIVE_SHA256_V2.zag")` resolves.
- Binary runs with CWD = clean checkout `docs/lab/prose-learning/` so
  `inputs/train_<s>.txt` etc. resolve to COMMITTED inputs. Learner performs
  no file writes (verified: no open/write in source) → clean checkout stays
  pristine; run logs captured to `crew/logs/`.

## 2026-09-22 ~22:00–22:25 PDT — battery build + run

- Build: `crew/build/` mirror (prose_learn.zag sha256
  88e91670e2549e76a48a22252cbb6691a6f0407cf1749ba9dcf272f14a68057a —
  matches clean checkout; R33_NATIVE_SHA256_V2.zag
  9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf).
  `znc_linux_x86_64_abed8aa1 prose_learn.zag -o prose_learn` → OK (122049 B).
- Smoke: 1× sol run → SUMMARY extract=240/240 full=231/240 clean=220/228
  absorb=12/12; DIGEST 8764bdee…/LEDGER 735b32c6…; **byte-identical to
  committed runs/sol_rep1.log** (`cmp` clean).
- Full sweep: 5 sources (grok, sol, step, muse-native, grok47) × 5 reps,
  CWD=clean checkout prose-learning dir; logs in `crew/logs/`. ~1.5 s/run.
- Determinism: 5/5 byte-identical per source (1 unique sha256 per source).
- Committed-log cross-check: **all 25 logs byte-identical** to
  `runs/<s>_rep<r>.log` (cmp clean on every pair) — DIGEST/DIGEST2/LEDGER
  all match.
- Input integrity: 240/240/12 lines per source incl. grok47;
  false_ids_grok47 = 3 29 55 71 80 103 117 139 163 178 205 231 (12).
- Tie-cause check (independent grep of my logs, ties≥2):
  grok 106(35) / sol 54(9) / step 43(23) / muse-native 12(10) —
  exactly the committed tie table; grok47 73(14) (new, consistent with the
  4.7 entity-naming tie-collapse mechanism).

## 2026-09-22 ~22:25–22:35 PDT — independent Q re-derivation

- Wrote `crew/build/q_derive.zag` (own code; imports only pinned
  R33_NATIVE_IO_V1.zag): parses SUMMARY clean=num/den from my five rep1 logs,
  exact-fraction Q, ±0.05 band applied in-code, viability + head-to-head gain.
- Built with pinned znc (1 analyzer warning: unused binding; harmless).
- Output (3/3 byte-identical, sha256
  ca12db85c91159ba6672a3c8e9aa1d6f64b57968443750e5817fb74f9dfe9c28):
  - parsed clean: grok=189/228 sol=220/228 step=204/228 muse=200/228 grok47=213/228
  - Q(4.6) = 1/456 = 0.002192 → NO-DIFFERENTIATION
  - Q(4.7) = 25/456 = 0.054824 → QUALITY-MATTERS
  - viability(≥0.98): grok=TRIP sol=TRIP step=TRIP muse=TRIP grok47=TRIP
  - head-to-head clean gain (4.7−4.6) = 10.52pp
- Wrote VERDICT.md → **REPRODUCED**. No commits made (none requested).
  Clean checkout untouched (git status clean); scratch only in
  ~/workspace/scratch-crossref/T2/PROSE/crew/.
