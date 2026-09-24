# PREREG — 10GB N-key investigation: three resolutions head-to-head

Date: 2026-09-24. Status: PREREGISTERED — no variant runs yet.
Corpus: dryrun_facts.dat (7 sources, 9,327,214 records,
SHA256 af10db8b03c47e91d809092d89e35f96a7a533c7f9aa2e331200e113818bc690)
— same verified inputs as DRYRUN_REPORT 2026-09-24.

## Background (mechanism, established before prereg)

- Source `r9_emit_unit` (clean2.py) splits >4096-byte SE posts into
  ≤4096-byte chunks keyed `se:<site>:<q|a>:<id>~N` (N=0,1,2...).
  117,470 records carry `~` keys; 91,866 kind-6.
- Gate `ig_se_key_ok` (gate.zag:579) requires all-digits after the post
  id → `~` fails → G3 verdict 3 (REJECT). GATE_SPEC G3 frozen.
- Lesson CAL (`ig_process_lesson`): first 4 records of each 65,536-record
  lesson are must-accept probes; ANY probe failing the gate drops the
  WHOLE lesson. Dry run: 3 lessons dropped × 65,536 = 196,608 records
  (2.1% of corpus) lost because a lesson-head record had a `~N` key.
- Install re-gates every record: `~N` records are individually
  G3-rejected even in surviving lessons.
- NOTHING downstream parses the post id numerically (verified by source
  read): keys are used for G2 adjacent-dupe byte-equality, merge/sindex
  byte-order sort, and panswer citation display. `~`(126) sorts
  deterministically after digits. The digits-only rule serves no
  integrity function — the rejection is spec-compliant but the SPEC is
  stricter than any consumer requires.

## Variants

- **V0 baseline**: rebuild committed gate.zag with pinned toolchain
  (znc_linux_x86_64_abed8aa1); must be byte-identical to dryrun/
  gate_bin_fixed or the rebuild is invalid. Frozen behavior.
- **V1 admit-`~N`**: `ig_se_key_ok` accepts one `~N` suffix
  (N = 1+ digits) after the numeric post id. `ig_se_is_q` inherits via
  the shared check. Question chunks still need `\n\n` (unchanged rule).
  Requires GATE_SPEC G3 amendment (governance if adopted).
- **V2 skip-rejected-in-CAL**: must-accept probe selection scans forward
  past gate-rejected records to find 4 gate-accepting probes per lesson;
  if <4 accepting records exist in the lesson, the lesson is REJECTED
  (stuck-gate detector preserved). Must-reject synthetic probes unchanged.
  Per-record install gating unchanged (`~N` still individually G3'd).
- **V3 re-key upstream**: source-stage re-key of chunks into keys the
  CURRENT grammar accepts, provenance-honest only. Hypothesis to test:
  no honest re-key exists (appending digits corrupts the post id;
  `:` inside the id field fails the grammar) — expected outcome is a
  documented impossibility proof, or a content-losing fallback
  (truncate to chunk 0). Tested on a tilde-only micro-corpus, not full.

## Bars (all must hold; any violation KILLS the variant)

1. **Determinism**: per variant, teach ×2 → `diff -r storeA storeB` rc=0
   AND aggregate store SHAs identical. KILL on any byte difference.
2. **Integrity**: negcontrol 1000/1000 every run; all 4 must-reject
   synthetic probes fire per lesson (lesson audit shows zero
   must-reject acceptances); seal present and deterministic across the
   variant's two runs. KILL on negcontrol<1000 or any must-reject pass.
3. **No silent widening**: G1 and G2 counts per variant must be within
   ±0.1% of V0 (the variants only touch G3-key and CAL selection).
   KILL on larger drift (indicates patch touched the wrong path).
4. **Coverage prediction match**: V1 installed must equal
   V0_installed + (probe-predicted admittable tilde records) EXACTLY.
   V2 installed must equal V0_installed + (good non-tilde records in
   the 3 rescued lessons) EXACTLY. Predictions computed by nkey_probe.py
   BEFORE variant runs. Any deviation = patch/model bug, investigate.

## Discrimination

Winner = max legitimate-record coverage subject to bars 1–4.
If V1 and V2 both pass: report both; the choice is governance
(spec amendment vs CAL-selection change) with the tradeoff table.
V3 expected to reduce to "impossible without content loss or spec
change" — if so, that IS the result (do not force a broken re-key).

## Cherry-picking (fast iteration before full runs)

- CP1: tilde-only micro-corpus (all 117,470 `~` records, sorted) through
  V0/V1/V2 gate classification only (no teach) — verifies per-record
  verdicts match the probe prediction.
- CP2: the 3 dropped lessons' records (196,608) as a micro-corpus —
  verifies V2 rescues the lessons and V1 installs the admittable subset.
- CP3: se_math-only teach ×2 per variant (tilde records concentrate
  there — verify with probe) for fast full-pipeline signal before the
  9.3M full-corpus confirmation runs.

## Run order

1. nkey_probe.py → predictions (running).
2. Rebuild V0, verify byte-identical to gate_bin_fixed.
3. CP1/CP2 classification checks.
4. Build V1, V2 (scratch-only .zag copies; committed gate.zag untouched).
5. CP3 fast signal → full-corpus teach ×2 per variant (sequential).
6. V3 impossibility analysis on micro-corpus.
7. Report as results resolve.

## AMENDMENT A1 (2026-09-24 ~17:05 UTC, before full V2 runs)

V2 semantics corrected — the prereg text ("scans forward past
gate-rejected records to find 4 gate-accepting probes") is NOT what is
built, because forward-scanning the stream would require buffering the
scanned prefix (the processor only buffers 4 records) and would change
stream-consumption order. What V2 actually implements (pure Zag,
`gate_v2.zag`, scratch-only):

- Peek window: up to 256 lesson-head records are classified with a
  LOCAL copy of the G2 prev-chain (real prev-chain untouched).
- Must-accept = the canary: the lesson proceeds iff >=4 window records
  PASS the gate. <4 accepts in a full 256 window -> lesson REJECTED as
  a unit, audit mask bit 8 set (mask = 256 + nacc).
- Final partial lesson (<4 records at stream end) keeps V0 semantics:
  all present records must pass.
- Must-reject synthetic probes UNCHANGED (4 per lesson, same R1..R4).
- Install: window records in stream order (re-gated against the real
  prev-chain, verdicts deterministic), then the lesson tail streamed
  as before. Per-record install gating UNCHANGED — `~N` records are
  still individually G3'd under V2.
- Net effect: a lesson is judged on its acceptable records, not on the
  first 4 positional records; a lesson of 100% rejects still trips the
  canary (mask=256), preserving the stuck-gate detector.

## AMENDMENT A2 (2026-09-24 ~17:05 UTC, determinism method)

Bar 1 prescribed `diff -r storeA storeB` per variant. DISK: 8.2G free,
one full teach store = 4.7G — two stores cannot coexist. Amended
method: per variant, teach x2 SEQUENTIALLY (one store on disk at a
time); compare manifest fields + aggregate store SHA (sorted relpath +
per-file SHA256, hashed — same construction as the dry run's
store1_aggsha.txt). Any byte difference changes the aggregate SHA, so
this is byte-equivalent evidence. V0 runs x1 only (rebuild validation
against the dry-run manifest; V0 determinism already proven by the dry
run's store1/store2 byte-identical pair with a byte-identical binary).

## AMENDMENT A3 (2026-09-24 ~17:05 UTC, V3 hypothesis updated)

The prereg's V3 impossibility hypothesis is WITHDRAWN — a concrete
honest scheme exists and will be TESTED head-to-head on the full
corpus (not just argued):
- Only kind-6 needs re-keying (CP1 proved kind-5/7 grammars already
  admit `~` keys: V0 installed 23,434 of 25,604 non-kind-6 tilde records).
- Scheme: `se:<site>:<q|a>:<id>~<n>` ->
  `se:<site>:<q|a>:<10^12 + id*10000 + n>` (n < 10000).
  Injective while genuine SE ids < 10^12 and n < 10000; provenance
  recoverable by arithmetic (id = (k-10^12)//10000, n = (k-10^12)%10000).
  Chunks sort after all genuine records in their (site,q/a) group, so a
  single streaming pass with per-group chunk buffering re-sorts honestly.
- Predicted full-corpus outcome: installed/g-counts IDENTICAL to V1
  (same admitted set). The head-to-head then turns on qualitative bars:
  key opacity, the baked-in 10^12/10^4 bounds (silent-collision fragility
  if upstream ids ever exceed them), and the extra re-sort pass — vs
  V1's transparent `~N` provenance + one-line grammar amendment.
- Bar 4 prediction for V3: V3_installed == V1_installed EXACTLY.
