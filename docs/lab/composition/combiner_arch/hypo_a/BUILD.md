# BUILD.md — H-A (combiner-architecture line, BUILDER-A)

**Hypothesis:** `hyp/hypo_a/HYPOTHESIS.md` (operator-primitive induction + miner growth)
**Workdir:** `~/workspace/composition_combiner_arch/build/hypo_a/`
**Target repo path:** `docs/lab/composition/combiner_arch/hypo_a/`
**Target branch:** `tnn-native-lab` (never `main`)
**Date:** 2026-09-28
**Builder:** BUILDER-A (subagent)

---

## 1. Source citations (exact)

| Source | Identity |
|---|---|
| Hypothesis | `~/workspace/composition_combiner_arch/hyp/hypo_a/HYPOTHESIS.md` — 27,225 bytes, SHA-256 to be recorded at commit time |
| Line brief | `~/workspace/composition_combiner_arch/LINE_BRIEF.md` |
| Frozen D1 battery | `docs/lab/composition/battery_amended/items.tsv` in checkout `~/workspace/tnn-native-lab-work/`, introducing commit `03ba8919e` |
| D1 six (exact) | `reverse, dupfirst, rotleft, droplast, upperfirst, sortchars` (from `items.tsv`; `battery_amended.zag` maps `0=REVERSE 1=DUPFIRST 2=ROTLEFT 3=DROPLAST 4=UPPERFIRST 5=SORTCHARS`) |
| Redo reference | commit `50633349939909645e9a06dc0896da0c9466a67b` |
| Toolchain (pinned) | `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` |

Checkout HEAD at build time: `e4e649ae72d25d21dde0e44ff5841e7bc9156630`
(imported pure-Zag SHA-256 validated: SHA-256(`abc`) =
`ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`).

---

## 2. What was built

**`ha.zag`** — H-A implemented in pure Zag (~1,400 lines), compiled with the
pinned toolchain to **`ha_bin`** (native, zero external tools).

Architecture (per §5.1–§5.6):
- **Position ops** (kinds 0–7): `ID, REV, ROTL, DROPLAST, DUPFIRST, SWAPENDS, SORTA, SORTD`
  (stable insertion sorts); grown positions get kinds ≥ 8.
- **Byte ops** (kinds 0–5): `BYIDENT, UPPER1, UPPER_ALL, LOWER_ALL, CAESAR(k), BYTABLE`;
  grown bytes get kinds ≥ 6.
- **Phase 1:** depth-1 then depth-2 search over `(P, B)` / `(P, B, P2)` with the
  five structured byte ops (+ grown bytes in admission order); `BYTABLE`
  excluded (§5.2: "`BYTABLE` is tried only in phase 2 (after growth)").
- **Growth (miner):** `tid` 1–8 in order; per tid, existing structured `(tid, B)`
  pairs, then `mine_byte(tid)` → BT1 (uniform shift, one consistent
  `d=(b−a) mod 26`, ≥2 distinct witness byte values) then BT2 (position-0 case
  pattern). G-novelty on canonical **behavioral** ids (BT1≡CAESAR=4,
  BT2≡UPPER1=1); gates: ≥2 pairs, ≥2 distinct input lengths. Admissions append
  64-byte provenance records (§5.1: `[0]` kind, `[1]` template/bt id,
  `[2]` out_len_fn, `[3]` param, `[4..7]` witness pair indices 0/1 as u16 LE,
  `[8]` admission seq). Cap 4/session, 32 total. Recursion ≤ 5 passes.
- **Phase 2:** depth-1 then depth-2 over `(P, BYTABLE)` / `(P, P2, BYTABLE)`.
- **Prediction:** apply program; BYTABLE withholds (`?`) on unseen input bytes;
  unknown rules (no teaches) withhold `?` (see Deviation D5).
- **Attestation:** per-rule SHA-256 over frozen order constants,
  `HZ_POSKIND`, `HZ_BYTEKIND`, all grown records, `HZ_PROG`, `HZ_NEX`,
  written to `attest.txt` beside `out.tsv`.

**Binary interface** (exact): `ha_bin teach.tsv probe.tsv out.tsv`
(`argv[4]` = optional ablation hook, test-only).
Teach: `RULEID\tINPUT\tOUTPUT`. Probe: `RULEID\tINPUT\tEXPECTED`.
Output: `RULEID\tINPUT\tPREDICTED\tEXPECTED\tMATCH\tWITHHELD`.
Withhold: `PREDICTED="?"`, `WITHHELD=1`, `MATCH=0`.
RULEIDs are arbitrary labels; the implementation groups by label but never
branches on label identity (verified by grep, §8).

**Constraint compliance:**
- Pure Zag, zero RNG: `grep -n "rand\|time("` → no hits (§8).
- No `as []i32/[]u32/[]u16` anywhere: byte arenas + explicit LE accessors
  (`ha_p16`/`ha_g16`/`ha_p32`/`ha_g32`) (ZNC-007).
- No rule-name branches in learn/apply; no per-item hardcodes. The only
  name-matching code is the K-HA-3 ablation hook (`argv[4]`), which is
  test harness, not learning.
- Callees defined before callers; `return;` in void functions; no `.*` on
  non-pointers. Two `znc` analyzer warnings (A0101) were fixed at the source
  (DUPFIRST 64-byte guard; path-copy bound); final build is warning-clean.
- Compound `A+B` RULEIDs (P2-style) are parsed as an extension; the capability
  battery does not depend on it (recorded as extension, §7 D4).

---

## 3. Capability battery results

**`battery_cap/`** — teaches: D1 six × 12 (exact pairs from frozen
`items.tsv`) + swap-first-last × 8 + sort-descending × 8 (hand-written).
Probes: 8 held-out per rule (lengths 2,2,3,3,4,4,5,5; deterministic generator
`gen_battery.py`; no probe input collides with a teach input of the same rule).
Caesar (`r9`) is **not taught** → honest withhold expected.

| Rule | Teaches | Probes | Score |
|---|---|---|---|
| r1 reverse | 12 | 8 | 8/8 |
| r2 dupfirst | 12 | 8 | 8/8 |
| r3 rotleft | 12 | 8 | 8/8 |
| r4 droplast | 12 | 8 | 8/8 |
| r5 upperfirst | 12 | 8 | 8/8 |
| r6 sortchars | 12 | 8 | 8/8 |
| r7 swap-first-last | 8 | 8 | 8/8 |
| r8 sort-descending | 8 | 8 | 8/8 |
| r9 caesar (untaught) | 0 | 8 | 8/8 withheld (`?`, WITHHELD=1, MATCH=0 per interface) |

**Total: 64/64 correct on taught rules; 8/8 honest withholds on the untaught
Caesar. Zero growth** (`grown=0` on the full battery) → **K-HA-2 holds.**

Learned programs (full seed): `(REV,BYIDENT)`, `(DUPFIRST,BYIDENT)`,
`(ROTL,BYIDENT)`, `(DROPLAST,BYIDENT)`, `(ID,UPPER1)`, `(SORTA,BYIDENT)`,
`(SWAPENDS,BYIDENT)`, `(SORTD,BYIDENT)` — all depth 1.

---

## 4. Kill-bar results

- **K-HA-2 (zero growth on capability battery): PASS.** `grown=0`; all eight
  taught rules found by phase-1 search alone.
- **K-HA-4 (Caesar by name): PASS.** `battery_kha4/` (Caesar k=5 taught, 8
  fresh probes): **8/8**, program `(ID, CAESAR, k=5)`, `grown=0`.
- **K-HA-3 (re-derivation ablation): MECHANISM EXACT, PREDICTION NOT MET —
  see Deviation D6.** Ablation removes `SWAPENDS, SORTD, CAESAR, UPPER1`
  (via `argv[4]` hook). Outcome: **3 admissions** in rule order —
  1. `UPPER1` (byte, BT2) for upperfirst,
  2. `SWAPENDS` (position, T6) for swap-first-last,
  3. `CAESAR` (byte, BT1, k=3) for caesar —
  each ≥2 pairs, ≥2 lengths, provenance recorded. Sort-descending is learned
  as the **depth-2 composite `(SORTA, BYIDENT, REV)`** by phase 1 *before*
  the miner runs, so `SORTD` is never re-derived. **Probe outcomes are
  byte-identical** between full-seed and ablated runs (`diff` clean, 72/72).
  The trace's "exactly 4 admissions / byte-identical programs" prediction is
  inconsistent with the frozen search order (§5.2: "phase 1 {depth 1, then 2}
  → growth"); the implementation follows the mechanism, not the prediction.

---

## 5. Determinism evidence

`battery_cap`: **3 normal runs + 1 `MALLOC_PERTURB_=165` run.**

| Artifact | Runs | SHA-256 |
|---|---|---|
| `out.tsv` | 4/4 identical | `72d8c6366a6f0de8d7445c36ce041fcadb9238ac4a8763ab8c033dcebcd4e5c` |
| `attest.txt` | 4/4 identical | `43b57c31e5fef46406fdb58f56dd646aafecd4ce1fabe4f3b6a2607a8b3ffb87` |

Byte-identical across all reruns including allocator perturbation.
No hash maps (linear scans in frozen order), stable sorts only, all arenas
zeroed at init, no uninitialized reads.

---

## 6. Build provenance

| Item | SHA-256 |
|---|---|
| Toolchain `znc_linux_x86_64_abed8aa1` | `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` |
| `ha.zag` (final) | `bac078cf583680f4148017808775cc3b39f16ef2aae61db34e36e513f189ad08` |
| `ha_bin` | `abb948157a985cd480f870203af36f829820b3aa1e4e085846fd6374135201c9` |

Build: `znc_linux_x86_64_abed8aa1 ha.zag -o ha_bin` — zero analyzer
warnings on the final source. **The binary is NOT committed** (per task).

---

## 7. Deviations and spec conflicts (do not invent — record)

- **D1. Truncated hypothesis.** The local `HYPOTHESIS.md` is 27,225 bytes and
  ends literally with `### 5.8... Cal\n...[truncated 1238 chars]`. §5.8
  (znc-compliance notes) is missing. Nothing was invented to fill it; the
  toolchain-hazard rules from the lab log (callees-before-callers, no
  `as []i32`, `return;`, no `.*` on non-pointers, 2^25 slice limit) were
  followed as standing lab law instead.
- **D2. Caesar conflict (task vs hypothesis).** The task's battery demands
  "Caesar-shift → honest withhold on novel input," but H-A seeds `CAESAR(k)`
  and K-HA-4 kills H-A on any Caesar withhold/error when examples determine
  k. Resolution implemented: Caesar **taught** → learned and predicted
  (K-HA-4: 8/8); Caesar **untaught** (novel rule) → honest `?` withhold.
  Both bars are satisfied simultaneously; the apparent conflict was
  taught-vs-untaught.
- **D3. Arena layout.** §5.1 says arenas are global `[]u8`; the implementation
  allocates each arena once in `main` and passes them explicitly (toolchain-
  safe pattern; identical semantics). Noted, not hidden.
- **D4. Compound RULEIDs.** The shared TSV interface does not define P2
  compound `A+B` RULEID encoding; the implementation parses it as an
  extension. The capability battery does not depend on it.
- **D5. Unknown-rule withhold vs P3 echo.** §5.6's P3 ("emit input unchanged")
  is overridden by the task's binary interface: a rule with no teaches (or a
  failed induce) emits `?` with `WITHHELD=1`, `MATCH=0`. The task's interface
  is explicit and higher-authority for the wire format.
- **D6. K-HA-3 prediction vs frozen search order.** The K-HA-3 trace predicts
  "exactly 4 admissions (UPPER1, SWAPENDS, SORTD, CAESAR), final programs
  byte-identical to the full-seed run." The frozen mechanism (§5.2: "phase 1
  {depth 1, then 2} → growth"; §5.5 `induce()` pseudocode) finds the depth-2
  composite `(SORTA, BYIDENT, REV)` for sort-descending in phase 1, before
  growth runs — so the miner never re-derives `SORTD`. Actual: 3 admissions,
  probe outcomes byte-identical (72/72). The prediction contradicts the
  mechanism; the implementation follows the mechanism exactly (zero design
  freedom). **Flag for parent: K-HA-3 as literally written ("must re-derive
  all four") is failed by the spec's own search order, not by an
  implementation bug.**
- **D7. K-HA-3 "byte-identical programs".** Re-derived primitives necessarily
  get grown kinds (≥8/≥6), so program bytes differ from the full-seed run by
  construction; what is byte-identical is the *probe outcomes* (verified by
  `diff`). The kill bar's "byte-identical programs" cannot literally hold
  under the spec's own grown-kind encoding.
- **D8. DUPFIRST length guard.** `DUPFIRST` on a 64-byte input would produce
  65 bytes, exceeding `HA_MAX_LEN=64` and the 64-byte scratch rows. The spec
  is silent; the implementation rejects the candidate (`-1`) rather than
  overflowing. Never triggers on the battery (max length 5).
- **D9. G-novelty canonical ids.** "G-novelty: not behaviorally identical to
  an existing primitive (canonical template ids make this an equality
  check)." Implemented as: grown BT1 ≡ CAESAR (kind 4), grown BT2 ≡ UPPER1
  (kind 1). Without this, seed `UPPER_ALL` (kind 2) would spuriously shadow a
  re-derived BT2 (template id 2) — caught during the ablation test.

---

## 8. Grep evidence

```
$ grep -n "rand\|time(" ha.zag | grep -v "^\s*//"     → (no hits)
$ grep -n "as \[\]i32\|as \[\]u32\|as \[\]u16" ha.zag → (no hits; one comment cites ZNC-007)
$ grep -n -i "reverse\|dupfirst\|rotleft\|droplast\|upperfirst\|sortchars" ha.zag | grep -v "^\s*//"
    → hits only in: the attestation frozen-constants string (line 904),
      the argv[4] ablation hook (lines 950–958), and comments.
```

No rule-name branches in learn/apply; no per-item hardcodes. RULEIDs
(`r1`..`r9`) are arbitrary labels used only for grouping.

---

## 9. Deliverables in this workdir

- `ha.zag` — implementation (final SHA above)
- `R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag` — imported support
  (must accompany the source at commit)
- `gen_battery.py`, `gen_kha4.py` — deterministic battery generators
- `battery_cap/{teach,probe}.tsv`, `battery_abl/{teach,probe}.tsv`,
  `battery_kha4/{teach,probe}.tsv`
- `run_cap1/`, `run_cap2/`, `run_cap3/`, `run_cap_pert/` — 4 determinism runs
  (`out.tsv` + `attest.txt` each)
- `run_abl_full/`, `run_abl_abl/` — K-HA-3 full vs ablated runs
- `run_kha4/` — K-HA-4 run
- `BUILD.md` (this file)

**Not for commit:** `ha_bin`, `smoke_bin`, `smoke2_bin` (build binaries stay
local per repo content standard).

---

## 10. Open items for the parent

1. **K-HA-3 verdict** (D6): the implementation is mechanism-exact, but the
   trace's 4-admission prediction does not materialize. Recommend recording
   the trace prediction as a spec bug, not an H-A failure — or rule otherwise.
2. Commit `ha.zag` + support files + `BUILD.md` + evidence TSVs/outputs to
   `tnn-native-lab` at `docs/lab/composition/combiner_arch/hypo_a/` (fetch +
   rebase onto current origin head first; concurrent crews are active).
   Do not commit any binary.
