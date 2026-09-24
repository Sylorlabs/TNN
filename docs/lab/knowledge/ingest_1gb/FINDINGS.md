# 1GB Ingestion — Consolidated Findings (red teams, audits, forks, more tests)

**Date:** 2026-09-23. **Ordered by:** Micah ("figure out issues with 1gb ingestion, send red teams and audits along with forks and more tests on it, document and tell me findings").
**Baseline under test:** report commit `ebcb273b` (1.86 GiB corpus, 3,707,990 merged, 2,597,057 installed, sealed).
**Method:** four independent crews, frozen preregs before every battery, pure Zag for mechanisms/verification, zero randomness, byte-identical reruns proven by SHA. All commits on `tnn-native-lab`.

## 1. Crew verdicts

| Crew | Verdict | Commits |
|---|---|---|
| Audit (sealed store) | 6/8 checks PASS; **3 violations** (padding defect blocks E2/E3; false report §2; seal-idempotency violation) | `406eb66f` (+prereg `7bab8109`) |
| Red team (replacement crew; first crew died on a safety-filter false positive, nothing committed) | **ALL attack families succeeded** — no defense held | `91bca241` (prereg) → `73781ab3` (amendment) → `a1e20eed` (verdict+evidence) |
| Gap closure (Wiktionary 56%, 9 CAL-rejected lessons, WordNet deviation) | All three root-caused and closed; WordNet amendment **pending Micah's signature** | `bda2c8c6` → `e51f05e0` → `454f3bd8` → `45a52291` → `52156b3e` → `4fe36acd` → `c2bd231e` → `924672b7` |
| Machinery (sindex fix, S5→scale-learner integration, scaling) | Both forks PASS; 10GB projection measured | `0e551199` → `4917dbbe` → `584d4fa3` |

## 2. Known issues — root-caused (not symptoms)

### 2.1 Wiktionary 56% partial → CLOSED
**Root cause:** non-clean process interruption/kill after a deliberate time-stop left a stale 5M-page checkpoint — not a parser limit, not a data-structure failure. Full dump is **10,895,934 pages** (not ~9M as estimated). Pages 5M–10.9M extracted: **1,220,431 clean records** (97,854 short + 3 malformed dropped, all legacy). Deterministic, SHA'd.

### 2.2 9 CAL-rejected lessons (1.1M records) → CLOSED
**Root causes (two defects; the report's "likely wiki append-duplicate quality" guess was wrong):**
1. The original merge **counted 539,418 duplicates but wrote them all** — it never actually deduped (independently confirmed by the audit crew: REPORT §2's "4,247,408 input → 3,707,990 unique, 539,418 removed" is false; 4,247,408 was a phantom = output + dupes).
2. Wiktionary emitted **97,857 G3-invalid records** that poisoned 9 lessons as units.
Re-merge with true dedup: 4,106,863 → **3,565,287 unique** (541,576 dropped). Two ingests: **55/55 CAL=OK, 0 rejections** — the rejections were downstream of the two defects, not bad data. New seal `93862fe1ea4a6944eae30b8fd1a72d27297860643658135ae85f12a03b9e306a`; E1 **1,000/1,000 exact**. REPORT.md corrected (CAL arithmetic was also wrong: 9×65,536=589,824, not 1,110,933).

### 2.3 WordNet transport deviation → TECHNICALLY CLOSED, governance pending
Transport changed zero bytes (all 4 data files byte-identical; extraction SHA `575bab57e195f27908cfcd660cd42ba38bccec3bf363c34f4922a48bd205cbb7`). Amendment `AMENDMENT_WORDNET_TRANSPORT.md` **awaits Micah's signature**.

### 2.4 E2/E3 ID-mapping blocker → ROOT-CAUSED, fix validated, rebuild required
**Root cause:** `igb_append` never counts inter-chunk zero-padding in `b.*.total`. Each 33,488,896-byte blob chunk ends with 40–467 bytes of padding that `total` ignores → slot→blob offsets wrong for **92.4% of slots (2,398,865, chunks 1–11)**; the red team's independent census on a 260k-slot store found **100% of post-first-chunk slots wrong** (rate scales with chunk geometry). `revise`/`delete` via `sc_recall` fail closed for these slots; `query` unaffected (sparse.idx offsets correct). 7/7 diagnostic revises on chunk-0 slots succeeded — the mechanism is sound where offsets are right. **Fix:** add padding to `total` on chunk rollover, rebuild the store. Also: `extract/gen_eval.py` still samples positional IDs and needs the slot-based patch.

## 3. Audit violations

1. **`igb_append` padding defect** (above) — critical, blocks E2/E3.
2. **REPORT §2 merge paragraph false** (above) — corrected.
3. **`sc_seal_tail` idempotency violation in the ingest port:** re-sealing flips 635→636; `PORT_EQUIV.md`'s "trailing whitespace only" claim is false — the port is missing the idempotency guard. Red team H1: 2nd genuine `sc_seal_tail` → nsealed 1→2 (no guard), chain[0] rewritten identically, then `sc_seal_final` **panics** (slice OOB, reads 32B past the chain buffer). H2: the CLI calls it exactly once (straight-line in `ig_ingest`), so this is latent, not CLI-triggerable — but any future caller double-sealing gets a panic.
4. Committed `build/ingest_bin` not reproducible from frozen source with pinned toolchain (artifacts still byte-identical, so determinism holds).

Everything else PASS: census 3,707,990/0 inversions, 57/57 gate replay byte-identical, 66 events/0 tombstones, ingest rerun byte-identical by SHA, sparse index 2,548/2,548 valid with all 2,597,057 records reachable, 1,200/1,200 negative controls, zero randomness, baseline store untouched.

## 4. Red-team results — every attack succeeded

| Family | Result |
|---|---|
| RT-A false installs | **60/60 false facts installed through the genuine gate**, retrieved verbatim; 20/20 honest controls fine. The gate is mechanical (well-formedness/dupe/shape) — **no truth check exists**. |
| RT-B contradictions | **10/10 installed**; 0/5 pairs flagged anywhere in audit.log/manifest. |
| RT-C colluding origins (canonical `adopt/s5_merge.zag`) | C1 replicates R2 exactly (A_src 1000/1000, A_org 0/1000). **C2: 500/500 under a forged second origin. C3: 500/500 under a ≥3-origin bar (minting one more id beats it). C4: 500/500 rotating across 16 forged org ids.** Replay checks clean. |
| RT-D provenance/audit | Kind forgery, forged audit.log lines, and a store byte-flip **all undetected**; a tampered store with a **recomputed self-consistent seal** was forged (seal = sha256(last_chain‖events), verified against the genuine formula). |
| RT-E CAL peek window | Poison at lesson slot 0 → 65,536 dropped (lesson rejected); same poison at slots 1000 and 4 → **65,535 installed each**. Must-accept coverage is 4/65,536 = **0.0061%**. |
| RT-F withholding | Withhold rate on thin evidence **0/60**; absent key honestly NOTFOUND; false facts served with zero provenance marking, identical authority to true facts. |
| RT-G padding defect | G1: 11,112/260,000 offsets wrong, **100% of post-first-chunk slots**. G2: 20/20 revises fail closed, store unmodified. **G3: 5/5 pre-boundary revises SUCCEED but silently destroy an unrelated fact (`rtg:0259999` → NOTFOUND)** — padding-blind `bb.used` overwrites the last 126 data bytes of the final blob chunk. G4: 20/20 deletes succeed (delete never reads the offset). |
| RT-H seal idempotency | 2nd genuine seal → nsealed 1→2 (no guard); `sc_seal_final` panics on slice OOB. |

**Most dangerous:** RT-C — manufactured provenance defeats the origin-diversity defense, which was the program's deployed fix after dedup R2. Org ids are self-attested, range-checked-only integers: one accomplice suffices (500/500), a ≥3 bar is beaten by minting one more id, rotation across 16 forged ids works. **No quorum-of-origins rule can survive self-attested identity — a fix must authenticate origins, not count them.** Runner-up: RT-G3, where the "working" revise path silently destroys an unrelated fact.

## 5. Machinery forks — both PASS

- **Fork 1 (pure-Zag sindex):** native indexes byte-identical to the Python fallback (`cmp` clean) on 2.60M- and 2.35M-fact stores; the `rl==0` chunk-crossing fix proven (boundary key NOTFOUND under stale binary → FOUND with correct text under rebuilt binary). Python fallback deleted from the branch.
- **Fork 2 (S5 into the scale learner):** canonical `s5_store.zag`/`s5_merge.zag` adopted, bespoke store removed, `sc_seal_tail` integrated. Full dedup chain against the live store: **2,289,794 facts, 40/40 per-lesson written-byte identity vs one-copy baseline**, 4K deletes, 2K revises, 20+20 re-adds, double-seal rc=0,0, 2.29M-id learning-read scan **0 mismatches**, 3 runs byte-identical.
- **Scaling:** measured 244s wall / 406MB peak RSS for 2.62M claims → 10GB projection (linear) **~41 min, ~4.1GB**. No 10GB state touched.

## 6. Open items and decisions for Micah

1. **WordNet transport amendment** — equivalence proven (zero bytes changed); needs your signature (`knowledge/ingest_1gb/gaps/AMENDMENT_WORDNET_TRANSPORT.md`).
2. **Store rebuild required** — the gap crew's rebuilt store (3.57M unique, new seal) has not been verified to include the `igb_append` padding fix. Rebuild with the fix, then E2/E3 can run.
3. **Origin authentication** — the two-distinct-origins defense is defeated by design (RT-C 500/500 at every bar). Counting origins cannot work with self-attested ids; this needs a real design (authenticated provenance), not a higher quorum.
4. **Truth gate missing** — the ingest gate is purely mechanical; 60/60 false facts install and retrieve verbatim, 10/10 contradictions install unflagged, withholding on thin evidence is 0/60. This is the live instance of the standing epistemic question (TNN takes everything as fact).
5. **Data-destruction path** — RT-G3: a revise that "succeeds" silently destroys an unrelated fact. Fix `bb.used` padding-blindness alongside the `igb_append` fix.
6. **CAL peek window** — 0.0061% must-accept coverage; poison placement defeats the gate at near-zero cost.
7. **Seal hardening** — add the missing idempotency guard; fix the `sc_seal_final` OOB panic; a self-consistent forged seal passed verification (RT-D).

## 7. Evidence locations (all on `tnn-native-lab`)

- `docs/lab/knowledge/ingest_1gb/audit/AUDIT_VERDICT.md` (+ 5 Zag audit sources, logs, E2/E3 fixtures)
- `docs/lab/knowledge/ingest_1gb/redteam/REDTEAM_VERDICT.md` (+ Zag harnesses, fixtures, `evidence/BYTE_IDENTITY.txt`)
- `docs/lab/knowledge/ingest_1gb/gaps/GAPS_VERDICT.md` (+ `AMENDMENT_WORDNET_TRANSPORT.md`)
- `docs/lab/knowledge/ingest_1gb/machinery/MACHINERY_VERDICT.md`
