# H-DIAG Result: Root Cause of H-STRESS Slot-0 Retention Failure

**Date:** 2026-09-29
**Prereg:** PREREG_DIAG.md (commit `cf50b7442`, frozen before investigation)
**Method:** Pure Zag, no Python. Diagnostic binary built to /tmp only.
**Raw evidence:** Diagnostic dumps (see below), committed source.

## Verdict: Root Cause Identified

**K-D1 (root cause identified): PASS**
**K-D2 (bug vs limitation classified): PASS**
**K-D3 (fix sketched): PASS**

## The Failure

H-STRESS KILLED because procedure slot 0 (reverse, learned in E1) no longer
maps `hello`->`olleh` after the 16-event pressure sequence. Bridge rule 0,
causal rules, and proc slots 1-15 remain intact.

## Investigation

### Step 1: Byte-level slot-0 trace (H1 test)

Built a diagnostic copy of `stress_learn.zag` (in /tmp, not committed) with
a `dump_slot0` function emitting `used`, `nnodes`, and program bytes after
each event E1-E9, F1, F2, EK1.

Result: **Slot-0 bytes NEVER change.**
```
DIAG E1 used=1 nnodes=5 prog=3,255,255,4,255,255,0,255,255,6,1,2,5,0,3,
DIAG E2 used=1 nnodes=5 prog=3,255,255,4,255,255,0,255,255,6,1,2,5,0,3,
...
DIAG EK1 used=1 nnodes=5 prog=3,255,255,4,255,255,0,255,255,6,1,2,5,0,3,
```

**H1 (overwrite bug): REFUTED.** No write corrupts W[0..64] after E1.

### Step 2: Program decoding

The 15-byte program (nnodes=5):
```
[3,255,255, 4,255,255, 0,255,255, 6,1,2, 5,0,3]
```

Decoding (types: 0=K, 1=N, 2=C0, 3=C1, 4=C2, 5=ADD, 6=SUB):
- Node 0: [3,255,255] = C1 = 1
- Node 1: [4,255,255] = C2 = 2
- Node 2: [0,255,255] = K
- Node 3: [6,1,2] = SUB(Node1, Node2) = 2 - K
- Node 4: [5,0,3] = ADD(Node0, Node3) = 1 + (2 - K) = **3 - K**

**The stored program is `3-K`, NOT `n-1-k`!**

### Step 3: Why proc_apply fails

`proc_apply(W, PBASE(), 0, "hello", o)` with n=5:
- k=0: 3-0=3 → 'l'
- k=1: 3-1=2 → 'l'
- k=2: 3-2=1 → 'e'
- k=3: 3-3=0 → 'h'
- k=4: 3-4=-1 → **idx < 0 → proc_apply returns 0**

The program `3-K` is a **length-specific overfit**. It correctly reverses
n=4 inputs (the E1 training: "abcd", "efgh") but fails on n=5 ("hello").

**H2 (index confusion): REFUTED.** `slot_rev`=0 is correct, `proc_apply`
correctly reads slot 0, and correctly returns 0 (failure) because the
program produces an invalid index. The read path is not at fault.

**H3 (intentional eviction): REFUTED.** `proc_store` contains no eviction
logic; it only scans for `used==0`. Code reading confirms.

**H4 (bridge interference): REFUTED.** The byte dump proves no bridge
operation touches slot 0. Bridge store (1024..1103) is far from slot 0
(0..64).

## Root Cause

The procedure discovery search (`pdiscover_direct`) enumerates programs in
a fixed syntactic order and returns the **first** program that fits all
training pairs. It has **no generality bias**.

For E1 training ("abcd>dcba;efgh>hgfe", both n=4):
- `3-K` (5 nodes) fits and is enumerated before `n-1-k` (5 nodes).
- The search returns `3-K`, a length-specific program.

**Cross-check with H-UNIFIED:** That test used mixed-length training
("abc>cba" n=3, "xy>yx" n=2). `2-K` fits n=3 but NOT n=2 (for "xy", k=0
gives idx=2 which exceeds n=2). The mixed lengths **forced** the search to
find the general `n-1-k`. This is why H-UNIFIED passed 9/9 while H-STRESS
failed on slot 0.

This is the **same failure mode** the CC-A3 adversary identified:
a spurious coincidental fit (`SUB(C2,K)=2-k`) that works on training length
but fails to generalize.

## Classification: Architectural Limitation (Not a Memory Bug)

**K-D2: PASS.** This is an **architectural limitation** of the discovery
mechanism, not a memory-safety bug:

- Memory is intact (bytes never change).
- Storage and retrieval are correct.
- The problem is the **discovered procedure itself** is overfit.
- The search lacks a generality preference (no bias toward N-using programs,
  no validation on varied lengths).

The H-STRESS KILL stands: the system does not retain a working reverse
procedure under the test's definition. But the mechanism of failure is
overfitting at discovery time, not corruption at retention time.

## Fix Sketch (Not Implemented - Out of Scope)

**K-D3: PASS.** Three concrete fixes, any one of which addresses the root cause:

1. **Generality bias in search order:** Enumerate N-using programs before
   constant-only programs. A program referencing N is more likely to
   generalize across lengths than one using only small constants.

2. **Multi-length validation:** During discovery, test each candidate
   program on synthetic inputs of varied lengths (not just training
   lengths). Reject candidates that produce invalid indices.

3. **Mixed-length training requirement:** Document that single-length
   training is insufficient; the router/handler should warn when all
   training pairs share the same length.

Option 1 is the most surgical (affects only enumeration order). Option 2 is
the most robust (catches all length-specific overfits). Option 3 is
documentation-only.

## Implications for Canonical State

- H-STRESS KILL is **upheld** but **recharacterized**: the failure is
  discovery-time overfitting, not retention-time corruption.
- The procedure discovery mechanism (bounded L2+) has a confirmed
  **generality gap**: it finds length-specific programs when training
  lengths are uniform.
- This strengthens the case for NQ2 (learned routing) and suggests a new
  sub-question: can the discovery mechanism acquire a generality bias?
- The F-LEAK finding (E9 wastes 2 slots) remains a separate, confirmed
  memory-management bug.

## Commits

- `cf50b7442`: Prereg H-DIAG FROZEN (K-D1..K-D3)
- (this commit): Diagnosis report

## Files

- PREREG_DIAG.md (committed in prereg)
- DIAG_RESULT.md (this file)

## Verification

- No em dashes in authored docs.
- No binaries committed (diagnostic binary built to /tmp only).
- No Python used at any stage (only znc + shell tools).
- Diagnostic output confirms byte-stability of slot 0 across all events.
