# PROSE-LEARN3 Proof

Implementation of v3 (two gated learner changes) in pure Zag plus an
independent Python oracle. Proof is by byte-identical log comparison;
no scored championship evaluations were run (per tasking).

## Artifacts

| File | SHA-256 |
|---|---|
| `src/prose_learn3` (native binary) | `a5cff7cde60074176b5a1c480ea58ed263fb22514c0a29992301e8b4ae82dc72` |
| `src/prose_learn3.zag` | `ac80c99348bebae0a45869b1744c6337cd858e081a2333da1eaa7a7c48c41d6d` |
| `src/oracle3.py` | `4985ffed54c24773123b330614f13cf0201f08ca16665024760a02f03496863e` |

Toolchain (pinned): `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

CLI: `prose_learn3 <source> [m0|m1|m2]` (default `m0`);
`oracle3.py <source> <indir> --mode m0|m1|m2` (default `m0`).

## Proof gate (a): v3 m0 vs frozen v2 binary — byte-identical

v2 binary rebuilt from `v2/src/prose_learn2.zag`
(sha256 `8dbb02fda28f32f88f10e2aa23668c308efd4b59d5369697e210b71cf8e1a901`).

| Input | v2 log | v3 m0 log | Result |
|---|---|---|---|
| championship `sol` (`proof/sol/inputs/`) | `f13ca52e…450ac0d` | `f13ca52e…450ac0d` | BYTE-IDENTICAL (`cmp` clean) |
| `synth.json` → txt (`proof/synth/inputs/`) | `f595709f…fd64cd2` | `f595709f…fd64cd2` | BYTE-IDENTICAL (`cmp` clean) |

`m0` prints the v2 header `PROSE-LEARN2 source=<s>` verbatim so the whole
log matches byte-for-byte. `m1`/`m2` print
`PROSE-LEARN3 source=<s> mode=<m>` in both implementations.

**Correction (2026-09-22):** gate (a) was under-tested. A full differential of
v3 m0 vs the frozen v2 binary over all 15 scored input classes (4 dense
championship + 4 single-exposure championship + 7 sub-batteries) finds
**14/15 byte-identical**; the single deviation is `sub_core` id 17 sent=1
(`The letter appears 5 times in the alphabet song.`). Root cause: the v3
tokenizer precomputes the coref trigger in `sctx[76]` with an **expanded**
trigger set — v2's `it/this/that` plus `its/these/those` and the
`"the word"`/`"the letter"` bigram — and that expanded set is consulted in
m0's v2-position coref block as well. v2's narrow trigger does not fire on
`The letter`; v2's 2d does not fire either (`appears` is not in its verb
list), so the v2 binary records entity=EMPTY while v3 m0 resolves `z` via
the bigram trigger. The expansion was not in PREREG3 §3 (which says "moves
the **existing** train-only coreference block"); see VERDICT.md §11. No
scored run used v3 m0 (A0/A1 ran the frozen v2 binary), so all ablation
scores are unaffected. The m1/m2 scored behavior is exactly as implemented
and oracle-verified; only the A1→A2 **attribution** is confounded (5 items
from the order change, 6 from the trigger expansion — VERDICT.md §11).

## Proof gate (b): oracle3 vs Zag — byte-identical

| Input | Mode | Zag log | Oracle log | Result |
|---|---|---|---|---|
| synth | m1 | `4df3639e…76a73e7` | `4df3639e…76a73e7` | BYTE-IDENTICAL |
| synth | m2 | `83fa64f4…6404f2d` | `83fa64f4…6404f2d` | BYTE-IDENTICAL |
| v2 sub_para (240 train / 48 test) | m1 | `e4970a25…5d721835` | `e4970a25…5d721835` | BYTE-IDENTICAL |
| v2 sub_para (240 train / 48 test) | m2 | `766d39da…3f369118` | `766d39da…3f369118` | BYTE-IDENTICAL |
| v2 sub_core (24/24, coref battery) | m1 | `c6955a1d…bbe78e14` | `c6955a1d…bbe78e14` | BYTE-IDENTICAL |
| v2 sub_core (24/24, coref battery) | m2 | `0ff73b25…2d7a8a6f` | `0ff73b25…2d7a8a6f` | BYTE-IDENTICAL |

Extra (not gated): `oracle3 --mode m0` is byte-identical to both the v2
binary and v3 m0 on synth. On sub_core, m1 ≠ m0 and m2 ≠ m1 (both changes
have observable effects on the coref battery).

Logs live under `proof/{sol,synth,subpara,subcore}/`.
Input plumbing: `proof/mk_inputs.py` (deterministic; input hashes below).

## Input hashes

- `proof/sol/inputs/train_sol.txt` `78aae5ad…90358894`
- `proof/sol/inputs/test_sol.txt` `82f39e0d…282ef890d1`
- `proof/sol/inputs/false_ids_sol.txt` `49e978a3…178e18ad34`
- `synth.json` `0a608029…5128e38cf3f61`
- `proof/synth/inputs/train_synth.txt` `740ccf42…b8372f1e`
- `proof/synth/inputs/test_synth.txt` `d56eaf07…ead996ad74`
- `sub_para_train.jsonl` `a1bdc295…a2e924f4`
- `sub_para_test.jsonl` `919a44bf…c707dfe`
- `proof/subpara/inputs/train_sub_para.txt` `21b11559…f011bc7e6`
- `proof/subpara/inputs/test_sub_para.txt` `f570ae53…21e128f6`

## Reproduction

```sh
cd ~/workspace/tnn-lab/prose-learning/v3/src && ./build.sh
# gate (a)
cd ../proof/sol && ~/workspace/tnn-lab/prose-learning/v2/src/prose_learn2 sol > v2.log
  ../../src/prose_learn3 sol m0 > v3m0.log && cmp v2.log v3m0.log
cd ../synth && ~/workspace/tnn-lab/prose-learning/v2/src/prose_learn2 synth > v2.log
  ../../src/prose_learn3 synth m0 > v3m0.log && cmp v2.log v3m0.log
# gate (b), e.g. synth m1/m2
  ../../src/prose_learn3 synth m1 > z1.log && ../../src/prose_learn3 synth m2 > z2.log
  python3 ../../src/oracle3.py synth inputs --mode m1 > o1.log
  python3 ../../src/oracle3.py synth inputs --mode m2 > o2.log
  cmp z1.log o1.log && cmp z2.log o2.log
```

## Resolved ambiguities

1. **Derived asserted rows have no install sentence.** Tier-3 key stored as
   count 0 (empty). They remain live asserted rows but can never satisfy
   tier-3 (`union>0` fails). Same in oracle (`t3keys.append([])`).
2. **Missing/invalid `argv[2]`** → deterministic `m0` (v2 behavior).
   Oracle `--mode` defaults to `m0`; unknown values fall back to `m0`.
3. **Tier-3 tie semantics** mirror the existing entity/Jaccard fallback
   exactly: argmax by cross-multiplication in `i64`, ties → lowest fact id,
   ties counted the same way.
4. **Contradicted / quarantine / denial rows** are excluded from tier-3 by
   the live-row check (`status==0`), matching the tier-2 fallback.
5. **m1/m2 INSTALL-key / probe header text** is identical between Zag and
   oracle by construction (same format strings).

## Compiler workarounds (znc, this build)

- `try_coref()` as a shared helper was removed: (i) a hoisted
  `tok_low(n5+1)` clobbered `lowb` before the `beq("the")` test; (ii) a
  `return` nested inside the trig/peid `if` miscompiled and corrupted the
  following 2d rule; (iii) any token-scan loop placed before 2d broke 2d
  when a prior item had run. Fix: the tokenizer precomputes the coref
  trigger into `sctx[76]` (offset 76 chosen clear of the `p64(sctx,64)`
  8-byte field and `sctx[72]`), and both call sites use a fire-flag with
  the `return` at the outer level. The v2 inline block's exact
  `peid!=4294967295` guard is preserved.
- No indexed `as []i32`/`as []u32`/`as []u16`; tier-3 uses byte arenas with
  `g32`/`p32`. No slice `==`, no `};`, no chained field access.

## Pending

- ~~The dense fixture proof (gate b on the forthcoming dense fixture) is
  pending until the fixture is supplied.~~ **Done 2026-09-22:** oracle3 is
  byte-identical to the Zag binary on all four dense championship sources in
  m1 and m2 (A2/A3 `champ_*_rep1.log`, 8/8 `cmp` clean), and on all four
  single-exposure championship sources in m0 (A0, 4/4 clean) plus the four
  dense sources in m0 (A1, 4/4 clean) — 16/16 championship oracle comparisons
  pass. Sub-batteries: oracle matches Zag on 26/28 (all of A2/A3 in m1/m2;
  the 2 misses are A0/A1 `sub_core` in m0, i.e. the v2 binary, differing on
  the single id-17 sentence per the gate-(a) correction above — the oracle
  implements the v3 expanded trigger, the frozen v2 binary the narrow one).
- No scored championship evaluations were run (implementation/proof only,
  per tasking).
