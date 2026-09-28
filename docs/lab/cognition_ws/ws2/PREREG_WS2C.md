# PREREG WS2-C — Self-found retrieval scheme (figure-it-out path)

**Status:** FROZEN 2026-09-24 — committed BEFORE any deliberation run.
**Worker:** WS2-C (self-found retrieval scheme crew). **Coordinator:** cognition workstream.
**Task:** Micah's verdict — "lookups should work EVERYWHERE for its memory. TNN
memory retrieval always needs to be 100%." WS2-A white-boxes today's failures;
WS2-B forces a table-of-contents; **WS2-C lets TNN FIND ITS OWN WAY**.
Any change to the loop design, batteries, gold sets, palette, policy, or bars
after this commit is a new dated amendment; results under a changed rule are a
new experiment, not this one.

## 1. Question

Can TNN itself — native deliberative control, no external policy hard-coding —
design a retrieval scheme that reaches 100% retrieval, given only the failure
evidence and the goal? The scheme-design decisions must come from TNN's own
deliberation, recorded in its audit trail. The crew provides scaffolding only:
harness, fixtures, instrumentation, red-team probes.

## 2. Inputs (all frozen before the run)

### 2.1 Probe battery for the figure-it-out loop: WS2-A v1 (landed)

`cognition_ws/shared/PROBE_BATTERY_SPEC.md` v1 (frozen by WS2-A 2026-09-24),
fixtures `cognition_ws/ws2/fixtures/probe_corpus.txt` (35 physical lines incl.
header = 34 data lines, 33 unique ids — PD01 duplicated) + `probe_queries.txt` (51 probes). Per the task instruction
("USE their probe battery if landed"), this battery IS the loop's probe
battery. TNN deliberates against all 51 probes:

- P-AGE (10): recent-vs-aged install-position symmetry, exact hints.
- P-COLL C1 (10): same-triple siblings, one distinctive token each; C2 (1):
  duplicate-id install semantics.
- P-CTX X1/X2/X3 (18): wrong-hint gates (X1, X3), hintless text queries (X2).
- P-PARA (6): paraphrases with **zero exact-token overlap by construction**
  (validator-verified) — not solvable from evidence (see §8).
- P-NEG (6): empty gold — correct behavior is abstention (empty return).

### 2.2 Failure evidence (TNN reads this; committed pre-run as `evidence.md`)

1. WS2-A's expected fail points for today's arms (from the frozen spec §0–1):
   `PARTITION_GATE` (hint-gated arms on X1/X3), `TOKEN_MISS` (P-PARA),
   `RANK_PAST_K`, `FALSE_POSITIVE` (MORG `topk` has no abstention — P-NEG).
2. MORG per-query miss reports (generated pre-run from
   `memory_org/results/*/run1/retrieval.txt` vs gold, 48 design queries):
   per query per arm: gold ids missed, non-gold ids returned. Headline
   patterns TNN will find there: SELF scores 0.0 on misleading-hint AMBIG
   probes (followed the wrong QUOTE hint: Q41, Q46); IMPOSED scores 0.1250
   on AMBIG (rigid taxonomy); FLAT leaks cross-domain on PURE (0.4875).
3. The goal statement (§4).

### 2.3 Supplementary visible test probes: MORG design 48

`memory_org/queries.txt` calib (16) + test (32) with `memory_org/corpus.txt`
(240 items). TNN may run candidate schemes against these to verify
scale-dependent behavior (40-item answers, misleading hints at scale).
These are failure evidence / test probes — VISIBLE during deliberation.

### 2.4 Held-out bar probes: MORG holdout 12 — SEALED

`memory_org/queries_holdout.txt` (H01–H12) + `memory_org/corpus_holdout.txt`
(astronomy, 40 items). **TNN never sees these during deliberation**: the
`deliberate` command takes no holdout path argument; the holdout files are
never staged in the deliberation workdir; the audit is grepped for
`H01..H12` to prove no leakage (seal is procedural — the native binary could
read any path — compliance is by crew procedure plus the audit grep, stated
honestly here).

Fixture SHAs (frozen): corpus.txt=`908d7ca2d853…`, corpus_holdout.txt=
`dd4a0ed71873…`, queries.txt=`5f94658caea4…`, queries_holdout.txt=
`4636d34f9c6c…` (full SHAs in evidence.md).

**Why the bar is not on the WS2-A battery:** the battery has no sealed split
(all `split=probe`) and contains P-PARA probes that are unsolvable in
principle from available evidence (§8). A 100%-or-FAIL bar must be
achievable-in-principle, otherwise it tests omniscience, not figuring-out.
The 12 holdout probes were verified (2026-09-24, token census over the
280-item store) to be content-solvable: every gold set is exactly
characterizable by hint filtering and/or token evidence, including the
misleading-hint probes (H10: `dhint=physics` contradicts all text evidence;
H12: `dhint=history` wrong while `thint=QUOTE` is right).

## 3. The figure-it-out loop (frozen design)

One native Zag binary (`delib.zag`, pure Zag, zero RNG) implements TNN's
deliberative control. The crew's Python/shell only builds, invokes, and
scores — **all scheme-design decisions execute inside the Zag deliberation
loop**:

```
S = BASELINE = (HM0 STRICT, SC0 COUNT, AB0 NEVER, EX0 NONE); tried = {}
audit <- preamble (engine's own summary stats computed from evidence.md)
loop:
  res    = evaluate(S) on 51 probe + 48 MORG-design probes
  misses = classify(res)                       # per-probe pass/fail + class
  audit <- observation(round, miss stats per class per battery)
  if total_misses == 0:                        # converged
    audit <- "converged: zero misses"; break
  cands  = [m in PALETTE if m not in tried and precond(m, misses)]
  if cands empty:
    audit <- "palette exhausted with misses remaining"; break
  sort cands by (misses-in-their-class desc, palette index asc)  # deterministic
  adopted = false
  for m in cands:
    hyp   = formulate(m, misses)   # evidence-citing hypothesis, engine-composed
    pred  = predict(m, misses)     # what the engine expects to change
    S2    = apply(S, m)
    res2  = evaluate(S2)
    (misses2, regress) = diff(res2, res)   # regress: passed under S, fails under S2
    audit <- trial(m, hyp, pred, misses2, regress, prediction-held?)
    tried.add(m)
    if misses2 < misses and regress == 0:
      S = S2; audit <- ADOPT(m, evidence-based reason); adopted = true; break
    else:
      audit <- REJECT(m, evidence-based reason)
  if not adopted:
    audit <- "no improving move this round"; break
freeze S -> scheme.json; audit -> audit.md (first-class evidence, committed)
```

`formulate`/`predict` compose rationale text from the live miss statistics
(e.g. "12/12 wrong-hint probes fail with gold excluded by STRICT filtering
(F_HINT_EXCLUDE); VERIFY drops hints contradicted by all text evidence;
predicts these 12 -> pass, PURE probes unaffected because their hints are
text-consistent"). The templates are scaffolding; the numbers, the choice of
move, the prediction, and the keep/reject verdict are TNN's deliberation.

## 4. Scheme language (scaffolding vocabulary — frozen, NOT the answer)

A scheme is a 4-tuple. The palette below is the executable vocabulary TNN
reasons over. It is deliberately NOT a complete algorithm: it contains moves
that do not help and moves that trade off against each other, so the choice
is real.

- **HINTMODE** — how query hints constrain candidacy:
  - `HM0 STRICT`: candidate iff item matches ALL given hints exactly
    (empty hint = no constraint). ≈ MORG baseline.
  - `HM1 VERIFY`: start from HM0; repeat ≤3 rounds: for each given hint h in
    order (type, domain, subject), let A = items matching current hint set,
    B = items matching current hint set minus h; if max-text-score(A)==0
    and max-text-score(B)>0, drop h (it contradicts ALL text evidence).
  - `HM2 SOFT`: no hard hint filtering; each matching hint adds bonus +10
    to the text score.
- **SCORE** — candidate scoring from query-text tokens (tokenizer: lowercase,
  maximal `[a-z0-9]` runs — identical to the battery validator):
  - `SC0 COUNT`: Σ token occurrence counts in `hay` (=
    lower(text + subject + domain + type)). ≈ MORG baseline.
  - `SC1 IDF`: Σ occurrences × w(tok), w(tok) = 1 + floor(8·(N−df(tok))/N),
    df from the ingested corpus, integer math, deterministic.
  - `SC2 COVER`: number of distinct query tokens present in hay.
  - Ranking: score desc, id asc tie-break (deterministic).
- **ABSTAIN**:
  - `AB0 NEVER`: always return top-K (≈ MORG: P-NEG false positives).
  - `AB1 ZERO`: if best score == 0, return empty (can say "not found").
- **EXPAND**:
  - `EX0 NONE`.
  - `EX1 CLUSTER`: after provisional top-K, for each subject value S in the
    store: if ≥ ceil(|S|/2) of S's items are in the provisional top-K (and ≥1,
    and some S-item scores >0), add all S items (score desc, id asc),
    truncate to K. (Generic cluster-hypothesis move.)

Baseline `(HM0, SC0, AB0, EX0)` reproduces MORG-like behavior.

## 5. Move palette, preconditions, failure classes (frozen)

Failure classes (computed per probe from ranked output vs gold):
- `F_HINT_EXCLUDE`: ≥1 gold item excluded by hint filtering while carrying
  text score > 0.
- `F_DILUTE`: gold outranked by non-gold whose score comes only from tokens
  with df > N/2 (stopword dilution).
- `F_CLUSTER`: ≥ half of some subject-cluster in provisional top-K but
  cluster members missed.
- `F_ABSTAIN`: (gold non-empty AND returned empty) OR (gold empty AND
  returned non-empty).
- `F_ORDER`: P-AGE install-position asymmetry (check; deterministic id
  tie-break must keep this at 0).
- `F_UNCLASSIFIED`: everything else (expected: P-PARA — see §8).

| # | move | transition | precondition (evidence pattern) |
|---|------|-----------|----------------------------------|
| 1 | M_AB1 | AB0→AB1 | ≥1 F_ABSTAIN miss |
| 2 | M_HM1 | HM0→HM1 | ≥1 F_HINT_EXCLUDE miss |
| 3 | M_HM2 | HM1→HM2 | M_HM1 adopted AND F_HINT_EXCLUDE remains |
| 4 | M_SC1 | SC0→SC1 | ≥1 F_DILUTE miss |
| 5 | M_SC2 | SC0/SC1→SC2 | M_SC1 tried AND (rejected OR dilution remains) |
| 6 | M_EX1 | EX0→EX1 | ≥1 F_CLUSTER miss |

Install semantics are FIXED (not deliberated): duplicate ids keep the FIRST
occurrence (matches the frozen battery's C2 expectation); retrieval-only
experiment.

## 6. The bar (frozen)

**PRIMARY BAR (PASS/FAIL):** after the scheme freezes, ingest
`corpus.txt` + `corpus_holdout.txt` (280 items) and run the 12 sealed
holdout queries ONCE. Per-probe K = max(20, |gold|) (the scheme is told K;
K is a limit parameter, not the answer). **PASS iff recall@K = 1.0 on ALL
12 probes** (every gold id inside the returned top-K). Any miss → FAIL with
per-miss mechanical diagnosis (which probe, which gold ids missed, what
outranked them, which scheme stage is responsible).

Anti-degeneracy: |returned| ≤ K always (worst-case precision |gold|/K ≥ 0.5;
a return-everything scheme cannot exceed K and fails recall on most probes).

**Diagnostics (reported, not bar):** per-probe precision/F1@20 (MORG-style),
WS2-A outcome vocabulary on the 51 probe battery (FOUND / NOT_INSTALLED /
NOT_RETRIEVABLE / FALSE_POSITIVE per class) for cross-crew comparability,
P-PARA limitation statement (§8).

## 7. Scaffolding vs TNN — the line (frozen)

**Crew scaffolding (not scheme design):** the 4-parameter scheme language,
the 6-move palette with preconditions, the fixed deliberation policy
(observe→hypothesize→predict→test→decide), the harness (build/run/score),
fixtures, evidence.md compilation, red-team probes, bill instrumentation.
**TNN's deliberation (the design):** the evidence summary it computes, every
hypothesis/prediction it composes, the order it tries moves, every
ADOPT/REJECT verdict with its evidence-based reason, the stopping decision,
the final scheme. The audit trail must show these decisions; a trace that
merely executes a forced path would fail this preregistration's §1
requirement.

What the crew does NOT do: hand TNN the ToC idea, any complete retrieval
algorithm, the holdout queries, synonym lists, or per-probe answers. The
deliberation binary contains no item-id literals and no query-text literals.

## 8. Known limitation (preregistered, not a bar failure)

P-PARA (QP01–QP06): zero exact-token overlap with gold items BY CONSTRUCTION
(validator-verified). No synonym/stem knowledge exists in any evidence
available to the deliberation; hand-coding a synonym map would be the crew
designing, not TNN figuring out. TNN is expected to diagnose these as
F_UNCLASSIFIED, record the limit, and move on. They are excluded from the
bar (which uses the 12 holdout probes) and reported as T-para.

## 9. Determinism contract (frozen)

Pure Zag, zero RNG in corpus, queries, engine, scoring. Fixed iteration
orders; argmax/argmin ties broken by (score desc, id asc) or palette index.
No wall-clock, no timestamps, no PIDs in any artifact. 3× full reruns
(deliberate + bar) from clean rebuilds; SHA-256 over every output file must
be byte-identical across runs. znc lessons honored: `[]u8` arenas with
explicit u32 accessors (never `as []i32/[]u32/[]u16`), 8-byte struct field
stride, no `.*` on non-pointer locals, no slice ≥ 2^25 bytes, no `};`, no
identifier named `try`. No binaries or `.zagd` files committed. Pinned
toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## 10. Bill (frozen metrics)

Counted in-binary, reported: ingest — index bytes vs corpus bytes, item
visits; lookup — per query candidate visits + token comparisons (mean over
the 99 deliberation probes); wall ms/query measured by shell over the bar
run. Compared against MORG SELF ops (`reads=480 writes=240 moves=240`).

## 11. Red-team (crew scaffolding, post-freeze, diagnostic — not bar)

- R1 hint-swap variants: 6 probes derived from X1/X3 with DIFFERENT wrong
  hints (gold unchanged) — the scheme must recover via the same mechanism,
  proving hint-verification generalizes rather than memorizing.
- R2 id-renaming: rename all holdout ids (AS01→ZZ01…) and golds identically;
  bar score must be unchanged — proves no id memorization.
- R3 novel abstention: 3 nonsense queries verified zero-overlap against the
  bar corpus — must return empty.
- R4 audit grep: `H01..H12` absent from `audit.md` (seal check).

## 12. Deliverables

`PREREG_WS2C.md` (this file), `evidence.md`, `delib.zag` + `build.sh` +
run scripts, `audit.md` (TNN's deliberation trace — first-class evidence),
`scheme.json` (frozen scheme), design results, bar results, `WS2C_PRELIM.md`
interim notes, `RUNLOG.md` entries, bill table, commit SHAs, final verdict
(PASS/FAIL vs §6, per-miss diagnosis on failure, recommendation).
All committed to `sylorlabs/TNN` branch `tnn-native-lab` via
`~/workspace/commit_racefree.py` (paths under `tnn-lab/cognition_ws/…`
→ `docs/lab/cognition_ws/…`), `TMPDIR=~/workspace/tmp_commit`.
