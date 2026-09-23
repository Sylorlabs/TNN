# K3′ Hardened Replay — Final (2026-09-20)

**Gate:** K3′ — hardened replay against the exact frozen binary.
**Harness:** phase-1 `REPLAY-2026-09-20-v1` (`docs/lab/wave12/step1a-v2/replay-hardening/`).
**Bar amendment:** `AMENDMENT_2026-09-20_REPLAY_BAR.md` — PROPOSED, pending Micah's
re-approval. Items A (frozen dirty1/dirty2 re-scoped to PASS) and B (control
mismatch → DIVERGE) are noted; verdicts below are provisional until signed.

## Method

1. Phase-1 harness re-ran fresh 2026-09-20: `run_replay.sh variation`
   (8 hardened conditions: BASE, NOASLR, ENV, FDS, CWD, ENVORDER, SKEW,
   COMBINED; per-run adversarial heap tags; determinism control).
2. The harnessed `variation` unit is derived from `modules/variation.zag`
   (sha256 `48b976b6…`), byte-identical to the thin certifier's frozen
   repbuild source. The `vary_expr` logic is the same.
3. Phase-1 evidence bridged to thin-certifier evidence format
   (`/tmp/tck3/k3_evidence.txt`): byte_identical, varies_with_state,
   exit_ok, rebuild_ok, runs.
4. Thin certifier run against the exact frozen binary
   (`75cf2006ca044081caad740afbf29b239a38dc9bb3214e477830912bd943a83c`,
   rebuilt byte-identical twice).

## Results

**Clean frozen build — K3′ PASS (final, amendment-pending):**
- Phase-1: verdict=PASS, 8/8 byte-identical (`97785f…`), control match=1,
  varies_with_state=1, divergent_pair=none.
- Thin certifier: rc=0, verdict=PASS. R1–R7 all PASS. REPLAY=PASS.
- Attestation: `/tmp/tck3/k3_att.txt`.

**dirty3_uninit (defense-in-depth demonstration):**
- Static: all R1–R7 PASS (documented R3′ residual — reads deterministic zeros).
- Hardened replay: DIVERGE (8/8 pairwise divergent).
- Thin certifier with bridged evidence: REPLAY=FAIL (`byte_identical!=`),
  verdict=FAIL. The replay layer catches what static misses.

## Verdict

**K3′: FINAL PASS** for the frozen representative build, conditional on:
1. Micah's re-approval of `AMENDMENT_2026-09-20_REPLAY_BAR.md` (phase-1 bar),
   and
2. Micah's re-approval of `AMENDMENT_2026-09-20_THINCERT_R3.md` (thin R3′).

Until both are signed, K3′ is provisional. The interim 8-condition matrix
result (byte-identical 1–7, varies on 8) is superseded by this hardened run.

## Artifacts

- Bridged evidence: `/tmp/tck3/k3_evidence.txt` (clean), `/tmp/tck3/k3_evidence_dirty3.txt`
- Attestations: `/tmp/tck3/k3_att.txt`, `/tmp/tck3/k3_att_dirty3.txt`
- Phase-1 evidence: `docs/lab/wave12/step1a-v2/replay-hardening/evidence/variation.evidence.txt`
  (fresh run 2026-09-20)
