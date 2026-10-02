# NAMECHECK.md -- Delayed Consequence Evaluation Worker

## Step 0: Toolchain Guard (mandatory)

Executed at worker startup, before any other work, via the mandated
setup script:

```
bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
which python3; which python; echo "guard-check-done"
```

Result: the setup script printed
`SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)` and its own
verify lines confirmed python3 and python absent from the safebin
PATH. `which python3` and `which python` afterwards returned NOTHING;
only `guard-check-done` printed. All subsequent work runs with
PATH=$HOME/safebin. znc resolves to the safebin pinned build.

No forbidden executable invoked at any point. Pure Zag via the pinned
znc (src/tools/toolchain/znc_linux_x86_64_abed8aa1 lineage) for all
research logic. Shell used only for: safebin setup, file writes, znc
invocation, binary runs, sha256sum, read-only greps, and git ops.

## Step 1: Task identity

Delayed Consequence Evaluation worker (subagent, 2026-10-02).
Mission: test the TEMPORAL dimension of learner-owned evaluation
(Micah priority 5): the learner commits to a composite, unrelated
episodes intervene, the world later kills a load-bearing fact, and
the learner must attribute the delayed failure back to the specific
commitment using only its own recorded prediction as reference, with
no harness expected answer anywhere in the learner's path.

Parent context: LEARNER-PROBE (C292) and PROBE-BUDGET proved the
learner can choose probes and score its own predictions; C280 built
learner-terminated verification; H-COMPINTEG-1 (C295) exposed circular
self-verification and value-replay failure modes now under red-team
attack. This wave tests the untested temporal axis: credit assignment
across a delay with interference in between.

## Step 2: Scope

`docs/lab/research-lead/overnight-20260928/delayed_consequence_eval/`
only. Frozen assets elsewhere are read only. No paper changes.
Nothing pushed (commits local only). Pure Zag for all research logic.
Zero new edge/MAP types, opcodes, modes, bridges, handlers, semantic
cases. Standalone simulation (world + learner + driver in one .zag
file); TNN core untouched.

## Step 3: Governance notes

- PREREG.md written and committed BEFORE any implementation file;
  PREREG.md + NAMECHECK.md alone in the prereg commit (hash recorded
  below). No implementation existed at that point.
- Kill bars K1..K10 frozen in PREREG.md; no bar moves after results.
  VOID is terminal.
- Determinism bar: 3 full binary runs byte identical (sha256, shell
  verified).
- Researcher-expected-value audit: the learner path never touches an
  expected answer; frozen grep audit over learner functions.
- No em/en dashes in loop docs (check_no_dash.sh before doc
  commits).
- Prereg commit: [recorded after commit]
- Implementation commit: [recorded after commit]
