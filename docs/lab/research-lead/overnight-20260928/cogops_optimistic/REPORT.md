# REPORT: COGOPS-OPTIMISTIC (optimistic efficiency selection)

Date: 2026-10-03. Worker: COGOPS-OPTIMISTIC.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_optimistic/`
Prereg: frozen commit 32c6799b9 (PREREG.md + NAMECHECK.md,
committed alone before any implementation file existed).
Implementation commit follows this report.

## Verdict: BUILD-PASS (K1..K14 all PASS, with transparent errata E1, E2)

The selection rule is now score(s) = (wins(s)+1)/(cost(s)+1)
with exact integer cross-multiplication. The landscape answers
the follow-up question directly: **untried WHOLE EARNS THE
LEAD.** On the fresh lag-2 full oscillation (S5, goal 820),
WHOLE leads at initial selection (DET-STRAT chosen=2, 1.0 >
2/3 strictly) and verifies in 1 comparison; under the
controlled lesion (S14, goal 825) it is the STRICT optimistic
argmax (1.0 > 3/7 > 1/5 > 1/9, not an id tie-break) and wins
in 1 comparison. Under pure efficiency this was structurally
impossible (untried scored 0); the preregistered structural
ceiling is lifted exactly as predicted.

Lead is not win: on the lesioned period-3 goal (S13), WHOLE
leads outright (chosen=2), fails at pass 2 (lag 3
inapplicable, 1 CMP), and ALT rescues via its PW-form at lag 3
(SWITCH 2->4). Optimism's promotion is falsifiable per
episode, as preregistered (P4).

The over-exploration tax is real, bounded, and measured (P5):
S8's untried ALT leads (chosen=4) and its PW-form fails (2
CMP) before its NEED-form wins (6 events vs 4 for
NEED-direct); S13's failed WHOLE lead costs 1 CMP. Across the
battery the tax does not dominate: S3..S13 log 68 comparison
events under optimism vs 70 under COGOPS-COSTAWARE. The one
large optimism cost is second-order (P7): the optimistic S7
hypothesizes at q=1 where costaware hypothesized at q=2, so
the stored phase snapshot has opposite parity to a fresh
trajectory start; S9B's mask-aware APPLY correctly rejects it
(single DET-APPLY line, match=1/3) and the learner re-detects
from scratch (13 events vs 2 for costaware's reuse).

No oscillation (P6): the prior is one-shot per strategy.
Once all four are tried (S9/S10), selection is (w+1)/(c+1)
argmax converging to empirical-efficiency argmax; S9 has PW
leading on the 2/3 id tie-break, S10 has WHOLE leading at 3/5
> 2/5, with no cycling. A perfect tried record (w = c) ties
untried at 1.0 and keeps the lead by id; optimism promotes
only the unproven over the imperfect.

## Kill bar assessment

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | S3: cold table, all 1.0, DET-STRAT chosen=1 (hedge needs evidence) | byte-exact | PASS |
| K2 | S5: WHOLE earns lead (chosen=2, 1.0 > 2/3), wins in 1 CMP; HYP lag=2 p=2 q=0 | byte-exact | PASS |
| K3 | S7: WHOLE leads (chosen=2), fails (1 CMP); SWITCH 2->3; NEED wins (4 NCMP, HYP lag=2 p=3 q=1) | byte-exact | PASS |
| K4 | S8: untried ALT leads (chosen=4); PW-form fails (2 CMP); NEED-form wins (4 NCMP); 6 events (tax) | byte-exact | PASS |
| K5 | S9: PW leads (2/3 tie-break), fails; SWITCH 1->2; WHOLE rescues, WINS at lag 3 (2 CMP) | byte-exact | PASS |
| K6 | S10: WHOLE leads (3/5 > 2/5); cascade all fail (19 events); how=0 passes=9; AGREE=1 | byte-exact | PASS |
| K7 | S9B: APPLY rejects (1/3); WHOLE->PW->NEED cascade; NEED wins (HYP lag=2 p=4 q=2); prior re-set to 2 | substantive byte-exact; 1 OSC-CYCLE line per E2 | PASS* |
| K8 | S11: zeroed -> chosen=1; cascade PW->WHOLE->NEED (8 events); NEED wins | byte-exact | PASS |
| K9 | S12: optimistic tie (PW 3/5 = NEED 3/5, both tried) -> hedge -> chosen=4; ALT wins via NEED-form | byte-exact | PASS |
| K10 | S13: WHOLE leads outright (chosen=2), fails (1 CMP); SWITCH 2->4; ALT wins at lag 3 | byte-exact | PASS |
| K11 | S14: WHOLE strict argmax (1.0) -> chosen=2; wins in 1 CMP; HYP lag=2 p=2 q=0 | byte-exact | PASS |
| K12 | 3/3 byte-identical stdout, stderr empty | sha256 d236880b x3; .err 0 bytes | PASS |
| K13 | safebin, no python, pure Zag, pinned znc, no while-neg-conjunction, proven nesting shape | verified | PASS |
| K14 | prefix/base cmp-identical; additive diff = strat_sel only; zero literals | all verified | PASS |

SUMMARY-DET: `agree=1 plans_built=8 plans_loaded=4 trials=6
declines=0 prior=2 strat_pw=3,2,6 strat_who=1,1,1
strat_need=2,0,8 strat_alt=1,0,4` (byte-exact as predicted).

## Errata (transparent; prereg NOT silently amended)

E1 (transcription slip): PREREG Section 7's S10 header carried
`LSTATE-RET ... cnts=16,16,0,3,0,8 ...` (carried over from the
S9 header block while copying). The binary produces
`cnts=16,16,0,0,0,8`, byte-identical to COGOPS-COSTAWARE's
actual S10 header (verified by direct comparison of the two
run files). One field, worker's slip, not a mechanism defect.

E2 (walk/slot modeling slip, one line): PREREG Section 7's S9B
OSC-CYCLE predicted
`ph0=[1,611][1,771][1,771][1,614]
ph1=[1,611][1,772][1,772][1,615]`
(fresh-walk steps 2,3 in slots 2,3). The binary produces
`ph0=[1,611][1,772][1,772][1,615]
ph1=[1,611][1,771][1,771][1,616]`
(walk steps 3,4). Root cause, verified against the frozen
source: when the APPLY branch rejects at mpass=0, the
`if(okk==1)` guard skips the mpass=1 trajectory pass, so the
failed APPLY consumes one walk step, not two, and the
re-detection trajectory lands shifted by one in the slots.
The worker's prediction assumed two APPLY trajectory passes
unconditionally. Everything the K7 bar was designed to test
— the APPLY rejection (single DET-APPLY, match=1/3), the
WHOLE->PW->NEED cascade order and event counts, the HYP
(lag=2 p=4 q=2 mask=7), the prior re-set to 2, the NEED win —
is byte-exact as predicted; the selection rule behaved
exactly per the preregistered design. One line, one
prediction-modeling slip, not a selection defect.

## Toolchain disclosure

safebin active for every command (PATH=$HOME/safebin exported
per invocation; `$HOME/safebin` verified directly: 49 entries,
no python3/python; the lane's safebin_setup script does not
exist in this checkout, same finding as the predecessor
workers). `which python3` / `which python` return nothing
before and after; pinned znc
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(2026.07.0-dev) for the single build. All computation pure
Zag; shell only for znc/binary/git/assembly/byte
verification. One near-miss to disclose: during driver edits
the worker typed a `python3` heredoc out of habit; the shell
returned `python3: command not found` (safebin PATH) and zero
Python code executed — the guard held, no contamination, all
subsequent edits via the file tools. New Zag scanned for the
`while.*!(` negated-conjunction pattern: clean (the new
`strat_sel` contains no `!`); nesting matches the proven
COGOPS-COSTAWARE shape (tried==0 / best!=0 / c1>0 / c3>0 /
exact == on hoisted locals, no function calls in nested
conditions). Git writes via /usr/bin/git absolute path,
explicit pathspecs, current branch only, nothing pushed.

## Evidence detail

Stage-by-stage vs COGOPS-COSTAWARE (lead chosen / logged
comparison events):

| stage | costaware lead | optimistic lead | ca events | opt events |
|-------|---------------|-----------------|-----------|------------|
| S3 | 1 (PW) | 1 (PW) | 2 | 2 |
| S5 | 1 (PW) | 2 (WHOLE) | 1 | 1 |
| S7 | 1 (PW) | 2 (WHOLE) | 8 | 5 |
| S8 | 1 (PW) | 4 (ALT) | 6 | 6 |
| S9 | 1 (PW) | 1 (PW) | 8 | 4 |
| S10 | 1 (PW) | 2 (WHOLE) | 20 | 19 |
| S9B | reuse (2 APPLY) | reject + cascade | 2 | 13 |
| S11 | 1 (PW) | 1 (PW) | 13 | 8 |
| S12 | 4 (ALT) | 4 (ALT) | 6 | 6 |
| S13 | 1 (PW) | 2 (WHOLE) | 4 | 4 |
| S14 | — | 2 (WHOLE) | — | 1 |

Totals S3..S13: 70 (costaware) vs 68 (optimistic). Optimism
is cheaper or equal on every stage except S9B, where the
misaligned stored snapshot forces full re-detection (+11).
The S9B effect is the honest headline cost of optimism in
this battery: not the per-episode exploration tax (small),
but the change to the learner's own stored evidence.

Selection dynamics worth recording: at S9 the table is
all-tried (PW[2,1,4]->2/5, WHO[3,2,4]->3/5, NEED[1,1,4]->2/5,
ALT[1,1,6]->2/7) and PW still leads on the 2/3 id tie-break
over WHOLE's 2/3 — optimism's promotion applied only while
WHOLE was untried (S5/S7). At S10 WHOLE leads at 3/5 on pure
evidence. The +1 prior visibly washes out: compare S10's
scores (3/6 vs 2/8) with what pure efficiency would give
(2/5 vs 1/7) — same ordering, converging.

The S12 hedge under optimism: PW[2,2,4]->3/5 and
NEED[5,5,9]->3/5 tie at the best with both tried, while
WHO/ALT sit at 1/5; the evidence-gated hedge fires (chosen=4)
exactly as preregistered. Without the c1>0/c3>0 evidence
gate, the cold-start vacuous tie would have hedged (K1
guards this).

## What this establishes (and does not)

Establishes: the +1/+1 optimistic prior lifts the structural
ceiling that kept untried strategies from ever leading —
untried WHOLE earns the lead on fresh full oscillations
(S5 natural, S14 controlled strict argmax) and converts it
to wins where its proposal order applies; the promotion is
per-episode falsifiable (S13); the exploration tax is bounded
and measured (S8, S13); no oscillation emerges because the
prior is one-shot per strategy and decays as 1/n (S9/S10);
the hedge and the cold-start default survive on optimistic
terms with the evidence gate (S12, S3); outcome-reuse is
alignment-sensitive and optimism exercises the rejection
path for the first time (S9B, with erratum E2 on one
predicted line).

Does not establish: learner-invented optimism (the rule and
the prior are researcher-provided; only table values are
learner-written); optimality of +1/+1 among optimistic rules;
per-context selection (table still global); L3
representational invention; that optimism is net-beneficial
in general (in this battery it is roughly cost-neutral: 68
vs 70 events, with the S9B second-order cost dominating).

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_optimistic/`:
PREREG.md (frozen, commit 32c6799b9), NAMECHECK.md (Step 0),
c12_base.zag (cmp-identical to c11_base.zag), c12_world.zag
(c11_world.zag plus mk_goal825_E3), c12_strat_additive.zag
(only strat_sel changed), c12_learn.zag (prefix cmp-identical
plus additive), c12_main.zag (driver plus S14, retied S12
lesion, S13/S14 lesions), c12_build.sh, c12_full.zag
(assembled; exactly one `fn main`), c12_bin, c12_compile.txt,
c12_run1/2/3.txt (sha256 d236880b x3) + .err (empty),
REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. Per-context strategy tables (COGOPS-COSTAWARE follow-up
   2): S9B shows optimism's largest cost flows through the
   global table's stored evidence; context-scoped tables
   would localize both the promotion and its side effects.
2. Expected-cost selection (follow-up 3): S8/S13's wasted
   comparisons are currently invisible to the rule; folding
   P(fail)*rescue-cost into the optimistic score would price
   the exploration the prior buys.
3. Learner-composed proposal orders (follow-up 4): choosing
   among four given forms is still selection, not invention.
4. The APPLY walk-shift (E2) is a frozen-substrate
   trajectory-indexing subtlety, not a selection defect; no
   action needed unless a future battery depends on
   predicting post-rejection slot contents.
