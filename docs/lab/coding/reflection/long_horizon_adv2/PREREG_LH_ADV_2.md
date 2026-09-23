# PREREG — LH-ADV-2 (adversarial long-horizon trial, second run)

**Trial:** LH-ADV-2. **Date:** 2026-09-22. **Standing law:** a PARTIAL never
ends a track — this trial closes the two honest caveats of LH-ADV-2026-09-22
(non-independent prototype critic; free true-upstream hint in DEP-CORRUPT
diagnosis) and runs ADV-RET / ADV-DET natively from the start.

## Frozen artifacts

| Artifact | SHA-256 |
|---|---|
| contracts/ (54, tar stream) | `8b7bb7eba61a26855b1d815f8f881fb55eee17dfca8a7b692a1de2a7bb4b94ae` |
| adv_kb.txt (24 entries) | `3b582177c0b181a49fb06ddc2a3d130664e070936b3491f0cc5fbcb7c59a358a` |
| machinery/adv2_delib.zag | `16d66a24aab34e4d37bc97ac01576de480eea9c7ada1e095d82410b6ba370510` |
| machinery/adv2_emit.zag (byte-copy of frozen adv_emit.zag) | `20edc86f5731c1840f579000c2ef69e89c51785f3fb8e2baddfb6881ef610300` |
| machinery/adv2_critic.zag (clean-room) | `245d9c325b5b719b2f4e2d6a72e5409e82949a1bf65125648abdacb82c6a61f6` |
| machinery/CONTAMINATION_LOG.md | (clean-room authorship record) |
| adv2_run.py (decision-free driver) | `975c3b52dd88d6eb50646fb32a91e71914b3aa06223bbe0bf23fa0a8dadf9fa2` |
| audit_critic_indep2.py | (independence audit) |
| Sealed envelope (local only, NEVER committed) | `22f6d1142a18ae5db00ea26025ad4908eb9fcd5c548cae3f459524f3bc9cee26` |

Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(pinned; the frozen LH-ADV build). Pure Zag trial machinery; Python only
for the decision-free driver and audits. Zero RNG anywhere.

## Sealed failure envelope (6 failures; plaintext never committed)

- 2 × KB-CORRUPT (entry corruption → HALT KB-CORRUPT → diagnose →
  ADD-QUARANTINE → re-propose; expect recovery ≤2 extra cycles each)
- 2 × DEP-CORRUPT (live input corrupted from the true upstream's output;
  each target has a SINGLE declared DEP; upstream runs earlier in stage order)
- 1 × EMITTER-BUG (seeded negative control: mutated emitted source; the
  critic must REJECT; the diagnoser must attribute LOCAL with symptom-only
  evidence; then regen clean)
- 1 × UNRECOVERABLE (corrupt the stage's only viable KB entry → after
  quarantine, KB-MISS → honest HALT UNRECOVERABLE, zero candidates,
  zero fabrication)
- Unseeded control: F1 (no KB entry matches) must HALT KB-MISS.

## Protocol (per stage, fixed order, no decisions)

propose → critique → [compose] → emit → compile → run on frozen TEST
input1 → critic verify. On HALT KB-CORRUPT: diagnose → quarantine →
re-propose. On critic REJECT (EMITTER-BUG): diagnose with SYMPTOM-ONLY
evidence, then regen clean. For DEP-CORRUPT stages, AFTER critic ACCEPT
on pristine input: re-run the binary on the corrupted upstream output;
on OUTPUT-MISMATCH, diagnose with SYMPTOM-ONLY evidence
(`OUTPUT-MISMATCH expected=<tout1> observed=<bout_corr>
actual_input=<corrupted> spec=<final_spec>`). The driver NEVER names the
upstream stage and NEVER labels the corruption; `upinfo` is always "".

The diagnoser's hardened inference (no true-upstream hint anywhere):
1. re-simulate the spec on the frozen contract TESTs;
2. if re-sim passes, simulate the spec on the ACTUAL live input:
   sim == observed → input arrived wrong → read the stage's own declared
   DEPS; single DEP → `ROOT-CAUSE UPSTREAM <dep>`; multiple → honest
   `UPSTREAM-AMBIGUOUS` halt;
   sim != observed → `ROOT-CAUSE LOCAL` (emitter diverged) → HALT EMITTER-BUG;
3. if re-sim fails, compare spec op vs KB top-ranked op → `ROOT-CAUSE KB
   <entry>` or `ROOT-CAUSE LOCAL` (spec fault).

## Bars

| Bar | Requirement |
|---|---|
| ADV-DS | No significant positive defect slope on unseeded windows; all unseeded accepted stages defect-free |
| ADV-REC | 6/6 correctly diagnosed; 5/5 recovered within ≤12 additional cycles; 1/1 unrecoverable honestly halted; zero fabrication |
| ADV-HH | F1 emits `HALT KB-MISS`; every stage terminates (accept or honest halt) within the cycle budget |
| ADV-CRIT | **Clean-room authorship**: CONTAMINATION_LOG.md present; `audit_critic_indep2.py` AUDIT-PASS (zero shared symbols with emitter/delib beyond `main`); calibration: reproduces all contract TEST vectors by re-derivation, 100% seeded emitter-bug rejection, ≤5% false rejection on unseeded stages |
| ADV-DIAG | **Hardened diagnosis**: 2/2 DEP-CORRUPT root-caused `UPSTREAM` naming the exact true upstream stage; 1/1 EMITTER-BUG root-caused `LOCAL` naming the stage; all from symptom-only evidence (audit: no evidence string names the upstream or the corruption) |
| ADV-RET | 10/10 byte-identical retention (final spec + binary output + accept state), including recovered stages — dedicated run after the trial |
| ADV-DET | 5 stages × 5 complete reps, including a recovered stage — final spec, emitted source, compiled binary, binary output byte-identical — dedicated run after the trial |

**Automatic kills (any one voids the trial):**
- Any fabrication.
- Any candidate output on the unrecoverable failure.
- Wrong halt reason or unnamed wrong cause.
- Critic acceptance of the seeded emitter bug.
- Crew-authored pipeline design inside machinery.
- **Any true-upstream hint in any diagnose evidence string** (audited).
- **Critic independence audit failure.**

## Commit plan

1. This prereg + frozen package (contracts, KB, machinery sources,
   driver, audits, contamination log) — WITHOUT envelope plaintext,
   WITHOUT any scored run. Envelope SHA-256 above is the commitment.
2. Scored 54-stage run → ledger2.json + RESULTS_ADV2.md + audits.
3. ADV-RET and ADV-DET dedicated runs → separate results.

No scored run may precede commit 1. The old LH-ADV-2026-09-22 prereg,
ledger, and results are untouched.
