# JUDGE BRIEF: ARENA-BLIND (wave-20261001-2321pdt, ARENA-BLIND lane)

## Provenance

- RENDER_SHA: 453855599c332c85eaaf896f9632888c5f23ca0a17b92415bfb24fdca4ecb3c2
  (sha256 of the frozen audited source roster_contestant.zag as
  extracted via git show from commit 171c45101; the audit subject;
  no new binary was built in this lane)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: ARENA4 BUILD-PASS ROSTER (C15 0.947, zero
  regressions on the other 15 capabilities, 3/3 byte-identical,
  commits 19d9edc87 / 171c45101 / f8d7b9b2e); BATTERY-E3
  E3-ORACLE-DEPENDENT as the mandating result (blind composition
  assembles graphs correctly, but CORRECT selections depended on the
  unmasked verifier t2_try_verify, mandating blind re-examination
  of every construction claim resting on unmasked QUERY evidence)
- NEW_KNOWLEDGE_CLAIM: The arena battery's query mechanism never
  feeds the expected answer to the contestant, so the ROSTER C15
  claim never rested on unmasked QUERY evidence and the ARENA4
  BUILD-PASS stands without a masked re-test.

## Verdict: ORACLE-FREE

The audit (ARENA_BLIND_AUDIT.md, criteria A1..A6, all PASS) shows:

- A1: the 72 sealed test turns carry exactly the fields
  {turn, kind, item, cap, q}; zero carry any exp/answer/key/
  oracle/expected field. The listnames turn is
  {"turn":117,"kind":"test","item":63,"cap":15,"q":"listnames"}.
- A2: the run driver passes the contestant one turn JSON plus its
  own state dir; the answer key goes to the scorer only.
- A3: the frozen turn-protocol contract defines test turns as
  (item, cap, q); the generator emit code constructs exactly those
  fields.
- A4: the frozen ROSTER source parses item/cap/q; item and cap are
  echoed into the reply envelope for scorer mapping, not cognition
  inputs; the listnames handler reads only the learner-state entity
  roster.
- A5: zero verifier-with-expected hits in the frozen source; no
  candidate set and no selection step exist, so the E3 failure mode
  (oracle selection among multiple executable chains) has no
  structural analogue here.
- A6: ROSTER never emits OBSERVE requests; its observe_result branch
  is a no-op exposure that never touches the roster.

Per the frozen decision rule (PREREG_ARENA_BLIND.md, commit
0b95a6601), ORACLE-FREE means the masked re-test branch is not
triggered: the C15 claim never rested on unmasked QUERY evidence,
so there is no unmasked query to mask. The E3 blind mandate is
satisfied for ROSTER by this audit. The ARENA4 BUILD-PASS stands as
scored. No repair is proposed (no-patch-treadmill rule); none is
needed.

## Evidence paths

- Prereg (frozen alone, commit 0b95a6601):
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA-BLIND/PREREG_ARENA_BLIND.md
- Audit record (this lane):
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA-BLIND/ARENA_BLIND_AUDIT.md
- Audited source (read-only, from commit 171c45101):
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA4/roster_contestant.zag
  (frozen sha256 453855599c332c85eaaf896f9632888c5f23ca0a17b92415bfb24fdca4ecb3c2)
- Sealed test turn:
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA4/sealed/world/turns.jsonl
  (line 118)
- Turn-protocol contract and emit code:
  docs/lab/research-lead/overnight-20260928/competitive_arena/world_gen.zag
- Mandating result:
  docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E3/E3_RUN.md

## Commits (local only, never pushed; branch tnn-native-lab)

- 0b95a6601: ARENA-BLIND prereg frozen alone + NAMECHECK
  (commit-order self-check: prereg commit strictly precedes all
  audit-evidence work)
- (this commit): ARENA_BLIND_AUDIT.md + JUDGE_BRIEF.md (no runs,
  no new binaries, no source edits to any lane)

## Caveats and follow-ups

- This audit covers the arena battery query mechanism and the
  frozen ROSTER source at commit 171c45101. It does not re-litigate
  the ARENA4 sealed evaluation, which stands on its own 8 kill
  bars.
- The arena turn protocol's lack of an expected-answer field is a
  property of the battery design (per-turn JSON, scorer-side keys),
  unlike the PF battery's QUERY lines. Future batteries that add
  answer-carrying query fields would need their own blind audit;
  this verdict does not transfer to them.
- ROSTER remains a CANDIDATE with no L3 claim, as recorded in the
  ARENA4 lane (K8). This blind verdict changes nothing about that
  scope.
