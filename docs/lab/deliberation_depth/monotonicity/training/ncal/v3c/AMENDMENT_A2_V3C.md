# AMENDMENT A2 (pre-implementation) — supersedes A1's Design D mechanism

- **Date:** 2026-09-25 (PDT). **Status:** FROZEN. Amends the v3c prereg (commit
  `567b399f`) + A1 (`fae0a215`) BEFORE any implementation or scored run.

## Why A1's D was still wrong

A1 corrected D to no-latch but kept the NEW (exact-cell) schema. White-box simulation
of that combination on the s1 matrix gives B3 gviol = 0 and B13 = 0 — it does not test
the §2 lemma at all, because the exact-cell seeds are already ≈1.0 for always-correct
items (nothing to rise to). A diagnostic that cannot fail is not a diagnostic.

## §3.4 Design D (diagnostic, s1-only) — CORRECTED

**D = v3b K-A oracle schema (frozen `schema_ka.zag`, 35 bins, already built) + NO
minimum latch.**

- tp=0: conf = `ka_schema(cls)` (the v3b coarse seed, e.g. 0.775578 for bin 15).
- tp≥1: conf = p_raw (direct personal correctness rate), no latch of any kind.
- nopool=1. Traces as specified (tp≥1 rows carry `-` for prev_cl_mil).

**Predicted (pre-registered, from white-box simulation on the s1 matrix):**
B3 gviol = **6** — strict G rises d1→d2 on D (−0.085→0.000), O (−0.369→0.000),
admit (−0.025→0.000), cost (−0.208→0.000), logic (−0.052→0.000), revoke (−0.141→0.000)
→ B3-kill. B13 = 3 (revoke/d1, cost/d1, O/d1 — the tp=0 seeds still pin d1 cells low).

**What D proves:** with the coarse v3b seeds, the latch is NECESSARY for B3 (removing it
kills B3 with 6 rises) and FATAL for B13 (keeping it gives 22 violations). The B3/B13
tradeoff is structural given coarse seeds — confirming the §2 lemma empirically and
showing why the reference-class redesign (Design S) is the only §6-legal way to hold both.

s1 matrix only; not adoption-eligible. Implementation note: `ka_schema` already exists
in the v3b source tree; variant 28 needs no new schema.
