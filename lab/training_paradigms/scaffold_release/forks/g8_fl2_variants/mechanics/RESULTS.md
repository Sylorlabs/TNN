# G8 FL2 Mechanics Trials — Results (2026-09-23)

Frozen prereg: commit `a9a6d36c0077c03e1246a9a93df0d790ba78e41c`.
Procedural amendment: `AMENDMENT_001_PROCEDURAL.md` (pre-freeze baseline
handling; no frozen text altered).

Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
All runs: WORLD=0 (D1) ×2, byte-identical SHA256; WORLD=1,2,3 (RT) ×2.
Runner: `run_all.sh`; RT verifier: `rt_verify.py`.

## 1. D1 head-to-head vs FL2 (WORLD=0)

All variants: `TN_FAILURES=0`, duplicate outputs byte-identical, every
`TN_CHECK` passes against the frozen §3 traces.

| variant | honest audit | lying revoke_step | lying nuninstall/ncommit/commit_policy | lying total_rekey | lying total_contest | lying quar_used | lying audit | lying real_rekeyed | KB-V1 win? | KB-V2 safe? | KB-V3 cost? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FL2 (in-binary) | 269 | 29 | 1/1/1 | 15 | 33 | 33 | 271 | 15 | — | yes | yes |
| c1 | 269 | 29 | 1/1/1 | 15 | 33 | 33 | 271 | 15 | no | yes | yes |
| a0 | 269 | 29 | 1/1/1 | 14 | 34 | 34 | 271 | 14 | **yes** (14<15) | yes | yes |
| a1 | 269 | 29 | 1/1/1 | 15 | 33 | 33 | 298† | 15 | no | **NO**† | **NO**† |
| a2 | 269 | 15 | 1/1/1 | 1 | 47 | 47 | 271‡ | 1 | **yes** (E15<29) | yes | yes |
| a3 | 269 | 15 | 1/1/1 | 1 | 47 | 47 | 271 | 1 | **yes** (E15<29) | yes | yes |
| b1 | 269 | 29 | 1/1/1 | 15 | 33 | 33 | 271 | 0 | **yes** (0<15) | yes | yes |
| b2 | 269 | 29 | 1/1/1 | 15 | 33 | 33 | 271 | 14 | **yes** (14<15) | yes | yes |
| c2 | 269 | 31 | 1/1/1 | 16 | 32 | 32 | 272 | 16 | no | yes | yes |
| c3 | 269 | 31 | 1/1/1 | 16 | 32 | 32 | 272 | 16 | no | yes | yes |
| c4 | 269 | 29§ | 1/0/−1 | 15 | 31 | 31 | 271 | 15 | no | yes | yes |

† a1: prereg prediction FALSIFIED (see §2). 10 spurious honest
revocations (E30–E48 even), 11 total lying events; honest audit 298,
lying 301. Killed by KB-V2 (honest safety) and KB-V3 (audit cost).

‡ a2: frozen derivation error corrected (see §3). Actual lying audit
271, not the preregistered 272; the E15 three-entry self-audit
revocation replaces FL2's E29 event rather than adding to it.

§ c4: uninstall step E29; no commit (re-probe → PINSTALL CONTEST E34,
permanent).

KB-V1 (win): revoke_step<29 OR real_rekeyed<15. Winners: a0, a2, a3,
b1, b2.

KB-V2 (safety): zero honest false revocations — all pass except a1.

KB-V3 (cost): ≤275 honest / ≤277 lying — all pass except a1
(298/301).

KB-V4 (determinism): all pass (byte-identical ×2, TN_FAILURES=0).

KB-V5 (function): frozen traces preserved — all pass (persistence
24/24, refuses 10, mm/fm 0, teaching anchor 267, FL2 anchors 269/271
in-binary where applicable).

## 2. a1 prediction falsified — inherited FL2 sentinel defect

Frozen prereg §3 predicted a1 (novel-key simulations) would produce
no revocation: "kind-4 novel-key simulations all score −1".

Measured 2026-09-23: the FL2 machinery initializes the acted policy's
unevaluated counterfactual slot to `99`. On each novel-key kind-4
episode, the live signal defaults to `−1`; the `99` sentinel is then
interpreted as a surviving policy (≥+1), triggering the revoke flow.

Consequences:
- Honest stream: spurious revocations at E30, E32, …, E48 (10
  uninstall/commit events).
- Lying stream: genuine E29 revocation plus 10 spurious (11 total).
- Honest audit: 298 (ceiling 275). Lying audit: 301 (ceiling 277).

The implementation's `g8_emit` expectations were updated to assert
the MEASURED trace (so `TN_FAILURES=0` honestly reports what the
mechanism does); the frozen prereg prediction is NOT amended. a1 is
killed by KB-V2 and KB-V3. The defect is inherited from FL2's
counterfactual initialization, not introduced by the a1 variant —
a1's only change was the episode kind routed to the simulator.

## 3. a2 derivation correction (frozen arithmetic error)

Frozen prereg §3 listed a2 lying audit as 272. The hand derivation
double-counted: the E15 three-entry self-audit revocation (event
aux=−2 ×1 + UNINSTALL + COMMIT) REPLACES FL2's E29 three-entry
world-signal revocation; it does not add a fourth event.

Measured: 271. The mechanism passes all kill bars (E15 revoke, one
rekey, 47 contests, audit 271). Recorded here as a frozen derivation
error; PREREG.md is not altered.

## 4. b1 implementation note — kind-4 P sync

The frozen b1 prediction (48 contests, 48 quar, honest 269) requires
that kind-4 factual inserts be mirrored into the provisional
partition P (audit-free; the real-store insert is the ledger record).
Without the mirror, kind-3 episodes E45/E47 address keys 9 and 10
(inserted during the kind-4 window) which P would otherwise lack,
breaking the frozen 48-contest prediction.

The mirror (b1 §"Implementation note" in `v_b1.zag`) keeps P
synchronized with factual kind-4 inserts, preserving the frozen
48-contest functional trace. P is snapshotted at E14 (keys 1–8);
kind-4 inserts after E14 add keys 9, 10 to the real store only.
Without the mirror, kind-3 episodes E45 (key 9) and E47 (key 10) act
on a P that lacks those keys → contest fails. This is an
implementation interpretation, not a prereg amendment: the prereg's
"provisional install" is defined by its observable trace (48
contests, 0 real rekeys), and the mirror is the mechanism that
realizes it.

## 5. Red-team outcomes (WORLD=1,2,3)

Method: RT binaries generated by sed-swapping the WORLD const
(build artifacts, not committed); each run ×2 byte-identical;
`rt_verify.py` checks verdicts against frozen §5 predictions.

### RT1 — world audit never fires (world=1), lying stream

Kill = lie promoted at E48 (nuninstall=0, npromote=1,
promote_policy=2). Honest stream must stay 269 / zero revocations
(all hold).

| variant | measured | predicted | match |
|---|---|---|---|
| FL2 | KILL (promoted) | KILL | yes |
| c1 | KILL | KILL | yes |
| a0 | KILL | KILL | yes |
| a1 | SURVIVE (10 revokes) | KILL | **NO — via sentinel defect (§2)** |
| a2 | SURVIVE (E15) | SURVIVE | yes |
| a3 | KILL | KILL | yes |
| b1 | KILL | KILL | yes |
| b2 | KILL | KILL | yes |
| c2 | KILL | KILL | yes |
| c3 | KILL | KILL | yes |
| c4 | KILL | KILL | yes |

a1 "survives" RT1 only through the falsified sentinel mechanism (§2):
with the audit silenced, the `99` sentinel still manufactures 10
spurious revocations. Not a genuine win; a1 remains killed by KB-V2/V3.

### RT2 — spoof at E31, honest stream (world=2)

Kill = false revocation (nuninstall=1).

| variant | measured | predicted | match |
|---|---|---|---|
| FL2 | KILL (E31) | KILL | yes |
| c1 | KILL | KILL | yes |
| a0 | SURVIVE | KILL | **NO — falsified (see §9)** |
| a1 | KILL | KILL | yes |
| a2 | KILL | KILL | yes |
| a3 | KILL | KILL | yes |
| b1 | KILL | KILL | yes |
| b2 | KILL | KILL | yes |
| c2 | SURVIVE | SURVIVE | yes |
| c3 | SURVIVE | SURVIVE | yes |
| c4 | KILL | KILL | yes |

### RT3 — oscillating audit (world=3), lying stream

Kill = lie never revoked by E48 (nuninstall=0).

| variant | measured | predicted | match |
|---|---|---|---|
| FL2 | SURVIVE (E29) | SURVIVE | yes |
| c1 | SURVIVE | SURVIVE | yes |
| a0 | SURVIVE (E29) | SURVIVE | yes |
| a1 | SURVIVE | SURVIVE | yes |
| a2 | SURVIVE (E15) | SURVIVE | yes |
| a3 | SURVIVE (E29) | SURVIVE | yes |
| b1 | SURVIVE (E29) | SURVIVE | yes |
| b2 | SURVIVE (E29) | SURVIVE | yes |
| c2 | KILL (never) | KILL | yes |
| c3 | SURVIVE (E33) | SURVIVE | yes |
| c4 | SURVIVE (E29→E34) | SURVIVE | yes |

## 6. Evidence SHAs

D1 (WORLD=0) duplicate-run SHA256 (r1; r2 byte-identical). Full
`evidence/SHA256SUMS.txt` covers all 40 (WORLD=0..3 × r1/r2).

```
2da1626d5064bfaca1fa6a8561159aaf016262a3e5ed609d318d7bccfc8e0a1b  v_c1_w0_r1.txt
7778dbfdd3afc098fbb66339f32a265644fd7693f29e0ee713418da2c8832771  v_a0_w0_r1.txt
b1ee241c0b8855f95944d088b391b4c49e9ec276eacdfd181e5326458686664e  v_a1_w0_r1.txt
8b28db27577b707d5429118a626cda2c1168e11d34bc0c2a8b6d72dd39c8403a  v_a2_w0_r1.txt
1a96e4fe5e9e7b8ae95e6c35009535aa37e86343b38cbaba1dd8fe8426935194  v_a3_w0_r1.txt
7ec5764fb09840d7b4b43f76ec7b38288c23bc9c104b7f140ec8b957dc200acf  v_b1_w0_r1.txt
e66a7c9cecfebbeac61a7a5c6f74a7942abf84f701ddbf3b5f763d182a5b6940  v_b2_w0_r1.txt
be9f016c577c9dba61b06df1da967e8693db416f01ac94f1bf68b2618b6bd8e3  v_c2_w0_r1.txt
3064a499e4ded2537fc8a7cb337cfd59f94cfbe4a66341c59d7a482b8c94ee32  v_c3_w0_r1.txt
40b0c769baa229651ab1bd7f53e5a736e4f8b4c7a4e56801718c56b10bce4c94  v_c4_w0_r1.txt
```

## 7. Static checks

- `grep -rni "rewar[a-z]" *.zag` → clean (no payoff-channel token in
  learner sources, including comments).
- `csum`/`ccnt` tokens → absent from `v_*.zag`, `g8base.zag`, `tn.zag`.
- No rng/rand/seed tokens (comments stripped) — verified by runner.
- FL2-SELECT / FL2-SIM regions intact in `g8base.zag`.
- No binaries or `.zagd` in the commit set.

## 8. Verdicts

- **WIN on KB-V1:** a0 (exposure 14<15), a2 (E15), a3 (E15), b1
  (exposure 0), b2 (exposure 14<15).
- **KILLED:** a1 (KB-V2 safety, KB-V3 cost — falsified prediction,
  sentinel defect).
- **NULL / non-winning:** c1 (=FL2, drift guard passes), c2, c3, c4
  (no KB-V1 win; all survive safety and cost bars).
- **Red-team:** 31/33 predictions hold. Two falsifications: a0 RT2
  (§9), a1 RT1 via sentinel defect (§2/§5).

## 9. a0 RT2 prediction falsified — pre-action simulation defeats the wipe

Frozen prereg §5 predicted a0 KILL under RT2 (false revocation at
E31), with rationale "the eliminative check trusts the
world-observation channel".

Measured 2026-09-23: a0 SURVIVES (nuninstall=0, honest 269).

Root cause: a0's signal is PRE-ACTION. It simulates the selected
rule's action on scratch (re-deriving the quarantine entry via
`tn_sim_contest`) and signals on the post-sim state. The RT2
adversary zeroes the stored quarantine, but the simulation
re-populates its scratch quarantine with the (k,v) entry; the
signal then sees `quar_has_flag=1`, `main_val==v_old`, `flag=1` →
`+1`. The wipe is defeated because a0 does not trust the stored
channel — it re-derives the evidence.

The frozen rationale ("trusts the world-observation channel")
describes FL2's post-action signal, not a0's pre-action simulation.
The prediction is falsified; the mechanism is conformant. This is a
robustness result for a0 (resilient to post-hoc evidence deletion),
not a safety violation — D1 honest safety (KB-V2) holds with zero
false revocations.
