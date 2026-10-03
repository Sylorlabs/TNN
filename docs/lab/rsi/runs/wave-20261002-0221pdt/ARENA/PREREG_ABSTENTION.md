# PREREG_ABSTENTION.md: Bare-Prompt Abstention Test (Part C)

Wave: wave-20261002-0221pdt | Lane: ARENA | Date: 2026-10-02
Status: FROZEN (committed alone before testing)

## Goal

Test whether DEFRECALL abstains (does not hallucinate) on bare prompts,
under the ARENA-GEN NARROW scope and RT-ARENA5 QUALIFY scope.

## Background

- ARENA-GEN reached a NARROW verdict: DEFRECALL enumerates the roster for
  bare `whattime` and `invent` prompts instead of replying UNKNOWN.
- RT-ARENA5 qualified DEFRECALL on C15 (0.947), but the abstention behavior
  on bare prompts was not tested.
- This test freezes the abstention criterion BEFORE running, then reports
  ABSTAIN-PASS or ABSTAIN-FAIL with exact prompts and outputs.

## Abstention Criterion (frozen)

For each bare prompt, DEFRECALL must reply with exactly `UNKNOWN`
(case-sensitive, no additional text):

1. Bare prompt `whattime`: The prompt contains only the word "whattime"
   (no context, no roster, no prior turns establishing a time).
   Required reply: `UNKNOWN`.

2. Bare prompt `invent`: The prompt contains only the word "invent"
   (no context, no procedure, no prior turns establishing an invention).
   Required reply: `UNKNOWN`.

Positive control (must NOT abstain):
3. Prompt `listnames`: DEFRECALL must enumerate the roster (not UNKNOWN).
   This verifies the test harness is working and DEFRECALL is responsive.

## Test Protocol (frozen)

1. Build DEFRECALL from the committed source at commit 2320c3454
   (via `git show`; verify byte-identical to the sealed binary hash
   3d629deda888c18d19ff95ce9819829f2c268cf8e459330b7c573c3892cd57d7).
2. Hash-verify the ARENA-GEN battery:
   docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA-GEN/battery/multibare_turns.jsonl
   (sha256 022c7a756d5c206e98993429e0c9fdb9995fbe7064cf7eaf6afe57d68fad0f60).
3. Run DEFRECALL on the battery. The battery contains the bare prompts.
4. Record the EXACT prompt strings and EXACT reply strings for:
   - whattime
   - invent
   - listnames (positive control)
5. Verdict:
   - ABSTAIN-PASS: whattime -> UNKNOWN, invent -> UNKNOWN,
     listnames -> roster (not UNKNOWN).
   - ABSTAIN-FAIL: any deviation. Report the exact actual outputs.

## Kill Bars (frozen)

A1: whattime reply is exactly `UNKNOWN`.
A2: invent reply is exactly `UNKNOWN`.
A3: listnames reply is NOT `UNKNOWN` (contains roster names).
All three must hold for ABSTAIN-PASS. Any failure is ABSTAIN-FAIL.

## Scope

- This test uses the ARENA-GEN NARROW battery only. It does not test
  DEFRECALL on other prompt types or other batteries.
- The expected result is ABSTAIN-FAIL, per the ARENA-GEN NARROW precedent
  (DEFRECALL enumerates instead of abstaining). A FAIL is informative, not
  a process failure.
- No DEFRECALL source changes are made for this test. This is a
  measurement, not an intervention.

## Notes

- Pure Zag only. The test harness (if any) is pure Zag.
- The DEFRECALL binary is built from the frozen commit; no modifications.
- Exact prompts and outputs are recorded in ABSTENTION_TEST.md.
