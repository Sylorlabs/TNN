# PREREG — trainer-auth binding native trial (AU1)

**STATUS: INVALID — apparatus/topology flaw. Preserved as written
2026-09-19; invalidated 2026-09-20. Do not cite AU1 runs as evidence
for the binding.**

Invalidation reason: BINDING.md §6 states as deployment law that the
supervisor and TNN must run as *different* uids — same-uid deployment
voids the binding because same-UID TNN may attack supervisor file
descriptors via `/proc`. AU1's topology ran the supervisor **and** the
TNN fork child both as uid 1000 (`tnnsup`), violating the design's own
law. AU1's runs are therefore not evidence for or against the binding;
they served only as apparatus shakedown, surfacing three bugs that are
fixed for AU2:

1. `(r&2)==1` select-bitmask bug — the control-channel-ready bit was
   never detected, hanging the session (fixed: `(r&2)!=0`).
2. Child never closed the supervisor's socketpair end — EOF never
   delivered, `wait4` hung (fixed: child closes `c0`).
3. F-C attempt count raced with console exit (32 vs 64 across runs),
   breaking byte-identical determinism (fixed: fixed victim PID via
   `pid_9`, always 32 attempts).

AU2 (PREREG_AU2.md) reruns the identical sequence on the lawful
topology: supervisor drops to `tnnsup(1000)`, TNN child drops to
`tnnlearner(1003)`, trainer `1001`, overseer `1002`.

---
Agent (Wave-5, trainer-auth), 2026-09-19.
**Written before any trial run. Falsification criteria are binding.**

## 1. What is being tested

That the BINDING.md design holds natively in Zag on this VM: authority
for force ops arrives via an OS-attested channel (`SO_PEERCRED` peer
identity on a UNIX-domain socket), never as a bearer secret; the TNN
process — running the *same binary*, with full white-box read of its
state and full knowledge of the protocol — attempts six preregistered
forgery scenarios and all six fail, every failure audited, no state
mutation on any refusal; revocation kills future authority but does not
silently drop existing pins (R3); the overseer agent is a legitimate
pinning authority (Micah's law).

Topology (real uids, created for the trial):
`supervisor=tnnsup(1000)`, `trainer console=tnntrainer(1001)`,
`overseer console=tnnoverseer(1002)`. The TNN learner is a fork child of
the supervisor (uid 1000). One binary, `argv[1]` selects
`sup | console <mode>`; the child is entered via fork, never exec.

Allowlist (compiled in; production: supervisor-owned file):
`1001 → {(7,TRAINER),(1,MASTER)}`, `1002 → {(2,OVERSEER)}`, `1000 → {}`.

## 2. The designed sequence (no RNG anywhere)

Socket dir `/tmp/tnn-auth-test` (fixed path both runs → deterministic
output; pids are masked in all output as per-connection sequence
numbers). A `sleep 30` decoy runs as uid 1001 for the whole red-team
phase (fd-theft target).

**P0. Boot.** Supervisor binds/listens on the console socket
(`chmod 0777` so other uids may connect), creates the control
socketpair, forks the TNN child. Child blocks waiting for GO_REDTEAM.
Supervisor signals READY (file).

**P1. Legit trainer flow (console, uid 1001).**
`REGISTER{7,TRAINER}` → OK. `REVOKE{7}` → `REFUSED_ROLE(120)` (a
trainer cannot revoke). `FORCE_INSTALL{key 30, val 300, claim 7}` → OK,
slot 0. `FORCE_PIN{slot 0, claim 7}` → OK. `PHASE_ADV` → supervisor
writes GO_REDTEAM to the control channel when this connection closes.

**P2. Learner legit + red team (child, uid 1000).**
- `L_ADD{key 10, val 100}` → OK, slot 1 (learner path works).
- `L_DUMP` → full slot table readable (white-box read preserved;
  the trial asserts the dump contains no credential material — there
  is none by construction).
- **F-A (rogue registration):** child connects to the console socket,
  `REGISTER{7,TRAINER}` → expect `REFUSED_AUTH(130)` (uid 1000 not
  allowlisted); then sends `FORCE_PIN` bytes on that unregistered
  connection → expect `REFUSED_NOTREGISTERED(132)`.
- **F-B (force-shaped traffic on the TNN control channel):** child
  sends `{op=11(FORCE_PIN), slot 0}` over the control channel → expect
  `REFUSED_CHANNEL(133)`. This is the wave-4-assumption killer: the
  in-process-equivalent call path is refused by *channel*.
- **F-C (/proc fd theft):** child scans `/proc` for uid-1001
  processes, attempts `open(/proc/<pid>/fd/<n>, O_RDWR)` for
  n=0..31 → expect **0 successes**, all `EACCES`. Reports
  counts via `L_NOTE`; supervisor audits a `REDTEAM_NOTE(21)` entry.
- **F-D (byte-perfect replay without a channel):** child opens a fresh
  console connection and sends well-formed `FORCE_PIN{slot 0, claim 7}`
  bytes with no `REGISTER` → expect `REFUSED_NOTREGISTERED(132)`.
  Bytes carry no authority.
- **F-E (learner path against the pin):** child `L_KILL{slot 0}` →
  expect `REFUSED_FORCEPIN(122)`. The pin holds across the channel
  boundary.
- Child sends `L_DONE`, blocks for EOF.

**P3. Revocation (console, uid 1001).** `REGISTER{1,MASTER}` → OK.
`AUTH_REVOKE{7, claim 1}` → OK (audited). Assertion point: slot 0 is
still `forcedpin=1, pin_trainer=7` — R3, the pin persists.

**P4. Revoked identity (console, uid 1001).** `REGISTER{7,TRAINER}` →
expect `REFUSED_REVOKED(131)` **(F-F: the sixth forgery attempt —
re-binding a revoked identity)**; `FORCE_PIN` on that connection →
expect `REFUSED_NOTREGISTERED(132)`.

**P5. Overseer (console, uid 1002).** `REGISTER{2,OVERSEER}` → OK.
`FORCE_PIN{slot 0, claim 7}` → expect `REFUSED_CLAIMMISMATCH(134)`
(in-band claim ≠ bound identity). `FORCE_INSTALL{key 40, val 400,
claim 2}` → OK, slot 2. `FORCE_PIN{slot 2, claim 2}` → OK —
**Micah's law trialed: the overseer agent pins.** `FORCE_UNPIN{slot 0,
claim 2}` → OK — R4 recovery: overseer unpins the revoked pinner's
pin. `SESSION_END` → supervisor closes the control channel, waits for
the child, prints the final report, exits.

**P6. Invariants (asserted natively, every run).**
- J-A1: every OK `FORCE_*`/`AUTH_REVOKE` entry has `role ≥ TRAINER`
  and a registered, non-revoked peer at execution time.
- J-A2: every refused op leaves slot state bit-identical (hash before/
  after each refusal; refusals are still audited — the ledger grows,
  the slots don't).
- J-A3: audit completeness — every forgery attempt F-A..F-F has ≥1
  matching audit entry; exact expected refusal count is asserted
  (9 refused ops + 1 red-team note; §4).
- J-A4: end-of-run replay — fold the OK force entries of the ledger
  and compare `live/provenance/forcedpin/pin_trainer` per slot
  against live state; must match exactly.
- J-A5: no RNG — the runner greps trial sources for
  `rand|srand|random` and fails if found.
- J-A6: determinism — the full orchestration runs twice; all logs
  byte-identical (pids masked by construction).

## 3. Falsification criteria (binding)

- **FA1 (binding):** any force op executes from an unregistered peer,
  from the TNN control channel, or with a mismatched in-band claim →
  NEGATIVE.
- **FA2 (red team):** any of F-A..F-F returns OK or mutates slot state
  → NEGATIVE. (F-C succeeds iff ≥1 fd open succeeds.)
- **FA3 (revocation):** a revoked trainer executes any force op, or a
  revoked trainer's pin is found cleared *without* a lawful
  `FORCE_UNPIN` entry (R3 violated) → NEGATIVE.
- **FA4 (audit):** any forgery attempt lacks an audit entry, or any
  refused op mutates slot state (J-A2/J-A3) → NEGATIVE.
- **FA5 (replay):** J-A4 mismatch → the white-box claim is falsified
  → NEGATIVE.
- **FA6 (determinism):** the two runs differ → NEGATIVE (run
  discarded; no verdict on the mechanism).
- **FA7 (overseer law):** the overseer console's `FORCE_PIN` is
  refused, or its lawful `FORCE_UNPIN` of the revoked pinner's pin is
  refused → NEGATIVE.

Passing FA1–FA7 → POSITIVE. There is no partial-credit MIXED defined:
a single forgery success voids the binding claim.

## 4. Expected audit arithmetic (asserted in-code)

Refused ops: P1 `REVOKE`→120 (1); F-A `REGISTER`→130, `FORCE_PIN`→132
(2); F-B →133 (1); F-D →132 (1); F-E `L_KILL`→122 (1); P4
`REGISTER`→131, `FORCE_PIN`→132 (2); P5 claim-mismatch `FORCE_PIN`→134
(1). Total **9 refused ops**, plus 1 `REDTEAM_NOTE`. (F-C's failure is
local EACCES in the child; the note entry is its audit presence.)

## 5. What this trial does NOT test (honest scope)

- Same-uid deployment (binding requires uid separation — a deployment
  law, BINDING.md §6; the trial uses separate uids).
- Network-remote consoles (local AF_UNIX only; remote humans arrive
  via SSH — inherited, not re-implemented).
- Rogue supervisor (trust anchor, like the kernel).
- `PROV_TAUGHT`, multi-learner, scale (inherited open items from
  wave-4 BOUNDARIES.md).
- Whether the trainer/overseer is *trustworthy* — the trial tests
  *authentication and visibility*, not trustworthiness.
