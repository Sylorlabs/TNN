# JUDGE'S RULING: wave-20260924-0521pdt debate group

Judge ruling on motions M1 through M4. Numbers below were re-verified
from committed sources by the judge before ruling. The owner's five
pending governance decisions (S7 strike, MD-SSD-1 keep-with-UNVERIFIABLE
vs re-freeze, S11 pull, S11-AUD pull, C12 queue) are his and are not
ruled on here.

## M1. Second judgment path part C

**Ruling: DISCARD stands. Tag: [VOID].** The red-team's [NEW] tag is
overturned on cited evidence (below). The verdict outcome is unchanged:
the frozen mapping mandates DISCARD on any SP-B1 miss, and the miss is
uncontested arithmetic.

Measured bars (re-verified from secondpath/evidence/summary_run2.txt):
SP-B1 1891 bp (7 false / 37 installs) vs frozen bar strictly below
7/38 (1842 bp): FAIL. PB-IND PASS (static grep clean). PB-DET 3/3
identical PASS. PB-AGREE 83 bp (1/120) vs 500 bp PASS. PA-B1 0 PASS.
SP-B2 8486 vs >= 8486 PASS (exact boundary). SP-B3 3/3 identical PASS.
SP-B4 1,017,190,050 ops vs <= 1,034,717,556 PASS. SP-B5 3000 bp vs >=
1621 bp PASS. Commit order PASS: prereg 7a0f69b62 (12:37:13 UTC)
strictly precedes implementation 6a61b8f4f (13:54:17 UTC).

The structural kill is confirmed and is genuinely independent of
path-B quality: the veto fired 32 times (1 adversarial, 30 noise,
1 primary); the single adversarial veto withheld p006.pcm, a true
install (truth=LOWER, candidate correct, path B wrong), moving FIR
from 7/38 to 7/37. With 0 false T4/T5 adversarial installs (PA-B1 =
0), a veto can only shrink the denominator, so the bar is
unsatisfiable by construction: 7/38 = 1842 bp is not strictly below
1842 bp, and any k > 0 true-install vetoes give 7/(38-k) > 1842 bp.

Tag reasoning. The owner red line, restored literally on 2026-09-24,
is "no Python anywhere in loop work". The prereg's own clause reads
"No Python touches any wave artifact at any point (S7)" (line 177),
citing S7, whose actual holding (recorded in the red-team report)
voided SHAPED-MEMBERS when Python generated /tmp debug sources. The
prereg text narrows both the owner red line and S7's holding; the
governance tightening bans any debate from narrowing an owner red
line, so the narrower wording cannot be given effect.

New fact, verified by the judge: the Python-edited scratch
/tmp/spc/probe_b.zag is the direct design ancestor of the shipped
path-B code. The b4_dft_energy function body is byte-identical
between the Python-edited scratch and committed judge4.zag (diff of
the function bodies is empty), and /tmp/spc/pathb_section.zag is the
shipped path-B section modulo the frozen threshold change (20000 to
5000). The verdict's claim "no wave artifact affected" is false at
the design level: the artifact's path-B code was designed with Python
assistance. The contamination is in design lineage, not file bytes,
and design lineage is loop work. The worker's honest disclosure is
credited, but disclosure does not cure the violation.

Consequences of the [VOID] tag for part C:

1. "Violated in letter, though not in spirit" is struck from the
   record. It narrows the red line and must not become precedent.
2. A red-line violation is recorded for this wave's part-C
   development process. The violation is already covered by the
   standing rules (owner red line plus S7 precedent cited by the
   prereg itself); no immunity and no exception is granted, and no
   future wave may cite this case as one.
3. The verdict's recommendation line "or revisit the SP-B1 bar
   definition" is struck. Proposing to weaken a frozen kill bar
   after a miss is an owner-red-line violation inside the verdict
   document.
4. The verdict's governance claims are voided: the "independently
   validated" Goertzel-bank language and the NEW_KNOWLEDGE_CLAIM
   cannot stand as loop knowledge. The Goertzel bank may not be
   cited as validated; any future use requires clean-room
   re-derivation under a fresh prereg. The static code facts
   (PB-IND grep-clean, the measured numbers) remain facts; they do
   not constitute validation of a Python-assisted design.

The DISCARD verdict itself stands on the frozen mapping applied to
uncontested numbers, exactly as the skeptic demanded.

Provenance (M1): judge4.zag and driver4.zag are new this wave; the
path-B section (lines 813-1092) is new but descends from the
Python-edited /tmp/spc/probe_b.zag and /tmp/spc/pathb_section.zag
(see above). R33_NATIVE_IO_V1.zag is vendored substrate. The path-A
KB4V2 section is inherited and JUDGED (distinct from part C, which is
NEW). evidence/summary_run2/3/4.txt are new this wave; the decisions
log they hash lives at /tmp/spc/run2/decisions.log (committed
decisions_sha256.txt points at a /tmp path: hygiene flag, the hash
itself is committed). No render this wave. No stacking.

## M2. D-VID-1 V2

**Ruling: DEAD [VOID], upheld on both killing causes.** Uncontested.

Void scope for the record: the python3 heredoc touched
dvid1v2/v2_verify.zag during this wave. Frozen VKB5 voids the wave
evidence produced with it: SHA256SUMS_V2.txt, VERIFY_OUT.txt, and all
verdict scoreboard measurements. Grep corroborates the scope rests on
the disclosed file: no other committed dvid1v2 file contains a
python token (only the verdict's own disclosure mentions it). The
file was rebuilt Python-free afterward, but the historical touch
stands and the void is total for the wave evidence.

The technical kill is re-derived by the judge from committed sources
alone, independent of the voided evidence:

- bfade = o_clamp01k((200 - wz) * 1000 / 140) in both baseline and
  variant; o_clamp01k clamps to [0,1000], so bfade = 0 for every
  pixel with wz >= 200.
- The vortex disc (160 world-unit radius around the vortex center,
  vwz = 720 +/- ~100) lies at wz 560..880, all >= 200, so bfade = 0
  throughout the disc.
- With bfade = 0: bupm = o_mix(1000, ..., 0) = 1000 constant; the
  streak breakup multiplier is o_mix(1000, ..., 0)/1000 = 1; abupm is
  computed but never consumed (definition-only in both files).
- The ocean.zag vs ocean_dvid1_v2.zag diff is exactly three hunks,
  retargeting bup, abup, and sbup sampling into co-rotating
  coordinates; all three are consumed only by bfade-gated terms.

Therefore every V2-retargeted breakup term is multiplied out or dead
code in the disc, and T1's exact equality (A_pm = 498, B_pm = 498 vs
bar B <= 0.7 * A = 348) is the predicted consequence. Caveat (C3):
this theorem depends on V2's non-V2 formulas matching baseline
exactly, verified here for the committed files; future variants must
re-verify rather than inherit the conclusion.

The empirical pixel proof (0/5024 in-disc differing pixels) rests on
uncommitted frames and probe machinery outside the record; it is
unauditable and is banned from citation. The verdict survives on the
analytic derivation only. Commit order PASS: 840d54e6c (12:34:02) <
8767a005a (12:48:11) < a7c695590 (13:21:14). No sealed pair was
prepared, correctly.

Provenance (M2): ocean_dvid1_v2.zag is new this wave (the three-hunk
diff above). v2_verify.zag is new and Python-touched (VOID).
zag_sha256.zag is new (pure-Zag manifest tool). substrate/ copy of
R33_NATIVE_IO_V1.zag is vendored. frames_base/ and frames_v2/ are
uncommitted. The baseline docs/lab/imagination_discovery/vid/ocean.zag
is inherited and untouched.

## M3. C-D19

**Ruling: DISCARD [NEW], upheld.** Numbers uncontested and
re-verified from freelunch/evidence/evidence_verify.txt:
KB2_FOCUS_BP = 11804 vs frozen bar >= 13000 (1.30x): FAIL, a 0.12x
shortfall on the frozen 40-point F3 set. The frozen mapping mandates
DISCARD on any KB1..KB6 fail; the PARTIAL clause (KB5-marginal or
fringing) does not apply because KB2 failed. Other bars pass:
KB1-DET 3/3 byte-identical PASS, KB3 = 19027 PASS, KB4 = 10000 PASS,
KB5 mean |dL| = 0.05 PASS, KB6 208 dabs exact and 934 ms vs 979 ms
(0.95x) PASS. Baseline byte-identity gate: base.bmp =
e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d,
matching the S14 record: PASS. No Python anywhere: run_d19.sh static
guards confirmed by the red-team grep audit (pure Zag, zero RNG).
Commit order PASS: 35f81a256 (12:49:18) < f26e277da (13:04:29). No
sealed pair prepared, correctly.

Record-integrity defect: VERDICT_C_D19.md's KB1 row prints a mangled
59-character sha256 (30a9cd5c404c4b14393660cfc305064c56e6e19745e093
b0b146feb013a, dropping "0a9ab") while evidence/SHA256SUMS carries
the authoritative 64-character hash
(30a9cd5c404c4b14393660cfc305064c56e6e19745e093b0a9ab0b146feb013a),
and the Commits section still holds a "<this commit>" placeholder.
Ruling: a committed correction is required, not a footnote. The
defect sits in the determinism attestation row itself and in the
Commits section; the verdict document's KB1 attestation is defective
until amended in a committed amendment that (a) prints the
64-character evidence-authoritative hash and (b) fills the verdict's
own commit SHA. The DISCARD stands on the numbers regardless.

Provenance (M3): var1.bmp, var2.bmp, var3.bmp are new this wave and
byte-identical (KB1-DET 3/3). s19_focus.zag, s19_verify.zag,
run_d19.sh are new this wave. base.bmp is a declared rebuild of the
r8c baseline, byte-identical to the committed S14 record (EVIDENCE
line 8 labels it "baseline rebuild": honest). The prereg explicitly
records D15/R9, D17/S13, D18/S14 as QUEUED-UNJUDGED and untouched,
and invokes the S11 precedent ("no recycled render is presented as a
fresh judgment"). This is a clean provenance record; the D14
fulfillment claim (first implementation of the frozen "detail will
gather there" decision at (430,400)) is legitimate.

## M4. Standing rules R1, R2, R3

**R1: ADOPT** as a prospective standing rule: any Python contact
anywhere in loop work, including /tmp scratch files, voids the wave
evidence. Coherence: adoption is prospective, but this wave's part-C
violation is recorded and its evidence voided under the rules that
already stood during the wave (the literal owner red line and the S7
precedent the prereg itself cited). No immunity is granted and no
exception exists to cite. The verdicts stand on their arithmetic:
frozen mappings applied to uncontested numbers. This ruling does not
prejudge the owner's pending S7 decision; it applies S7's holding as
cited by the prereg, whatever the owner decides about S7 itself.

**R2: ADOPT.** The veto-only second-path slot for FIR improvement on
the KB4V2 substrate is closed: a veto-only mechanism over tasks with
zero residual falses cannot improve adversarial FIR, and the SP-B1
"strictly below" bar is unsatisfiable for that class (M1 proved it:
7/38 is not strictly below 1842 bp, and 7/(38-k) only grows). Reopen
only if residual falses exist inside the vetoed tasks or the
residual distribution changes, stated in frozen testable form in a
future prereg. Equality under SP-B1 is never permitted; the verdict's
"revisit the SP-B1 bar definition" line is struck per M1.

**R3: ADOPT** with the reconciled frozen lane-termination statement:
The D-VID-1 foam-breakup lane is terminated. DEAD is the
coordinate-retargeting of breakup sampling for disc foam churn: with
bfade = 0 throughout the vortex disc, the retargeted terms vanish or
are dead code, so no coordinate transform can affect disc foam. OPEN
under a fresh prereg only: (a) disc foam churn addressed via a
different mechanism (geometry churn), or (b) a redefined goal.
Changing the bfade fade law itself is explicitly placed: it is a
different mechanism (breakup modulation, not coordinate retargeting)
and is likewise OPEN only under a fresh prereg, which must re-freeze
the inverse correctly given the disclosed defective inverse in the
V2 addendum (the forward transform applies cx = qx * inw / 1000 +
vwx; the exact inverse requires qx = (cx - vwx) * 1000 / inw before
inverse rotation).

## Verdict table

| Motion | Ruling | Tag | Key numbers |
|---|---|---|---|
| M1 part C | DISCARD (upheld; tag overturned to VOID on cited lineage evidence) | [VOID] | SP-B1 1891 bp (7/37) vs frozen strictly below 1842 bp (7/38): FAIL; PB-AGREE 83/500 bp; SP-B2 8486; commits 7a0f69b62 < 6a61b8f4f |
| M2 D-VID-1 V2 | DEAD (upheld) | [VOID] | T1 498 vs 498, bar <= 348: FAIL; bfade = 0 for wz >= 200, disc wz 560..880; commits 840d54e6c < 8767a005a < a7c695590 |
| M3 C-D19 | DISCARD (upheld) | [NEW] | KB2 11804 vs >= 13000: FAIL; KB3 19027, KB4 10000, KB5 0.05 pass; commits 35f81a256 < f26e277da |
| M4 R1 | ADOPT (prospective; this wave's violation recorded under existing rules, no immunity) | n/a | Owner red line "no Python anywhere in loop work" |
| M4 R2 | ADOPT (reopen only on residual falses inside vetoed tasks, frozen testable form; never equality) | n/a | SP-B1 class closure proven at 7/38 |
| M4 R3 | ADOPT (reconciled scoping; fade-law changes explicitly OPEN under fresh prereg) | n/a | bfade = 0 no-op proof from committed sources |

Hygiene flags carried forward (non-verdict): committed correction
of the M3 mangled sha and "<this commit>" placeholder; the
/tmp/spc/run2/decisions.log path inside committed
decisions_sha256.txt should be replaced with a committed copy in a
future wave; judge4_base.zag / driver4_base.zag and R33 vendored
copies under secondpath/ remain uncommitted in the working tree.
