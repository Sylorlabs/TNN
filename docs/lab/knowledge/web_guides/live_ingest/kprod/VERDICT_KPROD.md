# VERDICT_KPROD.md — live-ingestion knowledge-first production path

**Date:** 2026-09-25 UTC. **Branch:** `tnn-native-lab`.
**Prereg:** `PREREG_KPROD.md` (frozen pre-battery at `1eab14dc`).

## Main verdicts

### 1x leg — `runs/run1x` — **PASS (7/7 kill bars)**

72 clusters (64 Phase-1 + 8 lifecycle follow-ups), 2 arms × 2 passes,
K-arm 7-step lifecycle, frozen-BF1 N-arm replay both passes.

| Bar | Result |
|---|---|
| KP1 knowledge separation | PASS — K: hk 12/12 INSTALL (`KB\|CORROBORATED`); sk 0/12 installs |
| KP2 pending admission | PASS — K: fn 8/8 → PENDING, 0 INSTALL; N: fn 8/8 INSTALL (the frozen closed hole, documented) |
| KP3 zero sockpuppet installs | PASS — sk 0; pf re-ingest 0 |
| KP4 lifecycle completeness | PASS — 4 PROMOTED→INSTALL (seq>12), 8 RESOLVED_FALSE→WITHHOLD, 4 AUTO_FALSE, 4 AUTO_PROMOTED→INSTALL (seq>12); pn-05..08 held pending; pc pendings cleared; `LIFECYCLE\|DONE\|OK` |
| KP5 novel boundary | PASS — hn K≡N WITHHOLD 8/8; admission audit: 32/32 K PENDING entries have frozen-counterfactual INSTALL in N |
| KP6 determinism | PASS — pass1≡pass2 byte-identical (15 files: logs, ledgers, lifecycle, state); zero RNG |
| KP7 Arm N frozen-identity | PASS — N-arm verdicts + `installed.txt` byte-identical to fresh compile of frozen `webg_bf1.zag`, both passes |

Driver exit 0. Analyzer exit 0. K-arm totals: 20 installs (12 hk + 8
lifecycle follow-ups), 28 withholds (12 sk `KB_CONTRADICTION` + 8 hn
`NO_CORROBORATION` + 8 pf `KB_RESOLVED_FALSE`), 32 pendings (8 fn + 8 pn
+ 8 pf + 8 pc).

### 10x leg — `runs/run10x` — **PASS (4/4 kill bars)**

640 clusters (120 hk / 120 sk / 200 hn / 200 fn), 120-claim KB,
2 arms × 2 passes, no lifecycle.

| Bar | Result |
|---|---|
| KX1 profile stability | PASS — K: hk 120/120 INSTALL; sk 0/120 |
| KX2 no false binds at scale | PASS — K novel INSTALL 0/400 (hn 0/200, fn 0/200) |
| KX3 determinism at 10x | PASS — pass1≡pass2 byte-identical (15 files) |
| KX4 admission audit at 10x | PASS — 200/200 K PENDING entries have N INSTALL |

K-arm totals: 120 installs, 320 withholds (120 `KB_CONTRADICTION` + 200
`NO_CORROBORATION`), 200 pendings. Generator self-checks 882/882;
both generator runs byte-identical.

## Blind battery — `runs/runblind` (post-main-verdict probe, §3.3)

Blind author (subagent; read only the 12 claim texts; no instrument
runs, no matcher iteration; AUTHLOG on file) wrote 6 fresh-vocab honest
+ 6 fresh-vocab sockpuppet clusters, 2 pages each, distinct hosts.
Run once per arm × 2 passes, exit 0, deterministic.

| Class | K arm | N arm | Ground truth |
|---|---|---|---|
| Sockpuppet (bs-01..06) | 6/6 WITHHOLD (2 `KB_CONTRADICTION`, 4 `NO_CORROBORATION`) | 6/6 WITHHOLD | WITHHOLD both arms ✓ |
| Honest fresh-vocab (bh-01..06) | 0/6 INSTALL — all `NO_CORROBORATION` | 6/6 WITHHOLD ✓ | K INSTALL ✗ |

**Reading.** The safety direction generalizes: 12/12 blind sockpuppets
withheld across arms with fresh vocabulary the author never tested.
The recall direction is lexically bounded: the blind honest paraphrases
share only ~40% of content tokens with their committed claims, below
the frozen matcher's binding threshold (`3·overlap ≥ 2·an`, plus full
claim-token coverage and digit equality for AGREE). The KB prior stays
silent there, and the frozen machinery withholds — fail-closed
(ignorance → withhold, never mis-install), the same `NO_CORROBORATION`
the frozen arm returns for novel honest input (cf. hn 8/8 both arms in
the main 1x). Track B's near-verbatim honest paraphrases install 12/12
(1x) and 120/120 (10x); the blind battery measures where that recall
ends. This is the disclosed matcher limitation (prereg §7.4: matcher
hardening out of scope this round), now quantified: recall holds inside
the binding envelope, refusal holds everywhere. No kill bar covers the
blind battery (it is post-main-verdict evidence); the main verdicts
above are unaffected.

## What was proven

1. **Deliberate knowledge-claim store** — `kbcommit` installs only what
   is deliberately taught; G7 (uncalibrated) is rejected; no silent
   overwrites (append-only, seq-attributed).
2. **Knowledge as read-only retrieval prior** — `kb_prior`/`kb_tv`
   consulted on every verdict; committed claims are never mutated by
   ingestion.
3. **Honest paraphrases install** — 12/12 (1x), 120/120 (10x) via
   `KB|CORROBORATED`.
4. **Sockpuppets rejected** — 0 installs across sk (12), pf re-ingest
   (8), blind (12): `KB_CONTRADICTION` where they bind, withhold
   otherwise.
5. **Refusal when ignorant** — novel honest input withholds in both
   arms; fresh-vocab paraphrases outside the binding envelope withhold.
6. **Novel-claim boundary measured** — KP5/KX4: every K PENDING entry
   (32 + 200) has a frozen-counterfactual INSTALL; admission audit 100%.
7. **Pending lifecycle** — PENDING until `kbtest true` (promote) /
   `kbtest false` (resolve); auto-false on re-ingest collision,
   auto-promote on corroboration; resolved-false re-ingest gated.
8. **Determinism** — all legs byte-identical reruns, zero RNG;
   no-arbitrary-limits surgery byte-identical to predecessor.
9. **Frozen identity** — Arm N ≡ fresh BF1 compile on all clusters
   (KP7).

## Limitations & future work

- KB-prior recall is bounded by the frozen matcher's token-overlap
  binding rule (blind: 0/6 fresh-vocab honest installed). Matcher
  hardening is future work (prereg §7.4).
- Single-character digit perturbations are matcher-invisible (frozen
  `tokenize(minl=2)`); both batteries avoid them by construction.
- Subject-swapped sentences with equal digits can wrongly AGREE
  (inherited Track B disclosure).
- Governance parameters (DROP stoplist content, thresholds) are the
  frozen/preregistered values; adoption of any of this as production
  TNN machinery needs Micah's sign-off.

## Verdict

**The knowledge-first production path is SOUND on the preregistered
bars: 7/7 at 1x, 4/4 at 10x, with the blind battery confirming
sockpuppet rejection generalizes and quantifying the recall boundary
as fail-closed.** Recommended: commit source, drivers, batteries,
evidence, and this verdict to `tnn-native-lab`.
