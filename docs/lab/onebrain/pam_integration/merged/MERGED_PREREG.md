# MERGED PREREG — one-brain + self-PAM R1–R4 integration

Date: 2026-09-25. Branch: `tnn-native-lab`, repo `sylorlabs/TNN`.
Scope: merge the four verified self-PAM repairs (R1 N-AUTH, R2 exhaustion caps,
R3 PROVTAG shadowing, R4 poison recovery) into one tree, prove the repairs
compose (no cross-repair regressions, no weakened bars), and explicitly test
three cross-repair interactions.

## 0. Procedural note (timing deviation)

This prereg was WRITTEN from the task spec and the four frozen repair preregs
before any merged-tree evidence was collected, but it is being COMMITTED after
exploratory implementation and test runs already occurred (coordinator sequencing
error: the "commit prereg first" step was skipped). The kill bars below are
transcribed unweakened from the four repair preregs and the task's interaction
spec; no bar was altered on the basis of observed results. The deviation is
recorded here so the preregistration guarantee is honestly qualified: substance
preregistered, timestamp ordering violated.

## 1. Frozen inputs (repair preregs, unweakened)

### R1 (N-AUTH identity) kill bars
- K1: forged overseer identity with unkeyed hash refused at auth; no
  forwarding/install/weight/nonce consumption.
- K2: forged overseer-only force-pin refused at auth.
- K3: consumed-envelope replay refused BAD_NONCE.
- K4: wrong-organ-key tag refused at auth.
- K5: legitimate smoke, both LH legs, and non-N red-team behavior byte-identical
  to frozen refs; only N1/N2/N3 deltas allowed.
- K6: nonce-desync self-heal works under keyed tags.
- K7: zero RNG and 3× deterministic batteries.

### R2 (exhaustion caps) kill bars
- K1: exact 2000-revoke/4000-ledger-row and 600-withhold counts; no silent drops.
- K2: all 600 quarantine entries real; no phantom quarantine rows.
- K3: conflict detection correct past installed indexes 128, including 150 and 199.
- K4: 200 distinct first-round withholds do not falsely escalate; third round
  legitimately escalates with ledger/inbox.
- K5: LH T1–T5 byte-identical to frozen refs.
- K6: every physical chunk ≤ 2^25 bytes.
- K7: zero RNG.

### R3 (PROVTAG shadowing) kill bars
- K1: quarantine → EXT support → install records PROVTAG EXT.
- K2: GEN-only unsupported claims remain GEN and withheld.
- K3: later GEN sighting cannot downgrade EXT incumbent/reinstall.
- K4: all ten laundering attacks remain WITHHOLD.
- K5: LH T1–T5 unchanged.
- K6: zero RNG.

### R4 (poison recovery) kill bars
- K1: poisoned POS+NEG subject becomes recoverable after legitimate `M_REVISE`;
  POS installs and exactly one revision ledger row exists.
- K2: valid-auth non-overseer revision refused; no revision; poison remains.
- K3: four unsupported/bad-evidence/bad-target revision subcases refused.
- K4: revised-away falsehood remains withheld and dead evidence cannot authorize revision.
- K5: exact revision/refusal ledger accounting; raw store remains append-only with
  original EXT suffixes.
- K6: no-revision poisoned sequence remains byte-identical to frozen F4 behavior.
- K7: LH T1–T5 unchanged.
- K8: zero RNG and 3× determinism.
- R4's old 64-row cap was removed by `a94d5f56`; revision storage is logically
  unbounded, physically chunked (no-limit proof must remain).

## 2. Merged-tree design freezes

### 2.1 Ledger-code collision (R2 vs R4)
Both repairs independently froze code 312 (R2: SP_L_STORE_FULL; R4: SP_L_REVISE).
Resolution (frozen): R2 keeps `SP_L_STORE_FULL=312`; R4 merged codes shift to
`SP_L_REVISE=313`, `SP_L_REV_REFUSED=314`. All code uses symbolic constants;
semantics unchanged.

### 2.2 Gate-state layout (merged)
- G_CHUNK_HEAD=66608, G_CHUNK_N=66648 (R2 chunk metadata)
- G_POOL_HEAD=66668, G_POOL_N=66676
- G_LASTNTFY=66680
- G_KEYS=66712 (R1 key registry, 256 bytes)
- G_REV_HEAD=66968, G_REV_N=66976 (R4 revision metadata)
- G_STATE_SZ=66980
No overlaps among R2 chunk metadata, R1 key registry, R4 revision metadata.

### 2.3 Revision chunk byte accounting
R2's `sp_chunk_max_bytes()` is extended: allocated revision chunks contribute
`SP_REV_CHUNK_BYTES` to the max-chunk accounting. The only size bound is the
load-bearing znc 2^25-bytes-per-slice ceiling (worked around, never a design cap).

### 2.4 N-AUTH failure ledgering on M_REVISE (frozen behavior)
N-AUTH failures (bad tag/nonce) on M_REVISE ledger `SP_L_REFUSED_UNAUTH` +
`SP_L_NOTIFY` (existing path, no revision row). Authority-class failures ledger
`SP_L_REFUSED_UNAUTH` + `SP_L_REV_REFUSED(SP_R_UNAUTH)` (R4-verified behavior).

## 3. Cross-repair interaction tests (must all PASS; any failure = no adoption)

### MX1: R4 M_REVISE through R1 keyed N-AUTH
- MX1a: legitimate overseer M_REVISE with correctly keyed tag applies
  (SP_INSTALL, SP_R_REVISE_OK, exactly one SP_L_REVISE row).
- MX1b: forged identity (non-overseer claiming ORG_OVERSEER) with attacker-minted
  UNKEYED legacy tag on M_REVISE → refused AT AUTH (NAUTH_R_BAD_TAG); fwd=0,
  disp=SP_WITHHOLD, reason SP_R_UNAUTH; no revision row appended; no
  SP_L_REV_REFUSED row; victim's gate nonce NOT consumed (real overseer re-emits
  at the same nonce with its key and applies).
- MX1c: wrong-key tag (another organ's key, overseer-claimed) on M_REVISE →
  refused at AUTH (NAUTH_R_BAD_TAG); no revision row.
- MX1d: replay (valid tag, stale nonce) on M_REVISE → refused NAUTH_R_BAD_NONCE;
  no revision row.

### MX2: R4 revision rows through chunked storage
- 100 revisions applied (past the old 64 cap): G_REV_N=100 exact,
  SP_L_REVISE=100, zero SP_L_REV_REFUSED.
- Revision chunk chain walks to exactly the expected chunks; every chunk is
  exactly SP_REV_CHUNK_BYTES ≤ 2^25.
- Rows 64 and 99 read back exact (no truncation, no silent drop, no cap-64 reappearance).
- Supersession holds for beyond-cap targets.

### MX3: R3 effective provenance AFTER R4 rehabilitation
- Poisoned subject revised (NEG superseded by legitimate M_REVISE).
- Warranted surviving POS claim INSTALLS through the normal draft→verdict path
  (SP_INSTALL, SP_R_OK, fwd=1).
- Its install-time SP_L_PROVTAG row = EXT (1): not GEN-shadowed, not poison-stained.
- Revised-away NEG re-emitted withholds (SP_R_CONTRADICTED).

## 4. Battery bars (all must PASS)

- Smoke 3×: rc=0, OB_FAILURES,0, byte-identical; SHA must equal frozen ref
  `6855928854e38255e7275a18c5b07c82675fe1bc0752a616ba9ca90ba2e6d2e0`.
- Red team 3×: rc=0, RT_FAILURES,0, byte-identical (includes all R1/R2/R3/R4
  probes + MX1/MX2/MX3).
- LH B-alone 3× (s1/s10/s100): rc=0, OB_FAILURES,0, byte-identical; SHA must equal
  `cc7e86ed4a00be36bb4f5a2aacc6456197281270b4eb40717ebb1ca017ea93e9`.
- LH integrated 3× (s1/s10/s100): rc=0, OB_FAILURES,0, byte-identical; SHA must equal
  `356b7873bf07942c6b2283ed087911d3bfa724cea1ab707fb1ccaf14821cec3b`.
- Zero RNG: grep backstop (`rand|srand|random|lcg|entropy|/dev/urandom|getrandom`)
  zero hits across all merged src/ trees; empirical 3× byte-identity.
- Source identity: the three `sp_gate.zag` copies byte-identical.

## 5. Adoption rule

ADOPT iff every bar in §§1–4 passes unweakened and all three MX interactions pass.
Any interaction failure, any weakened kill bar, any non-byte-identical rerun, or
any RNG hit → HOLD/REJECT (no adoption).
