# WI-4 INCUMBENT REFERENCE — unsigned package (hardened replay + arena thin certifier) vs the §3 battery

**Crew:** WI-4 incumbent reference. **Date:** 2026-09-25 (PDT).
**Task:** score the UNSIGNED incumbent package against the frozen §3 battery
(P01–P12) and §4 clean set, producing the reference row for the head-to-head
table. **Measurement only — the incumbent is NOT re-killed here, nothing is
signed, nothing is adopted.**

Frozen refs: `PREREG_GATE_EXPANSION.md` (umbrella, frozen 2026-09-25);
`RE_DERIVATION_CERT_2026-09-25.md` (WI-3); `RE-RUN-LOG.md` §1 (replay matrix);
replay prereg `REPLAY-2026-09-20-v1` (`0f5cf8c594ee`) §10;
`RESIDUAL_RISK_STATEMENT_ARMC.md` (unsigned draft); CERT crew
`redteam/certifier-rebuild/results.tsv`.

## 1. Arena binary SHA verification

| Item | Value |
|---|---|
| Source | `redteam/certifier-rebuild/thincert_rb.zag`, sha256 `d1c50c1b3b14a84473c270b72fa1a5c80a1d9cf3d6753d8b919839df75d03371` (matches WI-3 record) |
| Substrate inputs | `R33_NATIVE_IO_V1.zag` `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8` · `R33_NATIVE_SHA256_V2.zag` `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf` (pinned, from `thin-certifier/certifier/substrate/`) |
| Toolchain (pinned) | `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` |
| Build | `znc build thincert_rb.zag -o thincert_arena`, two fresh dirs, no shared `.zag-cache` |
| Build 1 sha256 | `362089d5a4405b69fe072e1aa8e91481b1237a1852bac9a29d65335c125ebe37` |
| Build 2 sha256 | `362089d5a4405b69fe072e1aa8e91481b1237a1852bac9a29d65335c125ebe37` |
| Expected | `362089d5a4405b69fe072e1aa8e91481b1237a1852bac9a29d65335c125ebe37` |
| **K-BUILD** | **PASS** — 2/2 byte-identical, matches expected and the CERT crew's arena binary |

## 2. Method

Per plant: build dir = plant source (tier M) + pinned `R33_NATIVE_IO_V1.zag`
(tier S, hash-verified); plant built with the pinned toolchain (all 12 built,
rc=0); manifest with `M`/`S`/`BIN` records; **neutral replay evidence**
(`byte_identical=1, varies_with_state=1, exit_ok=1, rebuild_ok=1, runs=8,
tripwire_v2=PASS`) so the verdict is decided by the source rules — this
measures the **certifier layer**; the replay layer is classified from frozen
evidence (§3), not by re-running replay. Attestations byte-identical across
2 full runs (17/17 cases).

Plant sources (provenance per umbrella §3; adaptations documented):

| Plant | Source scanned (sha16) | Provenance |
|---|---|---|
| P01 | v1 `plant01.zag` (`b1d894e73dbc0908`) | `step1a-no-rng-audit/redteam/plants/` |
| P02 | v1 `plant06.zag` (`db5a3c6f122433dd`) | same corpus |
| P03 | v1 `plant03.zag` (`2fae2d219ddad2eb`) | same corpus |
| P04 | v1 `plant11.zag` (`00210050a82d908b`) | same corpus |
| P05 | v1 `plant20.zag` (`d19c61c75a53acec`) | same corpus (synthetic `get_env_flag` stub — the v1 killer shape) |
| P06 | v1 `plant19.zag` (`3b6a125265f51500`) | same corpus |
| P07 | M1 `t_p07.zag` (`09c6cf7ca71ea280`) | M1 crew build (rdtsc ELF child; no corpus source exists) |
| P08 | v1 `plant16.zag` (`742cee3d1ccb0c3d`) | same corpus |
| P09 | M1 `t_p09.zag` (`f7168fc80f7f6fde`) | v3 blind plant17 from `sylorlabs/TNN@7b64c89`, harness import fixed to pinned substrate by M1 |
| P10 | k2prime `plant19/variation.zag` (`938a306bfa50d742`) | `thin-certifier/k2prime-redteam/plants/` |
| P11 | k2prime `plant20/variation.zag` (`1ccee63c44c87e85`) | same corpus |
| P12 | M1 `t_p12.zag` (`f6bd84ecb390336f`) | M1 crew build (no corpus source exists) |

Note: M4's P09 adaptation was the *innocent* (clean) shape and is the wrong
polarity for K-CATCH; the true dirty P09 (above) was used. M4's P05/P07/P12
were crew-written equivalents of the same rationale; the corpus/M1 versions
above were preferred for traceability.

## 3. Per-plant results — the reference row

Certifier verdicts **measured** (arena binary, this run). Replay classes
**classified from frozen evidence** (RE-RUN-LOG §1, replay prereg §10,
residual-risk statement). Package = CAUGHT if EITHER layer catches; GAP if
neither.

| # | Plant | Certifier (measured) | Replay class (frozen evidence) | Package | Layer |
|---|---|---|---|---|---|
| P01 | getrandom(2) 318, byte to output | FAIL — R2 `_zag_raw_syscall` | DIVERGE — §10.1, entropy consumed to output (cf. `dirty1b_entropy_read` DIVERGE) | CAUGHT | both |
| P02 | clock_gettime 228 | FAIL — R2 `_zag_raw_syscall` | PASS — §10.5, clock invoked, value never emitted (`out=input`); cf. `dirty2_clock` PASS 8/8 | CAUGHT | certifier |
| P03 | open(2) /dev/urandom | FAIL — R2 `_zag_raw_syscall`, R6b `urandom` | PASS — §10.5, urandom opened, never consumed; cf. `dirty1_urandom` PASS 8/8 | CAUGHT | certifier |
| P04 | uninit heap read into output | PASS — no rule fires (R3′ allocation-idiom is amendment-pending and **not implemented** in `thincert_rb.zag`; the `R3p=3` id appears only in a code comment) | DIVERGE — §10.3, replay catches uninit reads **only under the §4 adversarial fill**; cf. `dirty3_uninit` DIVERGE pair (0,1), RE-RUN-LOG §1 | CAUGHT | replay |
| P05 | `get_env_flag` env indirection (v1 killer) | PASS — scanner inspects only `_zag_*` tokens; plain `get_env_flag` is invisible, and R6a has no `env_` pattern (the v1 transcription gap was fixed in the v2 auditor's rule 4.5, never in thincert R6a) | PASS — synthetic stub returns constant 0; no live channel | GAP | — |
| P06 | ASLR/pointer leak into output | FAIL — R2 `_zag_slice_ptr` (substrate-only intrinsic in a module) | DIVERGE — §10.2; cf. `dirty5_aslr` DIVERGE | CAUGHT | both |
| P07 | rdtsc via ELF child (M1) | FAIL — R2 `_zag_raw_syscall` | PASS — §10.5, rdtsc executes but the value is discarded (child prints literal "TSC"); a value-emitting variant would be §10.1 DIVERGE | CAUGHT | certifier |
| P08 | hash-iteration order to output (plant16) | PASS — no hash-order rule (`hashmap_slot` is a plain identifier; R6a is `_zag_*` intrinsics only) | PASS — §10.4, fixed hash + index-order emit is deterministic; cf. `dirty4_hash` PASS ("static 4.4 is the layer" — thincert implements no 4.4) | GAP | — |
| P09 | hand-rolled table, innocent names (v3 plant17) | PASS — invisible to the token scan by design (the v2/v3 killer property) | PASS — deterministic slot order across runs (§10.4 analog) | GAP | — |

| P10 | /etc/machine-id via allowlisted file IO (K2′ 19) | PASS — documented; arena-CONFIRMED (this run + WI-3). R6b bans only `urandom`, `/dev/`, `/proc/`, `/sys/`; `/etc/machine-id` is clean | PASS — §10.6 lab-constant env; residual-risk item 6: "zero replay signal, genuine cross-machine variance" | GAP | — (known) |
| P11 | `_zag_arg(0)` path bytes (K2′ 20) | PASS — documented; arena-CONFIRMED. `_zag_arg` is tier-M allowlisted (R2), and the harness contract's "declared inputs" are not a certifier rule | PASS — path string constant under fixed build/run conditions | GAP | — (known) |
| P12 | getrandom invoke-discard (M1) | FAIL — R2 `_zag_raw_syscall` (the token fires regardless of consumption — the scanner cannot see discard) | PASS — §10.5, replay **cannot catch even in principle** (constant function of inputs) | CAUGHT | certifier |

**Reference-row totals: CAUGHT 7/12** (P01, P02, P03, P04, P06, P07, P12) ·
**GAP 5/12** (P05, P08, P09, P10, P11). Certifier alone: 6/12. Replay alone
(from frozen classes): 3/12 (P01, P04, P06). Overlap (both catch): P01, P06.

## 4. Clean set (K-CLEAN reference)

| # | Module | Source | Certifier | Notes |
|---|---|---|---|---|
| C01 | canonical variation | M4 `C01_canonical.zag` as-is (`601d6742c756306c`) | **PASS** | no imports; `_zag_println` tier-M allowlisted |
| C02 | state-dependent phrasing | M4 `C02_state_phrasing.zag` as-is (`e9430dffcae1903a`) | **PASS** | |
| C03 | seeded fenced RNG at declared points | — not run — | out-of-scope (declared) | §4 permits pre-test out-of-scope declaration where the method lacks declared-point allowlisting. Thincert R6a bans `_zag_rand` unconditionally with no carve-out, so the Arm B pattern would FAIL R6a. Declared out-of-scope here. |
| C04 | pinned-substrate file IO | adapted from M4 `C04_pinned_io.zag` to pinned-substrate idiom (`c5cbd3253f3c93e7`); module-local loader via `nio_open_root`/`nio_open_child`/`nio_read_exact`; reads `data/phrases.bin` (M4 fixture) | **PASS** | R1c walk only collects `.zag`, so `data/` is untouched |
| C05 | step-budget timeout | M4 `C05_step_budget.zag` as-is (`96ab7cf549ef24d7`) | **PASS** | |
| C06 | fixed-order map | adapted from M4 `C06_fixed_order_map.zag` (`bdf2b70dbeb08480`): `z_alloc_init` → `nio_alloc` + explicit zero loop; insertion sort → **selection sort** | **PASS** | First adaptation FAILED R5 (`while(b>=0 && …)` is non-canonical); selection sort uses only `while(ident<…)` loops. Same module semantics (fixed-order emission), honest re-expression — recorded here. |

Clean result: **5/5 run modules PASS**, C03 declared out-of-scope per §4.

## 5. Red-history summary (no new plants — tabulation only)

- **K2′ blind red-team round** (the thin certifier's own, per residual-risk
  statement): 20 plants; **17/19 scored plants caught** (t1_plant01–06, 08–18
  FAIL, each naming its rule, 0 misses); t1_plant19/20 PASS/PASS
  (arena-CONFIRMED, this run and WI-3); t1_plant07 INCONCLUSIVE (unbuildable
  with the pinned toolchain — `x86 cpuid expects leaf and subleaf` — no
  stored attestation, not a pass).
- **CERT re-derivation (WI-3, independent):** 25/25 scored thincert cases
  CONFIRMED, 0 flips, 0 voided certifications; the six load-bearing PASS
  certifications (t1_plant19/20, t2_dirty3_uninit, t3_rerun, t3_k3) re-verify
  PASS under the fresh arena binary.
- **Arm C rerun thincert (2026-09-21, RE-RUN-LOG §2):** dirty1_urandom FAIL
  (R6a `_zag_rand` + R6b `urandom`); dirty2_clock FAIL (R2
  `_zag_raw_syscall`); dirty3_uninit **PASS (static)** — the static layer
  does not see uninit reads; dirty5_ptrleak FAIL (R2 `_zag_slice_ptr`).
  dirty1's recorded BIN was not reproducible from frozen sources (evidence
  gap, §3 of that log) — static attribution reproduced exactly.
- **Residual-risk "NOT certified" items 1–6** (unsigned draft, still the
  governing statement): (1) no general static proof — v1/v2/v3 auditors all
  killed, 3/3; (2) two draft amendments underpin the gate (replay-bar and
  THINCERT_R3), both unsigned; (3) lab-constant env nondeterminism;
  (4) output-silent hidden channels; (5) replay-backstop-only classes =
  replay prereg §10 classes 5–7 verbatim; (6) **K2′ novel classes 19
  (machine-id) and 20 (argv0) — "Neither is covered by the current rule
  set"**, coverage requires a dated amendment with Micah's re-approval.

## 6. Known gaps (honest list)

1. **P10 / K2′ plant19** (`/etc/machine-id` via allowlisted file IO) — no
   certifier rule, zero replay signal. Documented in residual-risk item 6.
2. **P11 / K2′ plant20** (`_zag_arg(0)` path bytes) — `_zag_arg` is
   tier-M allowlisted; harness "declared inputs" are not a certifier rule.
   Documented in residual-risk item 6.
3. **P09 class** (hand-rolled tables, innocent names — the v2/v3 killer) —
   invisible to the token scan by design; deterministic instances are also
   replay-silent. Residual-risk item 1 names this as the standing
   structural hole ("invisible to token-based detection").
4. **P08** (fixed-order hash iteration to output) — §10.4 assigns this to
   "static 4.4", which thincert does not implement; deterministic instances
   are replay-silent.
5. **P05** (`get_env_flag` shape) — the v1 transcription gap persists in
   thincert's R6a (no `env_` pattern; only `_zag_*` tokens are scanned).
6. **P04 static** — R3′ (allocation-idiom) is amendment-pending and
   unimplemented; uninit reads are caught **only** by replay under the §4
   adversarial fill. Under the production zeroing allocator without the
   adversarial variant they are behaviorally silent (the W2 failure).
7. **P12 class** (mechanism-without-consumption) — replay-blind by
   construction (§10.5); the certifier catches it only when the mechanism
   uses a banned token. A token-free invoke-discard (e.g. via an allowlisted
   path) would be a gap in both layers.

## 7. Files

- This report: `evidence/incumbent/INCUMBENT_REFERENCE.md`
- Battery dirs (per-case manifest, binary, neutral evidence, attestation):
  `evidence/incumbent/work/battery/{P01..P12,C01,C02,C04,C05,C06}/`
- Runner: `evidence/incumbent/work/run_battery.py`; results:
  `evidence/incumbent/work/results.tsv`
- Arena builds: `evidence/incumbent/work/build1/`, `work/build2/`
  (`thincert_arena` sha256 `362089d5a4405b69fe072e1aa8e91481b1237a1852bac9a29d65335c125ebe37` both)
- No commits made; working tree only, per task.
