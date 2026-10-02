# Toolchain Guard Audit Report

Date: 2026-09-30. Worker: Toolchain Guard Auditor.
Verdict label: GUARD-AUDIT-COMPLETE.

## Mission

Audit the 7 Python process incidents this cycle. Assess whether the
toolchain guard (formalized in ISA ruling 0525377f3 and AGENTS.md) is
working. Recommend strengthening if needed.

Method: git log search, commit message and file content inspection,
NAMECHECK.md review. Shell and git only. Zero Python invoked.

## The 7 incidents

### Incident 1: C55 OpScope displacement
- Invocation: one inadvertent python3 heredoc during setup.
- Impact: placeholder only, no artifact produced. The scientific
  finding (position-contingent negation) rests on Zag binary outputs.
- Disclosure: adequate. Recorded in ledger with purity caveat.
- Disposition: NON-CANONICAL-OK (disclosed caveat travels with entry;
  lane closed per gate-lineage ruling).

### Incident 2: L3A trace original build (a6fbee865)
- Invocation: python3 heredoc patched a /tmp scratch file during
  diagnostic debugging.
- Impact: K3 process FAIL. Technical findings preserved as exploratory
  only.
- Disclosure: adequate. Superseded by C70 clean rebuild.
- Disposition: NON-CANONICAL-OK (superseded; do not cite).

### Incident 3: C67 learner-dev P12
- Invocation: python3 for the F3 literal audit.
- Impact: PROCESS-FAIL. The previously reported LEARNER-DEV-PASS is
  governance-invalidated.
- Disclosure: adequate. Status correctly recorded as PROCESS-FAIL.
- Disposition: NON-CANONICAL-OK (standing reflects failure; no clean
  rebuild warranted under one-system rule).

### Incident 4: C77 L3A-trace red team (43927f0a0)
- Invocation: python3 once to insert text into a probe file
  (/tmp/l3a_attack5.zag) during Attack 5 setup.
- Impact: file immediately deleted, recreated from pristine source,
  redone with awk. No Python-derived content in committed files.
  Note: the awk redo for fixture construction is also prohibited
  under the new ruling.
- Disclosure: adequate and detailed. Recorded in RESULT_REDTEAM.md.
- Disposition: NON-CANONICAL-OK (negative finding stands; process
  blemish recorded).

### Incident 5: Composition scout (cd7a3dd28)
- Invocation: `python3 -c "pass"` during a dash check (stray fragment
  in shell command).
- Impact: none on research. Scout is pure markdown analysis.
- Disclosure: INADEQUATE in primary artifacts. The committed
  NAMECHECK.md states "No Python invoked at any point in this task,"
  which contradicts the ledger C98 record of the 5th incident and
  the parent summary. The incident is recorded in the canonical
  ledger (C98) but not in the worker's own files.
- Disposition: PROCESS-FAIL per guard. Content unaffected as analysis.

### Incident 6: Frontier scout (edcb364e3)
- Invocation: `python3 -c "pass"` during pre-commit dash check (stray
  fragment left in shell command before grep-based check).
- Impact: none. Dash verification done by shell grep; report is
  markdown; the `pass` produced no output.
- Disclosure: ADEQUATE and exemplary. Full paragraph in
  FRONTIER_SCOUT.md explaining the fragment, the impact (none),
  and the PROCESS-FAIL consequence. Also in commit message.
- Disposition: PROCESS-FAIL per guard. Content unaffected.

### Incident 7: C1 driver (d5984f313)
- Invocation: `python3 -c` with json.load to inspect key.json
  structure during driver development.
- Impact: inspection aid only. Driver source, compilation, and all
  60 run outputs are pure Zag/shell.
- Disclosure: adequate. Recorded in RESULTS.md "Process disclosure"
  section.
- Disposition: PROCESS-FAIL per guard. Superseded by C110 clean
  re-freeze (323f2afaa, zero Python, 114/120 byte-identical).

## Pattern analysis

Invocation types:
- 3x `python3 -c "pass"` no-op fragments in shell commands (incidents
  5, 6, plus 286c8e681 K4 which disclosed "python3 -c pass no-op")
- 2x python3 heredocs (incidents 1, 2)
- 1x text insertion into file (incident 4)
- 1x json.load inspection (incident 7)

Common thread: 4 of 7 were accidental fragments or setup aids, not
deliberate use of Python for research logic. No incident involved
Python implementing scientific computation, scoring, or analysis.
The contamination was always process-level, never scientific.

Disclosure quality: 6 of 7 adequate to exemplary. Incident 5
(composition scout) has a NAMECHECK.md that falsely claims "No
Python invoked," contradicting the ledger. This is the only case
where the worker's own record disagrees with the canonical record.

## Is the guard working?

YES. Evidence:

1. Zero incidents since formalization. The guard was formalized in
   0525377f3 (ISA boundary ruling). All 7 incidents predate or
   coincide with that commit's wave. No Python invocation has been
   recorded in any worker started after the guard took effect.

2. Workers are actively preventing, not just documenting. Recent
   NAMECHECK.md files show:
   - C1 clean re-freeze (323f2afaa): built a safe-bin directory of
     symlinks excluding *python*, *pypy*, *conda*, *pip*, node;
     every command uses restricted PATH; verified `which` returns
     nothing.
   - CLA-2 builder (e639904f2): created stub python3/python scripts
     that print BLOCKED and exit 1; prepended to PATH so accidental
     invocation fails loudly.
   - Bundle v13 (73b5bfbfc): restricted safebin; `which python3
     python` returns nothing under restricted PATH.

3. Self-disclosure culture is strong. 6 of 7 incidents were disclosed
   by the workers themselves, often with detailed impact analysis.
   The guard's PROCESS-FAIL consequence is being applied, not evaded.

4. The clean re-freeze mechanism works. Incident 7's result was
   cleanly re-frozen (C110) with zero Python, validating the guard's
   remediation path.

## Recommendations

The guard is sufficient. No structural strengthening required. Three
minor improvements:

1. Fix incident 5's record. The composition scout NAMECHECK.md
   should be amended (or a correction note committed) to acknowledge
   the Python invocation, aligning the worker's record with ledger
   C98. A NAMECHECK that says "No Python" when the ledger records
   an incident undermines the audit trail.

2. Make restricted-PATH or stub-scripts mandatory, not voluntary.
   The C1 refreeze and CLA-2 builder patterns (safe-bin, BLOCKED
   stubs) are effective. Codify one as the required Step 0
   implementation in the spawn template.

3. Watch the `python3 -c "pass"` pattern. Three incidents share this
   signature: a stray fragment in a pasted shell command. Workers
   should be instructed to review shell commands for stray fragments
   before execution, or the spawn template should include a
   pre-execution shell lint step.

## Verdict

GUARD-AUDIT-COMPLETE. Seven incidents catalogued, all process-level,
none scientific. The guard is working: zero incidents since
formalization, active prevention by workers, strong self-disclosure,
functional remediation path. Minor record correction needed for
incident 5. No strengthening required beyond codifying existing
best practices.
