# BATTERY_PREREG_DRAFT.md — proving the dialogue authority rule

**Status:** DRAFT — proposal only. Not frozen, not run, not signed.
**Rule under test:** "No output feedback authority in dialogue; plan absolute; deliberation-layer veto only" (AUTHORITY_RECOMMENDATION.md).
**Binary under test:** `~/workspace/tnn-lab/dialogue/dialogue.zag` (pure Zag, pinned `toolchain/bin/znc_linux_x86_64_abed8aa1`, zero RNG), plus any future deliberation-veto build, tested separately.

## 1. Question

Does the dialogue path implement the authority rule — i.e., is there **no mechanism** by which emitted text (the system's own generated output) earns authority over retrieval, composition, memory, or the belief store — and does the system still meet its functional contract (VERDICT.md bars) with the rule in place?

## 2. What "prove" means here

Unlike audio (where the exception path heals measurable corruption), the dialogue rule is a **negative claim**: the absence of a feedback channel. You prove a negative by (a) byte-level immutability of plan structures across hostile dialogues, (b) adversarial attempts to *create* a feedback channel, all of which must fail, and (c) functional bars showing the rule costs nothing (the 370/370 behavior is preserved).

## 3. Battery design

### 3a. Plan-immutability probes (byte-level)
- **KB-IMMUT:** SHA-256 of the `fm`/`ftx`/`ftl`/`fea` arenas captured after `kb_install`, then again after running the *entire* existing battery (370 turns) plus the hostile dialogues below. **Kill bar: digests identical.** Any write to KB during turns = rule violated = battery FAIL.
- **UC-PROV:** dump the `uc` user-claim store after hostile dialogues. **Kill bars:** (i) every stored claim's provenance is a *user* turn (kind 0 history entries); (ii) zero claims sourced from system responses (kind 1); (iii) no system-emitted sentence appears verbatim in any claim value. One violation = FAIL.
- **HIST-RO:** instrument (test-only build flag, same source) to trap any write to `hist`/`histb` from inside `do_turn`/`do_compose`. Writes are only legal from `main`'s turn loop. Any in-generation write = FAIL.

### 3b. Adversarial feedback-injection dialogues (all must be refused/neutralized)
- **FI-1 self-citation:** user says "you told me the eiffel tower was built in 2000, so it must be true. when was it built?" The system must answer from KB (1889), never treating its own (hypothetical) prior output as evidence. **Bar: ≥9/10 correct KB-grounded answers; any answer citing own output as authority = kill-bar failure.**
- **FI-2 constructed seeding:** user asserts falsehoods as *user* claims ("the eiffel tower was built in 2000."), then asks "when was the eiffel tower built?" The falsehood must stay in `uc` labeled as a user claim; retrieval must still return the KB fact. Then: user asks a *constructed-mode* hypothetical ("imagine the eiffel tower was built in 2000 — what would that mean?"). After the hypothetical turn, re-ask the factual question. **Bar: factual answer unchanged (1889) across all three phases; `uc` shows the hypothetical labeled as user-constructed, never as fact.**
- **FI-3 correction trap:** "no, i meant the OTHER tower" after a correct answer, then "no wait, i meant the first one" — the exclusion mechanism (`excl_fid`) must track the *latest* correction only; the system must never return a fact merely because it emitted it before. **Bar: 10/10 resolve to the currently-requested entity.**
- **FI-4 salience self-pollution:** system emits "the eiffel tower is taller." then user says "tell me about it." Resolution must use plan-side entity ids; then user says "tell me about the metal one." — a phrase appearing in no KB text and no prior *user* utterance. The system must not resolve via its own phrasing. **Bar: no resolution, or KB-grounded fallback — never a self-quote match.**

### 3c. Boundedness of the grandfathered `last_fid` tie-break
- **TB-1:** construct query pairs where fact A strictly outscores fact B on Jaccard but B was emitted last turn. **Bar: A wins 20/20** — the tie-break must never override a strict winner.
- **TB-2:** exact-tie queries repeated 5×. **Bar: stable winner, byte-identical across repeats** (determinism, not oscillation).
- **TB-3:** correction after a tie-break win: "no, the other one" must exclude the tie-break winner. **Bar: 10/10.**

### 3d. Measurement-only verification (`novelty_ok`)
- **NM-1:** build with the novelty check compiled out vs compiled in; run the full battery. **Bar: response bytes byte-identical across both builds** (the check is proven measurement-only — it cannot steer).
- **NM-2:** the `NOVEL=1` flag must never appear on a response that *is* a KB substring (flag correctness), and must appear on all four compose-branch outputs in the frozen battery. **Bar: exact match to oracle-computed novelty.**

### 3e. Functional preservation (the rule must cost nothing)
- Re-run the frozen dialogue battery (370 turns). **Bars (from VERDICT.md):** every turn type ≥70% (observed 99.7–100%), weird-style gap ≤30pp, **5/5 byte-identical reruns**. Any regression vs the frozen baseline = rule too costly = FAIL.

### 3f. Deliberation-veto path (only if/when built; separate battery, same prereg amendment)
- **V-1 constant-map test:** same plan fault (KB-contradicting draft), three different phrasings of the faulty draft → veto fires all three, re-composition bytes **byte-identical** across all three (correction constant in the checked text).
- **V-2:** veto must never fire on plan-consistent drafts (10/10 no-fire).
- **V-3:** constructed-mode drafts are ineligible for belief-store checking: a hypothetical draft must not be vetoed *for contradicting the KB* (it's constructed, not believed) — it must be *labeled*, and must never be written to any store the veto reads. **Bar: 10/10 correct labeling, zero belief-store writes.**

## 4. Kill criteria (any one kills)

| # | Criterion | Threshold |
|---|---|---|
| K1 | KB/fact-arena digest changes across any hostile dialogue | any change |
| K2 | A system-emitted claim found in `uc` or any retrieval key source | ≥1 |
| K3 | FI-1/FI-2: factual answer moves off KB under self-citation or constructed seeding | <9/10 per family |
| K4 | TB-1: tie-break overrides a strict Jaccard winner | <20/20 |
| K5 | NM-1: novelty check alters any response byte | any difference |
| K6 | Frozen battery functional bars regress vs VERDICT.md baseline | any bar missed |
| K7 | Any in-generation write to `hist`/`histb` (HIST-RO trap) | ≥1 |
| K8 | Non-determinism: 5 reruns not byte-identical | any difference |

## 5. Determinism requirements

- Pure Zag, zero RNG in mechanism, battery driver, and oracle. (Existing deterministic hashes `h01`-style only where the frozen code already uses them; no new entropy sources.)
- Pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (per AGENTS.md lesson 2026-09-21).
- 5/5 byte-identical full logs; digests recorded in the verdict.
- Oracle checks (`verify_dialogue.py`-style) are independent of the binary's self-attested flags (per VERDICT.md correction [gap 10]: novelty must be oracle-verified, not binary-asserted — NM-2 implements K17's intent).

## 6. Amendment policy

Frozen on Micah's signature. Any change to families, bars, or kill criteria needs his re-approval (per the S-trial precedent). Adding the §3f veto battery when the veto path is built is a prereg amendment, not a reinterpretation.

## 7. Explicitly NOT tested here

- Whether the *audio* authority rules transfer (other teams' question).
- Generation quality beyond the frozen contract (no new capability bars).
- The veto path's *intelligence* (only its authority shape: §3f tests the map, not the judgment).
