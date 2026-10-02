# NAMECHECK.md: STRUCT-COMPOSITION -- Structure-Transforming Composition

Worker: Structure-Transforming Composition Worker (subagent).
Date: 2026-10-02. Branch: tnn-native-lab (local commits only, no push).

## Step 0: Toolchain guard (mandatory)

Setup executed 2026-10-02 before any other work:
  mkdir -p $HOME/safebin
  for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum
      git-receive-pack git-upload-pack; do
    p=$(which $t 2>/dev/null | head -1)
    [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
  done
  export PATH="$HOME/safebin"
  which python3 python 2>/dev/null; echo "guard-check-done"
Result: `which python3 python` printed nothing; only "guard-check-done".
No python3/python in the safebin PATH. Guard recorded here.
All computation is pure Zag via the pinned znc
(`znc 2026.07.0-dev (edition 2026)`); shell used only to invoke znc,
move/copy files, and run git/sha256sum.

## Commit-order self-check

- PREREG.md first commit: <to record: hash>
  (must strictly precede any implementation commit)
- Implementation commit: <to record: hash>
- REPORT.md commit: <to record: hash>
Self-check: PASS only if the prereg commit timestamp/hash precedes the
implementation commit. No result was obtained before the prereg commit.

## Base / port hashes (read-only references, never copied or edited)

- composition_A/cx_core.zag:
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
  (matches xdomain_causal REPORT.md; substrate only: tnn2_init,
  ev_teach, ev_query, ng/ns/hg, z_alloc, get32/set32, emit/e64.
  No composition core is used: the prototype is a new operator.)
- sc_full.zag = cx_core.zag (verbatim) + sc_driver.zag (new).

## Build / run log

- Compile: znc sc_full.zag -> sc_bin (warnings only expected).
- Runs: sc_run1.txt, sc_run2.txt, sc_run3.txt; sha256 recorded below.
- Em/en dash byte check: grep -P for U+2013/U+2014 over all
  worker-authored files must return nothing.

Run hashes: <to record>

## Scorecard (from REPORT.md)

K1 COMPETENCE / K2 SURGERY / K3 ABLATION / K4 GENERALITY /
K5 IRREDUCIBILITY / K6 DEGENERATE / K7 AUDIT / K8 DETERMINISM:
<to record>
