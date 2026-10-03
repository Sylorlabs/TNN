# exp2c bar table (machine-readable)

Columns: leg, design, corpus, order, then per type TR PA NO DP LK, then
n_2c_fail, frozen_fail.

```
leg,design,corpus,order,t1_TR,t1_PA,t1_NO,t1_DP,t1_LK,t2_TR,t2_PA,t2_NO,t2_DP,t2_LK,t3_TR,t3_PA,t3_NO,t3_DP,t3_LK,t4_TR,t4_PA,t4_NO,t4_DP,t4_LK,t5_TR,t5_PA,t5_NO,t5_DP,t5_LK,n_2c_fail,frozen_fail
base,none,none,none,20,20,20,9,9,20,20,16,10,10,20,20,20,9,3,20,20,20,10,10,20,20,20,9,9,1,sinc_lk_3
ab-a,alpha,AB-32,E->W,20,20,20,9,9,20,20,16,10,10,20,20,20,9,9,20,20,20,10,10,20,20,20,9,9,0,sinc_lk_3
ab-b,beta,AB-32,E->W,20,20,20,9,9,20,20,16,10,10,20,20,20,9,9,20,20,20,10,10,20,20,20,9,9,0,sinc_lk_3
ab-a-rev,alpha,AB-32,W->E,20,20,20,9,9,20,20,16,10,10,20,20,20,9,9,20,20,20,10,10,20,20,20,10,9,0,sinc_lk_3
abc-a,alpha,ABC-48,E->W,20,20,20,4,9,20,20,20,5,0,20,20,20,5,0,20,20,20,5,0,20,20,20,5,0,9,sinc_lk_3
abc-b,beta,ABC-48,E->W,20,20,20,9,9,20,20,16,10,10,20,20,20,9,10,20,20,20,10,10,20,20,20,9,9,0,sinc_lk_3
vol-a,alpha,96-novel,E->W,20,20,20,5,9,20,20,20,5,0,20,20,20,5,0,20,20,20,5,0,20,20,20,5,0,9,sinc_lk_3
vol-b,beta,96-novel,E->W,20,20,20,10,9,20,20,16,10,10,20,20,20,9,10,20,20,20,10,10,20,20,20,10,9,0,sinc_lk_3
vol2-a,alpha,48+48,E->W,20,20,20,10,9,20,20,16,10,10,20,20,20,8,10,20,20,20,9,10,20,20,20,8,9,2,sinc_lk_3
vol2-b,beta,48+48,E->W,20,20,20,10,9,20,20,16,10,10,20,20,20,8,10,20,20,20,9,10,20,20,20,8,9,2,sinc_lk_3
de-a,alpha,DE-32,E->W,20,20,20,9,9,20,20,16,10,10,20,20,20,9,3,20,20,20,10,10,20,20,20,10,9,1,sinc_lk_3
de-b,beta,DE-32,E->W,20,20,20,9,9,20,20,16,10,10,20,20,20,9,3,20,20,20,10,10,20,20,20,10,9,1,sinc_lk_3
```

Notes:
- Bar rule per type: DP>=9 and LK>=9 (2c_sinc_dp_N / 2c_sinc_lk_N checks).
- n_2c_fail counts failed 2c_* checks; frozen_fail is the single pre-existing
  frozen failure present in every leg (measured pre-2c).
- type-2 NO=16/20 is pre-existing in all legs including base (unchanged).
- vol-a/vol-b corpus "96-novel" is the deviant composition (disclosed in
  REPORT.md §6); vol2-a/vol2-b "48+48" is the prereg-§6.2-compliant composition.
