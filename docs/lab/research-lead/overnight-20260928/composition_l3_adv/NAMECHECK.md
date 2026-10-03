# NAMECHECK.md -- Composition L3 Red-Team Worker (adversarial RELAY)

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
file concatenation, read-only greps, and shell-arithmetic verification
of the prereg's hand-derived design numbers (design check only; no
research logic outside Zag).

## Step 1: Task identity

Composition L3 Red-Team Worker (subagent, 2026-10-02). Mission: red-team
the COMPOSITION-L3-COMPLETE claim with an independent
adversary-designed world family (RELAY), per Micah's C0-C (sealed
post-freeze worlds, at least one evaluation family designed by an
independent adversary). The L3 mechanism (`learner.zag`) runs UNMODIFIED
(byte-identical copy, sha256-pinned); only the world is new.
Scenario RELAY: X = episode recall (outputs a 4-reading sequence),
Y = threshold decide (consumes a scalar), Z = open/closed decisions on
new episodes. Hidden rules are difference-based (phase 1: open iff
e0 - e1 >= 4), so the FORAGE sum-shaped intermediate cannot transfer;
the learner must discover `SUB R0,R1` through experience.

## Step 2: Constraints honored

- Unfrozen only. `composition_l3/` (frozen FORAGE build) touched
  read-only; the only reads were its sources and docs for method.
- learner.zag copied byte-identical; sha256 verified equal to the
  frozen FORAGE learner hash before and after the build
  (F-LEARNER-MODIFIED armed).
- Pure Zag. Zero Python invocations (F-PYTHON silent).
- Zero em/en dashes in documentation (byte-verified with grep -P).
- Paper untouched.
- Nothing pushed. Commits local only on tnn-native-lab, explicit
  pathspecs only.
- 0 modes, 0 handlers, 0 semantic cases; op basis {CPY,ADD,SUB,MAX,MIN}
  untouched (F-OP-EXPAND silent).
- No paired X/Y examples, no "combine" hint, no task label. The driver
  teaches X sequences and observed labels; the learner discovers M.
- Commit order: prereg committed alone (10389d72e) before any
  implementation file existed.

## Step 3: Development notes

1. Design verification before implementation. The prereg's hand-derived
   expectations were checked with shell arithmetic (two-pass: an
   initial verifier had a bash `local a=1 b=$a` pitfall that corrupted
   MAX/MIN values; rewritten with separate declarations and all
   numbers re-derived). Verified: phase-1 round 1 baseline 6/8 t=4,
   SUB R0,R1 unique 8/8 gain 2 t=3, all other 19 d=0 candidates <= 6/8;
   all 80 phase-3 extension candidates (unique 8/8 winner ADD R0,R3,
   gain 3, t=8; runner-up MIN R0,R3 7/8); menu fits and test scores;
   phase-2 refit 4/4 t=5; phase-3 refit best 5/8. One hand slip caught:
   MIN train fit is 4/8 t=0, not 5/8 t=1 (0 >= 1 is false); prereg
   records the corrected 4/8.
2. Episode table strings assembled from the frozen per-episode
   quadruples and cross-checked by decoding in the verifier: ph1
   "50996122407383119705764435882166", ph2 "7250981950376422", ph3
   "8142930573815529", ph4 "92634311", ph5
   "91027053621583449200831140925425", ph6 "9203517184256534".
3. K-ADV-2 audit pattern `threshold.*=.*3` (candidate during design) hit
   one benign comment line in learner.zag (adapt code listing); it was
   replaced before freezing by the precise patterns
   `set32(st,236,3)` and `set32(st,228,3)`, both 0 hits. All 8 frozen
   patterns return 0 on the copied learner.zag.
4. Build: `cat learner.zag world.zag driver.zag > relay_full.zag`,
   compiled with the pinned znc to `relay_bin`. Stdout follows the
   AGENTS.md workaround (one preallocated buffer, single raw-syscall
   write loop; no `_zag_print`). State uses u8 buffers with get32/set32
   only; no `as *i32` slice construction.
5. Output markers: L3-RELAY-START / L3-RELAY-END (distinct from the
   FORAGE binary's markers).

## Step 4: Determinism

- No RNG anywhere. Fixed candidate order (op 0..4, d 0..3, s 0..3),
  first-max tie-breaking, ascending threshold sweeps (t=0..40).
- relay_run1/2/3.txt sha256 identical (hashes recorded in REPORT.md),
  cmp clean both pairs. K-ADV-7 PASS.
