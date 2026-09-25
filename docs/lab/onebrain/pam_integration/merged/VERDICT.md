# MERGED VERDICT — one-brain + self-PAM R1–R4 integration

Date: 2026-09-25. Branch: `tnn-native-lab`. Prereg: `MERGED_PREREG.md` (commit
`d2c71e8ee839cdfb706d3eb08e05ba7b63376b84`).

## Verdict: ADOPT

All four repair kill-bar suites hold unweakened in the merged tree, all three
cross-repair interactions pass, all batteries are 3× byte-identical with zero
RNG, and legitimate behavior is byte-identical to the frozen refs.

## Per-repair bars (merged tree)

### R1 (N-AUTH)
- K1–K4: forged-identity / force-pin / replay / wrong-key attacks refused at
  auth (red-team N1–N5 probes, RT_FAILURES,0).
- K5: smoke + both LH legs byte-identical to frozen refs (SHAs below); red-team
  non-N behavior identical except N1/N2/N3 deltas.
- K6: nonce-desync self-heal verified under keyed tags.
- K7: zero RNG (grep 0 hits); 3× byte-identical batteries.

### R2 (exhaustion)
- K1: 2000-revoke/4000-ledger-row and 600-withhold counts exact; zero drops.
- K2: 600 quarantine entries, zero phantoms.
- K3: conflict detection correct past index 128 (150, 199 probed).
- K4: 200 distinct withholds no false escalate; third round escalates ledgered.
- K5: LH legs byte-identical to frozen refs.
- K6: every chunk ≤ 2^25 (incl. revision chunks via extended accounting).
- K7: zero RNG.

### R3 (PROVTAG)
- K1: rehabilitated install ledgers PROVTAG EXT.
- K2: GEN-only claims remain GEN/withheld.
- K3: no GEN downgrade of EXT incumbent.
- K4: all ten laundering attacks WITHHOLD.
- K5: LH unchanged. K6: zero RNG.

### R4 (poison recovery)
- K1–K4: revision apply/refuse semantics hold; poison recoverable; dead evidence inert.
- K5: exact revision/refusal accounting; store append-only.
- K6: no-revision behavior byte-identical to frozen F4.
- K7: LH unchanged. K8: zero RNG, 3× determinism.
- No-limit: 100-revision uncapped probe passes; old 64 cap gone.

## Interaction results

- MX1 (M_REVISE through keyed N-AUTH): PASS — legitimate applies; forged-identity,
  wrong-key, and replay revisions refused at AUTH with no row/forward/nonce effects.
- MX2 (revision chunking): PASS — 100 rows exact, chunk-walk byte-accounted,
  read-back clean past old cap.
- MX3 (provenance after rehab): PASS — rehabilitated install PROVTAG=EXT;
  revised-away side inert.

## Battery evidence (3× each, byte-identical)

| Battery | SHA-256 | Frozen ref | Match |
|---|---|---|---|
| Smoke | `6855928854e38255e7275a18c5b07c82675fe1bc0752a616ba9ca90ba2e6d2e0` | same | ✓ |
| LH B-alone | `cc7e86ed4a00be36bb4f5a2aacc6456197281270b4eb40717ebb1ca017ea93e9` | same | ✓ |
| LH integrated | `356b7873bf07942c6b2283ed087911d3bfa724cea1ab707fb1ccaf14821cec3b` | same | ✓ |
| Red team | RT_FAILURES,0 (3×) | — | ✓ |

Gate source identity: three `sp_gate.zag` copies byte-identical
(SHA-256 `3bbe7984fe84b0d36ff354433f3608fbe5363ca2c072d579b94692abb1ffca77`).

## Procedural notes

- Prereg timing deviation documented in MERGED_PREREG.md §0 (substance
  preregistered; commit ordering violated by coordinator error; no bar altered
  on results).
- One test-authoring bug during MX1b (superseded line reused as evidence;
  mechanism correctly refused); fixed, 3× clean re-run.
- N-AUTH-failure ledgering on M_REVISE frozen per prereg §2.4.
