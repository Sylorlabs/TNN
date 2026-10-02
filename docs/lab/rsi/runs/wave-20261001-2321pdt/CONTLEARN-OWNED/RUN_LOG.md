# RUN_LOG: CONTLEARN-OWNED machinery-disabled discrimination

Wave: wave-20261001-2321pdt. Lane: CONTLEARN-OWNED. Date: 2026-10-02.
Implements PREREG_OWNED.md as amended (Amendment A1, re-freeze d2fc968f4).
Binaries: `ow_treat` (machinery-disabled variant)
(`6b65e6a62e56f43feb14e1afa45309c9512759ad7ba471a24d68b6b0502c2f71`),
`ow_control` (unmodified frozen core)
(`58f2f9f2d3855c782106d41266bc30acea29870ea0cf1f1b08282ef78954d400`).

## Amendment A1 pilot runs (discarded, not counted)

A first pilot build/run cycle executed the exact frozen tuple script but
with the audit constant at 104 instead of the correct 98 (STORE is 24
events, not 30; total 98). All 6 pilot runs printed
`AUDIT_FAIL count=98 want=104` and exited 1. The tuple script was
byte-exact to the prereg; only the bookkeeping constant was wrong. Per the
prereg discipline the pilot runs were discarded, the prereg was amended
transparently (Amendment A1, no tuple/bar/decision change), the audit
constant was fixed, both binaries were rebuilt, and the runs below are
fresh runs against the amended freeze. Pilot transcripts were overwritten
by the fresh runs.

## Runs (K1a/K1c/CO-3)

Harness `run.sh`: 2 binaries x 3 reps = 6 learner processes. Each run
launched via `printf '%s' "$mode" | bash -c 'exec -c ./ow_<bin>'` (empty
argv, empty env). harness.log records: 6 spawns total (3 ow_treat, 3
ow_control), all exit 0, zero stderr bytes on all 6 runs,
pid_leak_check=0 (no PID appears in any transcript),
znc_invocations.log holds exactly 2 entries throughout (0 new during runs).

## CO-3 determinism

- TREAT stdout SHA-256 (3/3 identical):
  `60a8b778a2b9ddaf629101912f20f45e7b7373ac0b09090b80a7dbb4705819ca`
- CONTROL stdout SHA-256 (3/3 identical):
  `54b3cd30d3a7ac06114ba128d488b2e9406056ed466d8f8ed3bf55eef003bcc1`
- FNV-1a arena checksums equal across reps: TREAT -677949997, CONTROL
  -1785692917. Exit code 0 on all 6 runs. Zero stderr bytes. No PID,
  timestamps, or paths in transcripts.

## K3 no-regression (2321pdt battery, read-only re-run)

Committed 2321pdt binary `lo_driver`
(`35f78f8c3eb6fce9dec2262875f8cb1cb0efef1f7cffa824bdfaebb9a7a0ac4a`,
extracted read-only from the recorded commit) re-run 3x in TREAT mode,
read-only. Stdout SHA-256 on all 3 reps:
`1ff527fa97b36da25fd8163299773680e53ae47fba521fc2227b0bf7c39394d9`,
matching the recorded 2321pdt value.

## Results per bar (identical on all 3 reps per binary)

TREAT (machinery-disabled variant):

- OW_STOREOK 0/6. Zero MAPs promoted; all 6 family-D masked probes took
  the true miss path (returned -2).
- REUSE: OW_PROBE_OK 6/12 (only the 6 family-E standing probes),
  OW_DHIT 0/6, OW_DMISS 6/6, OW_EOK 6/6.
- DELAYED: OW_PROBE_OK 6/12, OW_DHIT 0/6, OW_DMISS 6/6, OW_EOK 6/6.
- OW_SANITY_E 6/6: standing retrieval intact in the variant.
- OW_BAR_MISS printed (expected: CO-1 bar not met).
- Mechanism census (CO-2 evidence):
  - STORE: MAPC=0 DEPC=6 UNC=6 GUIDEC=6 N1=24 N20=0 N30=6 E1=6 Eall=41
  - REUSE: MAPC=0 DEPC=12 UNC=12 GUIDEC=12 N1=60 N20=0 N30=12 E1=12
    Eall=89
  - DELAYED: MAPC=0 DEPC=18 UNC=18 GUIDEC=18 N1=86 N20=0 N30=18 E1=18
    Eall=133
  - The only DEP edges are guide-to-UNCERTAINTY edges written by
    `miss_inquire` (one per miss); zero MAP nodes at every phase; the
    learner-side response to the unintegrable queries is UNCERTAINTY
    reification plus guide construction into POLICY_ROOT, nothing more.
  - Final alive node count 86, far below the 1024 cap: no eviction; the
    missing structures are a capability gap, not capacity.

CONTROL (unmodified frozen core):

- OW_STOREOK 6/6. All 6 family-D masked probes promoted MAP(9501+i,702)
  with alive DEP edges to fact(9001+i,501,9101+i); answers 9101+i.
- REUSE: OW_PROBE_OK 12/12, OW_DHIT 6/6, OW_DMISS 0/6, OW_EOK 6/6.
- DELAYED: OW_PROBE_OK 12/12, OW_DHIT 6/6, OW_DMISS 0/6, OW_EOK 6/6.
- OW_SANITY_E 6/6.
- Mechanism census:
  - STORE: MAPC=6 DEPC=24 UNC=0 GUIDEC=0 N1=24 N20=6 N30=0 E1=24 Eall=83
  - REUSE: MAPC=6 DEPC=24 UNC=0 GUIDEC=0 N1=54 Eall=113
  - DELAYED: MAPC=6 DEPC=24 UNC=0 GUIDEC=0 N1=74 Eall=145
  - DEPC=24 accounting (verified against the source): per promoted chain,
    `t2_asm_chain` writes 2 DEP edges (one per constructed step, frozen
    file line 371) and `promote_graph` writes 2 DEP edges from the MAP to
    the licensing facts (line 540): 4 x 6 = 24. Every DEP edge in the
    control run traces to the trial/promotion machinery; zero UNCERT
    nodes, zero guides.

## CO-5 machinery absence (verified before and with the runs)

- (a) Source diff variant-vs-control shows exactly the two removed
  `ev_query` call blocks (six lines) and nothing else; variant-diff
  SHA-256 `3f385dc56367337f352da35ffd1b29bde0b7a124c68a42a57d717ad043cfaa75`.
- (b) Grep: no event-interface function contains any call to `mp_run`,
  `t2_trial`, `t2_try_verify`, `promote_graph`, or `bootstrap_miss`;
  the only remaining call sites sit inside the dead machinery cluster
  itself.
- (c) Behavioral: zero MAP nodes written on any of the 18 family-D masked
  probes across the TREAT runs (STORE 6 + REUSE 6 + DELAYED 6).

## K0 commit order

Prereg frozen alone at 3e837ff5c; Amendment A1 re-frozen alone at
d2fc968f4. `git merge-base --is-ancestor d2fc968f4 HEAD` true at verdict
time. All implementation and result files first appear strictly after the
re-freeze commit.
