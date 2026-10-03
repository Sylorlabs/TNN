# PREREG: F3 REVISE Step-9 Re-audit (Pipeline Step 11 Follow-up)

Status: FROZEN. This prereg is committed alone before any re-audit
analysis document exists. K1.

## Parent chain

- Step-9 transfer (contaminated): c3c3e3bc8 (REVISE-TRANSFER-PASS,
  K4 breach: one stdout-only `python3 -c` hex-to-decimal calculator
  disclosed).
- Step-10 red team: 4a2b8ef43 (REVISE-REDTEAM-KILLS generic reading;
  flagged the step-9 breach).
- Step-11 governance audit: 85fe2043c (REVISE-AUDIT-FAIL; A3 fails at
  step 9; steps 1-8 and 10 governance-clean; remedy prescribed: pure-Zag
  re-run under a new frozen prereg).
- Clean re-run prereg: 6f95d7b1c (frozen alone).
- Clean re-run result: 53b9a9a27 (REVISE-TRANSFER-PASS, zero Python).

## Scope of this re-audit

Narrow by design. The re-audit re-verifies ONLY whether the clean
re-run remediates the step-9 K4 breach flagged at A3 in 85fe2043c.
It does not re-litigate any other audit finding (A1 ancestry of steps
1-8/10, A2 verdict integrity, A4 disclosure, A5 blemish chain, A6
amendment discipline all stand as reported in 85fe2043c).

## Frozen checks (document review; no new runs)

- R1: Prereg 6f95d7b1c strictly precedes result 53b9a9a27
  (`git merge-base --is-ancestor`); prereg commit contains only the
  prereg file.
- R2: Zero Python invocation in the clean re-run: no `python` token in
  any build script, run harness, or command artifact of 53b9a9a27;
  disclosure mentions only in prose; build stderr has no python
  tracebacks.
- R3: World files byte-identical to the contaminated step-9 artifacts
  (via `git show` + `cmp`), so the remediation copies bytes, it does
  not recompute any constant by any tool.
- R4: Run logs 3/3 byte-identical per configuration with md5s matching
  the committed result doc and zero stderr bytes.
- R5: Verdict rule applied as frozen (V0, V1, T1-T4, C1-C3, D1); no bar
  moved after results.
- R6: All 23 files under the owned pathspec
  docs/lab/research-lead/overnight-20260928/revise_transfer_clean/;
  no pathspec leak.

## Verdict rule (frozen, no reinterpretation)

- REVISE-REAUDIT-PASS iff R1, R2, R3, R4, R5, R6 all hold.
- Any failure yields REVISE-REAUDIT-FAIL and names the failed check.

## Honest scope

A PASS restores a K4-clean REVISE-TRANSFER-PASS for the narrowed
bounded-L2 reuse characterization; it claims no L3 and no Criterion 0,
and it does not overturn step-10 REVISE-REDTEAM-KILLS. Step-11
REVISE-AUDIT-FAIL remains the governing audit verdict except where
this re-audit explicitly remediates step 9.

## Kill bars for this re-audit step

- K1: This prereg frozen alone before any re-audit analysis exists.
- K2: All six frozen checks executed against committed evidence.
- K3: Audit is document review; zero Python at every stage; shell-only
  dash check on new files.

## Standing rules (Step 0 name-check from LOOP_STATE.md)

Pure Zag only; no Python at any stage of this re-audit (authoring,
analysis, byte checks); shell-only check_no_dash.sh for dash bytes;
no em/en dash bytes in new files; commits local on tnn-native-lab;
owned pathspec
docs/lab/research-lead/overnight-20260928/revise_reaudit/ only;
nothing pushed; the contaminated research paper is not touched.
