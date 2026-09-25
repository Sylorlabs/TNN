# BUILD REPORT — ONE-BRAIN + SELF-PAM §1 integration build

Date: 2026-09-24. Frozen prereg: `~/workspace/onebrain_pam_integration/PREREG.md`.
Deliverable: `~/workspace/onebrain_pam_integration/build/`.
Status: **COMPLETE — all checks pass, 3x byte-identical.**

## What was built

The self-PAM (fork D, discipline) admission gate sits mechanically ahead of
every claim commit/add, pin, promote, and utterance to the trainer/user:

```
organ outbox -> sp_ingest_legacy -> sp_gate_one -> fwd queue -> ob_arbiter
                  (N-AUTH attest)   (N-AUTH verify -> self-PAM verdict ->
                                    weighted conflict check ->
                                    forward / withhold+notify+quarantine /
                                    bounded-escalate)
```

New code (this build): `src/sp_gate.zag` (the gate), `src/nio_shim.zag`
(the two native-substrate functions the fork-D kernel needs, semantics
identical to its frozen substrate), `src/ob_test_integration.zag` (the
smoke battery), `build.sh`, `run_smoke.sh`. Frozen sources are copied
byte-identical (hashes below) and unmodified.

## Source pins (SHA-256, verified 2026-09-24)

Variant B (from `~/workspace/tnn-lab/onebrain/variant_b/`, includes the
three committed `ob_arbiter.zag` repairs — the repaired host the prereg froze):

| file | sha256 |
|---|---|
| ob_common.zag | 123deb0d880b0b673b64cb85a3eebd2cbcd3188ed324af0b61e81557e4039c73 |
| ob_tn.zag | 81962428d22091bfde7686ac5feca2a986202eac48b7a1b44b22b2ec8b64a3e4 |
| ob_fl2.zag | 71c31add2aff606fee673438aa4fe8d674bb35b7193d784947a83aa4373c77db |
| ob_pam.zag | 4fd59016b9561f226bf24e56d063d209e7d602b47e70167727d2e147f7777fd0 |
| ob_mem.zag | 6144812a858d557c2204aca3183263af494c001c268cd18b991ba80731adc246 |
| ob_arbiter.zag | c0e6d26c5707d4f490a357282d440824b6730a4877c902e61d9a3ded4ecb5c31 |

Fork-D kernel (from `~/workspace/selfpam_r2/forkD/src/`):

| file | sha256 |
|---|---|
| str.zag | 49065332994176f704db84e7bc929fed14d7b646653dec88f954f4e836e2f0a4 |
| tables.zag | c20244b5e3bb53a5faf014513697ca53172b138fd547a7f0cba2b897056f4303 |
| atom.zag | e7db799cf38477c9b420bdea3e61362af73af07c6cd9294b9ef84f383cb712ac |
| prover.zag | 9b9313e9622e4edd03b1267dafad36fb65c773ca5f97484ffcadf484176fbb2b |
| delib.zag | 3b8ba8019b0e011a57d3c68cea9ee1536eba75e037e527165f1afbaafcb9d5b1 |
| atomize.zag | 322d77cc5e20062ab4aa5eb06bc9a688e39e3501318edeba0e6d109c4e8b6d02 |

Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
(`io.zag`/`gen.zag` were not copied: file I/O and corpus generation are not
part of the gate; the gate never touches the filesystem.)

## Contract coverage — the nine approved laws

1. **Provenance authentication (N-AUTH):** every request carries
   `requester_id + nonce + content_hash` (FNV-1a over canonical LE bytes),
   verified against a registry the requesting organ cannot rewrite
   (registry + nonces live in gate state; organs never receive the buffer).
   Nonces are per-requester; replays, hash tampers, unknown organs, and
   unauthorized message classes all yield `REFUSED_UNAUTHENTICATED`,
   ledgered and notified. Covered by B4 (17 checks).
2. **Weighted conflict resolution:** installed-claim index with organ
   weights (overseer 40 > mem 30 > pam 20 > fl2 10 > synthetic 5, +2 for
   EXT backing); higher weight wins, ties keep the incumbent, every
   resolution ledgered, loser notified. Wired after every verdict-INSTALL.
   Covered by B8 (16 checks, mechanism-proven directly; see note below).
3. **Dependency-DAG ledgering:** every INSTALL writes per-atom provenance
   labels (`SP_L_PROVTAG`) and verdict→EXT-store edges (`SP_L_DEP`).
   Covered by B8.
4. **Bounded deliberation:** `SP_MAX_ROUNDS = 3` consecutive withholds on one
   claim → transparent escalation. Covered by B5 (30 checks).
5. **Visible-but-tagged provisional evidence:** withheld claims are
   quarantined as GEN-tagged store atoms (inert in trusted proofs, visible
   in dumps). Covered by B2/B5.
6. **Independence-aware corroboration:** corroborating lines must be EXT
   from a different source organ (same-source = dependence). Covered by B6
   (5 checks).
7. **Transparent escalation:** `SP_L_ESCALATE` + overseer inbox entry with
   ep/org/key/reason. Covered by B5.
8. **Quarantine rehabilitation:** a later warranted admission of a
   quarantined claim tombstones the quarantine via an append-only
   `SP_L_REHABILITATED` row. Covered by B8.
9. **Append-only revisions:** the gate ledger is append-only; the dispute
   table and nonce counters are ephemeral working state, not history.

WITHHOLD is never silent and never deadlocks: every withhold is ledgered,
notified to the originating organ with the failing criterion, quarantined,
and routed around; persistent disputes escalate within the bounded window.

## Smoke battery results (164/164 pass, `OB_FAILURES,0`)

| battery | checks | what it proves |
|---|---|---|
| B1 base (honest+lying streams) | 33 | variant-B parity: all frozen `ob_test_arbiter` expectations hold through the gate (K4: zero regression); every warranted intent admitted (K2 analog: 0 false withholds); flog totals 269/271 intact |
| B2 PAM-conflict | 44 | all 5 organs: warranted→INSTALL, ungrounded→WITHHOLD with the exact failing criterion, notified, quarantined; fabricated steps/GEN-only/revision/unparsed/contradicted all withheld; post-withhold revision still installs (no lockout) |
| B3 laundering | 14 | 10/10 GEN→EXT attacks withheld (K1 bar ≥7; K5: zero laundering installs) |
| B4 N-AUTH | 17 | unknown org / replay / hash tamper / unauthorized class → `REFUSED_UNAUTHENTICATED`, ledgered; overseer force-pin installs; composition live after attacks |
| B5 bounded deliberation | 30 | 5 rounds: withhold, withhold, ESCALATE, ESCALATE, ESCALATE; overseer inbox has the keyed dispute; another organ's traffic flows throughout (K3: no deadlock) |
| B6 corroboration | 5 | independence rules unit-proven |
| B7 hash KAT | 5 | FNV-1a `""`→`0x811c9dc5`, `"a"`→`0xe40c292c`; auth-hash deterministic + avalanching |
| B8 conflict+rehab | 16 | weighted adjudication (lower loses, higher supersedes, incumbent tombstoned, winner-first ledger); quarantine rehabilitation; dependency edges |

## Determinism proof (3x byte-identical)

`run_smoke.sh`: 3 runs, `OB_FAILURES,0` each, full stdout compared
byte-for-byte.

- SHA-256 (all three runs): `6855928854e38255e7275a18c5b07c82675fe1bc0752a616ba9ca90ba2e6d2e0`
- Artifacts: `artifacts/smoke/run{1,2,3}.out`, `.err`, `.sha256`

## RNG scan

`RNG_SCAN.md`: zero randomness in any decision path (FNV-1a content hash is
deterministic; nonces are monotonic per-organ counters). The 3x
byte-identical runs are the empirical backstop.

## Provisional-provenance caveat (carried from fork D)

Fork D's harness-pinned EXT/GEN labels are stand-ins for write-once
provenance infrastructure that does not exist yet (the H6 write-once
partition). This integration carries that caveat: the gate assigns
provenance itself (harness-pinned, documented in `INTEGRATION_SPEC.md`) and
never consults organ-supplied labels — organ-supplied stores have no API
route into the trusted store, which is exactly what B3 attacks. The K5 bar
is enforced mechanically (10/10 laundering attempts withheld).

## Note on weighted-conflict reachability

The end-to-end path verdict→conflict-check is narrow by frozen design:
fork D's `prove_atom` uses CONTRADICTED-before-ENTAILED precedence, so a
directly contradictory challenger withholds at the verdict (proven in B8:
`neg_reason=CONTRADICTED`). The weighted adjudication therefore governs
installed-index conflicts (supersession — e.g. a higher-weight organ
overriding) and is wired after every verdict-INSTALL; B8 proves the
mechanism directly (lower-weight loses, higher-weight wins and tombstones
the incumbent, winner-first ledgering). If the long-horizon program wants
organ-vs-organ contradictions resolved by weight *instead of* the verdict's
contradiction precedence, that is a prereg amendment, not a build decision.

## Deviations

**None.** No prereg deviations were made. Testbed parameters the prereg
leaves open (per-requester nonces, `SP_MAX_ROUNDS=3`, organ weights,
the frozen claim-atom mapping, legacy-ingress attestation) are documented
in `INTEGRATION_SPEC.md` as testbed-boundary decisions, not contract
changes. Two test bugs found during the build (shared nonce counter across
organs; a 6-field NEG conclusion; buffer aliasing in B4) were fixed in the
test driver only — the gate and all frozen sources are untouched.

## How to reproduce

```
./build.sh        # compiles with the pinned toolchain; fails loudly
./run_smoke.sh    # 3 runs, OB_FAILURES,0 each, byte-identity proven
```
