# PAM Survivors — Runbook (2026-09-25)

All commands verified during the 2026-09-25 independent re-verification.
Toolchain: `ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

**znc quirk:** `@import` resolves relative to the CURRENT WORKING DIRECTORY —
always `cd` to the source dir (or the dir `build.sh` expects) before building.

**Determinism check (all arms):** run each mode ≥2×, `sha256sum` the outputs,
compare against the frozen SHAs in `REVERIFICATION_2026-09-25.md`. Any
mismatch = do not use; report it.

## X3 composition

```
cd ~/workspace/tnn-lab/senses/pam-rebuild/round2/b3034comp/x3/src
./build.sh /tmp/x3run          # writes /tmp/x3run/x3_battery
/tmp/x3run/x3_battery full > run_full.txt   # N=120, driver battery
/tmp/x3run/x3_battery nop  > run_nop.txt    # 34-half ablation
# expect: full b1e6b4e3e92534127d3e385b8506e9fcabbaa81d77670a5a2a2a19a264b6ff5b
#         nop  e55889eb3fd3e22c98f1ffa03a9e5e4e762fd7506fe219f00722b2671eef9c3c
```

## H-PAM-35

```
cd ~/workspace/tnn-lab/senses/pam-rebuild/round2/r35
$ZNC hpam3536_r35.zag -o /tmp/r35/probe_r35_bin
$ZNC drive35_r35.zag -o /tmp/r35/drive35_r35_bin
python3 run_r35.py    # builds + scores all bars itself, exit 0 = pass
```

## H-PAM-36

```
cd ~/workspace/r36_repair     # runner hardcodes this path; sources synced from canonical r36_repair/
python3 gen_r36.py
python3 run_r36.py
```

## H-PAM-33

```
cd ~/workspace/tnn-lab/senses/pam-rebuild/round2/round_c/hpam33
$ZNC hpam33.zag -o /tmp/h33/hpam33_bin
/tmp/h33/hpam33_bin honest | mint | tamper | wg | wg_manifest | classL | insider
```

## H-PAM-30 / H-PAM-34

```
cd ~/workspace/tnn-lab/senses/pam-rebuild/round2/b303134
$ZNC drive30.zag -o /tmp/h3034/drive30_bin
/tmp/h3034/drive30_bin honest|rf_coarse|rf_full|rc_full|xr_fresh|xr_reuse|n30|o30t|o30n|p30|j30|l30
$ZNC drive34.zag -o /tmp/h3034/drive34_bin
/tmp/h3034/drive34_bin honest|rcrf_coarse|rcrf_full|ge_closed|ge_open|if_window|n34|o34t|o34n|p34|j34|m34|l34
```

## H-8 (tripwire)

```
cd ~/workspace/tnn-lab/senses/pam-rebuild/round2/d1_build
$ZNC d1battery.zag -o /tmp/h8/d1battery
/tmp/h8/d1battery ../f5_redteam300/fixtures_ledger.txt ../f5_redteam300/d1_adv_fixtures.txt
# expect SHA 0ed3de64...920 and AUDIT line n=660 agree=660 ... verdict=SHARED_SOURCE
```

## WILD W1–W12

```
cd ~/workspace/tnn-lab/pam/round4/wild/wN
$ZNC wN.zag -o /tmp/wNtest     # w4: w4_selftrain.zag, w5: w5_memory.zag,
                               # w7: w7_hunter.zag, w10: w10_duel.zag,
                               # w11: w11_chain.zag, w12: w12_budget.zag
# batteries (each ×2, cmp clean):
w1..w6,w8,w9: /tmp/wNtest ~/workspace/tnn-lab/pam/round3/m1/m1_cases.txt
w4,w5:        same tape as argv[1]
w7:           /tmp/w7test ~/workspace/tnn-lab/pam/round4/wild/w7/launder_signals.txt
w10:          /tmp/w10test ~/workspace/tnn-lab/pam/round4/wild/w10/w10_bundles.txt 1000
              /tmp/w10test ~/workspace/tnn-lab/pam/round4/wild/w10/w10_bundles.txt 500
w11:          /tmp/w11test ~/workspace/tnn-lab/pam/round4/wild/w11/w11_chains.txt
w12:          /tmp/w12test ~/workspace/tnn-lab/pam/round4/wild/w12/w12_stream.txt
              /tmp/w12test ~/workspace/tnn-lab/pam/round4/wild/w12/w12_attack.txt
python3 wN/score_wN.py <output> [<fixture>]   # exit 0
```

## WILD W13/W14/W15 + wildc (designs 16–23)

```
cd ~/workspace/tnn-lab/pam/round4/wild/build
$ZNC --no-zagd wildc.zag -o /tmp/wc/wildc_verify
TAPE=~/workspace/tnn-lab/pam/round4/wild/tape/wildc/wildc_tape.txt
PROBES=~/workspace/tnn-lab/pam/round4/wild/tape/wildc/wildc_probes.txt
C3=~/workspace/pam_round2/o1_delivery/case_o1.txt
/tmp/wc/wildc_verify <16..23> run $TAPE $PROBES $C3     # ×2 each; run1≡run2
cd ../w13 && $ZNC --no-zagd w13_lease.zag -o /tmp/wc/w13_verify
/tmp/wc/w13_verify ~/workspace/tnn-lab/pam/round4/wild/w13/w13_stream.txt
cd ../w14 && $ZNC --no-zagd w14.zag -o /tmp/wc/w14_verify
/tmp/wc/w14_verify ~/workspace/tnn-lab/pam/round3/m1/m1_cases.txt
cd ../w15 && $ZNC --no-zagd w15_quarantine.zag -o /tmp/wc/w15_verify
/tmp/wc/w15_verify ~/workspace/tnn-lab/pam/round4/wild/w15/w15_stream.txt
```

## CU track

```
cd ~/workspace/tnn-lab/pam/round4/cu
$ZNC --no-zagd cu_pam.zag -o /tmp/cu/cu_pam
$ZNC --no-zagd cu_query.zag -o /tmp/cu/cu_query
for N in 1 2; do /tmp/cu/cu_pam c cu_tape.txt > /tmp/cu/c_run$N.txt; done
for N in 1 2; do /tmp/cu/cu_pam u cu_tape.txt > /tmp/cu/u_run$N.txt; done
for N in 1 2; do /tmp/cu/cu_pam h cu_tape.txt > /tmp/cu/h_run$N.txt; done
/tmp/cu/cu_query c_run1.txt cu_questions.txt > /tmp/cu/qc_run1.txt   # ×2
/tmp/cu/cu_query u_run1.txt cu_questions.txt > /tmp/cu/qu_run1.txt   # ×2
/tmp/cu/cu_query h_run1.txt cu_questions.txt > /tmp/cu/qh_run1.txt   # ×2
python3 score_cu.py     # all KB-CU bars
python3 probe_grok.py   # P-UNC / P-CON / P-HYB reconciliation
```
