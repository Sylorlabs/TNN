# RUNLOG_RT_S

2026-09-24 ~13:00 PDT — RT-S crew start.
- Read GROK_OBJECTOR_R2.md in full (36b1d5fc2); extracted classes N/O/P + S*
  spec by script. Fetched committed driver sources from tnn-native-lab
  (b3536.zag @ 7a1a8422, file SHA-256 1602247d..., git blob bff9f8161e7f;
  R33 files blob-verified a6b440d2 / 5dd858fa).
- verify_facts.py: grok's 5 mechanism facts independently verified by script
  against 7a1a8422 — ALL-5-FACTS-VERIFIED (fact 2: c_stage2 commitment vacuous;
  fact 3: cstep low-32 only, label uncommitted, id unchecked; fact 5: the
  honest-mint × world-close × dirty-label cell untested).

2026-09-24 ~13:10 — PREREG_RT_S.md drafted, committed ALONE: `577829e3`.
(S* fixed pre-run; dual gate/harm reporting; kill ≥97/120; O-temporal binary
property kill; falsifiers ≤15/120; honest-loss ≤15%; 3× byte-identical;
scope fork frozen: C36J carve names identity only, post-hoc extension forbidden.)

2026-09-24 ~13:20 — build: gen_sstar.py extracts 35 mechanisms verbatim from
7a1a8422 (byte-slices, asserted present-once); sstar_new.zag = N/O/P/HONEST/
ArmT fixtures + S* scorer + main; znc build clean (one pre-existing analyzer
warning inside verbatim ledger_add). b3536_sstar.zag SHA-256
199e0fbbf3d5716234935be8f96c87faf58006e1f7e56dbfbe95cb83f79156c2.
Build committed BEFORE any run: `f1a80f52`.

2026-09-24 ~13:25 — battery: 3 runs, identical material hex
(0123456789abcdef×4), fresh ledger per run.
- run1/2/3 stdout byte-identical: SHA
  bf436a5abeff5e893970fad23a3adf13da365cdd470c4f535287fed20ccf5200
- N: gate 120/120, harm 120/120. O: gate 120/120, harm 120/120.
  OT arm-T 0/120; O_TEMPORAL_FAIL 120/120. P: gate 120/120, harm 120/120.
  HONEST 120/120 admit, 0/0/0 harm. Anchors: C35J 0, C36K 0, C36M S1=120/S2=0,
  C36J 120 carry — all at measured positions.

VERDICT: KILL (all three grok kill conditions fired). Evidence commit follows.
Backlog H-PAM-35/36 updated: TESTED-killed as the composition.
