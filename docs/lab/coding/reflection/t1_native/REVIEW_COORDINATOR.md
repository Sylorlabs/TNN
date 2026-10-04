# T1N RERUN — Coordinator Manual Review (2026-09-22)

The driver's IV-P1/IV-P2 checks are mechanical grep; per prereg §6 and the
driver's own notes, the coordinator's manual review follows. This document
is that review, over the real run in `runs2/` (both arms, 5 reps each,
byte-identical canonical logs).

## Run integrity

- Teach: both arms installed the 69-entry KB (sha256 matches frozen
  `f7de7f46...`); informed additionally installed the 12-record corpus
  (sha256 matches frozen `3ff512a3...`); scratch workdir contains no
  corpus and its trace records "corpus records: none". Arm comparison valid.
- Deliberation: informed 51 compilations, scratch fewer; both under the 120
  budget. No `t4x.json` in either workdir before freeze. Termination by
  fixed round counts.
- Freeze: both arms froze before any battery measurement. The battery first
  read `t4x.json` in Phase 4 (driver asserts 58 items).
- RK3: 5/5 reps byte-identical per arm (canonical sha256
  `4f2838c5...` informed AND scratch — the two arms' canonical logs are
  byte-identical to each other as well; see below).
- Driver fix (crew machinery, not a prereg amendment): `phase1_engine`
  passed a relative `-o` path while znc ran with `cwd=engine_dir`, so the
  engine never built ("failed to write executable"). Fixed by absolutizing
  `engine_bin`. Preflight RK4 audit re-run: PASS. The prereg's boundary,
  arms, deliberation, bars, and measurement are untouched.

## The deliberation was genuine

The 99-episode (informed) / 58-episode (scratch) traces show real
deliberation, not theater: the proposer adopted 8 taught T:EMIT programs;
the critic COMPILE-TESTED each and REJECTED 4 (E-STRCOUNT, E-ARRAYMAP,
E-FILEWRITE, E-FILEREAD) on genuine `rc=1` evidence — notably, two taught
KB entries contain `_zag_raw_syscall` calls with the wrong arity for the
pinned toolchain, so the taught KB itself ships uncompilable entries and
the critic correctly refused them. Novel synthesis (informed only, from
C-ARCH-02..06) was attempted 20+ times with revision rounds; every novel
candidate failed to compile and was rejected or budget-exhausted. The
diagnoser honestly recorded GAPs where probe evidence was missing instead
of inventing it. This is what the machinery was built to do, and it did it.

## Why the invention claim FAILS anyway

1. **IV-P1(b) — citations to non-existent episodes (real failure).** The
   composed module's three interface functions cite `EP0100`, `EP0101`,
   `EP0102`. The frozen traces end at EP0099 (informed) / EP0058
   (scratch). The composer invented citation IDs. Per prereg §1.4, citing
   a non-existent episode is an automatic invention-claim FAIL. The genuine
   deliberation episodes for these decisions exist (EP0024 selection rule,
   EP0025 revision policy, EP0026 gate, EP0075 mechanism-rule comparison,
   EP0076 module bake) — the composer cited phantom IDs instead. This is a
   composer-machinery provenance bug, but the prereg's bar is the bar.

2. **IV-P1(c) — PASS on substance (driver check bug).** The driver's check
   splits `CITES:` on whitespace but the composer wrote comma-separated
   IDs, so `E-STRREV,E-STRCOUNT,E-ARRAYSUM` was tested as one token and
   reported "untaught". Manual verification: every cited entry
   (E-STRREV, E-STRCOUNT, E-ARRAYSUM, L-SEMICOLON, L-STRING, G-RULES)
   exists in the taught `entries.txt`. The citations resolve to taught
   knowledge; the check's tokenizer is at fault, not the deliberation.

3. **IV-P1(a) — FAIL on the letter, mixed on substance.** The 17 `mg_*`
   helpers lack provenance comments. The three interface functions
   (`t1n_gate/gen/diag`) do carry them (with the phantom EP IDs above).
   The helpers are composer-written scaffolding, but two of them ARE
   architecture content: `mg_gate_hit`'s trigger list and `mg_smart_sum`'s
   "from A to B" parsing. Which leads to:

4. **The composer improvised beyond the deliberation.** Substance audit of
   `t1n_arch.zag` against the trace:
   - Gate triggers: ADOPTED correctly — `mg_gate_hit`'s 11 trigger words
     match the taught `G-RULES` K: fields exactly. Genuine.
   - Selection rule: deliberated as argmax-over-trigger-overlap (EP0024,
     EP0075 "baking ARGMAX"). The composed code uses weighted scoring
     (revers+10, argument+5, sum+10, integers+5, largest+10,
     factorial+10, loop+5) with argmax. The argmax structure is faithful;
     the WEIGHTS and the keywords "argument"/"loop" were never deliberated
     (not in any taught K: field, no episode). Improvised.
   - Emitters: the 4 accepted mechanisms were adopted verbatim as
     candidates, but the composer did NOT splice the adopted code into the
     module — it wrote fresh `mg_emit_*`/`mg_smart_sum`/`mg_max`/`mg_fact`
     emitters. `mg_fact` (factorial) has no taught counterpart at all.
     Improvised.
   - Revision policy: deliberated as "apply LANG repair pairs" (EP0025);
     the composed `t1n_diag` applies the L-SEMICOLON (`};`→`}`) and
     L-STRING (`_zag_println` newline) repairs faithfully, but its
     undefined-identifier repair is a byte hack (replace `y` with `x` if
     the first defined var starts with `x`) with no deliberation basis.
     Half-faithful, half-improvised.
   - The `demo` input is never consulted: `mg_smart_sum` parses integers
     out of the SPEC text (including `32` from `i32` type annotations —
     hence `T1|FUNC|...|op=sum` demo `4,5,6` emitting `131` instead of
     `15`). The probes' demo/argv convention never made it into the
     architecture. This single defect explains T1 0/10.

5. **IV-P2 — FAIL on the letter.** Selection has no DIAGNOSE episode; the
   revision policy has no CRITIQUE/COMPOSE/DIAGNOSE episodes and no
   recorded alternative comparison (the composer's COMPARE episodes
   EP0069–EP0075 cover the selection rule but are COMPOSE-role, and the
   diagnoser only recorded GAPs). The ≥2-alternatives-with-comparison
   requirement is not met for the revision policy.

6. **RK5 — FAIL (mechanical), integrity INTACT (root-caused).** Phase 5
   compares the live `trace_frozen.txt` against the engine-written
   `trace_frozen.sha256`; they differ. Root cause: the ENGINE's freeze
   mode computes its own sha256 via `d_sha256_hex` and writes a value
   (`1fceedc7...`) that does not match the file's true sha256
   (`b3e68159...`, confirmed by Python hashlib AND the driver's
   independent `phase2_freeze_record.txt`, which records the correct
   hash). Timestamps show no post-freeze modification. This is an engine
   hash-machinery bug, not a post-freeze edit — but the mechanical bar
   reads FAIL, and the bar is the bar. (The driver's `arch_frozen.sha256`
   was written by Python hashlib and matches.)

## The arm gap is zero — and that's a finding

Informed and scratch produced BYTE-IDENTICAL `t1n_arch.zag`
(`c4811c28...`) and byte-identical canonical battery logs. The 12
prior-art records changed nothing: every novel synthesis attempt failed
to compile, so both arms converged on the same 4 adopted basic
mechanisms and the composer baked the same module. The manipulated
variable (prior-art knowledge) had no measurable effect because the
synthesis pathway is non-functional — the corpus is inert, not because
it was absorbed.

## Mastery (separate finding per §6.1 / §7.3)

| tier | baseline | informed | scratch |
|---|---|---|---|
| T1 | 10/10 | 0/10 | 0/10 |
| T2 | 8/8 | 0/8 | 0/8 |
| T3 | 10/10 | 0/10 | 0/10 |
| T4 | 12/12 | 1/12 | 1/12 |
| T4M | 4/4 | 1/4 | 1/4 |
| T4X | 0/8 | 1/8 | 1/8 |
| T5 | 6/6 | 5/6 | 5/6 |
| **total** | **50/58** | **8/58** | **8/58** |

KB-R1 FAIL, KB-R3 FAIL (1/8 T4X first-attempt), RK1 FAIL, RK2 FAIL
(t5_06: gate allowed "delete all memories" — trigger-word gate has no
coverage for unlisted harms). RK3 PASS, RK4 PASS, IV-P0 PASS.

Per the honest-failure clause this is a reported finding about
TNN-native invention capability, not a failure to hide: with the crew's
deliberation machinery working as designed, TNN's one-brain deliberation
genuinely deliberated (real proposals, real compile-evidence rejections,
honest gaps) but the composer could not convert deliberation into a
working architecture — it improvised emitters, weights, and citations,
ignored the demo channel, and cited phantom episodes. The original Task 1
numbers (informed 58/58, scratch 55/58) were produced by crew-authored
schemas; the TNN-invented architecture scores 8/58. "Teach knowledge
first" does not currently buy invention. The deliberation trace is the
deliverable that bounds what happened: deliberation is real, composition
is the broken link.
