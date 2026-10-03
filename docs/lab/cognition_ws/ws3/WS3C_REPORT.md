# WS3-C report — harder mixed-evidence / poison attacks on the popularity retune

Date: 2026-09-24. Prereg: `PREREG_WS3C.md` (frozen before runs, committed
`93dba9f6e56e54df128ce5eda14890003e195cef` on tnn-native-lab).
Module under test: `src/sense_after.zag` (WS3-A retune, unchanged).
Scorer: `src/score_popbias_c.py`, exit 0. All runs pure Zag, zero RNG,
3/3 byte-identical per arm (CK7), zero-RNG grep gate over src/ (CK8).

## Verdict: all kill bars CK1-CK8 HOLD

No new family breaks the retune. The one install of a falsehood in the whole
battery is P5, the preregistered trust-boundary case (driver-attested
verified=1 with a bogus warrant; V==1, satisfies CK1; see §5).

## Per-family before/after tables (AFTER arm; CONTROL identical modulo nudge)

### P — poison + popularity (majority is both popular AND poisoned)

| fid | BEFORE (bug) | AFTER | CONTROL |
|---|---|---|---|
| P1 3-dom poison, no contra | D1 / INSTALL | D1 N2 F52 / refused | D1 N0 F50 / refused |
| P2 5-dom poison + 1 live truth | D6 / INSTALL | D2 N0 / refused | D2 / refused |
| P3a 4-dom poison | D1 / INSTALL | D1 N3 F53 / refused | D1 / refused |
| P3b + installed truth@80 | D1 / refused | D2 N0 / refused | D2 / refused |
| P4 5-dom poison + installed truth@30 | D1 / INSTALL | D1 N4 F54 / refused | D1 / refused |
| P5 poison + driver warrant "POPULAR-CONSENSUS" | D1 / INSTALL | D1 N2 F52 / **INSTALL V=1** | D1 / INSTALL V=1 |

Findings: the evidence gate holds when poison arrives wearing popularity
(P2: 5 poisoned domains + 1 live truth → WITHHOLD, nudge 0; P3b: installed
truth reverses the poisoned majority, no residue). P4 pins the designed
threshold: a conf-30 contradiction does not fire the gate (bend persists at
N4/F54) but install stays impossible. P5 is the documented trust boundary
(§5).

### S — sleeper / reversal

| fid | BEFORE (bug) | AFTER | CONTROL |
|---|---|---|---|
| S1a 5-dom popular claim | D1 / INSTALL | D1 N4 F54 / refused | D1 / refused |
| S1b + installed contra@80 (reversed) | D1 / refused | D2 N0 / refused | D2 / refused |
| S2a 1v1 split | D2 / refused | D2 N0 / refused | D2 / refused |
| S2b 5v1 (one persistent contra) | D6 / INSTALL | D2 N0 / refused | D2 / refused |
| S3a lonely truth + WORLD-SETTLE | D2 / refused | D2 / **INSTALL V=1** S=Quince | D2 / INSTALL V=1 |
| S3b + 5-dom popular lie | D6 / INSTALL lie | D2 N0 / refused, S=Quince | D2 / refused |
| S4a override-install lie@80 | D2 / INSTALL V=1 | D2 / INSTALL V=1 S=Yarrow | D2 / INSTALL V=1 |
| S4b + 5-dom popular truth | D1 / refused | D2 N0 / refused, S=Yarrow | D2 / refused |
| S5a 3v1 | D6 / INSTALL | D2 N0 / refused | D2 / refused |
| S5b 4-dom unanimous (fresh) | D1 / INSTALL | D1 N3 F53 / refused | D1 / refused |

Findings: popularity leaves no residue after reversal (S1b nudge exactly 0).
A 5:1 majority with one persistent contradictor never resolves by popularity
(S2b). A warranted installed truth survives a 5-domain popular reversal
(S3b: stored value still "Quince"; BEFORE installs the lie). Symmetric cost:
an installed lie blocks a 5-domain popular truth (S4b: WITHHOLD) — the gate
is truth-blind by design; only deliberate agency (override) can correct it.
Gate release works: S5b returns to the bend once contradiction genuinely
resolves.

### L — mixed-evidence ladders (where the nudge bends vs breaks)

| fid | BEFORE (bug) | AFTER |
|---|---|---|
| L1 2:1 live (2 pop + 1 contra) | D6 / INSTALL | D2 N0 / refused |
| L2 5:1 live | D6 / INSTALL | D2 N0 / refused |
| L3 4:2 live | D6 / INSTALL | D2 N0 / refused |
| L3b 10:1 input (stored 5:1, §2 cap) | D6 / INSTALL | D2 N0 / refused |
| L4 5 pop + installed contra@49 | D1 / INSTALL | D1 N4 F54 / refused |
| L5 5 pop + installed contra@50 | D1 / refused | D2 N0 / refused |
| L6 5 pop + installed contra@51 | D1 / refused | D2 N0 / refused |
| L7 7 unanimous (6 stored) | D1 / INSTALL | D1 N5 F55 / refused |

Findings: the live gate is ratio-insensitive — 2:1, 5:1, and 10:1-input all
WITHHOLD with nudge 0 (any single live contradictor zeroes all popularity).
The installed-contradiction threshold is exactly 50: conf 49 bends (exact
N4/F54, proving the bend is computed not suppressed), conf 50 and 51 break to
WITHHOLD. Nudge cap never exceeded: L7 saturates at N5/F55 at the 6-slot
storage boundary. (CONTROL column omitted: identical verdicts, N0/F50-or-0.)

### SP — sockpuppet popularity (distinct domains, one operator)

| fid | BEFORE (bug) | AFTER |
|---|---|---|
| SP1 5 sockpuppets unanimous | D1 / INSTALL | D1 N4 F54 / refused |
| SP2 5 socks + 1 independent contra | D6 / INSTALL | D2 N0 / refused |
| SP3 4 socks + installed truth@80 | D1 / refused | D2 N0 / refused |
| SP4 3 socks vs 3 genuine (3v3) | D6 / INSTALL (socks win) | D2 N0 / refused |

Findings: the wire is sockpuppet-blind by design (no domain-independence
machinery; §2) — the retune's answer is the structural bound: at most +4 conf
annotation, never an install. One real contradictor beats five sockpuppets
(SP2). The 3v3 tie that BEFORE settles for the sockpuppets (first-seen order)
stays WITHHOLD.

## MW sibling port (report only, no kill bars)

`src/mw_after.zag` = frozen `mw_sense.zag` + 2 surgical rule-block edits
(MAJORITY → MAJORITY_RETIRED, CORROB → CORROB_HELD; RECENCY/TIE/INSUFFICIENT
untouched). 8 synthetic cases, frozen vs port, 3/3 byte-identical:

| case | FROZEN | PORT | delta |
|---|---|---|---|
| MW1 4v1 | CONVERGE/Alpha/MAJORITY | WITHHOLD/-/MAJORITY_RETIRED | changed |
| MW2 6v1 | CONVERGE/Alpha/MAJORITY | WITHHOLD/-/MAJORITY_RETIRED | changed |
| MW3 3v0 | CONVERGE/Alpha/MAJORITY | WITHHOLD/-/MAJORITY_RETIRED | changed |
| MW4 2v0 | CONVERGE/Alpha/CORROB | WITHHOLD/-/CORROB_HELD | changed |
| MW5 2v2 | WITHHOLD/-/TIE | WITHHOLD/-/TIE | none |
| MW6 1v0 | WITHHOLD/-/INSUFFICIENT | WITHHOLD/-/INSUFFICIENT | none |
| MW7 recency | CONVERGE/Gamma/RECENCY | CONVERGE/Gamma/RECENCY | none |
| MW8 3v2 | WITHHOLD/-/TIE | WITHHOLD/-/TIE | none |

Port assessment: the retune principle ports cleanly (2 edits, no regressions
in RECENCY/TIE/INSUFFICIENT). Cost: 4/8 frozen CONVERGE verdicts become
WITHHOLD. The CORROB change (MW4) is the lossy one: mw has no PROVISIONAL
verdict, so near-unanimous agreement can no longer be recorded as a
non-settling outcome — it must withhold outright. Open for Micah: whether the
sibling wants a PROVISIONAL-equivalent middle verdict added, or accepts the
stricter withhold. (Note: MW3's frozen rule is MAJORITY, not CORROB — with
runner-up count 0, bc=3 ≥ 2×0, MAJORITY fires first in rule order.)

## Residuals / open items

1. **Warrant authentication (P5).** The wire authenticates nothing; a caller
   asserting verified=1 installs anything, and the only defense is the ledger
   audit trail (op 73 records "W:POPULAR-CONSENSUS"). If the install path ever
   faces untrusted callers, warrant authentication becomes load-bearing. Today
   the caller is the trainer/driver by design (R5).
2. **Sub-50 installed contradictions (P4/L4).** A conf-49 installed belief
   buys the popular claim up to +5 conf annotation. Bounded, never an
   install, but a poisoner who can seed low-conf installed beliefs gets the
   bend. Threshold is preregistered; flagging the edge.
3. **Sockpuppet detection.** Out of scope for this retune by preregistered
   design (§2); belongs to ingestion provenance. The structural bound held on
   all SP fixtures.
4. **6-slot storage cap.** 10:1 input collapses to 5:1 stored (L3b); results
   past 6 are ledgered but invisible to decide. Pre-existing mechanism limit,
   not a retune finding.
5. **MW CORROB loss.** Needs Micah's word if the sibling is ever retuned
   (PROVISIONAL-equivalent verdict vs stricter withhold).

## Artifacts

- Prereg: `PREREG_WS3C.md` (committed 93dba9f6)
- Generators: `src/gen_drivers_c.py`, `src/gen_mw_port.py`
- Port module: `src/mw_after.zag` (frozen mw_sense.zag + 2 rule blocks)
- Scorer: `src/score_popbias_c.py` (exit 0, all CK1-CK8 HOLD)
- Fixture table: `shared/POPBIAS_PROBES/probes_table_c.json`
- Run logs: `runs_c/` (15 logs, sha256 in §6)

## Run SHAs (CK7)

- before: `c2d0a37236ef034a20c32b7b31ab1fb1295acadfbcd31afe5a3262ab332dc7f0`
- after: `f8156da5ce2fc4fda75268ff8888f2e30a4faeee49d227b3405b67e0d60587c4`
- control: `030dea93c3f2b60dc9b6040c24a5af23f99ea9e2d562081a7db10354f3c7e129`
- mw_frozen: `24c4e4df1c9f1e80f1db318a9919149140ca6d9d8729b2ba61b08aed9e0c539e`
- mw_port: `a62a14a17b78dbc9e125019c287b542d7107a70151d5849627eecf30b3d52eba`

(r1 SHAs shown; r2/r3 byte-identical per CK7)

Commits on tnn-native-lab: prereg `93dba9f6`; batteries + evidence SHAs below.
