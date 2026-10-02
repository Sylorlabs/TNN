# NAMECHECK.md -- Adversarial L2-L3 Worker

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
znc. Shell used only for: safebin setup, file copy/concatenation, znc
invocation, binary runs, sha256sum, read-only greps, and git ops.

## Step 1: Task identity

Adversarial L2-L3 Worker (subagent, 2026-10-02). Mission: test
whether the L2+L3 combination generalizes to an adversary-designed
world family, different from MEADOW. Scenario RELAY: X = episode
recall with learned replay length L=4 from old 4-reading protocol
episodes; new episodes carry 6 hourly signal-strength readings; the
L2 EXTEND standing rule replays continuation slots while they are
filled; the hidden rule (STABLE iff e5-e1 >= 5, an overnight signal
climb) needs slot 5; the L3 greedy construction invents M =
[CPY R0,R5, SUB R0,R1] bridging X' to the scalar threshold decider Y.
The hidden rule, episode tables, and hand-derived expectations were
designed by this worker independently of the MEADOW builder. The
learner mechanisms (learner.zag) are reused byte-identical and never
modified.

## Step 2: Constraints honored

- Unfrozen only. No frozen source touched. learner.zag copied
  byte-identical from l2_l3_combo (sha256 verified); never edited.
- Pure Zag. Zero Python invocations (F-PYTHON silent).
- Zero em/en dashes in documentation (byte-verified).
- Paper untouched.
- Nothing pushed. Commits local only on tnn-native-lab.
- 0 modes, 0 handlers, 0 semantic cases; op basis {CPY,ADD,SUB,MAX,MIN}
  frozen in prereg and never expanded (F-OP-EXPAND silent).
- ADAPT_ON is a driver-set causal-control flag (the composition_l2
  adapt_on precedent), never written by the learner.
- Commit order: prereg committed alone (4f87b09e6) before any
  implementation file existed. No amendments.

## Step 3: Development notes

1. The implementation reproduced every frozen hand-derived expectation
   on the first build with zero source changes after the prereg:
   Y-PRIOR fit=6/6 t=5; LEARN-LEN L=4 (phase 0 and phase 1);
   C-ROUND 1 base=4 eval=180 win=0,0,5 gain=3 score=7 t=5;
   C-ROUND 2 base=7 eval=180 win=2,0,1 gain=1 score=8 t=5;
   C-ROUND 3 base=8 eval=180 stop; M-BUILT n=2 t=5 score=8/8;
   M-STATE prog=0,0,5,2,0,1,...; Z-FULL 4/4; Z-L2ONLY 0/4 with ext=8;
   Z-L3ONLY 0/4 with ext=0 and M n=0 (C-ROUND 1 base=4 eval=180 stop);
   Z-FRESH 0/4; BARS k1=1 k2=1 k3=1 k4=1.
2. Build: `cat learner.zag world.zag driver.zag > adv_full.zag`
   (807 lines), then `znc adv_full.zag -o adv_bin`. Build exit 0.
   Only diagnostic is the benign zagd-unavailable notice.
3. Output path follows the AGENTS.md stdout workaround: numbers
   formatted directly into one preallocated 64KB buffer with
   cursor-returning helpers (ob_app/ob_i32), single
   `_zag_raw_syscall(1,1,ptr,len)` write loop. No `_zag_print`
   anywhere. Stdout verified: 100 lines, 0 NUL bytes, ends with
   L2L3-ADV-END.
4. learner.zag copied byte-identical from l2_l3_combo (sha256
   338c462287661c13ea02e06fc0b8f57dda2f567c4db68c5ebc3d0b2b89117c6b,
   cmp clean). Never edited.
5. Display note (auditable, not a defect): in ARM-L3-ONLY the Z lines
   show `true=` computed on the truncated 4-reading recall
   (sq[4]=sq[5]=0, so w_true yields 0), because the driver prints the
   label of the sequence the learner actually saw. Decisions are -1
   regardless, so the arm scores 0/4 either way. The kill bar depends
   only on the score.

## Step 4: Determinism

- No RNG anywhere. Fixed candidate order (op 0..4, d 0..5, s 0..5),
  first-max tie-breaking, ascending threshold sweeps (t=0..40).
- adv_run1/2/3.txt sha256 identical:
  d161cbc7c3f4011fb4f9999dcfac540942c3439d7b53adc4693c2b097fd52217
  (all three). K-CB-6 PASS.

## Step 5: Commit provenance

Implementation files staged and committed with explicit pathspecs
only. Verified after commit that the commit contains exactly the
l2_l3_adv implementation files and that the prereg commit 4f87b09e6
strictly precedes it.
