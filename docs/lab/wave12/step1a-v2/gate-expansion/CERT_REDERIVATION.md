# CERT RE-DERIVATION — arena certifier vs the 2026-09-20 gate evidence

> **FROZEN — 2026-09-25** under `PREREG_GATE_EXPANSION.md` WI-3.
> Independent track: needed regardless of which gate method wins.
> NOTHING HERE ADOPTS ANYTHING — adoption needs Micah's dated signature.

## 1. Background (established, not re-litigated)

- The i32-cast audit (`~/workspace/i32-investigation/CAST_AUDIT.md`,
  blast-radius rank 2) proved the historical thin certifier
  (`wave12/step1a-v2/thin-certifier/certifier/thincert.zag`, frozen
  source sha `9b55fa2f…`, binary `d5e4de74…`) reads garbage for manifest
  entries 0–2 and crashes on manifests ≥~70 entries (ZNC-2026-09-21-007).
  Its 2026-09-20 gate evidence (clean representative build PASS +
  dirty-plant attestations) therefore needs re-derivation from the
  arena-rebuilt certifier. A byte-identical rerun of the OLD binary is
  NOT sufficient (proves determinism, not correctness).
- The CERTIFIER-REBUILD crew (2026-09-21, prereg `26b86329`) already
  rebuilt `thincert_rb.zag` / `rngscan_v3_rb.zag` (arena-only tables),
  and re-ran old-vs-new over 35 historical certifications: 35
  CONFIRMED, 0 flips, 0 void (`redteam/certifier-rebuild/results.tsv`).
  The armc gate cases (t2_dirty1/2/3/5, t3_rerun, t3_k3) are in that set.
- One gap: t1_plant07 INCONCLUSIVE (no stored attestation; not scored).

## 2. Task (what "complete" means)

1. **Rebuild independently:** build `redteam/certifier-rebuild/thincert_rb.zag`
   with the pinned toolchain (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`),
   TWICE; the two binaries must be byte-identical (toolchain
   determinism). Record SHAs.
2. **Cross-check against the CERT crew's binary:** locate the CERT
   crew's built arena binary (under `redteam/certifier-rebuild/` or its
   committed evidence). If present, compare SHA with the fresh build —
   expect identical (same source + same toolchain). If absent, the fresh
   2/2-identical build stands as the reference; record that.
3. **Re-run the 2026-09-20 gate evidence set** through the fresh arena
   binary:
   - Inputs: `wave12/step1a-v2/armc-rerun-2026-09-21/thincert/{evidence,plants,k3}/`
     (rerun_attestation, k3_rerun, dirty1/2/3/5 plants) and
     `wave12/step1a-v2/thin-certifier/plants/` + k2prime red-team inputs
     per `redteam/certifier-rebuild/rerun_all.sh` (reuse the harness;
     do not modify it — copy to the evidence dir if output paths need
     changing).
   - Compare verdict AND full attestation bytes vs the stored records
     (`results.tsv` + the committed attestations). Expect: every case
     CONFIRMED (old==stored==new, byte-identical).
4. **Close or document the t1_plant07 gap:** if the plant07 input can be
   reconstructed from the k2prime red-team records, run it through the
   arena binary and record the verdict; if not reconstructible, record
   INCONCLUSIVE with the reason (missing input, not a pass).
5. **Write the completion record**
   `wave12/step1a-v2/gate-expansion/evidence/cert-rederivation/RE_DERIVATION_CERT_2026-09-25.md`:
   build SHAs, per-case old/new/stored table, plant07 disposition, and
   the citable statement: "the 2026-09-20 thin-certifier gate evidence
   re-derives cleanly under the arena-rebuilt certifier (zero verdict
   flips, zero voided certifications)."

## 3. Kill bars for this track

- K-BUILD: 2/2 byte-identical arena builds, else STOP (toolchain issue).
- K-FLIP: any gate-evidence case where new ≠ stored verdict → STOP and
  report (this would void a historical certification — it is not
  expected per the CERT crew's 35/35, but this is an independent check).
- K-HONEST: the completion record states exactly what was re-run and
  what was not; no extrapolation beyond the evidence set.

## 4. Out of scope

- Adopting the arena binary as the pinned certifier (needs Micah).
- Rebuilding rngscan_v2 (retired tripwire; informational only).
- The unsigned gate amendment itself (unchanged by this track).
