# R1-PRIMARY run log — D-family distillation (Track 5) replication

Crew: R1-PRIMARY (independent replication, clean environment)
Family: R1 (D-family distillation / Track 5)
Frozen prereg branch: sylorlabs/TNN, branch tnn-native-lab, commit 7b2100d09911c5c10252c5756c7def288e70bd1f
Clean clone dir: ~/workspace/scratch-crossref/R1/clean/
Run dir: ~/workspace/scratch-crossref/R1/primary/
znc: /home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
TMPDIR: /home/hatch/workspace/tmp_commit (NOT /tmp)
Started: 2026-09-22 ~16:00 PDT (subagent dispatch)

## Timeline

- T+0: created scratch dirs; began fresh clone of tnn-native-lab (backgrounded proc_ca6949a29f8e).
- Full clone attempt 1 FAILED after ~61 min at ~1GB (transient disconnect, early EOF).
- Retry full clone reaped by runtime (dir found empty); sibling R5 crew also fighting the same giant clone.
- Strategy change: `git clone --depth 1 --branch tnn-native-lab` (60166 files, ~35 min, exit 0).
- FOUND: branch tip had MOVED past the frozen pin — depth-1 tip was bae78244676d224e0711e2f9dcca0337a7ecdaa6 (2026-09-22 17:08 PDT "Battery 1c: fix kids v3 cutout"), NOT 7b2100d0.
- Fetched frozen commit explicitly: `git fetch --depth 1 origin 7b2100d09911c5c10252c5756c7def288e70bd1f` + `git checkout 7b2100d0`. HEAD now == 7b2100d09911c5c10252c5756c7def288e70bd1f, `git status` clean.
- Frozen tree layout: docs at docs/lab/crossref/ (not crossref/ root); Track 5 at docs/lab/wave12/track5-binding/; Q2 at docs/lab/wave12/q2-distillation/; q1 dirs at docs/lab/q1*/.
- NOTE: crossref/SCOPE.md in frozen tree is byte-identical to the working-tree copy I read for planning.

## Frozen pins (recorded BEFORE any run)

- prereg branch/commit: sylorlabs/TNN tnn-native-lab @ 7b2100d09911c5c10252c5756c7def288e70bd1f ("crossref: scope + frozen preregs...")
- depth-1 clone caveat: full history unavailable; evidence pinned by tree content at this commit. Branch tip at clone time: bae78244676d224e0711e2f9dcca0337a7ecdaa6 (post-freeze commits exist; NOT used).
- znc: /home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1, sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
- Track 5 binding evidence: docs/lab/wave12/track5-binding/evidence/logs/SHA256SUMS.txt (committed); metrics.csv committed.
- Q2 corpus: docs/lab/wave12/q2-distillation/corpus/ (verdict claims sha256 42aff7817739fe4db0cbf5b5972181562cd7b86ae3c76cbae655e15fbef1bada; will verify)
- Build strategy: copy src trees into primary/ scratch, build from the src dir as CWD (@import resolves relative to CWD), --no-zagd --no-analyze --no-foreground-cache, binaries into primary/build/ (never committed, never in clean tree).

## Build + rerun phase

### Track 5 (A/B/C comparison)
- Copied frozen track5-binding/src/ into primary/src/track5-binding/; verified byte-identical (diff -r clean).
- Built t5_trial.zag with pinned znc (--no-zagd --no-analyze --no-foreground-cache): `znc: wrote native binary build/t5t_bin (273867 bytes main, 0 external tools)`.
- Smoke: `t5t_bin bind X 1 0 1` → exit 0, byte-identical to committed evidence/logs/bind_X_rep0_s1.log. Domain hash `7cd0baf80a62acc338e1c9bdec5b33c0e3427af18d78b98b7cbda153a3f92ee8` = expected; digest `3d47f483150ff932625ac9d0340da910057b56aa8375f8b4c292c1cef1842007`.
- Full battery driver run_t5.sh: 75 configs (36 bind s1 + 36 btrap + 3 s10) × 3 runs each, byte-identity within triple, byte-compare vs committed evidence. Driver session was reaped by the runtime at 71/75; remaining 4 configs (btrap_Y_rep11 + 3 s10) rerun individually with identical protocol — all passed.
- Result: 75/75 configs × 3 runs byte-identical; matched_committed=75, fail=0. SHA256SUMS written to logs/t5/SHA256SUMS.txt.
- recompute_t5.py (glue; uses the FROZEN analyze_bind.py cost formula, confirmed in the file: `1.0/(1.0 + esc_per_100 + 0.1*ops_per_ep)`) recomputed from my logs:
  - B-learned: M=1.000000 Rv=1.000000 I=1.000000 Rt=1.000000 C=0.910775 S0=0.991077 → **0.9911**
  - C-hybrid: M=1.000000 Rv=1.000000 I=1.000000 Rt=1.000000 C=0.893078 S0=0.989308 → **0.9893**
  - A-planted: M=1.000000 Rv=0.000000 I=1.000000 Rt=1.000000 C=0.052360 S0=0.655236 → **0.6552**
  - (My first pass of the glue divided the escalation term by 100 twice — the prereg prose "esc/100ep" is ambiguous; the frozen analyze_bind.py disambiguates. Corrected, matches committed exactly.)
- K-T3 checks on my data: mastery parity 0.0000 ≤ 0.05; revisability delta 1.0000 ≥ 0.20; C beats B on zero metrics ≥ 5pp → K-T3 fires.
- Integrity hard gate: all trap families 20/20, hallu ≤ 1, K1=K2=K3=1, refusal=1 on all 36 reps → PASS.
- S10 no-degradation: all arms mastery 1.0000, revisability unchanged → PASS.

### Substrate gap (found, resolved, documented)
- Initial Q2 build failed: frozen q2-distillation/src/ lacks substrate/cl/common.zag (its substrate/ has only the two R33 native files). Same for the three noise-leg src trees.
- Investigation: the frozen q1b-teacher-bakeoff/src/substrate/ has the FULL substrate; its cl/common.zag is byte-identical (sha256 8aec83cb…) to track5-binding/src/substrate/cl/common.zag; the noise legs' R33 files are byte-identical (e6379ddb…) to track5's. The frozen Q2 prereg specifies "verbatim Track 5 substrate copies" / "identical substrate". Conclusion: one wave-canonical substrate; missing cl/ is a committed-tree gap, not a different artifact.
- Resolution: build areas completed with the wave-canonical frozen substrate bytes (byte-identical where files overlap). Proof of faithfulness: all 375 rerun outputs are byte-identical to the SEALED committed evidence (including sealed SHA-256 map, session digests, corpus digests) — a wrong substrate could not reproduce sealed digests.

### Q2 (D1/D2 distillation)
- Built q2t_bin (320838 bytes main, 0 external tools) from frozen Q2 sources + canonical substrate.
- Smoke: bind D1 3 0 1 and bind D2 4 0 1 → exit 0, both byte-identical to committed evidence logs.
- Q2 corpus SHA verified at 42aff7817739fe4db0cbf5b5972181562cd7b86ae3c76cbae655e15fbef1bada; binary embeds Q2_CORPUS_SHA256 with the same value (P4 startup check passed on every run).
- Full battery run_q2.sh: 50 configs (24 bind + 24 btrap + 2 s10) × 3 runs = 150 runs; matched_committed=50, fail=0, ALL RUNS OK.
- From my logs: D1 cost=0.0514 (esc=12, ops=547, eps=68) → comp 0.6551 ✓; D2 cost=0.9108 (esc=0, ops=289, eps=295) → comp 0.9911 ✓. D2 revisability 1.0000 ≥ 0.90, D1 0.0000 < 0.20 → K-Q1 fires; E_dump=E_obs=E_prb=0 → K-Q2 never fires.

### Q1B (learned teacher = planted teacher)
- Built q1b_bin (239239 bytes main) from frozen sources (full substrate present in tree; no additions needed).
- N=5 runs: all exit 0, all byte-identical, sha256 407974c35c68b5e2a234d3d17bfdf1847201ba3f47811af6fa8e07222190d151 = committed evidence/n5_sha256.txt ×5; run1 byte-identical to committed run1_stdout.txt.
- Q1B_DIGEST,planted,learner = Q1B_DIGEST,learned,learner = 6317c2dcf17e850c6e1419f547a8723efdeeda3a9747baf5f8af019ba3092467 (teachers themselves differ: 6aee9aa2… vs 6f387ee3…). Claim confirmed exactly.

### Noise series (no knee)
- Built q1n_bin, tqn_bin, q1tq_bin from frozen sources (+ canonical cl/, as above).
- Q1N 10%: N=5 byte-identical, hash e0bbbbd21ce4928e9c424017d591969cb55dcef28ed77fbfa29a782b39c4661f = committed; Q1N_ACCOUNT,taught,19,0,4.
- TQN 25%: N=5 byte-identical, hash e8983ac4e3e0b42360442015c45dc51b18267d5753a518c5b79784d337fd63d4 = committed; TQN_ABSORB,49,0,49,143,0.
- Q1TQ 50%: N=5 byte-identical, hash 7aa4c7861682660723a1423ba015b75d8e0ecf224b64aedc9aaae8bcb6b3a0a3 = committed; Q1TQ_ABSORB,noisy50,99,0,19.
- Absorption 19/19, 49/49, 99/99; filtered=0 at every level; mastery 173/192, 143/192, 93/192 per committed. No knee.

## Session notes
- Runtime session metadata timeouts ("failed to store metadata … timed out after 15s") hit twice mid-session; retried after sleeps and succeeded. One backgrounded driver (run_t5.sh) was reaped by the runtime at 71/75; the missing 4 configs were completed with the identical protocol and all passed.
- No repo writes, no clean-tree writes, no other workstream touched. Binaries live only in primary/build/.

## Outcome
VERDICT: REPRODUCED. See VERDICT.md. All frozen evidence git tree SHAs recorded there.
