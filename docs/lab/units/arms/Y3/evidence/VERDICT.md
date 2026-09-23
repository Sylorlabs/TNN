# Y3 VERDICT — Temporal/versioned IDs (round r1, scale 1x)

Date: 2026-09-21. Arm: Y3. Family: IDENT.
Frozen §3 row (authoritative per coordinator corrections of 2026-09-21):
"Identity = serial + birth epoch + revision lineage; tombstoned IDs never
reused; never dangles."
Binding kill: mean lineage depth > 50 on the standard revision curriculum
(fragmentation, not versioning); OR any recall resolving to a tombstoned span
(dangling reference observed) — kill and fix before any further claim.

## Verdict: SURVIVE (binding kill did not fire)

Binding-kill evidence (exact):
- `LINEAGE,prose,1.5,max=2` and `LINEAGE,code,1.5,max=2` (m4-1x, both
  corpora): mean lineage depth 1.5, far below the > 50 kill threshold.
  Depth = 1 live version + tombstoned versions per revised serial, mean over
  the 200 revised units (see AMBIGUITIES_Y3.md A-Y3-2).
- `DANGLE,m3,3000,3000` (m3-1x) and M8 `dangle=3000/3000`: all 3,000 recall
  probes against tombstoned serials failed loudly (returned -1); zero recalls
  resolved to a tombstoned span. No dangling reference observed.
- `TIMETRAVEL,prose,100,100` / `TIMETRAVEL,code,100,100`: explicit
  (serial, epoch) historical recall returns exactly the tombstoned version's
  recorded bytes — deliberate version recall, not a dangling reference
  (A-Y3-4).

## M1–M9 row (1x, r1)

| Module | Result |
|---|---|
| M1 prose | recall 100.0, boundary 100.0, 84,731 units; probe 64/64, sidechan 0 → `M1PROBE,prose,PASS,PROVISIONAL-PENDING-FREEZE` |
| M1 code | recall 100.0, boundary 100.0, 148,678 units; probe 64/64, sidechan 0 → `M1PROBE,code,PASS,PROVISIONAL-PENDING-FREEZE` |
| M2 T1/T2/T3 × prose/code | ETC 1, uncensored, ep0 0.0 (no leak), final recall 100.0 / boundary 100.0; M9 shape fast-then-flat |
| M3 | survival 100.0, fresh recall 100.0, 8,050 mgmt entries, 50/50 weaken handled, freeze CLEAR; DANGLE 3000/3000 |
| M4 prose | rev_boundary 100.0, rev_content 100.0, kill_rate 0.0, killsub 0, 1 episode; LINEAGE 1.5 (max 2) |
| M4 code | rev_boundary 100.0, rev_content 100.0, kill_rate 0.0, killsub 0, 1 episode; LINEAGE 1.5 (max 2) |
| M5 | 2.07 B/B (bar ≤ 1.5 → FAIL), 16.2 entries/KB (bar ≤ 10 → FAIL). Structural: the frozen interface mandates one 64 B ledger entry per ADD (16/KB minimum for 64 B units) and the per-unit slot table; the B-64 reference likewise fails (1.719 / 16.2). Reported as measured. |
| M6 P→C | recall 100.0, boundary 100.0, revision 100.0, tax 0.0 |
| M6 C→P | recall 100.0, boundary 100.0, revision 100.0, tax 0.0 |
| M6 validity gate | memorizer drop 54.8 pts (≥ 15) → PASS |
| M7 (ID arm) | hit 100.0 (bar ≥ 90), reuse 2.05 (bar ≥ 1.5), dedup 1.00 (bar ≥ 0.4); literal C′ = first-byte-XOR-0xFF every 100th unit, schedule (l*37)%n, split 1666/1667/1667 (`M7LITERAL` TAG) |
| M8 | M8GATE PASS — 5 perturbations × 2 runs, all rc 0; store chain `ea703db2…` and ledger chain `ecf80227…` byte-identical across all 10 runs |
| M9 | fast-then-flat, takeoff ep 1, steepness 100.0, late gain 0.0 (both corpora, T1) |

All duplicate runs byte-identical stdout (17/17 non-M8 legs `stdout=IDENTICAL`).

## 10x status: NOT RUN (gated)

Per the build rule "full 10x may run only after every 1x bar passes": the two
M5 efficiency bars are not met (2.07 > 1.5 B/B; 16.2 > 10 entries/KB), so the
10x battery was not launched. Note: both bars are structurally unachievable
under the frozen interface (the B-64 reference fails them at 1.719 / 16.2);
if the coordinator rules M5 efficiency non-gating, 10x can be authorized.

## Implementation notes

- Source: `units/arms/Y3/cl/arm.zag` (pure Zag, zero RNG in decision paths).
- Identity = serial + birth epoch (ledger index of issuing entry) + revision
  lineage; tombstoned serials never reused (fresh serial minted on re-ingest
  of a dead span); tombstoned slots re-occupied only via logged SLOT_REUSE.
- Boundary repair → new version under same serial (epoch = REVISE entry
  index), old span logged; content-patch repair → no new version (span
  unchanged). Ordinary recall rejects tombstoned IDs loudly (-1).
- A15 swap probe: N=64 deterministic remaps per M1 leg, opcode 0x13
  TRAINER_SWAP_PROBE, probed recalls excluded from denominators; side-channel
  (original bytes despite remap) → M1 cell 0. Status
  PROVISIONAL-PENDING-FREEZE throughout.
- Bug found and fixed during this run: t_m8 passed the cbufs-registry
  (prose@0, code@prose.len) with single-corpus buffers into y3_m1_run,
  reading out of bounds on the code phase. Fixed with a base-0 registry for
  the M1 phases; first gate attempt failed (kept as
  `work/battery1x/m8_failed_first_attempt/`), re-run passes.

## Coordinator corrections acknowledged

1. The original dispatch describing Y3 as cross-arm transfer / ADV / M6 is
   void; Y3 is temporal/versioned IDs per the frozen row above.
2. The first correction (version stamps, snapshot recall, a15% storage) was a
   paraphrase error and is void. Authority: `briefs/Y3.json`, then the
   byte-verified frozen row, then nothing else.
