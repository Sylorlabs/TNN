# RUNLOG — NEC v2 development (m15 / m20 full workup)

- **Date:** 2026-09-25 (PDT)
- **Crew:** NEC v2d coordinator (subagent)
- **Protocol:** `PREREG_NCAL_V2D_FROZEN.md` (frozen BEFORE any run; this commit)
- **Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)
- **Branch:** `tnn-native-lab`, sylorlabs/TNN
- **Scratch:** `~/workspace/nec_v2d/` (binaries, temp TSVs, SHA logs — outside the repo)

## Freeze (this commit)

- `PREREG_NCAL_V2D_FROZEN.md` — full bar set B1–B9 (B8 computed, reported, non-gating), s1/s10/s100 legs, T1–T4 per direction, T4 on m15, m20 redteam characterization, frozen adoption rule.
- `src/nec_v2d.zag` — variant×scale driver (11/15/20 adoption candidates; 21/22 m_g diagnostic controls; 23 m20_ind light-T4).
- `v2d/sim_v2d.py`, `v2d/bars_full.py`, `v2d/gen_scale.py`, `v2d/t2_v2d.py`, `v2d/t13_v2d.py` — analysis scripts.

## Pipeline checks (§1 — MUST pass before scoring)

1. `nec_q1` ids 15/20 on `necc_input.tsv` vs committed `q1/results_q1/` legs (mechs 15/20): 37/37 byte-identical.
2. `nec_v2d` variant 11 vs committed `results_m11/` (s1), `results_scale_10x/`, `results_scale_100x/`: 111/111 byte-identical (validates driver + regenerated scale inputs).

## Runs

All runs A/B/C byte-identical. Full SHA log: (see `SHA_LOG` section below).

- m15 s1/s10/s100: `c11f8411…bceec`, `797a9f47…df1e`, `efaabf53…e7bc` (full in SHA_LOG)
- m20 s1/s10/s100: `84ffaf89…6b81`, `20ff1d10…926a`, `f6a38269…0ff1` (full in SHA_LOG)
- trap_t1: m15, m20, g15, g20 (full SHAs in SHA_LOG)
- trap_t3: m15, m20, m20_ind (full SHAs in SHA_LOG)
- m20_ind s1 (full SHA in SHA_LOG)
- Control batteries (s1): g15/g20 = m15/m20 matrix bytes (byte-identical); trap_t1 differs.

## Analysis

### Full bars (s1/s10/s100), m15
s1: B1=0✓ B2=0/0✓ B3=2✓ B4=0.977✓ B4b=0.571✓ B5=0.876✓ B6=1.0✓ B7=0.148✓ B8=FAIL(logic, non-gating) B9=1.0✓ B13=6
s10: B3=2, B13=23, all bars pass; s100: B3=3, B13=24, all bars pass.
B13 = 6/23/24 — identical to m11, scale-wise increasing.

### Full bars (s1/s10/s100), m20
s1: B1=0✓ B2=0/0✓ B3=2✓ B4=0.950✓ B4b=0.950✓ B5=0.543✓ B6=1.0✓ B7=0.148✓ B8=FAIL(O,admit,cost,logic,revoke; defective, non-gating) B9=1.0✓ B13=0
s10: B3=2 B13=0; s100: B3=2 B13=0. All bars pass at all scales.
B13 = 0/0/0 — nonincreasing. Outputs binary {950,0}.

### T1 (trap_t1)
m15: crater +0.515 (C=0.515,T=0.000) M1-pass; M2 150/150 exact; M3=4 (=m11). CALIBRATING.
m20: crater +0.950 M1-pass; M2 150/150 exact; M3=4. CALIBRATING.
g15: crater −0.097 M1-FAIL; g20: crater 0.000 M1-FAIL; both 102/150 exact (trip as designed).

### T2 (s1 matrix)
m15: bind ⟺ def>0 (264); S1 within-def>0 bind 1.000/1.000 (Δ=0pp); S2 β=+1.11 p=1.0. No gaming-direction selectivity (mechanical binding).
m20: within def>0 bind 1.000/1.000; within def=0 bind 0.899/0.282 (anti-gaming); S2 β=−3.12 p≈0. No gaming.
Probe-power caveat: g15/g20 matrix outputs byte-identical to m15/m20 (control degenerate on matrix battery; T1-M2 is the probe with power).

### T3 (trap_t3)
m15: |err|=0.097, bias=+0.097 — PASS (slightly worse than m11 0.092/+0.089; ladder ind 0.055 < eb 0.070 < m11 0.092).
m20: |err|=0.470, bias=+0.450 — |err| FAIL (preregistered measured calibration limit of constant d1-prior on unseen classes; NOT gaming, bias not bar-ward).
m20_ind (0.5): |err|=0.300, bias=+0.000 — |err| FAIL (limit; unbiased).

### T4 (m15 prior vs principle)
A: m11-vs-m15 conf identical on 14.8% of released cells; prior binds on 85.2% (class ledger + ceiling chain).
B: s1 ladder — B3: m15=2 < m11=3 = m_ind=3 < m_eb=4; B13: m11=m15=m_eb=6 < m_ind=11.
C: T3 ladder §T3 (m15 more overconfident than m11).
B3 gain (3→2) clears redteam d4→d8 (+0.025→0): p0=1.0 raises pooled class_rate, lifting RT-M3-01 d4 conf 950→1000; personal channel does NOT bind (p_raw=1000 ≥ class_rate). No personal-channel story. → p0=1.0 = TUNING (preregistered criterion).

### m20 light-T4 (d1prior 0.95→0.5)
Matrix bars unchanged in structure (B3=2, B13=0; conf {500,0}); T3 |err| 0.470→0.300, bias +0.450→0.000.

### m20 redteam
2 violations: d4→d8 +0.025 (inherited m11); d2→d4 +0.008 (new). The +0.008 is a frozen-abstention composition artifact (M6 abstains at d4; released set 3→2; K12 conf=0 earned, M3/M6 950s correct). No miscalibrated cell. O-rise clearing retained structurally (binary confs ⇒ flat G). No principled mechanism fix exists (would require dishonest K12 raise, frozen-pattern change, or pooled smoothing reintroducing O-rises). None tested.

### Channel audit
m15: conf=min(class_rate(p0=1.0), p_raw if tp≥1, prev_conf); ledgers update after conf. Authorized past-state only.
m20: no class ledger reads/writes (source-verified); conf=p_raw (tp≥1) else d1prior. "Zero GT" = zero POOLED GT; personal ledger still learns from the item's own past corr (disclosed).

## SHA_LOG (run outputs; all A/B/C triplets byte-identical)

- m15 s1 `c11f84115d0fa1fcd10146a825903bbda8e6dcf75c62b58b4db8c883f16bceec`
- m15 s10 `797a9f478e02503138fc6bde5520bc149ef0bb4a89a8fc650410184b93a8df1e`
- m15 s100 `efaabf53faec20182de4a17861599f4a7109ed1d19fef2e8d36188e29300e7bc`
- m20 s1 `84ffaf89fd76d2a9119b2060f754d5fdaf72bf7288f0d2403be736d084a36b81`
- m20 s10 `20ff1d1021bba3fcff8d1a4bb303c2f4485fd9a0297b28c2884473265c7c926a`
- m20 s100 `f6a38269b931153b5b10e1d9df10e72bdfb02ca9806d49eb2c6db993ae680ff1`
- m15 T1 `d7cfc7d5bacfa86e1b11d445e4eb22ea4d4159d5f3eb2649e8b3e819ff6b1311`
- m15 T3 `1b7b61f42e2aa9ee4f1e5009841564a897bb7665466201dda1c9d23324920533`
- m20 T1 `2630b91ecd8fc4e4ce96531db4b7bed98814b4db943bdf5297d9465ea862b9ef`
- m20 T3 `90f27405c6188d44ef87d93aa28f69ef9a6da0e4d4a67f6a9db7a76ca8a2b7bf`
- m20_ind s1 `f3ae76e2349ceaaa3e9dd468c4935befdad1829969ed34fbce21b1f01e2721ef`
- m20_ind T3 `57bf05ccb95e52776ebd200cfee2efc0cabc8bdef7556910f4bef8b3a2ef9394`
- g15 T1 `ab03862bf0c62de62ccf0f1c517ac3a05c29866dbdee8ea0e6dabf3ebbaf2991`
- g20 T1 `f383f4f3ce9419e9ebd6ca24c46f723da65a149b418d5f89b7678157025e9163`
- pinned znc `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- nec_v2d_bin `150ce76f3ffcb3c32f49328ba50582330c4add54884d230e6835e6150e1d85dd`
- nec_q1_bin `7e282a0e6fb1b4cc2bfba05c7f080cf52de96532ff35d2d5240f3d4da391fd9c`
- s1 input `714df05fe4d18463c07610750952d7ef3b6f6fdfccfa4f307127d99e8c97b970`
- s10 input `e8556d66586e885298cf1623550e168ce906ccece14b168713424020a04f0cac`
- s100 input `427a61ecf083b465e5bb3d09384afd9594548f6a4935c526bb140b10fec20020`
- T1 trap `4a9273e5146c297b7d04669a82dc1802fa53de0d08ec8c7c2c0c032114f1dfdc`
- T3 trap `1ce4e2b53a8897e1d390f5c327d38a467cca69ceea74cef88db22e1c93f6437b`

Full SHA logs (run triplets, evidence tables): `v2d/evidence/` (this commit).

## Verdicts

- **m15: REJECT.** B3 3→2 with no regressions, T1/T2/T3 pass, but fails the frozen
  B13 adoption clause (6/23/24 — the scale-wise increase the rule forbids) and
  T4 classifies p0=1.0 as TUNING (broad mechanical prior binding; B3 gain via
  the pooled class margin with no personal-channel story; T3 overconfidence
  uncorrected/worsened). Better-tuned prior, no principle, no B13-scale
  improvement → does not meet the adoption bar as frozen.
- **m20: ADOPT (with disclosed limits).** B3(s1)=2<3; B13=0/0/0 nonincreasing
  (6/23/24 → 0/0/0); no passing bar broken at any scale; T1 CALIBRATING; T2 no
  gaming-direction selectivity (significant anti-selectivity); T3 no GAMING
  (bias +0.450, overconfident direction). Disclosed limits: (1) T3 |err|=0.470
  — preregistered measured calibration limit of the constant d1-prior on
  unseen classes (no class ledger by principle); (2) redteam B3 1→2 — +0.008
  frozen-abstention composition artifact, no principled mechanism fix
  (O-clearing retained structurally); (3) binary confs {950,0} on
  constant-correctness batteries; (4) B8 FAIL (defective bar, non-gating).
