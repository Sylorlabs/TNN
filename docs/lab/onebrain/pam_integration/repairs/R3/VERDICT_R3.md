# VERDICT_R3 — PROVTAG shadowing repair (O2)

Date: 2026-09-24. Repair crew R3 (residual #3 of 4). Frozen prereg:
`PREREG_R3.md` (committed `5d4584e52342` BEFORE any implementation).
Base: `~/workspace/onebrain_pam_integration/` (untouched);
workdir: `~/workspace/ob_pam_repairs/R3/`.

## Repair summary

**Design (a) — last-write-wins, scoped to the INSTALL path's ledger tag**
(prereg §2). In `sp_gate_one`'s INSTALL branch, the `SP_L_PROVTAG`
`{atom_idx, prov}` rows no longer read the first-match `sp_store_find` tag
(the first sighting — quarantined GEN history). The branch is reachable only
when `sp_verdict` proved every draft atom store-ENTAILED via the EXT-only
closure and trace-EARNED, so the provenance that warranted the install is
EXT by construction; the row records EXT (1).

What was NOT changed (frozen scope):
- `sp_store_find` untouched (first-match still serves `sp_dep_edges`'
  EXT-filtered dependency-DAG edges and `sp_derive_ext` guards).
- No store write added or removed: the store stays append-only; quarantined
  GEN lines and WITHHOLD verdict rows preserve the first-seen GEN history
  as a separate audit trail. Quarantined GEN lines stay out of the EXT
  closure (no trust creep).
- Verdict, conflict check, CONTRADICTED-before-ENTAILED precedence: frozen.
- Rejected alternatives (prereg §2): (b) latest-find breaks K3 and
  `sp_dep_edges`; (c) per-install store appends exhaust the 512-line cap
  and risk trust creep; store-line prov mutation is a K5-class trust-root
  change.

Files changed (identical edit in all three src trees):
- `build/src/sp_gate.zag`, `redteam/src/sp_gate.zag`,
  `longhorizon/src/sp_gate.zag` — INSTALL branch tag computation only.
- `redteam/src/ob_test_redteam.zag` — O2 probe expectation GEN→EXT
  (test-driver expectation update); new machine-checked probes
  `rt_t4_k2_gentag` (K2) and `rt_t4_k3_nodowngrade` (K3) with helpers
  `rt_all_gen` / `rt_first_prov`; hooked into `main()`.

## Kill-bar accounting

| Bar | Result |
|---|---|
| K1 quarantine→EXT-support→INSTALL records prov=EXT | **PASS** — `ro_o2_provtag_shadow,1,1` (was 0 pre-repair); finding now `O2-PROVTAG-REPAIRED` |
| K2 GEN-only claims keep GEN tags | **PASS** — `rk2_k2a/k2b/k2c_stays_gen,1,1` (L2/L3/L4 patterns: all withheld, every store line for the probe atoms prov=GEN, no EXT line appended) |
| K3 GEN sighting never downgrades EXT incumbent | **PASS** — `rk3_incumbent_tag_ext,1,1`, `rk3_gen_sighting_withhold,0,0` + quarantined, `rk3_incumbent_still_ext,1,1`, `rk3_reinstall_tag_ext,1,1` |
| K4 L1–L10 all WITHHOLD | **PASS** — `rl_launder_held,10,10`, `rl_k5_zero_installs,0,0` (no laundering opened; verdict logic untouched) |
| K5 T1–T5 long-horizon unchanged vs frozen refs | **PASS** — see below |
| K6 zero RNG in decision paths | **PASS** — grep scan over all three src trees: only the pre-documented benign `seed_independent` check-name hit |

## Battery results (pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`)

- **Redteam** (`ob_test_redteam.zag` → `ob_redteam_bin`): 3/3 runs
  `RT_FAILURES,0`, `RT_K3_HITS,0`, byte-identical.
  Output SHA-256 (all three): `847e4ef0070c16c37f7e0d7a4623ea45b2237699b6ba6e246d12ca8c39a0c0b8`
  (differs from the frozen `3fa5a17ae97cbf2107880f2f7c6b98fe2af33ed28575c880cacadb3cae37025c`
  exactly by the intended changes: O2 probe now records EXT=1, plus the two
  new K2/K3 probe blocks).
- **Smoke** (`ob_test_integration.zag` → `ob_integration_bin`): 3/3 runs
  `OB_FAILURES,0`, byte-identical.
  Output SHA-256 (all three): `6855928854e38255e7275a18c5b07c82675fe1bc0752a616ba9ca90ba2e6d2e0`
  — **identical to the frozen ref**: zero behavior delta on the smoke
  battery (none of its installs hit the shadowing case).
- **Long-horizon** (`run_lh.sh`, T1/T2/T5): 6/6 runs `OB_FAILURES,0`,
  byte-identical per battery.
  B-alone SHA: `cc7e86ed4a00be36bb4f5a2aacc6456197281270b4eb40717ebb1ca017ea93e9`
  (matches frozen ref); integrated SHA:
  `356b7873bf07942c6b2283ed087911d3bfa724cea1ab707fb1ccaf14821cec3b`
  (matches frozen ref).
  `compare_lh.py`: 76/76 shared LH metrics byte-equal (K4), all 27 B-alone
  OB_CHECK lines verbatim in integrated output, T5 strict beat held
  (40 → 0 false installs).

## Residuals / notes for the parent

- O2 is closed: the ledger no longer mislabels rehabilitated installs.
- The install-time tag is EXT by the gate's own INSTALL precondition; any
  future verdict change that admitted non-EXT-warranted installs would need
  to revisit the tag rule (flagged in PREREG_R3.md §6).
- Sibling residuals N1/N2 (N-AUTH identity), R1–R4 (exhaustion caps), F4
  (poisoned subject) are out of R3 scope and unchanged.

## Commits (sylorlabs/TNN, branch tnn-native-lab)

- Prereg: `5d4584e523422c16743cb8698aedc207ba8ff8a0`
- Evidence+verdict: `f4f1131f6d66f18c0da98d55d8b071fb1b0b3d60`
