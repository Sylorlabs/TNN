# NAMECHECK.md -- L2-L3 Specialize Worker

## Step 0: Toolchain Guard (mandatory)

Executed at worker startup, before any other work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` printed. `which python3 python` returned
NOTHING. All subsequent work ran with PATH=$HOME/safebin.

Note: `which znc` found nothing on the inherited PATH, so znc was
NOT linked by the loop above. The pinned znc was located at
`src/tools/toolchain/znc_linux_x86_64_abed8aa1` (repo root,
version `znc 2026.07.0-dev (edition 2026)`) and linked into
$HOME/safebin manually. No other toolchain was used.

No forbidden executable invoked at any point. Pure Zag via the pinned
znc. Shell used only for: safebin setup, file concatenation, znc
invocation, binary runs, sha256sum, read-only greps, and git ops.

## Step 1: Task identity

L2-L3 Specialize Worker (subagent, 2026-10-02). Mission: demonstrate
L2 adaptation AND L3 novel intermediate creation in a SINGLE problem,
where the L2 adaptation is SPECIALIZE (not EXTEND, not TRUNCATE).
Scenario ORCHARD: X = episode recall whose standing replay is the
general fixed full replay [k,a,b,c,d,e] (k = kind tag, slot 0); the
consumer is a fixed-capacity 2-register machine loading the first 2
replayed readings, so the kind tag and first data reading saturate it
and the kind-specific signal never reaches the registers. The L2
SPECIALIZE standing rule replays only the queried episode's kind
informative slots (per-kind variance masks learned from old
episodes): kind 1 -> [d,e], kind 2 -> [a,b], canonicalizing the signal
pair into (R0,R1). The hidden rule (PICK iff kind 1: d+e >= 10;
kind 2: a+b >= 10) needs the specialized view; the L3 greedy
construction invents M = [ADD R0,R1] bridging X' to the scalar
threshold decider Y (t=6).

## Step 2: Constraints honored

- Unfrozen only. No frozen source touched (read-only by design; the
  only reads of frozen-adjacent material were sibling reports and
  sibling source for method reuse, adapted with disclosed deltas).
- Pure Zag. Zero Python invocations (F-PYTHON silent).
- Zero em/en dashes in documentation (byte-verified before commit).
- Paper untouched.
- Nothing pushed. Commits local only on tnn-native-lab, with EXPLICIT
  pathspecs (concurrent workers active; shared index treated with
  care).
- 0 modes, 0 handlers, 0 semantic cases; op basis {CPY,ADD,SUB,MAX,MIN}
  frozen in prereg and never expanded (F-OP-EXPAND silent).
- ADAPT_ON is a driver-set causal-control flag (the composition_l2
  adapt_on precedent), never written by the learner.
- Commit order: prereg committed alone before any implementation file
  existed. No amendments.

## Step 3: Development notes

(To be filled after the build: construction trace, arm outcomes,
build command, stdout verification.)

## Step 4: Determinism

(To be filled after the runs: 3/3 sha256.)
