# NAMECHECK.md -- L2-L3 Combination Worker

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

No forbidden executable invoked at any point. Pure Zag via the pinned
znc (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`). Shell used only
for: safebin setup, file concatenation, znc invocation, binary runs,
sha256sum, read-only greps, and git ops.

## Step 1: Task identity

L2-L3 Combination Worker (subagent, 2026-10-02). Mission: demonstrate
L2 adaptation AND L3 novel intermediate creation in a SINGLE problem.
Scenario MEADOW: X = episode recall with learned replay length L=4
from old 4-reading episodes; new episodes carry 6 readings; the L2
EXTEND standing rule replays continuation slots while they are filled;
the hidden rule (rich iff e2+e4 >= 10) needs slot 4; the L3 greedy
construction invents M = [CPY R0,R4, ADD R0,R2] bridging X' to the
scalar threshold decider Y.

## Step 2: Constraints honored

- Unfrozen only. No frozen source touched (read-only by design; the
  only reads of frozen-adjacent material were sibling reports and
  sibling source for method reuse).
- Pure Zag. Zero Python invocations (F-PYTHON silent).
- Zero em/en dashes in documentation (byte-verified).
- Paper untouched.
- Nothing pushed. Commits local only on tnn-native-lab.
- 0 modes, 0 handlers, 0 semantic cases; op basis {CPY,ADD,SUB,MAX,MIN}
  frozen in prereg and never expanded (F-OP-EXPAND silent).
- ADAPT_ON is a driver-set causal-control flag (the composition_l2
  adapt_on precedent), never written by the learner.
- Commit order: prereg committed alone (fb1075ef0) before any
  implementation file existed. No amendments were needed.

## Step 3: Development notes

1. The implementation reproduced every frozen hand-derived expectation
   on the first build with zero source changes after the prereg:
   C-ROUND 1 win=0,0,4 gain=3 score=7 t=1; C-ROUND 2 win=1,0,2 gain=1
   score=8 t=10; C-ROUND 3 stop; M n=2 t=10; Z-FULL 4/4; Z-L2ONLY 0/4
   with ext=8; Z-L3ONLY 0/4 with ext=0 and M n=0; Z-FRESH 0/4.
2. Build: `cat learner.zag world.zag driver.zag > combo_full.zag`
   (803 lines), then `znc combo_full.zag -o combo_bin`. Build exit 0.
   Only diagnostic is the benign zagd-unavailable notice; zero A0102
   warnings.
3. Output path follows the AGENTS.md stdout workaround: numbers
   formatted directly into one preallocated 64KB buffer with
   cursor-returning helpers (ob_app/ob_i32), single
   `_zag_raw_syscall(1,1,ptr,len)` write loop. No `_zag_print`
   anywhere. Stdout verified: 100 lines, 0 NUL bytes, ends with
   L2L3-COMBO-END.
4. State uses u8 buffers with get32/set32 only; no `as *i32` slice
   construction. Register file is a 24-byte scratch (6 registers).
5. Display note (auditable, not a defect): in ARM-L3-ONLY the Z lines
   show `true=` computed on the truncated 4-reading recall
   (e.g. id=9 true=0), because the driver prints the label of the
   sequence the learner actually saw. Decisions are -1 regardless, so
   the arm scores 0/4 either way. The kill bar depends only on the
   score.

## Step 4: Determinism

- No RNG anywhere. Fixed candidate order (op 0..4, d 0..5, s 0..5),
  first-max tie-breaking, ascending threshold sweeps (t=0..40).
- combo_run1/2/3.txt sha256 identical:
  dc0651ba7f965c5c8f9567d114675f30ce84c868050697abf88627667ee483f6
  (all three). K-CB-6 PASS.

## Step 5: Commit provenance note (2026-10-02)

The implementation files were staged with explicit pathspecs, but the
first `git commit` hit a transient index.lock from a concurrent
worker. Before the retry, a different worker's commit (857bdb896,
"rule_revision prereg") swept the shared index and committed all
twelve l2_l3_combo files under its own message. Verified
byte-identical: every committed blob matches the working-tree file
(sha256). Commit order is preserved (prereg fb1075ef0 strictly
precedes the implementation files). This note records the
misattributed commit message; no content was altered and no history
was rewritten.
