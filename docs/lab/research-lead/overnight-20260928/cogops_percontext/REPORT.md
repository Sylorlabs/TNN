# REPORT: COGOPS-PERCONTEXT (per-context strategy tables)

Date: 2026-10-03. Worker: COGOPS-PERCONTEXT.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_percontext/`
Prereg: frozen commit 692b5f1f5 (PREREG.md + NAMECHECK.md,
committed alone before any implementation file existed).
Implementation commit follows this report.

## Verdict: BUILD-PASS (K1..K14 all PASS, with transparent errata E1, E2)

The global strategy table is now five context tables. The
context is a learner-computed signature `(nneeds,
need_f(G,1,0))` read from the goal record at structural
positions; no world/goal literals anywhere in the mechanism.
The battery answers the follow-up question directly:
**per-context localizes both the optimistic promotion and its
side effects, exactly as predicted.**

The headline results:

1. **The optimistic promotion does not cross contexts (K2).**
   On the fresh lag-2 full oscillation (S5, goal 820, context
   (3,613) first seen), the table is cold, all four strategies
   tie at 1.0, and PW leads by id (chosen=1) — NOT WHOLE.
   COGOPS-OPTIMISTIC's headline ("untried WHOLE earns the lead")
   does not reproduce on a fresh context. The promotion is
   context-local.

2. **Within-context promotion survives (K4).** S8 (goal 823,
   context (4,613) carrying S7): ALT is untried in-context,
   scores 1.0 strictly best, and leads (chosen=4) with the same
   6-event tax as under global optimism.

3. **S9B outcome reuse is restored (K7).** Because c13's S7 is
   PW-led (cold context), NEED wins with HYP lag=2 p=4 q=2 —
   the same alignment as COGOPS-COSTAWARE — so the stored phase
   snapshot matches a fresh trajectory and the mask-aware APPLY
   succeeds at 3/3. The learner reuses the outcome in 2 events
   instead of paying 13 for re-detection. **Per-context fixes
   optimism's largest cost.**

4. **A novel cascade order (K6).** S10 (goal 816, context
   (3,604) cold): PW leads, and rescue among context-untried
   strategies goes by id — PW->WHOLE->NEED->ALT — matching
   neither predecessor (costaware: PW->NEED->WHOLE->ALT by
   efficiency; optimistic: WHOLE-led). 19 comparison events,
   generic fallback, AGREE=1, byte-exact as predicted.

5. **No cross-context contamination (P8).** The final CTX dump
   shows five independent histories: context (3,613) never saw
   NEED's S7 win; context (4,613) never saw PW's S5 win;
   context (3,615) started cold at S9 despite S5.

## Kill bar assessment

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | S3: cold context (3,606) -> chosen=1 | byte-exact | PASS |
| K2 | S5: cold context (3,613) -> chosen=1 (NOT 2); 1 CMP; HYP lag=2 p=2 q=0 | byte-exact | PASS |
| K3 | S7: cold context (4,613) -> chosen=1; PW fail; SWITCH 1->2; WHOLE fail; SWITCH 2->3; NEED wins (4 NCMP, HYP p=4 q=2) | byte-exact | PASS |
| K4 | S8: in-context ALT untried (1.0 strict) -> chosen=4; 6 events | byte-exact | PASS |
| K5 | S9: cold context (3,615) -> chosen=1; PW fail; SWITCH 1->2; WHOLE wins at lag 3 | byte-exact | PASS |
| K6 | S10: cold context (3,604) -> chosen=1; cascade PW->WHOLE->NEED->ALT; 19 events; how=0; AGREE=1 | substantive byte-exact; 2 setup lines per E2 | PASS* |
| K7 | S9B: APPLY succeeds (two DET-APPLY, match=3/3); how=2; OSC-REUSE | byte-exact | PASS |
| K8 | S11: zeroed context -> chosen=1, prior=3; PW->WHOLE->NEED cascade; NEED wins (HYP p=4 q=2) | byte-exact | PASS |
| K9 | S12: context lesion -> hedge -> chosen=4; ALT wins via NEED-form | byte-exact | PASS |
| K10 | S13: context lesion -> chosen=2 (WHOLE 1.0); WHOLE fails (1 CMP); SWITCH 2->4; ALT wins at lag 3 | byte-exact | PASS |
| K11 | S14: context lesion -> chosen=2 strict argmax; WHOLE wins in 1 CMP | byte-exact | PASS |
| K12 | 3/3 byte-identical stdout, stderr empty | sha256 569befb0 x3; .err 0 bytes | PASS |
| K13 | safebin, no python, pure Zag, pinned znc, no while-neg-conjunction, proven nesting shape | verified | PASS |
| K14 | prefix/base/world cmp-identical; additive diff = CTXT pool + slot fns + strat_sel slot param + det_handle wiring; zero literals | all verified | PASS |

## Errata (transparent; prereg NOT silently amended)

E1 (transcription slip, one line): PREREG Section 7's S6L block
carried `LSTATE-RET ... cnts=16,16,0,3,0,8 ...`. The binary
produces `cnts=16,16,0,0,0,8`, byte-identical to
COGOPS-OPTIMISTIC's actual S6L output (verified by direct
comparison of the two run files). The worker copied the S6B
cnts pattern into S6L while transcribing. One field, worker's
slip, not a mechanism defect; S6L is selection-independent.

E2 (transcription slip, two lines): PREREG Section 7's S10
setup block carried `LSTATE-RET ... cnts=16,16,0,3,0,8 ...` and
`SPEC-VFY rev=7 nrel=7 ep0=21 ep1=22 nfacts=72`. The binary
produces `cnts=16,16,0,0,0,8` and `ep0=26 ep1=26`,
byte-identical to COGOPS-OPTIMISTIC's actual S10 setup (verified
by direct comparison). Same copy-paste slip as E1, plus a
wrong episode range on the SPEC-VFY line. Everything the K6 bar
was designed to test — the PW lead, the novel
PW->WHOLE->NEED->ALT cascade order and event counts, the 19
comparisons, the fallback, AGREE=1 — is byte-exact as
predicted. Two lines, worker's slip, not a selection defect.

## Toolchain disclosure

safebin active for every command (PATH=$HOME/safebin exported
per invocation; `which python3` / `which python` return nothing
before and after; the lane's safebin_setup script does not exist
in this checkout, same finding as the predecessor workers).
Pinned znc `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(2026.07.0-dev) for the single build. All computation pure Zag;
shell only for znc/binary/git/assembly/byte verification. Zero
forbidden-executable invocations, no near-misses. New Zag
scanned for the `while.*!(` negated-conjunction pattern: clean
(the new `strat_sel` contains no `!`); nesting matches the
proven COGOPS-OPTIMISTIC shape (tried==0 / best!=0 / c1>0 / c3>0
/ exact == on hoisted locals, no function calls in nested
conditions); only the table base address changes (slot base
instead of fixed 16600). Git writes via /usr/bin/git absolute
path, explicit pathspecs, current branch only, nothing pushed.

## Evidence detail

Stage-by-stage vs COGOPS-OPTIMISTIC (lead chosen / logged
comparison events, eq=-1 skips excluded):

| stage | optimistic lead | percontext lead | opt events | pc events |
|-------|---------------|-----------------|-----------|-----------|
| S3 | 1 (PW) | 1 (PW) | 2 | 2 |
| S5 | 2 (WHOLE) | 1 (PW) | 1 | 1 |
| S7 | 2 (WHOLE) | 1 (PW) | 5 | 8 |
| S8 | 4 (ALT) | 4 (ALT) | 6 | 6 |
| S9 | 1 (PW) | 1 (PW) | 4 | 4 |
| S10 | 2 (WHOLE) | 1 (PW) | 19 | 19 |
| S9B | reject + cascade | reuse (APPLY 3/3) | 13 | 0 (+2 APPLY) |
| S11 | 1 (PW) | 1 (PW) | 8 | 12 |
| S12 | 4 (ALT) | 4 (ALT) | 6 | 6 |
| S13 | 2 (WHOLE) | 2 (WHOLE) | 4 | 4 |
| S14 | 2 (WHOLE) | 2 (WHOLE) | 1 | 1 |

Totals S3..S13: 68 (optimistic) vs 62 (per-context). The S9B
restoration (-13) outweighs the cold-start taxes (S7 +3, S11
+5). S8/S9/S10/S12/S13/S14 event counts are unchanged vs
global optimism; S5's count is unchanged but the lead differs
(PW, not WHOLE).

The cold-start tax, itemized: S7 pays PW(2)+WHOLE(2) failures
before NEED wins (+3 vs optimism's WHOLE(1)+NEED(4)); S11 pays
PW(3: skip+2CMP)+WHOLE(2)+NEED(8: lag-3 then lag-2) (+4 in raw
counts vs optimism's 8; the prior=3 changes PW's and NEED's
proposal order vs the prior=2 optimistic run).

The S9B mechanism, confirmed: c13's S7 stores trajectory
passes 2,3 (HYP p=4 q=2); the masked needs (0,1,2) have
2-cycle parity, so fresh passes 0,1 match stored passes 2,3
exactly (3/3 both passes); the drifter need 3 is outside the
mask. The APPLY path returns before any strategy selection, so
no context table is touched and the lag prior stays 3.

Final context tables (CTX dump, byte-exact as predicted):
slot0 (3,606): PW[1,1,2]; slot1 (3,613): PW[3,2,6],
WHOLE[1,1,1], NEED[2,0,8], ALT[1,0,4] (S5 win + S14 lesion +
S14 WHOLE win); slot2 (4,613): PW[2,2,4], WHOLE[1,0,4],
NEED[5,5,9], ALT[2,1,10] (S7/S8 + S11 zero + S11 cascade + S12
lesion + S12 ALT win); slot3 (3,615): PW[3,2,6], WHOLE[1,0,1],
NEED[2,0,8], ALT[1,1,3] (S9 + S13 lesion + S13 cascade); slot4
(3,604): PW[1,0,3], WHOLE[1,0,2], NEED[1,0,6], ALT[1,0,9] (S10
cascade). Five independent histories; no cross-context
contamination.

## What this establishes (and does not)

Establishes: per-context tables localize the optimistic
promotion and its side effects. A fresh context is a cold
start (PW default; the S5/S7 WHOLE leads do not reproduce);
within a context the promotion works as before (S8 ALT lead);
the S9B second-order blowup is fixed by restoring outcome
reuse (13 -> 2 events); the lesion bars behave per-context
(S12 hedge, S13/S14 WHOLE leads); the context signature
(nneeds, need-1 relation field) partitions the battery into
five independent histories with no contamination. The "does
per-context fix S8/S9?" answer is mechanism-level: under the
optimistic base, S8/S9 keep their event counts (6 and 4) —
what per-context fixes is the S9B blowup and the
cross-context cheapness leak (PW's (3,613) wins no longer buy
leads in (4,613) or (3,615)).

Does not establish: learner-invented contexts (the signature
shape is researcher-chosen; only slot allocation and table
values are learner-written); optimality of the (nneeds, rel)
granularity (P1/P5 show its price: cold starts); L3
representational invention; that per-context is net-beneficial
in general (in this battery: 62 vs 68 events, with the S9B
fix dominating); the per-context + pure-efficiency variant
(explicit future work).

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_percontext/`:
PREREG.md (frozen, commit 692b5f1f5), NAMECHECK.md (Step 0),
c13_base.zag (cmp-identical to c12_base.zag), c13_world.zag
(cmp-identical to c12_world.zag), c13_strat_additive.zag (CTXT
pool + slot fns; strat_sel takes a slot), c13_learn.zag
(prefix cmp-identical plus additive), c13_main.zag (driver with
slot-targeted lesions and CTX dump), c13_build.sh,
c13_full.zag (assembled; exactly one `fn main`), c13_bin,
c13_compile.txt, c13_run1/2/3.txt (sha256 569befb0 x3) + .err
(empty), REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. Per-context + pure efficiency (costaware base): the
   S8/S9 finding was about pure efficiency's global table; the
   per-context fix should be tested on that base, where S8
   would become NEED-lead (4 events) instead of PW-lead (6).
2. Context granularity: (nneeds) alone vs (nneeds, rel) vs
   trajectory-behavioral signatures; measure cold-start tax vs
   contamination for each.
3. Expected-cost selection (follow-up 3): S8's 6-event ALT tax
   persists within-context; folding P(fail)*rescue-cost into
   the optimistic score would price it.
4. Learner-composed proposal orders (follow-up 4): choosing
   among four given forms is still selection, not invention.
