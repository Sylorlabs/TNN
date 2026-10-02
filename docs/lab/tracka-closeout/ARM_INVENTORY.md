# Track A — Arm Inventory Closeout (ARM INVENTORY CREW)

Date: 2026-09-21. Frozen source: `units/PREREG_FREEZE.md` §3 (extracted
programmatically; the frozen file's own "53 arms" footer is an arithmetic
error — §3 contains **52** frozen arms; Y2 is unfrozen and excluded).

## Counts

| Status | Count | Arms |
|---|---|---|
| KILLED | 15 | B-8, E, G1, G2, H2, I2, J1, J2, M, Q, R, R2, Y1, Z4, Z5 |
| PASS | 16 | A, B-16, C-P, C-W, F-S, H1, K2, L1, L2, N, S, X, Y3, Y5, Y6, Z6 |
| PROVISIONAL | 10 | D, D-T, D-R, F-B, I1, K3, O, U, Y4, Z1 |
| MISSING (no verdict/death certificate) | 11 | B-64, K1, M2, P, T, V, W, Z2, Z3, Z7, Z8 |

**52 arms inventoried. 41 verdict/death-certificate files found. 11 arms have
no verdict file.**

Status normalization: explicit killed/retired/dead → KILLED; explicit
pass/survives with completed binding adjudication → PASS; blocked,
incomplete, in-progress, conditional, partial, or otherwise unresolved →
PROVISIONAL; no verdict/death-certificate file → MISSING.

M8 honesty rule: M8 is reported as stated by each verdict. `NOT RUN`,
`INCOMPLETE`, `PENDING`, `FAIL`, and `NOT STATED` are reported as-is and are
**not** conflated with `FAIL—DISQUALIFIED`.

## Machine-readable table

Columns: `arm | verdict | kill_criterion_fired | m8 | legs | verdict_path`.
(`verdict_commit` follows in the per-arm notes where stated.)

```
arm  | verdict     | kill_criterion_fired | m8         | legs            | verdict_path
A    | PASS        | no                   | PASS       | 1x              | A/VERDICT.md
B-8  | KILLED      | yes                  | PASS       | 1x              | B-8/docs/RETIREMENT.md
B-16 | PASS        | no                   | PASS       | 1x              | B-16/VERDICT.md
B-64 | MISSING     | n/a                  | n/a        | none            | —
C-W  | PASS        | no                   | PASS       | 1x              | C-W/VERDICT.md
C-P  | PASS        | no                   | PASS       | 1x              | C-P/VERDICT.md
D    | PROVISIONAL | unresolved           | NOT RUN    | partial 1x      | D/VERDICT.md (DRAFT)
D-T  | PROVISIONAL | pending              | NOT RUN    | partial 1x      | D-T/VERDICT.md
D-R  | PROVISIONAL | not evaluated        | NOT RUN    | sub-1x          | D-R/docs/VERDICT.md
E    | KILLED      | yes                  | PASS       | 1x+10x           | E/VERDICT.md
F-S  | PASS        | no                   | PASS       | 1x              | F-S/docs/VERDICT.md
F-B  | PROVISIONAL | unresolved           | NOT RUN    | partial (M1)    | F-B/VERDICT.md
G1   | KILLED      | yes                  | NOT STATED | 1x              | G1/DEATH_CERTIFICATE.md
G2   | KILLED      | yes                  | PASS       | 1x              | G2/VERDICT.md
H1   | PASS        | no                   | PASS       | 1x              | H1/VERDICT.md
H2   | KILLED      | yes                  | NOT STATED | 1x              | H2/VERDICT.md
I1   | PROVISIONAL | unresolved           | INCOMPLETE | partial 1x      | I1/VERDICT.md
I2   | KILLED      | yes                  | NOT STATED | 1x              | I2/VERDICT.md
J1   | KILLED      | yes                  | NOT RUN    | 1x              | J1/DEATH_CERTIFICATE.md
J2   | KILLED      | yes                  | NOT RUN    | 1x (mechanism)  | J2/DEATH_CERTIFICATE.md
K1   | MISSING     | n/a                  | n/a        | M1 only         | —
K2   | PASS        | no                   | PASS       | 1x              | K2/VERDICT.md
K3   | PROVISIONAL | unresolved           | NOT ATTEMPTED | incomplete 1x | K3/docs/lab/units/arms/K3/VERDICT.md
L1   | PASS        | no                   | PASS       | 1x              | L1/VERDICT.md
L2   | PASS        | no                   | PASS       | 1x              | L2/VERDICT.md
M    | KILLED      | yes (scoped)         | PASS       | 1x              | M/VERDICT.md
M2   | MISSING     | kill evidenced        | n/a        | 10x (K2 leg)    | — (commit_msg_final.txt claims KILLED)
N    | PASS        | no                   | PASS       | 1x              | N/VERDICT.md
O    | PROVISIONAL | unresolved           | PENDING    | partial 1x      | O/VERDICT.md
P    | MISSING     | n/a                  | n/a        | partial         | —
Q    | KILLED      | yes                  | PASS       | 1x              | q/VERDICT.md
R    | KILLED      | yes                  | PASS       | 1x              | R/VERDICT.md
R2   | KILLED      | yes                  | PASS       | 1x              | R2/VERDICT.md
S    | PASS        | no                   | PASS       | 1x              | S/VERDICT.md
T    | MISSING     | (iii) not fired      | PASS*      | m8_10x logs     | — (commit_msg.txt claims PASS)
U    | PROVISIONAL | no                   | PASS       | 1x provisional  | U/VERDICT.md
V    | MISSING     | n/a                  | n/a        | barely started  | —
W    | MISSING     | n/a                  | n/a        | partial         | —
X    | PASS        | no                   | PASS       | 1x              | X/VERDICT.md
Y1   | KILLED      | yes                  | PASS       | 1x              | Y1/VERDICT.md
Y3   | PASS        | no                   | PASS       | 1x              | Y3/evidence/VERDICT.md
Y4   | PROVISIONAL | unresolved           | PASS       | 1x              | Y4/VERDICT.md
Y5   | PASS        | no                   | PASS       | 1x              | Y5/VERDICT.md
Y6   | PASS        | no                   | PASS       | 1x              | Y6/VERDICT.md
Z1   | PROVISIONAL | unresolved           | PASS       | 1x              | Z1/VERDICT.md
Z2   | MISSING     | n/a                  | n/a        | 1x scorecards   | —
Z3   | MISSING     | n/a                  | n/a        | barely started  | —
Z4   | KILLED      | yes                  | FAIL       | partial 1x      | Z4/DEATH_CERTIFICATE.md
Z5   | KILLED      | yes                  | FAIL       | 1x              | Z5/VERDICT.md
Z6   | PASS        | no                   | PASS       | 1x              | Z6/VERDICT.md
Z7   | MISSING     | n/a                  | PASS*      | 1x full battery | — (BATTERY_STATUS.md, no verdict)
Z8   | MISSING     | n/a                  | n/a        | battery_1x.sh   | —
```

`*` T's M8 PASS and Z7's M8GATE PASS come from work artifacts
(`T/work/m8_10x_*.txt`, `Z7/evidence/r1/BATTERY_STATUS.md`), not from a
verdict file.

## Per-arm notes (frozen kill criterion quoted; verdict commit where stated)

Frozen criteria below are the programmatic §3 extraction (whitespace
normalized). Quote-verbatim analysis was done by scripted diff
(`/tmp/quote_diff.py`, results `/tmp/quote_diff.json`): each verdict's
criterion quote was regex/anchor-extracted from its file and compared
against the frozen cell after markdown-formatting normalization only.

### A — PASS
- Frozen: "A retires as candidate only if B-64 strictly dominates it on M1,
  M2, and retrieval-op count on both corpora at 10x. (A-44)"
- Verdict quotes a shortened paraphrase ("Retire A only if B-64 strictly
  dominates it on M1, M2, and retrieval-op count on both corpora at 10x."),
  mislabeled "frozen §7". **Non-verbatim.**
- Kill did not fire. M8 PASS. 1x legs. Verdict commit `4617842c5b71`
  (docs commit `7d29e5fe725e`).

### B-8 — KILLED (retired at size level)
- Frozen: "A size retires when another B size strictly dominates it on
  M1/M2/M3 both corpora. B as a family is killed as contender the moment
  any smart arm beats the best B size by ≥2x on M3 at equal-or-better M1."
- Verdict (`docs/RETIREMENT.md`, the arm's death certificate) quotes the
  size-retirement clause verbatim but omits the family-kill clause.
  **Partial quote.**
- Fired: B-16 strictly dominates B-8 on M3 (100.0/100.0/CLEAR vs
  100.0/67.6/FROZEN-UNDER-PRESSURE) with M1/M2 tied at ceiling. M8GATE
  PASS. 1x legs. Prereg commit `b0b9140c0eda`.

### B-16 — PASS
- Frozen: same B-family row as B-8.
- Verdict paraphrases the retirement rule; does not quote verbatim.
  **Non-verbatim.**
- Neither retirement nor family-kill fired (B-64 ties B-16; no smart arm
  ≥2x on M3). M8 PASS. 1x legs. Verdict commit
  `9e4a0aff4f1768e29bf38c8fd8dd251f5dab89e2`.

### B-64 — MISSING
- Harness validator build at `units/arms/harness/b64/`. No verdict or
  death certificate found. Build dirs `cl/`, `substrate/`, `work/` only.
- No scorecards copied (none exist).

### C-W — PASS
- Frozen: "A variant retires if a smart arm beats it ≥2x on M3 and M2 at
  equal M1 both corpora. If no smart arm beats C-W on Shakespeare by end
  of 10x, every smart arm is killed. (C-28)"
- Verdict paraphrases the cross-arm criterion. **Non-verbatim.**
- No smart arm beat C-W; kill did not fire. M8 PASS. 1x legs. No commit
  stated.

### C-P — PASS
- Frozen: same C-family row as C-W.
- Verdict quotes two paraphrased sentences ("A variant retires if a smart
  arm beats it ≥2x on M3 and M2 at equal M1 both corpora." /
  "If no smart arm beats C-W on Shakespeare by end of 10x, every smart
  arm is killed."). **Non-verbatim.**
- Kill did not fire. M8 PASS. 1x legs. Verdict commit
  `d57ef6f0ae6da9fc97a2779ee8031f23f3bfb448`.

### D — PROVISIONAL (verdict is a DRAFT)
- Frozen: "Stored bytes per recall ≥ B-64 on both corpora at 10x. Churn
  > 0.30 at 10x. M1 < B-64 at equal memory budget."
- Draft lists three paraphrased criteria. **Non-verbatim.**
- Kill unresolved; 10x legs incomplete; M8 not run. No commit stated.

### D-T — PROVISIONAL
- Frozen: "≥50% of taught seed chunks are revised/killed by end of
  curriculum AND untaught D matches D-T on M1/M2/M3 — teaching adds
  nothing measurable."
- Verdict blockquote is close but rewords ("untaught D" phrasing) and
  drops exact frozen wording. **Non-verbatim.**
- Compound kill pending (needs untaught-D comparison at 10x); M8 NOT RUN;
  partial 1x. Verdict commit `4d346f0ae44ffcdbf2c0086fbd9bf2df5438e587`.

### D-R — PROVISIONAL (BLOCKED)
- Frozen: ">50% uncommitted at 10x while D commits and wins on M3."
- Verdict paraphrases (">50% uncommitted at 10x while D commits and wins
  on M3" is close but presented as paraphrase, not quote).
  **Non-verbatim.**
- Blocked: D's 10x never ran, so the comparator is missing; kill not
  evaluated; M8 not run; sub-1x fixture only. No commit stated.

### E — KILLED
- Frozen: "Stored-bytes-per-recall ≥ 2× B-64's at equal M1 on either
  corpus at 10x (copies-only strictly dominated by the dumbest persistent
  segmentation). **Expected to die informatively; its death certificate
  reads \"references matter, transient segmentation does not.\"**"
- Verdict quotes the binding criterion verbatim but omits the frozen
  cell's trailing bold sentence. **Partial quote** (verdict claims
  verbatim).
- Fired: 2.764× ≥ 2× at 10x, equal M1. M8 PASS. 1x + 10x kill-comparison
  legs. Verdict commits `4ce17ac…` (+ path fix `33dcc60…`).

### F-S — PASS
- Frozen: "F1-agreement with C-W on Shakespeare outside ±0.05 while reuse
  is no better than C-W's — the triage adds nothing; OR code cut count >
  5× C-W's (structure-hostile over-segmentation); OR loses to arm D on
  crew-local reuse M3 both corpora."
- Verdict lists three paraphrased "Kill N" criteria. **Non-verbatim.**
- No kill fired. M8 PASS. 1x legs. No commit stated.

### F-B — PROVISIONAL
- Frozen: "M3 < C-W's both corpora; OR within noise of F-S on all metrics
  both corpora."
- Verdict quotes a paraphrase ("M3 < C-W's both corpora; OR within noise
  of F-S on all metrics both corpora."). **Non-verbatim.**
- Blocked on arm-C/D comparators; kill unresolved; M8 not run; partial M1
  only. No commit stated.

### G1 — KILLED
- Frozen: "Recall-quality advantage over G2's deliberative superchunks at
  matched occupancy < 2 absolute points on byte-exact recall — deliberation
  buys nothing; OR deliberation cost per pressure event > 50× G2's sweep
  with no quality advantage; OR ≥ 10% of superchunks are never recalled
  nor re-split (dead weight created by triage) — G1 dies."
- Death certificate quotes only criterion (iii), paraphrased ("if ≥ 10%
  of superchunks are never recalled *nor* re-split (dead weight created by
  triage) → G1 dies."). **Partial + paraphrased.**
- Fired: 100% of superchunks untouched (≥10% bar). M8 not stated. 1x M3
  leg; no 10x. No commit stated.

### G2 — KILLED
- Frozen: "Recall-quality advantage over G1 at matched occupancy < 2
  absolute points on byte-exact recall, OR deliberation cost per pressure
  event > 50× G1's sweep with no quality advantage — deliberation buys
  nothing."
- Verdict blockquote matches the frozen cell exactly (modulo markdown
  line-wrapping). **Verbatim.**
- Fired: 0.0-point advantage (< 2 required). M8GATE PASS (per
  `evidence/m8-gate.summary.txt`; not summarized in verdict). 1x legs; no
  10x. No commit stated.

### H1 — PASS
- Frozen: "Reuse hit rate ≤ fixed-64B baseline + 10pp — deliberation buys
  nothing; OR refusal > 30% AND mean delib ops/cut > 10^4 — too expensive
  to run; OR BAR ±10% sensitivity flips > 25% — the quality is an artifact
  of the bar."
- Verdict lists three paraphrased criteria. **Non-verbatim.**
- No kill fired. M8 PASS. 1x legs. No commit stated.

### H2 — KILLED
- Frozen: "Per-window deliberation cost > 50× the C-W fixed-64B sweep with
  no recall advantage — deliberation buys nothing; OR fallback rate on
  corpus B > 40% of windows — the budget destroys the deliberation."
- Verdict quotes only the fallback-rate disjunct verbatim. **Partial
  quote.**
- Fired: 99.9% fallback on corpus B (> 40%). M8 status not cleanly stated
  in verdict (table points to `M8-REPORT.md`). 1x legs; no 10x. No commit
  stated.

### I1 — PROVISIONAL
- Frozen: "L2+ superchunk recall <5% vs flat comparator — hierarchy adds
  nothing; OR maintenance + stale rebuild >20% of audit ops (per corpus)
  — hierarchy costs too much to maintain; OR L1 boundary agreement <50%
  with natural breaks — superchunks are arbitrary."
- Verdict lists three paraphrased "Kill (i/ii/iii)" criteria.
  **Non-verbatim.**
- Kill unresolved (10x legs incomplete); M8 INCOMPLETE (timeouts); partial
  1x. No commit stated.

### I2 — KILLED
- Frozen: "Record savings over I1 < 10%, OR parent-arbitration error >
  10% — I2 dies, I1 remains the hierarchy candidate."
- Verdict contains the full criterion verbatim (in the assignment
  section) plus a verbatim quote of the fired disjunct. **Verbatim.**
- Fired: 55.9% parent-arbitration error (> 10%). M8 not cleanly stated
  (scorecard referenced). 1x legs. No commit hash stated.

### J1 — KILLED
- Frozen: "Best-of-k does not beat best single tiling by > 2 points at
  equal total budget on adversarial-cut corpus — tilings were never
  needed."
- Death certificate quotes a paraphrase ("Best-of-k ≤ best single tiling
  + 2 points at equal total budget on adversarial-cut corpus.").
  **Non-verbatim.**
- Fired: +1.8/+1.7 points, at or below the +2 bar. M8 not run (no M8 in
  certificate). 1x legs; no 10x. Verdict commit
  `4f89788a2aa40c08ad29d0ee4b2b4e11b2121881`.
- Note: `J1/DEATH_CERTIFICATE.md` is canonical; a `J1/VERDICT.md` also
  exists.

### J2 — KILLED
- Frozen: "k does not converge (birth→death→birth for the same phase
  twice on one corpus pass), OR converges to 1 on all corpora — tilings
  were never needed; J1 dies with it."
- Death certificate blockquote matches the frozen cell exactly.
  **Verbatim.**
- Fired: k converged to 1 on all corpora. M8 NOT RUN. Mechanism-level 1x
  adjudication; no 10x. Only prereg commit `b0b9140c0eda` stated.
- Note: `J2/DEATH_CERTIFICATE.md` is canonical; a `J2/VERDICT.md` also
  exists.

### K1 — MISSING
- Built (`cl/`, `substrate/`, `work/` with M1 legs in `work/runs/`,
  `BUILD_LOG.md`). No verdict or death certificate found.
- No scorecards copied (none exist).

### K2 — PASS
- Frozen: "Bidirectional: if K2's dedup savings within 2 pts of K1's AND
  per-add cost lower → K1 dies on cost grounds (keep K2). If chain lengths
  exceed 4 on any corpus run → K2 dies (64 bits too small for the store's
  lifetime)."
- Verdict quotes the criterion body verbatim but drops the frozen
  "Bidirectional:" label. **Verbatim modulo label.**
- Neither direction fired. M8 PASS. 1x legs. No commit stated.

### K3 — PROVISIONAL
- Frozen: "K3 does not beat both pure schemes on at least 3/5 bake-off
  metrics — the hybrid buys nothing."
- Verdict paraphrases the promotion rule ("if K3 beats both pure schemes
  on at least 3/5 bake-off metrics → K3 becomes substrate; if K3 loses,
  it dies."). **Non-verbatim.**
- Bake-off unresolved; M8 NOT ATTEMPTED; incomplete 1x. Work
  uncommitted; only the frozen prereg hash stated.
- Note: verdict lives at nested path
  `K3/docs/lab/units/arms/K3/VERDICT.md` (committed-tree layout).

### L1 — PASS
- Frozen: "Store cost >3× K1 on corpus A with no recall-accuracy advantage
  — positions cost too much; OR any revision batch changes an existing
  position ID — dies outright; OR mean segments touched per sequential
  recall >4 on corpus C — positions fragment access."
- Verdict lists three paraphrased "(i)/(ii)/(iii)" criteria.
  **Non-verbatim.**
- No kill fired. M8 PASS. 1x legs. Verdict commit
  `ac6c1442b39f522ef27bb6b7d26b0edd72594953`.

### L2 — PASS
- Frozen: "Any within-epoch ID change (same bar as L1), OR translation
  misses > 1% of cross-epoch recalls — the translation layer is lossy."
- Verdict quotes the first disjunct verbatim but drops the trailing
  clause. **Partial quote.**
- No kill fired. M8 PASS. 1x legs. Verdict commit
  `532c823437cb1cdb82774b764a26435f81a9bcc2`.

### M — KILLED (scoped: cross-store/global identity only)
- Frozen: "Scoped: KILL counter IDs as the cross-store/global identity if,
  in the two-TNN merge trial, remapping produces ≥1 dangling/misdirected
  pointer OR remap compute > 10% of total merge compute. (Survives
  unconditionally as the store-local handle.) Separately: the M-dedup
  claim dies (revert to pure issuance) if M7 dedup ratio < 0.4 on the
  repetition protocol."
- Verdict quotes both scoped kills near-verbatim, minus the frozen
  "Scoped:" label. **Verbatim modulo label.**
- Fired: remap compute 39.14% (> 10%). Local handles survive
  unconditionally. M8 PASS. 1x legs; no 10x. No commits ("No commits
  yet").
- Note: `M/docs/VERDICT.md` is byte-identical duplicate of
  `M/VERDICT.md`.

### M2 — MISSING (kill evidenced, verdict file absent)
- No `VERDICT.md`/`DEATH_CERTIFICATE.md` in the tree.
- `commit_msg_final.txt` describes a KILLED verdict ("K2 FIRES, M2 is
  KILLED") and claims the verdict files were updated with 10x evidence —
  but the files are not present. 10x K2 measurement exists
  (`k2_10x/`: 28.8%/26.8% > 10% bar → K2 disjunct of the frozen criterion
  "Single-byte leaf edit invalidates > 25% of cached compositions in the
  recall benchmark, OR ID recomputation > 10% of recall latency on the 10x
  run" fires on the evidence).
- Status is MISSING because no verdict file exists; the kill is evidenced
  but not certified in-file.

### N — PASS
- Frozen: "Full beats judgment-free control by ≥5pp on adversarial
  misleading-memory bar — judgment adds nothing; OR ablation within 2
  points of full — the judgment is decorative; OR >10% chunks flip sign
  >2× in 100-episode window — unstable."
- Verdict lists three paraphrased "(i)/(ii)/(iii)" criteria.
  **Non-verbatim.**
- No kill fired. M8 PASS. 1x legs (10x attempted, blocked by tool
  limits). No commit stated.

### O — PROVISIONAL
- Frozen: "Acceleration vs emergent-only P < 2× on the standard ingress
  curriculum — teaching buys nothing; OR disconnect test fails (post-
  disconnect recall < 95% of connected) — not actually learned; OR
  red-team ingress succeeds (planted false memory survives 100 episodes) —
  gullible; OR BPE-smuggling tripwire fires — the teacher channel is
  compromised."
- Verdict lists four paraphrased "(i)–(iv)" criteria. **Non-verbatim.**
- Comparator/battery incomplete (P arm missing); kill unresolved; M8
  PENDING; partial 1x. Commit placeholder only.

### P — MISSING
- `cl/`, `substrate/`, `work/` (bins, logs), `logs/`. `work/m3_out.txt`
  shows an M3 run; `work/err.txt` shows a panic ("slice index out of
  bounds"). No verdict or death certificate found.
- No scorecards copied (none exist).

### Q — KILLED
- Frozen: "Hybrid does not beat max(taught-only, emergent-only) + 3
  points on the standard curriculum — the hybrid buys nothing; OR
  collision resolution kills >10% of entries per W episodes — the store
  cannot hold both; OR adversarial score < emergent-only — the teacher
  channel is a vulnerability."
- Verdict paraphrases all three criteria ("Hybrid must beat
  max(taught-only, emergent-only) + 3 points", etc.).
  **Non-verbatim.** Additionally the verdict substitutes an internal
  taught-only/emergent-only ablation for the frozen O/P comparators (O/P
  never reported) — a comparator substitution, flagged openly in the
  verdict.
- Fired: hybrid tied taught-only internally (0-point margin vs +3 bar).
  M8 PASS. 1x legs; no 10x. No commit stated.

### R — KILLED
- Frozen: "Boundary F1 (vs whitespace/punctuation joints AND vs arm O's
  taught spans, separately) does not beat the fixed-64-byte baseline by
  ≥10 points on both corpora; OR held-out recall (M1) with R-cuts does not
  beat the 64-byte baseline. Note C9: ..."
- Verdict quotes the criterion proper verbatim but omits the frozen Note
  C9. **Partial quote.**
- Fired: 100%-vs-100% held-out recall ceiling tie (no beat of baseline).
  M8 PASS. 1x legs; no 10x. Evidence commit `76849610b8` referenced.

### R2 — KILLED
- Frozen kill cell: "Verified-boundary recall (M1) on held-out probes
  does not beat arm R by ≥3 points (receipts don't buy recall at 10×
  compute); OR proposals-per-accepted-cut does not fall over the corpus —
  core claim fails."
- Verdict quotes the entire frozen table row, which contains the kill
  cell verbatim (plus row context and the A-37 merge-decision note).
  **Criterion verbatim within full-row quote.**
- Fired: 0-point margin vs R (< 3 required). M8 PASS. 1x legs; no 10x.
  No commit stated.

### S — PASS
- Frozen: "Post-warmup B4 < 1.5× V's on either corpus — no win; OR
  merge-then-split churn > 25% of all merges — unstable; OR determinism
  gate fails — nondeterministic; OR universal floor rule fires."
- Verdict lists four paraphrased numbered criteria. **Non-verbatim.**
- No kill fired. M8 PASS. 1x legs. Commit placeholder only.

### T — MISSING (verdict claimed in commit message, file absent)
- No `VERDICT.md`/`DEATH_CERTIFICATE.md` in the tree.
- `commit_msg.txt` claims "ARM T: Episode-aligned chunks — PASS" with
  M1–M8 results (M8 10x byte-identical) and notes kill criteria
  (i),(ii),(iv) unresolved, (iii) not fired. `work/` contains
  `m8_10x_*.txt` logs. The claim is uncertified in-file → MISSING.
- No scorecards copied (none exist).

### U — PROVISIONAL
- Frozen: "CPU >10× D and B4 <10% — the index costs more than it saves; OR
  D-with-invalidation beats U on total cost at 100 edits — invalidation
  was enough; OR determinism fails."
- Verdict lists three paraphrased numbered criteria. **Non-verbatim.**
- No provisional kill fired; M8 PASS (provisional); 1x provisional legs.
  No commit stated.

### V — MISSING
- `cl/`, `substrate/`, `work/` (only `b64_test_bin`). Barely started. No
  verdict found. No scorecards.

### W — MISSING
- `cl/`, `substrate/`, `work/` (harness, m1/m8 artifacts, `w_bin`),
  `ledger.bin`. Partial progress. No verdict found. No scorecards.

### X — PASS
- Frozen: "Floor bars (A-44): retired as candidate only if B2 ≥10× AND B5
  ≥10× (crew-4 battery)."
- Verdict blockquotes the frozen criterion verbatim, then appends extra
  sentences (universal floor rule text, death-certificate instruction)
  not present in the frozen cell. **Verbatim core + embellishment.**
- Floor bars not fired. M8 PASS. 1x legs. No commit stated.

### Y1 — KILLED
- Frozen: "Over 10,000 cuts, negotiated boundaries show ≤10% better
  recall-stability than arm-D unilateral cuts at the same granularity; OR
  veto rate collapses to <1% within the first 1,000 cuts (lazy agreement
  — then Y1 ≡ D with extra ledger cost)."
- Verdict blockquote matches the frozen cell exactly. **Verbatim.**
- Fired: 0% stability improvement (≤10% bar). M8 PASS. 1x legs; no 10x.
  No commit stated.

### Y3 — PASS
- Frozen: "Mean lineage depth > 50 on the standard revision curriculum
  (fragmentation, not versioning); OR any recall resolving to a
  tombstoned span (dangling reference observed) — kill and fix before any
  further claim."
- Verdict quotes the criterion with only the leading letter lowercased
  ("mean lineage depth..."). **Verbatim modulo leading-letter case.**
- No kill fired. M8 PASS. 1x legs. No commit stated.
- Note: verdict lives at nested path `Y3/evidence/VERDICT.md`.

### Y4 — PROVISIONAL (conditional on arm D)
- Frozen: "Recall accuracy >5% below eager arm D at equal total ledger
  cost (candidates + materializations); OR >30% of materialized chunks
  never recalled twice — lazy materialization is just deferred eager."
- Verdict quotes the two disjuncts separately (each verbatim as a
  substring) but not as one contiguous cell. **Verbatim disjuncts, split.**
- Kill unresolved: clause (a) UNSCORED — arm D never reported M1/ledger
  cost. M8 PASS. 1x legs. Verdict commit
  `7998f9d568a02fbffc7886ceb50c4071e7a48b0a`.

### Y5 — PASS
- Frozen: ">20% of Y5 units on sqlite3.c degrade to single spans within
  the revision curriculum (links die faster than they pay); OR any kill
  leaves a live span pointing at a dead LINK (atomicity broken — kill the
  implementation)."
- Verdict splits into two clause quotes; Clause 1 drops the frozen
  parenthetical "(links die faster than they pay)". **Partial
  (parenthetical dropped).**
- No kill fired (0.0% degradation). M8 PASS. 1x legs (10x blocked).
  Verdict commit `0f07518d0937`.
- Note: draft at `Y5/.work/VERDICT_draft.md` is superseded by
  `Y5/VERDICT.md`.

### Y6 — PASS
- Frozen: "Ledger write volume > 10× arm D on the same curriculum
  (refcount writes dominate — kill or move to batched REF accounting,
  which weakens provability and must be re-preregistered); OR any checker
  audit finds a live reference to a tombstoned ID."
- Verdict blockquote matches the frozen cell exactly. **Verbatim.**
- No kill fired. M8 PASS. 1x legs; no 10x. No commit stated.

### Z1 — PROVISIONAL (blocked on arm D)
- Frozen: "Regretted-cut rate not ≥50% lower than arm D on the revision
  curriculum — the window buys nothing; OR challenge-set revision
  invalidates >10% of live witnesses — binding too brittle (kill the
  binding, keep the window)."
- Verdict quotes the criterion with only the leading letter lowercased
  ("regretted-cut rate..."). **Verbatim modulo leading-letter case.**
- Kill unresolved: clause (a) needs arm-D baseline, which never
  reported. M8 PASS. 1x legs. No commit stated.

### Z2 — MISSING
- `cl/`, `docs/` (BUILD_NOTES.md), `evidence/` (committed `r1_1x/`),
  `substrate/`, `work/`. Two 1x scorecards copied. No verdict found.

### Z3 — MISSING
- `cl/arm.zag` + `substrate/` only. Barely started. No verdict found. No
  scorecards.

### Z4 — KILLED
- Frozen: "Per-speaker lexicons do not converge ≥30% faster than a shared
  lexicon — namespacing buys nothing; OR >40% of chunks duplicated across
  namespaces (no real divergence — overhead without content). Conditional
  on Phase 4 working."
- Death certificate quotes the frozen cell exactly. **Verbatim.**
- Fired: 0% convergence speedup (< 30%); Phase-4 condition treated as
  satisfied. M8 FAIL (panic — slice index out of bounds; fail-closed
  battery incomplete). Partial 1x; no 10x. No commit stated.

### Z5 — KILLED
- Frozen: ">15% of recalls on the edit curriculum hit ambiguity or
  failure (loud failures count — the claim is stability, not honesty); OR
  recipe re-run cost > 50× cached-span recall at 10× scale — unaffordable
  online (survives only as ID-stability layer over cached spans,
  conceding the mechanism)."
- Verdict quotes the fired K1 disjunct verbatim (the full two-disjunct
  cell is not quoted contiguously). **Fired disjunct verbatim.**
- Fired: 52.5% prose ambiguity/failure (> 15%). M8 FAIL (panic —
  slice index out of bounds; fail-closed battery incomplete). 1x legs
  (M4 binding); no 10x. No commit stated.
- Note: verdict voids an earlier paraphrased "frozen §3 quote" from
  memory and re-grounds on the brief + byte-verified row.

### Z6 — PASS
- Frozen: "Scar boundaries match ground-truth units (sqlite3.c function
  boundaries, Shakespeare act/scene structure) no better than random cuts
  at the same count (±10%) — the claim is dead; OR the bootstrap arm's
  cuts are never displaced by scars after 10,000 revisions (decorative)."
- Verdict blockquote matches the frozen cell exactly. **Verbatim.**
- Kill did not fire (62.5%/90.9% vs random; ~98–99% displacement). M8
  PASS (byte-identical). 1x legs; no 10x. No commit stated.

### Z7 — MISSING
- Full 1x battery evidence (`evidence/r1/`: scorecard, M8GATE PASS,
  BATTERY_STATUS.md, ARTIFACTS.sha256), build notes, battery scripts.
  **No verdict file found** — the arm is battery-complete but
  uncertified.

### Z8 — MISSING
- `battery_1x.sh`, `cl/`, `docs/` (empty), `substrate/`. No verdict
  found. No scorecards.

## Discrepancy list

### D1 — Frozen arm count is 52, not 53
`units/PREREG_FREEZE.md` §3 programmatically yields **52** frozen arm
rows. The file's own footer ("53 arms ratified") is an arithmetic error.
Y2 is unfrozen and correctly excluded. All counts in this inventory use
52.

### D2 — Arm E was omitted from the dispatch list but is frozen
The task's parenthetical arm list omitted E; frozen §3 contains an E row
("E — Transient segmentation"), and it was inventoried (KILLED, kill
fired at 10x). E is included because frozen extraction is authoritative.

### D3 — 11 arms have no verdict or death certificate
B-64, K1, M2, P, T, V, W, Z2, Z3, Z7, Z8. Of these:
- **M2** has kill evidence (10x K2 leg: 28.8%/26.8% > 10% bar) and a
  `commit_msg_final.txt` claiming a KILLED verdict was written — but no
  verdict file exists in the tree.
- **T** has a `commit_msg.txt` claiming PASS with M1–M8 results — but no
  verdict file exists in the tree.
- **Z7** is battery-complete (scorecard + M8GATE PASS + BATTERY_STATUS.md)
  but has no verdict file.
- **B-8** is NOT in this list: its verdict is `docs/RETIREMENT.md`.
- K1, P, V, W, Z2, Z3, Z8 show build/evidence progress but no verdict.

### D4 — Non-verbatim criterion quotes (scripted diff, 41/41 captured)
- **Verbatim (7):** G2, I2, J2, Y1, Y6, Z4, Z6.
- **Verbatim modulo label/case/split (7):** K2 (drops "Bidirectional:"
  label), M (drops "Scoped:" label), Y3/Z1 (leading-letter case only),
  Y4 (disjuncts quoted separately, each verbatim), R2 (full frozen row
  quoted; kill cell verbatim within), Z5 (fired disjunct verbatim).
- **Partial quote — omits part of the frozen cell (6):** B-8 (family-kill
  clause), E (trailing "Expected to die informatively…" sentence), H2
  (cost disjunct), L2 (trailing clause), R (Note C9), Y5 (drops
  "(links die faster than they pay)").
- **Embellished (1):** X quotes the criterion verbatim then appends
  sentences not in the frozen cell.
- **Paraphrased / reworded (20):** A, B-16, C-P, C-W, D, D-T, D-R, F-B,
  F-S, G1, H1, I1, J1, K3, L1, N, O, Q, S, U. A additionally mislabels
  the source as "frozen §7".
- **Comparator substitution (1):** Q evaluates an internal
  taught-only/emergent-only ablation instead of the frozen O/P
  comparators (flagged openly in its verdict).

### D5 — M8 honesty exceptions
- **FAIL:** Z4, Z5 (both panicked: slice index out of bounds;
  fail-closed batteries incomplete). Their KILLED verdicts rest on the
  binding kill clauses, not on M8.
- **NOT RUN:** D-T, D-R, F-B, J1, J2 (D draft also has no M8).
- **INCOMPLETE:** I1 (timeouts). **NOT ATTEMPTED:** K3. **PENDING:** O.
  **NOT STATED:** G1, H2, I2 (verdicts do not summarize M8; H2 points to
  `M8-REPORT.md`, G2's M8GATE PASS confirmed via evidence file).
- 10x legs: **no arm completed a 10x scale leg.** E ran a 10x
  kill-comparison; M2 ran a 10x K2 measurement; N attempted 10x (tool
  limits); Y5's 10x was blocked. All copied scorecards are 1x.

### D6 — Scorecard coverage
47 scorecard JSONs copied for 33 arms (`scorecards/<ARM>/`, manifest at
`scorecards/_manifest.json`; originals untouched). 19 arms have no
scorecard JSONs: B-64, D, D-T, D-R, G1, J1, J2, K1, M2, O, P, Q, R, T,
U, V, W, Z3, Z8. (J1 has only `fragment.json` files, not scorecards.)
Notably **Q, R, J1, J2** have KILLED verdicts but no scorecard JSONs in
the tree.

### D7 — Duplicate / nested / draft verdict paths
- `M/docs/VERDICT.md` is a byte-identical duplicate of `M/VERDICT.md`.
- Nested canonical verdicts: `D-R/docs/VERDICT.md`,
  `F-S/docs/VERDICT.md`, `K3/docs/lab/units/arms/K3/VERDICT.md`,
  `Y3/evidence/VERDICT.md`.
- Drafts superseded (not counted): `I2/work/VERDICT_draft.md`,
  `Y5/.work/VERDICT_draft.md`; `D/VERDICT.md` is itself marked DRAFT.
- `J1/VERDICT.md` + `J1/DEATH_CERTIFICATE.md` and `J2/VERDICT.md` +
  `J2/DEATH_CERTIFICATE.md` both exist; the death certificates are
  canonical.

## Scorecard copies

All `scorecard*.json`, `*1x.json`, `*10x.json` files under each arm dir
(excluding `.zag-cache`) copied to `~/workspace/tracka-closeout/scorecards/<ARM>/`
with source-relative paths flattened (`__`-joined). Manifest:
`~/workspace/tracka-closeout/scorecards/_manifest.json`. Originals never
modified. 47 files, 0 from 10x legs.

## Method notes

- Frozen §3 rows extracted programmatically (`/tmp/extract_frozen.py` →
  `/tmp/frozen_criteria.json`); never transcribed from memory.
- Verdict quotes extracted by regex/anchor from the verdict files
  (`/tmp/quote_diff.py` → `/tmp/quote_diff.json`); normalization strips
  only markdown formatting (blockquote `>`, `**`/`*`, line-wrapping
  whitespace) and unifies `≥/≤/×` symbols — wording, punctuation, and
  case differences are all reported.
- No randomness used; no arm code executed. Pure inventory/read/diff
  work.
