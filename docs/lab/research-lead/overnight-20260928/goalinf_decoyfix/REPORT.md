# REPORT: Goalinf Decoy-Structure Repair (UNFROZEN variant)

Worker: Goalinf Decoy-Structure Repair Worker, RETRY-2. Date 2026-10-02.
Prereg: frozen at commit c1f0e5c30 before any implementation source existed.
Toolchain: pure Zag, pinned znc, safebin PATH. No python3/python in PATH
(guard verified at startup; see NAMECHECK.md Step 0).
Verdict: GOALINF-DECOYFIX-COMPLETE.

## What was done

Reproduced the Attack A kill from red-team 808ee293f in a minimal
fact/conflict store, then repaired the demotion gate to require
INDEPENDENT structure validation before a confident FACT may be
demoted or superseded. The single variable between the two binaries is
the gate; fact store, conflict detection, and observation-ingress
tagging are identical.

Repair gate (fixed variant), on conflict between confident FACT F
(conf >= 50) and challenger structure S:

* Provenance is DERIVED by the gate from the observation log
  (majority source tag over S.construction observations); structures
  cannot self-report provenance.
* circular = (S has zero external verification observations AND
  self_checks > 0) OR (all construction observations SELF-tagged).
* heldout_hits = correct predictions on held-out ENV observations not
  used in construction. Require >= 2.
* reliability = prior correct independent predictions for S.lineage,
  counted from the episode log. Require >= 3.
* Demote/supersede only if (not circular) AND (heldout_hits >= 2)
  AND (reliability >= 3). Otherwise WITHHOLD with reason bitmask
  1 = CIRCULAR, 2 = HELDOUT-INSUFFICIENT, 4 = RELIABILITY-INSUFFICIENT.
* Every supersede writes a restore record (prior claim, conf, ev,
  prov, challenger id); restore() reinstates the prior state exactly.
  Reversibility is a universal property, not a validation bypass.
* Weak facts (conf < 50) keep the pre-existing evidence-revision path.

## Kill bars (all frozen in PREREG.md before implementation)

| Bar | Result |
|---|---|
| KB1 ATTACK-A BLOCKED (fix_attacka) | PASS. F1 retained: conf 90, ev 12, claim 0, ACTIVE. EVT DEMOTE-WITHHELD fid 1 reason 7 (1+2+4). No demotion, no restore record. |
| KB1 sanity (vuln_attacka) | PASS. Kill reproduced: F1 DEMOTED, conf 0, EVT DEMOTED fid 1. Fixture genuinely attacks. |
| KB2 T-STALE RESOLVES (fix_tstale) | PASS. F4 superseded to claim 1, conf 70, ev 11, prov REVISED, with RESTORE-RECORD (prior 0/80/8/OBSERVED). restore() reinstated (0,80,8,OBSERVED,ACTIVE) exactly. |
| KB3 REGRESSION 5/5 (fix_regress) | PASS 5/5. R1 no-challenger query clean; R2 agreeing structure no-op; R3 weak fact revised without validation; R4 supersede+restore exact; R5 all-SELF circular structure (500 self-checks) withheld with CIRCULAR bit, F1 untouched. |
| KB4 DETERMINISM | PASS. 3 runs x 4 scenarios, sha256 identical within each scenario (12 runs). |

All binaries print RESULT,PASS on their self-checks; every CHECK line
shows actual == expected in outputs/.

## Output hashes (sha256, from outputs/sha256sums.txt)

* vuln_attacka (x3): 1cbff2ea0bc3036ebe7b3b0ea72d2e48880eb21584d0129bfc14ca218e93fd28
* fix_attacka (x3): d9c703376bd01ac1a731239989d836a43316a5299563b05f22d4e321fcd9418f
* fix_tstale (x3): cc11a59878d77735471e103b1a5f3f9873d9c968248b54d1cda1b803d6db2266
* fix_regress (x3): 3b1803ce9471dcf7aa0396980fc864e9afd3b9271223bdbd59347f2df278102a

## Files

* src/core.zag: emit helpers (single-buffer, one raw syscall), ig/is
  cells, event emitters, vulnerable gate, repaired gate, restore.
* src/scen_attacka.zag, src/scen_tstale.zag: fixtures A and B.
* src/main_vuln_attacka.zag, src/main_fix_attacka.zag,
  src/main_fix_tstale.zag, src/main_fix_regress.zag: scenario drivers
  with in-binary CHECK self-verification.
* bin/goalinf_vuln_attacka, bin/goalinf_fix_attacka,
  bin/goalinf_fix_tstale, bin/goalinf_fix_regress: compiled natives.
* outputs/*_r{1,2,3}.txt: raw stdout; outputs/sha256sums.txt.

## Honest scope and limits

* Provenance tagging ingress is trusted harness code; the tagging
  mechanism itself is not under test, only the gate that consumes tags.
* Earned reliability is derived from a fixed episode log; learning
  reliability over time is NOT implemented or claimed.
* No L3 or generality claim: this is a targeted repair of one
  red-team kill plus a regression battery. 0 modes, 0 bridges,
  0 handlers added. Paper untouched. Nothing pushed (commits local on
  tnn-native-lab only).
* One implementation bug was found and fixed during the build
  (obs table undersized for fixture slots; panic on first run);
  the fix was a table-size change only, no gate logic changed, and
  the prereg was untouched.

## Recommendation

The repair is validated against its frozen bars: Attack A is blocked
while legitimate T-STALE resolution and all five regression behaviors
hold, deterministically. The gate is a candidate for integration into
the goal-inference store, pending the usual promotion review (the
reliability-learning machinery remains future work).
