# LEARNER-REVERT-PASS: P11 law-change-then-revert inside the lifetime

Date: 2026-09-30 PDT. Worker: Law-Revert Integration Worker.
Verdict: LEARNER-REVERT-PASS (bounded L2).

## What was built

revert_learn.zag extends the composed learner (integrate_learn.zag at
d1305bd43, copied verbatim) with a P11 episode. The only new code:

1. load_r1b: a verbatim copy of the frozen load_r1 loader writing entry
   6 instead of 5, so the STATIC control runs the same frozen R1 case
   (G0,G1,G0) at a second ledger entry in the same binary.
2. The P11 driver in main(), appended after emit_stage_hash(W,10):
   ADAPT episode at e5 (mode 2), STATIC control at e6 (mode 3),
   persistence of the re-derived law as rule-store facts (910,1,0),
   (911,1,4), (912,1,2) each earned 3x to importance 31, a 20-item
   pressure wave (subj 600..619, rel 99, unproven), delayed probes, and
   emit_stage_hash(W,11).

No other line of the P1-P10 code was touched. One learner, one
32768-byte state, one main(), no resets.

## Kill-bar results

K1 (prereg strictly first): PASS. Prereg daf4f015d committed alone;
git merge-base --is-ancestor daf4f015d <impl> verified before the
implementation commit.

K2 (no regression + all four P11 predictions): PASS.

(a) No regression: RUN1.txt lines 1-143 (PHASE P1 through STATEHASH P10)
    are byte-identical to INTEGRATION_RAW_OUTPUT.txt at d1305bd43
    (verified by head+cmp). The only delta is the appended P11 region.

(b) ADAPT re-derives post-revert, exactly the frozen R1 trace:
    ADAPT e5 P0 RESOLVED winner=h0 rounds=1
    ADAPT e5 P1 RESOLVED winner=h1 rounds=2
    ADAPT e5 P2 RESOLVED winner=h0 rounds=1
    P11_ADAPT_W0=0, W1=1, W2=0; per-phase rounds 1,2,1;
    P11_ADAPT_ROUNDS=4; P11_ADAPT_Q (dquery e5,1,1)=1.
    The learner tracks the law through the change and back, re-deriving
    h0 in 1 round after the revert instead of sticking with h1.

(c) STATIC exhibits the C1-pathology, exactly the frozen signature:
    STATIC e6 P0 RETIRE h1; RETIRE h2; RESOLVED winner=h0 rounds=1
    STATIC e6 P1 SINGLE winner=h0 rounds=0 (misresolve: true law G1)
    STATIC e6 P2 SINGLE winner=h0 rounds=0 (accidentally right)
    P11_STATIC_W0=0, W1=0, W2=0; P1/P2 rounds=0. Permanent
    cross-episode retirement with zero intervention rounds after the
    change: the pathology the ADAPT design exists to avoid.

(d) Post-revert persistence: P11_CAUSAL 3/3, P11_FOUNDATION 8/8,
    P11_CORR 2/2 after the 20-item pressure wave.

K3 (purity/determinism): PASS. Pure Zag, zero Python (pinned znc build;
shell/grep/awk/cmp/sha256sum/mktemp analysis only). 3/3 byte-identical
runs (sha256 60762e2fada30a375b31e1d8e8d20c23d6a8373b8d9c91a1c6d31851f1082870),
exit 0, zero stderr. No em dashes (shell-only check_no_dash.sh). u8-backed
cells only; no as *i32 slices in functions. STATEHASH ticks strictly
increasing P1-P11 (16..337). Contaminated paper untouched (empty diff).

## What this shows, plainly

The composed learner now survives a law change and its revert inside one
unbroken lifetime: it re-derives the original hypothesis after the revert
in 1 round, persists the re-derived law as earned rule-store facts, and
retrieves all three after a further pressure wave with foundation and
corrections intact. The STATIC control in the same binary demonstrates
the exact failure mode that monotonic retirement would have produced.
Scope stays bounded L2: the candidate graphs are researcher-supplied;
the learner selects and re-selects among them, it does not invent a new
graph form. No L3 claim is made.

## Provenance note

Two live .git/index.lock encounters during the prereg commit (concurrent
workers committing); waited and retried per the rules, never removed.
The prereg commit daf4f015d contains exactly the two prereg files.
