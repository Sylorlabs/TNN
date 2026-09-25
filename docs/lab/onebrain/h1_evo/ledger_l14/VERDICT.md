# H1 ONE-BRAIN EVOLVE — Crew L14 — VERDICT.md

## Verdicts (each cell marked per prereg §2 kill bars)

| Cell | Verdict | Evidence |
|------|---------|----------|
| L1′ exact-byte hashing | **HOLDS** | `evidence/l14_l1_{1,2,3}.txt` — 39 checks, OB_FAILURES,0, 3× byte-identical, sha256 `a32965468a99c648f434da2d3155184868771c5877bb1e08eeafe8275126ccd4` |
| L2′ checkpoint identity + bound rollback | **HOLDS** | `evidence/l14_l2_{1,2,3}.txt` — 37 checks, OB_FAILURES,0, 3× byte-identical, sha256 `92c449dc3b0ca4505fff58ab951c5c5c1e810e92348585583dd3a68c47a57f13` |
| L3′ guarded clock | **HOLDS** | `evidence/l14_l3_{1,2,3}.txt` — 33 checks, OB_FAILURES,0, 3× byte-identical, sha256 `96ad616cf7ede4f13ff9d8f1725349f4d11b6d7ea7828171306c8a8828e94088` |
| L4′ priority lane + reservations | **HOLDS** | `evidence/l14_l4_{1,2,3}.txt` — 82 checks, OB_FAILURES,0, 3× byte-identical, sha256 `dc34eaa7703fbbeed2d508498af975eac8ed5bb4c6930b7ae36f07177e9fbc60` |
| ZD (4 suites + R2a–d) | **HOLDS** | `evidence/l14_{ob_test_mem,ob_test_arbiter,ob_test_fl2,ob_test_pam,r2_atk}_{1,2,3}.txt` — all OB_FAILURES,0, 3× identical, byte-identical vs `evidence/v0_*_1.txt` |
| LH 10× | **HOLDS** | `evidence/l14_lh10_{1,2,3}.txt` — OB_FAILURES,0, 3× byte-identical, sha256 `f7914e6a5da4e45841c8a7a13c83996780e5341b998f2eb4674e69b0bbe43570` |
| LH 100× | **HOLDS** | `evidence/l14_lh100_{1,2,3}.txt` — OB_FAILURES,0, 3× byte-identical, sha256 `d2cf547fcd8a33c2cb29e872e0f18bcbeaf541e1a70c6c88e66bc921daeedba2c8`; prefix-consistent with 10× |
| Composition smoke | **HOLDS** | `evidence/smoke_{1,2,3}.txt` — SMOKE,PASS, 3× byte-identical, sha256 `2ab3f9427103244200c3589f5b5e02eed3a27db879636fa828fc1f6ad2d2d7b3` |
| Original L1 attack | **DEAD** (kill cannot fire) | `evidence/orig_l1_escape_hardened_1.txt` — L1_FAILURES,0 (mode-2 adopted semantics pass 12/12) |
| Original L2 attack | **DEAD** | `evidence/orig_l2_checkpoint_hardened_1.txt` — 8 divergences, ALL = repair working (forgery refused rc=107, state unmutated, entries bound/discriminating) or the preregistered `mm_checkpoint`-returns-id API change |
| Original L3 attack | **DEAD** | `evidence/orig_l3_clock_hardened_1.txt` — 7 divergences, ALL = raw hdr@4 writes now inert (clock reads 0, never 500/7/999999/-5) |
| Original L4 attack | **DEAD** | `evidence/orig_l4_flood_hardened_1.txt` — kill legs dead: pin applied (2) + audited (1); ring metric stable (45); count divergences are the preregistered triage (960/252/56 boundaries) |
| RNG audit | **CLEAN** | static grep over `src/`+`tests/`: only "Zero RNG" comments; no rng/rand/seed/random in code |
| Compiler-risk audit | **CLEAN** | no `as []i32/u32/u16` indexed tables; `.*` only on `*i32`; no slice >2^25 (max ~300KB replay table); no `};` in code; no u64 shift/mod; no `_zag_arg` free |

## Breaking inputs (preregistered, EXPECTED divergences)

- **L1′**: any payload whose escaped/whitespace-normalized form differs from raw bytes (quote, backslash, tab/newline/space variants) — old harness hashed the collapsed form; L1′ hashes exact raw bytes.
- **L2′**: forged sidecar + `mm_rollback_to` → `MA_REFUSED_CKPT` (107); `mm_checkpoint` now returns the checkpoint id (old drivers asserting `!=0` see a nonzero return — API change, not a failure).
- **L3′**: any direct write to `hdr@4` (500, 7, 999999, −5) — now inert; clock reads via `mm_clock`/`mm_clock_advance` on `hdr@16`.
- **L4′**: 253rd ordinary queue enqueue → −1; 57th ordinary PAM observation → −1; 961st ordinary arbiter audit → −1; 65th governance audit → −1 with explicit overflow counter. Ordinary arbiter audit caps at 960 (was 1024); queue ordinary region 252 (was 256).

## NO WINNER declared (per assignment)

No repair variant is crowned; N-AUTH remains parked; L5/offline review out of scope.

## Backlog (new IDs from H-OB-81)

- **H-OB-81**: L2′ digest truncation — checkpoint audit binding carries 12 bytes of SHA-256 (frozen 12-word entry layout), not full 32. Documented residual; revisit if the entry layout is ever unfrozen.
- **H-OB-82**: Rollback restores checkpointed governance state (force-pins included) — consistent and audited, but confirm this is the desired semantic vs. pin-survives-rollback.
- **H-OB-83**: Midpoint replay contract — tail ROLLBACKs must cite tail checkpoints; operators replaying across older checkpoints must supply those sidecars (API currently accepts one starting sidecar).
- **H-OB-84**: PAM gov observations append (ordinary rows) rather than jumping to rows 56..63; reservation holds (≥8 gov rows always available) but placement is not reservation-first. Decide if placement should be strict.
- **H-OB-85**: At 100×, ordinary PAM observations saturate (56) and later claim messages skip the PAM gate (`slot=-1` handled); confirm the intended degradation is "gate skipped, message still processed" vs. "message held for review" (L5 territory).
