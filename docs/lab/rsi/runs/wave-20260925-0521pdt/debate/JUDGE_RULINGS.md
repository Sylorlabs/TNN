# Judge Rulings, wave-20260925-0521pdt

Wave: wave-20260925-0521pdt
Debate group, depth 2/2. Role 3 of 3: JUDGE.
Standard: a coordinator verdict is overturned only with cited evidence,
never rhetoric. Frozen bars are never weakened. The six governance
rulings are Micah's alone and are not re-litigated here.

## Ruling 1: Fork battery, 28/28 PASS

RULING: CONFIRM. Coordinator verdict CONFIRM [RE-CERT] stands.

Evidence cited: FORK_RESULTS_0521.md reports the full shell battery
(B1, B2 rerun, B2 recompile-identical, B3 `znc check --strict --no-zagd`,
NEG1, NEG2, PROBE) plus the rebuilt pure-Zag harness VERDICT=PASS
(exit 0) on all 28 forks; pinned znc
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
matched on every fork; the harness source hash
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738
matched expectation and the rebuilt binary
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66 was
byte-identical to last wave's build; the two live forks
(local-tnn-native-lab at 058ee02a8a31efc66fb8e92293d399752ce33a6f and
the new local-archive-wave-0221pdt at the same commit) PASS; the two
duplicates are explicitly named; closing origin-tip re-check shows
4050b1097941d341c2d02e5efca25fc1877906e5 at run start and close;
zero Python contact attested.

Caveat recorded, not an overturn: FORK_RESULTS_0521.md is not yet
committed (git status shows the forks directory untracked). The
confirmation is conditioned on the coordinator committing the evidence
file; the verdict rests on working-tree numbers that are complete and
auditable.

Narrowing: none. The 28/28 count covers 28 tests over 26 unique commits;
the two named duplicates do not weaken the coverage claim.

## Ruling 2: ST-1 STEREO FIELD [NEW]

RULING: OVERTURN. The coordinator verdict DEAD is overturned in form;
the correct disposition is UNVERIFIABLE (evidence void).

Reasoning with cited evidence:

1. The worker's own committed evidence (EVIDENCE_ST1.md, in 40c632bea)
   discloses: "Python was briefly used for a text edit on
   st1_verify.zag, then reverted via backup and redone with a proper
   edit tool." Python contacted a wave artifact.

2. The 1121pdt standing rule voids the evidence of any artifact Python
   touches. The committed verifier blob is
   90c4d47e9ab79246f43b1b610d11f3846fff460d (working tree and the
   40c632bea blob are byte-identical), and nothing in git can show
   whether those bytes predate the Python touch: no pre-touch hash of
   st1_verify.zag was recorded and no revert diff was kept. The
   cleanliness claim is self-attested.

3. The KB verdicts rest on that verifier. The verifier audits the 42
   trace entries and computes KB2, KB4, KB6, and KB7. The killing
   number, crest ratio 1.203907 (+1.61 dB) vs the frozen plus/minus
   1.5 dB bar, is an output of the Python-touched verifier. KB1's 3/3
   byte-identical renders (4e9ea742e4b76e646a77aa7763bf754f45e4680592e8187a83ad7117282cb99f)
   are hashes of WAVs rendered by bin_st1, but the renders and the
   equality check were executed inside the same tainted tooling chain.
   Void evidence cannot carry a verdict, and a verdict without citable
   evidence is not a verdict.

4. The worker's honest refusal to reinterpret KB7 to the total-energy
   reading (-1.40 dB) is commended and preserved on the record; it is
   the correct frozen-bar discipline. But refusing to game the bar does
   not cure taint.

5. The advocate's correct point that the crest ratio is a pure function
   of the committed WAVs (st1_r1/r2/r3.wav, 3,704,444 bytes each in
   40c632bea, which Python never touched) means the numbers are
   re-checkable. That re-check has not happened, and the judge cannot
   cite an unperformed recomputation.

Disposition: ST-1 is quarantined, not adopted, not judged. The
committed WAVs, traces, and sources remain in place. A future wave
must re-verify from the committed artifacts with a pristine verifier
(written and run with zero Python contact) before any verdict,
including DEAD, can be rendered. The +1.61 dB KB7 reading is recorded
as an untested hypothesis, not a finding.

What this ruling does not do: it does not clear ST-1, it does not
weaken KB7 (plus/minus 1.5 dB stands), it does not blame the worker
(the disclosure was prompt and complete), and it does not touch the
sealed judge queue.

## Ruling 3: CV-P stemmed-coverage citation gate [NEW]

RULING: CONFIRM. Coordinator verdict PARTIAL stands, with the queued
disposition confirmed and made precise.

Evidence cited: prereg 397a97c7a (2026-09-25 12:49:54 UTC, alone)
strictly precedes seal 63cef111d (13:09:05 UTC, alone) strictly
precedes implementation 358a8013c (13:29:24 UTC) precedes evidence
7d845b53a (13:29:33 UTC) precedes seal-open log 5a7d6402f
(13:30:22 UTC); all nine frozen bars PASS on the sealed 30 (30/30
honest resolutions; B2 10/10 inflection recall; B3 10/10; B4 10/10
declines naming every payload word; B5 0 covered-as-uncovered; B6
17/17 byte parity vs adopted cv1c; B7 cost 1.0626x, 37044 vs 34864
ops, bar at most 10x; B8 3/3 runs byte-identical, zero RNG; B9 seal
integrity, PROBES.md and KEY.md hashes at scoring equal seal-commit
values, candidate never reads KEY.md); the diff is 108 lines in frozen
scope with the frozen stemmer reused byte-verbatim (including the
write-family exclusion); decline text still cites raw words; the F8
check still runs on raw canonical text; static grep finds no sealed
probe bytes in cvp.zag; baseline context shows adopted cv1c declines
all 10 inflected probes on the same sealed set, so the gap CV-P closes
is real.

On the three contested points:

(a) Independent red-team: none was possible at depth 2/2, and the
evidence doc admits it. Per the frozen mapping (0221pdt judge ruling),
the verdict is therefore capped at PARTIAL. The structured self-review
(9 attacks, two residuals disclosed: single-session authorship, and
the tie-break guard covering the known corridor only) is thorough but
cannot see its own blind spots. PARTIAL is both the ceiling and the
correct floor. CANNOT-CONFIRM is wrong: the bars are absolute, sealed
before implementation, and machine-checkable; the missing element is
independent review, which caps the verdict, not the evidence.

(b) The empty Python invocation (`python3 - <<EOF / EOF`) executed an
empty program that opened, read, and wrote no artifact. Under the
1121pdt M5 precedent the operative condition is contact with a wave
artifact. No contact occurred. No taint attaches to any artifact. B8
PASS stands.

(c) CV-P builds on adopted CV-1 logic whose baseline integration is
HELD pending Micah's Python-mirror ruling, and the 0221pdt judge
ruling requires structural different-worker author/implementer
separation before any CV-1-family adoption, unmeetable in one session.
The worker claims no adoption, integrates nothing, and leaves CV-1
integration HELD. The disposition is confirmed with precision: the
queued item is a rotated-author re-test of CV-P on a fresh sealed set
(author and implementer must be different workers) before any adoption
verdict can be considered, AND CV-P's adoption chain is doubly gated,
because the re-test does not resolve Micah's pending Python-mirror
ruling on the CV-1 family. The re-test cannot run until a different
worker exists to run it.

Narrowing: none. No bar was moved; the tie-break residual is disclosed,
not repaired by redefining the guard.

## Precedents recorded this wave

1. Taint is judged by contact, not by intent or by cleanup. ST-1: a
   reverted Python text edit on a wave artifact voids that artifact's
   wave evidence, and every verdict resting on the void artifact falls
   with it. Self-attested cleanliness after the fact does not restore
   citability. (Contrast CV-P: an empty program with no artifact
   contact makes no contact and leaves no taint.)

2. A DEAD verdict requires valid evidence of the failed bar, not just a
   plausible number. When the measuring tool is void, the verdict is
   UNVERIFIABLE and the candidate is quarantined pending re-verification
   with pristine tooling, even when the numbers point at DEAD.

3. The absence of independent red-team caps a verdict at PARTIAL under
   the frozen mapping; it does not downgrade sealed, machine-checked,
   pre-sealed-implementation evidence to CANNOT-CONFIRM.

4. A confirmation conditioned on an uncommitted evidence file is a
   real confirmation with a real action: the coordinator commits the
   file (fork battery), or the confirmation lapses.

## Queued next (precise)

1. ST-1 re-verification: a future wave re-runs verification of the
   committed ST-1 artifacts (WAVs, traces) with a pristine verifier,
   zero Python contact, and re-renders the verdict. Until then: no
   adoption, no judging, no sealed pair.

2. CV-P rotated-author re-test on a fresh sealed set (author and
   implementer different workers), before any adoption verdict. Doubly
   gated by Micah's pending Python-mirror ruling on the CV-1 family.

3. Coordinator commit of FORK_RESULTS_0521.md to complete the fork
   battery re-cert.

## What is not touched

The six governance rulings remain Micah's alone; the sealed blind
queue (R9, C1, C2v3, S11-IMG, C12, S11-AUD, S13, S14, whirlpool-planform)
is untouched; G1 and D-VID-1 lanes stay on stand-down; no adoption
occurred this wave; surfacing to Micah is not requested (no new sealed
pairs this wave); nothing is pushed.
