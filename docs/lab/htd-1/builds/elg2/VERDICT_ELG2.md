# E-LG2 verdict sheet — checkpoint + delta durable ledger encoding

Crew: E-LG2 (respawned 2026-09-21 ~00:45 PDT; previous crew's work verified, not rebuilt).
Spec: `~/workspace/htd-1/specs/builds/elg2.md` (frozen prereg §3d + §7).
Workdir: `~/workspace/htd-1/builds/elg2/`. Toolchain: znc_linux_x86_64_abed8aa1.
Workload: D-P1 (600) + D-P2 (599; dp2-0319 excluded: 72658B > frozen 64KB parse
cap — documented in items_full.txt) = 1199 episodes, 43,157 ledger entries,
2,762,048 raw ledger bytes. R=5 reruns per config; one extra rerun by the
respawned crew (R=6 effective).

## REPLAY — PASS for all three K values

Replay verifier (`replay.zag`): independently re-decodes the LG2 section and
byte-compares the FULL reconstructed ledger (2,762,048 bytes, not spot checks)
against the unencoded FULL-DELIB ledger; re-verifies the FNV-1a chain over the
reconstruction; checks per-item outcome agreement.

| K | result | diff_at | chain | outcomes | enc bytes | base bytes | recon SHA == ref SHA |
|---|--------|---------|-------|----------|-----------|------------|----------------------|
| 16 | BYTE_IDENTICAL | -1 | OK | 1199/1199 | 802,480 | 2,762,048 | 41eceee2…cd65bbce == 41eceee2…cd65bbce |
| 64 | BYTE_IDENTICAL | -1 | OK | 1199/1199 | 704,700 | 2,762,048 | match |
| 256 | BYTE_IDENTICAL | -1 | OK | 1199/1199 | 680,148 | 2,762,048 | match |

Independent Python re-parse of the LG2 section framing (separate
implementation) confirms: section parses end-to-end with zero trailing bytes,
record counts match (snaps 75/19/5, deltas 1124/1180/1194, 1199 episodes,
43,157 entries), snapshot-raw byte counts match the Zag verifier exactly
(172,288 / 43,264 / 11,008). Per-item outcome records are byte-identical to
the baseline artifact (not just winner fields). Deliberation W counters
identical to baseline (expand 21576, gather 5995, verify 5995) — the
deliberation pipeline is provably unchanged.

## SAVINGS

| K | ledger bytes / baseline | bar: >50% at K=64 | snapshot share (snap_raw/enc) | bar: >20% | verdict |
|---|------------------------|-------------------|-------------------------------|-----------|---------|
| 16 | 29.05% | n/a | **21.47%** | **FAIL** | **FAIL** |
| 64 | **25.51%** | PASS | 6.14% | PASS | **PASS** |
| 256 | 24.62% | n/a | 1.62% | PASS | **PASS** |

- K=16 FAILS the snapshot-share bar: 172,288/802,480 = 21.47% > 20%.
  Checkpoint overhead is too heavy at K=16. FAIL is documented; one re-entry
  allowed per §7.
- Snapshot share denominator = the arm's own encoded ledger bytes (the natural
  reading of "share"; baseline-anchored reading would give 6.24% for K=16 —
  flagged for the referee, but the natural reading governs the verdict above).

## Determinism gate — HOLDS

R=5 reruns byte-identical (SHA-256) for all four configs (k16/k64/k256/fd_full).
Respawned crew recompiled `elg2.zag` from source: rebuilt binary is
byte-identical to the previous crew's `elg2_bin` (deterministic build), and a
fresh rerun from source + `state_pristine.bin` + `items_full.txt` reproduces
`runs/k64/set_1_run_0.bin` byte-exactly (SHA 37fca0aa…0665dc).

Artifact SHAs (run_0, all 5 reruns identical):
- k16:   572ef94d318cbdc6c7b2b76868382d32d9ca8167d5be3c9ad8223e2387da38af
- k64:   37fca0aacb532d9857f37072773ed7f19dd50345c2516cec971b8488ed0665dc
- k256:  aa1e16e78bab05f736c5495d7a227470f9945189e4dc49df129be03d42fc55f2
- fd_full (replay baseline): 7ec2a5997585dbda96ca12a36f6a4fae6ac09995f210e74b0ec8b9b69cdb509b

## Honest caveats (not pilot bars, but load-bearing for advancement)

1. **Full-cost accounting (KB-HTD-1.5) is negative.** Derived 11-class mapping
   (crew's page-granular OP-04/05 → words ×1024; OP-06 = actual section bytes;
   OP-09 = XOR words; identical in-memory staging 16 words/entry added to both
   sides): C_fd ≈ 1,646,721.56 vs C_k64 ≈ 1,745,120.20 → saving s = −6.0%.
   The ledger-byte saving (~41k units) is outweighed by encode overhead
   (serialization reads ≈ +106k in C_mem, XOR words ≈ +34k in C_verify).
   The mechanism wins its home metric (ledger bytes) but would NOT clear the
   §6 advancement bar (s ≥ 0.20). Integrity-gated research succeeded at its
   stated question (replay-to-exact-state preserved); it is not a cost win.
2. Minor accounting wrinkle: the per-byte `enc_copy` staging loops are not
   OP-counted individually (volume captured coarsely via 4KB-page OP-05
   counts). Immaterial to the verdicts; noted for the referee audit.
3. dp2-0319 excluded from the workload (documented in items_full.txt).

## Defects found

None affecting results. Previous crew's code reviewed against the znc defect
list (AGENTS.md ZNC-2026-09-21-00x): no `zalloc` naming, `_zag_strcmp == 1`
used correctly, `_zag_arg` read unconditionally (no argc gate), no
`nio_alloc as []i32` (u8 arenas + byte accessors throughout), slice-field
aliasing routed through pointers, no `_zag_arg` results freed, one binary
with argv[1] config dispatch, no /tmp battery runs. The respawn was
unnecessary for correctness — the prior work was complete and sound; the
verification above re-certifies it.
