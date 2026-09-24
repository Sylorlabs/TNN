# SELF-PAM gate — build record

Pure-Zag implementation of the self-PAM composition (Hypothesis 6), built
under the frozen prereg `docs/lab/senses/pam-rebuild/selfpam/PREREG.md`
(commit `204b82831bbabd7dc2918f07d3a5ad75c9842e53`) and `TECH_BRIEF.md`
(`19cb91fd`), on branch `tnn-native-lab` (sylorlabs/TNN).

## Authority note

The prereg's header states that build artifacts require "a committed prereg
amendment after the pre-build blockers in §8 are cleared." This build was
directed explicitly by the parent orchestrator notwithstanding that clause;
the §8 blockers below still gate MEASUREMENT — per PREREG §5.5, "a
measurement run against unsigned thresholds does not count," and per §4 no
cell counts as run until its evidence is committed. Nothing here runs a
battery cell.

## Composition

| File | What it is |
|---|---|
| `admit_claim.zag` | Gate core: cf1's gate-step (`v2/cf1_zag/cf1.zag`, lines 324–413) as an in-process function. Keeps verbatim: perm/prov/chal/neg arenas, the 700 high-confidence bar, the `tol_of` table, the 9 dispositions and the install law (nothing installs on first appearance; permanence = provisional re-observed within tolerance; revision = high-conf challenger corroborated twice; pointwise adjudication banned — trial-1145 rule). |
| `codec.zag` | FACT-type claim codec. Frozen codebook v1: `{ FACT = 0 }`. Record fields: task, jcode, conf, meas, evhash (SHA-256 of the cited evidence bundle, cross-bound byte-for-byte; mismatch ⇒ fail closed). Wire format v1: `0\|<jcode>\|<conf>\|<meas>\|<64-hex>\n`. |
| `corr.zag` | The frozen C1-class corroborator: independent analytic re-measurement (SPAN-SUM / SPAN-MAX families) over evidence bytes it re-reads itself, bound to the registered channel by attestation (IE amendment R2). |
| `g1_candidate.zag` | R2-3 candidate gate id 2 (`selfpam-fact-gate`): the four registration functions + validity, wired to the composition. |
| `main_smoke.zag` | 11-step smoke driver (all 9 dispositions + fail-closed paths). |
| `main_g1probe.zag` | Compile/behavior probe for the G1 candidate. |
| `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag` | Verbatim substrates (copied from `v2/cf1_zag/`). |
| `build.py` / `verify.py` | Pinned-toolchain build; 16-check verifier (two-run cmp, expected disposition sequence, digest, G1 probe, no-RNG grep). |

Published API (zero RNG, deterministic given state):

- `sp_init() -> []u8` — fresh zeroed gate-state blob.
- `admit_claim(st, task, jcode, conf, meas, evhash) -> i32` — draft presentation (proposer channel). The prereg's five arguments follow the state handle in prereg order; znc edition 2026 has no mutable globals, so the handle is the leading argument.
- `admit_neg(st, task, jcode, meas) -> i32` — negative-evidence record.
- `corr_observe(st, task, jcode, conf, meas, ev, gatt) -> i32` — attested corroborator-channel record.

## Frozen tables (starting bids — PROVISIONAL, Micah's sign-off open per §8)

- `tol_of(FACT) = 8` — cf1's task-0 tolerance, kept verbatim per PREREG §3.1 ("keeps, verbatim: ... the per-task/per-type tolerance table"); task 0 = FACT per §3.3 codebook.
- High-confidence bar 700 (verbatim).
- C1 channel test key `SELF-PAM-C1-REG-CHANNEL-2026-09-23` (frozen test key; production replaces with a channel-key ceremony — the mechanism, gate-verifies/forger-cannot-sign, is what's frozen, per IE amendment R2). The amendment's own test key stays scoped to the V2 hardening battery.
- Corroborator confidence: `700 + (evlen % 300)` on non-empty evidence, 0 (declines) on empty. Deterministic; no RNG anywhere in decision paths.

## Composition deltas (frozen here, documented)

- **D1** (install bar, IE R2/R3 via the C1 channel): `PERMANENT_INSTALL` (3) and `REVISED_INSTALL` (7) additionally require the corroborating observation to arrive attested over the registered independent channel (`corr_observe` with valid gatt, conf ≥ 700). An unattested re-observation leaves the claim provisional (disp 1 / 8). First appearance never installs, on either channel.
- **D2** (evidence-hash binding, PREREG §3.3): provisional/challenger slots store the claim's evhash; promotion requires the attested bytes' SHA-256 to match the stored evhash byte-for-byte. Mismatch ⇒ WITHHELD (fail closed, margin unknown).

## Standing blockers (not cleared — noted, not attempted)

- **CC1 correlated-corroborator guard — DEPLOY BLOCKER (standing).** PREREG §3.5: "no install path deploys before the CC1 correlated-corroborator guard is verified in Zag (contradiction-matrix verdict: two correlated-wrong high-conf PASSes agreeing within tolerance defeat the rule — CC1 seqs 10983/10992 → REVISED_INSTALL false permanent). The guard's Zag verification is its own experiment." This build does not clear it and must not be cited as clearing it.
- §8 pre-build blockers still open: KB threshold sign-off (Micah), frozen probe charter, marked-emission format, corpus manifests. The FACT tolerance table above is built against the §8 starting bids only.

## Build / verify

```
cd docs/lab/senses/pam-rebuild/selfpam/src
python3 build.py    # pinned znc -> build/smoke_bin, build/g1probe_bin (not committed)
python3 verify.py   # 16 checks incl. two-run byte-identical cmp
```

Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
`@import` paths resolve relative to CWD — build from `src/`.
