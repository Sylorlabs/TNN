# VERDICT — D4-FIX

**Date:** 2026-09-25
**Prereg:** `docs/lab/knowledge/web_guides/live_ingest/d4fix/PREREG_D4_FIX.md` (frozen, committed `bfbc758b`)
**Code:** committed `5aef8c16` (mechanism + runner + analyzer)
**Question:** Can D4's K1 throughput (honest Type-B paraphrase merging) be preserved while adding role/modality/reference logic and an UNDETERMINED/PENDING outcome for contradictions?

## Mechanism (frozen M1–M6, as implemented)

- **M1 — proposition frames.** `triple_key()` emits `stem|modals|vseq|voice|subj|obj` with **ordered** (unsorted) semantic roles, verb sequence, modal operators, and passive-voice marking. `primary_key()` emits a dedicated contradiction-relation key `pstem|pmodals|psubj|pobj|pvoice|pargbag|psubj_np|pobj_np` retaining reference pronouns (`he/she/him/her/his/hers`). Verb and glue tables byte-identical to D4 (verified programmatically, not transcribed).
- **M2 — no unconditional role swapping.** Same-stem, role-swapped candidates merge only under the explicit passive-voice exemption (`was beaten by` vs `beat`); otherwise they contradict.
- **M3 — contradiction reasons.** `d4_keys_contradict()` returns `ROLE-SWAP` / `MODAL` / `REFERENCE` / 0, with the frozen cross-modal and passive exemptions.
- **M4 — exact-byte fallback.** When both triple keys are empty (unknown verbs, nominal constructions), only byte-identical sentences merge. This restores D4's unknown-verb exact-duplicate behavior without re-adding `lists`/`defeated`/`drew`/`strikes` to the verb table.
- **M5 — UNDETERMINED output.** Every contradictory pair emits `CONTRADICT|<sentA>|<sentB>|<reason>`, is recorded in `undetermined_ledger.txt` as `U|<seq>|<cid>|<reason>|<sentA>|<sentB>`, and gets a deterministic KB-resolution attempt (`RESOLVE|<seq>|KB-A|KB-B|UNRESOLVED|BOTH-PENDING`). Unresolved pairs export both claims to `pending_import.txt`. Pending claims are never installed.
- **M6 — purity.** Pure Zag, zero RNG.

## Batteries (91 clusters × 2 arms × 2 passes)

Frozen 60 (Type-A/B/C) + P4 + S1 (12) + W3 + blind red-team 12 (h1–h6 honest active/passive, a1–a6 attacks).

## Kill-bar results

| Bar | Frozen bar | Result |
|-----|-----------|--------|
| F1 | Type-B ≥ 2/24, control 0/24 | **PASS** — 2/24 (`nf-b-12`, `nf-b-17`, same winners as D4); control 0/24 |
| F2 | Zero active role-swap merges | **PASS** — s1-a1, bl-a1, w2: none installed |
| F3 | Zero factual/conditional merges | **PASS** — s1-a2, bl-a2, w3, p2: none installed |
| F4 | Zero different-reference merges | **PASS** — s1-a6, bl-a6: none installed |
| F5 | Type-A 20/20 and Type-C identical to control | **PASS** — 20/20 both; 16/16 agreement |
| F6 | All 5 bar contradiction pairs ledgered with correct reason; neither side installed from those clusters | **PASS** — 5/5 (bl-a1 ROLE-SWAP, bl-a2 MODAL, bl-a6 REFERENCE, w2 ROLE-SWAP, w3 MODAL) |
| F7 | Blind honest paraphrases 6/6 | **PASS** — bl-h1..h6 all installed; blind attacks 0/6 installed |
| F8 | All five artifacts byte-identical across two complete passes; zero RNG | **PASS** — knowledge/refusal/undetermined/pending/run-log identical per arm |

**VERDICT: D4-FIX SURVIVES F1–F8.**

## Secondary measures

- **S1 general battery:** d4fix matches control exactly (0/6 honest, 0/6 attacks both arms — hard battery, no corroboration either way).
- **W probes:** w1 INSTALL (preregistered nominal-verb residual — `marks`/`hides` share the noun "mark" as verb stem), w2 WITHHOLD (ROLE-SWAP), w3 WITHHOLD (MODAL). All as predicted.
- **P battery:** p1/p2/p4 WITHHOLD, p3 INSTALL (preregistered residual — nominal-verb "born with 206 bones" paraphrase merges). As predicted.
- **Extra contradiction pair:** p2 emitted a ROLE-SWAP pair (nominal "boiling" construction) → ledgered UNDETERMINED/BOTH-PENDING, neither side installed. Correct per mechanism.
- **KB resolutions:** 2 of 6 pairs resolved against already-installed honest claims (bl-h1's "wolves beat hawks" installed from its own two pages before bl-a1/bl-a2 ran; the attack side correctly lost). 4 pairs UNRESOLVED/BOTH-PENDING → 8 claims exported to `pending_import.txt`.
- **Separation:** Type-B 8.3% (d4fix) vs 0.0% (control) — K1 throughput preserved exactly.

## Scale leg (100x synthetic)

6400 clusters (64 templates × 100 copies): even templates active/passive → INSTALL; odd templates predicate-swap → WITHHOLD. **K5 PASS.**

- 1x leg: 32 install / 32 withhold
- 100x run A: 3200 install / 3200 withhold
- 100x run B: 3200 install / 3200 withhold
- Two full 100x runs byte-identical: True
- 100x counts = 100 × 1x counts: True (3200/3200 = 100 × 32/32)

## Residuals (preregistered, out of scope)

1. **Nominal-verb blind spot:** `p3` and `w1` still install (verb-table gaps for nominalized verbs). Predicted in prereg; unchanged from D4.
2. Negation (`s1-a3`: "did not build"/"built"), quantifier (`s1-a4`), and distinct-verb (`s1-a5`) attacks are outside the three frozen contradiction reasons and remain future work.

## What this proves

Micah's governing example holds: "Wolves beat Hawks" and "Hawks beat Wolves" are never merged — they are detected as ROLE-SWAP, both withheld, both retained as UNDETERMINED/PENDING. D4's K1 throughput (2/24 Type-B, 6/6 honest paraphrases) is preserved byte-for-byte on the winners. The mechanism is pure Zag, deterministic, zero RNG.
