# PREREG_C174: Shared tag-61 store validation (frozen)

Lane: C174, wave wave-20261001-2321pdt.
Status: FROZEN. This document is the preregistration for the shared
consequence substrate validation battery. Frozen before any
implementation file for this battery exists in the lane directory.
Kill bars below never move after this freeze.

## 1. Lineage and scope boundary

Lineage: spec 550fa268b (SHARED-SUBSTRATE-COMPLETE, 619 lines);
ledger C174 (SUBSTRATE-CONSOLIDATION, EMERGES, exploratory, no
frozen prereg); C175 (UTILITY-DESIGN, design only); C180
(DEDUP-DECLINE-INTEGRATION, decline gate retired, dedup subsumed
decline); C181/C182/C183 (learner-owned reliability, adaptive
threshold, source reliability, all exploratory); C185/C194
(substrate expansion and integration, exploratory); CONSEQ lane
wave-20261001-2321pdt VALIDATION-PASS (Node2-v2 K-H3 reproduced,
consequence record causally necessary, scope honestly held to the
re-entry template, not the shared store).

Scope boundary with the concurrent TNN3-SUBSTRATE lane: that lane
owns the learner construction primitive, the contradiction trigger,
and learner standing. This lane owns ONLY the shared tag-61 store
(one keyed store, generic write sub_note, generic read sub_consec,
record lifecycle) plus consequence-derived utility
(sub_utility) plus exactly two consumers (trial reorder per spec
section 5.4, retention input per spec section 5.3). This lane does
NOT touch the frozen TNN-2 binary, does NOT rebuild the decline
gate (retired per C180), does NOT add modes, bridges, handlers, or
semantic cases.

What is validated here if all bars pass: the shared store itself
as infrastructure (writes via the generic path, two consumers
reading the same store, consequence-derived utility judgments
changing behavior, causal ablation, migration compatibility with
Node2-v2). What is NOT claimed: L3, general intelligence, FW1-FW9
gains, or that the substrate is the final TNN-3 design.

## 2. The prototype (dev harness, pure Zag)

Separate .zag files in this lane directory. The frozen TNN-2
binary is not modified. Files:

- c174_sub.zag: the shared store and consumers.
- c174_gen.zag: sealed world generator (seeded LCG, stdout emits
  world_sealed.zag).
- world_sealed.zag: generated worlds (seal commit, section 5).
- c174_eval.zag: evaluation driver (arms S/F/A).
- c174_migrate.zag: Node2-v2 migration-compat test.
- c174_selftest.zag: white-box machinery self test.
- armflag_s.zag / armflag_f.zag / armflag_a.zag: one-line arm
  selectors compiled into the eval binary.
- build.sh: exact build and run commands.

### 2.1 Record format (tag 61, fixed 64 bytes, 16 i32 fields)

Offsets: 0 tag (61); 4 key_type (1 PURSUIT, 2 STRATEGY); 8 key;
12 attempts; 16 successes; 20 consec_fail; 24 last_mode (F1-F7
vocabulary, 0 means last attempt succeeded); 28 cost_nodes
(saturating); 32 cost_tries; 36 src_taught; 40 src_observed;
44 src_self; 48 state (0 ACTIVE, 1 ABANDONED, 2 RE-ENGAGED);
52 last_active (event sequence number); 56 live flag; 60
reserved. No histories, no traces, no variable-length data.

Store: one flat array, header plus MAXREC records, linear lookup
by (key_type, key). Reclamation per spec section 6.2: when full,
reclaim the stalest record (minimum last_active, tie broken by
minimum attempts); ABANDONED records are reclaimed before ACTIVE
records at equal staleness. Reclamation is infrastructure with a
fixed rule and gets no record of its own (spec section 6.3).

### 2.2 Generic write: sub_note

Signature: sub_note(store, key_type, key, outcome, src, mode,
cost, ev) where outcome is 1 (success), 0 (failure); src is 0
taught, 1 observed, 2 self.

Behavior:
- Disabled flag set (ablation arm): no-op, returns -1.
- Find record by (key_type, key); create on first attempt
  (counters zero, state ACTIVE, last_active ev); reclaim per
  section 2.1 when full.
- src_self attempts: increment attempts and src_self only. They
  are excluded from the evidence tallies (successes,
  consec_fail, last_mode untouched). This implements spec
  section 7.1 (bootstrap exclusion): self-generated
  confirmations are counted as attempts but never as evidence.
- Success: attempts++, successes++, consec_fail := 0,
  last_mode := 0, applicable src counter++, last_active := ev.
- Failure: attempts++, consec_fail++, last_mode := mode,
  cost_nodes saturating add, applicable src counter++,
  last_active := ev.
- Record lifecycle (spec section 5.2 minimal rule, inside the
  store, not a separate gate engine): after the update, if
  consec_fail >= ABANDON_BOUND then state := ABANDONED; else if
  outcome is success and state is ABANDONED then
  state := RE-ENGAGED (a successful observation re-engages the
  pursuit) and consec_fail is already 0 from the success rule.

### 2.3 Generic read: sub_consec

Signature: sub_consec(store, key_type, key) returns the record
byte offset, or -1 on miss (or when the disabled flag is set).
Read counters are kept for the audit (section 7).

### 2.4 Consumer 1: trial reorder (spec section 5.4)

sub_reorder(store, order): for families 0..5, read the STRATEGY
record via sub_consec. Rate in permille :=
1000 * successes / max(1, attempts - src_self); families with
fewer than MINATT non-self attempts, or with no record, get the
neutral prior NEUTRAL_PRIOR (they are not buried for being
untried). Order families by descending rate, stable. This
replaces a private per-family counter with the shared record;
the decision is auditable from record fields.

### 2.5 Consequence-derived utility (C175 direction, C187 test 6)

sub_utility(store, key_type, key): U := rate_permille -
40 * consec_fail - cost_nodes / 20, clamped to
[-2000, 2000], where rate_permille is defined as in section
2.4. U is computed ONLY from record fields. It is use-derived,
not truth-derived (C175 honest scope). A missing record yields
U := 0 (the fixed baseline).

### 2.6 Consumer 2: retention input (spec section 5.3)

sub_victims: given candidate structures each tagged with its
creating pursuit key and a bid, produce the victim order:
first structures whose pursuit record has state ABANDONED
(ordered by ascending U, then struct id), then all others
ordered by ascending U, then ascending bid, then struct id.
Structures of ABANDONED pursuits are reclaimed before
structures of ACTIVE pursuits regardless of bid (spec section
5.3). A missing pursuit record counts as ACTIVE with U := 0.

### 2.7 Researcher-set constants (honestly labeled scaffolding)

MAXREC 64; ABANDON_BOUND 3; MINATT 2; NEUTRAL_PRIOR 500;
utility weights 40 and cost divisor 20, clamp [-2000, 2000];
cost_nodes saturation 1000000; K_REVELATIONS 3 (taken from the
frozen Node2-v2 prereg, not chosen here); fixed family order
for the fixed-bookkeeping arm [3,0,5,1,4,2] (chosen by the
author before the sealed worlds are generated, independent of
the world seed); world generator seed 20261001. None of these
are claimed as learner-owned or optimal.

## 3. Sealed worlds

Two sealed worlds plus the K-H3 migration world.

### 3.1 W-REORDER (strategy discrimination)

48 trials, 6 families. Sealed per-family success permille: the
multiset {150, 300, 450, 600, 750, 900} shuffled by the seeded
LCG (assignment committed via the world hash). Per-trial
per-family draws precomputed by the generator into a static
table (bit rows), so every arm faces the identical world
regardless of how many families it attempts per trial.
After each trial, with LCG probability 0.2, one src_self
confirmation is recorded for a random family (tests the
section 7.1 exclusion: these must not inflate rankings).
Each trial also writes one PURSUIT record (key 1000+t) with
the trial outcome, so both namespaces are exercised through
the generic path.

Driver per trial: determine the attempt order (arm dependent),
attempt families in order until the first success (draw table),
record each attempt via sub_note(STRATEGY, f, outcome,
SRC_TAUGHT, mode F1 on rejection, cost 1, ev t). Count total
attempts. After trial 48, record the final order.

### 3.2 W-RETIRE (retention under pressure)

5 pursuits (keys 100..104). Sealed event histories from the
seeded LCG with structural constraints fixed here before
generation: P0 8 events, at least 4 successes, never 3
consecutive failures (ends ACTIVE); P1 8 events, first 4 with
at least 1 success and at most 2 consecutive failures, last 4
all failures (ends ABANDONED, consec_fail 4); P2 6 events
mixed, at least 2 successes, at most 2 consecutive failures
(ends ACTIVE); P3 2 events (new pursuit, ACTIVE); P4 exactly
F,F,F,S (ABANDONED on the third, RE-ENGAGED on the fourth;
validates the lifecycle transition). All events src_taught.

10 structures, sealed creating-pursuit assignment (structs 0
and 1 forced to P1 so the abandoned pursuit owns structures)
and sealed bids (LCG mod 100). Memory pressure evicts 5 of 10.
Held-out queries: 6, each needing one of the clean ACTIVE
pursuits {P0, P2, P3} (sealed mapping); a query is answerable
iff at least one surviving structure was created by its needed
pursuit. This tests the spec section 5.3 intent: the
substrate-backed eviction should preserve the structures that
ongoing pursuits need.

### 3.3 K-H3 migration world (already sealed by CONSEQ)

The exact event sequence from frozen prereg 4b05c8011 section
5, independently re-executed by the CONSEQ lane (source SHA-256
99774fbc575db57f39d2c93844370aa66a76e38cb7ab101d8717ff5c78bd6855,
result SHA-256
74c48d5a85087eab5d9c86aebf6075ce69f89be5736422e6bf63e897f527aae9):
Phase 1 revelations [30, -1, 30] (default stays 30); Phase 2
revelations [45, 45, 45] (default 30, 30, then 45 on the third);
Phase 3 guide carries 45. No new seal needed; the seal is the
frozen prereg plus the CONSEQ committed hashes.

### 3.4 Seal procedure

The generator seed (20261001) and the procedure in this prereg
are frozen now. After the implementation commit, the generator
is compiled and run once; world_sealed.zag is committed with
WORLD_MANIFEST.md listing SHA-256 hashes, in a seal commit
made BEFORE any evaluation output exists. The evaluation
binaries are built from the committed world file. Anyone can
re-verify: frozen seed plus committed generator reproduces
the committed world hash bit for bit.

## 4. Arms

- Arm S (shared store): full substrate path. W-REORDER: writes
  via sub_note, order from sub_reorder each trial. W-RETIRE:
  pursuit histories via sub_note, victims from sub_victims.
- Arm F (fixed bookkeeping): no store interaction at all.
  W-REORDER: fixed order [3,0,5,1,4,2] every trial; same draw
  table, same stop-at-first-success, same attempt counting.
  W-RETIRE: victims by ascending bid (struct id tiebreak);
  utility constant 0.
- Arm A (ablation): identical code path to arm S, but the
  disabled flag makes every sub_note a no-op and every
  sub_consec a miss; consumers fall back exactly to the fixed
  rules (reorder falls back to [3,0,5,1,4,2]; victims fall back
  to bid order with U 0). This mirrors the CONSEQ Link 1
  ablation (record disabled, judgment reverts to fixed).

The printed decision channels are format-identical across
arms; only arm S additionally prints record internals.

## 5. Migration-compat test (kill bar d)

c174_migrate.zag runs two arms in one binary on the K-H3 world
(section 3.3):

- M1 (node-local): the Node2-v2 rule verbatim from frozen
  prereg 4b05c8011 section 2.4: three history slots init -1;
  on a_w >= 0 shift slots; if all three equal A >= 0 and
  A != default, set default := A and reset slots to -1;
  a_w = -1 leaves history unchanged.
- M2 (shared store): each a_w >= 0 revelation is recorded via
  sub_note(STRATEGY, 7000 + a_w, success, SRC_TAUGHT, 0, 0);
  the 3-revelation rule reads the per-value (value, count,
  source) record via sub_consec and shifts the default when
  successes = 3 and the value differs from the default, then
  resets the value records (the migration analog of the slot
  reset). This is the migration framing of prereg section 7:
  (value, count, source) triples in the shared store.

Honest boundary (stated before the run): the per-value-counter
rule and the shift-register rule coincide on worlds without
interleaved divergent revelations; the K-H3 sealed world has
none. A world with interleaved divergent revelations would
distinguish them; that case is out of scope for this bar.

## 6. Kill bars (all must pass for VALIDATION-PASS)

(a) STORE-SERVES-TWO: on both sealed worlds, every outcome
write goes through sub_note and both consumers' decisions are
computed from sub_consec reads on the same store instance.
PASS iff: W-REORDER completes 48 trials with sub_note writes
> 0 for both namespaces and sub_reorder reads > 0;
W-RETIRE completes with sub_note writes > 0 for PURSUIT and
sub_victims reads > 0; no consumer accesses record fields
except through sub_consec (build constraint, verified by
inspection of the committed source).

(b) BEHAVIOR-CHANGE: consequence-derived judgments change
behavior relative to fixed bookkeeping on the sealed worlds.
PASS iff: on W-REORDER, arm S final order differs from the
fixed order AND total attempts differ between S and F; on
W-RETIRE, the arm S victim sequence differs from the arm F
victim sequence. Direction (better/worse) is reported
honestly but is not bar-gated.

(c) ABLATION-CAUSAL: ablating the shared store reverts
judgments to the fixed baseline. PASS iff SHA-256(arm A
output) equals SHA-256(arm F output) on both worlds AND
SHA-256(arm S output) differs from arm F on both worlds.

(d) MIGRATION-COMPAT: PASS iff M1 reproduces the CONSEQ K-H3
decision trace exactly (Phase 1 default 30; Phase 2 mid
defaults 30, 30, 45; Phase 2 default 45; Phase 3 guide 45)
AND the M2 trace is byte-identical to the M1 trace.

(e) DETERMINISM: PASS iff 3/3 reruns of every binary
(eval_S, eval_F, eval_A, migrate, selftest, gen) are
byte-identical (SHA-256 equal within each triple).

Verdict rule: VALIDATION-PASS iff all five bars pass.
Otherwise the honest failure names the failed bar with the
killing evidence; the substrate stays EMERGES. No bar moves
after this freeze.

## 7. White-box audit counters

sub_note and sub_consec maintain caller-visible counters
(writes, reads, reclaims, per-consumer reads). The eval
prints them. Bar (a) is checked against these counters, not
against prose.

## 8. Non-goals (explicit)

No decline gate rebuild; no learner construction primitive;
no contradiction trigger; no learner standing; no threshold
learning (ABANDON_BOUND is scaffolding); no cross-pursuit
generalization; no second-order learning; no claim about
FW1-FW9, L3, or TNN-3 architecture. Reclamation is
implemented per spec but the battery does not fill the store,
so reclamation is exercised only in the self test, labeled
accordingly.

## 9. Commit order

1. This prereg alone (this commit).
2. Implementation (.zag sources, build.sh).
3. Worlds seal (world_sealed.zag + WORLD_MANIFEST.md with
   SHA-256 hashes), before any eval output exists.
4. Evaluation run (outputs, EVAL_RESULTS.md, JUDGE_BRIEF.md).
