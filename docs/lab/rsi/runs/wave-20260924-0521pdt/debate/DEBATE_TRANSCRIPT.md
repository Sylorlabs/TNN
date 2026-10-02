# DEBATE TRANSCRIPT: wave-20260924-0521pdt

Debate group convened by the finish-up coordinator after the scheduled worker
timed out (three worker commits landed: C-D19 verdicts, D-VID-1 V2, second-path
part C implementation, red-team review; the debate, LOOP_STATE update, and
lock removal were completed by the finish-up agent). Format: advocate argues
FOR the worker verdicts, skeptic argues AGAINST (gaming, confounds, weak bars,
void scoping, precedent), judge renders a reasoned ruling with numbers cited.
A worker verdict is overturned only with cited evidence, never rhetoric.

The skeptic's provenance probe ("What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?") is on the record in
every motion below; the judge answers it per motion.

The owner's five pending governance decisions (S7 strike, MD-SSD-1
keep-with-UNVERIFIABLE vs re-freeze, S11 pull, S11-AUD pull, C12 queue) are
his and are not ruled on here.

---

# ADVOCATE BRIEF

Position: FOR all three worker verdicts, FOR red-team agreement, FOR adoption
of R1, R2, R3. All figures below were verified against the committed files
before writing.

## M1. Second judgment path part C: uphold DISCARD [NEW]

The worker's verdict stands on arithmetic that admits no rebuttal. SP-B1
measured candidate adversarial FIR 1891 bp (7/37) against the frozen bar
requiring strictly below the pinned 7/38 (1842 bp). FAIL. Every other bar
passed with margin: PB-IND static grep clean, PB-DET 3/3 byte-identical,
PB-AGREE 83 bp against a 500 bp budget, PA-B1 zero false T4/T5 adversarial
installs, SP-B2 8486 bp exactly (floors only, confirmed exact at 50916/6),
SP-B3 3/3, SP-B4 1017190050 within 1034717556, SP-B5 3000 bp against 1621 bp.
The frozen verdict mapping mandates DISCARD on any bar miss. One miss is one
miss.

The red-team confirmed the kill generalizes to a structural proof, not a bad
sample: the path-B veto fired 32 times and its single adversarial veto
withheld p006.pcm, a true install (truth LOWER, jcand LOWER correct, path-B
SAME wrong). FIR moved from 7/38 to 7/37. With zero residual false installs
in T4/T5 and all 7 falses sitting in T2 colorconst, which path B does not
cover, a veto-only mechanism can only remove true installs (FIR rises) or
never fire (7/38, equal, not strictly below). The bar is unsatisfiable by
construction for this mechanism class on this substrate.

On the disclosed Python deviation (python3 edited /tmp/spc/probe_b.zag
twice): the red-team upheld [NEW] rather than [VOID] under a narrow immunity
argument I endorse. The killing evidence, the veto arithmetic and the 0 false
T4/T5 installs, is structurally independent of the contaminated scratch work;
even a perfect path-B component could only deliver 7/38, which still fails.
This is a one-time narrow exception tied to provable immunity, not a
precedent, which is exactly why R1 is needed.

Commit order passes: prereg 7a0f69b62 at 12:37:13 UTC strictly precedes
implementation 6a61b8f4f at 13:54:17 UTC.

## M2. D-VID-1 V2: uphold DEAD [VOID]

Two independent killing causes, either sufficient on its own. Cause 1
(governance): a python3 heredoc edited dvid1v2/v2_verify.zag mid-wave, and
the frozen VKB5 rule states any Python touch of a new wave artifact voids
its wave evidence. The worker self-voided SHA256SUMS_V2.txt, VERIFY_OUT.txt,
and all measurements, and presented nothing as non-void. The red-team
confirmed the self-void was correctly and completely applied.

Cause 2 (technical): an analytic no-op proof, re-derived by the red-team
from committed sources with no Python and no probes. In ocean_dvid1_v2.zag
line 455, bfade = o_clamp01k((200 - wz) * 1000 / 140), which is 0 for every
pixel with wz >= 200. The vortex disc spans wz in [510,930], entirely above
200, so bfade = 0 everywhere in the disc. With bfade = 0, bupm is the
constant 1000, the streak breakup multiplier is 1000/1000 = 1, and abupm is
dead code in both arms. Every term the V2 co-rotating block retargets is
multiplied out. The reported T1 of 498 vs 498 (bar needed at most 0.7*A,
i.e. 348) is exactly what the theorem predicts. The V2 hypothesis is wrong
at the source: there is no breakup modulation in the disc to fix.

Commit order passes: prereg 840d54e6c at 12:34:02 UTC, addendum 8767a005a
at 12:48:11 UTC, implementation a7c695590 at 13:21:14 UTC. No sealed pair was
prepared, correctly, since VKB1 through VKB6 did not all pass.

## M3. C-D19: uphold DISCARD [NEW]

The kill is numbers, not rhetoric. KB2_FOCUS measured 11804 bp (1.18x)
against the frozen bar of at least 1.30x (13000 bp): a 0.12x shortfall on
the frozen 40-point F3 set, whose points were frozen in the prereg before
any D19 code existed. Every other bar passed: KB1-DET 3/3 byte-identical,
KB3_STONE 19027 bp against 12000, KB4_SKY 10000 bp within 11000, KB5 0.05
against 8.0, KB6-COST 208 dabs exact and 0.95x wall. The frozen verdict
mapping mandates DISCARD on any KB1 through KB6 fail, and the PARTIAL
narrowing clause requires KB2 and KB3 both to pass, which KB2 did not. The
red-team confirmed the mapping was correctly applied and that KB3's 1.90x
does not rescue a KB2 miss.

Provenance is clean: var1/var2/var3.bmp are new this wave and byte-identical
(first rendered this wave); base.bmp is a declared rebuild of the r8c
baseline, verified byte-identical (e4f65557...), not presented as new; no
prior candidate is stacked in. Governance is clean: zero Python contact
(run_d19.sh carries static no-Python guards), commit order 35f81a256 <
f26e277da < cc48ae52a strict. No sealed pair was prepared, correctly. The
hygiene flag (a mangled 59-char sha256 printed in the verdict doc versus
the 64-char value in evidence/SHA256SUMS) is non-verdict; the evidence file
is authoritative.

## M4. Standing-rule recommendations R1, R2, R3: adopt all three

R1 (Python contact anywhere, including /tmp scratch, voids wave evidence):
adopt. The part-C verdict survives only under the narrow immunity argument;
its "letter vs spirit" framing must never become precedent. R1 aligns the
standing rule with the owner's literal red line and the S7 void precedent,
and leaves the immunity exception where it belongs: a one-off carve-out
proven by structural independence, not a policy.

R2 (close the veto-only second-path slot for FIR improvement on the KB4V2
substrate): adopt. M1's structural proof shows the slot cannot produce a
pass while residual falses live outside the vetoed tasks. Reopen only if
residual falses exist inside the vetoed tasks (e.g. a T2-targeted veto) or
the residual distribution changes. Equality must not be permitted under
SP-B1: the frozen bar says strictly below, and weakening it to permit
equality is exactly the bar-weakening the loop forbids.

R3 (terminate the D-VID-1 foam-breakup lane): adopt. M2's proof is
mechanism-level, not candidate-level: any V3 retargeting breakup sampling
coordinates hits the same bfade = 0 wall. Future disc-foam work only via a
different mechanism (geometry churn: arm and crest masks sweeping the
rotating frame) under a fresh prereg.

The following items are noted as the owner's pending decisions and are not
ruled on here: the S7 strike versus narrowed Python-test debate, MD-SSD-1
keep-with-UNVERIFIABLE versus re-freeze, pulling the S11 image pair, pulling
S11-AUD, and C12 staying in the judge queue versus being pulled.

---
# SKEPTIC BRIEF

I read all three verdict files, REDTEAM_WAVE_0521.md, the preregs, and
re-verified the load-bearing numbers and code claims against the committed
sources myself (shell/grep/diff only, no Python). Position per motion: the
three worker verdicts (DISCARD / DEAD / DISCARD) are numerically sound and I
do not contest them. What I contest is the governance around them: the
part-C [NEW]-via-immunity tag, the "letter vs spirit" framing, a
bar-weakening proposal sitting inside a verdict document, and several
scoping gaps the red-team waved through.

## M1: Second judgment path part C (worker: DISCARD [NEW]; red-team: AGREE [NEW])

**Conceded:** the arithmetic is verified from committed evidence.
`secondpath/evidence/summary_run2.txt`: cand_adv_false=7,
cand_adv_installs=37, cand_adv_fir_bp=1891 against the frozen bar strictly
below 7/38 (1842 bp). The veto withheld one true install (p006.pcm),
moving FIR from 7/38 to 7/37. With all 7 residual falses in T2 colorconst,
outside path-B coverage, no T4/T5 veto can reduce the false count; it can
only shrink the denominator. DISCARD is structurally forced and I do not
fight it.

**Attack A1: the [NEW] tag via "narrow immunity" is special pleading.**

- The owner's red line is "no Python anywhere in loop work," not "no Python
  touching wave artifacts." The worker's own verdict concedes python3 edited
  `/tmp/spc/probe_b.zag` twice and then frames it as "violated in letter,
  though not in spirit." That framing is itself a narrowing of the red line,
  which the 2026-09-24 governance tightening explicitly bans (pure-Zag rule
  restored literally; no debate may narrow a red line).
- The S7 precedent is directly on point: SHAPED-MEMBERS was voided when
  Python generated /tmp debug sources. The part-C prereg's Python clause
  (PREREG_SECONDPATH_PARTE_0521.md line 177: "No Python touches any wave
  artifact at any point (S7)") cites S7 while narrowing it. The cited
  precedent refutes the narrowing: S7 voided on /tmp contact, and
  probe_b.zag is a /tmp scratch file.
- The red-team's "no contamination path from scratch probe to veto ledger"
  is false at the design level. I diffed `b4_dft_energy` between
  `/tmp/spc/probe_b.zag` (the Python-edited scratch) and the committed
  `secondpath/judge4.zag`: the diff is empty. The Python-assisted design IS
  the shipped path-B implementation. Measurements ran in pure Zag, but the
  bank structure, constants, and peak-picking logic were developed with
  Python in the loop, and that design process is unauditable from committed
  files. (The `python` tokens I found in driver4.zag and R33_NATIVE_IO_V1.zag
  are comment-only "no Python" declarations; the artifact files are clean.
  The contamination is in design lineage, not file bytes.)
- The immunity logic saves the VERDICT but not the TAG, and it does quiet
  work beyond that: it preserves the verdict's "independently validated"
  language for the Goertzel/centroid (PB-AGREE 83 bp) and keeps the
  candidate in the [NEW] judged set. A verdict can survive contaminated
  development; the validation claims and the tag may not launder it.
- Precedent: a "narrow immunity exception" carrying a "must not become
  precedent" warning is still a precedent. R1 adopts the strict rule going
  forward while immunizing this wave. That is incoherent: if the owner's
  red line is the rule, this wave violated it. The next wave will cite this
  exception for its own /tmp Python.

**Demand:** DISCARD stands; strike "letter vs spirit" from the record;
record a red-line violation for this wave's development process; reject the
[NEW]-via-immunity rationale (the tag itself is the coordinator's call, but
immunity cannot be the reasoning). No future wave may cite this exception.
Corollary: the Goertzel bank cannot be adopted later as a "validated"
component without clean-room re-derivation under a fresh prereg, since its
design lineage is tainted.

**Attack B: the verdict text proposes weakening a frozen kill bar.** The
recommendation line "or revisit the SP-B1 bar definition" is, after a miss,
a proposal to weaken a frozen kill bar. That is an owner-red-line violation
sitting inside the verdict document itself. The red-team's R2 already
rejects permitting equality; the line must be struck from the verdict. A
missed frozen bar is documented, not revisited.

**Provenance probe (M1):** Artifacts under judgment (judge4.zag,
driver4.zag) are new this wave. Inherited and correctly disclosed: the
path-A KB4V2 section (ADOPTED-narrowed, JUDGED at 1421pdt, not re-judged
here; COMPONENT_LINEAGE discloses it), the R33_NATIVE_IO_V1.zag substrate
copy (vendored), the frozen fixture harness. New: j_pitchdisc2 Goertzel
bank, j_timbredisc2 centroid, the veto arbitration rule, driver4
candidate-arm dispatch. Nothing inherited is presented as new; no stacked
prior candidate; no re-certification masquerading as new. The gap is design
lineage (see A1): the path-B core is byte-identical to the Python-edited
/tmp scratch, which the artifact-level disclosure understates.

## M2: D-VID-1 V2 (worker: DEAD [VOID]; red-team: AGREE [VOID])

**Conceded:** the analytic no-op derivation is airtight, verified from
committed sources, not taken on trust. `diff` of
`docs/lab/imagination_discovery/vid/ocean.zag` vs
`dvid1v2/ocean_dvid1_v2.zag` shows exactly three hunks: the co-rotating
block plus the three retargeted sampling statements (bup, abup, sbup).
Everything else is identical, including `bfade = o_clamp01k((200 - wz) *
1000 / 140)` at line 455 in both files. o_clamp01k clamps to [0,1000]
(confirmed at ocean.zag lines 57-61). The vortex disc sits at wz 560..880
([510,930] allowing vortex-center noise), so bfade = 0 throughout with
enormous margin. cx/cz are consumed only by bup, abup, sbup; all three feed
terms gated by bfade (bupm, abupm, and the streakf multiplier all collapse
to 1000/1000 = 1 when bfade = 0); abupm is declared once and never consumed
in either file (dead code, confirmed by count). The bfade2 fine-shading
block is untouched by the diff and contributes identically to both arms.
The mechanism is dead at the source. DEAD stands on the technical kill
alone; the self-void over-determines it.

**Attack C1 (void scoping):** the worker's "the heredoc touched only
v2_verify.zag" rests on disclosure, not on anything recoverable from git; a
heredoc's scope leaves no commit trace. What is auditable: grep over all
committed dvid1v2 wave files shows no Python contact except the verdict's
own disclosure lines. That corroborates but does not prove the scope claim.
The void was correctly applied to every wave measurement
(SHA256SUMS_V2.txt, VERIFY_OUT.txt, all bars), and VKB1 was correctly not
run on void evidence.

**Attack C2 (the "independent pure-Zag probe" narrative):** the empirical
pixel proof (0/5024 differing cells) was computed with voided/uncommitted
machinery; no probe .zag sources exist in the wave dir. The claim is
unauditable from committed files. The red-team was right to refuse to cite
it, and the verdict survives only because the analytic derivation needs no
probes: it is a theorem about committed sources. Any future citation of
this kill must cite the analytic derivation, never the pixel counts.

**Attack C3:** the theorem depends on the committed V2 generator's non-V2
formulas matching the baseline exactly. Verified here (three hunks only),
but note the fragility: had the V2 author altered any shared line, the
theorem would break silently. Airtight in this instance, not a general
property.

**Attack E2 (lane-termination scoping):** the worker and red-team word the
termination differently. Worker: a future V3 must target geometry churn or
redefine the goal, under a fresh prereg. Red-team R3: the "foam-breakup
lane" is closed; geometry-churn mechanisms allowed under a fresh prereg.
Unresolved: a V3 that changes the bfade fade law itself rather than
retargeting sampling coordinates. That sits outside the letter of
"retargeting breakup sampling coordinates," but it would inject breakup
modulation into a disc the design currently zeroes by construction: a new
hypothesis needing fresh justification, not a continuation of D-VID-1.
Reconcile into one frozen statement: dead = coordinate-retargeting of
breakup sampling for disc churn; open = geometry-churn mechanisms or a
redefined goal, each under a fresh prereg that also re-freezes the
(currently defective, disclosed) inverse correctly.

**Provenance probe (M2):** ocean_dvid1_v2.zag is new this wave (first
rendered wave-20260924-0521pdt). The baseline ocean.zag is inherited and
untouched (last change the 3b011ef18 repair commit). v2_verify.zag has
tainted provenance (Python heredoc, rebuilt, VOID). zag_sha256.zag is new.
The 48+48 frames are uncommitted. Nothing inherited is presented as new; no
stacked prior candidate; the verdict honestly labels all measurements VOID.
Provenance is clean; the candidate is simply dead twice over.

## M3: C-D19 (worker: DISCARD [NEW]; red-team: AGREE [NEW])

**Conceded:** the kill is numeric and verified.
`freelunch/evidence/evidence_verify.txt`: KB2_FOCUS_BP=11804 vs frozen bar
>= 13000: FAIL. KB3=19027 (pass), KB4=10000 (pass), KB5_MEANABS_X100=5 =
0.05 (pass). The frozen mapping mandates DISCARD on any KB1..KB6 miss; the
PARTIAL clause cannot apply with KB2 failed. No sealed pair prepared,
correctly. DISCARD stands.

**Attack D1 (mangled sha):** the verdict's KB1 row prints a 59-character
sha256 (`30a9cd5c...093b0b146feb013a`), dropping `0a9ab` from the true
64-character hash in evidence/SHA256SUMS
(`30a9cd5c...093b0a9ab0b146feb013a`). I checked every other row of the
verdict table against evidence_verify.txt and SHA256SUMS: KB2, KB3, KB4,
KB5 all match; the baseline-gate hash is transcribed correctly. The
corruption is isolated to the KB1 row, but that row is the determinism
attestation, the single most load-bearing string in a byte-identity claim.
The red-team's "hygiene, non-verdict" shrug understates it: a verdict
document that cannot transcribe its own determinism hash has a
record-integrity defect. The fix must be a committed correction, not a
footnote. (The verdict's Commits section also still carries the
`<this commit>` placeholder.)

**Attack D2 (base.bmp honesty):** verified genuine, conceded. base.bmp's
sha256
(`e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d`)
matches the committed r8c baseline hash recorded in
`docs/lab/imagination_discovery/img/FORK_C_REPORT.md` (R9 evidence commit);
EVIDENCE_C_D19.md line 8 labels it "baseline rebuild." Declared rebuild,
byte-identical, honestly labeled. No shortcut.

**Provenance probe (M3):** var1/var2/var3.bmp are new this wave
(byte-identical to each other, first rendered wave-20260924-0521pdt).
base.bmp is a declared rebuild of the r8c baseline, not presented as new.
s19_focus.zag and s19_verify.zag are new; r8c_baseline.zag is the rebuild
generator. The prereg explicitly records S11-IMG, C1, C2v3, D15/R9, D17/S13,
D18/S14 as QUEUED-UNJUDGED and untouched: no stacking, no recycling. The
D14 fulfillment claim is legitimate (frozen world decision, "detail will
gather there" at (430,400); D19 is its first implementation). Fulfillment,
not invention. Provenance is clean.

## M4: the three standing-rule recommendations (R1/R2/R3)

- **R1 (adopt: any Python contact anywhere in loop work voids the wave
  evidence):** AGREE, it is the owner's red line. But adopting it
  prospectively while immunizing this wave is incoherent and
  precedent-setting no matter what the warning label says. Record the
  violation for this wave: DISCARD stands on the arithmetic, "letter vs
  spirit" is struck, [NEW]-via-immunity is rejected as reasoning. Note the
  prereg's Python clause cites "(S7)" while narrowing S7's actual holding
  (void on /tmp contact): the citation refutes the narrowing.
- **R2 (close the veto-only second-path slot for FIR improvement on the
  KB4V2 substrate):** AGREE; properly scoped, and it explicitly permits what
  the verdict suggested (a T2-targeting veto, since the residual falses live
  in T2), so the closure is not over-broad. Two demands: (a) strike the
  verdict's "revisit the SP-B1 bar definition" line, a bar-weakening
  proposal inside a verdict document; (b) the reopen condition ("residual
  falses inside the vetoed tasks or the residual distribution changes")
  needs a frozen, testable form in any future prereg, or the closure will
  erode into vibes.
- **R3 (terminate the D-VID-1 foam-breakup lane):** AGREE. Demand the
  worker/red-team wording split be reconciled into one frozen statement
  placing fade-law changes (bfade itself) explicitly: outside the
  terminated coordinate-retargeting lane, admissible only as a new
  hypothesis under a fresh prereg, since it contradicts the design the
  no-op proof relies on.

**Noted, not ruled:** the owner's five pending governance decisions (S7
strike, MD-SSD-1 keep-with-UNVERIFIABLE vs re-freeze, S11 pull, S11-AUD
pull, C12 queue) remain his; nothing in this brief prejudges them.

## Skeptic summary

| Motion | Verdict (uncontested) | Skeptic fight |
|---|---|---|
| M1 part C | DISCARD stands (SP-B1 1891 > 1842, verified) | [NEW]-via-immunity rejected as special pleading; Python-edited /tmp scratch is byte-identical to shipped path-B code; S7 precedent contradicts the narrow reading; strike "letter vs spirit" and the "revisit the SP-B1 bar" line; record the red-line violation |
| M2 D-VID-1 V2 | DEAD stands (bfade=0 no-op proven from committed sources; self-void over-determines) | Heredoc scope rests on disclosure, not audit; pixel-proof narrative is unauditable scratch and must never be cited; reconcile the lane-termination wording (fade-law changes vs coordinate retargeting) into one frozen statement |
| M3 C-D19 | DISCARD stands (KB2 11804 < 13000, verified) | Mangled 59-char sha in the verdict's KB1 row is a record-integrity defect needing a committed correction, not a footnote shrug; base.bmp rebuild verified honest |

---

# JUDGE RULING

The full ruling follows verbatim (also kept as JUDGE_RULING_0521.md):

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

---

## Debate record closed

Overturns: one (M1 tag [NEW] to [VOID], on cited lineage evidence). All
three worker verdict outcomes upheld. R1/R2/R3 adopted as standing rules.
Transcript: DEBATE_TRANSCRIPT.md. Full ruling: JUDGE_RULING_0521.md.
