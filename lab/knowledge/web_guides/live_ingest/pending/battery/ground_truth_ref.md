# REFUTE ground truth (4 cases) -- kill bar P3 (demote limb)

Setup (fresh state dir):
1. `kbpend` the 4 `claim.txt` lines in ref-01..ref-04 order
   -> stdout `PENDING|HELD|1` ... `PENDING|HELD|4`, exit 0.
2. For i in 1..4: `kbrefute <i> ref/ref-0<i>/p3.txt <state>` -> exit 0.

Expected per case ref-0i (claim C_i, evidence host EH_i, evidence title ET_i):
- `REJ|<r>|<C_i>|CONTRADICTED:<EH_i>:<ET_i>` appended to rejections.txt
  (r continues the rejection seq counter)
- `RESOLVE|<i>|REJ|CONTRADICTED|<detail>` appended to resolutions.txt,
  where <detail> carries `<EH_i>:<ET_i>`
- the claim is NEVER installed: no `KB|` line carries C_i.

The 4 evidence (EH_i : ET_i) pairs and exact REJ reasons:
1. measure-review.example : Millau Viaduct height check
   -> `CONTRADICTED:measure-review.example:Millau Viaduct height check`
2. height-audit.example : Tokyo Skytree height audit
   -> `CONTRADICTED:height-audit.example:Tokyo Skytree height audit`
3. hull-survey.example : Ever Given length survey
   -> `CONTRADICTED:hull-survey.example:Ever Given length survey`
4. capacity-check.example : Rungrado capacity check
   -> `CONTRADICTED:capacity-check.example:Rungrado capacity check`

Why each kbrefute must succeed (prereg S5c): the p3 page parses (1); its
best sentence CONTRADICT-binds the claim -- token overlap >= 2/3, >= 1
digit, digits differ (2, verified by verify_battery.py).

Kill bar P3: 4/4 demote with reason. Any shortfall = FAIL.
