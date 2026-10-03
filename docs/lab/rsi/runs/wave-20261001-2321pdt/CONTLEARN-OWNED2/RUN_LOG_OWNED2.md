# RUN_LOG_OWNED2: machinery-disabled integration discrimination

Wave: wave-20261001-2321pdt. Lane: CONTLEARN-OWNED2. Date: 2026-10-02.
Frozen prereg: PREREG_OWNED2.md (commit ffd31dbb3).
Transparent amendment: PREREG_OWNED2_ERRATUM1.md (commit 78d8c9e54):
the frozen script is 98 events (STORE is 24, not 30, per the exact tuple
loops); K1c expects 98. No tuple, oracle, bar, or decision-rule change.

## K0 commit order

- Prereg frozen alone: ffd31dbb3 (NAMECHECK.md + PREREG_OWNED2.md).
  Note: that commit briefly swept in two already-staged files from the
  RT-SENSE lane (staged by another worker, unrelated to this lane); the
  tree state was verified correct afterward and no implementation file of
  this lane existed at or before that commit.
- Erratum re-freeze: 78d8c9e54 (ERRATUM-1 alone), strictly after the
  prereg, strictly before any official build or run.
- `git merge-base --is-ancestor ffd31dbb3 HEAD` true;
  `git merge-base --is-ancestor 78d8c9e54 HEAD` true (verified before the
  verdict; the implementation commit is a strict descendant of both).

## K2a frozen ISA boundary (three checks)

1. Before implementation: SHA-256
   a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd.
2. Immediately before the official builds: same hash.
3. After all runs: same hash, and `git hash-object` gives blob
   b226b223cb3ee0be742af673653fb8ea8605f281, the exact blob recorded in
   commit f4de7ff46.
Note: the frozen path is currently untracked at HEAD (a side effect of
the LANE-AUDIT repair sweep that rewrote recent history; the working-tree
bytes are verified identical to the frozen blob). This worker never wrote
to the frozen path; it was read only.

## Sources and builds

- ow_core_control.zag: byte copy of the recorded nomain derivation
  (extracted via git show from dfcd3caf), SHA-256
  26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d.
- ow_core_disabled.zag: mechanical derivation removing exactly the two
  machinery call blocks (6 lines) from ev_query, SHA-256
  94b405fc8acce8c2de120d972797052a6468e415e874b549d03c3eecb2fe8407.
  CO-5a diff hash (control vs disabled):
  3f385dc56367337f352da35ffd1b29bde0b7a124c68a42a57d717ad043cfaa75.
- ow_driver.zag (official, audit constant 98): SHA-256
  e591028039f7c0d2ec0a2fdf2c47f9b6c38119697996ff0588d6233fadc7e465.
- Combined inputs: control
  51dbb6e0e2f272fcefc7c1290c24a05392ba2cf834290bdbd22bee0c8192e540;
  disabled
  6579d84613d11680c63150142a567dd118326c2600bdf47916f4b6c62783fd45.
- Binaries (official): ow_driver_treat
  d969faa29232ad3601d87ffeded3a01536c95414f803e3b91524dbef633f4039;
  ow_driver_control
  769379cc556fc0a4d4d15ac806b7646c1dc7d264a60a8223ec873e05fa0883c5.
  Both builds succeeded with analyzer warnings only (the same warning
  class as the prior wave: discarded non-void return in the driver).

## K1b: exactly two logged builds

Fresh znc_invocations_ow.log holds exactly 2 entries (one per binary)
before the official runs; 0 new entries during the 6 runs
(harness_ow.log: znc_invocations_during_runs=2). The two pilot builds are
recorded in the superseded znc_invocations_ow_PILOT.log (disclosed in the
erratum).

## K3 no regression

Committed 2321pdt lo_driver binary extracted read-only from dfcd3caf
(hash 35f78f8c3eb6fce9dec2262875f8cb1cb0efef1f7cffa824bdfaebb9a7a0ac4a),
re-run 3x in TREAT mode: stdout SHA-256
1ff527fa97b36da25fd8163299773680e53ae47fba521fc2227b0bf7c39394d9
on all 3 reps (matches the recorded 2321pdt value), rc=0, 0 stderr bytes.
K3 PASS.

## K1a/K1c/K6: the six official runs

harness_ow.log: 6 spawns total (3 TREAT + 3 CONTROL), one process per full
98-event run, empty argv, empty env (bash -c 'exec -c'); all rc=0;
pid_leak_check=0 (no PID in any transcript); all 6 stderr files 0 bytes.

CO-3 determinism: 3/3 byte-identical transcripts per binary.
TREAT: 27676a22ea1043376453022063b21e85376084f6a19aa1ddb9959f0c7e387c57.
CONTROL: 8454f6dbef98744acb8793e3cba279da72364ec76b7527c56e36213a8ad10aac.
FNV-1a arena checksums equal across reps (TREAT -677949997;
CONTROL -1785692917). No PID, timestamps, or paths in transcripts
(grep-clean). K1c: AUDIT_PASS (98/98) on all 6 runs; every tuple flowed
through the ow_event / ow_mquery choke points with the frozen masked-query
parameters expected=-2, flags=1; PHASE markers never reached cognition.

Pilot runs (voided, disclosed): 6 processes under the unamended freeze;
transcripts pilot_transcript_{TREAT,CONTROL}_r{1,2,3}.txt
(TREAT c72ecb6f198f4914b54788707e91885af9c722c2eed668ee69708bb497b6d106;
CONTROL 0514d9a4581b3e6ea42425d7786f26a677f1d5608eacca5a0267a83c9f59b5b1),
3/3 byte-identical per mode, rc=1 on the audit-label check only. Official
transcripts differ from pilot transcripts in exactly one line
(AUDIT_FAIL count=98 want=104 -> AUDIT_PASS); all scientific content is
byte-identical across the freeze amendment.

## Per-bar numbers (official runs)

TREAT (machinery-disabled variant):
- CENSUS STORE: MAPC=0 DEPC=6 UNC=6 GUIDEC=6 N1=24 Eall=41
- STORE_OK 0/6 (all six D integrate queries returned -2, true miss)
- REUSE: D_HIT 0/6 D_MISS 6/6 E_OK 6/6;
  CENSUS REUSE: MAPC=0 DEPC=12 UNC=12 GUIDEC=12 N1=60 Eall=89
- DELAYED: D_HIT 0/6 D_MISS 6/6 E_OK 6/6;
  CENSUS DELAYED: MAPC=0 DEPC=18 UNC=18 GUIDEC=18 N1=86 Eall=133
- STORE_OK_SUM 0/6; REUSE_OK_SUM 6/12; SANITY_E_SUM 6/6;
  DELAYED_OK_SUM 6/12; UNCERT 18.

CONTROL (unmodified frozen core):
- CENSUS STORE: MAPC=6 DEPC=24 UNC=0 GUIDEC=0 N1=24 Eall=83
- STORE_OK 6/6
- REUSE: D_HIT 6/6 D_MISS 0/6 E_OK 6/6;
  CENSUS REUSE: MAPC=6 DEPC=24 UNC=0 GUIDEC=0 N1=54 Eall=113
- DELAYED: D_HIT 6/6 D_MISS 0/6 E_OK 6/6;
  CENSUS DELAYED: MAPC=6 DEPC=24 UNC=0 GUIDEC=0 N1=74 Eall=145
- STORE_OK_SUM 6/6; REUSE_OK_SUM 12/12; SANITY_E_SUM 6/6;
  DELAYED_OK_SUM 12/12; UNCERT 0.

CO-5 absence checks: (a) diff shows exactly the six deleted lines, nothing
else; (b) every call site of mp_run/t2_trial/t2_try_verify/promote_graph/
bootstrap_miss in the variant lies inside one of those five functions own
bodies (verified by caller analysis); no path from the event interface can
reach them; (c) TREAT MAPC=0 at STORE, REUSE, and DELAYED censuses: zero
new MAP nodes on any of the 18 family-D masked probes.

## Verdict

MACHINERY-DEPENDENT. See VERDICT_OWNED2.md for the per-bar table and the
root-cause analysis.
