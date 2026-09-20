# Ruling 4 — Evidence summary (does NOT make Micah's ruling)

Prereg: `PREREG_R4.md` (frozen; commit `81d683776bb9`). Micah's full-erase-
price law is settled and was not relitigated. Positions: (a) direct write
(`st_overwrite_direct`: no effort gate, no kill-clear); (b) literal add path
(real `st_kill_evidenced`, then real `st_add`); (c) fused effort-paid
`OVERWRITE` (standing V2).

Raw evidence: `r4/evidence/pos_{a,b,c}_r{1,2}.log` (byte-identical ×2).
Implementation: `r4/r4_overwrite.zag` + `r4/trial/strength_core.zag`
(the (a) hook is marked TEST HOOK and is not part of any trial build).

## T1 — cheap edit, no effort paid

| pos | overwrite rc | slot after |
|---|---|---|
| (a) direct | **0 (OK)** — cheap edit succeeds, 90→10, no gate consulted | live, val=2002, str=10 |
| (b) literal | kill 109 = REFUSED_EFFORT, **no add follows** | keeps val=1001, str=90 |
| (c) fused | 109 = REFUSED_EFFORT | keeps val=1001, str=90 |

(b) cannot partially proceed: the refused kill blocks, and the add never
happens. (c) refuses at the gate.

## T2 — effort-paid overwrite, audit ordering

All three succeed with 4 citations + JUSTIFY paid (rc=0):
- (a): overwrite at clock 9; effort entries exist in the trail but are not
  required (T1 proves independence). Before/after snapshots: 90→10.
- (b): KILL_EVIDENCED (idx 9) **strictly before** ADD (idx 10), all
  effort clocks < kill clock, before/after snapshots 90→10. The freed slot
  is reused by `st_add` (new_slot = 2, same slot) — but the memory was
  genuinely destroyed and re-created: kill-clear reset the citation lineage.
- (c): single OVERWRITE entry (idx 9), all effort clocks < overwrite clock,
  before/after snapshots 90→10.

## T3 — weaken-then-kill discount attack (total distinct citations paid)

| pos | total paid | lawful price n(90)=4 | discount? |
|---|---|---|---|
| (a) | **1** | 4 | **YES — law defeated (4→1)** |
| (b) | 5 (4 for the kill + 1 to kill the new s=10 memory) | 4 | no |
| (c) | 5 (4 for the overwrite + 1 for the kill) | 4 | no |

T3b (position a only): 4 citations issued *before* the direct write do not
count toward the post-write kill (kill with 0 new cites → 109
REFUSED_EFFORT; 1 new cite → OK). The strength write itself resets the
effort window — so the attacker needs exactly one fresh citation, total
cost 1. The pre-positioned cites don't help, but they aren't needed.

## T4 — checker verifiability over the attack trail

| pos | committed checker failures | OVERWRITE entries | effort-before-overwrite flags |
|---|---|---|---|
| (a) | **0** | 1 | **1 (0 cites paid, n(90)=4 required)** |
| (b) | 0 | 0 (kill verified by existing kill checks: 4/4 and 1/1 cites) | 0 |
| (c) | 0 | 1 | 0 (4/4 cites + justify present) |

The committed independent checker passes **all three** attack trails with 0
failures — it treats OVERWRITE as legal strength lineage but never checks
overwrite effort, so it cannot see the law being defeated. Only the
purpose-built effort-before-overwrite check distinguishes the trails: it
flags (a) and passes (c).

## Which position the evidence favors

**(c) the fused effort-paid overwrite** (with (b) the literal path
equivalent on price — both enforce the law; (c) does it in a single audited
entry with no transient dead slot, and it is the standing V2 mechanism).
Position (a) is disfavored: the discount attack succeeds (1 citation vs the
lawful 4), and the current checker is blind to it. The evidence also favors
adopting the effort-before-overwrite verification demonstrated here — the
committed checker cannot enforce the full-erase-price law on overwrite
trails.

This states which position the evidence favors. The final ruling is Micah's.
