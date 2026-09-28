# Parameter-scaling prereg — frozen 2026-09-21/22, before any param run

Micah's question: data scaling changed nothing (mastery 1.0, 240 → 6.58M facts,
exactly linear cost). What happens when we scale the PARAMETERS — the TNN's
capacity, not its data? Fixed data size: N=24,000 (C=24, M=1000, P=1) — big
enough to matter, cheap enough to repeat.

## 1. Parameter inventory (the real capacity parameters of the learner core)

The learner core (`scale_learner.zag`, ported from championship `t5_core.zag`) is
a deliberately minimal deliberate-memory machine: evidence → eliminative verify
→ deliberate add. It has NO deliberation loop, NO hypothesis table, NO attention,
NO embedding dimension. Its actual capacity parameters:

| # | Parameter | Baseline (1×) | What it controls |
|---|---|---|---|
| P1 | SLOT_MULT | 1.0 (cap = N slots) | fact-slot capacity; <1.0 forces drops (rc=2) |
| P2 | EV_WIDTH | 64 codes | evidence-buffer width (codes + i64 vals) |
| P3 | VERIFY_DEPTH | 1 round | deliberation rounds per fact; install iff ALL rounds yield verdict 1 |
| P4 | AUDIT_MULT | 1.0 (cap = 2·slots+8192) | audit-ledger record capacity |
| P5 | REDUNDANCY | 1 copy | slot-level copies per fact (R consecutive slots, recall reads first) |

Chunk sizes (4096 slots/chunk etc.) are implementation constants, not capacity —
kept fixed. Slot record stays 24 B; audit entry stays 16 words / 64 B.

Mechanistic prediction (falsifiable): verification is a gate on evidence
*presence*, not on truth — the learner has no truth source. Re-running the same
deterministic gate (P3) or widening buffers (P2/P4) or duplicating storage (P5)
adds no new information, so verdicts should not change; only cost should move.
Capacity (P1) is the one parameter with a real behavioral edge: below 1.0 the
store fills and facts drop. Truth-detection is not expected from any parameter —
the web-search sense (12/12 teacher falsehoods caught via external corroboration)
shows what actually buys it: an independent information source, not capacity.

## 2. Config table (singly + jointly)

Singles (all other params at 1×):

| Sweep | Values |
|---|---|
| S-slot (P1) | 0.25, 0.5, 1, 2, 4, 8 |
| S-ev (P2) | 16, 32, 64, 128, 256 |
| S-depth (P3) | 1, 2, 4 |
| S-audit (P4) | 0.5, 1, 2, 4 |
| S-red (P5) | 1, 2, 4 |

Joint:

| Config | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|
| J-small | 0.5 | 16 | 1 | 0.5 | 1 |
| J-big | 4 | 256 | 4 | 4 | 4 |

19 unique configs (baseline counted once). Reps: 3 per config, 5 for baseline.
Byte-identity required within each config.

## 3. Measures (per config)

Clean mastery, all-fact mastery, §B.7 flaw battery (96), absorption (planted
falsehoods), ops/fact, measured bytes/fact (slot+index+audit allocations ÷ N),
byte-identical reps, learner digest (FNV-1a over (id, first-copy value)) —
digests comparable across configs since recall always reads the first copy.

## 4. Kill bars / decision rules

- KB-P-DET: any config with non-byte-identical reps → HALT, report.
- KB-P-EFF: efficiency frontier in (bytes/fact, ops/fact) × mastery. Any
  multiplier ≥2× cost with <1pp mastery gain is efficiency-dead (report, no halt).
- KB-P-EMERGE: absorption < 1.0 at any config (a bigger TNN catching ≥1 planted
  falsehood the baseline absorbs) → EMERGENT flag, reported prominently.
  Discovery, not halt.
- KB-P-GRACE: at SLOT_MULT=0.5, clean mastery over the *taught* subset (ids with
  slots) must remain 1.0 — capacity pressure may drop facts, never corrupt the
  ones that fit. Violation → GRACE-FAIL.
- Decision rule: if the small configs (ev16, audit0.5, depth1, red1, slots1)
  saturate mastery identically to baseline, the finding is parameter-
  insensitivity in this regime — a real result, reported as such.

## 5. Engineering constraints

- Pure Zag, zero RNG in decision paths. znc 2^25 slice limit: chunk as in the
  scale driver (implementation constants unchanged).
- Fidelity gate: all-1× config must reproduce the scale-up digests byte-exactly
  (N=240 → 44a61309cf780de1; N=24000 → 8e6238911bb7cef0) before the sweep runs.
- Build binaries and corpus texts excluded from commits (workspace convention).
