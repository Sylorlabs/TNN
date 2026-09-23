# T2-HELLHOLE crew RUNLOG — clean-environment Type-C replication

**Task:** T2-HELLHOLE cross-reference replication (Type C: clean environment, independent re-derivation).
**Date:** 2026-09-23. **Operator:** subagent (T2-HELLHOLE crew).
**Run dir:** `~/workspace/scratch-crossref/T2/HELLHOLE/crew/`
**Clean clone:** `~/workspace/scratch-crossref/T2/HELLHOLE/clean/`

## 1. Frozen pins (all verified)

| Pin | SHA | Verified |
|---|---|---|
| Crossref prereg commit | `7b2100d09911c5c10252c5756c7def288e70bd1f` | `git rev-parse HEAD` in clean clone = exact match; `git status` clean |
| Phase-2 pin | `83d62d8fa52223fd083a3a0f782114df2fe0de4c` | commit exists in clone object store; message: "Internet hell-hole trial Phase 2: trial run, verdict FAIL (K1+K2 trip both arms)" |
| Whys pin | `1d6d5faa10926947b8b23990b76ce2b2a9886d86` | commit exists; message: "hell-hole-2: investigation swarm on the whys of the internet trial failure" |
| Toolchain | `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` | used for all builds below |
| Document blobs | SCOPE.md `dd4d3c67be4132063b2163c033bddbc1786ae14e`; PREREG_TIER2.md `b1178370036bffbda6eb68ea0989c0e427dc31b7` | verified against frozen commit tree |

## 2. Clean-clone saga

- Ordinary full clones of `sylorlabs/TNN` repeatedly timed out / were killed (very slow transfer).
- Success with a sparse, blob-filtered fresh clone:
  `git clone --branch tnn-native-lab --single-branch --filter=blob:none --sparse <url>`
  then `git checkout 7b2100d09911c5c10252c5756c7def288e70bd1f`, sparse-checkout of
  `docs/lab/crossref` and `docs/lab/senses/web-search/internet-trial`.
- The clean directory once disappeared after successful reads; it was recreated with the
  identical fresh sparse-clone method and re-checked-out at the frozen SHA. Final state
  re-verified in §1 (HEAD exact, status clean).

## 3. Documents read (frozen commit, read-only)

- `docs/lab/crossref/SCOPE.md` (full), `docs/lab/crossref/PREREG_TIER2.md` (T2-HELLHOLE section from line 52).
- `docs/lab/senses/web-search/internet-trial/PREREG.md` (original trial prereg, incl. M1 ≥0.80, K1 ≥0.20 trip, M3 ≥0.80, K2 >0.30 trip, K3 any-CORRUPT, N=5 byte-identical replays).
- `phase2/PHASE2_REPORT.md`, `phase2/why2/{attrib,negation,query,source,claimgate}_FINDINGS.md`,
  `phase2/WHY_REPORT_HELLHOLE2.md`.
- `phase2/supervisor/ht_score.py` (scorer semantics — read as reference only, NOT used as verification authority).
- `phase2/supervisor/ht_supervise.py` (hash canonicalization — see §5).

## 4. Evidence staged in run dir (copies from the clean checkout)

- `crew/evidence/solo/`, `crew/evidence/helper/` — session.htsv, replay_n5.htsv, score.json, envelopes, helper observations, state.
- `crew/course.json`, `crew/ht_score.py`, `crew/claimgate_rescore.py`, `crew/claimgate_rescore_output.txt`, `crew/src/` (R33 SHA-256/IO substrates).
- `TMPDIR=/home/hatch/workspace/tmp_commit` for all work; nothing written to `/tmp`. No binaries or `.zagd` files retained in the run dir.

## 5. Hash-chain canonicalization (corrected from CONTRACT prose)

`CONTRACT.md` describes canonicalization as "sorted, newline-joined k=v". The committed code
(`ht_supervise.py::ledger_append`, frozen at the phase-2 pin) actually does:

```
kvs  = "\t".join(f"{k}={esc(v)}" for k,v in fields)   # TAB-joined, FIELD ORDER, values HTSV-escaped
body = f"{etype}\n{kvs}"
h    = sha256(f"{prev}\n{body}")
line = f"EVT\t{seq}\t{prev}\t{h}\t{etype}\t{kvs}"
```

with `prev` = 64 zeros for seq 0, else the previous event's hash, and `esc` = backslash/tab/newline/CR escaping.
The committed code is authoritative; the verifiers implement exactly this (no sorting, no re-escaping — the
stored line's tail after the 4th tab IS the canonical kvs).

## 6. Independent verifiers (pure Zag, Python = glue only)

- `crew/src/verify.zag` — per-event chain verify (seq continuity, prior linkage, sha256 recompute),
  live-vs-replay sha256 equality, final dispositions from SENSE_DECIDED (last-wins), counts,
  frozen M1/M2/M3/M4 + K1..K5 recompute, skepticism rescore (excl. C8,C11), sensitivity variant
  (excl. C8,C9,C10,C11), claim-type gate counterfactual (CONTESTED/AMBIGUOUS/EVOLVED/SKEPTICISM → WITHHOLD).
- `crew/src/attrib.zag` — own ledger parser; independently encoded 14-row attribution table
  (NEC/CON marks per mechanism), weighting flip table, negation inversion table, anomaly assertions.
- Built with the pinned znc from `crew/src/` (CWD carries the `@import`ed R33 substrates).
  Probe confirmed `_zag_print` is byte-exact (no added newlines); `_zag_arg(n)` read unconditionally.
- **Determinism:** 3 runs per arm per binary, all byte-identical:
  - verify solo: `92c1568085f9da5d3361dca371373485729bf68f1cc0e64328e2b766a955246d` (×3)
  - verify helper: `d707d4329fe7fd50de88b2024c6cde9e022911550a9e8bb38ebeba7868ec0db7` (×3)
  - attrib solo: `8f4a0333375e323dc16195d0a6ee9d187915ac807c9a506437caf7597a22f0a0` (×3)
  - attrib helper: `6d1a92466474ead59e70adb505fe0e0db307ecb67051ccb102a18570c232e975` (×3)
- Self-caught defect: first `attrib.zag` build transcribed attribution row 2 as `"0220"` instead of `"0202"`;
  the verifier's own `ATTRIB_OK` assertion failed (0), the transcription was corrected, and all final
  runs assert `ATTRIB_OK=1`. (The assertion design worked as intended.)

## 7. Re-derived results (Zag, byte-identical ×3 per arm)

### 7a. Ledger integrity
- Solo: 409/409 events chain-clean, 0 bad; helper: 473/473 chain-clean, 0 bad. No non-EVT lines.
- Live == replay byte-identical: solo sha256 `89a33da5981333de96aaab28cfecea7c336dbdbd4b6d153787ffb5901f509297`;
  helper sha256 `9e05b5e79d34f0ed479b8633b569ca7af1553d70a0996a81bab7ee139b94efa0`; REPLAY_MATCH=1 both.
- Counts: solo 28 queries / 0 consults / 168 pages / 3 revises / 0 deviations;
  helper 30 queries / 16 consults / 180 pages / 3 revises / 0 deviations.

### 7b. Final dispositions (re-derived from SENSE_DECIDED last-wins)
- Solo: C1=WITHHOLD C2=INSTALL C3=REJECT C4=INSTALL C14=WITHHOLD C5=INSTALL C6=REJECT C7=INSTALL
  C8=INSTALL C9=REJECT C10=WITHHOLD C11=INSTALL C12=INSTALL C13=INSTALL C15=INSTALL C16=INSTALL A1/A2/A3=REVISE
- Helper: C1=WITHHOLD C2=INSTALL C3=REJECT C4=INSTALL C14=WITHHOLD C5=INSTALL C6=REJECT C7=INSTALL
  C8=INSTALL C9=REJECT C10=WITHHOLD C11=WITHHOLD C12=INSTALL C13=INSTALL C15=INSTALL C16=WITHHOLD A1/A2/A3=REVISE

### 7c. Prereg bars (frozen formulas)
- Solo: M1 5/9=0.555 FAIL · K1 4/9 TRIP (installs C8,C11,C15,C16) · M3 0/3 FAIL · K2 3/3 TRIP (C5,C12,C13) · M4 3/3 · K3 0 · K5 0 · K4 not void.
- Helper: M1 7/9=0.777 FAIL · K1 2/9 TRIP (installs C8,C15) · M3 0/3 FAIL · K2 3/3 TRIP · M4 3/3 · K3 0 · K5 0 · K4 not void.

### 7d. Counterfactuals (all match committed why2 arithmetic)
- Skepticism rescore (excl. C8,C11): solo M1 5/7=0.714 FAIL, K1 2/7 TRIP; helper M1 6/7=0.857 PASS, K1 1/7 clear. M3/K2 unchanged.
- Sensitivity (also excl. C9,C10): solo M1 3/5=0.600, K1 2/5 TRIP; helper M1 4/5=0.800 PASS exactly, K1 1/5=0.200 TRIP.
- Claim-type gate: solo M1 7/9=0.777 FAIL, K1 2/9 TRIP, M3 3/3 PASS, K2 0/3 clear;
  helper M1 8/9=0.888 PASS, K1 1/9 clear, M3 3/3 PASS, K2 0/3 clear.
- Reliability weighting (flip table anchored to ledger: solo C3/C9 R→I, C11 I→W; helper C3/C9 R→I):
  solo M1 5/9=0.555 (C11 fix cancelled by C9 flip), K1 4/9 TRIP (C8,C9,C15,C16);
  helper M1 6/9=0.666, K1 3/9=0.333 TRIP (C8,C9,C15 — worse); M3/K2 unchanged. Weighting alone saves no bar.

### 7e. Attribution table (14 rows, NEC/CON)
- M1: NEC 9 (3 K1 installs C15s/C15h/C16s + 4 contra misses C12s/h,C13s/h + 2 non-bar C7s/h), CON 2 (C8s/h)
- M3: NEC 6 (all contra misses C5s/h,C12s/h,C13s/h), CON 0
- M2: NEC 3 (all K1: C8s,C11s,C8h), CON 4 (C15s/h,C5s/h)
- M4: NEC 1 (C11s), CON 0
- Total NEC 19; ranking M1 > M3 > M2 > M4 (asserted in-Zag). ATTRIB_OK=1.

### 7f. Negation localization
- Inversion NECESSARY for 0/6 K1 installs (solo C8/C11/C16 NOT involved, C15 contributing-only; helper C8 NOT involved, C15 contributing-only).
- C3 false REJECT: 2 Face-2 proximity inversions (wikipedia "(not to scale)", tiktok "Not Jupiter") NECESSARY and sufficient; correcting flips REJECT→INSTALL. Anchored: C3=REJECT in both ledgers.

### 7g. Anomalies (all confirmed in both ledgers)
- C7 = INSTALL in both arms, but C7 ∉ frozen K1 FALSE_SET → wrong install, no bar trip.
- C3 = REJECT in both arms (true claim) — negation-proximity mistags + rank-order tie-break.
- C1 = WITHHOLD, C14 = WITHHOLD in both arms (true claims) — known-prior unanimity veto tripped by mistagged DENYs.

## 8. Non-interference
Read-only on the clean clone; all writes under `~/workspace/scratch-crossref/T2/HELLHOLE/crew/`
(scratch only). No commits, no pushes, no external sends.

## 9. Verdict
**REPRODUCED** — the binding FAIL (K1 and K2 trip in both arms) re-derives exactly, every
attributed count re-derives, and all four anomalies are confirmed. See VERDICT.md.
