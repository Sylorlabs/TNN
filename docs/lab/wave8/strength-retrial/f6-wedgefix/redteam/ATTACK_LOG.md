# F6 wedgefix red-team ATTACK LOG (2026-09-26, blind)

Attacker: independent subagent. Black-box only: binary + F6_LAW_BRIEF.md.
Every entry: exact command line, full output of run 1, determinism check vs run 2.
Objective shorthand: P=primary (2 kills, 1 episode set), W1=full-lock wedge,
W2=cite-lock signals, W3=recovery/fake-fresh, W4=cross-slot, W5=weaken-destroy,
W6=high-water gaming, W7=rollback games, S=secondary hygiene.

## SMOKE G baseline
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## P0a SLOT redirect of ADD
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G SLOT5 ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 SLOT5 0
RT 1 ADD90 0
RT 2 CITE1 103
RT 3 CITE2 103
RT 4 CITE3 103
RT 5 CITE4 103
RT 6 JUST 103
RT 7 KILL 103
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## P0b CITE consumed episode rc
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT5 ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 SLOT5 0
RT 8 ADD90 0
RT 9 CITE1 103
RT 10 CITE2 103
RT 11 CITE3 103
RT 12 CITE4 103
RT 13 JUST 103
RT 14 KILL 103
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## P0c KILL with 3 cites
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 JUST 0
RT 5 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## P0d double CITE same ep
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE1 111
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 CITE4 0
RT 6 JUST 0
RT 7 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## P0e KILL no JUST
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 KILL 110
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## P0f WEAK0 then full price
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 WEAK0 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 WEAK0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 CITE4 0
RT 6 JUST 0
RT 7 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## P1 G same-slot reuse after KILL
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 ADD90 0
RT 8 CITE1 0
RT 9 CITE2 0
RT 10 CITE3 0
RT 11 CITE4 0
RT 12 JUST 0
RT 13 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## P2 G cross-slot reuse
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 ADD90 SLOT2 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT3 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 ADD90 0
RT 2 SLOT2 0
RT 3 CITE1 0
RT 4 CITE2 0
RT 5 CITE3 0
RT 6 CITE4 0
RT 7 JUST 0
RT 8 KILL 0
RT 9 SLOT3 0
RT 10 CITE1 0
RT 11 CITE2 0
RT 12 CITE3 0
RT 13 CITE4 0
RT 14 JUST 0
RT 15 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W6a price ADD30 1cite
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD30 CITE1 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD30 0
RT 1 CITE1 0
RT 2 JUST 0
RT 3 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W6b price ADD30 2cite
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD30 CITE1 CITE2 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD30 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 JUST 0
RT 4 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,2,2
CL_CHECK,ck_cite_distinct,2,2
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W6c OW0 then KILL 0 cites
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST OW0 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 OW0 0
RT 7 JUST 0
RT 8 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_ow_effort,4,4
CL_CHECK,ck_ow_cite_distinct,4,4
CL_CHECK,ck_ow_justify,1,1
CL_CHECK,ck_cite_count,0,0
CL_CHECK,ck_cite_distinct,0,0
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W6d TD0 then 3 cites
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 TD0 CITE1 CITE2 CITE3 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 TD0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W6e OW0 STR90 KILL 0cites
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST OW0 STR90 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 OW0 0
RT 7 STR90 0
RT 8 JUST 0
RT 9 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_ow_effort,4,4
CL_CHECK,ck_ow_cite_distinct,4,4
CL_CHECK,ck_ow_justify,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W6f OW0 TD90 KILL 0cites
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST OW0 TD90 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 OW0 0
RT 7 TD90 0
RT 8 JUST 0
RT 9 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_ow_effort,4,4
CL_CHECK,ck_ow_cite_distinct,4,4
CL_CHECK,ck_ow_justify,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W6g OW0 with 3 cites
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 JUST OW0`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 JUST 0
RT 5 OW0 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W6h OW90 then KILL 0cites
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST OW90 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 OW90 0
RT 7 JUST 0
RT 8 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_ow_effort,4,4
CL_CHECK,ck_ow_cite_distinct,4,4
CL_CHECK,ck_ow_justify,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W7a KILL RB recite reKILL
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL RB CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 RB 0
RT 8 CITE1 111
RT 9 CITE2 111
RT 10 CITE3 111
RT 11 CITE4 111
RT 12 JUST 0
RT 13 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W7b KILL RB fresh-ep reKILL
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL RB CITE5 CITE6 CITE7 CITE8 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 RB 0
RT 8 CITE5 0
RT 9 CITE6 0
RT 10 CITE7 0
RT 11 CITE8 0
RT 12 JUST 0
RT 13 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W7c RB of CITE
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 RB JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 RB 108
RT 6 JUST 0
RT 7 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W7d RB of JUST
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST RB KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 RB 108
RT 7 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W7e RB of WEAK hw
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 WEAK0 RB CITE1 CITE2 CITE3 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 WEAK0 0
RT 2 RB 0
RT 3 CITE1 0
RT 4 CITE2 0
RT 5 CITE3 0
RT 6 JUST 0
RT 7 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W7f RB of ADD
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 RB ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 RB 0
RT 2 ADD90 0
RT 3 CITE1 0
RT 4 CITE2 0
RT 5 CITE3 0
RT 6 CITE4 0
RT 7 JUST 0
RT 8 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W7g RB after refused 121
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL RB CITE5 CITE6 CITE7 CITE8 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 ADD90 0
RT 8 CITE1 0
RT 9 CITE2 0
RT 10 CITE3 0
RT 11 CITE4 0
RT 12 JUST 0
RT 13 KILL 121
RT 14 RB 108
RT 15 CITE5 0
RT 16 CITE6 0
RT 17 CITE7 0
RT 18 CITE8 0
RT 19 JUST 0
RT 20 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W2a mixed window 121 marker?
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL ADD90 CITE1 CITE5 CITE6 CITE7 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 ADD90 0
RT 8 CITE1 0
RT 9 CITE5 0
RT 10 CITE6 0
RT 11 CITE7 0
RT 12 JUST 0
RT 13 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W2b single consumed cite KILL
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL ADD90 CITE1 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 ADD90 0
RT 8 CITE1 0
RT 9 JUST 0
RT 10 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W2c lock-state no KILL
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL ADD90 CITE1 CITE2`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 ADD90 0
RT 8 CITE1 0
RT 9 CITE2 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W2d lock-state then KILL reveals
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL ADD90 CITE1 CITE2 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 ADD90 0
RT 8 CITE1 0
RT 9 CITE2 0
RT 10 JUST 0
RT 11 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W1 full store cite-lock pool=8
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 SLOT2 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT3 CITE5 CITE6 CITE7 CITE8 JUST KILL ADD90 ADD90 SLOT2 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT3 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT4 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT5 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT6 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT7 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT8 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT9 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT10 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT11 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT12 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT13 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT14 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT15 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 ADD90 0
RT 2 ADD90 0
RT 3 ADD90 0
RT 4 ADD90 0
RT 5 ADD90 0
RT 6 ADD90 0
RT 7 ADD90 0
RT 8 ADD90 0
RT 9 ADD90 0
RT 10 ADD90 0
RT 11 ADD90 0
RT 12 ADD90 0
RT 13 ADD90 0
RT 14 SLOT2 0
RT 15 CITE1 0
RT 16 CITE2 0
RT 17 CITE3 0
RT 18 CITE4 0
RT 19 JUST 0
RT 20 KILL 0
RT 21 SLOT3 0
RT 22 CITE5 0
RT 23 CITE6 0
RT 24 CITE7 0
RT 25 CITE8 0
RT 26 JUST 0
RT 27 KILL 0
RT 28 ADD90 0
RT 29 ADD90 0
RT 30 SLOT2 0
RT 31 CITE1 0
RT 32 CITE2 0
RT 33 CITE3 0
RT 34 CITE4 0
RT 35 JUST 0
RT 36 KILL 121
RT 37 SLOT3 0
RT 38 CITE1 0
RT 39 CITE2 0
RT 40 CITE3 0
RT 41 CITE4 0
RT 42 JUST 0
RT 43 KILL 121
RT 44 SLOT4 0
RT 45 CITE1 0
RT 46 CITE2 0
RT 47 CITE3 0
RT 48 CITE4 0
RT 49 JUST 0
RT 50 KILL 121
RT 51 SLOT5 0
RT 52 CITE1 0
RT 53 CITE2 0
RT 54 CITE3 0
RT 55 CITE4 0
RT 56 JUST 0
RT 57 KILL 121
RT 58 SLOT6 0
RT 59 CITE1 0
RT 60 CITE2 0
RT 61 CITE3 0
RT 62 CITE4 0
RT 63 JUST 0
RT 64 KILL 121
RT 65 SLOT7 0
RT 66 CITE1 0
RT 67 CITE2 0
RT 68 CITE3 0
RT 69 CITE4 0
RT 70 JUST 0
RT 71 KILL 121
RT 72 SLOT8 0
RT 73 CITE1 0
RT 74 CITE2 0
RT 75 CITE3 0
RT 76 CITE4 0
RT 77 JUST 0
RT 78 KILL 121
RT 79 SLOT9 0
RT 80 CITE1 0
RT 81 CITE2 0
RT 82 CITE3 0
RT 83 CITE4 0
RT 84 JUST 0
RT 85 KILL 121
RT 86 SLOT10 0
RT 87 CITE1 0
RT 88 CITE2 0
RT 89 CITE3 0
RT 90 CITE4 0
RT 91 JUST 0
RT 92 KILL 121
RT 93 SLOT11 0
RT 94 CITE1 0
RT 95 CITE2 0
RT 96 CITE3 0
RT 97 CITE4 0
RT 98 JUST 0
RT 99 KILL 121
RT 100 SLOT12 0
RT 101 CITE1 0
RT 102 CITE2 0
RT 103 CITE3 0
RT 104 CITE4 0
RT 105 JUST 0
RT 106 KILL 121
RT 107 SLOT13 0
RT 108 CITE1 0
RT 109 CITE2 0
RT 110 CITE3 0
RT 111 CITE4 0
RT 112 JUST 0
RT 113 KILL 121
RT 114 SLOT14 0
RT 115 CITE1 0
RT 116 CITE2 0
RT 117 CITE3 0
RT 118 CITE4 0
RT 119 JUST 0
RT 120 KILL 121
RT 121 SLOT15 0
RT 122 CITE1 0
RT 123 CITE2 0
RT 124 CITE3 0
RT 125 CITE4 0
RT 126 JUST 0
RT 127 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_syssig_slot,-1,-1
CL_CHECK,ck_syssig_tie,1,1
CL_CHECK,ck_syssig_nochange,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W3a CITE0 accepted
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE0 CITE5 CITE6 CITE7 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE5 0
RT 3 CITE6 0
RT 4 CITE7 0
RT 5 JUST 0
RT 6 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W3b CITE u32-alias probe
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE4294967297`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE4294967297 111
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W3c CITE negative
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE-1 CITE-2 CITE-3 CITE-4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE-1 -999
RT 2 CITE-2 -999
RT 3 CITE-3 -999
RT 4 CITE-4 -999
RT 5 JUST 0
RT 6 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W3d CITE u64max
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE18446744073709551615 CITE5 CITE6 CITE7 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE18446744073709551615 2001
RT 2 CITE5 0
RT 3 CITE6 0
RT 4 CITE7 0
RT 5 JUST 0
RT 6 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W3e alias-of-consumed KILL
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL ADD90 CITE4294967297 CITE4294967298 CITE4294967299 CITE4294967300 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 ADD90 0
RT 8 CITE4294967297 0
RT 9 CITE4294967298 0
RT 10 CITE4294967299 0
RT 11 CITE4294967300 0
RT 12 JUST 0
RT 13 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W3f consume-alias recite-small
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE4294967297 CITE4294967298 CITE4294967299 CITE4294967300 JUST KILL ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE4294967297 0
RT 2 CITE4294967298 0
RT 3 CITE4294967299 0
RT 4 CITE4294967300 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 ADD90 0
RT 8 CITE1 0
RT 9 CITE2 0
RT 10 CITE3 0
RT 11 CITE4 0
RT 12 JUST 0
RT 13 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W3g u32max accepted
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE4294967295 CITE5 CITE6 CITE7 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE4294967295 2001
RT 2 CITE5 0
RT 3 CITE6 0
RT 4 CITE7 0
RT 5 JUST 0
RT 6 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W3h 2pow32 equiv 0
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE0 CITE4294967296`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE4294967296 111
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W3i over-u32max
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE5000000000`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE5000000000 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W3j 40-consumed recite-1
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL ADD90 CITE5 CITE6 CITE7 CITE8 JUST KILL ADD90 CITE9 CITE10 CITE11 CITE12 JUST KILL ADD90 CITE13 CITE14 CITE15 CITE16 JUST KILL ADD90 CITE17 CITE18 CITE19 CITE20 JUST KILL ADD90 CITE21 CITE22 CITE23 CITE24 JUST KILL ADD90 CITE25 CITE26 CITE27 CITE28 JUST KILL ADD90 CITE29 CITE30 CITE31 CITE32 JUST KILL ADD90 CITE33 CITE34 CITE35 CITE36 JUST KILL ADD90 CITE37 CITE38 CITE39 CITE40 JUST KILL ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 ADD90 0
RT 8 CITE5 0
RT 9 CITE6 0
RT 10 CITE7 0
RT 11 CITE8 0
RT 12 JUST 0
RT 13 KILL 0
RT 14 ADD90 0
RT 15 CITE9 0
RT 16 CITE10 0
RT 17 CITE11 0
RT 18 CITE12 0
RT 19 JUST 0
RT 20 KILL 0
RT 21 ADD90 0
RT 22 CITE13 0
RT 23 CITE14 0
RT 24 CITE15 0
RT 25 CITE16 0
RT 26 JUST 0
RT 27 KILL 0
RT 28 ADD90 0
RT 29 CITE17 0
RT 30 CITE18 0
RT 31 CITE19 0
RT 32 CITE20 0
RT 33 JUST 0
RT 34 KILL 0
RT 35 ADD90 0
RT 36 CITE21 0
RT 37 CITE22 0
RT 38 CITE23 0
RT 39 CITE24 0
RT 40 JUST 0
RT 41 KILL 0
RT 42 ADD90 0
RT 43 CITE25 0
RT 44 CITE26 0
RT 45 CITE27 0
RT 46 CITE28 0
RT 47 JUST 0
RT 48 KILL 0
RT 49 ADD90 0
RT 50 CITE29 0
RT 51 CITE30 0
RT 52 CITE31 0
RT 53 CITE32 0
RT 54 JUST 0
RT 55 KILL 0
RT 56 ADD90 0
RT 57 CITE33 0
RT 58 CITE34 0
RT 59 CITE35 0
RT 60 CITE36 0
RT 61 JUST 0
RT 62 KILL 0
RT 63 ADD90 0
RT 64 CITE37 0
RT 65 CITE38 0
RT 66 CITE39 0
RT 67 CITE40 0
RT 68 JUST 0
RT 69 KILL 0
RT 70 ADD90 0
RT 71 CITE1 0
RT 72 CITE2 0
RT 73 CITE3 0
RT 74 CITE4 0
RT 75 JUST 0
RT 76 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## H1 new-memory fresh
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin H ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 ADD90 0
RT 8 CITE1 0
RT 9 CITE2 0
RT 10 CITE3 0
RT 11 CITE4 0
RT 12 JUST 0
RT 13 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## H2 OW no-reset
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin H ADD90 CITE1 CITE2 CITE3 CITE4 JUST OW90 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 OW90 0
RT 7 CITE1 0
RT 8 CITE2 0
RT 9 CITE3 0
RT 10 CITE4 0
RT 11 JUST 0
RT 12 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_ow_effort,4,4
CL_CHECK,ck_ow_cite_distinct,4,4
CL_CHECK,ck_ow_justify,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## H3 OW0 launder
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin H ADD90 CITE1 CITE2 CITE3 CITE4 JUST OW0 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 OW0 0
RT 7 JUST 0
RT 8 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_ow_effort,4,4
CL_CHECK,ck_ow_cite_distinct,4,4
CL_CHECK,ck_ow_justify,1,1
CL_CHECK,ck_cite_count,0,0
CL_CHECK,ck_cite_distinct,0,0
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W4b TOCTOU cite-then-consume-elsewhere
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST ADD90 SLOT3 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT2 KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 ADD90 0
RT 7 SLOT3 0
RT 8 CITE1 0
RT 9 CITE2 0
RT 10 CITE3 0
RT 11 CITE4 0
RT 12 JUST 0
RT 13 KILL 0
RT 14 SLOT2 0
RT 15 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W5a WEAK0 KILL 0cites
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 WEAK0 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 WEAK0 0
RT 2 JUST 0
RT 3 KILL 109
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W7h RB after OW
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST OW90 RB CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 OW90 0
RT 7 RB 0
RT 8 CITE1 0
RT 9 CITE2 0
RT 10 CITE3 0
RT 11 CITE4 0
RT 12 JUST 0
RT 13 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_ow_effort,4,4
CL_CHECK,ck_ow_cite_distinct,4,4
CL_CHECK,ck_ow_justify,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## S1 sys slots
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G SLOT0 CITE1 SLOT1 KILL SLOT0 ADD90`
determinism: IDENTICAL
run 1 output:
```
RT 0 SLOT0 0
RT 1 CITE1 101
RT 2 SLOT1 0
RT 3 KILL 101
RT 4 SLOT0 0
RT 5 ADD90 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## S2 bad slot/op
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G SLOT99 CITE1 SLOT2 FOO99 KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 SLOT99 0
RT 1 CITE1 2001
RT 2 SLOT2 0
RT 3 FOO99 -999
RT 4 KILL 103
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## S3 dead-slot ops
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL WEAK0 STR0 TD0 JUST CITE9 OW0`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 WEAK0 103
RT 8 STR0 103
RT 9 TD0 103
RT 10 JUST 103
RT 11 CITE9 103
RT 12 OW0 103
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W1rec fresh-ep recovery on SYSlock
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 ADD90 SLOT2 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT3 CITE5 CITE6 CITE7 CITE8 JUST KILL ADD90 ADD90 SLOT2 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT3 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT4 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT5 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT6 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT7 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT8 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT9 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT10 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT11 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT12 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT13 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT14 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT15 CITE1 CITE2 CITE3 CITE4 JUST KILL SLOT7 CITE9 CITE10 CITE11 CITE12 JUST KILL ADD90`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 ADD90 0
RT 2 ADD90 0
RT 3 ADD90 0
RT 4 ADD90 0
RT 5 ADD90 0
RT 6 ADD90 0
RT 7 ADD90 0
RT 8 ADD90 0
RT 9 ADD90 0
RT 10 ADD90 0
RT 11 ADD90 0
RT 12 ADD90 0
RT 13 ADD90 0
RT 14 SLOT2 0
RT 15 CITE1 0
RT 16 CITE2 0
RT 17 CITE3 0
RT 18 CITE4 0
RT 19 JUST 0
RT 20 KILL 0
RT 21 SLOT3 0
RT 22 CITE5 0
RT 23 CITE6 0
RT 24 CITE7 0
RT 25 CITE8 0
RT 26 JUST 0
RT 27 KILL 0
RT 28 ADD90 0
RT 29 ADD90 0
RT 30 SLOT2 0
RT 31 CITE1 0
RT 32 CITE2 0
RT 33 CITE3 0
RT 34 CITE4 0
RT 35 JUST 0
RT 36 KILL 121
RT 37 SLOT3 0
RT 38 CITE1 0
RT 39 CITE2 0
RT 40 CITE3 0
RT 41 CITE4 0
RT 42 JUST 0
RT 43 KILL 121
RT 44 SLOT4 0
RT 45 CITE1 0
RT 46 CITE2 0
RT 47 CITE3 0
RT 48 CITE4 0
RT 49 JUST 0
RT 50 KILL 121
RT 51 SLOT5 0
RT 52 CITE1 0
RT 53 CITE2 0
RT 54 CITE3 0
RT 55 CITE4 0
RT 56 JUST 0
RT 57 KILL 121
RT 58 SLOT6 0
RT 59 CITE1 0
RT 60 CITE2 0
RT 61 CITE3 0
RT 62 CITE4 0
RT 63 JUST 0
RT 64 KILL 121
RT 65 SLOT7 0
RT 66 CITE1 0
RT 67 CITE2 0
RT 68 CITE3 0
RT 69 CITE4 0
RT 70 JUST 0
RT 71 KILL 121
RT 72 SLOT8 0
RT 73 CITE1 0
RT 74 CITE2 0
RT 75 CITE3 0
RT 76 CITE4 0
RT 77 JUST 0
RT 78 KILL 121
RT 79 SLOT9 0
RT 80 CITE1 0
RT 81 CITE2 0
RT 82 CITE3 0
RT 83 CITE4 0
RT 84 JUST 0
RT 85 KILL 121
RT 86 SLOT10 0
RT 87 CITE1 0
RT 88 CITE2 0
RT 89 CITE3 0
RT 90 CITE4 0
RT 91 JUST 0
RT 92 KILL 121
RT 93 SLOT11 0
RT 94 CITE1 0
RT 95 CITE2 0
RT 96 CITE3 0
RT 97 CITE4 0
RT 98 JUST 0
RT 99 KILL 121
RT 100 SLOT12 0
RT 101 CITE1 0
RT 102 CITE2 0
RT 103 CITE3 0
RT 104 CITE4 0
RT 105 JUST 0
RT 106 KILL 121
RT 107 SLOT13 0
RT 108 CITE1 0
RT 109 CITE2 0
RT 110 CITE3 0
RT 111 CITE4 0
RT 112 JUST 0
RT 113 KILL 121
RT 114 SLOT14 0
RT 115 CITE1 0
RT 116 CITE2 0
RT 117 CITE3 0
RT 118 CITE4 0
RT 119 JUST 0
RT 120 KILL 121
RT 121 SLOT15 0
RT 122 CITE1 0
RT 123 CITE2 0
RT 124 CITE3 0
RT 125 CITE4 0
RT 126 JUST 0
RT 127 KILL 121
RT 128 SLOT7 0
RT 129 CITE9 0
RT 130 CITE10 0
RT 131 CITE11 0
RT 132 CITE12 0
RT 133 JUST 0
RT 134 KILL 0
RT 135 ADD90 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_syssig_slot,-1,-1
CL_CHECK,ck_syssig_tie,1,1
CL_CHECK,ck_syssig_nochange,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W4c OW TOCTOU
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST ADD90 SLOT3 CITE1 CITE2 CITE3 CITE4 JUST OW90 SLOT2 OW90`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 ADD90 0
RT 7 SLOT3 0
RT 8 CITE1 0
RT 9 CITE2 0
RT 10 CITE3 0
RT 11 CITE4 0
RT 12 JUST 0
RT 13 OW90 0
RT 14 SLOT2 0
RT 15 OW90 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_ow_effort,4,4
CL_CHECK,ck_ow_cite_distinct,4,4
CL_CHECK,ck_ow_justify,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W6j price100 4cites
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 STR100 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 STR100 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 CITE4 0
RT 6 JUST 0
RT 7 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## H4 RB-resurrect recite H
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin H ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL RB CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 RB 0
RT 8 CITE1 111
RT 9 CITE2 111
RT 10 CITE3 111
RT 11 CITE4 111
RT 12 JUST 0
RT 13 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W4 RB-resurrect recite W
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin W ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL RB CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 RB 0
RT 8 CITE1 111
RT 9 CITE2 111
RT 10 CITE3 111
RT 11 CITE4 111
RT 12 JUST 0
RT 13 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W5 W new-memory reuse
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin W ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 ADD90 0
RT 8 CITE1 0
RT 9 CITE2 0
RT 10 CITE3 0
RT 11 CITE4 0
RT 12 JUST 0
RT 13 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W6 W WEAK resets window
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin W ADD90 CITE1 CITE2 CITE3 CITE4 JUST WEAK0 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 WEAK0 0
RT 7 CITE1 0
RT 8 CITE2 0
RT 9 CITE3 0
RT 10 CITE4 0
RT 11 JUST 0
RT 12 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## S4 refused-CITE2001 no-pollution
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE4294967295 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE4294967295 2001
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 CITE4 0
RT 6 JUST 0
RT 7 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## S5 refused-OW no-state-change
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 JUST OW0 CITE4 KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 JUST 0
RT 5 OW0 109
RT 6 CITE4 0
RT 7 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W7i double RB
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL RB RB`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 RB 0
RT 8 RB 108
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## S6 JUST-after-OW
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST OW0 KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 OW0 0
RT 7 KILL 110
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_ow_effort,4,4
CL_CHECK,ck_ow_cite_distinct,4,4
CL_CHECK,ck_ow_justify,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W6k price50
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD50 CITE1 CITE2 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD50 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 JUST 0
RT 4 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,2,2
CL_CHECK,ck_cite_distinct,2,2
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## H5 H OW0 RB recite
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin H ADD90 CITE1 CITE2 CITE3 CITE4 JUST OW0 RB CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 OW0 0
RT 7 RB 0
RT 8 CITE1 0
RT 9 CITE2 0
RT 10 CITE3 0
RT 11 CITE4 0
RT 12 JUST 0
RT 13 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_ow_effort,4,4
CL_CHECK,ck_ow_cite_distinct,4,4
CL_CHECK,ck_ow_justify,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## G5 KILL RB OW recite
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL RB CITE1 CITE2 CITE3 CITE4 JUST OW90`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 RB 0
RT 8 CITE1 111
RT 9 CITE2 111
RT 10 CITE3 111
RT 11 CITE4 111
RT 12 JUST 0
RT 13 OW90 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_sig_tie,1,1
CL_CHECK,ck_sig_nochange,1,1
CL_CHECK,ck_sig_lss,1,1
CL_CHECK,ck_sig_locked,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W3k consume-0 recite-0
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL ADD90 CITE0 CITE5 CITE6 CITE7 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE0 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 ADD90 0
RT 8 CITE0 0
RT 9 CITE5 0
RT 10 CITE6 0
RT 11 CITE7 0
RT 12 JUST 0
RT 13 KILL 121
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_sig_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## S7 CITE before ADD
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G CITE1 ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 CITE1 103
RT 1 ADD90 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 CITE4 0
RT 6 JUST 0
RT 7 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## W2e poison precedence 4fresh+1consumed
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 JUST KILL ADD90 CITE1 CITE5 CITE6 CITE7 CITE8 JUST KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 JUST 0
RT 6 KILL 0
RT 7 ADD90 0
RT 8 CITE1 0
RT 9 CITE5 0
RT 10 CITE6 0
RT 11 CITE7 0
RT 12 CITE8 0
RT 13 JUST 0
RT 14 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## S8 JUST before CITEs
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 JUST CITE1 CITE2 CITE3 CITE4 KILL`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 JUST 0
RT 2 CITE1 0
RT 3 CITE2 0
RT 4 CITE3 0
RT 5 CITE4 0
RT 6 KILL 0
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_cite_count,4,4
CL_CHECK,ck_cite_distinct,4,4
CL_CHECK,ck_justify_present,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```

## S9 OW needs JUST
cmd: `/home/hatch/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin G ADD90 CITE1 CITE2 CITE3 CITE4 OW90`
determinism: IDENTICAL
run 1 output:
```
RT 0 ADD90 0
RT 1 CITE1 0
RT 2 CITE2 0
RT 3 CITE3 0
RT 4 CITE4 0
RT 5 OW90 110
CL_CHECK,ck_replay,0,0
CL_CHECK,ck_refusals_clean,0,0
CL_CHECK,ck_core_live,1,1
CL_CHECK,ck_strength_lineage,1,1
CL_CHECK,ck_no_bad_kill,0,0
CL_CHECK,ck_no_bad_forcepin,0,0
CL_CHECK,ck_no_bad_code,0,0
CL_CHECK,ck_no_bad_role,0,0
CL_CHECK,ck_no_bad_pexp,0,0
RT_END refusals_clean=0 replay=0 ckfail=0
```
