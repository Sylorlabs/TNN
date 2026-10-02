# JUDGE_2321.md (wave-20260929-2321pdt)

The judge renders reasoned rulings with numbers cited. A debate can
overturn a coordinator verdict only with cited evidence, never rhetoric.
The skeptic's provenance probe is answered verbatim in every motion:
"What is the provenance of the artifacts under judgment, and what
exactly is new versus inherited?"

## M1: H-PI-REV2 BUILD-PASS: CONFIRM, with the skeptic's caveats pinned
to the verdict line

Provenance: prereg inherited from the 1721pdt design lane (7c11ac5af);
fixtures inherited (H-REVISE set, Family X, RT2-A pairs); new this wave
are the implementation, the frozen binary, the evidence, and the audits.

Ruling: the seven frozen kill bars pass on the cited evidence, and the
numbers are not in dispute. K-RV2-1(a): zero 'x' char literals, zero
numeric 120, fixture strings confined to main (lines 702-826).
K-RV2-1(b): dsearch over T+F1 returns -1 on the port. K-RV2-1(c):
DIAGNOSIS pos=0 byte=120 conflicts=1 from the F-vs-P comparison.
K-RV2-1(d): F1-reuse "xqw"->"xxx" with no new revision; F2 ("iab")
revised correctly on the single first execution, byte=105, conflicts=0.
K-RV2-1(e): STRUCT base=38 nbranches=1 br0=(0,120)->2, then v3 adds
(0,105)->2. K-RV2-2: ROLLBACK(v1) restores "xab"->"bbb" and
"xy"->"yy". K-RV2-3: observe() audited, no content branch. K-RV2-4:
8/8 R after P6 and after P8. K-RV2-5: reverse found, identity at index
0. K-RV2-6: 3/3 byte-identical (9718685f). K-RV2-7: F2 first-execution
pass; zero 'i' char literals; zero "iab"/"iii"/"iqw" string literals.
Commit-order self-check VALID (7c11ac5af < 847a8f10f, ancestry
confirmed). The label is BUILD-PASS, not SURVIVES; no promotion.

The skeptic's attacks are sustained as narrowing caveats, not as
overturns, because none cites evidence that a bar was mismeasured:
S1 stays a live kill vector (the F2 byte was chosen by the implementer
under a declared rule, not by an independent adversary; the kit is
researcher-shaped). S2 is conceded boundedness (byte-equality tests at
positions only). S3 stands (finite diagnosis space). S4 stands
(position-ascending bias untested outside first-letter worlds). S5 is a
residual (trust assumption untested). The K-RV2-5 vacuous-pair quirk
("hello"->"olleh" constrains nothing under the ported extractor) is
pinned to the verdict line per the skeptic's M6 probe: the bar text
alone overreads the evidence without this note.

Verdict: BUILD-PASS (bounded revising mechanism, all frozen bars pass),
with S1-S5 live and the K-RV2-5 quirk disclosed on the verdict line.

## M2: Fork battery CONFIRM (process confirmation only): CONFIRM

Provenance: driver mechanically derived from frozen batch_1721.sh;
run_one.sh byte-identical to frozen (4c2fadfc); new are 75 per-entry
RESULT.txt files and the manifest.

Ruling: fresh 75-entry run, driver exit 0: 73 PASS, 0 FAIL, 2
UNTESTABLE (rh-pull-1-head, rh-pull-2-head; the known non-TNN
research-doc trees). Uniform on all 73 tested: znc pin 498abcb5 (0 pin
divergence); probe sha 3b29aa06 (0 divergence); b1/b2/b3 PASS;
NEG1 E0002 73/73; NEG2 char-1 discrimination 73/73. LIVE entries (2):
arch-wave-20260929-1721pdt at 7c11ac5af (newly enumerated archive,
pinned this wave), local-tnn-native-lab at fed72668 (run-start tip).
Duplicate-SHA group named: {arch-wave-20260929-1721pdt,
local-1721pdt-tip} at 7c11ac5af. Scope stamp (per skeptic M2): toolchain
and extraction stability only; not evidence the tip's contents are good.
Two stale RESULT.txt files from yesterday's wave-20260928-2321pdt
(arch-20260924-0521pdt, arch-20260927-0521pdt, same scratch dir name
fb2321pdt) were found in the scratch tree, excluded from the tally, and
recorded in the manifest. Remote: zero new refs (origin/tnn-native-lab
bedf8b4a unchanged).

## M3: Interactive survey NONE new: CONFIRM

Provenance: diff 7c11ac5af..HEAD over *.zag; new is the survey record.

Ruling: 166 new or modified .zag files since the 1721pdt pin (all from
the parallel research-lead process), zero with chat/stdin/readline/
interactive patterns. Frozen probe instruments remain the only
chat-capable instruments. tnn_chat FIT staleness 3 of 8 (due at 8 of 8).

## M4: Commit-order self-check VALID: CONFIRM

Provenance: commit record; new is the check result.

Ruling: prereg first commit 7c11ac5af (2026-09-30 00:37:26 UTC)
strictly precedes implementation first commit 847a8f10f (2026-09-30
06:32:23 UTC); merge-base ancestry confirmed. Scoping caveat (skeptic
M4): the check certifies commit order, which is exactly what the
standing rule requires.

## M5: Next step: AMEND (independent adversary before reproduction)

Provenance: queue inherited from the reorientation; new is the concrete
next step.

Ruling: the advocate's pipeline order (reproduction next) is amended.
The skeptic's cited reason stands: reproduction without a harder
adversary adds little information, while an independent adversary
choosing the byte AND a non-first-letter world is the cheapest way to
kill S1/S4. Next wave: independent adversary designs a post-freeze
family (byte of their choosing, plus at least one non-first-letter
diagnosis world), then the frozen binary is re-run under it; step 4
(independent reproduction) follows. The pipeline is not weakened; its
order is informed by information gain, which the mandate ranks above
experiment count.

## M6: Provenance honesty: CONFIRM with two pinned caveats

Provenance: this motion audits the wave's own documentation.

Ruling: the wave's documentation carries machine-checkable provenance:
the port declares cmp verification, the result doc separates new from
inherited, the F2 byte rule was declared pre-run, the ungrounded
"875-regression cell" is disclaimed. The skeptic's two probes are
pinned: (1) the F2 byte-choice rule was implementer-declared, so "no
designer discretion" is self-certified pending the independent
adversary (M5); (2) the K-RV2-5 vacuous-pair quirk is now on the
verdict line (M1). No recycled render or re-certification was presented
as new; nothing in this wave touches the image judge queue.

No frozen bar was weakened. Zero Python in wave work (one disclosed
stale index.lock from the parallel writer's crash, removed before
committing; no evidentiary consequence). No em-dashes in wave
documentation.
