# Honest boundaries — trainer-console (TC1)

What this investigation does **not** claim. Stated so the next step
doesn't build on air.

1. **Channel binding is assumed, not proven.** The trial models the
   trainer as an explicit `caller`/`trainer` argument; the role gate is
   proven *given* that argument. The real console still needs: how a
   human proves `trainer_id` (auth), how the channel prevents replay of
   a trainer's signed op, and how trainer identities are issued/revoked.
   Until that exists, "trainer A did it" is a ledger field, not an
   authentication fact.

2. **`PROV_TAUGHT` is a reserved enum, not a mechanism.** The verified
   teaching channel's commit op (wave-3 teaching-without-tables) is the
   rightful writer; this trial never writes it. The forced-vs-taught
   distinction in reads assumes that op exists and is correct.

3. **Single partition, single learner.** No `owner`/user dimension (the
   wave-3 separation machinery is compatible — provenance would be one
   more snapshot word — but not composed here), no concurrent learners,
   no serialization discipline beyond the append-only ledger.

4. **Scale is argued, not run.** Per-op costs are O(CAP) slot scans;
   the integrity scan is O(CAP + audit_n) and runs on demand, not
   per-op. CAP=64 here. The named next scale test: CAP=4096 with the
   audited key-index (wave-3 §7), a 100k-op soak, exact replay at the
   end, and the fail-closed ledger refusal exercised. The contradiction
   scan is the component that most wants the index at 100x.

5. **Two-level authority is a model, not a policy.** TRAINER/MASTER
   captures "the pinning trainer or a higher authority" and nothing
   richer — no delegation, no quorums, no time-bounded pins, no
   break-glass. Real deployments will want at least expiry/renewal on
   pins; specified as open, not designed.

6. **The checker flags; it does not resolve.** Read precedence
   (SELF > TAUGHT > FORCED, conflict → RC_CONFLICT with the system's
   value) is a simple honest-answer rule. Full contradiction *resolution*
   (re-executing both sides' supporting traces, per wave-3 §7) is future
   work; the flag is the interface it would consume.

7. **Rogue master is out of mechanism.** See SAFETY_ARGUMENT.md
   scenario 4b: the design bounds and exposes misuse up to the highest
   implemented authority, then stops. Organizational controls above
   that are not this track's business, but they are *somebody's*.

8. **The stale-snapshot guard has a known edge.** If a trainer write
   lands on a slot and is later erased (slot empty again), a subsequent
   TNN rollback of an older learner mutation on that slot will see a
   matching after-state (empty) and restore — no live trainer content
   is clobbered, but the restored content postdates a trainer touch of
   the slot. Acceptable per the analysis in SAFETY_ARGUMENT.md, but
   worth a dedicated check in the scale soak.

9. **No liveness / availability argument.** Fail-closed ledger
   (refuse new mutations when full) is implemented; what the *system*
   does when the trainer console is unavailable, and how a halted
   ledger recovers, are not addressed.

## Recommended next steps (ordered)

1. **Compose with the teaching channel** (wave-3): one store, `ADD`
   (SELF), verified-commit (TAUGHT), and force ops (FORCED) together;
   trial the three provenances interacting, including a taught-then-
   force-contested key.
2. **Channel binding design**: trainer identity/auth for the console;
   preregister what "authenticated trainer op" means before building.
3. **Scale soak** (item 4 above) with the audited key-index.
4. **Pin lifecycle**: expiry/renewal semantics for force-pins, so a
   lock cannot outlive its justification silently.
