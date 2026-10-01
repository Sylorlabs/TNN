# Persistent Cross-Domain Connections Report

**Verdict: PERSISTENT-CONNECTIONS-COMPLETE.**

**Date:** 2026-10-01
**Worker:** Persistent Cross-Domain Connections Worker
**Cognition delta:** `pc_patch.zag` (+link write, +two-pass rebind) on the
frozen TNN-2 base. Base SHA-256
`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
verified byte-identical to frozen. Control arm uses the vanilla rebind
patch verbatim (`pc_vanilla_patch.zag` = `adv_patch.zag` from `91585087c`).

## 1. Problem

The spontaneous lifetime (`82dd6c00d`) showed functional reuse (B rebound
from A, 7 vs 11 verifies) but XEDGES a-b = 0: no persistent structural
trace of the A-B connection. The reuse happened and vanished. Micah
Priority 2: make the learner record that A helped construct B, then show
C exploiting that recorded relationship.

## 2. Mechanism

On every verified rebind, `pc_try_one` writes a LINK edge (type 14, unused
in the frozen base) from the newly promoted MAP to the helper MAP whose
shape was reused: "helper helped construct built". The write is performed
by the rebind success event itself. The driver never authors, hints, or
names any A-B relation.

`rebind_try` runs two passes:
- Pass 1: MAPs with an outgoing type-14 edge (previously built via
  rebind), newest first. The learner tries its own prior successful
  constructions before anything else.
- Pass 2: all other MAPs in id order.

`pc_del_links` deletes all type-14 edges (ablation). Correctness is
unchanged in all cases: execution verification still arbitrates every
candidate. Only search order changes.

## 3. World

Distractors (4 wrong-plen MAPs, low ids) -> A (plen-5 chain, trial-built)
-> 20-event gap -> B (plen-5 + distractor paths; rebinds from A, LINK
written) -> 20-event gap -> C (plen-5 + distractor paths, fresh literals).

Three arms, 3/3 byte-identical runs per arm (SHA-256 verified):
- Treatment: link write + two-pass rebind.
- Control: vanilla rebind, no links.
- Ablation: treatment binary, links deleted after B.

## 4. Results

### 4.1 Faster later retrieval: YES, 11x

| arm | B-MAIN ans | B tries | C-MAIN ans | C tries |
|---|---|---|---|---|
| treatment | 114 | 11/10 | 214 | **1/0** |
| control | 114 | 11/10 | 214 | 11/10 |
| ablation | 114 | 11/10 | 214 | 11/10 |

B is identical across arms (11 tries): the link mechanism does not affect
B; B creates the first link. C in treatment costs 1 verification against
11 in control. The link is the cause: B_MAP exists in the ablation arm too
(promoted during B), but with the LINK deleted C costs 11, exactly the
control cost. B_MAP's mere existence does not explain the speedup; the
recorded connection does.

### 4.2 Transfer: cheaper, equally accurate

All arms answer C correctly (214). Accuracy is 100% everywhere, so the
link does not change WHAT is transferred, it changes the COST: 11x fewer
verifications. Transfer becomes cheaper as the reuse history grows.

### 4.3 Reusable higher-level structure: YES

Type-14 census (treatment): 2 -> 2 -> 3 -> 4 across
distractors/A/B/C. The final link graph:

```
26 -> 13    (distractor reuse)
134 -> 98   (distractor reuse)
582 -> 428  (B_MAP -> A_MAP: A helped construct B)
630 -> 582  (C_MAP -> B_MAP: B helped construct C)
```

C's solution structurally references the prior reuse (C_MAP -> B_MAP),
forming a persistent C -> B -> A chain. This is the structural connection
the spontaneous lifetime lacked (XEDGES a-b = 0 there; here the A-B link
is a real edge, 582 -> 428). The structure is learner-authored: which MAPs
get linked is determined entirely by which rebinds actually verify.

### 4.4 Ablation: link removal destroys the advantage

After B the ablation arm holds 3 links (including 582 -> 428).
`pc_del_links` confirmed at census 0. C then costs 11 tries, identical to
control. The speedup is not a priming or ordering artifact; it requires
the persistent link.

Notably, the ablation arm re-learns: C's slow id-order rebind finds A_MAP
(lower id than B_MAP) and writes a fresh link 736 -> 428 (C_MAP -> A_MAP),
census 0 -> 1. The mechanism rebuilds the connection from scratch when the
record is destroyed, at full search cost.

## 5. What this establishes

1. Rebind success now leaves a persistent structural trace (type-14 edge),
   written by the learner's own success event, not by the researcher.
2. A later query exploits the trace: 11x fewer verifications (11 -> 1).
3. The trace composes: C -> B -> A forms a growing cross-domain link
   graph, each link recording a real "helped construct" event.
4. Ablation is causal: delete the links, the speedup disappears; the
   learner re-learns them at full cost.
5. No researcher-authored A-B mapping exists anywhere. The driver teaches
   chains and queries; all links come from verified rebinds.

## 6. What this does NOT establish

- The link-priority rule itself (try linked MAPs first, newest first) is
  researcher-authored. Only the link contents are learner-owned.
- Accuracy transfer is unchanged (100% all arms); the gain is cost.
- Chain family only (inherited from the rebind mechanism).
- The distractor-distractor links (26 -> 13, 134 -> 98) show the mechanism
  is generic, but the experiment does not test link utility under many
  competing links (scale attack on pass 1 is open).
- Pass-1 newest-first ordering was not ablated against oldest-first; the
  C -> B (rather than C -> A) topology follows from it.

## 7. Standing metrics

- RESEARCHER-OWNED: pc_patch.zag (~90 lines: link write, two-pass scan,
  deletion); driver world-stream design.
- LEARNER-OWNED: all type-14 link endpoints and topology (determined by
  verified rebinds); all MAP graphs.
- SUF DECISIONS: 0. REUSE EVENTS: 3 per treatment run (D3-1, D4-1, B, C
  rebinds; B and C create the cross-domain links).
- COGNITION LINES: ~90 added. MODES: 0. BRIDGES: 0. HANDLERS: 0.
  SEMANTIC CASES: 0.

## 8. Process notes

- Toolchain guard: safebin PATH, `which python3 python` empty. One shell
  idiom typed `python3 - ... || sed ...`; under the guard PATH python3 was
  not found (exit 127) and sed performed the edit. No Python interpreter
  executed; verified the edited file by diff. Idiom not repeated.
- A 12-distractor pilot was killed at ~11 min: rebind-then-trial on A cost
  54+ verifications under memory pressure. Redesigned to 4 distractors;
  full 9-run battery completes in ~2 s with identical scientific content.
- Determinism: 3/3 byte-identical per arm, exit 0, zero stderr.
- Paper untouched. Nothing pushed. Frozen source read-only.

## 9. Artifacts

- `NAMECHECK.md` (Step 0 guard, provenance)
- `REPORT.md` (this file)
- `pc_base.zag` (frozen base copy, SHA verified)
- `pc_patch.zag` (link mechanism)
- `pc_vanilla_patch.zag` (control: vanilla rebind, verbatim)
- `pc_driver_treat.zag`, `pc_driver_abl.zag` (world streams)
- `pc_full_treat.zag`, `pc_full_ctrl.zag`, `pc_full_abl.zag` (assembled)
- `pc_treat_bin`, `pc_ctrl_bin`, `pc_abl_bin` (binaries)
- `pc_treat_run1/2/3.txt`, `pc_ctrl_run1/2/3.txt`, `pc_abl_run1/2/3.txt`
- `pc_*_compile.txt` (znc diagnostics)
