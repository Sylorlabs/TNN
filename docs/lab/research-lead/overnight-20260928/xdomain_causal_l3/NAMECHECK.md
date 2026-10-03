# NAMECHECK.md -- Cross-Domain Causal to Intervention L3 Worker

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
for: safebin setup, znc invocation, binary runs, sha256sum/cmp, git ops,
file concatenation, and read-only greps.

## Step 1: Task identity

Causal L3 Worker (subagent, 2026-10-02). Mission: test L3 novel
intermediate on causal to intervention. Scenario INTERVENE: X =
causal observation recall (outputs a 4-reading scenario), Y =
intervention gate (consumes a scalar strength), Z = ACT/SKIP
decisions on new scenarios. The frozen learner machinery (byte-
identical copy of composition_l3/learner.zag, never modified)
constructs the reduction program M through experience-guided greedy
search over a frozen generic op basis. M is then persisted, reused on
a new problem (phase 2), and revised when the world changes
(phase 3). Discriminating prediction: M = [ADD R0,R1] here versus
[ADD R0,R2] (FORAGE) and [ADD R0,R3] (COMPILE) from the same frozen
source.

## Step 2: Constraints honored

- Unfrozen only. No frozen source touched. learner.zag is a
  byte-identical copy of composition_l3/learner.zag (sha256
  9317f63c0a72263a533ef9a54b12eed7535dc71a0b202e0c9b14b247fce08e7b,
  verified equal to both composition_l3 and xdomain_l3 copies);
  copied with cp, never edited.
- Pure Zag. Zero Python invocations (F-PYTHON silent).
- Zero em/en dashes in documentation (byte-verified with grep -P).
- Paper untouched.
- Nothing pushed. Commits local only on tnn-native-lab.
- 0 modes, 0 handlers, 0 semantic cases; op basis {CPY,ADD,SUB,MAX,MIN}
  frozen in prereg and never expanded (F-OP-EXPAND silent).
- No paired X/Y examples, no "combine" hint, no task label. The driver
  teaches X scenarios and observed outcomes; the learner discovers M.
- Commit order: prereg committed alone (e53775073) before any
  implementation file existed.

## Step 3: Development notes

1. No amendments needed. The first full run reproduced every
   hand-derived prereg expectation exactly (construction winner and
   gains, all five menu fits and test scores, both adapt codes,
   thresholds, persistence, held-out and revision scores), so the
   frozen prereg stands unamended.
2. znc warnings (2, benign, same as the FORAGE and COMPILE builds):
   A0102 ignored return value of `x_recall` in d_menu_fit and
   d_menu_eval, where recall cannot fail (all scenarios taught).
   Build exit 0.
3. Output path follows the AGENTS.md stdout workaround: numbers
   formatted directly into one preallocated 64KB buffer with
   cursor-returning helpers (ob_app/ob_i32), single
   `_zag_raw_syscall(1,1,ptr,len)` write loop. No `_zag_print`
   anywhere. Stdout verified: 141 lines, ends with L3-CAUSAL-END,
   3/3 byte-identical.
4. State uses u8 buffers with get32/set32 only; no `as *i32` slice
   construction; no WAV reads. Register file is a 16-byte scratch.
5. Grep-audit hygiene: the single "handler" hit in learner.zag is
   the frozen header comment "0 modes, 0 handlers, 0 semantic
   cases" (a denial, present identically in the frozen source), not
   machinery. driver.zag and world.zag have 0 hits for _MODE,
   bridge (case-insensitive), and handler.
6. learner.zag copied with cp from composition_l3/learner.zag;
   sha256 9317f63c0a72263a533ef9a54b12eed7535dc71a0b202e0c9b14b247fce08e7b
   matches composition_l3 and xdomain_l3 copies exactly.

## Step 4: Determinism

- No RNG anywhere. Fixed candidate order (op 0..4, d 0..3, s 0..3),
  first-max tie-breaking, ascending threshold sweeps (t=0..40).
- xc_run1/2/3.txt sha256 identical:
  1a7c99158a8a347b439cd0a268acfeba8eb80cbbfdf5031f730e9c3f1c7cf7d0
  (all three), cmp clean both pairs. K-XC-7 PASS.
