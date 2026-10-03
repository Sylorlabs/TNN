# NAMECHECK: LW3 Learner Policy Revision and Transfer

Worker: Learner Policy Revision Worker (LW3), subagent, 2026-10-02.
Scope: `docs/lab/research-lead/overnight-20260928/learner_wiring_lw3/` only.
Parent mandate (C290 follow-up): test policy revision after counterexamples
and transfer of the try-keep pattern to a new domain, starting from LW2's
constructed policy 381.

## Step 0: Toolchain guard (mandatory, recorded before any work)

Setup executed 2026-10-02 (worker startup):
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `which python3 python` returned NOTHING under the worker PATH;
`guard-check-done` printed. znc resolved to `$HOME/safebin/znc`
(znc 2026.07.0-dev). All subsequent build/run/analysis commands in this
task run with `export PATH="$HOME/safebin"`.

Toolchain: pure Zag for all research logic (build, runs, analysis of
results by byte comparison with cmp/sha256sum only). Zero Python, zero
RNG. Any forbidden-executable invocation would be PROCESS-FAIL; none
occurred.

Compiler-defect workarounds applied (per AGENTS.md): single preallocated
output buffer with cursor-returning emit helpers and one raw syscall
write (no _zag_print); u8-backed cells with little-endian put64/get64
helpers (no `as *i32` slice construction); if-nesting kept at 3 or fewer
with call results hoisted into locals. Every binary's stdout bytes are
verified against preregistered predictions before any claim is trusted.

## Steps 1..n (record of this worker's actions)

1. Read LW2 prereg (bf523af0b), report and source (229a6baca) from the
   local tnn-rsi repo. Confirmed policy 381 = [EVAL,WIRE0,EVAL,IFB,UNWIRE0]
   and the verdict LW2-COMPLETE with the invention-regress analysis.
2. Wrote PREREG.md (frozen preregistration) BEFORE any implementation.
   Hand-derived all predictions P-R0..P-R5, P-T1..P-T4, P-D in the prereg
   text itself, including the uniqueness proof for policy 725.
3. Disk-full blocker encountered on /home/hatch (100G/100G used): the
   frozen PREREG.md + NAMECHECK.md could not be committed to the repo at
   first. All implementation and runs were performed in /tmp (separate
   tmpfs with free space). Deliverables were moved into the repo and
   committed with explicit pathspecs once placement was possible; the
   prereg content is byte-identical to the frozen version (sha256
   recorded in REPORT.md). No implementation edit preceded the freeze:
   the source was written only after PREREG.md was finalized.
4. Implemented lw3.zag, build.sh; built lw3_bin; ran 6 modes x 3 runs;
   recorded sha256sums.txt; compared all outputs against frozen
   predictions byte for byte.
5. Wrote REPORT.md; committed all deliverables with explicit pathspecs.
   Nothing pushed (standing red line). Paper untouched.
