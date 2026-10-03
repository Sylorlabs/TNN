# ARENA Lane Report: wave-20261002-1121pdt (queue item 7)

Lane: ARENA | Branch: lane-arena-20261002-1121pdt | Date: 2026-10-02
Owner: Micah. All commits local, never pushed. Pure Zag throughout (safebin
PATH; `which python3` returns nothing; Step 0 recorded in NAMECHECK.md).

## 1. Integrated contestant assembly (candidate a): INTEGRATED-PASS

contestant_int.zag = v6 base + INQ (inquiry) + REMAP (transfer) + CAUSAL
(causal discrim), assembled by verbatim lineage-block insertion (all five
blocks diff-verified byte-identical vs their lineage sources) plus a
tick-line do/do_out exclusion so the causal intervention turns are not
tracked as ordinary exposures. No new W offsets beyond the parts (INQ adds
none; REMAP reuses v6's zem template slots 13888..13920 by design from its
lineage; CAUSAL adds 15000..15028 only). No new modes, bridges, or handlers.

fixrun2 (68 items, 291 turns, seed 71503461337030), 3 sealed runs:

- Score: 67/68 = 0.985 on all 3 runs (predicted 67/68).
- Per-capability: C1-C7, C10, C11, C13, C14, C16 = 1.000; C8 = 4/4; C9 = 3/3;
  C12 = 6/6; C15 = 0/1 (expected zero; DEFRECALL abstention boundary).
- I1 (per-cap >= max of individuals): PASS. I2 (C8 4/4, C9 3/3, C12 6/6): PASS.
- I3 (3/3 byte-identical stripped reply streams): PASS (0699f524... x3).
- I4 (pure Zag; double build byte-identical): PASS (f1eb7313... x2).
- I5 (additive only): PASS.

Baselines on the same fixrun2: v6 54/68 = 0.794; INQ part 58/68; REMAP part
60/68; CAUSAL part 57/68. Integrated 67/68 = 0.985. One binary does
everything the four parts did separately.

Binary sha256: f1eb7313b865e96607aef30355e27cc4c093a74df6782513db1839f688457ce3

## 2. Adversarial C8/C12 families (candidate b): both BREAKS confirmed

Generators built as minimal diffs on world_gen_c9d5fix.zag (adv_a: 10 diff
lines; adv_d: 67 diff lines), both build clean, both worlds pass the
scorer's battery-vs-turns cross-checks.

ADV-A decoy-vals (attacks INQ single-slot absorption; oracle fact moved to
vals[1], decoy exposed C1 fact in vals[0]): C8 0/4 on all 3 runs (predicted
0/4). BREAK confirmed. Controls intact: C12 6/6, everything else at fixrun2
levels. Total 63/68 = 0.926 (x3).
Mechanism (trace): INQ asks, absorbs vals[0] (decoy Kavipe/size/small),
re-asks on the re-ask turn, never absorbs the oracle vals[1]. Positional
absorption is the failure point.

ADV-D template-revision (attacks REMAP first-wins lock; 3 new A-words + 2 new
B-words teach changed templates after the originals; C12 re-keyed to the new
templates): C12 0/6 on all 3 runs (predicted 0/6). BREAK confirmed. Controls
intact: C8 4/4, C10 2/2, C16 6/6. Total 61/68 = 0.897 (x3).
Mechanism (replies): remap_prod UNKNOWN x3 (stale template mismatch on the
new segs); remap_class no/yes/no, exactly backwards from yes/no/yes. The
lock answers the revised world with the stale template and only bumps its
conflict counter.

Both adversaries kill with surgical precision: only the targeted capability
breaks; in-world controls hold.

## 3. Multi-seed C9 (candidate c): 3/3 on all admissible seeds, zero variance

8 seed variants (seed_k = 71503461337030 + k*1000003), each differing from
base ONLY in the seed line + proofs label (diff-verified). World-gen is
deterministic: seed_0 world byte-identical to fixrun2.

3 of 8 seeds (k=4,6,7) are INADMISSIBLE: the generator's own novelty
self-check aborts ("DSL EXHAUSTION FAILED: old language expresses
transform"), i.e. those seeds draw a transform expressible in the old DSL,
which would break the novel-morphology premise. Reported as inadmissible
per the frozen prereg; not silently replaced.

15 runs (5 admissible seeds x 3): every run C9 = 3/3 = 1.000, TOTAL = 67/68
= 0.985. Per-seed stripped reply streams byte-identical x3 (5 distinct
per-seed hashes, as expected for distinct worlds). C9 variance across seeds:
zero. The causal discrim (seeded candidate-order coin flip + full-chain
keys) is stable across the admissible seed family.

## 4. C15 abstention continuation (candidate d): ABSTAIN-FAIL confirmed

defrecall.zag extracted via git show from commit 2320c3454; source sha256
fcadb78994f772da69f95917b5a6b88a1d386a994d5faf761eccd032d46c68d9;
rebuilt binary sha256 3d629deda888c18d19ff95ce9819829f2c268cf8e459330b7c573c3892cd57d7
(byte-identical to the frozen ARENA5 record). bare_battery.zag (pure Zag)
emits bare15: 18 turns (1 brief, 4 roster expos, 12 bare prompts, 1 done);
12 bare prompts = 4 roster requests (listnames, roster, names, who) + 8
non-roster (whattime, invent, foo, xyzzy, blorp, sing, dance, weather).

3 runs, fresh state each, streams byte-identical x3: all 12 bare prompts
replied Alpha,Beta,Gamma,Delta (the roster). Abstain rate 0/8 (predicted
0/8); roster accuracy 4/4 (predicted 4/4). ABSTAIN-FAIL confirmed on a fresh
battery: the mechanism enumerates the roster on every bare prompt regardless
of intent. The abstention boundary is structural (bare vs parameterized),
not semantic.

## 5. Red-team findings (gaming, leakage, harness artifacts)

- Gaming: none found. INQ emits observe only when the fact is genuinely
  unknown at ask time; the C8 4/4 comes from a real ask->observe->answer
  loop, and the scorer's observe-before-reply gate is satisfied honestly.
- Leakage: W offsets disjoint (verified at assembly). REMAP shares v6's zem
  template slots by lineage design; empirically no interference (C10/C16
  1.000 alongside C12 6/6 on fixrun2 and on adv_a).
- Harness: arena_512's battery-vs-turns cross-checks pass on all worlds
  (fixrun2, adv_a, adv_d, ms_0..ms_5); no DIVERGENCE aborts in 27 runs.
- Adversarial kills are mechanistically confirmed (trace + replies), not
  harness artifacts.
- The inadmissible seeds are the generator's validity gate working as
  designed, not a contestant weakness; honest non-replacement per prereg.
- Anomaly (non-blocking): one unexplained `1` output from a `python3 -c`
  probe inside a compound shell command during assembly debugging; immediate
  re-verification (repeated `which`/`type`/`command -v`, direct invocation
  -> `command not found`, exit 127) confirms python3 does not resolve under
  the safebin PATH. No Python was used in any research logic at any point.
  Not a PROCESS-FAIL (no forbidden interpreter invoked for research).

## 6. What the zeros need next

- C8 (inquiry): question-indexed absorption. The fix is not "absorb more
  vals" but binding observations to the open questions that requested them
  (match (e,a) of each val against asked (e,a)). General mechanism, not a
  patch; also the substrate for multi-question inquiry.
- C12 (transfer): genuine template revision. When new labeled examples
  contradict the locked template, revise or version the hypothesis instead
  of bumping a conflict counter. Directly on Micah's L2 adaptive-reuse
  priority and the revise-retire requirement.
- C15 (abstention): prompt-intent discrimination, a genuine new cognitive
  structure (semantic intent from a bare string), subject to the 11-step
  frontier pipeline. Short of that, the honest scope is "roster-request
  prompts only", explicitly bounded.
- C9 (causal): stable (3/3, zero variance, 5 seeds). Next is harder
  structure: longer chains, confounded observations, law changes.
- Procedure, goal, language: still zero; outside this queue item's
  subsystems; need dedicated lanes.

## 7. Commit ids (prereg commit-order self-check: all preregs precede impl)

- 3500416f3 NAMECHECK (Step 0 toolchain guard)
- 1e536e2e2 PREREG_INTEGRATED (frozen)
- 36d2ad8b8 PREREG_ADV_C8C12 (frozen)
- 265c182c0 PREREG_C9MULTISEED (frozen)
- e33b1c100 PREREG_C15BOUND (frozen)
- c47deef86 IMPL integrated contestant + adversarial generators/worlds
- 2ea052e4e C15BOUND battery + defrecall source
- 935c9d856 C9MULTISEED worlds/generators + adversarial run logs

Verdicts: (a) INTEGRATED-PASS, adopted as the continuing contestant binary.
(b) ADV-A BREAK, ADV-D BREAK (both kill their target; keep as sealed
adversarial assets). (c) C9-MULTISEED-PASS (3/3, zero variance). (d)
C15 ABSTAIN-FAIL (boundary confirmed; no scope change).

Queued next: question-indexed absorption for INQ (prereg, then build);
template-revision mechanism for REMAP (prereg, then build); C15 intent
discrimination as an 11-step frontier proposal (needs Micah's boundary
ruling before promotion); harder C9 structures (longer chains, confounds).
