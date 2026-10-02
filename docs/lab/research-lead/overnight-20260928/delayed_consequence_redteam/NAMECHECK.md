# NAMECHECK.md -- Delayed Consequence Red Team Worker

## Step 0: Toolchain Guard (mandatory)

Executed at worker startup, before any other work, via the mandated
setup script:

```
bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
which python3; which python; echo "guard-check-done"
```

Result: the setup script printed
`SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)` and its own
verify lines confirmed python3 and python absent from the safebin
PATH. `which python3` and `which python` afterwards returned NOTHING;
only `guard-check-done` printed. All subsequent work runs with
PATH=$HOME/safebin. znc resolves to the safebin pinned build
(src/tools/toolchain/znc_linux_x86_64_abed8aa1 lineage).

No forbidden executable invoked at any point. Pure Zag via the pinned
znc for all research logic. Shell used only for: safebin setup, file
writes, znc invocation, binary runs, sha256sum, read-only greps, and
git ops.

Compiler lessons applied (from AGENTS.md): u8-backed cells with
ig/is style get32/set32 helpers, never `as *i32` slice construction
in functions; single preallocated output buffer with one
_zag_raw_syscall flush, never _zag_print for dynamic output, stdout
bytes verified; no reliance on .len of cast slices; if-nesting at
most 3 with hoisted sub-conditions; no `!(.. && ..)` in while
conditions (De Morgan rewrites only, grep checked).

## Step 1: Task identity

Delayed Consequence red team worker (subagent, 2026-10-02). Target:
ledger C306 DELAYED-CONSEQUENCE-PASS (prereg c0cff4c48, implementation
f58603a33), the temporal credit assignment machinery
(tamper-evident commitment record, delayed consequence, attribution,
revision). Per Micah's standing rule every success triggers a red
team. Four preregistered attacks: A1 confounded kill, A2 decoy
volatility, A3 record corruption, A4 targeted interference. Verdict
per attack against frozen bars; no global claim.

## Step 2: Scope

`docs/lab/research-lead/overnight-20260928/delayed_consequence_redteam/`
only. The C306 committed files
(docs/lab/research-lead/overnight-20260928/delayed_consequence_eval/)
are read only; the implementation source was copied (hash verified,
recorded below) and never modified. No paper changes. Commits local
only, never pushed. Pure Zag for all research logic. Zero new
edge/MAP types, opcodes, modes, bridges, handlers, semantic cases.
Standalone simulation; TNN core untouched.

## Step 3: Governance notes

- PREREG.md written and committed BEFORE any attack implementation;
  PREREG.md + NAMECHECK.md alone in the prereg commit (hash recorded
  below). No attack code existed at that point.
- Per-attack ATTACK-SUCCEEDS / ATTACK-FAILS bars frozen in PREREG.md;
  no bar moves after results. VOID is terminal.
- Determinism bar: 3 full binary runs byte identical per binary
  (sha256, shell verified).
- No em/en dashes in loop docs (check_no_dash.sh before doc
  commits).
- Learner under test: exact copy of the C306 learner functions from
  commit f58603a33 (sha256
  af3915aa66d935f6d848d456e64d25651ed1df9b691e71082b0510a33ff502a9).
  The unguarded redteam binary reuses those functions verbatim; the
  guarded binary adds only the preregistered checksum guard.
- Redteam prereg commit: 7c1629e97 (PREREG.md + NAMECHECK.md only; no
  attack code existed at that point; verified via git show --stat).
- Attack implementation commit: (recorded after commit)
- REPORT.md: per-attack verdicts against the frozen bars, guard
  proposal with control results, cognition lines touched.
