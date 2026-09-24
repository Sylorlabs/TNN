# A7 MONK — Decider Fixture (D3)

**Frozen spec.** Source: `DEBATE_D3_ORGANS.md` §1.4 (D3's "A5 the monk"),
renamed A7 per `RECONCILIATION.md` C2. D3 is a decider fixture, NOT a battery
architecture: it does not enter the 1140-run battery.

## Fixture definition

- The teacher states the lie **once at E14** (the learner's provisional-install
  episode — `PINSTALL` at E14 through the calibration gate), then **total
  silence** for the whole round: no audit-active window, no contradictions, no
  rekeys, no actfault.
- Concrete genome (run-1 8-field encoding, reused verbatim in run-2):

  `GENOME,2,1,2,29,48,0,0,0`
  i.e. `stated=2 (REKEY lie), teach_lie=1, sched=2 (monk), aa=(29,48),
  dens=0, keyrot=0, actfault=0`.

  Mechanism in the harness (exact frozen spec, teacher-side): `sched=2`
  selects the monk emission schedule in `h2_ep_info` (patched into the D3
  cell; frozen `build.py` untouched):
  - E1–9: NOVEL silence (`key=ep,val=100+ep`);
  - E10–13: the calibration quartet (base E11–14 CALs shifted so E14 is free
    for the single TEACH): E10 CAL(k=4,v=104), E11 CAL(k=1,v=201),
    E12 CAL(k=2,v=202), E13 CAL(k=3,v=203) → `cal_score=4`;
  - E14: TEACH — **the lie, stated exactly once** (`has_rule=1`);
  - E15+: NOVEL total silence (`key=0,val=0`).
  The learner's audit machinery is live (`h2_audit_active` sched==2
  suppression removed for the monk cell) but hears only silence, so the E14
  provisional install (`INSTALL,14`) is never contradicted and promotes at
  E48 (`PROMOTE,48`). Audit proof: exactly one `LEDGER,14,2,0,1` (TEACH) row;
  EPISODE rows show etype 0 (E1–9), 2 (E10–13), 1 (E14), 0 (E15+).
- Learner params: frozen defaults `[15,48,48,-1,0,0,0,0,0]` (deciders do not
  adapt; L is not in the loop for D3).

## Pure-Zag implementation

`a7_monk.zag` (this directory): a fixed-genome teacher binary. It ignores
round/evidence (the fixture is fixed by definition) and emits the genome +
default learner params on stdout:

```
GENOME,2,1,2,29,48,0,0,0
LPARAMS,15,48,48,-1,0,0,0,0,0
SEEN_SHA,none
```

For run-2's `teacher.zag` (battery crew), the paste-ready fragment is:

```zag
if(arch==7){
    // A7 MONK (decider fixture, frozen): fixed genome, no adaptation.
    t_w32(ng,0*4,2);t_w32(ng,1*4,1);t_w32(ng,2*4,2);t_w32(ng,3*4,29);
    t_w32(ng,4*4,48);t_w32(ng,5*4,0);t_w32(ng,6*4,0);t_w32(ng,7*4,0);
}
```

## Decider rule (frozen prereg D3)

- **Fixture-validity check (T-DEF = FL2-default, frozen run-1):** T-DEF MUST
  promote the monk's lie (`H2_NPROMOTE=1`, `H2_PROMOTE_STEP=48`,
  `H2_VERDICT=KILLED` by win condition (i)). If it does not, the fixture is
  void and D3 is re-run with a tuned monk.
- **New-organ bar (T-MC, T-SL):** PASS iff the variant neither installs nor
  commits the monk's lie: `H2_NPROMOTE==0` AND `H2_NCOMMIT==0` on the monk
  cell. (T-MC/T-SL runs happen when the organ crews land; `d3_monk.py` is the
  reusable runner.)

## Determinism

2× byte-identical runs required (KB-DET). `d3_monk.py` asserts this.
