# NAMECHECK.md -- Invention H1 Red-Team Worker (adversarial attack on structural mutation from failure)

## Step 0: Toolchain Guard (mandatory)

Executed at worker startup:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` printed. `which python3 python` returned NOTHING.
PATH=/home/hatch/safebin. Safebin active for all subsequent work.
safebin/znc resolves to the pinned Linux znc
(src/tools/toolchain/znc_linux_x86_64_abed8aa1).

No forbidden executable invoked at any point. Pure Zag. Shell only for
znc invocation, binary runs, git, file moves, and sha256sum.

## Step 1: Task identity

Invention H1 Red-Team Worker. Mission: independent adversarial attack on
Invention Hypothesis 1 (commit 96e9bdea3), which claims that on failure of
all mechanisms the mutate stage extends the longest chain MAP by one cell
using the learner-available "too short" signal (plen-6 invented from
plen-5; open-ended iteration 116 -> 271 -> 549; honest L2 bound).

Method: five adversarial experiments (A1-A5), each a fresh Zag driver
compiled against the UNMODIFIED H1 sources (mu_core.zag + mu_patch.zag +
mu_shared.zag extracted read-only from commit 96e9bdea3). No source edits
to H1 machinery; attacks are adversarial WORLDS, not patches.

Attack battery:
- A1 WRONG-PARENT: distractor domain holds the longest chain MAP; correct
  parent is shorter. Tests whether mutation parent selection is
  relevance-blind and whether provenance is contaminated.
- A2 DECOY-SIGNAL: continuing facts past the endpoint under decoy
  relations. Tests whether the "too short" signal is relation-blind.
- A3 NON-CHAIN: learner state with only non-chain MAPs (count). Tests
  whether the operator does anything outside chain-family.
- A4 EXPLOSION: 20 sequential failing queries in one workspace. Tests for
  mutant spam, brakes, node exhaustion, and parent cannibalization.
- A5 SUF: same query world, different parent training values. Tests
  whether the parent's learned content is causally inert (mutation =
  re-deriving the researcher's world chain at parent-plen+1).

## Step 2: Constraints honored

- Unfrozen only. H1 commit 96e9bdea3 is unfrozen work; its files were
  extracted read-only via `git show` and never modified. Frozen TNN-2
  core untouched.
- Pure Zag. All experiment logic in Zag; shell only for znc, runs, git,
  sha256sum, file moves.
- Zero em/en dashes in documentation (byte-verified before commit).
- Paper untouched.
- Nothing pushed. Commits local only on tnn-native-lab.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases in the attack
  drivers. Drivers only teach facts, issue queries, and dump white-box
  state through existing accessors.
- Adversarial posture: each attack was designed to KILL or BOUND the H1
  claim; verdicts recorded honestly per attack.

## Step 3: Development notes

- Build recipe per attack N:
  cat mu_core.zag mu_patch.zag mu_shared.zag attack_aN.zag > build_aN.zag
  znc build_aN.zag -o bin_aN
  (mu_core/mu_patch/mu_shared extracted read-only from 96e9bdea3)
- New driver code follows the pinned-znc workaround rules from AGENTS.md:
  no `as *i32` + slice construction; emit/e64/i64s/z_alloc/get32/set32
  helpers copied verbatim from the H1 sources (same names, same bodies);
  every binary's stdout bytes sanity-checked (numeric outputs verified
  present and correct) before trusting results.
- A4 sizing: per-query node cost measured first at small N, then N=20
  chosen so node exhaustion and eviction behavior are observable.
- A2 uses relation 99 as the decoy relation (never used for chain facts
  anywhere in the H1 sources).

## Step 4: Determinism

Each attack binary run 3x (A4 2x for time); sha256 of stdout compared.
Results in REPORT.md. Run transcripts: run_aN_1.txt, run_aN_2.txt,
(run_aN_3.txt), plus sha256sums.txt.

## Architecture accounting

- Cognition source lines added: 0 to H1 machinery (read-only reuse).
  Attack drivers are experiment harnesses, not cognition: ~450 lines
  total across attack_a1..a5.zag, all in the redteam deliverable dir.
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
  New task-specific handlers: 0.
- Learner-state structures created: only inside the attack workspaces at
  runtime (facts, MAPs, mutants); none persisted to the repo.
- Capability-source delta: none; this worker attacks, it does not build.
