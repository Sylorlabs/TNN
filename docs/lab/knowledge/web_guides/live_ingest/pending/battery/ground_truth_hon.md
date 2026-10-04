# HON ground truth (8 cases) -- kill bar P3 (promote limb)

Setup (fresh state dir):
1. `kbpend` the 8 `claim.txt` lines in hon-01..hon-08 order
   -> stdout `PENDING|HELD|1` ... `PENDING|HELD|8`, exit 0.
2. For i in 1..8: `kbcorroborate <i> hon/hon-0<i>/p2.txt <state>` -> exit 0.

Expected per case hon-0i (claim C_i, p2 host H_i, p2 title T_i):
- `RESOLVE|<i>|KB|CORROBORATED|<H_i>:<T_i>` appended to resolutions.txt
- `KB|<k>|<C_i>` appended to knowledge.txt (k continues the KB seq counter)
- pending seq <i> leaves the active pending set; its seq is never reused.

The 8 (H_i, T_i) pairs:
1. signalarchive.example : Golden Gate Bridge span notes
2. maritime-ledger.example : Jeddah Light height notes
3. transit-record.example : Channel Tunnel length notes
4. optics-journal.example : Gran Telescopio Canarias mirror notes
5. reading-room.example : Library of Congress holdings notes
6. roman-ways.example : Pont du Gard height notes
7. north-sea-wind.example : Vestas V164 blade length notes
8. dam-register.example : Hoover Dam height notes

Why each kbcorroborate must succeed (prereg S5a): seq is pending (1); the
page parses with TITLE and HOST lines (2); the p2 sentence AGREE-binds the
claim -- token overlap >= 2/3, digits equal (3, verified by
verify_battery.py); provenance is DELIBERATE, which records no host, so the
host-independence requirement holds (4); the p2 sentence AGREE-binds no
other pending claim -- the 8 topics are pairwise bind < 2/3 (5, verified by
verify_battery.py).

Kill bar P3: 8/8 promote. Any shortfall = FAIL.
