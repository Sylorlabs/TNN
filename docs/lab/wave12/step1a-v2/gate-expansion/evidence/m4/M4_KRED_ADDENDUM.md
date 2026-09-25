# M4 K-RED addendum — KILLED

**Date:** 2026-09-25. **Round:** blind red team, 12 novel plants, frozen
2026-09-25 in `redteam/` (`MANIFEST.md`, SHAs byte-verified).

**Procedure note:** the red team probed the SHA-verified frozen checker
binary (`m4_subset`, `62b9728a…c45be73`) black-box. The coordinator
independently re-ran all 12 frozen plants through the frozen checker +
frozen `config/` (deterministic — K-DET 3/3, no information lost vs a
method-crew re-run). Table below is the coordinator's independent run.

## K-RED results: 12/12 CERTIFY on valid dirty plants — MISS RATE 1.0

| Plant | Cat | Targets | Verdict | Mechanism |
|---|---|---|---|---|
| rt_a1_clock | (a) | D6 | CERTIFY — MISS | `_zag_clock_monotonic_ms`: banned word embedded mid-identifier; word-boundary match never fires |
| rt_a2_exec | (a) | rule gap | CERTIFY — MISS | `_zag_exec_capture("date +%s%N")`: process execution covered by NO rule |
| rt_a3_freelist | (a) | D3,D7 | CERTIFY — MISS | `_zag_malloc`/`_zag_free` unlisted by D3; freed-chunk bytes read, no tainted cast |
| rt_b1_malloc_seed | (b) | D7 | CERTIFY — MISS | `_zag_malloc` return not in taint-seed set → `p as i64` unflagged |
| rt_b2_fnret | (b) | D7 | CERTIFY — MISS | taint doesn't cross function boundary |
| rt_b3_array | (b) | D7 | CERTIFY — MISS | taint laundered through `arr[0]` store/load |
| rt_c1_readfile | (c) | D5 | CERTIFY — MISS | `_zag_read_file` not in D5's hooked set; reads `/proc/sys/kernel/random/uuid` |
| rt_c2_d5alias | (c) | D5 | CERTIFY — MISS | alias defeats syntactic hook match (controlled pair: direct call → REFUSE, alias → CERTIFY) |
| rt_c3_mkdir | (c) | D5 | CERTIFY — MISS | `nio_mkdir` omitted from D5's hook list |
| rt_d1_newline_as | (d) | D7 | CERTIFY — MISS | cast detector is line-oriented; newline before `as` defeats it (controlled pair verified) |
| rt_d2_hashorder | (d) | D4 | CERTIFY — MISS | genuine chained hash table under innocent names; UUID-seeded bucket order varies |
| rt_d3_argc | (d) | D2 | CERTIFY — MISS | `_zag_argc` not covered by D2's `_zag_arg` logic |

## Verdict: K-RED FIRED — M4 version M4-2026-09-25-v1 is DEAD

Miss rate 12/12 > 0. Per the frozen kill bar, the version is killed. No
mid-round repair, no v-next under this prereg.

## What the kill means (and doesn't)

- Killed is the **implementation**, not the idea. Every kill is a
  syntactic-enforcement gap: unlisted primitives (`_zag_malloc`,
  `_zag_exec_capture`, `_zag_read_file`, `_zag_argc`, `nio_mkdir`),
  word-boundary matching vs mid-identifier embedding, line-oriented
  detection, syntactic (non-resolving) hook matching, taint that doesn't
  cross function boundaries or survive store/load laundering.
- This is the same empirical signature that killed v1–v3: the language
  surface is larger than any token/rule list. A refusing compiler with
  SYNTACTIC rules inherits the inexhaustible-idiom problem; only a
  SEMANTIC (type/effect-level) enforcement could escape it — that is a
  new hypothesis, not a repair of this version.
- M4's fixed-battery results (12/12 catch, 5/5 clean) stand as evidence
  of what syntactic refusal CAN do; the red round shows what it can't.
