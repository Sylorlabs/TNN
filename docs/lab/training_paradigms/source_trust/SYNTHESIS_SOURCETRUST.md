# SOURCE-TRUST FORKS — Final Synthesis

**Date:** 2026-09-24. **Ordered by:** Micah ("as a human I don't have knobs, I just learned
myself" — fork everything, test head-to-head, figure-it-out wins ties).
**Branch:** `tnn-native-lab` (sylorlabs/TNN). **Dir:** `training_paradigms/source_trust/`

## The question

Should TNN carry trust in a source as a scalar 0→1 (Micah's first proposal, e.g. 0.36),
and — his immediate self-correction — should that scalar be a hand-set knob at all?
Three forks were built in pure Zag (zero RNG, byte-identical reruns) and tested
head-to-head on a frozen battery plus two red-team waves.

## Commit index

| What | Commit |
|---|---|
| Frozen prereg (alone, before any code/results) | `db069c41` |
| Debate record (Sol + role-separated Muse, frozen alone) | `e2dec8bc` |
| Fork S build spec (frozen alone) | `41cbbe83` |
| Fork S module | `cc3ec0b2` |
| Fork K build spec (frozen alone) | `c5a333e0` |
| Fork K module + debate response | `091c5740` |
| Fork L build spec (frozen alone) | `ff30e218` |
| Fork L module + debate response | `986d7931` |
| Battery/driver/streams (before any fork result) + scorer fix | `cce9832a` / `fd10e605` |
| Red-team wave-2 evidence | `01b6fe8d` |
| This synthesis | (this commit) |

## The three forks

- **K (knob control):** explicit scalar, t0=0.500, δ_up=+0.050, δ_down=−0.150,
  θ_admit=0.600, θ_reject=0.250, clamp [0,1] fixed-point. Baseline to beat.
- **L (learned trust):** no hand-set value. Per-source outcome ring written only by
  world-anchored events; trust recomputed per query as `1000·(ok+1)/(tot+2)` over the
  current regime; first caught lie drops any history to 333 discontinuously;
  MAL (defiant restatement of a refuted claim) is never expunged; corroboration never
  mints trust (no circularity). Swap test PASS (source-symmetric init, byte-identical).
- **S (structural, no scalar):** provenance graph + tagged event logs + frozen structural
  quorums (CORROB_QUORUM=2, REPAIR_QUORUM=3); ordered pattern-match decision; every
  verdict carries a structure-citing warrant. Cold-start R8: first-seen claims INSTALL.

## Battery scoreboard (wave 1, all forks 2× byte-identical)

| metric | K | L | S | floor |
|---|---|---|---|---|
| ST-1 false installs (60) | 0 | 0 | 6 | 60 (KB-1 ☠) |
| ST-1 forged-corroboration installs (20) | **20** | 0 | 0 | 20 |
| ST-1 honest controls (20) | 12 | **0** | 20 | 20 |
| ST-2 pairs / double-installs | 5/5, 0 | 5/5, 0 | 5/5, 0 | 0/5, 5 |
| ST-3 sleeper lies / post-clampdown | 3/5, 2 | 1/5, 0 | 1/5, 0 | 5/5, 4 |
| ST-3P patient lies (10) | 10 | **1** | 10 | 10 |
| RT-T4 slow-drip lies (20) | 20 | **0** | 20 | 20 |
| ST-4 honest-error recovery (episodes) | 24 | 34 | 6 | — |
| ST-5 re-earn first / to-θ | 24 / 24 | 34 / 34 | 6 / — | — |
| ST-6 low-trust-corroborated truth rate | 1.00 | **0.60** (bar 0.80 FAIL) | 0.95 | 1.00 |
| CALIB trust–reality correlation | r=0.84 | r=0.93 | τ-b=0.81 | — |
| RT-T1 betrayal installs | 0/1 | 0/1 | 0/1 | 1/1 |
| RT-T2 Sybil installs (25) | **24 (KB-3 ☠)** | 0 | **5 (KB-3 ☠)** | 25 (☠) |
| RT-T3 laundered (2) | 2 | 0 | 2 | 2 |

**Frozen kill bars:** KB-3 fires on **K (24/25)** and **S (5/25)**. KB-1 fires on the floor
only. KB-2 (r<0): no fork. **L survives all frozen kill bars.**

## Red-team wave 2 (novel attacks, 33/33 byte-identical)

- **Sleeper Sybil breaks ALL forks 25/25** (RT2-V4, novel construction): 8 identities earn
  18 world-confirmed honest outcomes each while co-asserting with honest outsiders, then
  lie in concert. K, L, S, and the S′ probe all install 25/25. History-based independence
  credentials are farmable at ~18 honest episodes/identity. Frozen KB-3 status unchanged
  (novel construction), but L's KB-3 survival now rests on a cold-start-only test.
  **→ Prereg amendment proposed: extend the Sybil bar to established-history rings
  (needs Micah's signature).**
- **K killed robustly** across 5 Sybil variants (23–25 installs). **S killed robustly**
  (5, 5, 8, 25; 1/25 on the one-key variant — the failure is per-key R8 exposure).
- **L attacked successfully:** denial-of-truth 10/10 (burner pre-asserts true claims, L
  withholds when the honest source repeats them); correct-and-re-lie cycle installs
  1 lie / 3 episodes (33% drip — more efficient than K's 14% mechanical drip, via the H4
  correction rule expunging PEND); forged-MAL framing repeatable (burns an honest source,
  though not permanently — 17 OKs re-earn).
- **S′ cautious-prior probe** (structural, no scalar): fixes the naive key-opener
  (RT-T2 5→0, ST-1 false 6/80→0/80) at a first-contact truth cost; sleeper still 25/25.
- **CROSS campaign** (same 186-ep stream): K 17/21, L 1/21, S 8/21 false installs.
- **Warrant quality under attack:** S best (names the attack shape), L good, K weakest.

## Verdict

1. **L wins the frozen battery** — the only fork surviving all kill bars. Micah's
   figure-it-out law holds again: the learned dynamics (L) beat the rigid mechanical
   rule (K), which was killed exactly where its own crew predicted.
2. **The knob deserves scrapping — as the trust mechanism.** K died on Sybil (24/25),
   installed every slow-drip lie (20/20) and every forged corroboration (20/20).
   Hand-set trust constants are attacker-legible: the red team sized its drip from K's
   *declared* δ/θ and walked through.
3. **But the scalar is not dead — the debate's endgame is confirmed.** L's own
   anti-knob audit admits two real knobs in its *admission policy* (L_TH=900 verdict
   cutoff, corroboration quorum 2); S's quorums are "numbers too." The honest line,
   per the debate criterion: a knob = a human's trust theory TNN can't revise. The
   trust *value* can and should be learned (L proved it: r=0.93, zero hand-set
   dynamics). The admission *policy* still needs thresholds — explicit, labeled,
   revisable, never smuggled. Recommended architecture: **L's conservative cold start
   + learned dynamics, S's structural provenance and warrants, K's scalar kept only
   as an explicitly-labeled cache of the structure** — exactly the debate's predicted
   L+S merge with K-as-cache.
4. **No fork is production-safe.** Four proved defects the merge must fix:
   (a) taint → denial-of-truth; (b) correction expunges PEND → tripwire reset;
   (c) self-attested source ids → framing; (d) the sleeper — high-stakes admission
   needs world evidence or costly identity, not a better trust formula.
5. **The sleeper reframes the problem.** ~18 honest episodes buys a trustworthy
   identity under every fork. Trust formulas cannot survive costless identities —
   this is an identity/authentication problem, not a trust problem (same lesson as
   the 1GB colluding-origins 500/500 defeat).

## Open items needing Micah

- **Sign the prereg amendment** extending the Sybil bar to established-history rings
  (RT2-V4), or accept it as a known boundary.
- **Adopt the merge direction** (L dynamics + S structure, K-as-cache) or order
  competing merge forks.
- **ST-6 tension:** L withholds 40% of corroborated truths from low-trust sources
  (fails the 0.80 bar); S installs them at 0.95. The merge must resolve
  conservatism vs truth-installation — this is the live trade-off, not a bug.
