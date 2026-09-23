# STEP 2 prereg — per-episode audit entry/byte histogram instrumentation

Dated: 2026-09-20. Frozen BEFORE any build. Amendments dated only, flagged for
retroactive review.

## 1. What is measured
For each of the three Track 4 curriculum dry-run harnesses (code, english,
messy-reality), over 200 dry-run episodes at 1x: per episode, the number of
audit-ledger entries appended, the bytes those entries occupy, and the op-class
mix. One audit entry = 16 words = 64 bytes (canonical layout op@0 … d2@60;
slice 20 §3). Bytes/episode = entries × 64.

Op classes (op numbers verbatim from the reused substrates):
- add: ST_OP_ADD (1)
- revise: STRENGTHEN(20), WEAKEN(21), OVERWRITE(25), TRAINER_DECLARE(26)
- manage: PIN(3), UNPIN(4), PROMOTE(5), DEMOTE(6)
- kill: KILL(2), KILL_EVIDENCED(24)
- deliberation: EVIDENCE(22), JUSTIFY(23), ABANDON(29)
- verify: ROLLBACK(7)
- governance: SETSTAGE(8), FORCE_PIN(27), FORCE_UNPIN(28)
- trust-tier: TT_OP family 51..71 (verbatim op numbers from
  wave9/trust-tiers/substrate/trust_tiers.zag; MRC harness only)
- other: any op outside the above (must be zero; a nonzero count fails the run)

## 2. How it is measured
- `hist.zag`: one native Zag counter module. It does NOT modify the audit
  append path. The harness records `audit_n` at each episode start; at episode
  end the module scans the append-only ledger entries in [start, audit_n) and
  tallies op→class. Every appended entry is counted exactly once because
  attribution is by ledger position and the harness is the only appender.
  Rationale: the st_memory_core.zag substrate stays vendored byte-identical to
  wave10/debate-norecord (checked with cmp in the runner); zero divergence risk
  to replay semantics.
- One native binary, argv[1] selects harness (code|english|messy). 200 episodes
  per harness, deterministic variation from the episode index only (ep % N
  patterns). NO RNG anywhere (static-grepped in the runner).
- Each run executes each harness twice with identical args; the run is valid
  only if both transcripts are byte-identical (cmp).
- Output: one `EP,...` line per episode (entries, bytes, 9 class counts), then
  one `HISTAGG,...` line per harness: n, median/min/max/p90 of bytes/episode,
  class totals. Median via deterministic in-Zag sort.

## 3. Kill bar
- **K1 (slice 20 §4):** if ANY episode of ANY harness measures > 4096 audit
  bytes, the slice-20 cost model is falsified → verdict DEAD for the model,
  reported as-is. Implemented in-Zag as cl_check on max bytes ≤ 4096 and
  re-checked independently from the transcript by the runner.
- The 1 KiB nominal is NOT a kill bar: it is calibration output. The report
  states the measured median per harness and what fraction of episodes exceed
  1024 B; the 10x budgets scale from the measured median per slice 20 §3.

## 4. What the dry-run harnesses do (representativeness claims)
Full curricula do not exist yet. Each harness is a minimal dry run that
exercises the audit-traffic shape its curriculum's spec implies:
- **code** (slice 01): each episode = deliberate add of one concept-memory
  (canonical form + trace bundle + tags, strength by judgment), one
  deliberation record of trace-evidence review, periodic near-miss
  counterexamples (EVIDENCE), and periodic deliberate revision/kill of a
  superseded memory (EVIDENCE ×n + JUSTIFY + KILL_EVIDENCED). Every 5th episode
  is a fault-localization episode with 3 killing-evidence records (elimination
  record without which a localization scores 0 per slice 01).
- **english** (slice 02, E1): each episode = deliberate add of one word↔referent
  binding + one disambiguating-evidence record + justification; gavagai-style
  ambiguous episodes add a second evidence record + deliberate strengthen;
  periodic deliberate kill of a wrong binding (full evidenced-kill sequence).
- **messy** (slice 03, stage-1 contradiction+noise): episode type rotates
  clean / contradiction T1-vs-T1 / contradiction T0-vs-T1 (H1 hold) / noise /
  correlated noise. Clean: add + ORIGIN tag + corroborating CITE records.
  Contradiction: ABANDON (deliberate hold of resolution) + HOLD-family TT ops +
  citation records + justification. Noise: EVIDENCE of disagreeing observation
  + CHANNEL_DISTRUSTED, never a strengthen from noise. Periodic deliberate
  evidenced revision of a defeated belief.
- All three: one post-change verification per episode (st_replay_check +
  st_audit_clean_refusals, read-only) logged as one JUSTIFY entry — the
  "1–3 post-change verifications" term of the slice-20 model.

## 5. Acceptance
Build is accepted iff: all three harnesses compile under znc with the vendored
substrate byte-identical (cmp), no-RNG static check passes, both replicates
per harness are byte-identical, in-Zag K1 check and runner transcript check
agree, and RESULTS_STEP2.md reports the measured histograms plus the GO/DEAD
verdict on the 1 KiB nominal / 4 KiB cap model. Nothing else in Track 4 may
spend this number until it lands.
