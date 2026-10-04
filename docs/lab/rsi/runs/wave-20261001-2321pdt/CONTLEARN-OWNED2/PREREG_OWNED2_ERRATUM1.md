# ERRATUM-1 to PREREG_OWNED2 (transparent amendment, re-freeze)

Date: 2026-10-02. Lane: CONTLEARN-OWNED2. Wave: wave-20261001-2321pdt.
Amends: PREREG_OWNED2.md frozen at commit ffd31dbb3.
Status: RE-FROZEN by this commit. No implementation of the amended freeze
exists before this commit.

## The inconsistency

PREREG_OWNED2 section 4 labels STORE as "(30 events)" and the full script
as "(104 events)", and K1c expects "audited count 104 per run". But the
same section gives the exact, authoritative tuple loops:

- STORE: 6 concept-link TEACH + 6 anchor-link TEACH + 6 integrate MQUERY
  + 6 family-E TEACH = 24 events, not 30.
- INTERFERE-1: 30. REUSE: 12. INTERFERE-2: 20. DELAYED: 12.
- Exact total: 24 + 30 + 12 + 20 + 12 = 98 events, not 104.

The summary labels (30, 104) are arithmetic errors carried over from the
adopted phase-1 design. The exact tuple loops are unambiguous and are the
authoritative frozen script.

## Correction (the only change)

- Section 4: "STORE (30 events)" reads "STORE (24 events)";
  "Full script (104 events)" reads "Full script (98 events)".
- Section 6 K1c: "expected audited count 104 per run" reads
  "expected audited count 98 per run".
- The fixture driver audit constant changes 104 to 98 to match.

Nothing else changes: no tuple added, removed, or reordered; no oracle
definition altered; no CO/K bar threshold altered; the frozen decision
rule is untouched. The 98-event tuple script executed by the pilot runs is
byte-identical to the script the official runs will execute.

## Pilot runs (disclosed, voided as official evidence)

Six pilot processes (3 TREAT, 3 CONTROL) were executed under the unamended
freeze before this erratum was noticed. They executed the exact frozen
98-event tuple script; their only defect is the audit-label mismatch
(transcripts print "AUDIT_FAIL count=98 want=104", exit code 1 on the
audit check alone). Their scientific content is disclosed, not hidden:
3/3 byte-identical per mode; TREAT STORE_OK 0/6, REUSE_OK 6/12,
SANITY_E 6/6, DELAYED_OK 6/12, MAPC 0, UNCERT 18; CONTROL STORE_OK 6/6,
REUSE_OK 12/12, SANITY_E 6/6, DELAYED_OK 12/12, MAPC 6, UNCERT 0.
They are VOID as verdict evidence because the freeze they ran under was
internally inconsistent. The verdict rests solely on the six official
runs executed after this re-freeze.

## Consequences for the governance bars

- K0: the K0 anchor remains ffd31dbb3 (original freeze); this erratum is a
  transparent amendment strictly before any official implementation run.
  merge-base ancestry is re-verified before the verdict.
- K1a: six official learner processes (2 binaries x 3 reps) under the
  amended freeze; the six pilot processes are disclosed above and do not
  count toward the official six.
- K1b: the driver rebuild (audit constant only) is performed under a fresh
  znc invocation log; the official log holds exactly 2 entries (one per
  binary) before the official runs and gains 0 during them. The two pilot
  builds are recorded in the superseded pilot log, disclosed here.
- K1c: expected audited count 98 per run; official transcripts must print
  AUDIT_PASS.
- All other bars (CO-1..CO-5, K2, K3, K6) are unchanged.
