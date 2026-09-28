# ADDENDUM — JOB 1 red-team: dated pre-run freeze (2026-09-25)

- **Status:** FROZEN — 2026-09-25 (PDT). Batteries below are frozen by
  SHA-256. No battery edits after this commit; any new battery needs a
  new dated addendum. Committed BEFORE any attack run, per
  PREREG_NCAL_V3B_FROZEN.md §2.1.
- **Parent:** `PREREG_NCAL_V3B_FROZEN.md` (SHA
  `4c8780d12287c84c83c7576e45ee7f1e36dfa51799081787dfd9d36597196f21`,
  verified by crew before any work).
- **Generator:** `job1/gen_attacks.py` (pure Python, zero RNG,
  deterministic). All batteries: 7-col TSV
  (id, fam, depth, f1, f5, release, correct), depth-major row order
  (d1 rows, then d2, …; id order within a depth), f1=931, f5=1000
  (inert for m20/nopool=1 — the class ledger is never read or written
  for variant 20 — valid 35-grid coords regardless).
- **Driver:** `nec_v2d` variant 20, pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (SHA-256 `498abcb5…`). A/B/C byte-identical runs, SHA-logged.
- **Scoring:** `v2d/bars_full.py` (frozen semantics) on analyzer legs
  via `q2_analysis/to_analyzer.py`; T-probe analogs per attack.

## Pipeline check (§4 — MUST pass before scoring): PASS

Variant 20 re-run on the frozen v2d inputs reproduces the adopted m20
legs **byte-identically** at s1/s10/s100:
- s1: `84ffaf89fd76d2a9119b2060f754d5fdaf72bf7288f0d2403be736d084a36b81`
- s10: `20ff1d1021bba3fcff8d1a4bb303c2f4485fd9a0297b28c2884473265c7c926a`
- s100: `f6a38269b931153b5b10e1d9df10e72bdfb02ca9806d49eb2c6db993ae680ff1`
(all match `v2d/evidence/sha_runs.txt`). Re-scored bars: B1=0, B2=0/0,
B3=2/2/2, B13=0/0/0, B4=0.950, B4b=0.950, B5=0.543, B6=1.000, B7=0.148,
B9=100% — adopted numbers hold; the full frozen H5 red-team battery
(inside the matrix) is confirmed.

Operational note (recorded, not a finding): `nec_v2d` opens inputs with
`O_NOFOLLOW` — symlinked inputs fail with rc=102. Use real paths.

## RT-A — adversarial class distributions (`rta_s1.tsv`, 300 rows)

f1/f5 are inert for m20, so "class" here = the item's own correctness
process (the only channel m20 has). Three families × depths {1,2,4,8,16}:
- `rta_low` (20 items, true rates 0.0–0.4 — exploit first-observation
  overconfidence + test personal-ledger self-correction):
  5× L1=`[C,W,W,W,W]` (0.2), 5× L2=`[W,W,W,W,C]` (0.2, wrong-first),
  5× L3=`[W,W,W,W,W]` (0.0), 5× L4=`[C,W,C,W,W]` (0.4).
- `rta_mid` (20 items): M1=`[C,W,C,W,C]` (0.6, boundary).
- `rta_rate1` (20 items): `[C,C,C,C,C]` (1.0 — exploit the 950 ceiling;
  permanent 50-point underconfidence, G=−0.050/cell).
All rel=1. Hypothesis: confs track empirical rates honestly (no
miscalibration); B4/B4b move down vs adopted 0.950 (predicted ≈0.81 /
≈0.60) without tripping the ≥0.50 floors; B3/B13 measured for movement.
A bar trip here is reported with the white-box rate-tracking diagnosis.

## RT-B — ceiling-latch ordering attacks (`rtb_s1.tsv`, 100 rows)

Family `rtb`, 20 items, identical multiset {C,C,C,W,W} in four orders
(5 items each), depths {1,2,4,8,16}, all rel=1:
- `rtb-wf` = `[W,W,C,C,C]` (wrong-first), `rtb-cf` = `[C,C,C,W,W]`
  (correct-first), `rtb-wm` = `[C,W,C,W,C]`, `rtb-wa` = `[C,C,W,C,W]`.
Hypothesis (from source): conf never rises per item ⇒ V2=0
structurally in all orders. V1 trips exactly on 1→0 correctness flips
whose past keeps p_raw ≥ ceiling (conf at the flip cell cannot reflect
the flip — the frozen authorized-state rule: conf uses PAST cells'
GT only). Predicted V1>0 on cf/wa/wm orderings, V1=0 on wf.
Diagnostic control: same battery on variant 11 (m11) — if m11 also
trips V1, the trips are the authorized-state artifact, not m20-specific.
B1 will trip (batteries contain 1→0 flips by construction); B1/B2/V1
are diagnosed transition-by-transition, white-box.

## RT-C — abstention-composition perturbations (`rtc_*.tsv`, 25 rows each)

Clean isolation: ONLY always-correct (conf 950, stable) + always-wrong
(950@d1, 0@d2+, stable) items — 12+12, family `rtc`, depths
{1,2,4,8,16} — so item confs and correctness are CONSTANT on d2..d16
and the ONLY G driver is the abstention pattern. Then
G(F,d) = −0.050 × (fraction correct among released) on d2..d16:
removing correct-950 items raises G by pure composition.
- `rtc_base`: all released (control — predicts flat G=−0.025, no rises).
- `rtc_v1`: `rtc-C00` abstains at d4. `rtc_v2`: same at d8.
- `rtc_v3`: three correct abstain at d4. `rtc_v4`: one wrong abstains
  at d4. `rtc_v5`: one correct abstains at d2.
- `rtc_v6`: all 12 correct abstain at d16 (bound probe — far
  neighborhood, shows the structural max).
The release rule is NOT changed (sparse abstentions "near" the frozen
M6-at-d4 pattern; v6 is the explicit bound probe). Hypothesis: base has
no rises; v1/v2 ≈ +0.001, v3 ≈ +0.004, v6 = +0.025 (structural max for
binary confs: fraction-correct 0.5→0). All rises diagnosed as pure
composition (no cell miscalibrated). Question answered: how large can
composition-driven rises get within the frozen neighborhood.

## RT-D — distributional shift at scale

s1 diet (`rtd_s1.tsv`, 200 rows): `rtd_low` 8 items (2 per L1..L4),
`rtd_r1` 8, `rtd_mid` 8 (M1), `rtd_norm` 16 (8 all-C + 8 all-W).
s10 (`rtd_s10.tsv`, 3200 rows): 10 deterministic replications, SHIFTED
mix — low ×3 (24/rep), r1 ×2 (16/rep), mid 8, norm 16 → 64 items/rep,
ids `#rtd10rNN`. s100 (`rtd_s100.tsv`, 44000 rows): 100 replications,
low ×5 (40/rep), r1 ×3 (24/rep) → 88 items/rep, ids `#rtd100rNNN`.
(more low-rate + more rate-1.0 at scale, per §2.1). Hypothesis: B13
stays 0/0/0 (nonincreasing, adopted clause); B3/B4/B4b movement measured.
Driver caps respected (s100: 8800 items < 120000; ~2.6MB < 30MB buf).

## RT-E — personal-ledger gaming channel

- `rte_learn.tsv` (150 rows): fam `rte_learn`, 10× `[W,W,C,C,C]`
  (0→1 "learning" — correctness correlates with depth bar-ward),
  10× all-C, 10× all-W controls.
- `rte_fatigue.tsv` (150 rows): fam `rte_fatigue`, 10× `[C,C,C,W,W]`
  (1→0 "fatigue"), same controls.
- `rte_solo_learn.tsv` / `rte_solo_fatigue.tsv` (5 rows each): the
  attacked item alone.
Probes (T1/T2 analogs on the attacked configurations):
- E1 (M2 exact-rule): every emitted conf vs the stated personal-only
  rule `min(p_raw_mil if tp≥1 else 950000, prev_conf_mil)/1000`
  (byte-validated `v2d/sim_v2d.py`) — must be 100% exact; any deviation
  is a channel finding.
- E2 (cross-item independence): attacked item's conf trajectory solo
  vs in-battery must be byte-identical — proves the personal ledger
  carries no cross-item (hence no bar) information.
- E3 (rise-selectivity): V2=0 on both batteries; conf never exceeds
  the stated rule (no selective sparing).
Hypothesis: all three hold — the ledger provably cannot carry bar
information (no depth/family/bar inputs; conf a pure function of the
item's own past correctness; never rises).

## RT-F — item-identity stress (63-byte id truncation; auxiliary probe)

White-box (source `nec_v2d.zag`, `nec_cmp_id`): the id comparison loop
is capped at 63 bytes (`while(k<id.len && k<63)`) and then
`if(k<id.len){return 0;}` — so an id LONGER than 63 bytes NEVER matches
its own slot. Every observation of such an item is treated as a FIRST
observation: conf = d1prior = 950 on every cell, personal ledger never
accumulates (slots also leak one per row; >max_items such rows →
driver rc=107, no output).
`rtf_collide.tsv` (100 rows): 5 always-wrong + 5 always-correct items
with 72-char ids (fam `rtf_long`), 5+5 short-id controls (fam
`rtf_short`), depths {1,2,4,8,16}, all rel=1.
Hypothesis: `rtf_long` wrong items emit 950 on ALL five cells
(|err|=0.95/cell — worse than the disclosed T3 limit, systematic);
short-id controls behave normally (950,0,0,0,0). The Python sim cannot
replicate this (full-id dict keys) — binary-only finding.
Classification if confirmed: mechanism (implementation) break with a
principled in-class fix direction (full-id comparison — lookup
correctness, not a mechanism change); NEEDS-WORK fix round per §2.2
iff the fix is principled and keeps all passing bars.

## Frozen battery SHAs

```
82c75d5265576da046cc962a84de9bb840c125ed106b0d9c16705472099a2700  rta_s1.tsv
bb2ea662e813eb523ec547635d7c32b6011d3ac751c134743e6e67c9ca7c5613  rtb_s1.tsv
15d9044296c07f81863ea92dd0c45274f9db61e043982642eb66d665cc14cc79  rtc_base.tsv
4370ef60e505207b78822b65058e9985ec71bf88df9b0349468dffac58702e8a  rtc_v1.tsv
818a08e336d026da7f21d8ac4846d3039295b354adcf25828dd4b1c11c05c2c1  rtc_v2.tsv
736e7da5562f676622c4fbd5ddee7515683adddfb8c8cbc7dc45f4ebe05904a7  rtc_v3.tsv
49192b154e6e178fc2a21a513acebfd7a1e93b2d6fa153a4708f1bdfd3609fc9  rtc_v4.tsv
3d62e2cbdf7f4ca28f9571e820a0ece3bb822cf5210dab5a3d1c807bdf3a67cd  rtc_v5.tsv
afd0fce38f645da872782462fd0ea92fed5038f79f7778c5a829732ec8309229  rtc_v6.tsv
b852c389b786e1d22b28a230aad8813e62bd1c3dd3b785efaa19d237e3672065  rtd_s1.tsv
801a3aabcf209d8aa8530a712c35777b800cdd39fac652761ed43968385af022  rtd_s10.tsv
a11202c8af5b04d38eceb2a67eeeab150ceb4c67a109c65d002f9776af5d87e5  rtd_s100.tsv
0a14f40a24ad518323b6c3ac9abe3366f9505bdd3b6146f08b0ee7aa9fa2757b  rte_fatigue.tsv
9e7f9eaf2bd8b9cfc14e7b1157bd79bc91aea8d7d5ea1ccc9e6324d1ae1f9c52  rte_learn.tsv
d6efc5d3fb1ad4d68d4231dcc867c8ace944241b870495332f96fe0624411aaa  rte_solo_fatigue.tsv
51f5945f9558067da925d2eb9e3764414a3a0dc2ccb19327e9a18e0425b0353f  rte_solo_learn.tsv
34ee8d668058f0dd4c990ac23f120f7af2753bad3e9e42e6215e1f555cccfa33  rtf_collide.tsv
```

## Break criteria (frozen, §2.2)

"Breaks" ⟺ ANY of: (a) violates a frozen bar (B2 ≠ 0 immediate
critical; B3/B13/B4/B4b/B5/B6/B7/B9 regressions vs §1 adopted numbers);
(b) bar-information channel (T1/T2 trip bar-ward, or channel audit finds
one); (c) adversarial miscalibration strictly worse than the disclosed
limits, systematic not unlucky. Every break gets the white-box
diagnosis (exact items, conf values, mechanism steps; classified
knowledge-bounded / selection / mechanism). Principled in-class fix →
v2d §3 NEEDS-WORK path (one fix round under a dated pre-run addendum);
else the honest residual with the diagnosis.
