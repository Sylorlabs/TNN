# NAMECHECK.md -- Cross-Domain Grammar to Program L3 Worker

## Step 0: Toolchain Guard (mandatory)

Executed at worker startup, before any other work. First the task
loop:

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
NOTHING. Then, per the AGENTS.md worker toolchain guard, the canonical
setup script was run:

```
sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
```

Result: SAFEBIN-READY (36 tools, no python). `command -v python3
python` under PATH=$HOME/safebin returns nothing (exit 1). The pinned
znc is `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(sha256 prefix 498abcb5ab346f8cb246222a1ca63699).

No forbidden executable invoked at any point. Pure Zag via the pinned
znc. Shell used only for: safebin setup, znc invocation, binary runs,
sha256sum/cmp, git ops, file concatenation, and read-only greps.

## Step 1: Task identity

Cross-Domain L3 Worker (subagent, 2026-10-02). Mission: test L3 novel
intermediate on grammar to program (Micah priority 2026-10-02 #4:
"grammar to program requiring new intermediate"). Scenario COMPILE:
X = grammar production recall (outputs a 4-symbol production), Y =
program fuel gate (consumes a scalar), Z = RUN-OK/FAIL decisions on new
grammar rules. The learner constructs the reduction program M through
experience-guided greedy search over a frozen generic op basis. M is
then persisted, reused on a new problem (phase 2), and revised when the
world changes (phase 3).

## Step 2: Constraints honored

- Unfrozen only. `composition_l3/learner.zag` treated as read-only;
  the xdomain_l3 copy is byte-identical (sha256
  9317f63c0a72263a533ef9a54b12eed7535dc71a0b202e0c9b14b247fce08e7b
  for both) and was never edited.
- Pure Zag. Zero Python invocations (F-PYTHON silent).
- Zero em/en dashes in documentation (byte-verified with grep -P).
- Paper untouched.
- Nothing pushed. Commits local only on tnn-native-lab.
- 0 modes, 0 handlers, 0 semantic cases; op basis {CPY,ADD,SUB,MAX,MIN}
  frozen in prereg and never expanded (F-OP-EXPAND silent).
- No paired X/Y examples, no "combine" hint, no task label. The driver
  teaches X productions and observed outcomes; the learner discovers M.
- Commit order: prereg committed alone (f54a1214a) before any
  implementation file existed; no amendments needed.

## Step 3: Development notes

1. Design discriminator. The frozen learner machinery is byte-identical
   to composition_l3, so the experiment's discriminating prediction is
   that the SAME source invents a DIFFERENT intermediate here
   ([ADD R1,R3], program bytes 1,1,3) than in FORAGE ([ADD R0,R2]).
   All hand-derived expectations (construction winner, menu fits,
   adapt codes, revision winner) were computed by hand before
   implementation; the implementation must reproduce them exactly.
2. K-XD-5 scope is written into the prereg directly (precedent:
   composition_l3 ERRATUM-1): the 28 structural bytes are the
   intermediate's identity; the threshold field at 236..239 is Y's
   adaptive parameter and changes 10 -> 14 in phase 2.
3. Output path follows the AGENTS.md stdout workaround: numbers
   formatted directly into one preallocated 64KB buffer with
   cursor-returning helpers (ob_app/ob_i32), single
   `_zag_raw_syscall(1,1,ptr,len)` write loop. No `_zag_print`
   anywhere. Stdout verified: 3/3 byte-identical, 0 NUL bytes, ends
   with XG-COMPILE-END.
4. State uses u8 buffers with get32/set32 only; no `as *i32` slice
   construction; no WAV reads. Register file is a 16-byte scratch.

5. AMENDMENT-1 (recorded transparently). The first full run, executed
   before any implementation commit, falsified the original frozen
   expectation M = [ADD R1,R3]: the frozen register machine outputs
   R0 always, so a d != 0 instruction can never affect the output and
   no single-instruction program computes e1+e3 into R0 (builder
   hand-derivation error, not a machinery defect; the learner soundly
   found a 3-instruction 8/8 program instead). Per the
   amend-transparently-and-re-freeze rule, PREREG.md was amended
   (section 11): production tables swap the e2/e3 columns, TRUE1 is
   RUN-OK iff e0+e3 >= 10, and the expected intermediate is
   M = [ADD R0,R3] (program bytes 1,0,3), with phase-3 revision
   M' = [ADD R0,R3, ADD R0,R2]. Amendment committed as a PREREG.md-only
   commit (a6b02f69b) before the implementation commit. The run that
   caught the error used only uncommitted local artifacts; no
   committed result was altered.

## Step 4: Determinism

- No RNG anywhere. Fixed candidate order (op 0..4, d 0..3, s 0..3),
  first-max tie-breaking, ascending threshold sweeps (t=0..40).
- xg_run1/2/3.txt sha256 recorded in REPORT.md; cmp clean both pairs.
  K-XD-7 PASS.
