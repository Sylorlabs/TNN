# NAMECHECK.md -- DCE-V2 Integration Worker

## Step 0: Toolchain Guard (mandatory)

Implementation worker startup record (2026-10-02; the text below
describes the prereg commit only and is kept for the record). Executed
before any other work, via the mandated inline setup:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null); [ -n "$p" ] && ln -sf "$p" $HOME/safebin/$t 2>/dev/null
done
export PATH="$HOME/safebin"
```

Result: afterwards `which python3` returned NOTHING (rc=1) and
`which python` returned NOTHING (rc=1); the safebin PATH contains only
the allowed tools. All subsequent work runs with PATH=$HOME/safebin.
znc resolves to the pinned build via the safebin symlink
($HOME/safebin/znc -> src/tools/toolchain/znc_linux_x86_64_abed8aa1).

No forbidden executable invoked at any point. Pure Zag via the pinned
znc for all research logic. Shell used only for: safebin setup, file
writes, znc invocation, binary runs, sha256sum, read-only greps/diffs,
and git ops.

Compiler lessons applied (from AGENTS.md): u8-backed cells with
get32/set32 little-endian helpers, never `as *i32` slice construction
in functions (grep clean); single preallocated output buffer with one
_zag_raw_syscall flush, never _zag_print for dynamic output (grep
clean), stdout bytes verified; no reliance on .len of cast slices;
flat if-nesting with hoisted flags; no `!(.. && ..)` in while
conditions (grep clean).

Prereg worker note (from the frozen prereg commit, kept verbatim):
the prereg worker ran
bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh,
exported PATH=$HOME/safebin, and confirmed python3 and python absent
(SAFEBIN-READY, 36 tools, no python).

## Step 1: Task identity

DCE-V2 integration worker (subagent, 2026-10-02). Adoption step:
integrate the C309 red-team guard (learner_phase4_record_checked,
16 lines, GUARD-EFFECTIVE with zero overreach) INTO the C306
delayed-consequence mechanism as a permanent P4-entry step. V2
supersedes V1 with the guard built in (not a const-flag variant).
Re-verify the full C306 battery (D1-D4, K1-K10), re-run red-team
attacks A1-A4 against V2, add new arm A5 (partial corruption of a
non-id record field, not run by the red team).

## Step 2: Scope

`docs/lab/research-lead/overnight-20260928/delayed_consequence_v2/`
only. The C306 committed files
(docs/lab/research-lead/overnight-20260928/delayed_consequence_eval/)
and the C309 red-team files
(docs/lab/research-lead/overnight-20260928/delayed_consequence_redteam/)
are read only: copied, hash verified, never modified. No paper
changes. Commits local only, never pushed. Pure Zag for all research
logic. Zero new edge/MAP types, opcodes, modes, bridges, handlers,
semantic cases. Standalone simulation; TNN core untouched.

## Step 3: Governance notes

- PREREG.md written and committed BEFORE any implementation;
  PREREG.md + NAMECHECK.md alone in the prereg commit (hash recorded
  below). No implementation code existed at that point.
- K1-K10 bars copied verbatim from the C306 prereg (commit c0cff4c48);
  A1-A4 attack bars copied verbatim from the DCRT prereg (commit
  7c1629e97). The prereg is self-contained: no silent inheritance.
- Frozen V2 bars: V2-REG (C306 regression), A3Q (A3 now quarantines),
  A5Q (new arm), G-IDENT (guard logic byte-identical to the red-team
  guarded copy, diff verified), MACH-0 (0 new machinery beyond the
  16-line guard), K7 (3/3 byte-identical runs, sha256), COMMIT-ORDER
  (prereg commit strictly precedes implementation).
- Verdict DCE-V2-COMPLETE iff all frozen bars pass. VOID is terminal.
- No em/en dashes in loop docs (check_no_dash.sh before doc commits).
- This adopts the guard into the experimental mechanism only;
  promotion to any frozen base is out of scope (banked for Micah).
- Redteam prereg commit: 7c1629e97.
- Redteam implementation commit: f58e3eabd.
- DCE-V2 prereg commit: e5e350bb0 (PREREG.md + NAMECHECK.md only;
  verified via git show --stat: 2 files, 357 insertions).
- DCE-V2 implementation commit: <to be recorded after commit>.
- COMMIT-ORDER self-check: e5e350bb0 must be an ancestor of the
  implementation commit (git merge-base --is-ancestor); the prereg
  commit strictly precedes the implementation commit. Recorded after
  the commit lands.
- REPORT.md: per-bar verdicts against the frozen bars, guard-identity
  diff evidence, per-arm verdicts, cognition lines added.
