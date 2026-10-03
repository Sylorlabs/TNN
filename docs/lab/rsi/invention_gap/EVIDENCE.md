# Mechanical evidence for the invention-gap diagnosis

All checks run 2026-09-22 against the frozen T1N rerun sources on
`sylorlabs/TNN`, branch `tnn-native-lab`
(`docs/lab/coding/reflection/t1_native/`). Pure read-only analysis; no
executable built.

## E1. Composer parameters are dead (d_emit_module)

`fn d_emit_module(t1k, t1t, t2s, t2v, t4k, goal)` — the six parameters carry the
bake episode number and citation strings from the deliberation.

- Uses of `t1k` in body: 0
- Uses of `t1t` in body: 0
- Uses of `t2s` in body: 0
- Uses of `t2v` in body: 0
- Uses of `t4k` in body: 0
- Uses of `goal` in body: 0 (one match inside the comment string
  "goal body: text after the leading tier/field markers" — not a parameter use)

The body is ~450 lines of `d_cmo("...")` string literals. **Zero bits of
deliberation flow into the emitted module.**

## E2. Phantom citations are template literals, not TNN decisions

The strings `EP0100`, `EP0101`, `EP0102` appear as literals inside the
`d_cmo(...)` chunks. The frozen traces end at EP0099 (informed) / EP0058
(scratch). The engine comment above the call reads "(EP numbers for the three
functions: use the bake episode and following)" — the intent was live episode
numbers; the implementation is hardcoded text. No mechanism exists that derives
a citation ID from the episode sequence.

## E3. Weights/keywords/emitters are template literals, never deliberated

Literal in the template: `s_rev+10` ("revers"), `s_sum+10` ("sum"),
`s_max+10` ("largest"), `s_fact+10` ("factorial"), `+5` for "argument"/"loop",
`mg_fact` (no taught counterpart), `mg_smart_sum` (parses integers from spec
text). The trace deliberates "use argmax" (EP0024, EP0075) — the *structure* is
faithful; every *weight and keyword* is stencil content with no episode behind it.

## E4. Accepted mechanisms do not reach the artifact

Critic ACCEPTs (trace): E-STRREV, E-ARRAYSUM, E-SORT, E-HASH.
Module emitters (template): literal, count, reverse, smart-sum, max, factorial.
E-SORT and E-HASH have no emitter; `mg_fact` has no taught counterpart.
The emitted module is not a function of the accepted set.

## E5. Novel synthesis: 13 proposals, 100% compile failure

Trace `SYNTHESIZE:` proposals: EP0010–EP0022 (13; C-ARCH-02..06 × ranked bases).
Critic outcomes: every novel candidate `REJECT ... compile rc=1`, with
"revise produced no candidate" (operator returned no steps / no ranked base) or
"revision budget exhausted" (3 re-runs of the same substitution operator).
The revision loop (m_critique) re-invokes `d_synthesize` at deeper round — same
operator, no failure localization.

## E6. Arm gap is exactly zero

`runs2/informed/t1n_arch.zag` vs `runs2/scratch/t1n_arch.zag`: byte-identical
(sha `c4811c28...` per REVIEW_COORDINATOR.md). Canonical battery logs:
byte-identical across arms. The 12-record corpus changed no candidate, no
accept, no module byte.

## E7. The critic judges knowledge correctly (the judge works)

Trace REJECTs on compile evidence: E-STRCOUNT, E-ARRAYMAP (rc=1), E-FILEWRITE /
E-FILEREAD (`_zag_raw_syscall` arity — the taught KB shipped uncompilable
entries and the critic refused them). The knowledge-judging path is functional;
the knowledge-consuming path (E1–E5) is not.

## E8. Corpus/KB contents not in the committed tree

`teach_audit.txt` records fingerprints only
(entries `f7de7f46...`, corpus `3ff512a3...`, 69 entries / 12 records).
No `corpus.*` / `entries.*` blob exists under `docs/lab/coding/reflection/t1_native/`
in the branch tree (55 blobs enumerated, none matching). The diagnosis therefore
characterizes the knowledge from the trace's proposal/citation records, not from
the corpus text — see DIAGNOSIS.md §3 caveat.
