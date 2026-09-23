# T2-HTD1 VERDICT — HTD-1 verdict sheet (Type C)

Crew: T2-HTD1 (REPLACEMENT — predecessor killed mid-run by daemon restart)
Date: 2026-09-22/23 PDT | Authorization: Micah 2026-09-22 "run everything"
Frozen prereg: sylorlabs/TNN branch `tnn-native-lab`, commit
`7b2100d09911c5c10252c5756c7def288e70bd1f` — `docs/lab/crossref/PREREG_TIER2.md`
(blob `b1178370036bffbda6eb68ea0989c0e427dc31b7`), § T2-HTD1.

## Frozen § T2-HTD1, quoted verbatim (authoritative)

> ## T2-HTD1 — HTD-1 verdict sheet (Type C)
>
> **Claims:** commit `8d74c47b5737` (`docs/lab/htd-1/RESULTS_VERDICT_SHEET.md`):
> killed by own bars E-DE1/E-DE2/E-DE3; survivors E-DE4-narrow, E-DE5a, E-LG1,
> E-LG2 (K=64/256; K=16 fails; full-cost saving −6%), E-LG4, G-CO2, G-CO3,
> G-CM1c over G-CM1d; G-CO3's PASS rests on the weighted KB2a reading (flips
> to KILLED if Micah rules raw ops); G-CM1b eviction PASS (`16a2574f3d`);
> E-LG1 epclose R=5 PASS (`1005582b5c`); E-DE2+E-DE4 composition (`302796210b`
> — compose for D-P2-like, not D-P1-like); G-CM1b evict leg source-matched
> rerun done; E-SP research plan not executed (explicit gap).
> **Method:** Type C — re-derive the sheet from committed build evidence with
> independent checks; verify each kill/survive bar was applied per the frozen
> preregs; confirm the G-CO3 contract-dependence caveat is as stated.
> **Rule:** REPRODUCED if every kill/survive entry re-derives and the
> caveats/gaps are as stated; PARTIAL if any entry's bar application is
> questionable (name it).

Decision rule applied verbatim: REPRODUCED iff every kill/survive entry
re-derives AND the caveats/gaps are as stated.

## Frozen pins (recorded before work; all resolved)

| Pin | Resolved to | Evidence |
|---|---|---|
| Prereg commit | `7b2100d09911c5c10252c5756c7def288e70bd1f` — "crossref: scope + frozen preregs for the cross-reference / clean-environment replication program" | clone + API |
| Verdict sheet | `8d74c47b5737743f4f2ff6eb807f05f2308358b0` — "htd-1: final results verdict sheet (closeout survey, 2026-09-21)"; adds `docs/lab/htd-1/RESULTS_VERDICT_SHEET.md` (blob `02c97bf9…`) | clone + API; byte-matches API copy |
| Composition | `302796210b659925391cd98a5bd61c7844f4877d` — "HTD-1: E-DE2+E-DE4 composition head-to-head evidence"; adds doc + `builds/comp/` | clone + API; byte-matches |
| E-LG1 epclose R=5 | `16a2574f3d01fed8b51f02de2b7a7ac6113de2de` — "htd-1: E-LG1 episode-close R=5 completion verdict — PASS"; adds `E-LG1-episode-close-R5.md` | clone + API; byte-matches |
| G-CM1b evict rerun | `1005582b5c467e7dca554017bdc2f39573c39b6a` — "HTD-1: G-CM1b eviction-leg rerun verdict (PASS)"; adds `G-CM1b-evict-rerun.md` | clone + API; byte-matches |
| E-LG2 committed verdict | `af6a22305a…` — "htd-1 RESULT: E-LG2 checkpoint+delta — verdict recorded (independently verified)"; adds `builds/elg2/` | API |
| E-DE3 committed verdict | `00984047f2…` — "htd-1 RESULT: E-DE3 lazy verification debt — KILLED (independently verified)"; adds `builds/ede3/` | API |
| znc | `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (8337204 B, sha256 `498abcb5ab346f8c…`) | verified present |

**Pin anomaly (flagged, non-blocking):** the frozen prereg's T2-HTD1 section
labels the G-CM1b commit `16a2574f3d` and the E-LG1 commit `1005582b5c` —
the branch history proves these two short SHAs are **swapped**:
`16a2574f3d` adds `E-LG1-episode-close-R5.md`, `1005582b5c` adds
`G-CM1b-evict-rerun.md` (confirmed via `git ls-tree` on both commits in the
clean clone and via the commits API). Both verdicts are PASS; the verdicts
are unaffected — only the labels are transposed. The independent checker
emits the swap as its own finding (`PINSWAP` line). — Additionally, the
predecessor crew's RUNLOG recorded an expected pin `e7c5bcd6` for the
verdict sheet; `e7c5bcd6` does not exist in the branch (searched 200
commits) — a predecessor error. The prereg's own pin `8d74c47b5737` is the
valid one and was verified.

## Clean-environment integrity

- Clone: `~/workspace/scratch-crossref/T2/HTD1/clean/t2-htd1-shallow`
  (`--depth 300`, branch `tnn-native-lab`; HEAD `2f61ed6ac79a3f9571ef5b243d59330a8fe641f7` = API branch tip).
  A full fetch was attempted first and SIGKILL'd (OOM in index-pack); the
  predecessor's partial clone was wiped by the daemon restart, so re-clone
  was required.
- `git status --short`: clean (empty).
- `git fsck --full`: rc=0, no errors.
- Frozen prereg at frozen commit byte-matches the API copy (`cmp` clean).
- Verdict sheet, composition doc, E-LG1 doc, G-CM1b doc at their commits
  byte-match the API copies (`cmp` clean).

## Independent re-derivation (pure Zag, zero RNG, 3× byte-identical)

`crew/htd1_barcheck.zag` built from source with the pinned znc
(`htd1_barcheck_bin`, scratch only, not committed). It recomputes every
bar-application arithmetic from the frozen prereg bars (§3a–3d, §1, §7) and
the sheet's committed numbers in integer tenths-of-percent, then emits the
kill/survive verdict per entry.

Runs: `68f6ae67d87794b0d28d41165eeb22bd1e4928db29903c5c1568ea0b1f9a1611`
×3 — byte-identical (3/3).

## Claim-by-claim verdict (prereg claim → measured → bar application)

| # | Claim | Measured | Bar application | Result |
|---|---|---|---|---|
| 1 | E-DE1 KILLED (KB1, KB3) | div 163/599 = 27.2% > 2%; BUDGET_EXHAUSTED 100% of items > 10% | KB1/KB3 hard-kill trip correctly per §3a | ✔ REPRODUCED |
| 2 | E-DE2 KILLED (KB2) | savings −4.3%/+11.9% < 15%; KB1 0 div, KB3 certs replay, KB4 R=5 hold | KB2 (<15% → KILL) trips correctly; other bars hold as stated | ✔ REPRODUCED |
| 3 | E-DE3 KILLED (KB2, KB3) | saving +0.015% < 15%; main arms emit with debts outstanding | KB2 + KB3 zero-tolerance trip correctly per §3a | ✔ REPRODUCED |
| 4 | E-DE4-narrow survives; broad killed (KB2) | narrow 42.2%/44.8%, 50% hit rate, 0 false hits; broad 0% hits, 6–9% costlier | narrow clears all; broad <10% hit rate → KILL per §3a | ✔ REPRODUCED |
| 5 | E-DE5a PASSES; E-DE5b KILLED (KB2); E-DE5d PASSES | (a) 37.06%, 0/1200 div; (b) <15%; (d) 18.45% graceful degradation | KB2 applied per §3a; (b) killed correctly | ✔ REPRODUCED |
| 6 | E-LG1 PASS (+ epclose R=5, `16a2574f3d`) | R=5 × 500 epclose: SHA `397dd7dd…` = baseline SHA all 5; 11/11 kill-restarts IDENTICAL; syscall saving 94.45% ≥ 60%; bytes 102.78% ≤ 110% | §3d REPLAY (0 div) + SAVINGS bars not tripped | ✔ REPRODUCED |
| 7 | E-LG2 PASS K=64/256; FAIL K=16; full-cost −6% (`af6a22305ab9`) | replay byte-identical all K; K=64 bytes 25.51% ≤ 50%, snap share 6.14% ≤ 20%; K=16 snap share 21.47% > 20%; K=256 24.62%/1.62%; full-cost −6.0% (KB-HTD-1.5) | §3d SAVINGS fail: K=16 >20% snapshot share → FAIL correctly; −6% caveat stated in committed verdict | ✔ REPRODUCED |
| 8 | E-LG4 PASS | ledger byte-identical on/off; verification 0.068% ≤ 25%; maintenance 0.104% ≤ 10%; staleness 750/750 match; R=5 byte-identical | all §3d bars hold | ✔ REPRODUCED |
| 9 | G-CO2 PASS | KB1 48/48 ≥ 75%; KB2 0.0016 ≤ 30%; KB3 0 faults/0 fill; KB4 abstains 196/200 = 98% ≥ 90% | all §3b bars hold; loose-tau kill by KB4 noted honestly | ✔ REPRODUCED |
| 10 | G-CO3 PASS — contract-dependent (`KB2a 0.686` weighted; raw `0.499` < 0.60 would KILL) | KB1 64/64 ≥ 80%; KB2a 0.686 ≥ 0.60 weighted; KB3 0 dev/1240; KB4 0/124 ≤ 25%; 3 negative controls live | COST_MODEL §5 routes gating bars through the 11-class taxonomy ("G-CO3 KB2 planning-op share"), so the weighted reading is contract-correct; the sheet states the flip-condition exactly; Micah has not ruled raw ops → PASS stands | ✔ REPRODUCED |
| 11 | G-CM1c over G-CM1d (shootout) | 200/200 correct both, zero leakage; stringency 3.06 vs 2.83 correct/1k-cost; cm-prom-0155 defect noted as non-deciding | §3b G-CM1 P1/P2/KB1/KB2 all hold; §7 family champion selected on home metric; both tie-break directions same winner | ✔ REPRODUCED |
| 12 | G-CM1b eviction PASS (`1005582b5c` — prereg label swapped) | rerun: 9/9 checks (fp/live/tag-KB-CM-TAG1/copyprobe/replay/compact/chain/evict_count/probe_live); N=5 byte-identical (SHA `4a684028…`); 0 unauthorized ≥16-byte windows; original failure diagnosed as naive-spot-check harness artifact (demonstrated via probe_live, not proven for the unrecoverable original predicate — the doc says this itself) | KB-CM-TAG1/KB-CM-REPLAY1 (amendment R8/R10) not tripped; "source-matched rerun done" true: exact aligned mechanism sources pre-date the build | ✔ REPRODUCED |
| 13 | E-DE2+E-DE4 composition (`302796210b` — compose for D-P2-like, not D-P1-like) | comp KB1 0/1200 div; KB2 46.51% aggregate / 40.03% D-P1 / 50.64% D-P2 ≥ 15%; KB4 R=5 byte-identical; interaction D-P1 +752k (comp worse — 600 misses × E-DE2 overhead, 0 exits), D-P2 −3.24M (165/600 exits fire); sub-additivity I=+3.24M confirmed D-P2; "do not compose" annotation trigger (divergence > either parent) does not fire | §3a composition arm requirements met; verdict sheet's "premise dead" inference correctly refuted for D-P2-like, confirmed for D-P1-like | ✔ REPRODUCED |
| 14 | E-SP research plan NOT executed (explicit gap) | `builds/esp-research/` at frozen commit contains only `RESEARCH_PLAN.md` (960713df0f); pilot scorecard bars retained; no architecture claim | gap stated exactly as in the sheet | ✔ REPRODUCED |

Caveats stated in the sheet and confirmed as stated:
- E-LG2 full-cost −6.0% (committed verdict VERDICT_ELG2.md) — ledger win ≠ cost win.
- G-CO3 weighted-KB2a contract dependence (see row 10).
- E-LG1: `base_r3.ledger` excluded as UNVERIFIED (not needed; r1/r2 byte-identical).
- E-DE4: D-P2 narrow ran R=2 (noted, not fatal).
- G-CM1c/d: cm-prom-0155 battery defect noted, non-deciding.
- E-DE3: debt-cap=0 sanity arm must reproduce FULL-DELIB byte-identically (stated in prereg; sheet's kill rests on KB2+KB3).

## Verdict

**REPRODUCED.** Every kill/survive entry re-derives from the frozen preregs
with the bars applied exactly as written — the three kills (E-DE1, E-DE2,
E-DE3), the seven survivors (E-DE4-narrow, E-DE5a, E-LG1, E-LG2 K=64/256,
E-LG4, G-CO2, G-CO3), the G-CM1c-over-G-CM1d shootout, and the three
follow-up resolutions (G-CM1b eviction PASS, E-LG1 epclose R=5 PASS,
E-DE2+E-DE4 composition with the D-P2-like-only composition rule). The
caveats and gaps are as stated: G-CO3's PASS is contract-dependent on the
weighted KB2a reading (flips to KILLED if Micah rules raw ops — he has not),
E-LG2's full-cost saving is −6.0%, and the E-SP research plan remains
unexecuted. No entry's bar application is questionable.

One anomaly, not affecting the verdict: the frozen prereg's T2-HTD1 section
transposes the two follow-up commit pins — `16a2574f3d` is the E-LG1
episode-close verdict and `1005582b5c` is the G-CM1b eviction rerun, not vice
versa. Both commits exist on `tnn-native-lab` with the expected verdict
content; the evidence itself is correct.

## Method notes (for the record)

- Pin correction (coordinator, 2026-09-22 23:37 PDT): `e7c5bcd6` was a
  transcription artifact — disregarded; work proceeded on the frozen
  prereg's authority (`8d74c47b5737`), which independently resolved.
  Retired the predecessor's STOP clause. No re-work needed.

- Type C; no live-web recapture. All evidence pulled at frozen commit SHAs.
- Python used only as glue (API fetch, base64 decode); all reasoning /
  bar-arithmetic verification in pure Zag (zero RNG), 3× byte-identical.
- Scratch-only; no `/tmp` use; `TMPDIR=/home/hatch/workspace/tmp_commit`.
- No `.zagd` caches; no binaries committed (`htd1_barcheck_bin` stays in
  the scratch crew dir).
- No interference with live workstreams (read-only API + scratch builds).

## Files in this run dir (`~/workspace/scratch-crossref/T2/HTD1/crew/`)

- `VERDICT.md` (this file), `RUNLOG.md`
- `htd1_barcheck.zag`, `htd1_barcheck_bin`, `run1.txt`/`run2.txt`/`run3.txt`
  (identical, `68f6ae67…`)
- `PREREG_TIER2_frozen.md`, `VERDICT_SHEET_8d74c47b5737.md`
- `evidence/` — frozen prereg, constructed-mode amendment, COST_MODEL,
  composition doc, E-LG1 R5 doc, G-CM1b rerun doc, VERDICT_ELG2.md
