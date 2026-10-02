# JUDGE_BRIEF.md: RT-HPIREV2 independent review + adversarial family

## Provenance

- RENDER_SHA: 7be01e25eeabc8bc3f342cab66ba3c7f2641785fc6fb70818fe804f26fb03959
  (sha256 of the primary new evidence artifact, the ADV-S4 sealed
  adversarial transcript adv_S4_run1.txt; runs 2-3 byte-identical;
  the full 18-transcript adversarial matrix is traceable to the
  frozen machinery binary rt_adv_exec_bin da58510e...)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: H-PI-REV2 narrowed single-conflict claim
  BUILD-PASS (wave-20261001-2321pdt, prereg 00b31af53,
  implementation ec52cf1ca, binary
  aee1b6f21a4b5309a3c93e9f66d9c38553bd75db926feeba123207373117ddbc)
  as the reviewed artifact; RT-HPIREV2 is the independent
  red-team second opinion plus the C0-C post-freeze adversarial
  family (seal 8b86b27d2, erratum amendment 1c40232af).
- NEW_KNOWLEDGE_CLAIM: Independent re-verification confirms the
  lane's BUILD-PASS numbers on all five worlds under the frozen
  bars, but the adversarial family breaks the narrowed claim as
  literally stated (a valid single-conflict world whose true
  trigger is not the rank-1 diagnosis fails with fails_total=1,
  and a masked second conflict yields silent success), so the
  claim requires an explicit rank-diagnosability qualifier and a
  probe-dependence qualifier on the bound-trip signal.

## Verdict

Part 1 (second opinion): QUALIFY. The BUILD-PASS verdict stands
on the five tested worlds under the frozen bars as written;
every hash, transcript, commit-order check, and metric value was
independently re-verified and matches. Two qualifications travel
with it: (Q1) the prereg's frozen hash line for D2_FW.txt is a
62-char transcription typo, so the "25/25 verified, all match"
certification sentence is not literally true and needs the
erratum (true hash
2d5083a3c47f0f41fc5f44d3a9e66e02f520db072e74755c6eddc7eddc27fa57);
(Q2) all five lane worlds accommodate the frozen rank-biased
diagnosis by (disclosed) design, so the evidence never tested a
conflict the rank bias does not select.

Part 2 (adversarial family): the bound PARTIALLY SURVIVES.
ADV-S1/S2/S3 (novel base programs, novel consequents, longer
inputs) all PASS with margin: the single-conflict bound
generalizes beyond the lane's four dimensions. ADV-S4 BREAKS the
claim as literally stated: fails_total=1 on a valid
single-conflict world (`PREDICT p!Br -> rrrr [MISMATCH want
pppp]`), loud not silent. ADV-M1 shows the bound-trip signal is
probe-dependent: a masked second conflict yields fails_total=0
with zero detection (silent success claim). ADV-M2 confirms the
explicit trip still fires when the second conflict is probed
alone, mirroring K-SC-B.

## Key evidence

- Prereg 00b31af53 strictly precedes implementation ec52cf1ca
  (merge-base --is-ancestor true); prereg commit contains only
  the prereg file; exactly one lane-dir commit between them.
- Lane binary aee1b6f2..., mechanism dd3cb02d..., machinery
  prefix 8d2b16ab... all re-verified from committed blobs.
- 15 lane transcripts re-hashed: 3/3 byte-identical per world,
  matching the lane's JUDGE_BRIEF; 18/18 stderr files 0 bytes.
- Adversarial seal: 8b86b27d2 (alone, pre-execution), erratum
  amendment 1c40232af (three transcription errors caught by
  pre-execution sha256sum -c; 30/30 verified; no execution
  preceded the amendment).
- Adversarial executor binary
  da58510e0a20d1a2956dc7556dfd5546870cd8e269b945d5a0d01b884f5e1e23
  (frozen machinery byte-verbatim, cognition delta 0).
- 18 adversarial transcripts, 3/3 byte-identical per world,
  exit 0, zero stderr; STAGE lines byte-exact vs sealed files.
- Per-world adversarial transcript hashes in ADV_EXEC_RECORD.md.

## Boundaries

This review does not re-litigate steps 5, 6, or 7; does not
claim L3; does not grant SURVIVES. The adversarial worlds were
designed and validated by the reviewer (independent of the lane);
three pre-freeze design slips were fixed and disclosed in
ADV_SEAL.md. Pure Zag throughout; no em-dashes or en-dashes in
review docs (byte-checked).

No em-dashes or en-dashes appear in this file.
