# RT-C174 Second-Opinion Review: C174 shared tag-61 store validation

Reviewer: RT-C174 (second opinion), wave wave-20261001-2321pdt.
Lane under review: docs/lab/rsi/runs/wave-20261001-2321pdt/C174/
Date: 2026-10-01. Branch: tnn-native-lab. Nothing pushed.

## Verdict: EVIDENCE-HOLDS

The lane's VALIDATION-PASS claim survives independent attack. All five
frozen kill bars pass against the verbatim prereg text, commit order is
strict, the sealed world reproduces bit-for-bit from the frozen seed and
committed generator, and I independently rebuilt every binary from the
committed sources and reproduced every claimed hash (A/F de193b84...,
S 6c33f7c4..., migrate fce270e6..., selftest 0e8617cc..., world
e66dab44...). The post-seal fix is legitimate: it removed exactly one
metadata line, cannot change any decision, and was fully disclosed.
Qualifications (not kills) are listed in section 8. No DISSENT warranted.

## 1. Toolchain guard (Step 0)

Safebin activated per AGENTS.md worker toolchain guard before any lane
work: `sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`,
then `export PATH="$HOME/safebin"`. `which python3` printed nothing
(exit 1); setup output confirmed "python3 absent from safebin PATH (OK)".
Recorded in RT-C174/NAMECHECK.md. All verification below used safebin
tools only (sh, git, sha256sum, grep, diff, znc); no interpreter invoked.
Read-only toward the C174 lane dir: all sources extracted with
`git show` from the recorded commits into /tmp/rt-c174.

## 2. Kill bars vs the frozen prereg (verbatim, unweakened)

Prereg: docs/lab/rsi/runs/wave-20261001-2321pdt/C174/PREREG_C174.md,
commit 134af1cb2, frozen 2026-10-02 06:41:07 UTC. Verdict rule:
VALIDATION-PASS iff all five bars pass; no bar moves after the freeze.
Each bar below is checked against the prereg's own words.

(a) STORE-SERVES-TWO: prereg PASS iff W-REORDER completes 48 trials
with sub_note writes > 0 for both namespaces and sub_reorder reads > 0;
W-RETIRE completes with sub_note writes > 0 for PURSUIT and
sub_victims reads > 0; no consumer reads record fields except through
sub_consec (inspection). Committed arm-S output shows
REORDER_WRITES 121, READS 294, RORD 294, RECLAIMS 0;
REORDER_PURSUIT_RECORDS 48 (6 STRATEGY + 48 PURSUIT records via the
generic path); RETIRE_WRITES 28, RRET 10, RUTIL 15, RECLAIMS 0.
I inspected the committed c174_sub.zag: sub_reorder, sub_victims,
and sub_utility obtain every record offset via sub_consec; fam_rate
and the comparator read only offsets sub_consec returned. The eval
driver's arm-S diagnostic dumps also route through sub_consec and
feed no decision (they print after decisions are emitted). PASS,
unweakened.

(b) BEHAVIOR-CHANGE: prereg PASS iff on W-REORDER arm S final order
differs from the fixed order AND total attempts differ between S and
F; on W-RETIRE the arm S victim sequence differs from arm F's.
Direction is explicitly not bar-gated. From the committed outputs
(decision channels, diagnostic lines stripped): S final order
[0 5 1 2 3 4] vs fixed [3 0 5 1 4 2]; attempts 63 vs 103; victims
[7 0 1 6 5] vs [4 8 3 9 7]; held-out answerability 6/6 vs 3/6
(reported, not gated). The per-trial T lines show the S order
evolving over trials (0 1 2 3 4 5, then 0 2 4 5 1 3, then
0 5 1 2 3 4), which is genuine store-driven reordering, not noise.
PASS, unweakened.

(c) ABLATION-CAUSAL: prereg PASS iff SHA-256(arm A output) equals
SHA-256(arm F output) on both worlds AND SHA-256(arm S output)
differs from arm F on both worlds. Committed hashes (re-hashed by me
from 3028240e4): A and F both
de193b844847bd73ef6894fe7745dca424ec2fe5432bdba821042e512cd291ae
(3/3 runs each), S
6c33f7c4cca7833ee2b0bc5ed269f0d8c2007d810f9259ced0a4303783f431f8
(3/3). Both worlds are inside each output file, so "on both worlds"
is covered. PASS, unweakened.

(d) MIGRATION-COMPAT: prereg PASS iff M1 reproduces the CONSEQ K-H3
decision trace exactly (Phase 1 default 30; Phase 2 mid defaults 30,
30, 45; Phase 2 default 45; Phase 3 guide 45) AND the M2 trace is
byte-identical to the M1 trace. Committed migrate output:
M1_KH3_OK 1, M1_TRACE "30 30 30 30 30 45 guide=45",
M2_TRACE byte-identical, MIGRATION_MATCH 1. I verified the
CONSEQ lane's committed record independently: its n2v2_test.zag
hashes to 99774fbc575db57f39d2c93844370aa66a76e38cb7ab101d8717ff5c78bd6855
(the hash the prereg cites) and its rerun shows PHASE1 no shift
(30), PHASE2_MID_DEFAULT 30, 30, 45, PHASE2_DEFAULT 45,
PHASE3_GUIDE 45. The prereg's cited trace matches. PASS, unweakened.

(e) DETERMINISM: prereg PASS iff 3/3 reruns of every binary
(eval_S, eval_F, eval_A, migrate, selftest, gen) are byte-identical.
All three committed runs per binary hash identically; I ran each
binary a fourth time from my own rebuild and matched the committed
hash every time. PASS, unweakened.

## 3. Commit order (prereg self-check)

- 134af1cb2 PREREG FROZEN, 2026-10-02 06:41:07 UTC, contains ONLY
  NAMECHECK.md + PREREG_C174.md. No .zag, no outputs, no world.
- b5e0274f7 IMPLEMENT, 06:45:10 UTC. Sources + build.sh only.
- 0096b30ca SEAL, 06:45:26 UTC. WORLD_MANIFEST.md + world_sealed.zag
  only. No eval output exists in this commit.
- 3028240e4 EVAL, 06:47:53 UTC. Outputs, binaries, EVAL_RESULTS.md,
  JUDGE_BRIEF.md, and the fixed c174_eval.zag.

Prereg strictly precedes implementation, seal, and eval. The seal
commit contains no evaluation artifacts. The commit-order self-check
passes. world_sealed.zag is byte-identical between 0096b30ca and
3028240e4 (not re-committed; seal untouched by the eval commit).

## 4. Post-seal fix scrutiny (does it hold up, or mask a bar (c) problem?)

The disclosed fix: after the seal and before the eval run, the
`emit("C174_EVAL arm="); pi(arm); pnl();` line was removed from
c174_eval.zag main(). I diffed b5e0274f7 vs 3028240e4 for that file:
the diff is exactly that one line removed and a comment added. No
constant, no world, no generator, no store logic, no consumer logic,
no decision logic changed. Seal hash unchanged.

Assessment: the fix holds up, for four reasons.

1. The removed line was metadata, not a decision channel. A pure
   emit cannot change any trial order, attempt count, victim order,
   or utility value. It is impossible for its removal to mask a
   behavioral difference.
2. The prereg's own section 4 anticipated this exact design: "The
   printed decision channels are format-identical across arms; only
   arm S additionally prints record internals." The label violated
   that design; removing it aligns the implementation with the
   prereg, not the reverse.
3. If A and F had differed behaviorally, removing the label would
   not have produced equality; the builder would have failed bar
   (c). The post-fix equality is positive evidence, not masking.
   I independently reproduced A == F (de193b84...) and S != F from
   a fresh build of the committed sources, so the equality does not
   depend on the builder's binaries.
4. It is not a bar move: bar (c)'s letter ("SHA-256(arm A output)
   equals SHA-256(arm F output)") was uncheckable with the label
   present (equality impossible by construction); the fix makes the
   frozen bar checkable as written, with its intent (decision
   channel equivalence) preserved.

Caveats recorded honestly: no pre-fix eval output was committed,
so the claim that the label was the sole pre-fix difference is
self-attested. It is strongly corroborated by points 1-3, but it is
not independently falsifiable from the committed record.

One nuance that must ride along with the bar (c) reading: the
ablation equality partly rests on shared code by construction.
Arm A runs the same driver branches as S, but store_disabled()
(arm_id()==2) gates every sub_note/sub_consec; sub_reorder then
falls back via fixed_order(o) when hits==0, and sub_victims builds
zero abd/u arrays and calls the same order_victims comparator arm F
calls directly. The comment in the source states this explicitly:
"shared comparator lives in exactly one function so the fixed arm
and the ablated arm order identically by construction." So A == F
proves the disabled-store fallback routes correctly to the fixed
rules; it should not be read as two independently written
implementations converging. That is the correct causal reading of
the ablation, and it mirrors the CONSEQ Link 1 pattern the prereg
cited.

## 5. Independent reproduction (my rebuild from committed sources)

Extracted committed sources with git show (3028240e4 for sources,
0096b30ca for the world) into /tmp, rebuilt with the pinned znc:

- gen from committed c174_gen.zag reproduces world_sealed.zag
  bit-for-bit: e66dab44370eaad23da57cedfef59e202a1f14aec42447addeaec4edad787fc8.
  Seal reproducibility confirmed from frozen seed 20261001.
- eval_S -> 6c33f7c4..., eval_F -> de193b84..., eval_A ->
  de193b84...: A == F byte-for-byte confirmed independently;
  S differs.
- migrate -> fce270e6..., selftest -> 0e8617cc...: both match.
- White-box spot checks in the committed arm-S output confirm the
  lane's honest details: FAM 5 att=10 succ=4 sself=5 rate=800
  (the 5 src_self confirmations correctly excluded from evidence,
  spec 7.1); pursuit 101 ABANDONED with cf=4; pursuit 104
  RE-ENGAGED after F,F,F,S; SELFTEST_OK.
- znc emitted one cosmetic warning on the generator
  (E0101 adding 0 has no effect, c174_gen.zag:31); it does not
  affect the output (world hash matches).

## 6. Knowledge vs architecture: is the verdict calibrated to scope?

Yes. The lane scopes itself as dev-harness infrastructure validation
with researcher-scaffolded thresholds and weights, and the verdict
language stays inside that scope throughout:

- EVAL_RESULTS.md: "Dev harness, not TNN-2 integration"; "No claim
  about L3, FW1-FW9, general intelligence, or the final TNN-3
  architecture"; "C174 moves from EMERGES (exploratory) to validated
  infrastructure on the frozen bars; broader generality remains
  untested."
- JUDGE_BRIEF.md: "the shared substrate remains a hypothesis for
  broader worlds, not an established general mechanism."
- PREREG_C174.md section 2.7 honestly labels every constant as
  scaffolding ("None of these are claimed as learner-owned or
  optimal"); section 1 states what is NOT claimed.

I found no language that reaches toward TNN-2/TNN-3 integration,
L3, or generality. The "learner construction primitive,
contradiction trigger, learner standing" boundary with the
concurrent TNN3-SUBSTRATE lane is stated in the prereg and
respected (no new modes, bridges, handlers, or semantic cases;
the frozen TNN-2 binary untouched). The VALIDATION-PASS verdict is
exactly as broad as the frozen bars and no broader.

## 7. Migration-boundary disclosure (real limitation? does it bound the verdict?)

The limitation is real and was disclosed before the run. Prereg
section 5: "the per-value-counter rule and the shift-register rule
coincide on worlds without interleaved divergent revelations; the
K-H3 sealed world has none. A world with interleaved divergent
revelations would distinguish them; that case is out of scope for
this bar." EVAL_RESULTS and JUDGE_BRIEF restate it under honest
scope. Because the limitation is pre-disclosed and bar (d)'s frozen
wording only demands the K-H3 reproduction, the verdict stays
calibrated: "migration-compat on the K-H3 world," not "the store
representation is equivalent to node-local slots in general." This
is a properly bounded claim. A future lane that runs interleaved
divergent revelations would be a genuine new test, not a
re-litigation.

## 8. Attacks attempted and their outcomes

1. "The post-seal fix weakened bar (c)." Did not hold. Diff is one
   metadata line; removal cannot change decisions; bar text is now
   checkable as written; equality independently reproduced.
2. "A == F is vacuous because the label was the only difference
   anyone checked." Did not hold. With the label gone, A == F had to
   come from the disabled-store fallback routing to the fixed rules;
   any routing bug would have broken equality. The shared-code
   nuance is real but does not make the check vacuous (see sec. 4).
3. "S != F is just diagnostic-line noise, not decision difference."
   Did not hold. After stripping all arm-S-only diagnostic lines,
   the decision channels differ per trial (orders, attempts,
   victims, answerability).
4. "The fixed order was tuned against the sealed worlds." No
   evidence. Prereg 2.7 states the fixed order was chosen by the
   author before generation, independent of the world seed; the bar
   does not gate on direction, removing the gaming incentive.
5. "The world was hand-tuned to make S look good." The generator
   reproduces the sealed world bit-for-bit from the frozen seed;
   the assignment is committed via the world hash per the prereg.
6. "Overclaim toward TNN-3." Did not hold; scope language is
   consistently bounded (sec. 6).
7. "Commit-order violation or pre-seal eval run." Did not hold.
   Strict timestamps, clean commit contents, seal commit free of
   eval artifacts. The one residual: the no-eval-before-seal claim
   is self-attested, but the committed record is fully consistent
   with it and the one post-seal source change is disclosed and
   checkable.
8. "The migration test is a trivial coincidence." Partially true
   and already disclosed: the K-H3 world is exactly the world on
   which the two rules coincide. The lane never claims more.
   Not a kill against the frozen bar.

Minor nits (do not affect the verdict):
- EVAL_RESULTS bar (a) parenthetical: "30 sub_consec reads (10
  retention reads, 15 utility reads)" is arithmetically loose.
  The true breakdown from the output is READS 30 = 10 RRET +
  10 RUTIL from sub_victims + 5 PUR diagnostic reads + 5 PUR
  diagnostic utility reads; the counter print happens after the
  PUR dump loop, so it includes diagnostic reads. The bar itself
  only needs > 0 and is satisfied.
- JUDGE_BRIEF carries a template artifact: "RENDER_SHA: not yet
  committed." Immaterial to the verdict.
- Cosmetic znc warning E0101 in c174_gen.zag:31 (adding 0 has no
  effect). Immaterial; world hash matches.

## 9. Commits and evidence paths

Lane commits (local only, never pushed; branch tnn-native-lab):
- 134af1cb2 PREREG_C174 FROZEN (kill bars a-e, seal procedure)
- b5e0274f7 IMPLEMENT shared tag-61 store + eval harness
- 0096b30ca SEAL worlds (hashes before any eval run)
- 3028240e4 EVAL VALIDATION-PASS (outputs, results, judge brief)

Evidence paths (all under
docs/lab/rsi/runs/wave-20261001-2321pdt/C174/):
PREREG_C174.md, WORLD_MANIFEST.md, EVAL_RESULTS.md, JUDGE_BRIEF.md,
c174_sub.zag, c174_gen.zag, c174_eval.zag, c174_migrate.zag,
c174_selftest.zag, armflag_{s,f,a}.zag, build.sh, world_sealed.zag,
runs/eval_{S,F,A}_{1,2,3}.txt, runs/migrate_{1,2,3}.txt,
runs/selftest_{1,2,3}.txt. This review: RT-C174/RT-C174_REVIEW.md,
RT-C174/NAMECHECK.md.

Key hashes (all re-verified by the reviewer):
- world_sealed.zag: e66dab44370eaad23da57cedfef59e202a1f14aec42447addeaec4edad787fc8
- eval A/F: de193b844847bd73ef6894fe7745dca424ec2fe5432bdba821042e512cd291ae
- eval S: 6c33f7c4cca7833ee2b0bc5ed269f0d8c2007d810f9259ced0a4303783f431f8
- migrate: fce270e621ab9ce8a57e6684ab203c2c8199db1a11da586ed8482b6ee26431d7
- selftest: 0e8617cc668b84176dbf71f5095c496d53c0aedcd31e6cda0e89c507c89e8fff

## Final line

EVIDENCE-HOLDS. The C174 VALIDATION-PASS is earned on its frozen
bars, honestly scoped to dev-harness infrastructure, with the
post-seal fix legitimate and fully disclosed, the migration
limitation pre-disclosed and bounding, and no bar weakened.
Qualifications to carry forward: the bar (c) reading is
"disabling the store reverts to the fixed rules via shared fallback
code," not independent-implementation convergence; bar (d) is
"K-H3-world migration compat," not general representation
equivalence; one self-attested timing claim (no eval before seal)
remains corroborated-but-not-independently-falsifiable.
