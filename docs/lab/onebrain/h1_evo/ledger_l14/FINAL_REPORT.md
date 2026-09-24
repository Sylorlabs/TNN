# H1 ONE-BRAIN EVOLVE — Crew L14 — FINAL REPORT

**Assignment:** implement and test L1′–L4′ ledger/governance hardening under
`~/workspace/h1evo/PREREG_H1EVO.md` (prior authority
`~/workspace/ob2_ledgergov/PREREG_LEDGERGOV.md`).
**Work dir:** `~/workspace/h1evo/ledger_l14/`.
**Baseline (read-only):** `~/workspace/ob2_repairatk/vb/`.
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Pure Zag, deterministic, zero RNG. Every claim: 3× byte-identical stdout
reruns with SHA-256 evidence (`SHA_MANIFEST.txt`).

**Standing constraints honored:** NO winner declared. N-AUTH parked, not
implemented. L5/offline review out of scope. New backlog IDs from H-OB-81.
`~/workspace/selfpam_run/tnn-lab` never touched. Baseline sources copied
pristine into `v0/` (read-only); all evolution in `src/` + `tests/`.

---

## 1. V0 baseline (evidence `evidence/v0_*_{1,2,3}.txt`, binaries `bin/v0_*`)

Built `ob_test_mem`, `ob_test_arbiter`, `ob_test_fl2`, `ob_test_pam`,
`r2_atk` from pristine sources. Each: 3× byte-identical, OB_FAILURES,0.

## 2. What was built

### L1′ — exact-byte tamper hashing (`tests/l14_l1_test.zag`)
The frozen kill bar ("hash the exact raw bytes that crossed the trust
boundary; whitespace mutations must NOT verify") was adopted over the
conflicting "whitespace-collapsed pre-escape" caption: the ledger hashes
**exact raw, unescaped runtime bytes**; any normalization happens before
bytes enter the ledger, never inside verification. 39 checks: 12 honest
payloads (quotes, backslashes, tabs, newlines, space variants) all verify;
byte flips, whitespace insert/convert, quote/backslash mutations, truncation
and appends all caught; normalization traps prove raw≠escaped and
whitespace variants hash differently.
→ **HOLDS** — `evidence/l14_l1_{1,2,3}.txt`, 3× identical,
sha256 `a3296546…ccd4`.

### L2′ — checkpoint identity + bound rollback (`src/ob_mem.zag`, `tests/l14_l2_test.zag`)
- MEM header 12→20 bytes: guarded clock@16 (see L3′).
- `mm_checkpoint` now **returns the checkpoint id** (preregistered breaking change).
- Checkpoint audit entries bind `{id, episode/clock, 12-byte SHA-256 over exact
  snapshot bytes}` (12 bytes = 3 free words of the frozen 12-word entry;
  residual H-OB-81).
- `mm_rollback_to(..., id)` rehashes the supplied sidecar, rejects unknown
  ids / digest mismatch **before mutation** (`MA_REFUSED_CKPT`=107); refused
  and honest rollbacks write discriminating audit entries.
- Replay keeps snapshots by explicit checkpoint id; `mm_replay_core` /
  `mm_replay_from` added; legacy `mm_rollback` kept as a latest-checkpoint
  wrapper that still enforces the binding.
- 37 checks: forged sidecar refused, state provably unmutated, entries
  discriminate forged vs honest, unknown id refused, non-latest rollback,
  genesis vs midpoint vs tail replay convergence.
→ **HOLDS** — `evidence/l14_l2_{1,2,3}.txt`, 3× identical,
sha256 `92c449dc…a57f13`.

### L3′ — guarded clock (`src/ob_mem.zag`, `tests/l14_l3_test.zag`)
Audit/MEM step timestamps use guarded clock `hdr@16`; legacy `hdr@4` is
inert (old direct-write attacks cannot forge clocks). `mm_clock_advance`
accepts any nonnegative strictly-forward move (no arbitrary max stride —
per the standing "limits are not a thing" law, a forward jump to 500 via the
sanctioned API is valid); rejects zero/equal/negative/backward; every
attempt audit-logged (`MA_OP_CLOCK`=10, refusals 108).
→ **HOLDS** — `evidence/l14_l3_{1,2,3}.txt`, 3× identical,
sha256 `96ad616c…94088`.

### L4′ — governance triage: priority lane + reservations
(`src/ob_common.zag`, `src/ob_arbiter.zag`, `src/ob_pam.zag`, `tests/l14_l4_test.zag`)
- Queue: tail 4 slots reserved for `M_FORCE_PIN` (`LANE_N`); ordinary traffic
  capped at `[0, cap-4)`; total physical allocation unchanged (no new cap —
  a partition, per the no-arbitrary-limits law). Force-pin drains first,
  is applied, is audit-traced.
- Arbiter audit: ordinary entries stop at 960; 64 reserved for governance
  (`ARB_GOV_RES`; state word@8 counts governance overflows explicitly —
  never silent). `M_FORCE_PIN`, `M_PAM_VERDICT`, `ARB_REFUSED_CONTRADICTED`
  route via `arb_audit_gov`.
- PAM: ordinary observations stop at 56 rows; 8 reserved via
  `pam_observe_gov`. Disposition ledger is now a 256-entry **ring**: every
  verdict logged, oldest evicted once full, evictions counted
  (`PAM_EVICTED`) — zero unlogged ADMITs.
- 82 checks: 10k-junk flood (all 10,000 processed; ordinary audit caps at
  960 with 64 reserved); 252-junk + genuine pin → pin lands/applies/audits/
  drains-first; junk cannot steal lane slots; lane-full boundary (4 ok, 5th
  → −1); PAM reservation boundaries; 301 verdicts → all rc 0, ring holds
  #45..#300 in order, evicted=45; audit reservation boundary with explicit
  overflow count.
→ **HOLDS** — `evidence/l14_l4_{1,2,3}.txt`, 3× identical,
sha256 `dc34eaa7…fbc60`.

### ZD — zero drift
All four organ suites + `r2_atk` (R2a–d): 3× byte-identical AND
byte-identical vs V0 outputs, OB_FAILURES,0 throughout.
(`evidence/l14_{ob_test_mem,ob_test_arbiter,ob_test_fl2,ob_test_pam,r2_atk}_{1,2,3}.txt`)

### LH — 10×/100× mixed streams (`tests/l14_lh.zag`, `bin/l14_lh`)
One binary, `argv[1]` selects 10/100 units; each unit is a deterministic
function of its index (clock advance, 2 adds, checkpoint, honest rollback to
u−2 on a scale-independent schedule, forged rollback attempt every 5th unit,
20 scripted arbiter messages + force-pin every 7th, 3 PAM verdicts, bounded
gov observations). End-of-run: genesis replay ≡ live; midpoint replay from
checkpoint units−2 converges.
- 10×: OB_FAILURES,0, 3× identical, sha256 `f7914e6a…b70`.
- 100×: OB_FAILURES,0, 3× identical, sha256 `d2cf547f…a2c8`.
- Prefix consistency: 100× first-10-unit lines ≡ 10× unit lines ✓.
- No new failure mode at 100×: the ring engages (evicted=94 at 100× under
  mixed arbiter+driver verdict load) — expected, pinned by counts; ordinary
  PAM observations saturate at 56 and later claim messages skip the PAM gate
  gracefully (`slot=-1` guarded; residual H-OB-85).

### Composition smoke (`run_l14_smoke.sh`)
Re-runs the full battery (ZD + R2 + L1′–L4′ + LH10/100 + original attacks),
asserts OB_FAILURES,0 everywhere, byte-identity vs recorded evidence, and
the original attacks' preregistered divergences.
→ **SMOKE,PASS**, 3× byte-identical, sha256 `2ab3f942…d2d7b3`.

### Original L1–L4 attacks vs hardened code (`orig_attacks/`, `evidence/orig_*`)
- **L1** (`orig_l1_escape`): L1_FAILURES,0 — the driver's self-contained mode
  demonstration holds; mode 2 (adopted L1′ semantics) passes 12/12. Kill
  cannot fire.
- **L2** (`orig_l2_checkpoint`): 8 divergences — ALL are the repair working
  (forged rollback → rc 107 refused; forged state never installed; entries
  bound and discriminating; `no_ckpt_binds_bytes` now binds) or the
  preregistered `mm_checkpoint`-returns-id API change (`script_ok` legs).
- **L3** (`orig_l3_clock`): 7 divergences — ALL are raw `hdr@4` writes now
  inert (clock reads 0, never 500/7/999999/−5); the dependent gate legs
  behave as clock=0.
- **L4** (`orig_l4_flood`): kill legs dead — pin applied (2) + audited (1);
  `unlogged_verdicts` metric stable at 45 (now evicted-but-counted, not
  silently unlogged). Count divergences (960/252/56 boundaries) are the
  preregistered triage.

### Static audits
- RNG grep over `src/`+`tests/`: **clean** (only "Zero RNG" comments).
- Compiler-risk audit: **clean** — no `as []i32/u32/u16` indexed tables;
  `.*` only on pointer-typed operands; no slice >2^25 (max ~300KB replay
  table); no `};` in code; no u64 shift/mod; no `_zag_arg` free.

## 3. Verdict table

| Cell | Verdict |
|------|---------|
| L1′ | **HOLDS** |
| L2′ | **HOLDS** |
| L3′ | **HOLDS** |
| L4′ | **HOLDS** |
| ZD (4 suites + R2a–d) | **HOLDS** |
| LH 10× / 100× | **HOLDS** |
| Composition smoke | **HOLDS** |
| Original attacks | **DEAD** (none can break the hardened code) |

**NO WINNER declared** — per assignment; the evidence stands without a
crowned variant.

## 4. Interactions & residuals

- L2′ digest truncation (12 of 32 SHA-256 bytes) is layout-bound, documented,
  not full-strength — H-OB-81.
- Rollbacks restore checkpointed governance state (pins included): consistent
  and audited; confirm desired — H-OB-82.
- Midpoint replay requires tail rollbacks to cite tail checkpoints; cross-
  older-checkpoint replay needs operator-supplied sidecars — H-OB-83.
- `pam_observe_gov` appends rather than jumping to rows 56..63; the
  reservation guarantee (≥8 gov rows) holds regardless — H-OB-84.
- At 100×, saturated ordinary PAM rows make later claim messages skip the
  PAM gate (processed, ungated); intended vs hold-for-review is L5 territory
  — H-OB-85.
- L4′ changes are partitions of existing capacity, not new caps (queue 252+4,
  audit 960+64, PAM 56+8) — compliant with the no-arbitrary-limits law.

## 5. Backlog (new IDs from H-OB-81)

H-OB-81 … H-OB-85 as listed in §4 / VERDICT.md.

## 6. Evidence index

- `evidence/v0_*_{1,2,3}.txt` — V0 baseline runs.
- `evidence/l14_{ob_test_mem,ob_test_arbiter,ob_test_fl2,ob_test_pam,r2_atk}_{1,2,3}.txt` — ZD.
- `evidence/l14_l{1,2,3,4}_{1,2,3}.txt` — hardened drivers.
- `evidence/l14_lh{10,100}_{1,2,3}.txt` — long horizon.
- `evidence/orig_{l1_escape,l2_checkpoint,l3_clock,l4_flood}_hardened_1.txt` — original attacks.
- `evidence/smoke_{1,2,3}.txt` — composition smoke.
- `SHA_MANIFEST.txt` — SHA-256 of every evidence file.
- `bin/` — all pinned binaries (`l14_*`, `orig_*`, `v0_*`).
- `v0/` — pristine read-only baseline sources; `src/` — evolved sources;
  `tests/` — `l14_l1_test`, `l14_l2_test`, `l14_l3_test`, `l14_l4_test`, `l14_lh`;
  `orig_attacks/` — original L1–L4 drivers (symlinked to `../src`).
