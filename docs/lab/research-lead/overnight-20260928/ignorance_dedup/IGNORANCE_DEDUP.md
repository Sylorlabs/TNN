# Ignorance Dedup: Root Cause Analysis

Verdict: IGNORANCE-DEDUP-COMPLETE with root cause.
Analysis only. No fix implemented. Frozen TNN-2 source read but not modified.

## 1. The observed finding

State dynamics `ee238d8d4`, Section 5: phases B and G issue the same
6 masked queries on the same subjects. Both times every query misses,
and phase G creates 6 MORE UNCERTAINTY nodes (T30 count 10 -> 16) for
keys that already have uncertainty nodes from phase B.

Per-experience delta table: `ev_query masked miss (no trial success)`
costs exactly +14 nodes / +6 edges EVERY time, identically composed:
+1 UNCERTAINTY (T30), +3 T101, +2 T102, +1 T103, +6 T902 literals,
+1 T1 (the guide). Phases B, D, G all show the identical +14/+6.

"The learner does not remember its own ignorance."

## 2. Root-cause trace (frozen source, read-only)

File: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`.
Line numbers refer to this file. Production cognition code is lines
86-916; lines 918+ are the test battery and main.

### 2a. Where the UNCERTAINTY node is created

`miss_inquire`, lines 795-811:

```
fn miss_inquire(W:[]u8,s:i32,r:i32)void {
  let u:i32=alloc_node(W); if(u<0){return;}
  ns(W,u,0,30);
  ns(W,u,4,-4);
  write_node(W,u,s,r,2,0);
  ...
  let g:i32=alloc_node(W); if(g<0){return;}
  ns(W,g,0,1); ns(W,g,4,s);
  write_node(W,g,30,-999,0,0);
  link_edge(W,g,1,u,0);
  link_edge(W,pr,10,g,0);
  return;
}
```

It unconditionally allocates a fresh node, tags it 30 (UNCERTAINTY),
and writes the query key (s, r) into fields 20/24. It then allocates a
guide node (tag 1), writes a placeholder proposed action (field 20 =
30, field 24 = -999), links guide -> uncertainty (edge type 1), and
links POLICY_ROOT -> guide (edge type 10).

### 2b. The single call site

`miss_inquire` has exactly ONE production caller: `ev_query`, line 833,
the terminal branch of the miss path (lines 813-835):

```
fn ev_query(W:[]u8,s:i32,r:i32,expected:i32,flags:i32)i32 {
  ...
  let n:i32=activate(W,s,r);        // exact hit? no.
  ...
  let ans:i32=mp_run(W,s,r,expected,flags);   // trial loop? fails (-2).
  ...
  let bv:i32=bootstrap_miss(W,s,r); // P-INV bootstrap? fails (-2).
  ...
  log_ev(W,2,s,r,-2,0,0,0);
  miss_inquire(W,s,r);              // unconditional reification.
  return -2;
}
```

### 2c. Is there any check for an existing uncertainty on the same key?

No. There is no scan of T30 nodes by (s, r) anywhere in production
code. The exhaustive evidence:

- `grep` for tag-30 reads in production (lines 86-916) returns zero
  hits. The only tag-30 references in production are the creation site
  in `miss_inquire` (line 797).
- The other T30 creation/read sites (lines 1047, 1182, 1244, 1378)
  are all inside the test battery (lines 918-1357) or test helpers,
  not the cognition path.
- `activate` (line 141) scans only tag-1 (FACT) nodes for (s, r) in
  fields 20/24. Uncertainty nodes are invisible to it.
- `is_superseded` (line 132) detects type-3 self-edges. Uncertainty
  nodes never receive type-3 self-edges in production (only FACTs do,
  in `ev_observe` on contradiction).

### 2d. The deeper fact: the uncertainty record has no production read path

The (s, r) key written by `write_node(W,u,s,r,2,0)` is write-only in
production. Nothing ever reads it back:

- `ev_act` (lines 858-899) selects guides linked to POLICY_ROOT by
  context-ring match on the guide's field 4 (subject) plus `bid`.
  It never consults uncertainty nodes or their keys.
- `bid` (line 237) counts event types on the candidate and on nodes
  linked to it by edge type 10. The guide -> uncertainty link is edge
  type 1, so uncertainty nodes contribute nothing to any bid.
- No `resolve_uncertainty` exists. When the answer for (s, r) is later
  taught, `activate` hits the new FACT; the stale uncertainty node
  stays live, unretired, unreferenced.

Ablation consequence: deleting every T30 node from a live learner
would change no production behavior. The uncertainty nodes are
behaviorally inert records.

### 2e. The miss pipeline is history-independent by construction

Not only `miss_inquire` but every stage re-runs identically on repeat
misses: the trial loop `mp_run` allocates its 12 trial cells and
literals (+3 T101, +2 T102, +1 T103, +6 T902) even when it fails, with
no check for prior attempts. The constant +14/+6 per-miss cost across
260 experiences is the signature of a pipeline with no conditional
branch on history at any stage.

## 3. Classification: architectural limitation (missing-feature surface, not a bug)

This is NOT a bug in the "code fails to do what its author intended"
sense. There is no evidence of intended dedup: no commented-out
check, no half-written scan, no design note promising it. The inquiry
build (commit 18ed3331c, integrated per the comment at lines 789-794)
specifies `miss_inquire` as an unconditional reification step: a miss
IS the admission, and the admission IS a fresh node. The code does
exactly what the design says.

It IS a missing feature at the surface (no dedup check), but the
missing check is not the root cause. The root cause is architectural:
the uncertainty record was designed as a write-only reification with
no production read path, no retirement path, and no decision point
anywhere in the cognition path where a remembered-ignorance record
could causally intervene. Adding a dedup check alone would save node
allocations and change nothing about behavior, because the records it
would deduplicate are already behaviorally inert.

In Micah's write-path-audit terms: this is the dual of the theater
failure. The uncertainty node has an exercised production WRITE path
but no exercised production READ path. A record that is written and
never read is theater regardless of whether duplicates are suppressed.

## 4. Why not: would a check break something?

Mechanically, no. A pre-allocation scan ("does a live T30 with
field20==s and field24==r exist; if so, skip") would be
behavior-preserving precisely because the nodes are inert. It would
reduce node churn (+14 -> +13 per repeat miss, trial cells still
allocated) and nothing else.

But it would be dishonest to report as progress: it would make the
ledger show "the learner remembers ignorance" while no decision the
learner makes is altered by the remembered record. Per the standing
rule, a value in learner state with no causal role in a production
decision is theater. The check would be cosmetic surgery on a
write-only log.

## 5. What "remembering ignorance" would require (minimal mechanism, not implementation)

Four jointly necessary elements. Element 1 alone is theater.

1. Keyed lookup at creation: scan live T30 nodes for (s, r) before
   allocating (an O(1024) scan like `activate`). This is the dedup
   check. Necessary, not sufficient.

2. A production READ path that consumes the record: at least one
   decision that branches on "uncertainty already exists for this
   key." Examples of the shape (not prescriptions): skip or shorten
   the trial loop on a second miss (cheaper second miss); reuse or
   augment the existing guide instead of minting a new placeholder;
   escalate to a different inquiry strategy. Without this, the record
   cannot affect behavior.

3. A retirement path: when (s, r) is later taught or observed,
   resolve the uncertainty (supersede self-edge or equivalent), so
   the record tracks current epistemic state instead of accumulating
   stale fossils. The dynamics show uncertainty nodes are never
   retired: T30 only grows.

4. Guide content that learns: the guide's proposed action (field 20)
   and confidence (field 24) are written once as (30, -999) and never
   updated in production. A remembered-ignorance system needs the
   guide's content to change with experience, or the "policy" in
   POLICY_ROOT is a growing list of identical placeholders (the
   dynamics confirm: "act returns 30 every time").

## 6. Implications for the inquiry machinery's claim to be a learning system

1. The inquiry subsystem (miss -> UNCERTAINTY -> guide -> POLICY_ROOT
   -> ev_act) records ignorance but never learns from the record.
   Across 260 experiences: REUSE EVENTS 0, LEARNER-INTERNAL CRITERIA
   0 exercised, per-miss cost constant. It is a logging pipeline, not
   a learning loop.

2. It cannot satisfy K-H2-3 as constructed. K-H2-3 requires a
   learner-created persistent value in the causal chain of an
   accept/reject decision, with ablation of that value alone flipping
   the decision (anti-theater clause). The uncertainty node is in no
   decision's causal chain: ablating all T30 nodes changes no
   behavior. This is a structural prediction, verifiable by ablation,
   and it predicts K-H2-3 FAIL for frozen TNN-2 independent of the
   sealed worlds.

3. The duplicate-node symptom is the visible tip of the write-only
   design. Fixing the symptom (dedup) without the read path would
   satisfy a metric while leaving the architecture unchanged. The
   honest unit of progress is elements 2-4 of Section 5, which is why
   H3-lite's write-path audit (6 elements including "sealed
   behavioral variation") is the right gate: it demands the record
   change behavior, not just exist.

4. Connection to the reuse-path result: the same write-only pattern
   appears there (promoted MAP shadowed by a memorized FACT; the MAP
   never read). TNN-2's learner state is write-mostly across
   subsystems: facts, uncertainties, guides, and trial graphs are all
   appended far more than they are consulted. The ignorance-dedup
   finding is one instance of the general disease the lifetime-stream
   evaluation is meant to diagnose: state that changes continuously
   without the change ever feeding back into cognition.

## 7. Standing architectural metric (this analysis)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (read-only analysis).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0 (no mechanism built or run).
- SOURCE-ENUMERABLE FORMS: all (analysis of existing source).
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: 0 exercised (finding: none exist on the
  miss path).
- REUSE EVENTS: 0 observed (finding: the uncertainty record is never
  read, so never reused).
- REVISION EVENTS: 0 (finding: uncertainty nodes are never retired).
- COGNITION LINES: 0 added. MODES/BRIDGES/HANDLERS/SEMANTIC CASES:
  0/0/0/0.

## 8. Files

- `NAMECHECK.md`: Step 0 guard, scope, input provenance, constraints.
- `IGNORANCE_DEDUP.md`: this document.

## 9. Recommended follow-ups (for parent scheduling, not this task)

- Ablation test (unfrozen variant, white-box): delete all T30 nodes
  from a live learner and verify zero behavioral change. Predicted:
  no change. Would confirm Section 2d empirically.
- K-H2-3 pre-registration check: the structural argument in Section
  6.2 predicts FAIL independent of sealed-world content; record as a
  frozen directional prediction if not already present.
- Any future "remembered ignorance" work must be gated on the
  4-element mechanism of Section 5, with element 2 (production read
  path) demonstrated by sealed behavioral variation, not by
  allocation counts.
