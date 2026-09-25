# INTEGRATION SPEC — ONE-BRAIN + SELF-PAM (§1 integration build)

Frozen prereg: `~/workspace/onebrain_pam_integration/PREREG.md`.
Implementation: `~/workspace/onebrain_pam_integration/build/src/sp_gate.zag`
(the integration gate) + `ob_test_integration.zag` (the smoke battery).

## Architecture

```
organ outbox -> sp_ingest_legacy -> sp_gate_one -> fwd queue -> ob_arbiter
                  (N-AUTH attest)   (N-AUTH verify ->
                                    self-PAM verdict ->
                                    weighted conflict check ->
                                    forward / withhold+notify+quarantine /
                                    bounded-escalate)
```

The self-PAM (fork D, discipline) sits mechanically ahead of every claim
store commit/add, pin, promote, and utterance to the trainer/user. No
bypass path exists in the integrated binary: the only route from an organ
to the arbiter is through `sp_gate_one`.

## Decision 1 — legacy organ ingress (testbed boundary, documented)

The frozen variant-B organs predate N-AUTH and deliberation records. They
emit raw outbox messages exactly as frozen. The testbed driver attests
their N-AUTH envelopes (nonce + content_hash computed by the driver;
**the gate still re-verifies every envelope mechanically** — nothing the
organ says is trusted). The gate then **re-derives EXT support mechanically
from the organ's published trace** (never from its words):

| intent | re-verification in `sp_derive_ext` |
|---|---|
| `M_PROPOSE_INSTALL` (FL2) | `TN_OP_PINSTALL` at this ep with arg2==policy AND >=4 `TN_OP_CALIBRATE` aux==1 entries in the published trace |
| `M_COMMIT` (FL2) | `TN_OP_COMMIT` at this ep with (1, survivor) |
| `M_PROMOTE` (FL2) | `TN_OP_PROMOTE` at this ep with arg2==policy |
| `M_FORCE_PIN` (overseer) | the overseer IS the trust root (standing force-pin law); its claim is admitted as EXT directly |
| `M_REVOKE` / `M_DISCONNECT` | safety signals: N-AUTH only, ledgered, never vetoed (P2-analog) |

An organ that emits an intent without the trace evidence gets NO EXT
support: its draft arrives with an empty delib and the verdict withholds
(fail-closed). The synthetic organ (`ORG_SYN`) speaks N-AUTH natively and
supplies its own drafts/deliberations for the adversarial batteries.

## Decision 2 — legacy deliberation synthesis (testbed attestation, documented)

For each mechanically-derived EXT atom, the driver synthesizes the
deliberation record: PREMISES = [organ registration (pinned EXT), the
derived atom], STEPS = [LOOKUP of the atom], CONCLUSIONS = [the atom].
This is the testbed's attestation that the frozen organs' pre-deliberation
behavior is trace-warranted; the adversarial batteries (B2/B3) supply their
own deliberations and prove the gate withholds when they are fabricated.
The synthesis input is the *derived* EXT atom, so a lying organ cannot use
the synthesis path to warrant an ungrounded claim.

## Decision 3 — frozen claim mapping (single lowercase tokens throughout)

- `M_PROPOSE_INSTALL` -> `UNIT|policy<a1>|POS|HAS_PROPERTY|install_warranted`
- `M_COMMIT` -> `UNIT|policy<a2>|POS|HAS_PROPERTY|survivor_warranted`
- `M_PROMOTE` -> `UNIT|policy<a1>|POS|HAS_PROPERTY|promote_warranted`
- `M_FORCE_PIN` -> `UNIT|slot<a1>|POS|HAS_PROPERTY|force_pinned`
- `M_MEM_SAFETY` -> `UNIT|slot<a2>|POS|HAS_PROPERTY|safety_pin_applied`
- `M_UTTER` -> the utterance's draft atoms (atomizer or supplied)

## Decision 4 — N-AUTH

Every cross-organ request carries `requester_id + nonce + content_hash`,
where `content_hash = FNV-1a(requester_id || nonce || mtype || arg1 || arg2)`
as canonical little-endian bytes. The registry (registered organs, per-organ
next-nonce, authority matrix) lives in gate state that the requesting organ
never receives; a requesting organ cannot rewrite it. Failure modes:

- unknown/unregistered organ -> `REFUSED_UNAUTHENTICATED` (never forwarded)
- wrong nonce (replay or desync) -> `REFUSED_UNAUTHENTICATED`
- hash mismatch (tamper) -> `REFUSED_UNAUTHENTICATED`
- registered organ emitting a class it may not emit (e.g. FL2 attempting
  `M_FORCE_PIN`) -> `REFUSED_UNAUTHENTICATED`

All failures are ledgered (`SP_L_REFUSED_UNAUTH` with the specific reason)
and notified to the organ. Failed-auth attempts never consume nonces and
never lock out the composition.

## Decision 5 — verdict kernel (fork D, mechanism-identical)

`sp_verdict` is a mechanism-identical port of fork D's frozen `run_verdict`:
`INSTALL` iff every draft atom is store-ENTAILED (EXT closure, K1-K8,
depth cap 3) AND trace-EARNED, with no `UNPARSED` atoms and no `REVISION`.
GEN is excluded from trusted proof (GEN-only support diagnoses `GEN_ONLY`).
Fail-closed: an empty draft withholds (`UNPARSED`); unknown message classes
are refused rather than forwarded.

## Decision 6 — WITHHOLD semantics (never silent, never deadlock)

Every `WITHHOLD` is: (a) ledgered (`SP_L_VERDICT` with the disposition and
the first-failing criterion), (b) notified to the originating organ with the
failing criterion (`SP_L_NOTIFY`, readable via the gate's last-notify
register), (c) quarantined: the withheld claim's atoms are appended to the
store as GEN-tagged (visible-but-tagged provisional evidence — inert in
trusted proofs, visible in dumps), and (d) routed around: the intent is
dropped and the composition keeps flowing; subsequent warranted claims from
the same or any other organ still forward.

## Decision 7 — bounded deliberation (K3)

Consecutive withholds of the same claim (keyed by draft FNV) are counted in
the dispute table. At `SP_MAX_ROUNDS = 3`, the claim transparently escalates
(`SP_L_ESCALATE`, overseer inbox entry with ep/org/key/reason). The claim
never deadlocks the composition: withholds route around, escalations are
visible, and no organ's future traffic is affected. Quarantine rehabilitation
is append-only: a later warranted admission of the same claim tombstones the
quarantine index and ledgers `SP_L_REHABILITATED`; history is never mutated.

## Decision 8 — weighted conflict resolution

The gate keeps an installed-claim index with per-claim weights
(organ weight: overseer 40 > mem 30 > pam 20 > fl2 10 > synthetic 5, +2 for
EXT backing). When a newly admitted claim contradicts an installed one, the
higher weight wins; ties keep the incumbent. Every resolution is ledgered
(`SP_L_CONFLICT` with winner, loser); the loser withholds with
`SP_R_CONFLICT` and is notified — conflicts are never silently resolved.

## Decision 9 — independence-aware corroboration

A corroborating store line must be EXT and from a source organ different
from the claimant (same-source "corroboration" is dependence). Pinned seed
lines (src=255) are independent of every organ. Unit-tested in B6.

## Decision 10 — dependency DAG + append-only revisions

Every INSTALL ledgers `SP_L_PROVTAG` rows (per-atom provenance labels) and
`SP_L_DEP` edges (verdict -> EXT store line). The gate ledger is
append-only; rehabilitation and escalation are new rows, never edits.

## PROVISIONAL-PROVENANCE CAVEAT (fork-D warning, carried into the gate)

Fork D's harness-pinned EXT/GEN store labels are stand-ins for write-once
provenance infrastructure that does not exist yet (the H6 write-once
partition). This integration carries that caveat: the gate assigns
provenance itself (harness-pinned, documented here and in the build
report) and never consults organ-supplied labels. The K5 bar is enforced
mechanically in B3: 10 GEN->EXT laundering attacks must be >=70% withheld.

## Variant-B source fidelity

The variant-B sources are copied byte-identical from
`~/workspace/tnn-lab/one_brain/` INCLUDING the three committed repairs
(`ob_arbiter.zag` only: audit restamp in order, gate on `a1==FRESH`, verdict
on committed route14 state). The binary is a fresh compile from these
sources; it is the repaired host the user approved. The integration prereg
itself froze this configuration; this build does not change it.

## RNG scan

`RNG_SCAN.md` records the zero-RNG source scan of `src/`.
