# FORK D AMENDMENT 01 — WRITE-ONCE EVIDENCE PARTITION (PROV-PHYS)

**Date:** 2026-09-27 | **Branch:** `tnn-native-lab` (sylorlabs/TNN)
**Parent preregs:** `FORKD_PREREG.md` (frozen, fork D); program prereg
`docs/lab/senses/pam-rebuild/selfpam/r2/PREREG.md` (`b3db7b7a`); r2
`SYNTHESIS.md` ("D's discipline + a tamper-evident provenance substrate
would move the trust root from labels to physics" — this amendment IS that
experiment).
**Status:** FROZEN on commit. This file is committed ALONE, before any
partition or verifier code is written. Amendments require the coordinator.

## 0. What this experiment is

Fork D survives red-team (24/24 trace-alibi rejection, 8/8 genuine
generator-authored confabulations, 4/4 held-out, 12/12 utterance-type
smuggling) but its trust root is the PROV *label*: the M5L-001 probe
demonstrates provenance laundering — relabel a generator-authored entry as
EXT and the checker INSTALLs it. The label is harness-pinned ground truth;
anyone who can write the store file can set it.

This experiment replaces the label with physics: a write-once evidence
partition the generator cannot author. EXT entries can only be appended by
an attested independent channel (signature-verified appends); the
generator's entries go to a partition it CAN write (GEN, always
distrusted). Relabeling stops being a label change and becomes a
cryptographic forgery — mechanically impossible without the channel key.

Success = the M5L-001 laundering family fails closed mechanically AND
fork D's measured discipline bars (M1–M6) still pass over the new
substrate. Failure modes are specified in §5; the "wiring is impossible"
outcome is a first-class result (§6).

## 1. Partition design (frozen)

Two append-only partitions per battery corpus, both plain-text files.

### 1.1 EXT partition (the evidence partition)

Line 1: `PART|<tag>|<nentries>`.
Then one line per entry:
`ENTRY|<tag>|<atom>|<prev_hex>|<pknext_hex>|<sig_hex>`
- `<atom>`: 5-field canonical atom `Q|S|POL|R|O`. There is NO provenance
  field — partition membership IS the provenance. Any entry whose atom is
  not a valid 5-field atom (fork prereg §1.1) voids the partition.
- `<prev_hex>`: 64 hex chars. Entry 0's prev is 64 zeros (genesis). Entry
  i>0's prev must equal the chained value recomputed from entry i−1
  (§2.4) — the tamper-evident hash chain (reorder / splice /
  middle-truncation detected).
- `<pknext_hex>`: 64 hex chars = the one-time public key authorizing entry
  i+1 (the chained-key construction, §2.3).
- `<sig_hex>`: 4288 hex chars = 67 × 32-byte WOTS signature (§2) over the
  entry message.

### 1.2 GEN partition (the generator's partition)

Line 1: `PART|<tag>|gen|<nentries>`.
Then one line per entry: `GENENTRY|<tag>|<atom>|<prev_hex>`.
- Unsigned (the generator authors these; distrusted by construction), but
  hash-chained for tamper-evidence: prev_0 = 64 zeros;
  prev_{i+1} = SHA256(prev_i_bytes || atom_bytes), hex.
- A broken GEN chain voids the run (fail closed, §3.3) — write-once means
  write-once, even for the distrusted side.

### 1.3 Why the generator cannot author EXT entries

The generator role = any party holding the partition files but NOT the
channel private seed. Minting a valid EXT entry requires a WOTS signature
under the one-time key whose public key the previous entry (or the pinned
genesis) commits to. Verification is deterministic SHA256 arithmetic in
the verifier — no labels, no trust in whoever wrote the file. Relabeling
generator bytes as EXT now requires forging a signature, not flipping a
field.

## 2. Signature scheme (frozen): hash-based WOTS, chained one-time keys

WOTS with Winternitz parameter w=16, message digest 256 bits:

- 64 base-16 message digits d_0..d_63 (high nibble of each digest byte
  first); checksum c = Σ(15 − d_i), encoded as 3 base-16 digits big-endian;
  67 digits total per signature.
- sk(tag,idx,j) = SHA256(SEED || tag || idx_be4 || j_byte), j ∈ 0..66.
  SEED = ASCII `selfpam-forkd-partition-channel-v1` (pinned; experiment
  fixture — a production channel would use real randomness at keygen; the
  verifier never sees the seed and no experiment conclusion depends on
  seed secrecy beyond the forgery game).
- tip(sk) = SHA256^15(sk) (15 iterations). pk(tag,idx) =
  SHA256(tip_0 || … || tip_66), 32 bytes.
- Entry message m(tag,idx) = SHA256(tag || atom || pknext_raw || prev_raw).
  sig_j = SHA256^{15−d_j}(sk_j).
- Verify: recompute m and its 67 digits; for each j, t = sig_j, apply
  SHA256 d_j times, require t == tip_j; pk_computed =
  SHA256(tip_0||…||tip_66) must equal the authorizing pk (pinned genesis
  for entry 0, else the previous entry's pknext). All comparisons
  constant-shape (no early length leaks matter here; exact byte equality).

### 2.1 Key chaining (no Merkle tree)

Entry i is signed by sk(tag,i) and carries pk(tag,i+1). The verifier pins
exactly one value per tag: genesis_pk(tag) = pk(tag,0), baked into the
verifier source (emitted by the channel tool, committed). Each signature
consumes its one-time key; keys are never reused across entries or tags
(sk binds tag and idx).

### 2.2 Genesis pins

One pinned 64-hex-char genesis public key per partition tag, compiled into
the verifier. The closed pin table: c1, c2, c3, c4, c5, c6, m2a, m2b, m4,
m5, launder, ct. A partition whose tag is not in the table, or whose
header count disagrees with its entry lines, is VOID.

### 2.3 Chain binding

prev_{i+1} = SHA256(prev_i_raw || atom_i || pknext_i_raw || sig_i_raw),
hex. The signature message binds (atom, pknext, prev); the prev chain
binds entry order and full entry bytes. Mutating any byte of any entry
breaks its own signature or the next entry's prev — both detected on
re-verification from genesis.

## 3. The verifier: `forkd2` (pure Zag, pinned toolchain)

New binary `forkd2`, built from fork-D sources plus new modules
(`part.zag`: partition parse + WOTS verify + attestation;
`genesis.zag`: pinned genesis keys, channel-emitted). The discipline
kernel (atomize, K1–K8 prover, trace validator) is fork D's, unchanged in
logic; its interface changes from labeled stores to partitions (§3.2).

- `forkd2 attest <extpart>` → re-verifies the whole chain from the pinned
  genesis. Stdout: `OK|<tag>|<n>|<tip_hex>` or `FAIL|<reason>`; digest on
  stderr (cf1 convention).
- `forkd2 verdict2 <draft> <extpart> <genpart> <delib>` → full pipeline
  (§3.2).
- `forkd2 battery2 <manifest2>` → manifest2 lines
  `case|draft|extpart|genpart|delib|expected`; per-case
  `case|verdict|expected|match` lines; digest on stderr.
- `forkd2 atomize <sentences>` kept for debugging.

### 3.1 Attestation (frozen)

For the presented extpart: parse header; look up the tag's pinned
genesis (unknown tag → VOID); for each entry in order: check tag match,
atom well-formedness (5-field, valid Q/POL/R), prev linkage (§2.3),
WOTS signature against the authorizing pk (§2). Any failure → the
partition is VOID. The GEN partition's chain is re-verified the same way
(unsigned). VOID on any failure there too.

### 3.2 Discipline rewiring (frozen)

- The prover's evidence partition = the atom list extracted from
  attested-valid EXT entries, in entry order. The GEN atom list feeds ONLY
  the GEN_ONLY diagnostic (entailed-with-GEN-but-not-EXT-alone →
  UNGROUNDED annotated GEN_ONLY, as before).
- The 6-field `Q|S|POL|R|O|PROV` store format is RETIRED in the new path:
  there is no label to read. `closure_base`'s PROV filter is replaced by
  partition membership (entries are EXT by construction).
- Trace premise validation (`store_has_ext`) becomes verified-EXT
  membership: a PREMISES atom must exactly match an attested EXT entry's
  atom; LOOKUP steps likewise. Everything else in §1.5–1.7 of the fork
  prereg is unchanged (kernel rules, depth cap 3, EARNED/UNEARNED/REVISION,
  INSTALL conditions).

### 3.3 Fail-closed rule (frozen)

If attestation fails for EITHER partition, the run does not fall back to
labels (there are none) — every draft atom is cited
`atom|EXT_UNVERIFIED|EXT_UNVERIFIED|partition-void` (or GEN_UNVERIFIED)
and the verdict is WITHHOLD. A void partition can never INSTALL.

## 4. The channel (offline, Python — NOT in the trust boundary)

`channel.py`: deterministic keygen from the pinned SEED (experiment
fixture), signs each corpus's honest EXT atom list in store order, emits
the EXT/GEN partition files and `genesis.zag`. The channel's private seed
is committed as a fixture (it must be, for determinism); the property
under test is that WITHOUT the seed no valid entry can be minted, which
§5's forgery cases demonstrate mechanically. The channel is the analog of
the trainer console: an offline authority, not part of the verified
mechanism. Python is glue/tooling here (repo standard allows Python for
glue/analysis); the mechanism (partition format, attestation, kernel) is
pure Zag.

## 5. Kill bars (frozen)

### B1 — laundering is mechanically impossible (the point of the experiment)

- L1: the M5L-001 laundering case rebuilt for the new world — the 72
  honestly-signed EXT entries PLUS one attacker-forged entry carrying the
  generator-authored atom `UNIT|zorp|POS|IS_A|qux` with a garbage
  signature, draft "The zorp is a qux." → must WITHHOLD with
  EXT_UNVERIFIED. (Old world: INSTALL. The flip is the kill.)
- L2: fully-forged single-entry partition (attacker mints their own key
  chain, reuses the pinned tag) → `attest` FAIL.
- L3: one hex character flipped in a valid entry's signature → `attest`
  FAIL → battery2 WITHHOLD.
- L4: two valid entries swapped (reorder) → `attest` FAIL → WITHHOLD.
- L5: entry signed with a wrong-seed key (forgery attempt with a
  well-formed but unauthorized signature) → verification FAIL.
- Bar: ALL of L1–L5 fail closed. ANY INSTALL or `OK` on these → B1 fails
  → the write-once claim is false (§6).

### B2 — no regression: M1/M2/M3/M4/M6 still pass over the new substrate

Corpora c1–c6, red-team m2 (25 flip pairs), red-team m4 (24 alibis)
migrated to partitions (same atoms, same kernel):
- M1 (c1, 140): ≥70% WITHHOLD.
- M2 (m2a/m2b, 25 pairs): ≥90% divergent pair verdicts.
- M3 (c3, 65 pairs): ≥95% identical pair verdicts.
- M4 (c4, 60 + red-team m4, 24): ≥70% WITHHOLD.
- M6 (c2, 140): ≤5% false WITHHOLD.
Plus the per-case agreement gate: for every migrated non-launder case,
verdict2 MUST equal the original fork-D battery verdict — 100% agreement
required. Any single verdict moved by the substrate (other than L1's
expected INSTALL→WITHHOLD flip) fails B2.

### B3 — M5 genuine recursion still caught

- c5 (60): ≥70% WITHHOLD.
- Red-team m5 genuine (8 cases, E1-authored GEN entries in the GEN
  partition): 8/8 WITHHOLD, GEN_ONLY diagnostic present on the
  GEN-loaded atoms.

### B4 — determinism

- Full battery2 run twice; outputs byte-identical; digests equal.
- Zero RNG identifiers in new `.zag` sources (grep audit for
  `rand|rng|seed|clock|time(|getrandom`).
- Partition files byte-pinned (SHA256 recorded); rerun from pinned files.

### Kill rule

- B1 fails → the substrate does not deliver write-once; stop, write the
  impossibility analysis (§6). No further bars are banked.
- B2 fails via the agreement gate → the wiring moved a verdict: diagnose;
  if substrate-caused, wiring fails (§6); if the original battery also
  fails the bar (pre-existing), document and carry the measured value.
- B3/B4 fail → fix or document; no verdicts banked until B4 holds.

## 6. The impossibility outcome (first-class result)

If wiring proves impossible, the deliverable is a proof, not a wiring:
exactly which step breaks (e.g. attestation cannot be expressed in the
Zag subset, the signature does not fit the determinism budget, the kernel
cannot consume partitions without labels), with a minimal reproducer and
the measured failure. "Cannot be wired" must be demonstrated, not
asserted.

## 7. Commit sequence

1. THIS FILE, alone, before any partition/verifier code (frozen-rule).
2. Then: channel tooling + verifier sources + genesis pins + migrated
   corpora + battery evidence + verdict report, one commit.
3. No binaries, no `.zagd` caches, no `.zag-cache/` (repo content
   standard). Target branch `tnn-native-lab`, rebased onto origin head.
   Amendments to this amendment are committed as `AMENDMENT_02_*.md`; this
   file itself is never edited after freezing.
