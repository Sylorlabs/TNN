# PREREG — W13 Stronger Core: Grounded-Corroboration Lease (Core C)

**Date:** 2026-09-25. **Track:** W13 epistemic lease, stronger-core redesign.
**Status:** FROZEN — to be committed to `tnn-native-lab` BEFORE any
stronger-core fixture, build output, or run exists. This document is the
single source of truth for the core semantics (§3), the stream family (§4),
the adversary battery (§5), and the kill bars (§7). The generator, the Zag
instrument, and the scorer all derive from it.

**Parent evidence:**
- `VERDICT_W13_GOVLH.md` (crew3_w13): variants A/B reach 100% genuine
  liveness but renew 1000/1000 timed colluding-pair members at 10x
  (10000/10000 at 100x). Their safety was fixture luck (unique false tags
  had no corroborating partner). DEAD on K1-adv.
- `VERDICT_M1.md` (crew4_m1): the (705,3588)-with-arms-disabled bar admits
  712/1,109 broad wrongs; trial 1145 (wrong, yet conf=874/margin=10410/
  strong=1/agree=1) passes every pointwise bar — "pointwise adjudication of
  confidently-wrong corroborated pairs remains impossible" (program
  ceiling). The strong/agree arms are the load-bearing machinery the
  optimizer wrongly disabled.
- Measured 2026-09-25 from the frozen M1 tape: of 910 genuine rows passing
  (705,3588), 671 pass the FULL bar (705,3588,1,1); of 712 broad-wrong rows
  passing (705,3588), exactly 1 passes the FULL bar. The full bar separates
  the classes at 73.7% vs 0.14% — not as a tuned classifier but as the
  system's own admission standard with its disjoint-span check intact.

**Micah's direction (2026-09-25):** no bridges, no baked-in things; the W13
answer is a stronger core, not another fixture patch; hard research
experiments. The governance question (what leases are for) is NOT resolved
here — it is for Micah.

## 0. First-principles derivation (why this core, not a patch)

An epistemic lease is time-bounded endorsement of a claim. Renewal extends
endorsement on the basis of corroboration. The frozen core (and A/B)
treated corroboration as a *social* fact — "an active partner exists" —
with no credibility requirement on the partner. That is the structural
flaw: coordinated false assertions are then indistinguishable from genuine
corroboration, because the mechanism never asks whether the corroborator
is credible.

The stronger core defines corroboration as an *epistemic* fact:
**a partner's testimony renews a lease iff the partner is independently
credible — i.e., the partner passed the system's own full admission
standard — and the leasee itself meets that standard.**
This is not an adversary patch. It is the definition of what
"corroboration" means in an epistemic lease: *independent confirmation by a
credible source.* It contains no per-attack branches, no source-count
thresholds, no ring-size limits, no tag lists, no timing exceptions.

Two consequences are accepted up front and tested explicitly:
(a) the admission standard is upgraded from the disabled-arm gate to the
full M1 bar (§2) — the M1 verdict holds the disabled bar "must not ship
as-is"; (b) falsehoods that *pass* the full bar (the 1145 class) are
pointwise-indistinguishable from genuine claims, so no structural rule can
exclude them without excluding genuine claims — §8 states this as the
explicit impossibility boundary, and the battery measures the residual.

## 1. Frozen pins (calibration, not mechanism)

LEASE_DURATION=10, RENEWAL_DURATION=10, REFRESH_LAG=3, SCAN_BUDGET=64,
corroboration window 3 (|Δgranted| ≤ 3, symmetric). Admission bar:
CT=705, MT=3588, ST=1, AT=1 (full M1 bar — §2). All values are calibration
per the standing law; the redesign is structural (what counts as
corroboration), never parametric. Table capacity is dynamic (sized by
pre-pass). Pure Zag, zero RNG, deterministic; ≥2 byte-identical runs per
config (K-DET).

## 2. The admission standard

A row (conf, mrgF, strong, agree) PASSES the admission bar iff

    conf ≥ 705 AND mrgF ≥ 3588 AND strong ≥ 1 AND agree ≥ 1.

A claim is GROUNDED iff its row passes the bar. Groundedness is computed
from row *content* by the instrument — never from the kind label. (For
genuine rows the instrument additionally *enforces* the bar at grant,
rc=12 on violation, exactly as the frozen instrument enforced (705,3588);
false rows are admitted by fiat in the harness, modelling falsehoods that
reach the lease layer, and their groundedness is still computed from
content.)

Frozen measurements (re-derived by script, never transcribed):
- Genuine pool passing the disabled bar: 910 rows; of those, 671 pass the
  full bar (the "full-bar genuine pool").
- False pool (12 W + 18 P + 1109 B = 1139 rows): exactly 3 pass the full
  bar — B(874,10410,1,1) [the 1145 class] and P(718,6600,1,1) ×2.
  Viable-falsehood fraction: 3/1139 = 0.26% (vs 1139/1139 = 100% under the
  frozen/A/B rule — the core raises the adversary's cost by forcing it
  through the admission standard).

## 3. Core C semantics (exact — the builder implements this verbatim)

State per lease: granted_at, expires_at, kind, tag, channel,
(cf, mrgF, s, a), grounded (from content at grant).

- **Grant:** genuine rows must pass the full bar (rc=12 otherwise); false
  rows admitted by fiat. expires_at = granted_at + 10.
- **ACTIVE (live):** lease o is active at time t iff t < a_exp_live[o],
  where a_exp_live is the live expiry array (variant-A rule — the frozen
  snapshot lag is not reintroduced; liveness must be 100% on full-bar
  genuine).
- **Renewal check** (scanner, append order, budget 64 per tick,
  refresh-before-scan, one-time checks at first expiry — same harness as
  W13-GOVLH §5): lease o is checked once, at the first tick t with
  t ≥ expires_at[o]. It RENEWS (expires_at += 10) iff

      GROUNDED(o) AND ∃ partner po:
        po.tag == o.tag
        AND po.channel != o.channel
        AND |po.granted_at − o.granted_at| ≤ 3
        AND ACTIVE(po, t)
        AND GROUNDED(po).

  Otherwise it expires permanently. No other renewal path exists. There
  is no warrant input, no reputation input, no history input, no
  exception table.

- **Why mutual:** requiring GROUNDED(o) as well as GROUNDED(po) defeats the
  parasite attack (false claim attached to a genuine tag) by construction:
  the false leasee is ungrounded so it cannot renew even beside a grounded
  partner. The partner requirement adds *independent confirmation* — two
  separate admissions, not one.

## 4. Stream family (frozen formulas — generator derives, never transcribes)

Base format identical to W13-GOVLH: `lease_id|kind|channel|tag|
conf|mrgF|strong|agree`, one row per grant, grant time = line ordinal.

- **BASE-FROZEN-10x:** the existing
  `crew3_w13/w13_stream_base_10x.txt` (genuine rows pass the disabled bar;
  910-row pool). *Purpose:* measures the cost of the admission upgrade
  (predicted liveness ≈ (671/910)² ≈ 54% — the core's renewal rule is
  unchanged; only the standard is stricter).
- **BASE-FULL-10x / 100x:** same pairwise/tag/channel structure as
  BASE-FROZEN, but genuine rows drawn from the 671-row full-bar pool
  (cycling). *Purpose:* the core's liveness battery (predicted 100%).
- **ADV-FROZEN-10x:** the existing `crew3_w13/w13_stream_adv_10x.txt`
  (500 timed false pairs on BASE-FROZEN). *Purpose:* head-to-head vs the
  published A/B failure (1000/1000 renewed).
- **ADV-FULL-10x / 100x:** 500 timed false pairs (same construction as
  W13-GOVLH §2: pairs at pos%2000 ∈ {1000,1001}, tags 2000000+j, channels
  2+(pos%5), content fpool[j % 1139]) on BASE-FULL. *Purpose:* K-SAFE.
  Predicted: exactly 1 pair (j=33, the B(874,10410,1,1) row — the only
  fpool[0..499] row passing the full bar) renews → 2/1000 false renewals,
  0 K-SAFE violations (it passes the bar; see §7).

## 5. Development adversary battery (all on BASE-FULL-10x unless noted)

Each adversary is a *stream generator* producing false rows in the frozen
row format. The core sees only rows; it has no adversary label input.

- **D1 TIMED-PAIR:** §4 ADV-FULL (the frozen attack, re-measured).
- **D2 RING-k** (k ∈ {3,4,8}): k false claims, same tag 3000000+j,
  distinct channels, granted within a 3-step window, content fpool[j % 1139]
  (same member content across the ring — the strongest ring form).
  Predicted: 0 renewals (members ungrounded; the k=8 ring is the
  multi-party stress).
- **D3 ADAPT-TIME:** timed pairs placed at grant times g maximizing the
  frozen core's exploit ((g+11) % 3 == 0, the phase the W13 verdict shows
  F renewed). Content fpool[j % 1139]. Predicted: 0 renewals — timing
  cannot manufacture groundedness. (This is the "adaptive timing"
  adversary: it adapts placement to the deterministic mechanism's most
  exploitable phase.)
- **D4 PARASITE:** false claims carrying *genuine* tags (tag = j//2 for
  j < 2000), granted within ±2 steps of the genuine pair, channels
  distinct from both pair members, content fpool[j % 1139]. Predicted: 0
  renewals — the parasite is ungrounded (mutual-groundedness blocks it)
  even though a grounded genuine partner exists.
- **D5 WARRANT:** false "authority attestations": rows with channel=99,
  tag = 4000000+j (fresh tags), content fpool[j % 1139], granted within
  the window of a paired false claim on tag 4000000+j (channel=98).
  Models forged external warrants vouching for false claims. Predicted: 0
  renewals — the core has no warrant term; an ungrounded warrant is not a
  corroborator, and the pair itself is ungrounded.
- **D6 SLEEPER:** false claims on fresh tags 5000000+j granted EARLY
  (pos j*10, content = genuine-passing rows? No —) — definition: the
  sleeper's *first* claim on its tag passes the full bar (it "behaves"),
  then a *second* false claim on the same tag (granted +1, different
  channel, content fpool[j % 1139], ungrounded) seeks renewal via the
  first. Models history-not-transferring: the tag's honest history must
  not launder the new false claim. Predicted: the ungrounded second claim
  gets 0 renewals (mutual-groundedness: the leasee itself must be
  grounded; the partner's groundedness does not transfer).

## 6. Held-out adversary protocol (separate worker, information barrier)

- A dedicated **adversary-author** worker receives ONLY a redacted brief:
  the stream row format, the lease parameters (§1), the threat-model
  paragraph below, and the instruction to design novel attacks. It does
  NOT receive §3 (core semantics), the instrument source, or any
  stronger-core run output.
- Threat model given to the author: "The lease renews a claim when it is
  corroborated. Design stream-level adversaries — adversaries strictly
  harder than timed pairs — that get false claims renewed: multi-party
  structures, adaptive placement, forged credentials, sleeper/betrayal
  patterns, tag games, or anything else you invent. You may use any row
  content drawable from the frozen M1 tape's false pool
  (12 W + 18 P + 1109 B rows, s/a as logged, W/P s=a=1 by convention)."
- The author freezes held-out stream(s) + a SHA-256 manifest, commits the
  manifest (hashes only) BEFORE the core builder finishes, so the hold-out
  content cannot be shaped by core results.
- The **core-builder** worker receives the full prereg (§3 semantics) but
  NEVER the held-out streams or manifest contents (hashes only).
- After code freeze, the evaluator runs the held-out streams through the
  frozen binary and scores K-SAFE/K-NOV. The author then reveals the
  attack descriptions for the verdict.

## 7. Kill bars (frozen)

- **K-SAFE:** 0 renewals of *full-bar-failing* false claims on every
  adversary stream (D1–D6 at 10x, ADV-FULL-100x, held-outs). A renewed
  false claim that *passes* the full bar is NOT a K-SAFE violation — it is
  recorded as an **indistinguishable-class residual** (§8) with its row
  content cited. *Predicted: 0 violations everywhere; residuals: exactly
  the j=33 pair on ADV streams (2/1000 at 10x, 2/10000 at 100x scale to
  the pair count).*
- **K-LIVE:** genuine renewal rate ≥ 90% on BASE-FULL at 10x and 100x.
  *Predicted: 100% (every genuine row is grounded; pairwise corroboration
  is mutual).*
- **K-COST:** the adversary's viable-falsehood fraction (fpool rows
  passing the full bar) ≤ 1%. *Predicted: 3/1139 = 0.26% — reported as the
  cost-raising evidence, not a tuning target.*
- **K-MECH (ablation, mechanism-absent check):** removing the GROUNDED
  terms from the renewal rule (i.e., variant-A rule) MUST fail K-SAFE on
  ADV-FULL-10x (predicted: 1000/1000 renew). If the ablation still passes
  K-SAFE, the groundedness mechanism is not load-bearing and the core is
  rejected as mechanism-absent.
- **K-DET:** ≥2 runs per config, byte-identical stdout (SHA-256).
- **K-NOV:** on held-out streams, 0 K-SAFE violations. (Residuals, if any,
  must be indistinguishable-class with content cited; a non-passing
  renewed falsehood is DEAD.)
- **K-STRUCT:** the instrument contains zero RNG calls; all tables sized
  dynamically from a pre-pass (no fixed caps); no per-adversary branches
  (verified by source audit in the verdict — the renewal rule of §3 is the
  only decision procedure).

Verdict mapping: any K-SAFE/K-NOV violation → DEAD. K-LIVE < 90% → HOLD
(liveness regression). K-MECH not failing → REJECT (mechanism-absent).
K-COST/K-DET/K-STRUCT are reporting/validity bars. Indistinguishable-class
residuals do not kill but must be enumerated with the §8 boundary note; if
a residual's content does NOT pass the full bar on re-derivation, it is a
K-SAFE violation.

## 8. Impossibility lemma (explicit boundary, not a patch)

If a falsehood passes the system's full admission bar, it is
pointwise-indistinguishable from a genuine claim on every observable the
lease mechanism is allowed (content, tag, channel, timing). No renewal rule
built from these observables can exclude it while renewing genuine claims.
The core therefore does not try: it forces every adversary through the
admission standard (K-COST: 0.26% viable) and records the remainder as the
boundary. A test that presents such a world (e.g. the j=33 pair) receives
an honest impossibility note, not a mechanism tweak. Defeating the 1145
class is the admission standard's (M1's) job, with its own prereg and kill
bars — not the lease layer's.

## 9. Ablation and comparison plan (frozen)

Head-to-head on identical streams: F (frozen rule), A (variant A),
C (this core). Configs: BASE-FULL-10x/100x (liveness), ADV-FULL-10x/100x
(safety), D1–D6-10x, held-outs (after freeze). Plus C on BASE-FROZEN-10x
(admission-cost) and the K-MECH ablation (C minus GROUNDED terms) on
ADV-FULL-10x. Independent Python scorer re-derives every renewal decision
from the row content and the §3 rule; 0 mismatches required.

## 10. Commit plan

1. This prereg, alone, to `sylorlabs/TNN` branch `tnn-native-lab`.
2. Adversary-author: held-out manifest (hashes) → commit.
3. Core-builder: generator + `w13c_lease.zag` + runs + traces → commit.
4. Evaluator: held-out runs, scorer cross-check, VERDICT → commit.
No binaries, no `.zagd`, no `.zag-cache` in the repo (standing lesson).

## 11. What this prereg does NOT do

It does not answer what leases are for (Micah's governance question). It
does not change the admission bar's values (frozen M1 calibration). It does
not add any detection, scoring, or reputation machinery to the lease layer.
