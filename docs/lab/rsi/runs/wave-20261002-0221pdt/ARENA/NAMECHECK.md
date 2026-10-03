# NAMECHECK: Arena lane worker (wave-20261002-0221pdt)

Wave: wave-20261002-0221pdt
Lane: docs/lab/rsi/runs/wave-20261002-0221pdt/ARENA/
Worker role: Arena capability worker (C9 causal candidate, C9
world-generator fix, DEFRECALL bare-prompt abstention test). No
child subagents (depth 2/2, can_spawn=no).

## Step 0: Worker toolchain guard (mandatory, first)

- Ran: sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
  (exit 0). Output: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python);
  znc OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1).
- export PATH="$HOME/safebin" for all subsequent commands in this lane.
- Fresh-shell verification with PATH=/home/hatch/safebin:
  `which python3` prints NOTHING (exit 1); `which python` prints NOTHING
  (exit 1). `which znc` resolves to /home/hatch/safebin/znc (pinned toolchain).
- PURE ZAG ONLY for this lane: all computational research work uses Zag
  compiled with the pinned znc, or shell plus safebin coreutils. No python
  for glue, analysis, verifiers, harnesses, or fixture provisioning.
  Any forbidden executable invocation is automatic PROCESS-FAIL and will be
  reported honestly.
- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab.
- Write scope: ONLY docs/lab/rsi/runs/wave-20261002-0221pdt/ARENA/.
- No git push, no git reset --hard, no rebase in this lane. Commits local
  only, under this lane directory, explicit pathspec, never git add -A.
  Retry on git ref-lock races.
- Documentation rule: zero em-dash bytes in anything written in this lane
  (colons, parentheses, and commas only). Every doc checked with
  sh docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
  before commit.

## Step 1: Prior records re-derived (from files, not memory)

Sources read:
- docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA/NAMECHECK.md and
  SEALED_EVAL.md (INQ candidate: C8 0.000 -> 1.000, total 58/68 = 0.853,
  3/3 byte-identical, zero regressions; remaining zeros C9, C12, C15).
- docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA2/NAMECHECK.md (C9 negative
  finding: frozen C9 battery unpassable by genuine means; REMAP C12
  candidate BUILD-PASS, 60/68 = 0.882).
- docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA5/PREREG_DEFRECALL.md,
  RT-ARENA5/RT-ARENA5_REVIEW.md (DEFRECALL C15 candidate, QUALIFY).
- docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA-GEN/PREREG_MULTIBARE.md
  and EVAL_REPORT.md (NARROW verdict: whattime and bare invent
  enumerate the roster instead of UNKNOWN).
- docs/lab/rsi/runs/wave-20261001-2321pdt/C9BAT/PREREG_C9GEN.md and
  DEV_VALIDATION.md (C9GEN instrument GEN-PASS; two RNG bugs found and
  fixed: LCG bit-0 degeneracy via rng_bit, Fisher-Yates coverage via
  mod-6000 uniform permutation index).
- docs/lab/research-lead/overnight-20260928/competitive_arena/world_gen.zag
  (frozen source), arena.zag (frozen scorer), ARENA_PREREG.md.
- docs/lab/rsi/runs/wave-20261001-1721pdt/ARENA/refreeze/REFREEZE_RECORD.md
  (v6 base source c6dbc20cf447dce7ab506576b42557a0542065e170bee6516558ecfb435d1e89;
  arena scorer 3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076;
  world_gen c4c8340c818e6848c88e34f1989bf382ff097c69a71d6621c6bf28b58dc85211).

State of the board (sealed 68-item battery, 16 capabilities):
- v6 base: 54/68 = 0.794; zeros on C8, C9, C12, C15.
- INQ candidate (C8): 58/68 = 0.853, candidate on v6 base.
- REMAP candidate (C12): 60/68 = 0.882, candidate on v6 base.
- DEFRECALL candidate (C15): 0.947 on C15 (fresh battery), QUALIFY.
- No candidate exists for C9. The frozen C9 battery is broken by design
  (ARENA2 negative finding): 12 observations enforce x==y==z (CHECK 1),
  zero intervention turns, discrim items always list the true chain
  first with key = chain[0]; the only 3/3 mechanism is question-format
  parsing (rejected as gaming). Queued fix: randomize candidate order,
  add real intervention turns; C9 stays a sealed zero until the fix lands.

## Step 2: This lane's plan (three parts)

Part B (first): C9 world-generator fix. Copy the frozen world_gen.zag
into this lane as world_gen_c9fix.zag with surgical edits only to the
causal subsystem: (1) uniform chain draw from all 6 permutations via
the mod-6000 index (C9BAT amendment A1 method); (2) noisy observations
(root bit via rng_bit, per-edge flip p=0.05), CHECK 1 exactness removed;
(3) real intervention exposure turns (do/do_out, intervened ancestral
sampling in chain order); (4) discrim items list true chain plus one
alternative in seeded coin-flip order, key = full chain string. The
frozen competitive_arena/ tree is never modified. Prereg frozen alone
before implementation; validation: 3/3 byte-identical generation,
old format exploit scores 0, an honest interventional protocol
recovers the chain.

Part A (second): C9 candidate mechanism (CAUSAL) on the v6 base,
evaluated sealed on a world from the fixed generator. Genuine
intervention-driven likelihood inference over do_out turns; replies
the full chain string matching a listed candidate. Full per-candidate
discipline: frozen prereg alone, pure-Zag implementation, sealed eval,
3/3 byte-identical reruns, no regressions vs the v6 baseline on the
same fixed world, architecture accounting. Builders report
BUILD-PASS/BUILD-FAIL only.

Part C (third): bare-prompt abstention test of the committed
DEFRECALL mechanism (commit 2320c3454, binary hash to be verified
byte-identical to ARENA5's sealed binary) on the committed ARENA-GEN
multi-bare-prompt battery (hash verified before runs). Abstention
criterion frozen in this lane's prereg before testing. Report
ABSTAIN-PASS or ABSTAIN-FAIL with exact prompts and outputs.

Commit order per part: prereg committed alone, then implementation or
evaluation commits. Each commit uses an explicit pathspec limited to
this lane directory.

## Step 3: Log

- 2026-10-02 ~02:26 PDT: Step 0 toolchain guard recorded. Safebin
  active, python3 and python absent. Lane directory created.
- (continued below as work proceeds)
