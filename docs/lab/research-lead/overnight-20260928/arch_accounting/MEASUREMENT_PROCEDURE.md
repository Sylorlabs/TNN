# Architecture Accounting: Measurement Procedure

Date: 2026-09-30. Worker: Architecture Accounting Auditor.
Status: ARCH-ACCOUNTING-BASELINE-COMPLETE (baselines measured; CLA-2/CAM-1/ACT pending).

## Purpose

Micah's standing rule: track per architecture generation capabilities passed,
cognition source lines, semantic cases, modes, bridges, handlers,
learner-state bytes, and new learned structures. Desired trajectory:
capability and learner-created state increase while specialized code, modes,
bridges, and handlers decrease.

This document defines the exact measurement procedure so every generation
is counted the same way.

## Metric definitions

### 1. Capabilities passed

What it is: the count or label of sealed evaluation batteries the
generation passes, using frozen bars.

How to measure: read the frozen verdict from the canonical ledger or the
sealed run record. For the freeze challenge: X/9 WORLD-PASS. For other
lanes: the frozen verdict label (e.g. LEARNER-EXTENDED). Never infer;
quote the frozen record.

### 2. Cognition source lines

What it is: lines of researcher-written code implementing cognitive
operations: learning, retrieval, inference, retention/eviction, planning,
causal derivation, procedure induction.

How to measure:
1. Take the frozen cognition source file or files for the generation.
2. Count total lines with `wc -l`.
3. Count comment-only lines with `grep -cE "^[[:space:]]*//"`.
4. List every `^fn ` definition with its line span
   (`awk '/^fn /{...}'`).
5. Classify each function into exactly one category:
   - INFRA: IO, allocation, string conversion, byte helpers
     (emit, z_alloc, get32, set32, i32s, i64s, errln)
   - ACCESSOR: slot/field read/write helpers (rf, wf, sbase, sf, sw)
   - PARSE: event parsing, line splitting, integer parsing
   - DRIVER: main, world driver, test harness entry
   - DIAG: hashing, junk counting, collision recording, stage hashes
   - FIXTURE: frozen case loaders, hardcoded test data
   - LEGACY: superseded code retained for provenance
   - COGNITION: learn, query, eviction, importance, inference,
     causal derivation, plan synthesis, discovery, revision
6. Cognition source lines = sum of line spans for COGNITION functions.
7. Report the full categorized breakdown alongside the headline number.

Rationale: the metric tracks researcher-authored cognitive machinery.
Infrastructure and parsing are necessary but not cognitive. Diagnostics
and fixtures are test scaffolding. The COGNITION bucket is what must
shrink as intelligence moves into learner-created state.

### 3. Semantic cases

What it is: hardcoded branches on domain content: world type, relation id,
subject id range, or other target-domain values in the cognition path.

How to measure:
1. `grep -cE "^[[:space:]]*(switch|match)[[:space:]]"` on cognition sources.
   Must be 0; any occurrence is a semantic case.
2. `grep -nE "== *[0-9]{4,}"` to find hardcoded multi-digit id
   comparisons. Each hit is manually reviewed: newline/ASCII constants
   (e.g. 10 for '\n') are not semantic; domain ids (relation numbers,
   world ids, subject ranges) are semantic cases.
3. `grep -niE "world|task" ` in cognition functions, reviewed for
   per-world or per-task branches.

Count = number of confirmed domain-content branches in the cognition path.
Generic event-type dispatch (OBSERVE/QUERY/ACT) is not a semantic case;
it is the domain-neutral interface.

### 4. Modes

What it is: architectural modes that route cognition through different
subsystems (CAUSAL_MODE, REVISION_MODE, LANGUAGE_MODE, MEMORY_MODE,
PROCEDURE_MODE or equivalents).

How to measure: `grep -c "_MODE"` on cognition sources, then review each
hit. Ablation condition flags confined to one experiment file (e.g.
SEL_MODE, CARRY_MODE in hypd_v3) are noted but do not count as
architectural modes. Count = architectural modes only.

### 5. Bridges

What it is: dedicated cross-subsystem bridge mechanisms: researcher-written
code that translates between two separate cognitive stores or formats
(e.g. bridge_apply, bridge_learn between procedure and conditional stores).

How to measure: `grep -ci "bridge"` on cognition sources, then review.
A bridge is a function or mechanism whose purpose is translation between
two researcher-defined representations. Count = distinct bridge
mechanisms. The One-System Rule triggers review at three.

### 6. Handlers

What it is: task-specific handler functions: separate learn/query entry
points per cognitive domain (handle_proc_learn, handle_caus_query, etc.).

How to measure: `grep -c "^fn handle_"` on cognition sources, deduplicated
across copies. Count = distinct handler names. A single generic
learn/query path counts 0.

### 7. Learner-state bytes

What it is: the size in bytes of the persistent learner state that
carries information across episodes or worlds.

How to measure: find the state allocation in main or the driver
(`z_alloc(N)`), confirmed by the freeze record or REGIONS.md. Report N.
For workspace architectures: the workspace byte size plus the
append-only log size. Fixed slots and learner-structured workspaces both
count; the metric tracks capacity, while "new learned structures"
tracks what the learner does with it.

### 8. New learned structures

What it is: distinct types of learner-created structural state:
node types, edge types, or structural conventions that the learner
authors during operation and that did not exist as fixed slots.

How to measure: enumerate from the architecture prereg or the source.
Fixed-slot stores (key/value slots, ledgers with fixed schema) count 0:
the learner fills values but creates no structure. Each learner-authored
node type, edge type, or structural convention counts 1. Evidence:
white-box state inspection showing the structure present after
experience and absent before.

## Re-measurement triggers

Re-measure a generation when any of these occurs:
1. A builder commits an implementation for CLA-2, CAM-1, or ACT.
   Measure at the BUILD-PASS or BUILD-FAIL commit.
2. A new architecture generation is frozen (new prereg implementation).
3. The comparison protocol (128921ed9) runs CLA-2 vs contlearn2:
   both sides are measured with this procedure before scoring.
4. Any commit changes cognition source lines by more than 10 percent.

The auditor re-runs the full procedure on the new frozen source and
appends a dated row. Never edit a historical row.

## Scope note

These baselines measure the frozen cognition source files, not the
broader repository. The One-System audit (f2684204b) measured the
broader active substrate (7 handlers, 1 bridge repo-wide); those numbers
describe the codebase, while this table describes each frozen
generation's cognition source. Both are valid; do not conflate them.
