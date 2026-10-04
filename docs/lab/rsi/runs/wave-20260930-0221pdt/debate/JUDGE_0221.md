# JUDGE_0221.md (wave-20260930-0221pdt)

The judge renders reasoned rulings with numbers cited. A debate can
overturn a coordinator verdict only with cited evidence, never
rhetoric. The skeptic's provenance probe is answered verbatim in
every motion: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?"

## M1: F3a verdict: BUILD-FAIL on K-F3-4 (bar text); mechanism
exonerated on the functional lines

Provenance: prereg new this wave (d80106155, committed alone);
implementation inherited byte-identical from 847a8f10f (verified:
working tree diff empty; built binary from that source; one benign
analyzer lint A0102 at line 604, pre-existing code); fixtures
inherited; evidence new (3 runs, byte-identical 97dd4276).

Ruling: the skeptic's textual case is dispositive. K-F3-4 as frozen
reads "'w' occurs in none of the frozen T, F1, or R fixture inputs
(audit of the frozen fixture strings)." The audit found 'w' in
"xqw", a frozen F1-reuse fixture input. The bar fails literally. The
advocate's narrow reading (F1 = the counterexample bullet only)
requires importing a distinction the bar text does not make; adopting
it after the run would weaken a frozen bar to force a pass, which
the owner's rule forbids. The verdict rule frozen in the prereg
controls: any bar failing means BUILD-FAIL with the killing line
cited. Verdict: BUILD-FAIL. Killing line: K-F3-4, 'w' occurs in the
frozen F1-reuse fixture "xqw".

Pinned to the verdict line (not overturning it): (1) K-F3-1 PASS on
all measured lines (COUNTEREXAMPLE_DETECTED(wab); DIAGNOSIS pos=0
byte=119 conflicts=0; PRIMITIVE-CONSTRUCTED (0,119); alt=C0 index 2;
v3 ACTIVE parent v2; wab->www; xab->xxx, abc->ccc, xy->xx,
defg->gggg unchanged; wqw->www reuse with no new revision; R 8/8;
fails=0, exit 0). (2) K-F3-2 PASS: 3/3 byte-identical (97dd4276). (3)
K-F3-3 PASS: zero 'w' char literal, zero "wab"/"www"/"wqw", zero 119
in the committed machinery. The white-box trace shows the diagnosis
came from the F-vs-P comparison. No mechanism failure is evidenced;
the kill is on the family/bar design, not the mechanism. (4) Audit
finding: the parent prereg's allowed-set disjointness rationale is
inaccurate. Of {i,j,k,l,m,n,o,r,t,u,v,w}, only {i,k,m,r,v} are
genuinely absent from all frozen fixture inputs (j,l,n,o,t,u occur
in R inputs; w occurs in the F1-reuse fixture). 'i' was spent on F2.
(5) Remedy (no re-freeze this wave): next wave re-freezes F3a with a
corrected disjointness bar and a byte from {k,m,r,v} chosen by a
declared rule, then re-runs. The re-run is the test, not a formality.

## M2: Fork battery CONFIRM (process confirmation only)

Provenance: driver mechanically derived from frozen batch_2321.sh
(sed/awk; zero Python in derivation); run_one.sh byte-identical to
frozen (4c2fadfc); harness re-verified byte-identical to frozen pin
(a2e6284c); new are 77 per-entry RESULT.txt files and the manifest.

Ruling: fresh 77-entry run: 75 PASS, 0 FAIL, 2 UNTESTABLE
(rh-pull-1-head, rh-pull-2-head; the known non-TNN research-doc
trees). Uniform on all 75 tested: znc pin 498abcb5 (0 pin
divergence); probe sha 3b29aa06 (0 divergence); b1/b2/b3 PASS;
NEG1 E0002 75/75; NEG2 char-1 discrimination 75/75;
harness_verdict_pass_count 1 on 75/75. LIVE entries (2):
arch-wave-20260929-2321pdt at a4314633 (newly enumerated archive),
local-tnn-native-lab at 1f681e87b (run-start tip). Duplicate-SHA
group carried: {arch-wave-20260929-1721pdt, local-1721pdt-tip} at
7c11ac5af. Naming note: this wave's prior-tip fixture entry is
local-20260929-2321pdt-tip (full date) because local-2321pdt-tip was
already taken by the 2026-09-28 2321pdt tip; recorded in the driver.
Remote: zero new refs (origin/tnn-native-lab bedf8b4a unchanged;
read-only ls-remote at wave start). Scope stamp (per skeptic S2):
toolchain and extraction stability only; not evidence the tip's
contents are good.

## M3: Interactive survey NONE new: CONFIRM

Provenance: diff fed72668..HEAD over *.zag; new is the survey record.

Ruling: 158 new or modified .zag files since the 2321pdt pin, all
from the parallel research-lead process (beam, conditional-first,
bridge, c0integ lanes); zero with stdin/readline/interactive/chat
patterns. The frozen probe instruments remain the only chat-capable
instruments. tnn_chat FIT staleness 4 of 8 (due at 8 of 8). The
skeptic's governance note (paper edits under a standing stop order)
is out of this survey's scope and is recorded, not ruled on, here.

## M4: Commit-order self-check VALID: CONFIRM

Provenance: commit record; new is the check result.

Ruling: prereg first commit d80106155 (2026-09-30, this wave)
contains exactly PREREG_PI_REV2_F3.md and strictly precedes all F3
evidence commits (this commit). No implementation file was created
or modified this wave (git status shows only .txt/.md additions).
The check certifies commit order, which is exactly what the standing
rule requires. The skeptic's prereg-quality note (S1) is a separate
matter and does not affect ordering validity.

## M5: Queue: re-freeze F3a next, then reproduction

Provenance: queue inherited from the reorientation and the 2321pdt
M5; new is the concrete next step.

Ruling: next wave (1) re-freezes F3a: corrected K-F3-4 text
("adversary byte absent from every frozen fixture input string in
the parent prereg's fixture list, audited before the run") plus a
byte from {k,m,r,v} by a declared deterministic rule, then re-runs
the frozen binary under it; (2) then step 4, independent
reproduction of H-PI-REV2 from committed source; (3) F3b execution
stays queued behind its interface-extension prereg (frozen design
stands; no F3b code exists). The advocate's A5 ordering (F3b prereg
in parallel with reproduction) is accepted. Banked and untouched:
NQ4/NQ5, the six governance rulings, sealed blind pairs, DP-1, Q1/Q2,
DDES t*=0 repair, H-EXP2, H-ROUTER2, DEVANG2 retry, the
conditional-first builder lane, tnn_chat FIT at 4 of 8 staleness.

No frozen bar was weakened. Zero Python in wave work. No em-dashes
in wave documentation.
