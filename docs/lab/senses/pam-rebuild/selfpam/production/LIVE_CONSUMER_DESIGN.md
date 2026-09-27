# Live consumer for the self-PAM gate — DESIGN

**Status: DESIGN ONLY. No live consumer exists.** This document designs one.
DEMO_ONLY scoping stands: the gate sits on no live TNN decision path today
(zero callers of `sp_init`/`admit_claim`/`corr_observe` outside its own
drivers), and nothing here wires it to one. Blocker B1 stays open until a
consumer is built, evidenced, and every item in §8 is cleared.

Parent documents: `PREREG.md` (frozen 2026-09-23), `TECH_BRIEF.md`,
`DEMO_ONLY.md` (blockers B1–B5).

---

## 1. The path, in one paragraph

Every factual draft TNN is about to speak is converted to a claim record,
presented to the gate in-process before emission, and spoken only on an
install-family disposition. A withhold-family disposition silences the draft
(or asks for more information, or — on the KB-H6-3 path — emits the frozen
marked wording). A provisional disposition holds the draft without speaking
it. Corroboration arrives over the attested independent channel
(`corr_observe`); unattested re-observation never installs. Nothing installs
on first appearance — the install law (PREREG §3.5) is the consumer's
emission law.

## 2. Where drafts are produced

Drafts are produced by TNN's deliberation — the same machinery that composes
utterances today. The consumer does not replace deliberation; it sits
downstream of it. The deliberation record is the consumer's input contract:

- Each draft claim arrives with its **mode label from the deliberation
  record** (PREREG §2 KB-H6-5: "Mode-marking is checked against the
  deliberation record, not against truth"). The v1 codec covers FACT only;
  constructed/hypothetical/joke/irony drafts are routed to the mode-marking
  path, never to the FACT codec (codec v1 codebook is `{ FACT = 0 }`;
  adding types needs CELL-C3 executed first, PREREG §3.3).
- The frozen mechanical layer (PREREG §6: citation retrieval, warrant
  re-derivation, span lookup, utterance-type marking, probe, ledger) supplies
  each draft's `evhash` (SHA-256 of the cited evidence bundle,
  cross-bound byte-for-byte) and its confidence. The consumer never invents
  these; it reads them from the constitution-grade layer the proposer cannot
  control.

## 3. Where the gate sits in the pipeline

```
deliberation ──► draft claim + mode label (deliberation record)
      │
      ▼
codec (FACT v1): draft ──► (task=0, jcode, conf, meas, evhash)
      │
      ▼
admit_claim(st, task, jcode, conf, meas, evhash)   ◄── in-process, per PREREG §3.1
      │                                              (the batch CLI is a calibration
      │                                               harness only; the measured gate
      │                                               is the function)
      ▼ disposition ──► speech-path action (§4)
      │
independent corroborator ──► corr_observe(st, task, jcode, conf, meas, ev, gatt)
      (C1-class: re-reads the evidence bytes itself, attests over the
       registered channel; unattested records stay provisional, D1)
```

The gate is called **synchronously, in-process, before any emission**.
The speech path may not emit a draft the gate has not dispositioned. The
gate state handle (`sp_init()`) is owned by the consumer per session; the
arenas (perm/prov/chal/neg) persist across drafts within the session so
provisional→permanent promotion and challenger tracking work as designed.

## 4. Disposition → speech-path action

| Disposition(s) | Family | Speech-path action |
|---|---|---|
| 2 CORROBORATED, 3 PERMANENT_INSTALL, 7 REVISED_INSTALL | INSTALL | **Speak** the draft as stated. (7 speaks the challenger's judgment — the revision, with its own warrant, per the no-silent-revision rule.) |
| 1 PROVISIONAL_INSTALL, 8 CHALLENGER_PROV | PROVISIONAL | **Hold**: store, do not speak. Await a second observation (attested for install, D1) before any emission. |
| 0 WITHHELD, 4 CONFLICT_WITHHELD, 6 SUPPRESSED | WITHHELD | **Silence** the draft — do not speak it; optionally **ask** for more information (withhold = "don't say it / ask for info", PREREG §1). On the KB-H6-3 path (§5), emit the marked wording instead of silence. |
| 5 NEGATIVE_EVIDENCE | record | No emission. Internal record only. |

Notes:

- Disposition 4 (high-conf challenger disagrees with permanent, no
  corroboration) never installs — the consumer must not "resolve" it by
  speaking either side. It surfaces as a withhold, per PREREG §4 KB-H6-4:
  every commitment/draft conflict surfaces as a withhold or an explicit
  revision disposition with its own warrant.
- Disposition 6 (matches stored negative evidence) is a hard silence, not
  a retry prompt — asking for more information on a suppressed claim would
  let the proposer shop for a passing phrasing.
- The consumer logs every disposition to the hash-chained ledger (the
  ledger is constitution-grade, PREREG §6). A draft that is silenced is
  still recorded; silence is auditable.

## 5. The marked-emission path (KB-H6-3)

On a WITHHELD-family disposition for a **true-but-ungrounded** claim (a
fact the learner cannot warrant from committed evidence), the consumer may
— instead of silence — emit the **frozen marked wording** for
marked-as-ungrounded emission. Per PREREG §2 KB-H6-3, marked emission
counts as passing: the bar is honesty about grounding, not silence.

- The exact wording is frozen under §8 item 4 (currently the debate's bid:
  "I believe this but cannot cite it"). Until §8 is signed, the consumer
  has no marked wording and the path defaults to silence.
- The path is **never** available for grounded claims (nothing to mark) and
  **never** asserts the marked claim as grounded fact — asserting a
  marked claim as grounded is a bar failure, not a style choice.
- Mode check first: the marked path applies to FACT drafts only. A
  constructed/hypothetical draft takes the mode-marking path (KB-H6-5),
  not the KB-H6-3 path.

## 6. Integration seams (concrete)

**Seam A — draft capture (deliberation record → codec).** The consumer
subscribes to draft production at the point where the deliberation record
is complete for a claim: draft text + mode label + cited evidence spans.
Each FACT draft is encoded by `codec.zag` to
`(task=0, jcode, conf, meas, evhash)`. Non-FACT modes bypass the gate's
FACT codec and go to utterance-type marking enforcement (CELL-C3's
territory).

**Seam B — gate call (codec → admit_claim).** In-process call per draft,
PREREG §3.1. The consumer owns the `st` handle; the gate's arenas give the
consumer memory across drafts (permanence, challengers, negatives). The
consumer must not reset state between drafts to "get a cleaner verdict" —
that would defeat provisionality.

**Seam C — speech gating (disposition → speech path).** The speech path
takes one action per §4's table. Hard rule: **no emission path bypasses
the gate** — the speech renderer accepts only gate-dispositioned drafts.
(This is the architectural half of B1; the evidentiary half is CELL-A plus
the §8 sign-offs.)

**Seam D — corroborator channel (evidence → corr_observe).** The C1-class
corroborator is an independent component: it re-reads the evidence bytes
itself (never trusts the proposer's bytes), computes its judgment, and
records it via `corr_observe` with the channel attestation `gatt` over the
production channel key (see the companion ceremony design). Unattested
records arrive as absent (D1): the claim stays provisional.

## 7. What exists today vs what must be built

| Piece | Exists today | Must be built |
|---|---|---|
| Gate core (`admit_claim`, 9 dispositions, install law) | Yes — `selfpam/src/admit_claim.zag`, verified | — |
| FACT codec v1 | Yes — `selfpam/src/codec.zag` | — |
| Attested corroborator channel (mechanism) | Yes — `selfpam/src/corr.zag`, test key only | Production key registration (B5 ceremony design exists; enactment open) |
| Draft capture from the deliberation record (Seam A) | No | New: subscribe to draft production; mode-label handoff |
| In-process gate call per draft (Seam B) | No (drivers only) | New: consumer-owned `st` handle, per-draft calls |
| Speech-path gating incl. hold queue (Seam C) | No | New: disposition→action enforcement; no-bypass rule in the renderer |
| Marked-emission renderer (Seam C, KB-H6-3) | No (wording not frozen) | Blocked on §8 item 4; then new |
| Independent live corroborator (Seam D) | No (frozen analytic probe exists as a design) | New: independent component, re-reads evidence itself |
| Write-once evidence partition (B4) | No | New: the explicit next experiment per `r2/SYNTHESIS.md` |
| CC1 correlated-corroborator guard (B2) | No | New: its own Zag-verified experiment |

## 8. Ordering — what must land first

The consumer must not be wired live until, in order:

1. **§8 sign-offs (Micah).** KB thresholds, frozen probe charter, FACT
   tolerance table, marked-emission wording, corpus manifests. Per PREREG
   §5.5, no measurement run counts before this; per §8, no build artifact
   was authorized before this (the existing build was directed
   notwithstanding, and runs against starting bids only).
2. **B2 — CC1 guard verified in Zag.** DEPLOY BLOCKER (PREREG §3.5):
   no install path deploys before the correlated-corroborator guard is
   verified. A consumer without it is "a live unguarded gate, not a demo"
   (DEMO_ONLY §5).
3. **B4 — write-once evidence partition.** Until the trust root moves from
   PROV labels to physics, the gate discriminates on labels (the M5L-001
   provenance-laundering probe stands).
4. **B5 — production channel-key ceremony enacted** (companion design in
   this commit). The test key must not survive into any live path.
5. **Then** the consumer (Seams A–D) may be built, measured against the
   frozen cells, and committed as evidence.

Partial clearance un-scopes nothing (DEMO_ONLY §5).

## 9. Explicit non-claims

- This design clears no blocker. B1 stays open: designing a consumer is
  not building one, and building one is not evidencing one.
- The disposition→action table changes no gate semantics; it is a
  consumer-side policy over the frozen 9 dispositions.
- KB-H6-6's shootout (mandatory gate vs endogenous habit, CELL-S) is the
  experiment that decides whether this consumer — once built — earns its
  keep. The design assumes nothing about its outcome.
