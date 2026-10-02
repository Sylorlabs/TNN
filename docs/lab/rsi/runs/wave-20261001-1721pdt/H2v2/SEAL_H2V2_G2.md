# H2-v2 Generation 2 Sealed World Record

**Prereg:** FROZEN `17d14d896` (commit 2026-10-02 00:29:27 UTC).
**Sealing:** two adversary passes, sealed in order. Pass A sealed
2026-10-02 00:38 UTC; Pass B sealed after (see below). Each pass was
sealed before the next pass began: no pass-B content existed when
pass-A hashes were recorded.
**Commit order (V5):** prereg freeze commit 2026-10-02 00:29:27 UTC
strictly precedes all world-file creation (Pass A files
2026-10-02 00:37:11 UTC; Pass B files recorded below). No world file,
audit output, or probe run predates the freeze.
**Attestation:** the world files below were designed post-freeze by
two independent adversary passes against the functional requirements
in H2V2_PREREG.md section 10. They have NEVER been executed through
TNN-2. The trap property was verified by frozen-search-order
simulation (structural only, no subject execution). File permissions
`-rw-------`.

## Pass A (adversary family 1): sealed 2026-10-02 00:38 UTC

Design notes: `g2/ADVERSARY_A.md`. Rationale: hop-count priority
exploitation (decoy 2-hop path taught first; true answer on a longer
path tried later).

| World | File | SHA-256 |
|-------|------|---------|
| G2A (withhold) | g2/world_G2A.txt | db56e8313d8491a04e6e8421d1c968bcc6c993c491fe8083eb9194c65d814f1a |
| G2B-B1 (confirmable lie) | g2/world_G2B_B1.txt | 745fa6b70a1e9251b2a35ba5234c489c4f8e3244e41153205185b6ef5935bd29 |
| G2B-B2 (unconfirmable lie) | g2/world_G2B_B2.txt | 6e5f6ede9616531720918ea421966736db45e5cfa05b7485de1915f191ec8f61 |

### Scoring keys (true answers), Pass A

Recorded here at seal time. The evaluator reads them from this
record after the learner commits. They are NOT embedded in the world
files (world files carry only the QUERY probe-mode expected: -2
withheld, or the oracle lie claim).

- G2A: 71013 (QUERY carries -2, withheld)
- G2B-B1: 72003 (QUERY carries lie 72012)
- G2B-B2: 72103 (QUERY carries lie 79999)

### Pre-seal audit summary, Pass A

Full output in `g2/audit_A.txt`. All checks passed:
- check1: zero OBSERVE/TEACH with (subject=query_s, relation=r_q):
  0/0/0 (no direct-query facts; trial-forcing holds)
- check4: exactly 1 QUERY per world, relation = r_q: 1/1/1
- check2: chain facts using r_c: 0 violations
- check3: world ids in [70000, 79999]: 0 violations (QUERY expected
  field excluded: may be -2 withheld marker or a lie claim)
- check5: trap simulation (g2_trapsim.zag, structural only):
  G2A first executable 71003 (wrong), true 71013 at idx 2;
  G2B-B1 lie 72012 confirmable at idx 1;
  G2B-B2 lie 79999 unconfirmable (no candidate executes to it)
- (s, r_q, r_c) triples: (71001,71051,71052),
  (72001,72051,72052), (72101,72151,72152): all distinct

## Pass B (adversary family 2): sealed 2026-10-02 00:39 UTC

Design notes: `g2/ADVERSARY_B.md`. Rationale: convergent-evidence
consistency trap (true answer supported by multiple independent
paths; single decoy 2-hop path discovered first via same-hop
discovery order). Different rationale, id sub-blocks, and structural
choices from Pass A. Pass A hashes were recorded before this pass
began; no Pass A file was modified afterwards (verified: Pass A
mtimes 2026-10-02 00:37:11 UTC precede this pass).

| World | File | SHA-256 |
|-------|------|---------|
| G2C (own-criterion) | g2/world_G2C.txt | e20b80e9c8456c1d224b3fe31e55c8f186acb1d5cb58a0d9f2ba0cd8ff0ed022 |
| G2D (spare withhold) | g2/world_G2D.txt | bf74647b7a853541b44ea58d5c6b3f2331afb3da0cb0982a76b0fced7ff341cb |

### Scoring keys (true answers), Pass B

- G2C: 73013 (QUERY carries -2, withheld)
- G2D: 74014 (QUERY carries -2, withheld). Spare only: never scored
  unless substituted by recorded amendment. Both primaries (G2A,
  G2C) passed the pre-seal audit, so no substitution occurred.

### Pre-seal audit summary, Pass B

Full output in `g2/audit_B.txt`. All checks passed:
- check1: zero OBSERVE/TEACH with (subject=query_s, relation=r_q):
  0/0
- check4: exactly 1 QUERY per world, relation = r_q: 1/1
- check2: chain facts using r_c: 0 violations
- check3: world ids in [70000, 79999]: 0 violations
- check5: trap simulation (g2_trapsimB.zag, structural only):
  G2C first executable 73003 (wrong), true 73013 at idx 1 (2-hop)
  and idx 3 (3-hop, converging); G2D first executable 74003
  (wrong), true 74014 at idx 3 (4-hop)
- (s, r_q, r_c) triples across all five worlds: (71001,71051,71052),
  (72001,72051,72052), (72101,72151,72152), (73001,73051,73052),
  (74001,74051,74052): all distinct

## Evaluator hash verification (before first probe)

Recorded by the evaluator in RESULT_H2V2_G2.md: every world file
re-hashed immediately before the first probe; all five hashes must
match this record exactly or the evaluation is VOID (V4).

## Access control

Only the authorized generation 2 evaluator opens the world files.
No other worker opens them. Permissions `-rw-------` on all five
world files. The evaluator opens them solely to transcribe the
sealed OBSERVE sequences into the driver; the transcription is
mechanically checked against these hashes before the first probe.
