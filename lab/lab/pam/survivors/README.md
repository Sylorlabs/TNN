# PAM Survivors — Usable Package (2026-09-25)

Every PAM below was **independently re-verified** on 2026-09-25: rebuilt from
frozen sources with the pinned toolchain
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`), batteries
re-run, outputs byte-identical to frozen evidence, kill bars re-adjudicated.
Pure Zag, zero RNG. Full method and per-arm SHAs: `REVERIFICATION_2026-09-25.md`.
Runbook: `RUNBOOK.md`. Everything still needing Micah's signature:
`GOVERNANCE_GAPS.md`.

**Nothing here is unqualified.** Each entry states its scoped claim and its
limits. Killed arms are NOT listed as usable (W5, W10, W14 stay dead; W13 is
HOLD, not usable).

## Composition

| PAM | Status | What it does | Canonical source |
|---|---|---|---|
| H-PAM-3034COMP-X3 | **DEMOTED** (not killed, not survived) | 30+34 composition driver: owns queue, K counting, clocks, gap auth, digests, trajectory, ledger, sink call. Refuses all attack classes, admits honest 120/120, anti-stub ablation moves all 7 required classes. | `docs/lab/senses/pam-rebuild/round2/b3034comp/x3/src/` |

## Individual PAMs

| PAM | Status | What it does | Canonical source |
|---|---|---|---|
| H-PAM-35 | **SURVIVED, unforgeability-only** | Full-64-bit tag binding closes the J-35 forgery path. Does NOT claim verdict-bit authority. | `docs/lab/senses/pam-rebuild/round2/r35/` |
| H-PAM-36 | **SURVIVED, standalone temporal game** | Commit-then-sample + fresh-seed discipline; M-36 installs 0/120. Rests on fresh-seed discipline as harness policy. | `docs/lab/senses/pam-rebuild/round2/r36_repair/` |
| H-PAM-33 | **KILLED as gate; RETAINED as channel-integrity check** | WG fires 20/20 plain + 20/20 manifest. Conditional survival requires escape-(i) enforced externally. | `docs/lab/senses/pam-rebuild/round2/round_c/hpam33/` |
| H-PAM-30 | **DEMOTED to composition-only** | Anti-RF + anti-RC + anti-XR + explicit goal-set + distal exclusion + conf>=95 sink gate. Kill bars green; triage bar fired. | `docs/lab/senses/pam-rebuild/round2/b303134/` (`drive30.zag`) |
| H-PAM-34 | **Coarse KILLED; full-pin DEMOTED** | Full-pin form is "H-PAM-30 with a delay line" — no independent admission claim. | `docs/lab/senses/pam-rebuild/round2/b303134/` (`drive34.zag`) |
| H-8 (H-PAM-8) | **Tripwire / audit ONLY** | Detects 3/3 named hidden common causes (100% agree, premium_bp=0). A pass must NEVER be used as attestation of causal independence. | `docs/lab/senses/pam-rebuild/round2/d1_build/` |

## WILD survivors (PAM Round 4)

| PAM | Status | What it does | Canonical source |
|---|---|---|---|
| W1 deliberation-vote | **SURVIVED** | C 82.67%, W 0/12, 0/14 attacks. Vote threshold 650 load-bearing. | `docs/lab/pam/round4/wild/w1/` |
| W2 adversarial pair | **SURVIVED** | C 72.69%, both-must-agree. Skeptic/advocate pair. | `docs/lab/pam/round4/wild/w2/` |
| W3 veto-only | **SURVIVED** | C 82.58%, 14/14 attacks vetoed. M1 bar admit path + vetoes. | `docs/lab/pam/round4/wild/w3/` |
| W4 self-train | **SURVIVED with documented tradeoff** | Admits 0/12 wrongs where frozen M1 admits 12/12. C only 39.29% — correctness over coverage. | `docs/lab/pam/round4/wild/w4/` |
| W6 arguing PAMs | **SURVIVED** | C 83.21%, 0 wrongs. Persuasion rounds, >=2/3 majority. | `docs/lab/pam/round4/wild/w6/` |
| W7 laundering-hunter | **SURVIVED** | TPR 100/100, FPR 0/100; score gap laundered 675-950 vs genuine 108-546. | `docs/lab/pam/round4/wild/w7/` |
| W8 retro-PAM | **SURVIVED** | 12/12 W + 18/18 P revoked; 0/1102 C revoked; fence_cross=0. | `docs/lab/pam/round4/wild/w8/` |
| W9 render-PAM | **SURVIVED** | C 75.23%, 0 wrongs. Fidelity threshold 0.55 is brittle (thin band 10,979-11,109). | `docs/lab/pam/round4/wild/w9/` |
| W11 chain-of-custody | **SURVIVED** | 370/370 dispositions vs independent HMAC recompute; 0/170 attacks; 0/60 forgery. | `docs/lab/pam/round4/wild/w11/` |
| W12 budget-PAM | **SURVIVED** (K1 premise failure carried) | 1132/1132 + 628/628 rows match mirror. K1-as-written trips on 2 frozen-bar items [1124, 1126] — premise failure is real, frozen, upstream. | `docs/lab/pam/round4/wild/w12/` |
| W15 quarantine | **SURVIVED** | F-K5 0/200, K1 0/30, LIVE 4998/4998. | `docs/lab/pam/round4/wild/w15/` |
| W16 CTG | **SURVIVED** | 4/4 laundering re-jurisdicted; 6/6 forgery probes blocked. | `docs/lab/pam/round4/wild/build/` (`wildc.zag` design 16) |
| W17 CC | **SURVIVED** | 14/14 attacks kept out; probe quarantined. | `docs/lab/pam/round4/wild/build/` (`wildc.zag` design 17) |
| W18 NKL | **SURVIVED** | Veto machinery. **0% attack catch by prereg design** — never present as an attack-catcher. | `docs/lab/pam/round4/wild/build/` (`wildc.zag` design 18) |
| W19 AF | **SURVIVED** | 0/14 attacks admitted; unstaked probe handling. | `docs/lab/pam/round4/wild/build/` (`wildc.zag` design 19) |
| W20 ETB | **SURVIVED** | C 71.69%, 0/14 attacks in FACT. Prereg inconsistency open (see governance gaps). | `docs/lab/pam/round4/wild/build/` (`wildc.zag` design 20) |
| W21 DIR | **SURVIVED** | 14/14 attacks vetoed; anchors not vetoed. | `docs/lab/pam/round4/wild/build/` (`wildc.zag` design 21) |
| W22 TPC | **SURVIVED** | 0/14 committed; divergence emitted on probe. | `docs/lab/pam/round4/wild/build/` (`wildc.zag` design 22) |
| W23 TRR | **SURVIVED** | C 96.64% via 274 SINGLETON promotions; 0/14 attacks promoted. | `docs/lab/pam/round4/wild/build/` (`wildc.zag` design 23) |

## CU track

| Claim | Status | Meaning |
|---|---|---|
| Conscious PAMs worth their cost | **ADOPTED (re-verified)** | KB-CU-WORTH PASS: intro 1.00 >= 0.85, speed ratio 7.915x <= 12x. |
| P-UNC holds | **RE-VERIFIED** | G_full +0.0, K1 GREEN, necessity agreement 0.0 < 0.90. |
| P-CON falsified | **RE-VERIFIED** | G +0.0, cycles 7.915x, agreement 0.0 — three independent failures. |
| P-HYB fails cost bar | **RE-VERIFIED** | 2.434x > 1.3x bar. |
| Both arms catch 40/40 laundering | **RE-VERIFIED** | LAU 40/40, FORK 30/30, AUTH 30/30 both arms. |

Canonical CU source: `docs/lab/pam/round4/cu/` (`cu_pam.zag`, `cu_query.zag`, `score_cu.py`).

## Not usable

- **W5** (PAM-as-memory): CONFIRMED DEAD — KB-W5-M fired (27/2035 hit-mismatches).
- **W10** (forge-duel): CONFIRMED DEAD — D1 fired (573/1102 C duel-rejected).
- **W14** (auction): CONFIRMED DEAD — K1 + F-K2a fired (392/392 false percepts with margin>0).
- **W13** (epistemic lease): HOLD — separate hard-research track; not usable pending redesign.
- **H-PAM-31**: killed. **H-PAM-3034COMP-X3**: demoted, not survived.
