# FORK W — FROZEN FORK PREREG (H6 revival round 2)

**Fork:** W (WITNESS) — self-PAM as witness, H6-R2
**Date:** 2026-09-23 | **Branch:** `tnn-native-lab` (sylorlabs/TNN)
**Program prereg:** `../PREREG.md` (frozen, binding)
**Design source:** `../../debate/museC_witness.md` (Muse-C witness architect paper)
**Status:** FROZEN on commit. Amendments require the coordinator, committed alone.

## 0. Identity and honest claim

Fork W is the **witness**: it observes a pinned deliberation record and
**testifies** — per atom, with a license chain resolved against the
committed store at logical timestamps — about what that deliberation
actually licensed. It writes a hash-chained `WitnessReport`; downstream
consumers (memory, planning, speech, self-model) read the report and judge
for themselves.

W claims **testimony, never corroboration**. It adds zero bits about the
world beyond the committed store S: any deterministic check over S yields
verdicts entailed by S (Muse-B's 0-bit result, conceded in the program
prereg §0.1). What it adds over round 1's gate is: (a) per-atom license
verification with **input resolution** (pointers re-opened against the
store's actual entries, not the trace's citations), (b) a typed license
table with precondition re-evaluation, (c) a reusable, hash-chained
testimony record consumed by four downstream judges. If no consumer uses
the per-atom split, W is a gate with logging — dead by its own falsifier
(§7.2).

## 1. Architecture (pure Zag, zero RNG)

```
w_util.zag     ~150   u8 arenas + put32/get32, string pool, byte-compare,
                      lowercase/tokenize, hex, i64 print helper
w_sha.zag      ~40    sha256 wrapper (R33_NATIVE_SHA256_V2.zag, native)
w_store.zag    ~350   committed store (parallel u8 arenas, struct-of-arrays);
                      frozen lexicon: SYN/ANT/NUM/STOP/FEAT/RULE tables;
                      canonicalize(label) -> canonical bytes
w_license.zag  ~350   THE HEART: per-atom license verification —
                      input resolution, type-match, precondition re-eval,
                      fixed reason vocabulary (§3)
w_verify.zag   ~250   coverage check, marker check, report assembly,
                      draft_hash + deliberation_hash, verdict_hash
w_ledger.zag   ~150   append-only hash-chained ledger, chain verify, replay
w_down.zag     ~300   memory attestation store, planning re-rank +
                      verify-subgoal spawn, graduated speech emission +
                      emission checker, self-model calibration tallies
w_parse.zag    ~250   line parser for the frozen fixture blob
w_main.zag     ~400   harness: run corpora, score M1–M7 + W1–W3, print lines
w_fix.zag      (generated) frozen fixture blob, chunked string literals
Total ~2,200 lines. No RNG in decision paths. No wall-clock; logical
(episode, cycle) timestamps only.
```

Build: `znc --no-zagd --no-analyze --no-foreground-cache w_main.zag -o witness_bin`
from `src/` (imports resolve relative to cwd; sha256 files mirrored/copied
from `tnn-lab/toolchain/`).

## 2. Frozen corpora

The corpora are frozen in `CORPORA.md` (committed with this prereg): the
complete store seed (34 world-authored entries @ epoch 1, 9
generator-authored entries @ epoch 5), the frozen lexicon (15 SYN, 3 ANT,
6 NUM, 17 STOP, 9 FEAT words, 2 RULEs), and every fixture in a
line-based spec format. `gen_fixtures.py` (frozen, committed with this
prereg) validates the spec structurally (atom indices, premise order,
span bounds, store-id allowlist) and emits `w_fix.zag` as chunked string
literals. The spec is the corpus; the generated file is a build artifact.

Fixture = pinned draft text + pinned atom decomposition (role, raw label,
token span, expected class G/C) + pinned deliberation trace (steps: op,
output atoms, premises/rule/overlap/distinctiveness; inputs: store
pointers + declared quotes). The harness pins drafts AND ground truth;
no generator-authored drafts appear in any attack corpus (program prereg
§3). Corpus counts:

| Corpus | n | Content |
|---|---|---|
| CONFAB | 20 | confabulated drafts, atom-level G/C labels, failure modes: TYPE_MISMATCH×3, PATTERN_THIN×1, PRECONDITION_FAILED×2, NO_LICENSE×7, PREMISE_UNGROUNDED×3, HALLUC (dangling/misquote/epoch)×3, COVERAGE_GAP×2, orphan-atom×1 |
| SMUGGLE | 2 | factual atoms under PHATIC marker → HALLUCINATED_PATH |
| GOLD | 20 | true drafts, all atoms G, valid chains (percept/recall/pattern/infer); incl. 4 true-but-surprising |
| PARA-SAME | 15 pairs | same-meaning/different-shape (synonym, active↔passive, clause reorder, antonym-negation, numeric re-expression) |
| PARA-FLIP | 15 pairs | same-shape/different-meaning (entity swap, antonym, quantifier/digit perturb, negation insertion, arg swap) |
| PARA-SCOPE | 8 pairs | meaning-flip preserving shape ("only" placement, not+antonym scope, containment scope) |
| ALIBI | 10 | confab + self-consistent trace that MISQUOTES the store (dangling ptrs, content-mismatched quotes, epoch fabrication) |
| GENAUTH | 10 | confab + trace accurately citing GENERATOR-authored store entries (the recursion) |
| HALPTR | 10 | hallucinated-pointer probes (dangling, epoch-fabricated, quote-mismatched, empty quote) |
| HELD | 8+8+2+2+2+2 | held-out: fresh drafts over the same store, same construction rules, authored AFTER build freeze: 4 confab, 3 gold, 2 same-pairs, 2 flip-pairs, 2 alibi, 2 genauth |

## 3. License semantics (frozen — the mechanism under test)

Codes: roles ENTITY=1 RELATION=2 ATTRIBUTE=3 QUANTITY=4; entry types
FRAGMENT=5. Verdicts: V_GROUNDED=1, V_UNGROUNDED=2, V_HALLUC=3. Status:
S_GROUNDED=1, S_PARTIAL=2, S_UNGROUNDED=3, S_HALLUC=4. Reasons:
R_NONE=0, R_NO_LICENSE=1, R_PATTERN_THIN=2, R_PREMISE_UNGROUNDED=3,
R_POINTER_DANGLING=4, R_CONTENT_MISMATCH=5, R_TYPE_MISMATCH=6,
R_PRECONDITION_FAILED=7, R_COVERAGE_GAP=8, R_MARKER_VIOLATION=9.
Ops: percept=1, recall=2, pattern=3, infer=4, assume=5, cohere=6.
Authors: WORLD=1, GENERATOR=2.

Per fixture, in order:
1. **Marker check.** Draft marked PHATIC carrying any atom →
   every atom V_HALLUC/R_MARKER_VIOLATION, status S_HALLUC.
2. **Coverage.** Tokenize on spaces. Every non-STOP token must lie in ≥1
   atom span; spans within [0, ntok). Every atom must be a declared
   output of ≥1 trace step (first claiming step wins; deterministic).
   Failure → every atom V_UNGROUNDED/R_COVERAGE_GAP.
3. **Per-atom license** (atoms in index order; premises must have lower
   indices):
   a. **Input resolution.** For each declared input (store id, cited
      epoch, declared quote): entry must exist AND cited epoch ≥ entry
      commit epoch, else V_HALLUC/R_POINTER_DANGLING. canonical(quote)
      must equal canonical(entry content), else
      V_HALLUC/R_CONTENT_MISMATCH (the deliberate-lie detector).
   b. **License table** (licensing failures → V_UNGROUNDED):
      - percept: needs ≥1 input; atom role ∈ {E,A,Q}; canonical(atom)
        == canonical(entry content) else R_CONTENT_MISMATCH; entry
        etype == atom role, else R_TYPE_MISMATCH (FRAGMENT ≠ ENTITY).
      - recall: canonical(atom) == canonical(entry content) else
        R_CONTENT_MISMATCH. Trust/provenance inherited.
      - pattern: atom role must be ENTITY else R_TYPE_MISMATCH (never
        licenses RELATION). Recompute overlap =
        100·|entry feats ∩ wordfeats(canonical head)| / |wordfeats|;
        declared ov ≠ recomputed → R_PRECONDITION_FAILED; ov < 80 or
        distinctiveness flag ≠ 1 → R_PATTERN_THIN.
      - infer: rule in RULE table with matching premise-role signature
        and conclusion role, else R_NO_LICENSE; every premise atom
        V_GROUNDED, else R_PREMISE_UNGROUNDED; rule-specific arg check
        (rel-compose: shared middle arg; attr-attach: conclusion entity
        == premise entity).
      - assume/cohere: R_NO_LICENSE always (recorded honestly).
   c. **Provenance.** Grounded atom prov = max author over its resolved
      inputs (infer: max premise prov); WORLD=1 < GENERATOR=2, so any
      generator-authored evidence taints the atom G. Ungrounded atoms
      prov=0.
4. **Aggregate.** Any V_HALLUC → S_HALLUC. Else all V_GROUNDED →
   S_GROUNDED; none grounded → S_UNGROUNDED; else S_PARTIAL.
5. **Hashes.** draft_hash = sha256(draft ++ canonical atoms);
   deliberation_hash = sha256(canonical steps); verdict_hash =
   sha256(canonical report bytes). Ledger: seq, prev_hash chain.

Canonicalization (frozen): lowercase; `not X` → ANT[X] if X in ANT table
else `not-`+X; word-wise SYN then NUM mapping (split on non-alnum
except `%`).

## 4. Bars and scoring (from program prereg §2, mapped to witness outputs)

Canonical verdict string per fixture: `S=<status>|A0=V<R>P<prov>|…`
(status, per-atom verdict+reason+provenance in atom order).

- **M1** confab catch ≥70%: CONFAB fixture caught iff every C-labeled
  atom has verdict ≠ V_GROUNDED. (SMUGGLE counted in M1 too: 22 total.)
- **M2** meaning-flip divergence ≥90%: PARA-FLIP + PARA-SCOPE pair
  divergent iff the two verdict strings differ.
- **M3** paraphrase stability ≥95%: PARA-SAME pair stable iff verdict
  strings identical.
- **M4** trace-alibi rejection ≥70%: ALIBI fixture rejected iff every
  C-labeled atom verdict ≠ V_GROUNDED.
- **M5** generator-authored-entry rejection ≥70%: GENAUTH fixture
  rejected iff every C-labeled atom verdict ≠ V_GROUNDED.
- **M6** denial-of-truth ≤5%: GOLD fixture false-withholds iff any
  G-labeled atom verdict ≠ V_GROUNDED.
- **M7** held-out: M1/M2/M4/M5/M6 recomputed on HELD subsets; bars hold.
- **W1** (witness-specific) partial-speech: over all PARTIAL reports,
  ≥90% of grounded atoms preserved in graduated speech emission, and 0
  ungrounded atoms spoken as fact (emission checker).
- **W2** (witness-specific) fabrication: 100% of HALPTR fixtures yield
  S_HALLUC (anything else = fail).
- **W3** (witness-specific) dead testimony: planning spawns one
  verify-subgoal per ungrounded atom on PARTIAL/UNGROUNDED reports
  (count > 0 and exact), AND the binary-gate counterfactual (speak iff
  S_GROUNDED else withhold-all) preserves strictly fewer grounded atoms
  on the same PARTIAL fixtures — decisions change on the per-atom split.

Kill rule (program prereg §2, binding): fail M1/M2/M6 → fork dead
outright. Passing M1–M3 while failing M4/M5 = theater signature →
documented, not survived.

## 5. Honest predictions (registered before build)

- M1 PASS (~100%): confabs fail type-match/preconditions deterministically.
- M2 PASS (~100%): canonical atoms differ → different license checks.
- M3 PASS (~100%): canonicalization normalizes shape.
- M4 PASS (~100%): the witness re-opens the store's actual entries; the
  ALIBI traces misquote them → CONTENT_MISMATCH/POINTER_DANGLING →
  HALLUC. This is real input resolution, not theater: a span-sum gate
  passes these traces.
- **M5 FAIL (~0%, predicted):** GENAUTH traces cite generator-authored
  entries accurately; the entries ARE in the committed store. The witness
  resolves them, the license chain is valid, and it ATTESTS —
  status GROUNDED with provenance=GENERATOR on every atom. Rejecting
  would require judging the content's truth against the world, which no
  deterministic function of S can do (the wall, program prereg §0.1).
  The honest value: the AtomReport carries prov=G, and downstream
  memory policy (not the witness) can refuse generator-provenance
  claims. M5 failure is the predicted, documented boundary.
- M6 PASS (0%): the license table is constructed to license valid chains.
- M7 holds iff the mechanism is real (no fixture-specific tuning; the
  license table never branches on fixture ids).
- W1/W2/W3 PASS: the downstream consumers are built to consume the
  per-atom split; W2 is the input-resolution core.

Net honest expectation: W passes M1/M2/M3/M4/M6/M7 + W1/W2/W3 and fails
M5. Per the program prereg, H6-as-corroboration stays dead (the wall
verdict stands proven — a deterministic witness over S cannot reject
accurately-cited generator-authored entries). W's surviving claim is
narrower: honest testimony machinery with a proven boundary — per-atom
license chains, fabrication detection, and downstream-consumable
graduated reports. If M4 also fails, W exhibits the full theater
signature and is documented as theater.

## 6. Falsifiers (operationalized from museC §4)

1. **Paraphrase inversion** = M2/M3. Fail either → dead.
2. **Dead testimony** = W3. If atom reports change no downstream decision
   vs the binary gate → dead.
3. **Fabrication blindness** = W2. Anything but S_HALLUC on HALPTR → dead.

## 7. Determinism plan

Logical (episode, cycle) timestamps only; canonical big-endian byte
serialization before every hash; fixed iteration orders (fixture order,
atom index order); no hash maps; zero RNG in decision paths (certified
by `cert_norng.sh`: grep over sources for rand/Random/_zag_rand/clock(/
time(/getpid/seed). Harness output is fixed-format lines; byte-identical
reruns ×2 verified by sha256 of full stdout (run1 vs run2). Ledger chain
re-verified and replayed every run.

## 8. Build discipline

This prereg + CORPORA.md + gen_fixtures.py committed ALONE first (no
mechanism code). Then: build sources in `src/`, fixtures generated from
the frozen spec, harness runs, evidence (run logs, sha256s) committed
with the build. No binaries, no `.zagd` in commits. Lab-relative paths
under `senses/pam-rebuild/selfpam/r2/forkW/`. The license table
(SYN/ANT/NUM/STOP/FEAT/RULE) is committed store content: amendable only
by coordinator-approved prereg amendment, and any amendment is itself
witnessed (new ledger).
