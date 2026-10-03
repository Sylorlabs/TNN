# NAMECHECK.md -- L2-L3 Truncate Worker

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
znc. Shell used only for: safebin setup, file concatenation, znc
invocation, binary runs, sha256sum, read-only greps, and git ops.

## Step 1: Task identity

L2-L3 Truncate Worker (subagent, 2026-10-02). Mission: demonstrate
L2 adaptation AND L3 novel intermediate creation in a SINGLE problem,
where the L2 adaptation is TRUNCATE (not EXTEND). Scenario STUBBLE:
X = episode recall consolidated at L=6 from old 6-reading episodes;
new episodes carry 4 readings; the L2 TRUNCATE standing rule stops
replay at the first unfilled slot; the consumer is a fixed 4-register
recency window, so X's over-long 6-slot replay lets phantom 255s
displace the informative early readings; the hidden rule (KEEP iff
e1+e2 >= 12) needs slot 1; the L3 greedy construction invents
M = [CPY R0,R1, ADD R0,R2] bridging X' to the scalar threshold
decider Y (t=12).

## Step 2: Constraints honored

- Unfrozen only. No frozen source touched.
- Pure Zag. Zero Python invocations (F-PYTHON silent).
- Zero em/en dashes in documentation (byte-verified).
- Paper untouched.
- Nothing pushed. Commits local only on tnn-native-lab.
- 0 modes, 0 handlers, 0 semantic cases; op basis {CPY,ADD,SUB,MAX,MIN}
  frozen in prereg and never expanded (F-OP-EXPAND silent).
- ADAPT_ON is a driver-set causal-control flag (the composition_l2
  adapt_on precedent), never written by the learner.
- Commit order: prereg committed alone (fc2417e3c) before any
  implementation file existed.

## Step 3: Development notes

1. The implementation reproduced every frozen hand-derived expectation
   on the first build with zero source changes after the prereg:
   C-ROUND 1 win=0,0,1 gain=3 score=7 t=3; C-ROUND 2 win=1,0,2 gain=1
   score=8 t=12; C-ROUND 3 stop; M n=2 t=12 prog=0,0,1,1,0,2,...;
   Z-FULL 4/4; Z-L2ONLY 0/4 with trunc=8; Z-L3ONLY 0/4 with trunc=0
   and M n=0 (C-ROUND 1 base=4 eval=80 stop, pairing proof holds);
   Z-FRESH 0/4. Y-PRIOR fit=6/6 t=12; LEARN-LEN L=6; L-STILL 6.
2. Build: `cat learner.zag world.zag driver.zag > trunc_full.zag`
   (822 lines), then `znc trunc_full.zag -o trunc_bin`. Build exit 0.
   Only diagnostic is the benign zagd-unavailable notice; zero A0102
   warnings.
3. Output path follows the AGENTS.md stdout workaround: numbers
   formatted directly into one preallocated 64KB buffer with
   cursor-returning helpers (ob_app/ob_i32), single
   `_zag_raw_syscall(1,1,ptr,len)` write loop. No `_zag_print`
   anywhere. Stdout verified: 100 lines, 0 NUL bytes, ends with
   L2L3-TRUNC-END.
4. State uses u8 buffers with get32/set32 only; no `as *i32` slice
   construction. Register file is a 16-byte scratch (4 registers)
   loaded by the recency-window r_load helper.
5. K-CB-5 audit: all 10 frozen patterns return 0 hits on
   learner.zag (verified by shell grep after the build).
6. No display anomaly: Z lines in ARM-L3-ONLY show the untruncated
   6-reading replay with 255 phantoms (e.g. id=9
   seq=3,7,6,5,255,255), and true= labels computed on the real
   readings via w_true(e0..e3). Decisions are -1 regardless, so the
   arm scores 0/4 either way. The kill bar depends only on the score.

## Step 4: Determinism

- No RNG anywhere. Fixed candidate order (op 0..4, d 0..3, s 0..3),
  first-max tie-breaking, ascending threshold sweeps (t=0..40).
- trunc_run1/2/3.txt sha256 identical:
  2d9908601667d6bff4eb2f18a1e263b02fdb3cea7e4fea2d53e128fe9aebab65
  (all three). K-CB-6 PASS.

## Step 5: Design delta from the combo build (disclosed)

`learner.zag` is adapted from `l2_l3_combo/learner.zag` (not
byte-identical; the L2 adaptation differs by design). Two disclosed
deltas, both frozen in PREREG.md section 2:
(a) the L2 standing rule is TRUNCATE (stop at first 255) instead of
EXTEND (continue past L while filled);
(b) the reduction machine has 4 registers with recency-window
(keep-last) loading instead of 6 registers with first-6 loading.
Design note: with first-6 loading, trailing constant slots are
provably ignorable by the greedy search, so TRUNCATE could not be
load-bearing; the fixed-capacity recency window is the disclosed
consumer-side constraint that makes the over-long replay displace
informative readings. Greedy construction policy, op basis, decide
pipeline, and state layout are unchanged in mechanism.
