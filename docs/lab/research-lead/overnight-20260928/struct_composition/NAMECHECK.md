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

- PREREG.md first commit: dfa75105fc05b3408c0c87bfb0a11c505917b1e9
  (frozen before any implementation file existed)
- Implementation + REPORT commit: 266b95b393eacf4c88b64bd5da3c54bb52550010
- Self-check: PASS. sc_driver.zag was written after dfa75105; no
  result was obtained before the prereg commit. (One build failure
  occurred post-prereg: ev_query lives in cx_patch.zag, not the
  substrate base; the assembly was corrected to
  cx_core + cx_patch + sc_driver, both bases verbatim and
  sha256-verified.)

## Base / port hashes (read-only references, never copied or edited)

- composition_A/cx_core.zag:
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
  (substrate: tnn2_init, ev_teach, ng/ns/hg, z_alloc, get32/set32,
  emit/e64. No composition core is used by the prototype.)
- composition_A/cx_patch.zag:
  c7074c5928040014900f0a2eea8595f19074cfaf420b0632b2b8fd45977bcf12
  (matches the hash recorded in xdomain_causal/NAMECHECK.md; used
  ONLY for ev_query, the learner's own trial/rebind engine, in the
  K1 competence census. The prototype mechanism sc_do never calls
  compose_try, rebind_try, or any composition function.)
- sc_driver.zag (new, 497 lines, 46 comment lines):
  5dbb39fb6284b68f5d7c92d261f30b88cd33d2ad4333befcbe0e03b5b4360dcc
- sc_full.zag = cx_core.zag + cx_patch.zag + sc_driver.zag (verbatim
  concatenation):
  92fa47ccc67daeda09d27a0793c96dd721af69adcd19d47e28d5bc2f2ddfc6ed
- sc_bin (pinned znc 2026.07.0-dev, warnings only, exit 0):
  b9d8764b5d00c2c743462b495380f81485e0eed2b0f11d201d68b32465a8abd5

## Build / run log

- Compile: `znc sc_full.zag -o sc_bin` -> sc_compile.txt, warnings
  only (A0102 ignored-return-value notes, all from the verbatim
  bases), exit 0.
- Runs: sc_run1.txt, sc_run2.txt, sc_run3.txt.
- Em/en dash byte check: grep for U+2013/U+2014 over all
  worker-authored files returns nothing (the only hits are znc's own
  warning text inside sc_compile.txt, which is compiler output, not
  authored content).

Run hashes (3/3 byte-identical):
  f0374f3dc73c9393a958b5620b5b4f14158d9a7f0a8d79a606c3b430d779096c
  (sc_run1.txt, sc_run2.txt, sc_run3.txt all identical)

## Scorecard

- K1 COMPETENCE: PASS. X1=3 (trial, tried=2 rejected=1), X2=6
  (rebind), Y1=1 (trial, tried=2 rejected=1), Y2=2 (rebind); trial
  stats identical to xdomain K1.
- K2 SURGERY: PASS. TREAT Z answers exactly (5,3,6,4).
- K3 ABLATION: PASS. ABL-NOEDGE, ABL-NOEQ, ABL-NOOBS, FRESH all give
  -2 on every Z query with STRUCT-MISSING emitted.
- K4 GENERALITY: PASS. GEN arm gives exactly (3,0) with unmodified
  operator code on a new structure (Q=2*P, R=P+Q), a new
  intervention target (middle variable Q), and a root intervention
  (do(P=0), surgery no-op).
- K5 IRREDUCIBILITY: PASS. IRRED arm gives exactly (4,2) on Z1,Z4
  with value facts identical to TREAT (same X/Y facts, same units,
  same trial stats; only edge (801,71,803) and term (803,72,8011)
  deleted).
- K6 DEGENERATE: PASS. DEGEN arm gives exactly 7 (no intervention,
  single-edge graph).
- K7 AUDIT: PASS. Surgery record shows SEVER 801->802, TOPO
  [802,801,803], VALS 802=2 801=1 803=5, answer 5.
- K8 DETERMINISM: PASS. 3/3 byte-identical.
