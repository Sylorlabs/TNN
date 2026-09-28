# DATED AMENDMENT — 2026-09-20 — RNGSCAN v2 (no-RNG auditor)

**Status:** DRAFT — PENDING Micah's approval. v2 does not start without it.
**Authority for drafting:** standing build-coordinator instruction (draft amendments, flag for review; never silently bend rules).
**Trigger:** K2 fired on RNGSCAN-2026-09-20-v1. Blind red-team round: 19/20 plants caught, 1 miss (miss rate 0.05 > 0). Per the frozen kill bar, the audit version is DEAD. The builder correctly stopped rather than bending the bar.

**The miss (plant20):** frozen prereg §4.5 bans the identifier substring `env_` (environment reads). The checker implemented `getenv`/`environ` but not the `env_` pattern — a transcription gap between the frozen banned list and the implementation. `fn get_env_flag()i32` with its result mixed into output passed with 0 hits. The red-team caught exactly what it exists to catch: the audit not enforcing its own frozen rule. Full evidence: `docs/lab/wave12/step1a-no-rng-audit/redteam/REDTEAM_REPORT.md`.

**What changes in v2:**
1. Rule 4.5 gains the `env_` identifier-substring pattern, keeping the `lookup_table` / `pin_table` carve-outs.
2. Precision-note ruling (plant01/02/16): the v1 dataflow's false-positive 4.3 hits on early-return paths are documented as a known precision limitation; scored verdicts were unaffected; no bar change.
3. Full re-run of all rounds under v2: 5-plant dirty round (5 FAIL attestations), clean round (PASS + byte-identical replay), 20-plant blind red-team round (miss rate must be 0).

**What does NOT change:**
- Kill bars K1/K2 themselves are unchanged.
- RNGSCAN v1 stays dead. No trial ever ran under v1; no v1-gated result exists or counts. The Arm C trial (Step 1e) remains gated on a PASSING audit version.
- The allowlist ALLOW-2026-09-20-v1 and all other banned categories are untouched.

**Review:** flagged for Micah's approval (or explicit retroactive review). On approval, v2 gets a new dated prereg version and the build order from the v1 prereg §6 re-runs in full.
