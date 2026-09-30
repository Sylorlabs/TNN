# ADVOCATE_0221.md (wave-20260930-0221pdt)

The advocate argues FOR each adoption. Provenance probe (verbatim):
"What is the provenance of the artifacts under judgment, and what
exactly is new versus inherited?"

## A1: F3a deserves BUILD-PASS

Provenance: prereg new this wave (d80106155, committed alone);
implementation inherited byte-identical from 847a8f10f; fixtures
inherited; evidence new (3 runs, byte-identical 97dd4276).

The numbers are clean. K-F3-1: COUNTEREXAMPLE_DETECTED(wab),
DIAGNOSIS pos=0 byte=119 conflicts=0, PRIMITIVE-CONSTRUCTED (0,119),
alt=C0 index 2, v3 ACTIVE parent v2, wab->www, all priors unchanged,
wqw->www reuse with no new revision, R 8/8, fails=0, exit 0. K-F3-2:
3/3 byte-identical. K-F3-3: zero w-literals, zero 119 in committed
machinery. The mechanism did everything the prereg asked on a byte
chosen by a declared zero-discretion rule (last of the sorted frozen
allowed set), which is exactly the S1-narrowing the judge ordered.

On K-F3-4: the parent prereg's frozen-fixtures section lists F1 and
F1-reuse as separate bullets. "F1 fixture inputs" in the bar text
refers to the F1 bullet ("xab"), which contains no 'w'. Under the
prereg's own taxonomy the bar passes. The 'w' in "xqw" sits at
position 1 and is mechanistically inert: the diagnosis selected
(0,'w') with conflicts=0 and the white-box trace shows the causal
chain through the F-vs-P comparison. No contamination path exists
from a position-1 'w' in a passing example to a position-0 diagnosis.
Failing the build on this reading punishes the mechanism for a
bar-text ambiguity the mechanism did not create, and discards a clean
adversary result the judge explicitly ordered this wave to obtain.
Verdict: BUILD-PASS with the "xqw" caveat pinned to the verdict line.

## A2: Fork battery CONFIRM

Provenance: driver mechanically derived from frozen batch_2321.sh
(sed/awk, zero Python); run_one.sh byte-identical to frozen
(4c2fadfc); harness re-verified byte-identical to frozen pin
(a2e6284c); new are 77 per-entry RESULT.txt files and the manifest.

77 entries, 75 PASS, 0 FAIL, 2 UNTESTABLE (rh-pull-1-head,
rh-pull-2-head, the known non-TNN research-doc trees). Uniform on all
75: znc pin 498abcb5 (0 divergence); probe sha 3b29aa06; b1/b2/b3
PASS; NEG1 E0002 75/75; NEG2 char-1 discrimination 75/75. LIVE entries
(2): arch-wave-20260929-2321pdt at a4314633 (newly enumerated
archive), local-tnn-native-lab at 1f681e87b (run-start tip).
Duplicate-SHA group: {arch-wave-20260929-1721pdt, local-1721pdt-tip}
at 7c11ac5af (carried). Remote: zero new refs (origin/tnn-native-lab
bedf8b4a unchanged). Process confirmation only: toolchain and
extraction stability, not evidence the tip's contents are good.

## A3: Interactive survey NONE new CONFIRM

Provenance: diff fed72668..HEAD over *.zag; new is the survey record.

158 new or modified .zag files since the 2321pdt pin, all from the
parallel research-lead process (beam, conditional-first, bridge,
c0integ lanes); zero with stdin/readline/interactive/chat patterns.
The frozen probe instruments remain the only chat-capable
instruments. tnn_chat FIT staleness 4 of 8 (due at 8 of 8).

## A4: Commit-order self-check VALID CONFIRM

Provenance: commit record; new is the check result.

Prereg first commit d80106155 contains exactly
PREREG_PI_REV2_F3.md and strictly precedes all F3 evidence commits.
No implementation file was created or modified this wave. The check
certifies commit order, which is what the standing rule requires.

## A5: Queue AMEND as ordered

Provenance: queue inherited; new is the concrete next step.

Next wave: F3b execution needs an interface-extension prereg first;
step 4 (independent reproduction of H-PI-REV2) should run in parallel
with the F3b prereg design. The pipeline order stands.
