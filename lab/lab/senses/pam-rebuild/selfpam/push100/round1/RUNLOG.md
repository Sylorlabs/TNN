# RUNLOG — Self-PAM push-to-100%, round 1 (miss autopsy)

## 2026-09-27 ~16:48 PDT — task received
Autopsy crew dispatched. Task: independently reproduce the 101 admits, white-box every
miss, build miss table + mechanism taxonomy, commit under
`docs/lab/senses/pam-rebuild/selfpam/push100/round1/`. Follow-up: also commit
`push100/NUMBERS.json` (machine-readable numbers, schema at top).

## Environment setup
- Repo work done in a fresh worktree `~/workspace/tnn-native-lab-r1` (the shared
  checkout `~/workspace/tnn-native-lab-work/` was on branch `adopt-final`; switching it
  would disturb other crews).
- First `git worktree add` + `git checkout tnn-native-lab` hit a stale `index.lock`
  from an interrupted checkout that deleted 108,171 working-tree files. Recovered with
  `git reset --hard` to the origin head (all files restored, `git status` clean), then
  `git checkout -B tnn-native-lab origin/tnn-native-lab` (old local head 9ba148136 was a
  strict ancestor of the new origin head 5063334993 — nothing orphaned).
- Analysis scratch: `~/workspace/push100r1/scratch/` (kept out of the repo).

## Analysis steps (all deterministic, zero RNG)
1. Extracted `ledger_selfpam_r{1,2,3}.txt` from `origin/tnn-native-lab` via `git show`.
   md5 identical across runs: `3b1fe7145677a7a41b83480f94feff76`.
2. `analyze_admits.py`: parsed ledger → 1099 withheld / 101 admitted; recomputed
   `span_sum//8` over actual F/G bytes for all 1,200 pairs → **0 mismatches**;
   confirmed admit breakdown 100× (motiondir, reversed) + 1× (colordisc, truth unknown
   from pairs_full at that point).
3. `prove_mechanisms.py`: proved 100/100 motiondir admits are exact frame reversals
   (`F_frames == G_frames[::-1]`, 50/50 distinct frames); dissected colordisc_135:
   d65 pixel (48,167,159) vs warm pixel (137,155,82), per-pixel channel sums both 374,
   total sums exactly 2,872,404 both sides — exact collision, ÷8 tolerance uninvolved.
4. Verified corpus: 1,200/1,200 `.pair` SHAs in `~/workspace/selfpam_consumer/pairs_full/`
   match committed `MANIFEST.r2p.sha256` (covers 600 committed + 600 frozen-generator
   regenerated pairs).
5. `build_miss_table.py`: final `miss_table.tsv` (101 rows) using the authoritative
   committed `*.pair.truth` oracle files (not the pairs_full copies); asserted
   header-scene == truth-scene and truth-family == header-fkind for every admit.
6. Read `gen_r2p.py`, `g1_candidate.zag`, `codec.zag`, `sense.zag` (ledger_final is a
   per-entry hash chain — explains why it differs from sha256 of the ledger file),
   `VERDICT_R2-3.md` (reference gate withholds 100% because every F is verified fooled).

## Key decisions
- Ledger flag field: the task brief said "4th field"; the actual format
  `e <idx> <jf> <jg> <0|1> <hash>` puts the flag 5th whitespace-separated. Parsed
  accordingly; counts confirmed against the admission report (1099).
- The 101st admit (colordisc_135, truth=SAME) judged a genuine MISS, not a correct
  admit: generator-certified fooled F, reference gate withholds it, no prereg carve-out
  for truth=SAME pairs (VERDICT_R2-3 B5 counts all 1,200).
- Mechanism classes named A (permutation-blindness) and B (exact sum collision); both
  classified gate-measurement limitations, both fixable, neither information-theoretic.

## Deliverables committed
- `docs/lab/senses/pam-rebuild/selfpam/push100/round1/MISS_AUTOPSY.md`
- `docs/lab/senses/pam-rebuild/selfpam/push100/round1/miss_table.tsv` (101 rows)
- `docs/lab/senses/pam-rebuild/selfpam/push100/round1/scripts/{analyze_admits,prove_mechanisms,build_miss_table}.py`
- `docs/lab/senses/pam-rebuild/selfpam/push100/round1/RUNLOG.md` (this file)
- `docs/lab/senses/pam-rebuild/selfpam/push100/NUMBERS.json` (schema + round-1 numbers)

No binaries, no caches, no frozen corpus/prereg files modified. Commit verified by
re-reading committed blobs after the commit (see below).
