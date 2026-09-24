# V-QUOTA Build & Determinism Proof

## Source identity

- `src/webg_quota.zag` — the variant source (BF1 + V-QUOTA addon).
- Base: `webg_quota_base.zag` = `variants/v-bf1/webg_bf1.zag`,
  SHA-256 `dafb2cb7a61451566da23d4c3cda711f59c2bda5df1b26298c6d24ea4080f761`
  (verified before the fork).
- Additivity proof: `webg_quota.zag` minus (`quota_addon.zag` + the
  `quota` dispatch arm) reproduces `webg_bf1.zag` **byte-identically**
  (script-checked at splice time). The strict `verdict` path is untouched.

## Toolchain

Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(the lab-pinned znc; see workspace AGENTS.md).

## Binary determinism

Two consecutive builds of `src/webg_quota.zag` from the same cwd:

- build 1 SHA-256: `51682cf59bed450e86cc985347e89191af23050e16f948c3d609585896d2e05f`
- build 2 SHA-256: `51682cf59bed450e86cc985347e89191af23050e16f948c3d609585896d2e05f`

`cmp`: identical. (Binaries themselves are NOT committed, per lab rule.)

## Verdict-path fidelity

`webg_quota verdict` vs `webg_bf1 verdict` (binary built from the
unmodified BF1 source) on identical inputs:

- R1 battery: 14/14 transcripts byte-identical.
- C1C2 battery: 105/105 verdict transcripts byte-identical
  (10 clusters never reached verdict: fetch/select gates).

## Run determinism (H5-K4)

Two full passes per battery; ledgers, logs, audits, and all `work/`
transcripts byte-identical (`diff -rq` clean):

| Battery | run_quota.log SHA-256 (both passes) |
|---|---|
| R1 | `8da5b8747bc350b6f97ba7a8844e83fcf79ec7de227df760bf1e3d21e9db2427` |
| C1C2 | `792bda5877724483b67380fbe95903f08f427dcca1bb11c10be0070f8123bb96` |
| H0 | `b7324a5f6b33337b195da100c120dc8b980b06171933045cbfd83558edc0d338` |

## Spend-pressure replay (H5-K3)

`scripts/audit_replay.py` independently recomputes E1/E2/E4 eligibility
and the frozen priority order from run artifacts and checks every
`SLOT|` line: **PASS** on all three batteries (R1: 2 candidates;
C1C2: 72 candidates, top-5 = c005..c009; H0: 20 candidates, top-5 =
H0-01..H0-05).

## Mechanism notes (frozen-spec deltas: none)

- E3 is computed via the same `cluster_best` winner the strict path
  uses (not a second `verdict_core` call — whose out-winner is
  post-host-gate and cannot observe the E3 case). Same winner value,
  same inputs; documented here, not a spec change.
- Pure Zag for all mechanisms; zero randomness anywhere (no RNG in
  instrument, driver, or fixtures).
