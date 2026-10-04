# H2R sealed evaluation results (wave-20261001-2321pdt)

Verdict: BUILD-PASS. All frozen KB-H2R kill bars met, unweakened.

## Frozen bars vs measured

| Bar | Frozen threshold | Measured | Result |
|-----|-----------------|----------|--------|
| B1 (V1 construction reachable, content-neutral) | dv_v1() = 1 | 1 | PASS |
| B2 (hidden queries correct via ticket-built graphs) | >= 29/36 (80%) | 36/36 (100%) | PASS |
| B3 (source novelty: no 1001/1002 literals; guard slot only as 1000+g; white-box ticket shows inverse content) | audit clean | grep: no code literal (only wave-label string); guard = 1000+g at h2r_impl.zag:69; white-box ticket cell tag=102 f4=1001 | PASS |
| B4 (ablation: tombstone ticket cells, re-execute dead root must fail) | S_ablated <= S_baseline | ablated_ok = 36/36; baseline = 0/36 | PASS |
| G-TRIAL (anti-triviality gate) | TRIAL_ENTERED > 0 on every sealed query, else VOID | min TRIAL_ENTERED = 2 across all 36 | PASS (not VOID) |
| G-DET (determinism) | 3/3 byte-identical reruns | sha256 88ee58d0a5114ea04fd078d0291a99583d8ddb8ee7b1b0fab7d38ded6bc59194 x3 | PASS |
| K-C0A (zero new semantic cases) | (i) commit order prereg < impl < worlds; (ii) expected read only in verifier; (iii) grep: no sealed value/relation in impl | (i) bded89be0 < 6f7c08e20 < e3f7375d1; (ii) expected only in h2_trial verify + driver compare; (iii) zero collisions | PASS |

## Per-family breakdown (36 queries)

Families A (w0-2, 2-hop), B (w3-5, 3-hop), C (w6-8, 2-hop + distractor):
12/12 correct in each family. Every query: correct=1, TRIAL_ENTERED=2,
ablated_ok=1, baseline=0.

## Controls

- Frozen-path baseline (ev_query on fresh workspace, no tickets): 0/36.
  The frozen forward path cannot answer inversion queries; all 36 answers
  came from ticket-built graphs.
- Informative masked control (h2_trial with expected=-2, accept first clean
  execution): 36/36. Not a bar; shows the trial converges on the inversion
  from execution feedback alone, without fitting the expected answer.

## Trial dynamics (white-box)

Uniform TRIAL_ENTERED=2: for each query the learner tries the longest
reverse path with guard orientation g=0 (guard slot 0), which fails closed
(slot 0 holds 0, not the given), then g=1 (guard slot 1, the given slot),
which verifies. The inversion (guard on slot 1, a slot the
researcher-written assemblers never guard) is discovered by trial, never
hardcoded: the source contains no 1001/1002 literal; the guard slot code is
always the computed 1000+g.

Family C distractor note (honest): the distractor paths (d->a, e->d) were
present in every family-C world, but emission-order gather placed the true
inversion path first in the trial order, so no distractor path was executed.
Trial *selection* (try, fail closed, reject, try next) was exercised on
every query via the g=0 -> g=1 orientation rejection. The mechanism handles
distractors by the same verify-reject path; this run did not produce a
distractor-rejection event.

## Ablation (B4)

h2_tombstone walks each verifying ticket from its root (BRANCHEQ
true-target via field12, SEQ via the substrate seq_nx ET_SEQ edge walk),
sets every reachable cell tag to 0, then re-executes the dead root on the
query frame. 36/36 queries: answer destroyed (ablated_ok=1). The ticket,
not the frozen path, carries the causal responsibility for each answer.

## Determinism

h2r_sealed built from substrate_proto.zag (verbatim, commit a11dde4b9) +
h2r_impl.zag + worlds_sealed.zag via build_h2r.sh (mechanical main swap).
Three consecutive runs, exit 0, byte-identical stdout (sha256 above).
Binary: h2r_sealed (not committed; reproducible via build_h2r.sh sealed).

## Commit order (prereg discipline)

1. bded89be0 PREREG_H2R frozen (alone)
2. 6f7c08e20 implementation (learner + driver + generator + practice 2/2)
3. e3f7375d1 sealed worlds (seed 20261002, 36 queries)
4. this commit: sealed evaluation

No Python used at any step (safebin toolchain, Step 0 in NAMECHECK.md).
tnn2.zag not modified. PKG block and SUBSTRATE-HOOK lines untouched.
Nothing pushed (local commits only).
