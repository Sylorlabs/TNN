# DATED AMENDMENT — 2026-09-20 — RNGSCAN v3 (no-RNG auditor)

**Status:** DRAFT — PENDING Micah's approval. v3 does not start without it.
**Authority for drafting:** standing build-coordinator instruction (draft amendments, flag for review; never silently bend rules).
**Trigger:** K2 fired on RNGSCAN-2026-09-20-v2. Blind red-team round: 3 verdict-level misses among 14 scored plants (07, 10, 11); plants 15–20 never scored. Miss rate ≥ 3/20 > 0 → the audit version is DEAD. K3 also fired on the three miss plants (moot alongside K2, recorded). The scorer stopped the round honestly; no fixes attempted, no re-runs. Full evidence: `docs/lab/wave12/step1a-v2/redteam/REDTEAM_REPORT.md` (commit `d368014`).

## The misses (diagnosis, not excuses)

- **M1 — plant07 (4.3 uninit).** An even-slots-only init loop, shaped exactly like a full init loop, was marked INIT; the genuinely-uninitialized odd slots were missed. Root cause: the 4.3 analysis checks loop *shape*, not *coverage*. A shape test cannot distinguish full init from partial init.
- **M2 — plant10 (4.4 hash-iteration).** A from-scratch open-addressed table named `EntrySet` was invisible to the 4.4 scan. Root cause: 4.4 detection is identifier-token-based; a hand-rolled structure with a clean name evades it. (The v1 prereg §11 already flagged 4.4 as the weakest rule — the red team has now proven it.)
- **M3 — plant11 (4.4 hash-iteration).** The same real map, literally named `pin_table`, rode the pinned-table carve-out untouched. Root cause: the carve-out is keyed on *name*, not on const-ness + `// PINNED` marking + attestation hashing.

## Watch items the round exposed (not misses, but load-bearing)

- **W1 — static-scan gaps papered by replay (plants 01, 02, 04, 05, 06).** Computed syscall immediates, a runtime-built `/dev/urandom` path, and a compiler timer intrinsic were caught ONLY via replay divergence — both static scans missed the mechanisms entirely. Root causes: (a) the object scan recovers immediates moved directly before `syscall`, but not syscall numbers carried through registers (`mov reg,imm32` … `mov eax,reg` → `syscall`); (b) `_zag_clock_monotonic_ms` matches no banned token; (c) runtime-built paths leave no literal bytes for the byte search. Defense in depth worked, but the static arms are weaker than claimed.
- **W2 — replay hid behind zeroed pages.** K1 did not fire on the uninit miss plants "for the wrong reasons": the allocator zeroed the heap, so the uninitialized reads were deterministically zero across runs. Replay-as-backstop is blind to uninit reads on a zeroing allocator. The backstop needs adversarial conditions, not just repetition.
- **W3 — spurious 4.3 hits (plants 01, 03).** Kernel-filled buffers drew 4.3 hits — fail-closed luck that caught the plants for the wrong reason, and a false-positive risk for honest clean modules.

## What changes in v3 (proposed)

1. **4.3 — strict canonical init form.** INIT is granted only for the exact form `while(i<BUF.len){ BUF[i]=<expr>; i=i+1; }` with the write guarded by nothing, the index exactly the loop counter, and no early exit before completion. Any conditional in the body, any non-counter index expression, any `break`/`return` before the loop completes → 4.3 hit (fail-closed). Blessed pattern for kernel-filled buffers: explicit full-range zeroing loop after alloc (the v1 clean-round precedent) — documented, not weakened.
2. **4.4 — structural, not token-based.** On the variation path, only index-iterated slices/arrays are permitted. Any struct/type with insert/put + iterate/enumerate methods where iteration is not plain index order → 4.4 hit. The identifier token list is retained as a first-pass tripwire only.
3. **Carve-out narrowed.** `lookup_table` / `pin_table` are exempt ONLY when the declaration is `const`, marked `// PINNED`, and hashed into the attestation. A mutable map gets no carve-out regardless of its name.
4. **Object scan — register taint for syscall numbers.** Track `mov reg,imm32` … `mov eax/rax,reg` → `syscall` within a bounded window (bounds documented from observed znc lowering), in addition to the existing immediate-before-syscall recovery.
5. **4.2 — intrinsic surface audit.** Explicitly ban `_zag_clock_*`; one-time audit of the full `_zag_*` intrinsic surface with the rest allowlisted by name in the prereg.
6. **Replay hardening.** N runs per replay check (e.g. 8, not 2) plus heap pre-dirtying (allocate-and-fill garbage before the trial binary runs) to defeat zeroed-page hiding of uninit reads. The prereg must name the disguise classes that remain replay-backstop-only in principle (residual risk stated, not hidden).
7. **Fresh blind round.** Plants 15–20 (unscored this round) plus new plants covering the fixed gaps; same K2 bar (miss rate 0 over 20); same blinding discipline (separate agent, frozen prereg + clean template only).

## What does NOT change

- Kill bars K1/K2/K3 themselves are unchanged.
- RNGSCAN v1 and v2 stay dead. No trial ever ran under either; no result gated on them exists or counts.
- The Arm C trial (Step 1e, prereg frozen at `97882fc`) stays gated on a PASSING auditor version. The 1e builder does not start.

## Review

Flagged for Micah's approval (or explicit retroactive review). On approval, v3 gets a new dated prereg version (`PREREG_NO_RNG_AUDIT_V3.md`, frozen before any code) and the full build order re-runs: dirty round → clean round → freeze → blind round. Estimated scope: moderate — the checker is ~1280 lines of Zag and the fixes are localized (4.3 form check, 4.4 structural rule, carve-out condition, register taint, token additions, runner hardening).

## Honest note for the reviewer

Two auditor versions have now been killed by their own red teams, both times honestly and both times for real gaps (v1: transcription gap on `env_`; v2: shape-based 4.3, token-based 4.4, name-keyed carve-out, register-carried syscall numbers). The red-team process is working as designed — it is catching what it exists to catch. The open question for Micah is not whether v3 is buildable (it is — the fixes are concrete) but whether a third round is worth it, or whether the auditor approach is hitting diminishing returns and the program should accept the residual risk statement instead. That judgment belongs to Micah at review.
