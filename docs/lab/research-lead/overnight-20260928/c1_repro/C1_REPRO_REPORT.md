# C1-REPRO REPORT: Independent Reproduction of C1-CLEAN (pipeline step 4)

Reproducer: C1-CLEAN Independent Reproducer (subagent)
Date: 2026-09-30 UTC
Prereg: PREREG_C1REPRO.md, frozen alone as d71ef6586 before any rebuild or rerun.

## Verdict

**C1-REPRO-PASS**

Pipeline step 4 (independent reproduction from committed source) is
satisfied for the C1-CLEAN claim.

## Source chain used

- C1-CLEAN prereg: 13e4b1ce3
- Freeze: b8d38d9c8 (prereg -> freeze -> worlds commit order verified)
- Worlds: e0a30377f
- Original results: b2b1ec415

## K1: independent rebuild from committed source only

PASS.

- contestant.zag extracted from freeze commit b8d38d9c8 blob; sha256
  4ef635cd3705f66fea6bfa518bd6e63cea2bd1f96fe97fbade11488f19f56589,
  matching the freeze record exactly.
- run_race.sh extracted from freeze commit b8d38d9c8 blob; sha256
  4cd7bec75915fb93dc8e874d25f9ec6428ee604beadff79b9357ea1c092850a9,
  matching the freeze record exactly.
- Rebuilt with the repo znc compiler (2026.07.0-dev). The rebuilt binary
  sha256 is 8c7ccf308b46e193defeba137c701076cb5b7f7bed28f0393c314bf8bcaa48e4,
  byte-identical to the frozen contestant binary hash. Deterministic
  compilation confirmed independently.
- No original-worker binary was used in the rebuild path. (The original
  binary blob was hashed once from the commit to confirm the freeze
  record, then deleted; only source blobs fed the compiler.)
- All 10 world files (w0, w1, w2, h0, h1; turns.jsonl and key.json) were
  verified byte-identical against the e0a30377f blobs before any run.

## K2: results reproduce

PASS. Zero discrepancies.

Canonical (score claim):

| World | Rep 1 | Rep 2 | Rep 3 | Determinism (repro) |
|-------|-------|-------|-------|---------------------|
| W0 | 63/63 | 63/63 | 63/63 | 3/3 byte-identical |
| W1 | 63/63 | 63/63 | 63/63 | 3/3 byte-identical |
| W2 | 63/63 | 63/63 | 63/63 | 3/3 byte-identical |

Stage scores, all canonical reps: A 20/20, B 8/8, C 6/6, D 6/6, E 8/8,
F 3/3, G 2/2, H 4/4, T 2/2, K 2/2, L 2/2. Sum 63/63.

Exploratory (non-canonical, consistency check only):

| World | Rep 1 | Rep 2 | Rep 3 | Determinism (repro) |
|-------|-------|-------|-------|---------------------|
| H0 | 66/67 | 66/67 | 66/67 | 3/3 byte-identical |
| H1 | 67/67 | 67/67 | 67/67 | 3/3 byte-identical |

Byte-identity confirmation: for all 5 worlds, across all 30 compared
content files (scores.jsonl, replies.jsonl, stage_scores.txt,
state/state.txt, state/ledger.txt, state/checksum.txt per world), the
3/3 repro repetitions are byte-identical within each world AND
byte-identical to the committed C1-CLEAN originals in b2b1ec415.
costs.txt differs only in the wall_ms timing line (machine-speed
artifact; all other lines identical). No content discrepancy of any
magnitude.

H0 law-revert boundary reproduces deterministically: L3 miss,
expected "ttxy", answered "tyxt", byte-identical scores.jsonl line to
the committed original. The mechanism boundary (single law change
handled, law revert missed) is confirmed as a real property of the
frozen contestant, not a flake.

## K3: pure Zag, zero Python, no em dashes

PASS. No Python invoked at any step (compile, sequencer, runs,
comparisons, report writing). All dash byte checks via the shell-only
check_no_dash.sh snippet. No em/en-dash bytes in this report.

## Purity and governance notes

- No new Zag source was written for this reproduction; the frozen
  source was compiled as-is.
- Contaminated paper file untouched.
- Commits local, owned pathspec only.

## What this does and does not establish

Establishes: pipeline step 4 for C1-CLEAN. The 63/63 canonical result
is independently reproducible from committed source; the claim's
determinism and byte-identity hold under an independent rebuild.

Does not establish: steps 5-11 (simple baseline, alternative-explanation
attack, OOD, ablation, transfer/reuse, independent red team, governance
audit). LLM BASELINE remains PENDING. No L3 or Criterion 0 claim is
made: C1-CLEAN remains bounded L2 lifetime learning under the
standing dispositions.

## Recommendation: next pipeline step

Step 5 (simple-baseline comparison) and step 6 (alternative-explanation
attack) should run next, in this order, because the single most
valuable open question is whether 63/63 requires the contestant's
learner-owned structures or can be matched by a memorization or
pattern-fitting control:

1. Step 5 target: a simple baseline (e.g. last-hypothesis replay or a
   shallow associative lookup with no persistent learning state) on the
   same frozen worlds. If a trivial control reaches 63/63, the C1-CLEAN
   score is a world property, not a learning property.
2. Step 6 target: the known deterministic H0 law-revert miss. The miss
   is byte-identical across independent builds, which makes it an ideal
   anchor for an alternative-explanation attack: characterize exactly
   which revision machinery exists in the contestant and whether the
   L3 miss reflects a genuine revision boundary or a scoring artifact
   of the world generator.
3. Parallel lane (already underway elsewhere): the CORE FREEZE CHALLENGE
   worlds attacking the law-revert boundary should treat this
   reproduced miss as a confirmed mechanism property, not a candidate
   flake.

Rationale: reproducibility is now banked twice (original + this
independent rebuild). The remaining information gain is in what the
score does NOT prove. A baseline that matches 63/63 would kill the
learning interpretation; a baseline that fails while the contestant
holds strengthens the claim toward the remaining pipeline steps.
