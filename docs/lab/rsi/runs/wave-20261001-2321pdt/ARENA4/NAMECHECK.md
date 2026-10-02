# ARENA4 NAMECHECK (wave-20261001-2321pdt)

## Step 0 (toolchain guard, mandatory)
- Ran: `sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
- Output: `safebin: /home/hatch/safebin`, `linked: 36 tools`, `znc: OK`, `verify: python3 absent from safebin PATH (OK)`, `verify: python absent from safebin PATH (OK)`, `SAFEBIN-READY`
- Verification: `which python3` printed NOTHING (exit code 1). python3/python absent from PATH.
- Guard status: SATISFIED. Pure Zag constraint in force for this worker.

## Capability pick (recorded before prereg freeze)

Zeros in the v6 refreeze (54/68 = 0.794, 16 capabilities): C8 (n=4),
C9 (n=3), C12 (n=6), C15 (n=1). C8 taken by sibling ARENA lane;
C12 taken twice independently (ARENA2 REMAP 0.882, ARENA3 TRX 0.941);
C9 is the C9BAT lane's on the corrected battery. Not duplicated here.

C15 (goal, n=1, "listnames") AUDITED from the frozen sources
(full evidence in C15_AUDIT.md). The ARENA2 rejection ("1 item,
narrow enumeration, ordering-fragile") is not sustained:
  - The frozen scorer (arena.zag, hash matches refreeze) scores cap
    15 as order-insensitive set F1: sc = 2000*inter/(ne+nr) over
    comma-split names. Ordering-fragile is refuted by the source.
  - 9 of 10 entities are observable in exposure turns (verified by
    grep on the sealed world: "Segunu" occurs 0 times). An
    experience-based roster scores 2000*9/(10+9) = 947 = 0.947 in
    any order. The honest answer is 0.947, not 0.
  - Unlike C9 (only gaming passes; honest mechanism scores 0), C15
    is passable by a general mechanism: a persistent entity roster
    in learner state, built from exposure experience, enumerated to
    satisfy the stated goal. No sealed values, no briefing exploit,
    no format trick.

C15 SELECTED. Mechanism: ROSTER (entity-roster goal enumeration),
built on the v6 base (devint1_contestant_v6.zag); the roster does not
compose with the TRX/INQ candidate line, it is orthogonal, and the
v6 base is the honest substrate. Prereg frozen in
PREREG_ARENA_GOAL.md with kill bars K1-K8.

## Lane-end status (2026-10-01, post sealed evaluation)

- Toolchain re-verified at lane end: `which python3` prints nothing
  (exit 1). Zero non-safebin invocations all lane. No PROCESS-FAIL.
- Verdict: BUILD-PASS. All 8 frozen kill bars pass (SEALED_EVAL.md).
  C15 0.000 -> 0.947; total 54/68 = 0.794 -> 54.947/68 = 0.808;
  zero regressions on the other 15 capabilities; 3/3 byte-identical.
- Commits: 19d9edc87 (prereg+audit, no implementation), 171c45101
  (ROSTER implementation). Commit-order self-check: prereg commit
  strictly precedes implementation commit. Satisfied.
- L3 disclaimed (K8). ROSTER is a CANDIDATE only.
