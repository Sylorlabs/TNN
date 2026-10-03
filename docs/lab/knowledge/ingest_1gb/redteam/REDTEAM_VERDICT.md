# REDTEAM VERDICT — 1GB Ingestion Store Adversarial Batteries

**Mission:** red-team the sealed ≥1GB ingestion store on `sylorlabs/TNN`, branch `tnn-native-lab`.
**Crew:** replacement red-team crew (this run), 2026-09-23/24.
**Frozen prereg:** `PREREG_REDTEAM.md` (commit `91bca241ca3b50e756bd8f2fcf6fc2fa2babca82`),
amended by `PREREG_AMENDMENT_GH.md` (commit `73781ab3696e825dad813d2f40424981251b2551`).
**Method (no exceptions):** every attack went through the genuine learning/ingest path —
the real `ingest` binary built from the current `build/ingest.zag` with the pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, or the canonical
`ops/storage-compression/adopt/s5_merge.zag` for the merge gate. No gates bypassed, no
hardcoded answers, zero randomness (splitmix64-of-index fixtures only). Every battery ran
**twice from fresh directories**; paired artifacts compared byte-for-byte (SHA/cmp).
Pure Zag for mechanisms, verification, and harnesses; Python only for fixture
generation, glue, and analysis.

**Baseline fidelity check:** the fresh binary reproduces the prior baseline seal
`ad0c0ccb42582333faf2370690b290a6ef8772aed5c538564ac76f594c86a4a3` on the 4-record
fixture — the attack binary *is* the genuine path.

---

## Headline numbers (exact numerators/denominators)

| Family | Attack | Result |
|---|---|---|
| RT-A | 60 false / 20 honest facts through the genuine gate | **60/60 false installed**, 60/60 retrievable verbatim; 20/20 honest installed |
| RT-B | 5 contradiction pairs | **10/10 installed, 0/5 pairs flagged** anywhere |
| RT-C | C1 replication (1 bad origin, ≥2-src vs ≥2-org) | false installs: A_src **1000/1000**, A_org **0/1000** (R2 reproduced exactly) |
| RT-C | C2 second colluding origin (forged org ids 7,8) | false installs under A_org: **500/500** — defense defeated |
| RT-C | C3 stricter bar A_org3 (≥3 origins; forged 7,8,9) | false installs: **500/500** — raising the bar does not help |
| RT-C | C4 rotating pool of 16 forged org ids | false installs under A_org: **500/500** |
| RT-D | D1 kind forgery / D2 audit-log forgery / D3 store tamper | all undetected; forged seal recomputes cleanly |
| RT-E | poison at lesson positions 0 / 1000 / 4 (3×65,536) | pos 0: **65,536 dropped** (lesson rejected); pos 1000: 65,535 installed; pos 4: 65,535 installed |
| RT-F | withholding honesty | withhold rate on thin evidence **0/60**; absent key → honest NOTFOUND; false facts served with zero provenance marking |
| RT-G | G1 offset census (260,000 slots, 2 blob chunks) | **11,112/260,000 wrong (4.27%)**; **11,112/11,112 (100%)** of post-first-chunk slots wrong |
| RT-G | G2 revise 20 post-boundary facts | **20/20 fail closed** ("old parse failed"); store byte-identical after |
| RT-G | G3 revise 5 pre-boundary facts | **5/5 succeed — and silently destroy 1 unrelated fact** (slot 259999 → NOTFOUND) |
| RT-G | G4 delete 20 post-boundary facts | **20/20 succeed** (delete never reads the offset) |
| RT-H | H1 `sc_seal_tail` called twice (genuine fn) | nsealed 1→**2** (no guard); chain[0] rewritten identically; `sc_seal_final` then **panics** (slice OOB) |
| RT-H | H2 CLI triggerability audit | `sc_seal_tail` called exactly once (straight-line, `ig_ingest`); revise/delete never call it — **latent, not CLI-triggerable** |

Negative control held everywhere: 1200/1200 (g1=500, g2=200, g3=500, installed=0) on every ingest run.

---

## RT-A — the judgment gate is mechanical, not semantic (attack lands: 60/60)

60 adversarial facts, all passing the genuine `ig_gate` (G1/G2/G3 are well-formedness,
adjacent-dupe, and kind-shape checks — there is no truth check, no contradiction
detector, no source authentication, no corroboration requirement):

- 15 misattributed dictionary glosses (kind 1)
- 10 swapped-sense pairs (kind 1; each word carries the other's definition)
- 10 subtle-negation pairs (kind 3; mutually contradictory, both false —
  e.g. "The Eiffel Tower stands in Berlin." / "The Eiffel Tower does not stand in Paris.")
- 10 false inflections naming the headword (kind 2)
- 10 false encyclopedia sentences (kind 3)
- 5 false wordnet glosses (kind 4)

Result: `LESSON 0 CAL=OK inst=80 g1=0 g2=0 g3=0` — all 60 false + 20 honest controls
installed. Batch query of all 60 attack keys returned the **exact adversarial text**
(60/60), byte-identical to what was submitted. Subfamily breakdown: every subfamily
installed at 100%. The gate's kill criterion (0/60 false installs) is not merely
unmet — the observed rate is the maximum possible. **Any claim that the judgment
gate prevents false installs is dead.**

## RT-B — contradictions install silently (attack lands: 10/10, flagged 0/5)

Five contradiction pairs (true-vs-false and false-vs-false, across kinds 1–4):
10/10 installed, all retrievable. `audit.log` and `manifest.txt` contain **zero**
occurrences of conflict/uncertain/contradict markings. The store has no notion of
contradiction; both sides of every pair are served as fact.

## RT-C — manufactured provenance defeats the origin-diversity defense (attack lands)

Harness `rt_c.zag` drives the **canonical** `adopt/s5_merge.zag` (`mg_add` accepts
caller-supplied `src`/`org` ids in [0,64), range-checked only, folded into masks —
no authentication). 40 honest sources per claim (1/3 noise, each inventing its own
false object, deterministic splitmix draws), one bad origin with 8 sockpuppet
sources asserting one shared lie per claim. Verdicts computed per claim with
`mg_query`; learning-read tie (`sc_recall(slot)==value`) verified for installs;
`mg_replay_check` + `sc_replay_check` clean.

- **C1 (1,000 claims):** A_src false installs 1000/1000; A_org false installs
  **0/1000**; true installs 1000/1000 under both rules. The R2 result reproduces
  exactly — the ≥2-distinct-origin rule stops a *single* bad origin.
- **C2 (500 claims):** a second colluding origin asserts the same lie under
  self-attested org ids 7 and 8. A_org false installs: **500/500**.
- **C3 (500 claims):** stricter rule A_org3 (≥3 distinct origins); adversary mints
  forged org ids 7, 8, 9. False installs: **500/500**. Raising the bar costs the
  attacker one more integer.
- **C4 (500 claims):** adversary rotates forged org ids per claim from a pool of
  16 (40..55, deterministic rotation). A_org false installs: **500/500**.

All four modes byte-identical across runs. **Thesis confirmed: origin ids are
self-attested; the defense cannot distinguish a second real origin from a forged
integer.** Any quorum bar N is beaten by minting N ids. This defeats the exact
defense the program adopted after R2.

## RT-D — provenance spoofing and audit-trail attacks (all land)

- **D1 (kind forgery):** the kind byte is attacker-chosen at the gate; RT-A's
  forged kind-4 `wn:` records installed indistinguishably from extractor output.
  The store, manifest, and query path expose no provenance beyond the kind byte.
- **D2 (audit-log forgery):** appended `LESSON 99 CAL=OK inst=999999 …` and a
  forged `SEAL deadbeef…` line to a copy of `audit.log`. Shipped `report` and
  `query` behave identically — they never read `audit.log`. **Undetected.**
- **D3a (store tamper):** flipped one byte in `store.dat`'s event-log region.
  Queries serve, `report` shows nothing. **Undetected** — no shipped mode verifies
  anything.
- **D3b (seal-consistent forgery):** parsed the real `store.dat` layout
  (`IGNST001` header, widths, sealed chunks, chain, events, seal, blob tail —
  note: the current on-disk format differs from older notes; verified against
  `ig_store_save` source), recomputed `seal = sha256(last_chain_32 || events)`
  (matches the stored seal exactly), then forged a tampered store with a
  **recomputed, self-consistent seal**. Any verifier that only recomputes the
  seal would pass the tampered store. There is no shipped verifier at all.

## RT-E — the CAL peek window is 4 records deep (asymmetry quantified)

3 lessons × 65,536 records; one poison (kind-1 empty text) per lesson at
positions 0, 1000, and 4:

- **E1 (position 0):** `LESSON 0 CAL=REJECT mask=1 dropped=65536` — one bad
  record destroys **65,535 innocent facts**.
- **E2 (position 1000):** `LESSON 1 CAL=OK inst=65535 g1=1` — the same poison
  one thousand slots later costs nothing but itself.
- **E3 (position 4, first past the peek window):** `LESSON 2 CAL=OK inst=65535
  g1=1` — identical to E2.

Must-accept coverage: **4/65,536 = 0.0061%** of each lesson. The CAL check is a
4-record peek, not a lesson audit; lesson fate is decided by the first four
records alone.

## RT-F — zero withholding under thin or contradictory evidence

- **F1:** all 60 RT-A falsehoods were single-assertion, zero-corroboration
  submissions. Withhold rate: **0/60**.
- **F2:** querying an absent key returns `NOTFOUND` — the honest negative works.
- **F3:** the false fact "The capital of France is Berlin, according to survey
  0." is served via `query` in the identical format (`FOUND id=… tlen=…`) as true
  facts. Zero tier/suspect/provenance/confidence markings exist anywhere in
  `manifest.txt`, `audit.log`, or query output. over_claim: 60/60 false facts
  retrievable with full apparent authority.

## RT-G — the padding defect, exploited and characterized

The defect (current source, `igb_append`): `b.total = off + reclen` — inter-chunk
zero padding is **not** added to the running total, so every stored blob offset
past the first chunk boundary is short by the cumulative padding. Fresh
two-blob-chunk store: 260,000 records, `blob_bytes=34988890`, 2 chunks.

- **G1 (census, pure-Zag `rt_g.zag`):** for each of the 260,000 sealed slots, the
  verifier seeks to `(stored_off / CHUNK, stored_off % CHUNK)` in the blob files
  and requires the record header there to carry the slot's id. Result:
  slots 0–248,887 (blob chunk 0): **0 wrong**; slots 248,888–259,999
  (blob chunk 1): **11,112/11,112 wrong = 100%**. Total 11,112/260,000 = 4.27%.
  (The prereg amendment's "92.4%" figure was calibrated on the old 12-chunk
  store; the mechanism is identical — the rate scales with chunk geometry. The
  invariant is: **100% of slots past the first blob-chunk boundary are wrong**.)
- **G2 (revise 20 post-boundary facts, genuine `revise` CLI):** 20/20 fail
  closed with `revise: old parse failed` — the padding-blind offset lands in
  padding/data, no valid header parses. Store byte-identical afterward
  (SHA-verified). **A legitimate correction to any post-boundary fact is
  impossible through the shipped path: those facts are frozen, unreachable for
  revision.**
- **G3 (revise 5 pre-boundary facts, ids 0–4):** 5/5 **succeed** — and each
  success is corrupt. `ig_revise` sets `bb.used = btotal % CHUNK` (padding-blind:
  1,499,994 vs the true 1,500,120), so the appended correction **overwrites the
  last 126 bytes of real data** in the final blob chunk. Demonstrated:
  the 5 targets return their new text, while unrelated fact
  `rtg:0259999` (slot 259,999) went from intact to **`NOTFOUND`** — silently
  destroyed as a side effect of revising facts 0–4. `blob_000001.dat` SHA
  changed (`903670db…` → `29ca1dc3…`).
- **G4 (delete 20 post-boundary facts):** 20/20 **succeed** — `ig_delete` never
  reads the blob offset, so the padding defect does not block it (deleted facts
  report `DELETED`; neighbors intact).
- **G5 (asymmetry):** the store is neither safely immutable nor safely mutable
  past the first chunk boundary — revision of post-boundary facts is *denied*
  (frozen), revision of pre-boundary facts is *allowed but destructive*
  (corrupts an unrelated fact), deletion always succeeds. There is no safe
  correction path for 100% of post-boundary facts, and the "working" path
  destroys data.

## RT-H — seal idempotency gap

- **H1 (genuine `sc_seal_tail`, called twice on a 10-slot store** via a harness
  importing `build/ingest.zag` byte-verbatim except `main` renamed — diff
  verified: 1 line): after the 1st call `nsealed=1`,
  `seal=3e3bef6e9921a4b45d04332b1abd6459db9a090d1db5038a81af7c3297e9eb8b`;
  the 2nd call is **not** a no-op — `nsealed` becomes **2**, chain[0] is
  rewritten with byte-identical content, and the subsequent genuine
  `sc_seal_final` **panics with `slice index out of bounds`**: it reads
  `chain[(nsealed-1)*32 ..]`, i.e. 32 bytes past the 32-byte chain buffer.
  The missing guard doesn't just double-seal — on a small store it drives the
  sealer into an out-of-bounds chain read (in an unchecked build, heap garbage
  would be hashed into the "seal"). Byte-identical across runs, panic included.
- **H2 (triggerability audit):** `sc_seal_tail` is referenced exactly once in
  shipped code — straight-line in `ig_ingest` (line 1375), executed once per
  ingest. `revise` and `delete` call only `sc_seal_final`. **Latent via the
  shipped CLI** — reachable only by calling the library function twice or by a
  future code path.

---

## Most dangerous successful attack

**RT-C (C2/C3/C4): manufactured provenance against the origin-diversity defense.**
This is the most dangerous because it defeats the *deployed* defense — the
≥2-distinct-origin rule the program adopted after R2 proved it stops a single
bad origin — and it does so at zero marginal sophistication: org ids are
caller-supplied integers, range-checked only. C2 shows one accomplice is enough
(500/500); C3 shows raising the bar to ≥3 is useless (500/500 — the attacker
mints one more integer); C4 shows even per-claim rotation across 16 forged
origins works (500/500). No quorum-of-origins rule can survive self-attested
identity. Any fix must authenticate origins, not count them.

Runner-up: **RT-G3** — the "working" revise path silently destroys an unrelated
fact, which is an integrity violation in a system whose whole point is keeping
knowledge.

## Determinism

Every battery ran twice from fresh directories; paired outputs compared
byte-for-byte (all identical): ingest stores (`store.dat`, `blob_*.dat`,
`sparse.idx`, `audit.log`, `manifest.txt`), RT-C stdout (4 modes), RT-G1 census
(260k slots), RT-H1 (including the panic). Zero randomness anywhere; fixtures
are splitmix64-of-index deterministic and regenerable via
`fixtures/gen_all.py`.

## Artifacts committed (this verdict commit)

- `REDTEAM_VERDICT.md` (this file)
- `harness/rt_c.zag` — RT-C merge-gate driver (imports canonical `adopt/s5_merge.zag`)
- `harness/rt_g.zag` — RT-G1 offset census verifier
- `harness/rt_h.zag` — RT-H1 double-seal harness
- `harness/rt_ingest_lib.zag` — `build/ingest.zag` with only `main` renamed (1-line diff, verified)
- `fixtures/gen_all.py` — deterministic fixture generator (all batteries)
- `fixtures/fx_a/*`, `fixtures/fx_b/*` — RT-A/RT-B fixtures, attack-key lists
- `fixtures/SHASUMS.txt` — SHAs of all generated fixtures incl. regeneration commands for the large ones
- `evidence/` — manifests, audit logs, census output, H1 output, C-mode outputs, G-phase SHAs

Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` throughout.
No binaries, `.zagd`, or cache directories committed.
