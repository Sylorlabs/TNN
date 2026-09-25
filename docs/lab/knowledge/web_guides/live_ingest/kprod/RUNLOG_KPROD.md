# RUNLOG_KPROD.md — live-ingestion knowledge-first production path

**Status: LIVE** (1x complete 7/7; 10x running; blind pending).
Prereg: `PREREG_KPROD.md`, frozen at commit `1eab14dc` on `tnn-native-lab`
(2026-09-24). This log records every result-producing run.

## Pins

- Instrument `instrument_kprod.zag`:
  `0d9f392b60e722fff717c00d3e263114018c32fe0aa6f5f329e5c9437b03c46e`
  (binary `1bbf3b5c…`, 344981 bytes main, deterministic rebuild)
- Frozen BF1 `webg_bf1.zag`: `dafb2cb7…f761` (build deterministic:
  fresh compile byte-identical)
- `knowledge_base.txt` (12): `6552481b…e7ebf063`
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (`498abcb5…37e58ef`)

## Shakedown (throwaway inputs only, pre-freeze)

`shake/run2.sh` — full corpus replay + 20-pair `kb_tv`≡`kb_prior`
differential + Arm N byte-identity vs fresh BF1 compile.

- 54/54 checks pass on the final (uncapped) binary.
- Determinism: run2a ≡ run2b byte-identical (zero RNG, behavioral).
- Surgery equivalence: run2a (uncapped) ≡ run1 (dead crew's capped
  binary) byte-identical on every output/rc/state file — the
  no-arbitrary-limits surgery (§2.8) is behavior-preserving.
- Differential: 20/20 pairs agree (6 AGREE / 5 CONTRADICT / 9 UNKNOWN).
  One test-expectation fix during shakedown: single-char digit swaps
  (e.g. 9↔8) are matcher-invisible under frozen `tokenize(minl=2)` and
  read AGREE — frozen behavior, disclosed, both batteries avoid 1-char
  digits by construction.

## 1x run — `runs/run1x` (2026-09-25)

Driver `run_kprod.py` (+ lifecycle-hardening: unforeseen lifecycle
exceptions → VOID), analyzer `analyze_kprod.py`. 72 clusters
(64 Phase-1 + 8 follow-ups), 2 arms × 2 passes, K-arm lifecycle,
`--bf1` frozen replay both N passes.

- Exit 0. All 15 determinism files IDENTICAL; pass SHAs match.
- Arm K pass1: 20 installs (12 hk + 8 lifecycle follow-ups), 28
  withholds (12 sk KB_CONTRADICTION + 8 hn NO_CORROBORATION + 8 pf
  re-ingest KB_RESOLVED_FALSE), 32 pendings (8 fn + 8 pn + 8 pf + 8 pc).
- Lifecycle: LIFECYCLE|DONE|OK (4 PROMOTED, 8 RESOLVED_FALSE,
  4 AUTO_FALSE, 4 AUTO_PROMOTED; follow-up installs attributed seq>12).

ANALYSIS.md (`runs/run1x/ANALYSIS.md`):

| Bar | Result |
|---|---|
| KP1 knowledge separation | PASS — K hk 12/12 INSTALL; K sk 0 installs |
| KP2 pending admission | PASS — K fn 8/8 PENDING, 0 INSTALL; N fn 8/8 INSTALL (closed hole documented) |
| KP3 zero sockpuppet installs | PASS — sk 0; pf re-ingest 0 |
| KP4 lifecycle completeness | PASS — all 8 sub-checks |
| KP5 novel boundary | PASS — hn 8/8 withhold both arms; admission audit 32/32 pendings have N INSTALL |
| KP6 determinism | PASS — pass1==pass2 byte-identical |
| KP7 Arm N frozen-identity | PASS — N-arm verdicts + installed.txt byte-identical to fresh BF1, both passes |

**Verdict: PASS (7/7).**

## 10x run — `runs/run10x` (2026-09-25, COMPLETE)

`--battery battery10x --kb battery10x/claims120.txt --bf1 … --no-lifecycle`.
640 clusters, 2 arms × 2 passes.

- Exit 0. All 15 determinism files IDENTICAL; pass SHAs match.
- Arm K pass1: 120 installs (120 hk), 320 withholds (120 sk
  KB_CONTRADICTION + 200 hn NO_CORROBORATION), 200 pendings (200 fn).

ANALYSIS.md (`runs/run10x/ANALYSIS.md`):

| Bar | Result |
|---|---|
| KX1 profile stability | PASS — K hk 120/120 INSTALL; K sk 0 installs |
| KX2 no false binds at scale | PASS — K novel INSTALL 0/400 |
| KX3 determinism at 10x | PASS — pass1==pass2 byte-identical |
| KX4 admission audit at 10x | PASS — 200/200 pendings have N INSTALL |

**Verdict: PASS (4/4).**

## Blind battery — `battery_blind/` + `runs/runblind` (2026-09-25, COMPLETE)

§3.3: blind author (subagent; only the 12 claim texts read; no
instrument runs, no matcher iteration; `battery_blind/AUTHLOG.md`)
authored 6 honest + 6 sockpuppet fresh-vocab clusters, 2 pages each,
distinct hosts. Ran once per arm × 2 passes: exit 0, deterministic.

- Sockpuppets bs-01..06: **6/6 WITHHOLD K** (2 `KB_CONTRADICTION`, 4
  `NO_CORROBORATION`), **6/6 WITHHOLD N** — rejection generalizes to
  fresh vocab ✓
- Honest bh-01..06: **0/6 INSTALL in K** (all `NO_CORROBORATION`),
  6/6 WITHHOLD N — fresh-vocab paraphrases (~40% token overlap) fall
  below the frozen binding threshold (`3·overlap ≥ 2·an`); KB prior
  silent; fail-closed withhold. Recall boundary quantified; see
  VERDICT_KPROD.md.

## Commits

- `1eab14dc` — prereg freeze (FIRST, pre-battery).
- (pending) source + drivers + batteries + evidence + verdict.
