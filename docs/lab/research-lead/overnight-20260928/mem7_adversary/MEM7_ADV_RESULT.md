# MEM7_ADV_RESULT.md -- H-MEM7 red-team report

Verdict: H-MEM7 DOWNGRADED (not killed). Two downgrade findings narrow
frozen builder claims; the mechanism implements its spec and all six
builder bars reproduce. No em dashes are used in this file.

## 1. Adversary posture and governance

The red team assumed the H-MEM7 claim ("decayed recency-weighted merit
repairs the merit cliff while preserving every R5 fresh-merit shape by
construction") was false and attacked four surfaces the builder named
as open boundaries. Preregistration: PREREG_MEM7_ADV.md, frozen alone
in commit a3203c3d0 BEFORE any adversary code existed. Kill and
downgrade criteria were frozen per attack before execution.

Harness: mem7_adv.zag = lines 1..749 of the frozen mem7_learn.zag
blob at builder commit 60c3ba3a0 (cmp-verified byte-identical against
the worktree file), plus a new adversary main() and a chkfail helper.
No mechanism line was altered. Pure Zag throughout: no Python
anywhere (no generators, verifiers, analysis, or scratch). Only the
Zag compiler and shell diff/cmp/md5sum were used.

Evidence: MEM7_ADV_RAW_OUTPUT.txt (this directory), md5
3fdef4617279646c222002450f36aee3, three consecutive runs
byte-identical, exit 0, 23/23 adversary CHECKs PASS.

## 2. X-M7-1 (margin): HOLD, the 24-vs-25 edge is exactly as disclosed

Minimal pair on the builder's own setup_m7pair fixture, differing by
ONE query position:
- M25 (positions 17,18): decmerit=25, elig=0 (protected),
  LFU victim=slot0. All 3 CHECKs PASS.
- M24 (positions 16,18): decmerit=24, elig=1 (evictable),
  LFU victim=slot7. All 3 CHECKs PASS.

The protection edge is exactly at decmerit=25 and is load-bearing: a
single query sliding one position flips a real eviction (LFU victim
slot0 -> slot7). The builder disclosed this knife-edge, so this is a
confirmation, not a break. No kill criterion fired (the mechanism
implements its spec exactly); no downgrade criterion fired.

## 3. X-M7-2 (harm-weighting split): DOWNGRADE, merit/harm inversion

Finding: R6 inverts the merit/harm ordering. A protected slot can
have strictly LOWER window-count harm than an evictable slot, with
both slots age-open. Under R5 (merit = harm = count) this is
impossible: protected implied count >= 2 and age-open evictable
implied count <= 1.

Hand-built fixture (frozen Q layout, nq=26, seq=105; full derivation
in the prereg). Measured, all 10 CHECKs PASS:
- slot7 (proc7): decmerit=25 -> protected (elig=0), age-open
  (seq=105 < prot=109). winuses=2, replay harm 2.
- slot0 (proc0): decmerit=21 -> evictable (elig=1), age-open
  (seq=105 < prot=109). winuses=6, replay harm 6.
- LFU protected winner: victim slot0 (harm 6).
  LFU unprotected winner: victim slot7 (harm 2).
Protection flips the LFU victim slot7 -> slot0 and the measured harm
2 -> 6: protection-induced harm = 4, with BOTH slots age-open.

Frozen bound (derived before execution): an age-open evictable slot
has mass < 25, hence count <= 6 (7 queries have minimum mass 28);
a protected slot has count >= 2. So R6 admits protection-induced
harm up to 4 between two age-open slots, where R5 admitted none
(R5 all-age-open harm <= 1 - 2 < 0).

Downgrade (narrowing, not a spec violation): the "decayed merit is a
strict improvement over the count cliff" reading is narrowed. The
merit/harm split (R6 protects by recency-mass while replay harm
stays count-based, a disclosed scope decision) has a concrete cost:
protection can now shield the lower-harm slot and expose the
higher-harm one. The mechanism does what its spec says; the claim
that needs narrowing is the improvement narrative, not the code.

## 4. X-M7-3 (decay calibration): DOWNGRADE, age-window lemma falsified

Finding: the frozen age-window lemma ("any 2 queries since learning
protect (weights >= 12 each, lightest pair 12+13 = 25)") is FALSE for
nq < 20. The weights >= 12 step silently assumes a full window
(nq >= 20, so lo = nq-20). For nq < 20, lo = 0 and the newest
weights are below 20.

Real-run construction (public API only, no hand-set counters):
store_init; learn_stream pids 0..6 (slots 0..6, prot=10 at seq=0);
st_learn pid7 -> slot7 (sseq=7, prot=10); 7 filler queries
(pids 0..6); 2 queries for pid7. End state: seq=9, nq=9,
Q[7]=Q[8]=7. Measured, all 7 CHECKs PASS:
- st_nq=9, st_seq=9.
- decmerit(slot7)=17 (positions 7,8 -> weights 8,9).
- winuses(slot7)=2 >= MERITK: under R5 this slot PROTECTS.
- Age-open confirmed: seq=9 < prot=10.
- elig(slot7, win=20, use_prot=1)=1: EVICTABLE under R6.

A canonical R5 fresh-merit shape (2 queries since learning,
age-open) is evictable under R6 whenever the window is not full.
For nq <= 19 the two newest queries weigh at most (nq-1)+nq =
2nq-1 < 25, so no fresh pair can protect; the threshold is exactly
nq >= 20.

Downgrade (narrowing): "every R5 fresh-merit shape is preserved by
construction" must be narrowed to full windows (nq >= 20). For
nq < 20, R6 evicts fresh-merit slots that R5 protects. This is a
regime the builder's suite never exercised (all fixtures have
nq >= 20 or age-expired slots). The mechanism implements its spec;
the preservation claim is regime-bound, not by construction.

## 5. X-M7-4 (regression): HOLD, no silent changes

- 4a: frozen mem7_learn.zag blob at 60c3ba3a0 cmp-identical to the
  worktree file. PASS.
- 4b: rebuilt from the frozen blob, 3 consecutive runs byte-identical,
  md5 79fdc6eea90c8ed9c019e6893e693bba x3, matching the committed
  MEM7_RAW_OUTPUT.txt. PASS.
- 4c: diff of frozen mem6_learn.zag (266fbde85) vs frozen
  mem7_learn.zag (60c3ba3a0): 13 hunk groups, every one in a
  preregistered R6 category. Non-comment code changes are exactly:
  MTHRESH() + decmerit() added; elig() merit check changed from
  winuses>=MERITK to decmerit>=MTHRESH; setup_m7pair() fixture
  added; F-M6-3c replaced by F-M7-3c (preregistered supersession);
  K-M7-1a/1b/2/3/4/5/6 check code added. Everything else is comments,
  emit strings, and PASS/FAIL lines. No silent behavior change. PASS.

## 6. Overall verdict: H-MEM7 DOWNGRADED

- No KILL criterion fired: the mechanism implements its
  preregistered spec exactly, all six builder bars reproduce
  byte-identical, and the mem6->mem7 diff contains no silent changes.
- Two DOWNGRADE criteria fired:
  (a) X-M7-2: merit/harm inversion, impossible under R5, admits
      protection-induced harm up to 4 between two age-open slots.
      Narrows the "strict improvement" reading.
  (b) X-M7-3: the age-window lemma is false for nq < 20; the
      "every R5 fresh-merit shape preserved by construction" claim
      is narrowed to full windows (nq >= 20).
- X-M7-1 and X-M7-4 HOLD.

Both downgrades are narrowings of builder claims, not mechanism
defects: the code does what the preregistered spec says. A successor
hypothesis should (i) unify or reconcile the merit/harm weighting,
and (ii) re-derive the preservation claim with the nq >= 20 regime
condition, or recalibrate MTHRESH for short windows.

Classification: bounded L2. Nothing here establishes L3.

## 7. Lineage

- Builder: H-MEM7 SURVIVES (6/6), commit 60c3ba3a0.
- Red-team prereg: PREREG_MEM7_ADV.md, commit a3203c3d0 (alone).
- Adversary evidence: MEM7_ADV_RAW_OUTPUT.txt, md5
  3fdef4617279646c222002450f36aee3 (3/3 byte-identical).
- This report: MEM7_ADV_RESULT.md (this file).
- Pure Zag: no Python anywhere. Commits local on tnn-native-lab;
  only explicitly owned paths staged.
