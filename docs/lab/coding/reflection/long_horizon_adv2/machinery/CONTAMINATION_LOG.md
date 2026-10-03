# CONTAMINATION_LOG.md — LH-ADV-2 clean-room critic authorship record

## Claim

`machinery/adv2_critic.zag` (the LH-ADV-2 independent critic) was authored
clean-room: derived ONLY from the frozen behavior contracts (`contracts/`,
54 files) and the capability KB (`adv_kb.txt`). The author never inspected
the emitter source, the old prototype critic body, or any simulator bodies.

## What the author SAW (allowed inputs)

1. `contracts/*.txt` — all 54 frozen behavior contracts (STAGE/DESC/WIN/
   DEPS/TEST in=/TEST out= lines). These are the ground truth the critic
   re-derives semantics from.
2. `adv_kb.txt` — the 24-entry capability KB (ID/OP/CAT/K lines only).
3. The critic INTERFACE contract (mode/args/output lines), taken from the
   trial protocol, not from any implementation:
   `adv2_critic verify <stage> <contract> <spec> <binout>` prints
   `CRITIC-ACCEPT` or `CRITIC-REJECT <reason>`.
4. The list of 24 op names (from KB IDs and contract TESTs).

## What the author did NOT see (contamination firewall)

1. `machinery/adv2_emit.zag` / the frozen `adv_emit.zag` BODY — the file was
   copied byte-wise (`cp`) into `machinery/` without being opened or read
   by the author. Its SHA-256 (`20ed86f5...`) matches the frozen emitter.
2. The old prototype `adv_critic.zag` BODY (only its interface was known).
3. `contracts/_oracle.py` (the frozen oracle used to generate TEST vectors).
4. The `sim_*` bodies in `adv_delib.zag` / `adv2_delib.zag`.
5. The deliberator's critique heuristics or candidate-scoring code.

## How op semantics were re-derived

For each of the 24 ops, the author read that op's contract TEST in=/out=
pairs and wrote an independent simulator (`kx_f_upper`, `kx_p_gt`,
`kx_agg`, `kx_sort`, `kx_join`, `kx_fmt_template`, …) reproducing the
observed input/output mapping. No emitter code was consulted; where the
author's first derivation was ambiguous, the TEST vectors (not the emitter)
were the arbiter.

## Symbol hygiene

Every internal symbol in `adv2_critic.zag` is `kx_`-prefixed. The audit
`audit_critic_indep2.py` enforces:

    defined_fns(adv2_critic) ∩ defined_fns(adv2_emit)   ⊆ {main}
    defined_fns(adv2_critic) ∩ defined_fns(adv2_delib)  ⊆ {main}

`main` (the language entry point) is the sole allowed shared symbol.

## Behavioral independence evidence

- The critic reproduces all contract TEST out= vectors by re-derivation:
  51/51 clean specs ACCEPT; the one historic buggy-output case (frozen
  A7 ledger binary_output) is correctly REJECTed as EMITTER-BUG.
- Negative probes: a wrong spec → `CRITIC-REJECT SPEC-MISMATCH test=<k>`;
  a correct spec with a mutated binary's output → `CRITIC-REJECT
  EMITTER-BUG`. The critic distinguishes spec-wrong from binary-wrong
  without ever having seen the emitter.

## Deliberation engine (NOT clean-room — and not claimed to be)

`machinery/adv2_delib.zag` is a modified copy of the frozen
`adv_delib.zag` (only the OUTPUT-MISMATCH diagnose branch was replaced
with the hardened symptom-based inference). It is the deliberation
engine under test, not an independent component; no independence is
claimed for it.

Authored: 2026-09-22. Author: the LH-ADV-2 machinery session.
