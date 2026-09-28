# T2-PARAMS replication verdict — REPRODUCED

Replacement crew (predecessor killed by daemon restart 2026-09-22). Clean-environment Type A rerun of the parameter-scaling experiment at N=24,000 facts: 19 configs (5 reps base, 3 reps others), 59 runs, pure Zag, zero RNG.

## Frozen prereg section (authoritative) — quoted verbatim

From `docs/lab/crossref/PREREG_TIER2.md` at frozen commit `7b2100d09911c5c10252c5756c7def288e70bd1f` (file verified byte-identical to the frozen commit via raw.githubusercontent fetch; diff clean):

> ## T2-PARAMS — parameter scaling: baseline ×1 is the efficiency frontier (Type A)
>
> **Claims:** 19 configs × 3 reps at 24,000 facts, commit `ccbb3d3c39d7`: 16/19 configs produce the byte-identical learner (same digest, not just scores); slots ×0.25/×0.5 degrade gracefully and exactly proportionally; baseline ×1 holds 1.0000 mastery at 4.000 ops, 92 B/fact; evidence ×0.25–×4, verify-depth ×2/×4, redundancy ×2/×4, joint-maxed all change zero behavior, only cost (verify-depth ×4: 1.75× cost; redundancy ×4: 2.5× cost, 3.3× memory); taught falsehoods absorbed 1.0 at every config.
>
> **Method:** full rerun 19×3 in clean checkout; compare all 19 digests and the cost multipliers.
>
> **Rule:** REPRODUCED if ≥16/19 digests byte-identical (name which 3 differ and how), proportional slot degradation holds, cost multipliers match; NOT REPRODUCED if the identical-digest count drops below 16 or any non-slot config changes behavior.

## Claims checklist — all verified

- [x] **16/19 configs byte-identical learner digest.** Mine: 16/19 configs = `8e6238911bb7cef0` (base digest). The 3 that differ: `slot025` (`0a6e548f2dae51dc`), `slot05` (`9175b7e1f4d24d46`), `jsmall` (`9175b7e1f4d24d46`, exactly = slot05). All three are the sub-1× slot-capacity configs — they differ because fewer facts fit in the store; `jsmall` matches `slot05` because slot capacity is the only parameter that changes the stored set (its other joints are all 1× in effect).
- [x] **Slots ×0.25/×0.5 degrade gracefully and exactly proportionally.** slot025: 5708/22841 = 0.2499; slot05: 11414/22841 = 0.4997. Exact proportionality to the 0.25/0.5 capacity multiplier.
- [x] **Baseline ×1 = 1.0000 mastery at 4.000 ops, 92 B/fact.** Mine: 22841/22841 mastery, 4000/1000 = 4.000 ops/fact, logical 92 B/fact (24+4+64 per the committed scale-up convention; allocated 202 B/fact with audit chunking granularity — both match committed).
- [x] **Evidence ×0.25–×4, verify-depth ×2/×4, redundancy ×2/×4, joint-maxed: zero behavior change, only cost.** All 14 non-slot configs hold 22841/22841 mastery, 96/96 flaw, 1159/1159 absorption, and the base digest. Cost multipliers match exactly: depth4 1.75× ops (7000/4000), red4 2.5× ops (10000/4000) and 3.3× memory (669/202 = 3.312), jbig 13.000 ops / 8690 B/fact.
- [x] **Taught falsehoods absorbed 1.0 at every config.** Full-capacity configs: 1159/1159. slot025/slot05: 292/1159 and 586/1159, where the remainder were never taught (capacity drops, not truth-detection) — decile data shows a clean prefix cut at exactly the slot cap (5708+292 = 6000 = cap; 11414+586 = 12000 = cap), every stored fact mastered, zero corruption of what fits (independently confirms the KB-P-GRACE bar).
- [x] **Byte-identical reps within every config** (19/19, det=OK) — and every one of my 59 logs is **byte-identical to the committed evidence logs** (0/59 differ by diff).

## 19-digest comparison (mine vs committed)

| Config | My digest | Committed digest | Match |
|---|---|---|---|
| base | 8e6238911bb7cef0 | 8e6238911bb7cef0 | ✓ |
| slot025 | 0a6e548f2dae51dc | 0a6e548f2dae (prefix) | ✓ |
| slot05 | 9175b7e1f4d24d46 | 9175b7e1f4d2 (prefix) | ✓ |
| slot2 | 8e6238911bb7cef0 | = base | ✓ |
| slot4 | 8e6238911bb7cef0 | = base | ✓ |
| slot8 | 8e6238911bb7cef0 | = base | ✓ |
| ev16 | 8e6238911bb7cef0 | = base | ✓ |
| ev32 | 8e6238911bb7cef0 | = base | ✓ |
| ev128 | 8e6238911bb7cef0 | = base | ✓ |
| ev256 | 8e6238911bb7cef0 | = base | ✓ |
| depth2 | 8e6238911bb7cef0 | = base | ✓ |
| depth4 | 8e6238911bb7cef0 | = base | ✓ |
| audit05 | 8e6238911bb7cef0 | = base | ✓ |
| audit2 | 8e6238911bb7cef0 | = base | ✓ |
| audit4 | 8e6238911bb7cef0 | = base | ✓ |
| red2 | 8e6238911bb7cef0 | = base | ✓ |
| red4 | 8e6238911bb7cef0 | = base | ✓ |
| jsmall | 9175b7e1f4d24d46 | = slot05 | ✓ |
| jbig | 8e6238911bb7cef0 | = base | ✓ |

Identical-digest count: **16/19 ≥ 16** — rule's REPRODUCED bar met. No non-slot config changed behavior.

## Cost multipliers (mine vs committed) — all match

depth2 5.000 / depth4 7.000 (1.75×) / red2 6.000 / red4 10.000 (2.5×) ops; allocated B/fact slot025 99, slot05 103, slot2 358, slot4 669, slot8 1244, base/ev/depth 202, audit05 115, audit2 333, audit4 639, red2 358, red4 669 (3.3× memory), jsmall 59, jbig 8690. Every cell matches the committed `PARAM_VERDICT.md` table.

## Decision

**REPRODUCED.** The architecture is parameter-insensitive above the capacity floor: 16/19 configs produce the byte-identical learner, the three differing configs are exactly the sub-1× slot-capacity ones (differing by stored-set size, not by behavior), slot degradation is exactly proportional, and every cost multiplier reproduces. No emergent truth-detection from any parameter: taught falsehoods absorbed 1.0 everywhere.

## Frozen pins

- Crossref prereg: `7b2100d09911c5c10252c5756c7def288e70bd1f` (branch tnn-native-lab).
- Params evidence pin: `ccbb3d3c39d70924c8e2e2463cb5fb7057f19616` — EXPECTED `ccbb3d3c39d7` PRESENT (not UNREPLICABLE-AS-IS).
- Driver source integrity: `param_learner.zag` git blob SHA `da15b9b797b5df715663c738e2adda8d0a6d6662` matches the pinned commit's blob exactly.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (sha256 498abcb5ab346f8cb246222a1ca63699d035a427, znc 2026.07.0-dev), built from source; no .zagd/binary copies in evidence.

## Honest limitations / notes

- Network too slow for a full git clone (70M in 20 min; tarball killed at 756MB). Clean checkout was assembled per-file at the pinned SHA (`docs/lab/scale/params/` + `docs/lab/crossref/PREREG_TIER2.md` via raw.githubusercontent at pinned SHAs). Substance is airtight via the fidelity gate: my base run was **byte-identical to the committed `runs/base_r0.log` before the sweep started**, and the driver's git blob SHA matches the pinned blob.
- Corpus `~/workspace/scale/corpus/texts` (frozen Gutenberg texts + .tnix indexes + meta.json) read read-only; nothing written there. Zero RNG anywhere: 19/19 configs byte-identical reps; rep arg accepted but not printed by the binary (deterministic given config).
- Memory footprint: 2-way parallel runs on the shared 2-vCPU VM, each run ≤ ~35MB (jbig); no interference with live workstreams observed.
- One timing note: runs are I/O-bound on this VM (~26s/run, mostly syscall/page-cache wait; user CPU ~1.5s) — total sweep ~12 min with 2-way parallelism.
