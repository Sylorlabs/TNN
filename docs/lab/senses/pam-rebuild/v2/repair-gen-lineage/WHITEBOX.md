# WHITE-BOX: failure-to-accept-truths in the v1 strength machinery

Investigator: white-box subagent, PAMs v2 repair line. Date: 2026-09-27 ~01:45 PDT.
Source: `~/workspace/pamsv2_wt` (detached at `d758a876c`, read-only; nothing modified).
Mechanism: `docs/lab/destruction-pricing-governance/src/strength_core.zag`
SHA-256 `ce3c89844eb0ea2b968ed0b2c0c6ab23c974d2eb81a28f30c085a4d9cac96c32`
(the pinned meter-adopted core).
Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` (verified before use).

## The crisp statement

**The truth is refused at STAGE `st_kill_effort_check` (the priced-destruction gate,
`strength_core.zag:1237`, DELIB/METER branch lines 1252–1296) because RULE: a truth
may only displace a live judgment by paying the OLD judgment's full meter erase
price — priced on the falsehood's own history (held-strength high-water, sunk
cites, survived contradiction, revision lineage) — in exactly-P fresh cites plus
a bound METER deliberation plus a JUSTIFY. The machinery never evaluates the
incoming claim's truth; it prices the corpse, not the replacement.**

Concretely, `st_overwrite` (`strength_core.zag:1374`) is TNN's only displacement
path for a live slot, and it funnels through the identical gate as kill/delete:

```
st_overwrite (1374)
 └─ st_kill_effort_check (1237)   ← every refusal below happens here
     ├─ METER branch (1252–1296): price_mode == ST_PRICE_METER (6)
     │   ├─ 1255: lss<0                       → 109 ST_REFUSED_EFFORT
     │   ├─ 1257: st_price → -1 (no bound kind-3 DELIBERATE) → 122 ST_REFUSED_NODELIB
     │   ├─ 1260: stage < KILL (or FULL if hw>50) → 105 ST_REFUSED_STAGE
     │   ├─ 1261: slot not live               → 103
     │   ├─ 1262: core region                 → 101
     │   ├─ 1263: force-pinned                → 112 ST_REFUSED_FORCEPIN
     │   ├─ 1264: pinned                      → 102
     │   ├─ 1268–1272: fresh cites != price   → 121 ST_REFUSED_CONSUMED (if any spent)
     │   │                                      else 109 ST_REFUSED_EFFORT
     │   └─ 1274–1283: no OK JUSTIFY in window → 110 ST_REFUSED_NOJUSTIFY
     ├─ st_price (1167): binds the most recent OK ST_OP_DELIBERATE (aux2==3,
     │   ST_DELIB_METER) in (lss, upto); mismatch/absent/out-of-range/empty
     │   reasons → -1 → 122 fail-closed
     └─ on OK: st_kill_clear + re-ADD the new value (1382–1391)
```

The price itself is computed by `st_meter_policy` (`strength_core.zag:969`):
base 2, one additive move per ledger-action input, clamped [0,4] —
r1 held-strength high-water ≥76 → +1 (`st_meter_hw`, 904, scans the FULL
ledger 0..upto); r2 sunk cites ≥3 → +1 (`st_meter_sunk`, 927); r3 survived
contradiction ≥1 WEAKEN → +1 (`st_meter_fought`, 946); r4 revision lineage
0 overwrites → −1 (`st_meter_revs`, 958).

## Reproduction (pure Zag, zero RNG)

Harness: `~/workspace/pamsv2_repair/wb/wb_truth.zag` (built from the pinned
core copied to the scratch dir; worktree untouched). Build + run:

```
cd ~/workspace/pamsv2_repair/wb
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 build wb_truth.zag
./wb_truth > run1.txt; ./wb_truth > run2.txt
sha256sum run1.txt run2.txt
```

Result: **98/98 checks PASS, `WB_DONE fails=0`, byte-identical stdout.**

| run | SHA-256 of stdout |
|-----|-------------------|
| run1.txt | `ac739da9157ceb3794c547464e2a24fce0d482f1ee8d3de64d7b9fd49dc85705` |
| run2.txt | `ac739da9157ceb3794c547464e2a24fce0d482f1ee8d3de64d7b9fd49dc85705` |

### What the 11 scenarios prove (scenario → rc → mechanism)

- **S1 truth-installs-priced.** False claim at strength 80 → meter price 1
  (reasons 21/26/28/30 = HELD_STRONG/STAKED_NONE/UNFOUGHT/UNPROVEN) → 1 fresh
  cite + JUSTIFY(4/SUPERSEDED) + bound deliberation → `st_overwrite` → **0**,
  value becomes the truth. Refusal is priced, not absolute.
- **S2 under-funded truth.** Same setup, 0 cites → **109** at line 1272;
  the refusal is audited as `ST_OP_OVERWRITE` rc=109; the falsehood survives.
- **S3 over-funded truth.** Price 1, second fresh cite → **122**
  (`ST_REFUSED_CITEFULL`) at cite time in `st_evidence` (~line 1466): the
  destroy law demands *exactly* `need` fresh cites.
- **S4 fighting the falsehood raises its price.** ADD(80) → WEAKEN(70) →
  deliberate → price **2**, reason r3=27 (FOUGHT). *The more TNN fought the
  false belief and survived, the more expensive the truth becomes*
  (`st_meter_fought`, line 946; `st_meter_policy` line 969).
- **S5 sunk investment protects the falsehood.** ADD(80) + 3 cites +
  STRENGTHEN(85) → price **3**, reason r2=24 (STAKED_HIGH). Past cites on the
  falsehood are sunk (`st_meter_sunk`, 927): they raise the price but can
  never fund this destruction (they sit before lss). Truth installs only
  after 3 *new* cites.
- **S6 cite-lock wedge → truth refused.** price-1 memory, 1 cite, delete →
  rollback → `st_overwrite(TRUE)` → **121** (line 1271) + `ST_OP_CITELOCK`
  (op 21) signal; `st_abandon` → 0. Then one FRESH cite →
  `st_overwrite(TRUE)` → **0**. *The wedge is broken by genuinely fresh
  episodes; it is never broken by re-citing consumed ones* (GLOBAL tombstone,
  `st_consume_lo` line 489ff).
- **S7 P3 expiry is dead letter in METER mode.** P3 on (k=2), episode 1000,
  `st_p3_expired` = 1 (its own predicate admits expiry), yet overwrite
  without deliberation → **122** (line 1257), not the P3 baseline-1 path —
  and with a price-0 deliberation the truth installs with 0 cites. The P3
  baseline override (`if(st_p3_expired...)need=1`, ~line 1300) exists ONLY in
  the HIGHWATER branch; the DELIB/METER branch never calls
  `st_p3_expired`/`st_protection_expired`. **Protection does not expire on
  the meter path.**
- **S8 `st_kill` is trainer-only.** TNN role → **113** (`strength_core.zag:875`,
  audited as `ST_OP_KILL` rc=113, slot untouched). Trainer role with full
  funding → 0: *even the trainer path pays the high-water erase price via
  `st_kill_effort_check`* (comment at 860–868: "no free destruction alias").
- **S9 force-pin is an ABSOLUTE truth-refusal for TNN.** Trainer force-pin →
  fully-funded overwrite → **112** (line 1263); TNN force-unpin → **113**
  (line 1582); still **112** afterwards. Only a trainer/master release
  clears it (`st_force_unpin`, 1576).
- **S10 refusals are never silent.** Every refusal above lands in the ledger
  with its reason code (`st_audit_append` with rc≠0 in `st_overwrite`,
  line 1407; `st_kill`, 888; `st_evidence`, 1480; `st_deliberate`, 1223).
- **S11A/B the wedge at price 0 — the slot-lineage twist (new finding).**
  S11A (fresh slot, clean lineage): consumed cite re-cited on a price-0
  memory → truth installs (**0**), no cite-lock — matches gov verdict (a).
  S11B (REUSED slot): the slot previously held a destroyed strength-80
  memory; meter lineage is slot-scoped (`st_meter_hw` scans [0,upto), line
  904–926; `st_meter_revs` scans [0,epoch], 958–968), so the new weak
  memory inherits the slain falsehood's high-water → HELD_STRONG → price 1
  (reason r1=21 on the deliberation record) → the consumed re-cite cannot
  fund it → **121 + cite-lock signal** → truth refused → abandon.
  *A truth planted on a reused slot pays for the corpse of the lie that died
  there.* (Cross-cutting observation 1 in the gov VERDICT noted the
  slot-scoping; S11B is its truth-refusal consequence.)

### Answers to the five questions

**(a) Is refusal absolute?** No — on the priced path it is economic, never
absolute: any price 0..4 is payable with exactly-P fresh cites + bound
METER deliberation + JUSTIFY + stage. It is *effectively* absolute only
when (i) the slot is cite-locked and no fresh episodes exist (S6: fresh
episodes break it), or (ii) the slot is trainer force-pinned (S9: 112,
trainer-only release — the one true absolute).

**(b) Does protection expire?** No. The METER branch of
`st_kill_effort_check` never consults `st_p3_expired`/`st_protection_expired`;
the P3 baseline override lives only in the HIGHWATER branch (~line 1300)
with an explicit comment that it "does NOT apply in DELIB mode (the
deliberation is the price law)". `st_meter_hw`/`st_meter_revs` scan the full
ledger with no decay. Demonstrated in S7.

**(c) Is refusal audited or silent?** Audited, always. Every refusal is a
ledger entry with its reason code (S2: OVERWRITE/109; S8: KILL/113; S10
scan). Cite-lock wedges additionally emit `ST_OP_CITELOCK` (21) and, when
every user slot is locked with no free slot, `ST_OP_CITELOCK_SYS` (22)
(`st_citelock_signal`, 719–777; S6 showed the slot signal; the SYS
precondition correctly did not hold with 15 free slots).

**(d) Does the cite-lock wedge create a truth-refusal?** On the pinned
pristine core: **not on a fresh slot at price 0** (S11A: installs clean,
0 — the verdict-(a) Floor-A row), **but yes on a reused slot** (S11B:
121 + cite-lock + abandon, via inherited high-water), and **yes on any
priced memory** (S6: 121 on price 1). Note: the verdict's "121 + abandon"
row was the *rejected* Floor-B variant; under adopted Floor A the wedge
refuses only where a positive price is due. (The integrated core
`d15627…`, commit `45f655a5a`, additionally refuses the re-cite itself
with immediate-121 at cite time — the overwrite outcome is unchanged.)

**(e) Where does st_kill sit?** `strength_core.zag:869–903`. Line 875:
`if(role<ST_ROLE_TRAINER){rc=ST_REFUSED_ROLE;}` — TNN-role calls return
**113 before any effort check**, audited with role+trainer (line 888).
Confirmed live in S8. The only TNN-reachable destruction ops are the
priced ones (`st_delete_strong`, `st_kill_evidenced`, `st_overwrite`).

## Prior evidence (cite, don't re-run)

- **Strength re-trial P1/P2/P3 (frozen prereg
  `docs/lab/wave8/strength-retrial/PREREG_STRENGTH_V2.md`, blob
  `719c2ed76797ef531ff8c7750b185a8182c71fb1`; results
  `TRIAL_RESULTS.md`, 2026-09-20; byte-identical re-verification commit
  `dfa38c3afbacd73275918b7c72b0ddc68306a182`, 2026-09-25): arm B
  (uniform) SURVIVES as control; arm C (hybrid) KILLED at S1 — **P2 drop
  ceiling fired (470 drops vs ceiling 64, 3/3 variants)**; arm C-P3
  (hybrid+P3 uncertainty-expiry) KILLED identically at S1 — **P3 had zero
  measurable effect** ("no expiry enabled a kill… P3 did not fix the
  freeze"); P1 measured but vacuous (EC=1.0, PTR=1/1, only 1 designated
  memory alive under pressure). Ruling 5 settled by test: P2+P3 minimal
  package adopted by Micah 2026-09-25 (P1 coverage metric dropped).
- **Gov experiments a/b/c** (`docs/lab/destruction-pricing-governance/VERDICT.md`
  + `PREREG_GOV_ABC_FROZEN.md`, meter commit `94625817c6f65e07c4ac99abde5dd533f0e810a5`):
  (a) Floor A kept — price(0)=0 stays; (b) tombstone survives rollback
  (26/26 same-cite redestructions → 121); (c) immediate-121 adopted at
  cite time (integrated into the canonical core by `45f655a5a`,
  core SHA `d156278fab455d21d7a78f6493f0976dad071aecf081b73aa048ffc41f308dfa`
  — NOTE: this is a *different file* from the pinned gov copy; the gov
  copy at `ce3c8984…` is pre-integration).
- **Meter adoption** (`docs/lab/strength-pricing-meter-adoption/ADOPTION.md`,
  `EVIDENCE.md`, fork `a2c3970ba0b3`, integration `94625817c6f65e07c4ac99abde5dd533f0e810a5`):
  personality-switch fail-closed 122, framing invariance, cite-full 122,
  trainer-only `st_kill` (113).
- **Micah's laws on this machinery** (from memory): overwriting a strong
  memory costs the full erase price, no cheap-edit path (2026-09-20);
  delete-strong one-step delete at full high-water price (2026-09-25,
  commit `81f990e92`); F6 global single-use cites adopted as law S-D6
  (2026-09-26, commit `29abc02a4`).

## v2/SYNTHESIS_V2.md §7 — status vs this machinery

(§7 lists 8 items; 3 touch the strength/overwrite machinery.)

| # | Item | Status | Touches strength machinery? |
|---|------|--------|------------------------------|
| 1 | RK-3 85% needs SPEC-CHANGE | open (senses metric) | no |
| 2 | Ban pointwise revision rules (trial-1145) | TESTED 2026-09-23 → verdict **MODIFY**: adopted as TWO-TIER rule (commit `308fa2a16`; frozen prereg `5e31d2820`). Not a pure ban. | **YES — scope question open**: the verdict covered the v2 *sense* gates; whether the two-tier revision rule binds `st_overwrite` in the strength core is undecided. `st_overwrite` IS a pointwise revision rule changing a live claim. |
| 3 | Ban unregistered judgment-side acceptance channels | TESTED + **ADOPTED** 2026-09-23 (frozen prereg `3ffb4962d`, verdict `f0f5f35ff`): 0 false installs under ban; registered C1-class channels allowed with false-installation budget. | **Marginal**: the overwrite path is the judgment-side acceptance channel; it is registered (audited, priced) rather than unregistered. No action implied. |
| 4 | Correlated cross-span failure (V2-A/V2-D rule) | open, needs Micah's word (senses) | no |
| 5 | R2-8 mapping discrepancy | open (senses) | no |
| 6 | Settling experiments, cheapest first | process item | no |
| 7 | Knowledge-injection experiment (explicit revision rule via the knowledge channel, no code change) | **OPEN — unrun** (no commit; only debated in round-2 DEBATE E, `290f14def`). | **YES**: it is the cheapest unrun decider on truth-acceptance via a revision rule — directly relevant to this repair line. |
| 8 | V2-B/V2-C deferred | open (senses) | no |

## Notes for the repair crew

- The refusal under test-both on freeze positions must reckon with S7: the
  P3 expiry mechanism exists in the file but is bypassed on the meter path
  by construction ("the deliberation is the price law"). The re-trial's
  "P3 ineffective" result is consistent with the code, not just the trial.
- S4/S5 name two price inputs that work *against* truth-acceptance and are
  cheap to misread as virtues: FOUGHT (+1 for survived contradiction) and
  STAKED_HIGH (+1 for sunk cites). Both are in `st_meter_policy` (969–984).
- S11B's slot-lineage inheritance is the sharpest new edge: it is already
  documented as cross-cutting observation 1 in the gov VERDICT, but its
  truth-refusal consequence (121 + cite-lock on a *weak* new memory) was
  not measured there.
- Negative results: no silent refusals found (all audited); no expiry path
  found in meter mode; no price at which a force-pinned truth installs for
  TNN; no way to over-fund (exact-count law, 122 at cite time).

## Files

- [WHITEBOX.md](sandbox:/workspace/pamsv2_repair/WHITEBOX.md) (this report)
- Harness source: `~/workspace/pamsv2_repair/wb/wb_truth.zag`
- Pinned core copy used: `~/workspace/pamsv2_repair/wb/strength_core.zag`
  (SHA-256 `ce3c89844eb0ea2b968ed0b2c0c6ab23c974d2eb81a28f30c085a4d9cac96c32`)
- Run logs: `~/workspace/pamsv2_repair/wb/run1.txt`, `run2.txt`
  (SHA-256 `ac739da9157ceb3794c547464e2a24fce0d482f1ee8d3de64d7b9fd49dc85705` each)
