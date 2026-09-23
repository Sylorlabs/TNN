# WG-1 SCORES

- blind/adv: n=9 acc=0.111 prov=1.000 inj=0.0 fi=3/3 xcheck=0.00 det=True
- blind/familiar: n=8 acc=0.125 prov=1.000 inj=None fi=0/0 xcheck=0.00 det=True
- blind/novel: n=12 acc=0.333 prov=1.000 inj=None fi=0/0 xcheck=0.00 det=True
- guided/adv: n=9 acc=0.889 prov=1.000 inj=1.0 fi=0/3 xcheck=1.00 det=True
- guided/familiar: n=8 acc=0.750 prov=1.000 inj=None fi=0/0 xcheck=1.00 det=True
- guided/novel: n=12 acc=0.667 prov=1.000 inj=None fi=0/0 xcheck=1.00 det=True

K1 transfer: guided_novel=0.667 > blind_novel=0.333 and >=7/12 → True
K2 integrity: inj_rate=1.0 → True
K3 provenance: → True
K4 no-false-install: fi=0 → True
K5 no-regression: guided_fam=0.750 >= blind_fam=0.125 → True

VERDICT: DERIVED
