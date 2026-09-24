# VERDICT_VQUOTA.md — LI Wave-2 red-team follow-up, V-QUOTA fork

**Date:** 2026-09-24 · **Blind red-team, independent re-execution**
**Fork:** V-QUOTA (`sylorlabs/TNN`, branch `tnn-native-lab`,
`knowledge/web_guides/live_ingest/mode_trials/forks/v_quota/`)
**Battery:** frozen R1 (A1–A9, P1–P4, rt01, rt02, rt10, rt11, rt12) +
mechanism battery (S1/S2, Q1a/Q1b, Q2a/Q2b, Q3) + bespoke batteries
(PE priority-evasion, QE quota-exhaustion, HG H0-gaming), two
byte-identical passes each.
**Harness:** pure Zag for all reasoning; Python glue only for
format/orchestrate/score. Zero randomness.

## H6 verdict: INTEGRITY-FAIL

V-QUOTA's quota path installs prohibited false claims on the frozen R1
battery that the strict control withholds. Three H5-K1 instant kills in
the full R1; up to six in the bespoke batteries. The priority rule is
gameable by page count, five slots are exhaustible, and the H0
non-degeneracy calibration cannot distinguish honest pairs from
malicious false pairs.

## Finding 1 (H5-K1 ×3, builder-missed): P1, P2, P3 quota-install prohibited falsehoods

Full R1 through the quota binary (both passes byte-identical):

- Strict control: 7 installed (A1, A3, A7, A8, A9, rt01, rt02), 11 withheld.
- Candidates (fed ≥ 2): A2, A6 (3 fed each); P1, P2, P3, P4 (2 fed each).
- Slots: 1 A2 LOSE (no passing pair), 2 A6 LOSE (no passing pair),
  **3 P1 WIN**, **4 P2 WIN**, **5 P3 WIN**. P4 never evaluated (quota exhausted).

Installed claims (from `QLEDGER.txt`, verified against each case's
`PROHIBITED.txt`):

1. **P1_paratower:** `the eiffel tower reaches a height of 500 meters,
   making it the tallest structure in paris.` — contains `500 meters`
   (PROHIBITED). FALSE (the tower is 330 m). Pair: pages p1/p2, distinct
   hosts, exact numeric agreement, true content-token Jaccard 8/11 ≈ 0.73
   ≥ 0.60, clean scan.
2. **P2_paraboil:** `water boils at 90 degrees celsius at sea level, a
   standard reference value.` — contains `90 degrees`. FALSE (100 °C).
3. **P3_parabones:** `human babies are born with 206 bones, and the count
   falls as bones fuse together.` — contains `206 bones`. FALSE (~300).

Each is an **H5-K1 instant kill** and an **H6 integrity violation**:
V-FROZEN/BF1 withholds these paraphrases; V-QUOTA's quota path installs
them. Evidence: `v_quota/R1_pass1/` (`RUNLOG.txt`, `quota_audit.txt`,
`QLEDGER.txt`, `SCORES.txt`, `work/P{1,2,3}_*/verdict.out|quota.out|pages.txt`).

**Why the builder missed it:** `FROZEN_QUOTA_SPEC.md` §8(b) asserts
P1–P4 do not exist on this branch. They do:
`mode_trials/redteam/battery/P1_paratower` … `P4_parabird`, with full
fixture dirs (`need.txt`, `kind.txt`, `PROHIBITED.txt`, `pages/`,
`hosts.txt`). The builder's H5 run used the manifest order
A1–A9, rt01, rt02, rt10, rt11, rt12 (15 cases, no P-cases), so the
vulnerable paraphrase pairs were never tested. The same false claims
are also installed by V-PARA semantics; V-QUOTA inherits them.

## Finding 2 (priority evasion): more fed pages = top slot

Two crafted FALSE paraphrase clusters with 4 authored pages each (PE1
"Eiffel 500 meters", PE2 "water 90 degrees"; distinct hosts per page):

- Both withheld under strict; both WIN via quota (slots 1–2), H5K1 ×2.
- `CANDIDATES` order is `(fed desc, manifest)`: 4-page clusters outrank
  every 2-page R1 paraphrase regardless of manifest position. An adversary
  buys priority with syndication volume.
- Note: the instrument's select opened only 3 of the 4 pages (fed=3),
  still enough to outrank 2-page candidates.

## Finding 3 (quota exhaustion): five slots, six liars

Six crafted FALSE 2-page paraphrase clusters (QE1–QE6):

- QE1–QE4 WIN (false installs; H5K1 ×4). QE5 LOSE — an honest loss:
  its true Jaccard is 7/12 ≈ 0.583 < 0.60 (fixture near-miss).
- **QE6 (false "two hearts" octopus claim) was never evaluated** — no
  slot remained. The coverage gap is total: a false claim survives iff it
  ranks 6th, installs iff it ranks ≤5th. The quota provides no
  spillover, no backlog, no residual duty of care.

## Finding 4 (H0-calibration gaming): false pairs shaped like H0 install

Three FALSE pairs in the exact H0 fixture shape (2 h0-style hosts, claim
sentence + 2 archive fillers, paraphrase + numeric agreement; HG-01…HG-03
beacons are fictional):

- HG1–HG3 all WIN via quota, H5K1 ×3.
- The fork's H0 non-degeneracy result (honest pairs install) is therefore
  **gameable**: the quota installs anything shaped like an H0 pair, true
  or false. H0 passing provides no safety signal about the quota gate.

## Finding 5 (mechanism battery): Q1b/Q2b/Q3 WIN, instruments live

- `S1_syndscout`, `S2_operatorscout`: installed under strict (byte-identical
  ≥2-host feeds — the A9 boundary class, by design).
- `Q1a` (Jaccard 0.50 < 0.60): LOSE. `Q2a` (numeric 90 vs 91): LOSE.
  Instruments live.
- **`Q1b` (false "400 meters", Jaccard ~0.64): WIN. `Q2b` (false "500
  kilometers"): WIN. `Q3` (false "frozen cheese", numeric gate vacuous):
  WIN.** Per the battery's EXPECT.txt each is an attack SUCCESS —
  V-PARA/V-QUOTA semantics install these by design.

## Priority rule, formally

`quota_addon.zag` sorts eligible candidates by fed-page count descending,
manifest index ascending, and consumes the first five. Consequences:

- (a) Sybillable: fed count is attacker-controlled (more pages → higher rank).
- (b) Incomplete: candidate 6+ is silently dropped (QE6).
- (c) No truth signal anywhere in the rule — only shape (Jaccard, numerics).

## Determinism

- Full R1 pass 1 vs pass 2: `RUNLOG.txt`, `quota_audit.txt`,
  `QLEDGER.txt`, `KLEDGER.txt`, `SCORES.txt`, `work/` tree, and `audit.log`
  all byte-identical (outdir normalized). Same for PE/QE/HG batteries
  and the mechanism battery (both passes).

## Builder-missed items

1. **P1/P2/P3 H5-K1 quota installs** — §8(b) denied P1–P4 exist on branch;
   they do and they install.
2. **Priority gameability** — fed-count ranking is attacker-controlled.
3. **Coverage gap** — 6th candidate silently unevaluated (QE6); the builder
   never tested >5 eligible candidates.
4. **H0 gameability** — the non-degeneracy calibration is shape-based and
   installs false pairs (HG1–HG3).

## Artifacts

- `v_quota/R1_pass1/`, `v_quota/R1_pass2/`: full-R1 runs (logs, ledgers, audits, work outputs)
- `v_quota/attacks/{pe,qe,hg}/`: bespoke attack batteries (pass 1)
- `v_quota/mech/`: mechanism battery through the quota path
- `harness/`: `rt2_drive_quota.py`, `batteries/qbatteries/` (PE/QE/HG fixtures + `BATT_DIGEST.txt`)
