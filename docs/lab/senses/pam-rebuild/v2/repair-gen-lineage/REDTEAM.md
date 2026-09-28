# RED TEAM REPORT — GEN-LINEAGE repair (PAMs v2 repair line)

Red-team subagent, 2026-09-27 ~02:00 PDT. Target: the GEN-LINEAGE repair in
`~/workspace/pamsv2_repair/fix/` (WHITEBOX.md + REPAIR.md read first; the
implementer's harness was NOT used as the attack surface — all probes below
are my own, written in pure Zag against the core sources directly).

Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
(re-verified before use). Pure Zag, zero RNG, every binary run 2× with
byte-identical stdout (SHA-256 per leg below).

## Verdicts

| Direction | Result |
|---|---|
| **1 — smuggle a falsehood past the repaired gate** | **REPAIR HOLDS** — 97/97 checks pass. No epoch-forcing, no laundering, no premium-shedding, no cross-generation inheritance found. |
| **2 — truth still refused by the repaired gate** | **REPAIR HOLDS** — 108/108 checks pass. No legitimate truth refused: 3-generation reuse, overwrite-founded truths, no-op-WEAKEN edges, exactly-P boundaries all accept at their own-lineage price. |
| **Port to the canonical integrated core** | **HOLDS — repair is shippable.** Patch applies 1:1; patched functions byte-identical at identical lines; 70/70 key probes pass on the ported core; the canonical-only immediate-121 is intact. |

I could not break it. What follows is the evidence.

## Files (this directory)

- `red1.zag` — Direction-1 attack harness (97 checks), imports `red_core.zag`
- `red2.zag` — Direction-2 probe harness (108 checks), imports `red_core.zag`
- `red3.zag` — port-verification harness (70 checks), imports `port_core.zag`
- `red_core.zag` — patched fix core, SHA-256
  `98bba0dbc950aea51140a2042983d035b05c733a5588bcd298fcad27a9379e78`
  (verified byte-identical to `fix/strength_core.zag`)
- `port_core.zag` — canonical integrated core
  (`docs/lab/strength-pricing-meter-adoption/src/strength_core.zag`,
  pristine SHA-256 `d156278fab455d21d7a78f6493f0976dad071aecf081b73aa048ffc41f308dfa`)
  with `fix/strength_core_genlineage.patch` applied; patched SHA-256
  `003d622c782b3516a60007477cfcb41d5e41439217ac3d9db68cbc10cfe1f56b`
- `red1_run1.txt`, `red1_run2.txt`, `red2_run1.txt`, `red2_run2.txt`,
  `red3_run1.txt`, `red3_run2.txt` — run logs (byte-identical pairs)
- Build: `cd` here (or any dir holding the core + `substrate/`);
  `znc build redN.zag`. (`substrate/` = copy of `fix/substrate/`, not
  duplicated here; the implementer's copy is authoritative.)

## Run evidence

| leg | target | checks | SHA-256 of stdout (run1 = run2) |
|---|---|---|---|
| red1 | patched fix core | 97/97 PASS, `RED1_DONE fails=0` | `4be4b68ee17e2685fa3104fae7f305a83c31d388cefc4a82ade1278a68ccd3d2` |
| red2 | patched fix core | 108/108 PASS, `RED2_DONE fails=0` | `321ddbe235aa405afe14c8fa2f0703918085fb565dd71cc95231e43f80e46504` |
| red3 | patched canonical core | 70/70 PASS, `RED3_DONE fails=0` | `612b2e03d8ccfeaf78483cb84adfd490278674fe0154114ad943aa36e722c042` |

(Disk was at 100% for most of this run; builds ran in `/tmp/pamsv2_red`,
binaries deleted after logging. ~910M of cold pip/huggingface caches were
cleared to make the deliverable writable; nothing else was touched.)

---

## DIRECTION 1 — attacks, probes, results (all in `red1.zag`)

**A1 — force an epoch advance on a live slot.** Filled all 16 slots, then
(a) `st_add` onto the live slot → `ST_REFUSED_FULL` (104), no slot assigned;
(b) failed `st_overwrite` (no cites) → 109. Verified via ledger scan that
zero OK ADD/OVERWRITE records landed for the slot and `st_delib_epoch_start`
is unmoved by either attempt; the judgment still deliberates at its honest
price 1. Companion: with a free slot, `st_add` lands on the FREE slot, the
victim's epoch unmoved. — *The epoch cannot be forced: the only OK
ADD/OVERWRITE writers are `st_add` (dead slots only) and `st_overwrite`
(full priced gate).* HOLD.

**A2 — plant weak, then grow.** Falsehood planted at strength 10 prices 0;
after STRENGTHENs to 50→90 it deliberates at **1 with r1=HELD_STRONG** —
the founding peak, not the weak start. No discount from a weak birth. HOLD.

**A2b — weak-then-overwrite laundering.** Weak falsehood (price 0) overwritten
by a strength-90 falsehood (pays 0, honest): the new generation deliberates
at **2** (r1=HELD_STRONG own peak, r4=REVISED founding overwrite) — MORE
than installing the strong falsehood directly (price 1). *Laundering through
a weak judgment raises the later destruction price; it never lowers it.*
HOLD.

**A2c — sunk premium paid at crossing, never shed.** Judgment with 3 sunk
cites + strengthen → price 3; the overwrite pays all 3 (fresh cites) and
the new generation deliberates at 2 with no sunk carry. HOLD.

**A3 — overwrite chain, three generations.** 80 →(paid 1)→ 60 →(paid 1)→ 90.
Each generation's deliberate shows only its own lineage (r1 = MID 22 for
the 60, STRONG 21 for the 90; r3 = UNFOUGHT; r2 = NONE). No hw/fought/sunk
leaks across generations. HOLD.

**A4 — sunk-cite premium cannot be shed (sharpest attack).** TRUE(80) + 3
sunk cites + strengthen → price 3.
- Under-fund by one (2 fresh cites) → **109**, TRUE survives.
- Deliberate-then-WEAKEN (bind 3, mutate, overwrite) → **122 fail-closed**
  (the deliberate falls outside `(lss, upto)`), TRUE survives — and the
  mutation *raised* the honest price 3→4 (sunk 5, fought 1). *Mutation is
  anti-laundering: it can only raise the price.*
- Full payment of 4 → installs. Tombstone check: re-citing a consumed ep is
  accepted at cite time on this core but the gate refuses **121** with the
  cite-lock machinery; two genuinely fresh cites break the wedge (R6
  property intact post-repair). HOLD.

**A5 — control.** Exact-price payment displaces even a TRUE memory (the gate
is economic, not directional); 0 cites → 109. Confirms the kill bar's
premise: only *below-honest-price* displacement would void, and none was found.

*Direction-1 kill bar (falsehood displacing a TRUE protected memory below
its honest current-generation price): never triggered. REPAIR HOLDS.*

---

## DIRECTION 2 — probes, results (all in `red2.zag`)

**B1 — truth after TWO kills on the same slot.** 80 →(paid kill)→ 70
→(paid kill)→ truth(30): deliberates **0** with reasons 22/26/28/30 —
own lineage only (r1=MID for 30, not the corpses' STRONG). The S11B shape
(consumed re-cite before deliberate) installs clean: overwrite → ST_OK,
no cite-lock. A STRONG truth(80) on the thrice-reused slot deliberates
**1** (own peak only) and installs at exactly 1 cite. HOLD.

**B1d — deliberate(0)-then-cite → 122.** When a deliberate has already bound
price 0, any cite is refused 122 at cite time (adopted exact-count law: the
price is already exactly met, so any cite is over-funding — same law as the
implementer's R3 at price 1). **This is not a truth refusal**: the overwrite
still succeeds with 0 cites + JUSTIFY → ST_OK. Documented, not a kill.

**B2 — overwrite-founded truth on a reused slot.** Weak falsehood → truth(60)
installed by overwrite at price 0 → deliberates **1** with r4=REVISED (the
founding-overwrite check sees the real `st_overwrite` record) → installs at
exactly 1 cite. The founding-event-only r4 works through the real path. HOLD.

**B3 — no-op WEAKEN.** Truth(60) + WEAKEN(60→60) → price 1 (the +1 fought is
real, adopted meter policy — Q2's perversity, unchanged by this repair);
installs at exactly 1 cite. Truth(20) + no-op WEAKEN → price **0** (floor
absorbs the +1); installs with 0 cites. *The +1 raises an honest price; it
never refuses a truth.* HOLD.

**B4 — exactly-P on a repair-changed price.** ADD-founded 80 on a reused slot
deliberates **1** post-repair (was 2 pre-repair — the intended corpse-shed):
0 cites → 109; exactly 1 cite → ST_OK; 2nd cite → 122 at cite time. The
boundary is exact in both directions. HOLD.

**B5 — epoch<0 reachability.** Rolling back the founding ADD kills the slot
(`live=0`); re-adding founds a fresh epoch. No public op produces a live
slot without an OK ADD/OVERWRITE, so the new `epoch<0` fail-closed guards in
`st_meter_hw`/`st_meter_revs` are unreachable dead code (the call site
`st_meter_compute_at` already guards first; it is the only caller of both).
Harmless defense-in-depth, not a refusal path. HOLD.

**B6 — fought leakage.** WEAKEN in generation 1, kill, new truth(30):
r3=UNFOUGHT, r1=MID(30) — zero leakage of fought or high-water. (fought was
already generation-scoped; confirmed it stays that way.) HOLD.

*Direction-2 kill bar (a truth the repaired logic should accept but the gate
refuses): never triggered. REPAIR INCOMPLETE — not found; REPAIR HOLDS.*

Two probe-design corrections made during the run (my hand-computed
expectations, not mechanism findings): strength 30 is HELD_MID (22), not
HELD_WEAK (23) — the WEAK band is ≤25; and gate precedence fires 122 (no
bound deliberate) before the 109 cite-count check, so the A1 probe binds a
deliberate first.

---

## PORT VERIFICATION (all in `red3.zag`)

1. Extracted the canonical core from the read-only worktree
   `~/workspace/pamsv2_wt` (detached at `d758a876c`); SHA-256 =
   `d156278fab455d21d7a78f6493f0976dad071aecf081b73aa048ffc41f308dfa` —
   matches the implementer's claim.
2. Diffed it against the pinned gov base: exactly 8 lines differ, all in
   `st_evidence` (the GOV-C immediate-121-at-cite-time, commit `45f655a5a`).
   The two meter functions are byte-identical at lines 904/958 with the
   identical full-ledger scans — the implementer's "1:1 at identical lines"
   claim is accurate.
3. Applied `fix/strength_core_genlineage.patch` to the canonical copy: all 3
   hunks applied cleanly. Patched port SHA-256
   `003d622c782b3516a60007477cfcb41d5e41439217ac3d9db68cbc10cfe1f56b`;
   it differs from the patched fix core in exactly the 8 pre-existing
   immediate-121 lines. The patched `st_meter_hw` (898–940), `st_meter_revs`
   (965–985), and the call site (line 1002) are **byte-identical** between
   port and fix core.
4. Re-ran the key probes on the ported core (70 checks): S11B neuter
   (price 0, reasons 23/26/28/30, installs, no citelock), overwrite chain,
   two-kills-then-truth, sunk-premium enforcement, overwrite-founded truth,
   and K6 — the canonical-only immediate-121 (re-cite of a consumed ep →
   121 at cite time) is intact after the patch. **70/70 PASS.**

*The port holds: the repair is shippable to the canonical core. The only
behavioral delta between the two patched cores is the pre-existing,
adopted immediate-121.*

---

## Coverage table

| # | Attack / probe | Target | Result |
|---|---|---|---|
| A1 | force epoch advance (full slots; failed overwrite) | fix core | HOLD — 104/109, epoch unmoved |
| A1b | ADD lands on free slot, never live victim | fix core | HOLD |
| A2 | weak plant → grow to 90 | fix core | HOLD — prices founding peak (1) |
| A2b | weak→overwrite(90) laundering | fix core | HOLD — costs MORE (2 > 1) |
| A2c | sunk premium paid at crossing | fix core | HOLD — 3 paid, no carry |
| A3 | 3-generation overwrite chain | fix core | HOLD — own-lineage only |
| A4 | sunk-premium shed (under-fund / mutate / full-pay) | fix core | HOLD — 109 / 122+price 3→4 / paid |
| A4 | tombstone at gate + fresh-episode break | fix core | HOLD — 121, then ST_OK |
| A5 | exact-price displacement control | fix core | HOLD |
| B1 | truth after 2 kills (weak + strong) | fix core | HOLD — own-lineage prices 0 / 1 |
| B1d | deliberate(0)-then-cite → 122 | fix core | adopted exact-count law, truth still installs |
| B2 | overwrite-founded truth, reused slot | fix core | HOLD — r4=REVISED, installs at 1 |
| B3 | no-op WEAKEN edges (60 and 20) | fix core | HOLD — payable 1 / floor 0 |
| B4 | exactly-P on repair-changed price (2→1) | fix core | HOLD — 109 / OK / 122 exact |
| B5 | epoch<0 reachability | fix core | unreachable via public ops |
| B6 | fought/high-water leakage across kill | fix core | HOLD — zero leakage |
| K1–K6 | port: neuter, chain, reuse, premium, founding, imm-121 | canonical+patch | HOLD — 70/70 |

## Notes for the coordinator / Micah (not kills)

- The r3 no-op-WEAKEN +1 (implementer's Q2) is real and unchanged: one
  expressed doubt permanently +1s that generation's price. It is payable
  policy, not a refusal — but it is the cheapest remaining "price a truth"
  lever an adversary holds *within* a generation. The repair correctly did
  not touch it (adopted meter table).
- The deliberate(0)-then-cite 122 (B1d) is the exact-count law meeting the
  repair's new price-0 outcomes more often. It fails fast at cite time and
  never blocks the truth. Worth one line in the repair doc so nobody
  misreads it as a regression.
- The two `epoch<0` guards added inside `st_meter_hw`/`st_meter_revs` are
  dead code (single caller already guards). Harmless; leave them.
- Disk: home hit 100% repeatedly during this run (an unknown active consumer
  re-fills it); I worked in `/tmp/pamsv2_red` and cleared ~910M of cold
  pip/huggingface caches. Final deliverables are in this directory.
