# SEALED_EVAL.md - INDEX lane, wave-20261002-1121pdt

Governing frozen bars: PREREG_REVISE.md (commit `6667a9c4d`, alone,
before any implementation file) as amended by PREREG_REVISE_AMEND1.md
(commit `2a6be2522`, alone, before re-execution). The original
condition (vi) FAILED on its predicted counter values (exploratory
runs: candidate R1/R2 unchain 0 vs predicted >= 1, R3 unchain 1 vs
predicted >= 2); the amendment derives the corrected accounting a
priori from the frozen source order (rewire at base line 660
precedes the hook at line 667, so the hook unlinks only collateral
MAPs, never the rewired revised MAP). No acceptance criterion
((ii)-(v)) was changed. Verdict lines name the amended prereg.

## Builds (frozen inputs, pure Zag, pinned znc, safebin)

Input shas (match the frozen 0521pdt BUILD.txt records):
- base_control.zag: eac0006a78aabe717428ef2d6c489523b8129e3b225785fb0d075a3bcf2c22be
- patch_control.zag: 1362b906fe89e1e9da6383550b8599d225fb570e5c25c654353c364bf2000f43
- evict_driver.zag: b421402707b429bad88b89640b11956720ce6fcd53c4e5e4364732052ad6b450

Candidate source delta (base_candidate.zag vs base_control.zag):
1 hook line (`idx_on_chain_break(W,stale);`) after the tombstone in
`t2_revise_graph`, plus 2 mode-guarded `idx_refile(W,m);` lines
(success and revert paths). patch_candidate.zag adds `idx_refile`
(~30 lines, dup-safe refile under the recomputed chain plen).
New modes: 0. New bridges: 0. New handlers: 0. New semantic cases: 0.

Binaries and run logs live in `work/`:
- revise_control_bin / revise_candidate_bin (revise_driver.zag)
- noop_control_bin / noop_candidate_bin (frozen evict_driver.zag)
- storm_fill_bin / storm_evict_bin / storm_churn_bin / storm_fault_bin

## REVISE verdict: REVISE-PASS (under the amended prereg)

Sealed runs (post-amendment, fresh): 3/3 byte-identical per binary.
- sealed_control_r1..3.txt: sha256
  bafe6bdf4bd09a8efa462310582531ce59f2cf802a6bc19fb168b74ec37bc73e
- sealed_candidate_r1..3.txt: sha256
  9e943a4f19513c64ec07a428a126d6177032ec7b3b88b078c41256fab80182b7

(i) Coverage vacuity (CONTROL). PASS. R3 adversarial shared-stale:
`idx_validate` flips 1 -> 0 with first-flip cause 3 (plen mismatch)
after `revise_on_contradict`; R1 (success) and R2 (revert) keep
`idx_validate==1`. The storm exercises the stale path; not vacuous.
The red-team-flagged gap is REAL and demonstrated: revising MAP A
tombstones the shared 101 step, MAP B's chain breaks, and without
the hook MAP B stays indexed under a plen that no longer describes
it.

(ii) Hook coherence (CANDIDATE). PASS. `idx_validate==1` and
`fidx_validate==1` (and `deep==1`) after every revision in R1, R2,
R3, all 3 runs. R3: MAP A refiled in the plen-3 bucket
(`inbuckA==3`), MAP B unlinked from every bucket (`inbuckB==0`).

(iii) Revision semantics preserved. PASS. R1 MAP answer 6105 ->
7105 on both builds; R2 answer unchanged (6105) on both; R3 MAP A
9001 -> 9999 on both, MAP B 9001 on both. Control and candidate
agree everywhere.

(iv) Determinism. PASS. 3/3 byte-identical per binary (hashes above).

(v) Healthy-state no-op. PASS. noop_control_bin vs noop_candidate_bin
(candidate carries the revise hook) on the frozen evict_driver.zag:
6/6 stdout byte-identical, and every run hashes to the 0521pdt
sealed_new canonical
54df62307f28fcd05fcbe455cbc6e062ed90c2287860f4c8011a3d6d86293414.
The hook is output-silent on the healthy eviction path, and the
reconstructed control reproduces the 0521pdt sealed hash exactly.

(vi-a) Mechanism engagement. PASS. Candidate R3 `inbuckB==0` vs
control R3 `inbuckB==3`; candidate `inbuckA==3`. The hook demonstrably
unlinks the collateral MAP; the pass is not vacuous.

(vi-b) Counter accounting. PASS. Candidate R1/R2 unchain == 0, R3
unchain == 1; control 0/0/0/0/0/0 -- exactly the amended causal
model (rewire-before-hook: only collateral MAPs are unlinked).

## STORM verdict: section pending (runs in progress)

(vii) Panic hunt. PASS (3/3 byte-identical, hash
3f99d63c9439e5a661085e9152d6ed1ab6839d5c273484ec60e2046fabf7318a).
F1 cycle in MAP bucket: gate idx=0, hardened `idx_collect` terminates
(nc=3, no panic: the exact 0221pdt crash site), fallback answer equals
pre-injection answer (20004), SURVIVED. F2 OOB next pointer: gate 0,
collect terminates (nc=2), answers equal, SURVIVED. F3 dead member at
bucket head (hook bypassed by direct kill): gate 0, collect terminates
(nc=10, dead skipped), answers equal, SURVIVED. F4 cycle in FACT
bucket: fidx=0, gather/lu fall back to linear (np and lu unchanged),
SURVIVED. The 0221pdt index-cycle panic class is dead under direct
adversarial corruption: the gate rejects and every hardened path
completes.

(viii)-(xi): storm_fill / storm_evict / storm_churn runs in progress.
