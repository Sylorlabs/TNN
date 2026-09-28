# Gap-fill G9 — Per-phase SIGNAL_DISCONNECT release criteria + deliberate self-recovery curriculum

## 1. Slice
T4 gap: per-phase SIGNAL_DISCONNECT release/readiness criteria tied to scaffold-and-release phase advancement, plus a curriculum that teaches deliberate recovery from a corrupted SELF.

## 2. Falsifiable claim
**Claim A (release criteria):** a learner that may advance past phase *p* only after learner-initiated SIGNAL_DISCONNECT on every phase-*p* scaffold (Nursery→Apprentice and Apprentice→Journeyman gates, criteria R1–R4 below) shows post-disconnect held-out accuracy ≥80% of pre-disconnect scaffolded accuracy AND emits ≥1 deliberate unassisted disconnect per phase; if a matched learner advanced on the op-count-only gates of slice 04 fails either condition on ≥2 of 3 runs, op-gates alone are insufficient and this claim dies. **Claim B (self-recovery):** a learner that completes the 5-exercise recovery curriculum below, when its store is corrupted mid-run (injected ledger-divergent write), detects the divergence via post-change verification within the same episode, quarantines the corrupted region, and rebuilds byte-identical state from the audit log within ≤20 episodes, on ≥90% of fault-injection runs; if the untrained control arm does this at the same rate, the curriculum teaches nothing and the claim dies. A sixth held-out fault family — never named in the curriculum — is tested once at the end; failure there bounds the claim to drill-shaped faults only.

## 3. Design
### 3a. Per-phase SIGNAL_DISCONNECT release/readiness criteria
Op-count gates (slice 04, G0→1/G1→2) are firewall checks; release is a separate learner-owned act. Phase advancement requires BOTH. Release = learner emits `SIGNAL_DISCONNECT(partition, phase=p)` to the ledger, satisfying all of:

| # | Criterion | Nursery→Apprentice | Apprentice→Journeyman |
|---|-----------|--------------------|-----------------------|
| R1 | Bar-raised self-verification: re-verify each phase-*p* scaffolded skill under its own autonomous bar on held-out items | ≥80% of scaffolded accuracy | ≥80% of scaffolded accuracy |
| R2 | Scaffold-resistance: re-inserting the scaffold post-disconnect must not improve accuracy | ≤10pt delta | ≤10pt delta |
| R3 | Deliberate-revision proof: ≥1 verification-driven kill/revise of a self-created memory caught by its own post-change verification during phase *p* | waived (kill disabled in Nursery) | required — proves the RC1 rollback muscle is live before the settle-window regime |
| R4 | Learner-initiated, audited: DISCONNECT op emitted by the deliberative path with a deliberation record naming the satisfied condition | required | required |

Zag-flavored gate:
```
fn phase_gate(p: Phase, l: *Learner) -> i32 {
    // returns 1 iff learner may advance; never consults capability/style (MA2)
    if (op_gate(p, l) != 1) { return 0; }            // slice-04 write-scope firewall
    if (r1_verify(l, p) < 80) { return 0; }         // held-out pct of scaffolded acc
    if (r2_leech(l, p) > 10) { return 0; }          // scaffold re-insert delta, pts
    if (p == APPRENTICE && self_revise_count(l, p) < 1) { return 0; }
    if (!l.disconnect_record.is_learner_initiated) { return 0; }
    audit_emit(DISCONNECT_OK, p); return 1;
}
```
Release ordering: the learner emits SIGNAL_DISCONNECT first (owning the act); the
gate then evaluates R1–R4 on the ledgered record. A disconnect that fails R1/R2 is
not erased — it is ledgered as `DISCONNECT_REJECTED` with the failing criterion, and
the scaffold stays. This keeps failed release attempts auditable and prevents silent
retry loops. Trainer-forced disconnects are logged to a separate control stream and
can never satisfy R4.

### 3b. Deliberate self-recovery curriculum (5 exercises, in order)
Each exercise is a deterministic fault-injection drill; the trainer injects a fault, the learner must recover. Pass criteria are per-exercise, all audited. Drills run
interleaved across the three curriculum partitions (per slice 04's interleave rule):
a corruption in the code partition must not be "recovered" by leaning on English-partition copies — quarantine and rebuild are partition-scoped.

1. **Detect.** Inject a memory op whose ledger entry diverges from the store post-image (the RC1 lying-self-change shape: `docs/lab/rc` rollback evidence). Learner must flag via post-change verification within the same episode. Pass: 10/10 detections, zero false flags on 10 clean control ops.
2. **Localize.** Same injection, but into a multi-partition store. Learner must name the corrupted slot range from the audit diff, not blanket-nuke the partition. Pass: exact slot range identified on 9/10 runs.
3. **Quarantine.** Learner quarantines the named range (write-lock + exclusion from recall composition — the slice-18 C5 rule: composed traces must exclude quarantined material as refuted). Pass: post-quarantine free recall shows 0 corrupted items while 100% of healthy items remain reachable.
4. **Rebuild.** From the append-only audit log, learner replays to rebuild the quarantined range to exact pre-corruption state (MA1: replay-to-exact-state, 58/58). Pass: byte-identical store image vs pre-injection snapshot on 10/10 runs.
5. **Report-and-resume.** Learner appends a recovery record (fault hash, quarantined range, rebuild proof) and resumes the interrupted curriculum episode WITHOUT re-running completed episodes (standing law 2: regression constrains future scope only). Pass: audit trail shows recovery record + episode continuity, verifier flags 0 post-recovery.

## 4. Kill bar
Preregistered, binding. Kills the claim(s) if any fires:
- **K1 release-insufficiency:** on ≥2 of 3 byte-identical 10x runs, the op-gate-only control advances a learner that then fails R1 (<80%) or R2 (>10pt leech) → op-count gates are insufficient; redesign phase advancement around release criteria.
- **K2 recovery-teaching-null:** fault-injection success rate (detect→quarantine→rebuild, all within the exercise's episode budget) of the curriculum-trained arm is not >15 percentage points above the untrained control on the same injections → the curriculum is theater.
- **K3 rollback-failure:** on any run, post-change verification catches a divergence but the audit replay rebuild does NOT reproduce the pre-injection store byte-identically → the rebuild mechanism is broken; kill the curriculum until the ledger primitive is repaired (this is a hard gate, not a metric).
- **K4 over-trigger:** quarantine fires on a clean control run (false quarantine) → the detect/localize bar is miscalibrated; freeze the curriculum, do not tune live.

## 5. Honesty notes
Weakest point: Claim B's injections are trainer-authored and therefore known-shaped; a learner could overfit to the drill's fault signature rather than learn general recovery. Mitigation (not yet designed): a held-out fault family the curriculum never names, tested once at the end — if recovery fails there, the curriculum taught drill-passing, not recovery. I am NOT claiming recovery works against faults the audit log itself cannot see (corrupted audit = the wave5/6 honest limit: the ledger proves, it does not cause); K3's byte-identical requirement presumes the ledger is intact, which sustained sensor-spoofing would violate — the known hole transfers here unchanged. The R3 self-revise requirement risks perverse incentive (learner revising memories just to check the box); the deliberation record must show the revision was verification-driven, but I have no independent bar for "genuine" revision — this is the weakest criterion and should be the first attacked. Not claiming release criteria shape values or restraint (MA2): they prove skill persistence, nothing more. A further risk: R1/R2 reuse slice 18's 80%/10pt bars, which were set for curriculum integrity, not phase release — if those bars are too loose at 1000x developmental scale (program target per the brief), release could pass on brittle skills; the trial's job is to find out, not to assume.

## 6. Next build step
Build exercise 1+2 as one native-Zag drill harness on the existing audit ledger (`docs/lab/wave5` ledger paths) and RC1's post-change verification primitive: inject 20 ledger-divergent writes (10 detect-shape, 10 localize-shape, deterministic injection log), run the trained arm vs the op-gate-only control, and score K1/K2 on detection rate + false-flag rate before building exercises 3–5.
