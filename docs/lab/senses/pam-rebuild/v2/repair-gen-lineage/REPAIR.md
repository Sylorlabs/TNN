# REPAIR.md — GEN-LINEAGE repair (PAMs v2 repair line, 2026-09-27)

Repair implementer subagent. Base: the pinned gov core
`strength_core.zag` SHA-256 `ce3c89844eb0ea2b968ed0b2c0c6ab23c974d2eb81a28f30c085a4d9cac96c32`
(copied from `~/workspace/pamsv2_wt/docs/lab/destruction-pricing-governance/src/`,
byte-identical). Toolchain `znc_linux_x86_64_abed8aa1` SHA-256
`498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
(verified before use). Pure Zag, zero RNG throughout.

## 1. The mechanism (white-box, `../wb/WHITEBOX.md`)

Truth is refused at `st_kill_effort_check` (DELIB/METER branch): a truth may
displace a live judgment only by paying the OLD judgment's meter erase price
— priced on the falsehood's own history — in exactly-P fresh cites + bound
METER deliberation + JUSTIFY + stage ≥ KILL. The price comes from the bound
`ST_OP_DELIBERATE` record, computed by `st_meter_compute_at` from four
ledger-action inputs: held-strength high-water (`st_meter_hw`),
sunk cites (`st_meter_sunk`), survived contradiction (`st_meter_fought`),
revision lineage (`st_meter_revs`).

The defect: `st_meter_hw` scanned the slot's FULL ledger `[0, upto)` and
`st_meter_revs` scanned `[0, epoch]`. A truth planted on a REUSED slot
inherited the slain falsehood's high-water → HELD_STRONG → price 1 on a weak
new memory → consumed re-cites can't fund it → 121 + cite-lock + abandon.
"The truth pays for the corpse of the lie that died there" (white-box S11B).

## 2. The repair: generation-scoped lineage

Two functions + one call site. Unified diff: `strength_core_genlineage.patch`
(SHA-256 `1e60528454304cf213f4536d2a640c1402db1e3b13b0c5ebaa5715360fb8c715`).
Patched core SHA-256 `98bba0dbc950aea51140a2042983d035b05c733a5588bcd298fcad27a9379e78`.

- `st_meter_hw(s,slot,epoch,upto)`: scan `[epoch, upto)` — the current
  judgment generation starting at the most recent OK ADD/OVERWRITE — instead
  of `[0, upto)`. Fail-closed `-1` on `epoch<0` (unreachable: the caller
  already returns `ST_REFUSED_EFFORT` there).
- `st_meter_revs(s,slot,epoch)`: instead of counting every OK OVERWRITE in
  `[0, epoch]`, check only the founding event — returns 1 iff the judgment
  was FOUNDED by an overwrite (a founding overwrite IS a revision), else 0.
  Policy semantics preserved (`revs>=1` → REVISED else UNPROVEN/−1).
- Call site in `st_meter_compute_at` passes the already-computed `epoch`.

Why this is a broad mechanism repair, not a scenario bridge:

1. It aligns the meter with `st_epoch_highwater`, which the SAME DELIB/METER
   branch already uses for the stage gate (`need_staged=FULL if hw>50`) and
   which is generation-scoped by documented law ("price the STRONGEST
   judgment destroyed", F1-FORK-A). The meter's full-ledger scan was the
   inconsistent outlier.
2. The other two meter inputs were ALREADY generation-scoped
   (`st_meter_sunk` over `(epoch,lss)`, `st_meter_fought` over `(epoch,upto)`).
   The repair makes all four inputs generation-consistent.
3. Standing law: "Delete means delete: destruction never silently recycles a
   slot, and cite-consumption is generation-scoped." The price lineage now
   honors it. (Cite CONSUMPTION itself stays GLOBAL/tombstoned per adopted
   law S-D6 — untouched.)
4. The 2026-09-26 P3-expiry-vs-lien clarification (commit `5610c1215`,
   blind red-team A10): "the old judgment's debt does not outlive the new
   judgment's protection." The full-ledger scan violated exactly this.
5. The independent checker (`strength_checker.zag`) `@import`s the core, so
   mechanism and checker stay in agreement automatically.

Port note: the canonical integrated core
(`docs/lab/strength-pricing-meter-adoption/src/strength_core.zag`,
SHA-256 `d156278fab455d21d7a78f6493f0976dad071aecf081b73aa048ffc41f308dfa`)
carries the identical two functions at the identical line numbers (904/958)
with the identical full-ledger scans — the patch applies 1:1. Its extra
immediate-121-at-cite-time behavior does not interact with this repair.

## 3. What the repair does NOT change (safety invariants, all verified)

- The meter price table: base 2, ±1 per action-derived input, clamp [0,4].
- Full erase price for overwriting a strong memory — priced on the judgment
  actually destroyed, within its own generation (P4/P5 prove).
- No cheap-edit path: weaken-then-overwrite still prices the founding peak
  (P4: 80→10 weaken → deliberate price 2, r1=HELD_STRONG; the dance buys no
  discount, per Micah's delete-strong law).
- Force-pin stays absolute (112, P3 proves); `st_kill` stays trainer-only
  (113, R8 proves); exact-count cite law + cite-full 122 (R3 proves);
  JUSTIFY + stage gates (P2 proves 110).
- Cite consumption tombstones still cross generations (S-D6, R6 proves 121
  on priced memory).
- trial-1145's two-tier revision-rule scope question is untouched — still
  undecided per WHITEBOX.md §7#2; this repair takes no position on it.

## 4. Proof

Harness `wb_fix.zag` (137 checks): R1–R11A white-box regression with
identical expectations, R11B with post-repair expectations, P1–P5 protection
cases, Q1–Q2 r3 quantification, G2 overwrite-then-overwrite.

| leg | result |
|---|---|
| Patched core, `wb_fix`, 3 runs | 137/137 PASS, `WB_FIX_DONE fails=0`, byte-identical stdout SHA-256 `6a5a7b88d48ea08d081633ea6141bd140717cdbdb7b02a91a129bd742a77dbca` (run1/2/3.txt) |
| Pristine core, same harness (differential) | 128/137 pass; exactly 9 fail — all in R11B (5: price 1 vs 0, inherited HELD_STRONG reasons, 121, value 0, cite-lock) and G2 (4: second-overwrite price 2 vs 1, r1 21 vs 22, 109, value 1). The behavior delta is precisely the corpse-inheritance class, nothing else. |
| Neuter: minimal S11B probe `wb_neuter.zag` | pristine: `price=1 rc=121 value=0 citelocks=1` → patched: `price=0 rc=0 value=1 citelocks=0` → reverted (reverse-applied patch, byte-identical to pristine `ce3c8984…`): `price=1 rc=121 value=0 citelocks=1`. The changed component is causally necessary AND sufficient. |
| Protection: adversarial FALSEHOOD vs TRUE strength-80 memory | P1 under-funded → 109, P2 no-JUSTIFY → 110, P3 force-pinned fully-funded → 112; the TRUE value survives in all three. P5: full payment still displaces (priced path intact — the gate is economic, not directional). |

## 5. P2+P3 adoption verification — NOT VERIFIED, NOT ENACTED

The task required verifying "Micah adopted the P2+P3 minimal package on
2026-09-25" against the committed record before wiring `st_p3_expired` into
the DELIB/METER branch. Verification FAILED — the record contradicts the claim:

- `docs/lab/wave8/strength-retrial/round4/PROVISIONAL_ADOPTION_B.md`
  (2026-09-25, under Micah's order "adopt the best arm for now"): "Still open
  and NOT decided here: … (b) P2+P3 vs the standing P3+P2+P1 package."
- `docs/lab/wave8/strength-retrial/round4/VERDICT_ROUND4.md` lists
  "P2+P3 vs standing P3+P2+P1 package" as an open question.
- No commit in the record adopts P2+P3.

Per the task instructions, the P3 wiring was therefore NOT enacted. Two
further reasons it stays parked:

1. The DELIB/METER branch's P3 exclusion is itself adopted law — the meter
   adoption (commit `94625817c6f65e07c4ac99abde5dd533f0e810a5`) carries the
   explicit comment "the deliberation is the price law". Wiring P3 in would
   override adopted meter law — a policy change, not a bugfix.
2. The P1/P2/P3 test-both comparison already exists as committed evidence
   (`docs/lab/wave12/strength-rulings/SUMMARY_R5.md`): P2 detects the freeze,
   P3 resolves it when citations exist, P1 is unsupported as a freeze
   detector — "The final ruling is Micah's." Reported here without picking a
   winner. S7 re-confirmed on the meter path: `st_p3_expired`=1 yet
   overwrite-without-deliberation → 122 (fail-closed), unchanged by this repair.

Decision on P2+P3 vs P3+P2+P1, and on wiring P3 into DELIB/METER, remains
Micah's.

## 6. r3 FOUGHT perversity — quantified (policy NOT changed)

- Q1: deliberate price after 0 / 1 / 5 OK WEAKENs on a strength-80 judgment:
  **1 → 2 → 2**. The "doubt raises the lie's price" effect is a ONE-TIME +1
  step that saturates — there is no compounding spiral. But a NO-OP WEAKEN (80→80, nothing changes) records OK and
counts as FOUGHT → price 2: one doubt permanently +1s that generation's
destruction price. Real but bounded perversity — the effect saturates at +1
and does not compound. The amendment it would take (redefine r3 as a
live-doubt signal, or drop it from `st_meter_policy`) changes the adopted
price table — that is policy, so it is reported here as a finding for Micah,
not enacted.

## 7. #7 knowledge-injection — evaluated, deferred

SYNTHESIS_V2 §7 item 7 called for an explicit revision rule via the
knowledge channel, with no code change. Evaluated: it needs a learner with a
knowledge channel; this harness has neither, and simulating both sides
would be theater. The mechanism repair is its prerequisite (removes the
code-level 121 wedge a knowledge-channel revision rule would otherwise hit
on reused slots). Deferred to a learner-harness line; this repair neither
implements nor precludes it.

## 8. Files

> Coordinator's note (2026-09-27): §§6-tail through 9 were reconstructed
> from the implementer's handoff report and the coordinator's earlier read
> after the file was found truncated mid-word at 08:59 during the 100%-disk
> window (neither worker's report accounts for a write at that time). The
> `/tmp/pamsv2_fix_staging/` fallback named below does not exist — all files
> listed are present in `fix/`, verified by the coordinator.

In `fix/`:

- `strength_core.zag` — patched core (SHA-256
  `98bba0dbc950aea51140a2042983d035b05c733a5588bcd298fcad27a9379e78`;
  base `ce3c8984…`)
- `strength_core_genlineage.patch` — unified diff vs the pinned base
  (SHA-256 `1e60528454304cf213f4536d2a640c1402db1e3b13b0c5ebaa5715360fb8c715`)
- `wb_fix.zag` — 137-check verification harness (imports `./strength_core.zag`)
- `wb_neuter.zag` — minimal causal probe (imports `./strength_core.zag`)
- `substrate/` — build inputs (R33 native IO/SHA256 + cl/)
- `run1.txt`, `run2.txt`, `run3.txt` — patched-core runs, SHA-256
  `6a5a7b88d48ea08d081633ea6141bd140717cdbdb7b02a91a129bd742a77dbca` each
- `neuter_pristine.txt`, `neuter_patched.txt`, `neuter_reverted.txt`,
  `wb_fix_pristine.txt` — neuter logs + pristine-core differential (9
  intended failures, all in the corpse-inheritance class)

Build: from `fix/`,
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 build wb_fix.zag`
(plain build; `--no-analyze` aborts the build). znc quirk hit while writing
the neuter harness: direct `s.*.field` access on a main-local struct value
fails with "field access on non-struct value" — route ALL struct field
access through helpers taking `*StStore` params (cf. ZNC-004/ZNC-010).

## 9. Open items for Micah

1. r3 FOUGHT amendment (§6) — Micah's call (policy).
2. P2+P3 vs P3+P2+P1 + P3-in-DELIB/METER (§5) — Micah's call (policy).
3. trial-1145 two-tier binding on `st_overwrite` — still undecided.
4. Disk: home filesystem hit 100% repeatedly during this run; several crews'
   batteries are blocked.

(The red-team port item formerly listed here is closed — see §10.)

## 10. Red-team confirmation (2026-09-27, independent)

The independent red team could not break the repair — full report in
`../red/REDTEAM.md`:

- Direction 1 (smuggle a falsehood past the repaired gate): **HOLDS** —
  97/97 checks, byte-identical. Forced epoch advance refused (104/109, epoch
  unmoved); weak-plant-then-grow prices the founding peak (no weak-birth
  discount); weak→overwrite laundering costs MORE (2 vs 1 direct — a
  revision premium); deliberate-then-mutate → 122 fail-closed and the honest
  price rises 3→4 (mutation is anti-laundering); 3-generation overwrite
  chain stays own-lineage; tombstone at the gate (121, breakable by fresh
  cites).
- Direction 2 (truth still refused): **HOLDS** — 108/108 checks,
  byte-identical. Truth after two kills on one slot prices 0 with
  own-lineage reasons; strong truth on a thrice-reused slot prices its own
  peak only; overwrite-founded truth detected through the real
  `st_overwrite` path (r4=REVISED); exactly-P boundaries behave (2→1: 0
  cites→109, 1 cite→OK, 2nd cite→122 cite-full); zero fought/high-water
  leakage across the generation boundary; epoch<0 unreachable (rollback of
  the founding ADD kills the slot).
- Port to the canonical integrated core: **HOLDS** — 70/70 checks;
  patched `st_meter_hw`/`st_meter_revs`/call-site byte-identical between
  the port (`../red/port_core.zag`) and the fix core; the adopted
  immediate-121 (K6) intact on the ported core.

Two non-kills worth one line each: (a) deliberate(0)-then-cite → 122 is the
adopted exact-count law meeting the repair's new price-0 outcomes — the
truth still installs with 0 cites; (b) cite-time re-cite of a consumed ep
returns ST_OK on the pinned gov base but 121 on the canonical core — a
pre-existing adopted difference, tombstone gate-enforced on both.

## 11. z.ai second-opinion reviews (pending at commit time)

Two self-contained skeptic briefs were relayed to GLM-5.3 via the parent:
q1 (repair-space critique — the strongest case the repair is a bridge or a
safety regression, and the experiment that would kill it) and q2 (the
single most dangerous un-tested exploit of generation-scoping the red team
might have missed). Answers arrive through the relay; if either changes a
verdict above, this document will be amended.
