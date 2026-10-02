# NAMECHECK: Grammar Third-System Worker

## Step 0: Toolchain Guard (2026-10-02)

Safebin activated:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING. Guard check done.
No Python, no forbidden executables in PATH. Pure Zag for all research
computation. Shell only for: invoking znc, running binaries, git ops,
file moves/copies, checksums, diffs.

## Worker identity

Grammar Third-System Worker. Mission: design EXL3 breaking exactly ONE
of the transfer report's explicit machinery assumptions, run the
byte-identical induction machinery on it, and diagnose which assumption
is load-bearing. Unfrozen variant only. Frozen read-only.

## Assumption broken

EXL3 breaks assumption (3) only: pair decoding assumes P(a,b) = a*16+b.
EXL3 uses P(a,b) = a*8+b with literals 0..7 (injective: 8(a1-a2)=b2-b1
forces a1=a2 since |b2-b1|<=7<8; P in 0..63 unique per pair).
Preserved: assumption (1) eval lookup references 41/42 (SUB=41, DIV=42,
same constraint shapes as EXL2); assumption (2) rubric references 43/44
(DSUB=43, DDIV=44) with literal range 0..9 (world literals 0..7 lie
inside it). BUILD=45. TRAIN {1,3,5,7} with alternating DIV-first/SUB-first
canonical examples (4 BUILD facts); TEST {0,2,4,6} (4 novel targets).

## Files

- g3_base.zag: byte copy of grammar_transfer/gt_base.zag.
  SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
  (matches source; 2 files share this digest).
- g3_patch.zag: byte copy of grammar_transfer/gt_patch.zag.
  SHA-256 ae94800e0167d72aaba3879216699c3be2fbdc5d7c60eeea62428594c3db50d3
  (matches source; 2 files share this digest). THE machinery-identity proof.
- g3_driver.zag: experiment driver. Teaching section rewritten for EXL3
  (g3_P = a*8+b, literal loops 0..7, g3_dsub/g3_ddiv/g3_teach_decomp/
  g3_canon_build/g3_teach_build/g3_teach); arm functions
  gi_report_grammar, gi_arm_induce, gi_arm_base, gi_arm_hardcode
  byte-identical to gt_driver.zag (verified per-function with cmp);
  gi_test_targets uses EXL3 targets {0,2,4,6}; main runs W1-W4
  (INDUCE, ABLATE, HARDCODE, FRESH); W5a/W5b contradiction arms dropped
  (already passed on byte-identical machinery in the transfer run).
- g3_build.sh: assemble + compile with pinned znc.
- g3_full.zag: concatenated build input (generated).
- g3_compile.txt: compiler output.
- g3_bin: compiled binary.
- g3_run1.txt, g3_run2.txt, g3_run3.txt: 3 deterministic runs,
  byte-identical (SHA-256 b16383700c8acb696542bdda9d17ee7d3f0582753160b991e67fc20866a1ed5c).
- REPORT.md: assumption-breakage analysis and verdict.

## Constraints observed

- Pure Zag. Zero em/en dashes in docs.
- 0 modes/bridges/handlers. 0 new semantic cases. 0 base modifications.
- Machinery byte-identical: base and patch are copies; arms verified
  identical per function; driver diff confined to teaching functions,
  pair encoder, test battery, and main (same confinement rule as the
  transfer worker).
- No generalization implemented (diagnosis only, per task).
- Nothing pushed. Commits local only.
