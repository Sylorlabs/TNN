# NAMECHECK.md -- Composition L3 2-Op First-Creation Worker (LEDGER)

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
file concatenation, read-only greps, awk-based design verification of
the prereg's hand-derived numbers (design check only; no research logic
outside Zag), and byte checks for em/en dashes.

## Step 1: Task identity

Composition L3 2-Op First-Creation Worker (subagent, 2026-10-02).
Mission: test whether the unmodified L3 intermediate-construction
learner can invent a 2-operation intermediate in its FIRST fresh
creation, not via later revision. FORAGE built `ADD R0,R2` (1 op) then
extended to 2 ops on revision; RELAY built `SUB R0,R1` (1 op) then
extended to 2 ops on revision. The open question is first-creation
2-op invention. Scenario LEDGER: X = episode recall (outputs a
4-reading sequence), Y = threshold decide (consumes a scalar),
Z = clear/hold settlement decisions on new episodes. Hidden rules are
credit-minus-debit shaped (phase 1: clear iff e0+e1-e2 >= 6), so no
single op from {CPY,ADD,SUB,MAX,MIN} suffices and the correct
intermediate needs 2 composed ops.

## Step 2: Constraints honored

- Unfrozen only. `composition_l3/` and `composition_l3_adv/` (frozen
  builds) touched read-only; the only reads were their sources and
  docs for method.
- learner.zag copied byte-identical from the frozen FORAGE learner;
  sha256 verified equal to
  9317f63c0a72263a533ef9a54b12eed7535dc71a0b202e0c9b14b247fce08e7b
  before and after the build (F-LEARNER-MODIFIED armed).
- Pure Zag. Zero Python invocations (F-PYTHON silent).
- Zero em/en dashes in documentation (byte-verified with grep -P).
- Paper untouched.
- Nothing pushed. Commits local only on tnn-native-lab, explicit
  pathspecs only.
- 0 modes, 0 handlers, 0 semantic cases; op basis {CPY,ADD,SUB,MAX,MIN}
  untouched (F-OP-EXPAND silent).
- No paired X/Y examples, no "combine" hint, no task label. The driver
  teaches X sequences and observed labels; the learner discovers M.
- Commit order: prereg committed alone before any implementation file
  existed.

## Step 3: Development notes

1. Design verification before implementation. The prereg's hand-derived
   expectations were checked with awk re-implementations of the
   learner's scoring semantics (best-threshold sweep t=0..40
   first-max; candidate order op 0..4, d 0..3, s 0..3). Verified:
   phase-1 round 1 baseline 5/8 t=2, ADD R0,R1 unique 7/8 gain 2 t=9,
   all other 19 d=0 candidates <= 7/8 with the 5 earlier-in-order ones
   <= 5/8; round 2 SUB R0,R2 unique 8/8 gain 1 t=6; round 3 stops;
   menu fits (SUM 5/8 t=14, MAX 5/8 t=9, MIN 5/8 t=2, FIRST 5/8 t=2,
   LAST 5/8 t=8) and test scores (3/4,1/4,1/4,3/4,1/4);
   phase-2 M+t=6 scores 2/4, refit 4/4 t=7; phase-3 M(v)+t=7 scores
   6/8, refit best 7/8 t=5, extension ADD R0,R3 unique 8/8 gain 1 t=9.
2. Two design iterations were needed and both were caught by the
   verifier before freezing: (a) the first phase-1 draft let
   SUB R0,R2 reach 8/8 in round 1 (1-op sufficiency, would have voided
   the build); fixed by adding rich episodes with low e0-e2 and poor
   episodes with high e0-e2. (b) the first phase-3 draft let
   CPY R0,R3 reach 8/8 in the extension round (e3 was label-correlated);
   fixed by adding poor episodes with high e3 and very negative v,
   and rich episodes with low e3. A verifier bug (round3 mode falling
   through to round2 base) was also caught and fixed before freezing;
   all numbers above are from the corrected verifier.
3. Episode table strings assembled from the frozen per-episode
   quadruples and cross-checked by decoding: ph1
   "29509148767254239594803517663217", ph2 "8451336967601245", ph3
   "9870896195827673", ph4 "99845455", ph5
   "96608784594173569230009944411188", ph6 "9322555584612228".
4. Build: `cat learner.zag world.zag driver.zag > ledger_full.zag`,
   compiled with the pinned znc to `ledger_bin`. Stdout follows the
   AGENTS.md workaround (one preallocated buffer, single raw-syscall
   write loop; no `_zag_print`). State uses u8 buffers with get32/set32
   only; no `as *i32` slice construction.
5. Output markers: L3-LEDGER-START / L3-LEDGER-END (distinct from the
   FORAGE and RELAY binaries' markers).

## Step 4: Determinism

- No RNG anywhere. Fixed candidate order (op 0..4, d 0..3, s 0..3),
  first-max tie-breaking, ascending threshold sweeps (t=0..40).
- ledger_run1/2/3.txt sha256 identical (hashes recorded in REPORT.md),
  cmp clean both pairs. K-2OP-5 PASS.
