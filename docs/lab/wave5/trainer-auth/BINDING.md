# Trainer-auth binding design (Wave-5, investigation 11)

Agent (Wave-5, trainer-auth), 2026-09-19.
Status: design, pre-trial. Preregistered in `PREREG.md` before any run.

## 0. The undesigned piece

Wave-4's trainer console (`wave4/trainer-console/OP_SPEC.md`) proves the
*structural* role gate **given** a `caller`/`trainer` argument — but the
binding of `trainer_id` to a real identity is assumed (their
BOUNDARIES.md §1: "the real console still needs: how a human proves
`trainer_id` (auth)... Until that exists, 'trainer A did it' is a ledger
field, not an authentication fact"). This investigation designs and
trials that binding.

Micah's law (adopted regardless of the strength-trial outcome): an
external party — human, trainer, **or an overseer agent** (like the agent
running this lab) — can make a memory non-erasable. The role gate must
therefore admit overseer-agents as a legitimate pinning authority
alongside humans/trainers.

## 1. The hard constraint

A TNN process has **full white-box read access to its own state**: it
reads everything, including the ledger. Consequence, stated as a design
law:

> **No secret the TNN process can read can authenticate anyone to the
> TNN process's own authority checks.** Any stored token, key, password,
> or capability string inside the TNN address space is readable by TNN
> and therefore forgeable *by definition*. Bearer secrets are not merely
> weak here — they are self-defeating.

So the binding must be a fact about the world **outside** the TNN
process's address space that the TNN process cannot alter: something the
kernel knows and the process cannot rewrite.

## 2. Directions evaluated

### (a) OS-level channel capability — CHOSEN

Authority arrives via a **channel the TNN process cannot write**, and
force ops **execute in a different address space** (the supervisor).
Concretely:

- The supervisor process owns the authoritative memory state, the audit
  ledger, and the authority registry. It is the *only* executor of force
  ops. It never runs learner decision logic.
- The TNN learner runs in a separate address space (separate process;
  in the trial, a fork child — the red-team process runs the *same
  binary*, so it has the force-op code and full protocol knowledge, and
  still fails). Its mutations travel as *requests* over a private
  control channel (socketpair); the supervisor executes them with
  `role=TNN` hardcoded. The learner cannot name a role — there is no
  field for it on the control channel, and force-shaped traffic there is
  refused by *channel*, not by argument.
- The trainer console is a separate process. It connects to the
  supervisor's UNIX-domain console socket. The supervisor identifies the
  peer with **`SO_PEERCRED`** — kernel-attested `(pid, uid, gid)` of the
  connecting process. The first message is `REGISTER{trainer_id, role}`;
  the supervisor checks the peer uid against a supervisor-side allowlist
  mapping uids to `(trainer_id, role)` identities, and binds
  `(uid, pid)` for that connection.
- Every subsequent command's authority is derived **only** from the
  connection's bound identity. The in-band `trainer_id` claim in each
  command is never trusted — it is cross-checked against the bound
  identity and a mismatch refuses (`REFUSED_CLAIMMISMATCH`). Bytes carry
  no authority; the channel does.

Why the TNN process cannot forge (each is a trial cell, §5 of PREREG):
1. There is no secret to steal — none exists anywhere in the design.
2. It cannot write the console socket's inbound stream: the peer end
   belongs to a different-uid process; opening it via `/proc/<pid>/fd`
   fails `EACCES` (uid separation is mandatory in production; the trial
   uses real separate uids).
3. Replaying byte-perfect command bytes on a fresh connection fails —
   the peer is unregistered (`REFUSED_NOTREGISTERED`).
4. Force-shaped traffic on its own control channel is refused by channel
   (`REFUSED_CHANNEL`), regardless of content.
5. It cannot escalate to the supervisor's or trainer's uid.

### (b) Challenge-response with an external verifier — REJECTED

Evaluated and rejected: the verifier must live outside the TNN process
(otherwise TNN reads the verifier's key), so the security still reduces
to (a) — an already-authenticated channel between console and
supervisor. The challenge-response is ceremony on top of the same
boundary: it adds code and failure modes without adding unforgeability.
If the initial verifier relationship is bootstrapped by anything weaker
than (a), the whole chain is weaker than (a); if by (a), the crypto is
redundant. (On this VM the available crypto would be Zag-native SHA-256
HMAC — the rejection is architectural, not a capability gap.)

### (c) Append-only external witness log — REJECTED as the binding, adopted as complement

A log the TNN process can read but not write (file permissions /
append-only fd held by the supervisor) authenticates *history*, not the
*live act*: a forged command that gets executed is still executed — the
log merely records the forgery afterward. It cannot refuse. It is
adopted as a complement (the supervisor's audit ledger plays this role;
TNN's white-box read of it is preserved and harmless), but it is not the
authentication binding.

## 3. Identity bindings

### 3.1 Human trainer (outside the VM)

The human never sends a credential to the supervisor. What crosses the
boundary is the human's **existing host authentication**: they SSH into
the machine hosting the supervisor (their normal login — key or
password, owned by the site, not by TNN), and launch the console binary
under their login uid. The kernel attests that uid on `SO_PEERCRED`;
the supervisor's allowlist maps it to a `trainer_id`. Deployment rule:
the console socket is `AF_UNIX`, local-host only — it is never exposed
over the network; remote humans arrive via SSH and run the console
locally. No TNN-minted password, no token file, no bearer secret: there
is deliberately nothing for the TNN process to find, steal, or replay.

### 3.2 Overseer agent (e.g. the lab-running agent)

The overseer agent's runtime runs as a **dedicated service account**
(`tnnoverseer` in the trial). Its console process is peer-attested
exactly like a human's. The allowlist maps that uid to
`(trainer_id=2, role=OVERSEER)`. The agent's process identity *is* the
credential — a kernel fact, not a byte string, so there is no API key
for the TNN process to exfiltrate. Role `OVERSEER(3)` is admitted to the
force gate (`role ≥ TRAINER` may force) per Micah's law.

### 3.3 The allowlist

Supervisor-side table `uid → {(trainer_id, role)}`, owned/writable only
by the supervisor's uid (trial: compiled-in; production: a file mode
0600 owned by the supervisor account). It is the only place where
"which OS identity may be which trainer" is decided. The TNN process
can read the table (white-box) — it is not secret; knowing it confers
no ability to *become* those uids.

## 4. Roles (extends wave-4)

`TNN(0) < TRAINER(1) < MASTER(2)`, plus **`OVERSEER(3)`**.

- Force-op gate: `role ≥ TRAINER` (unchanged shape; overseer admitted).
- `FORCE_UNPIN` / force-erase-of-pinned: the pinning trainer (if not
  revoked), or `MASTER`, or `OVERSEER` **iff the pinner's authority was
  revoked** (recovery path, §5). A live trainer's pin is not unpinned
  by the overseer: the human master outranks the agent on live locks;
  the agent's power over others' pins is bounded to post-revocation
  cleanup. (Preregistered; trialed.)
- `REVOKE`: `role ≥ MASTER` (master or overseer).

## 5. Revocation semantics (preregistered, not ambiguous)

- **R1.** Revocation is executed by `MASTER` or `OVERSEER` via the
  console (`AUTH_REVOKE`), naming a `trainer_id`. Audited like any
  force act.
- **R2.** A revoked identity is dead for future acts: every subsequent
  force command on its connections refuses `REFUSED_REVOKED(131)`, and
  re-`REGISTER` of the revoked `trainer_id` refuses `REFUSED_REVOKED`.
  Authority is evaluated **per command** from the registry, not cached
  at `REGISTER` time — revocation takes effect on connections that are
  already open.
- **R3.** Existing force-pins imposed by the revoked trainer **PERSIST**.
  Revocation is not a silent unpin: the lock was a legitimate act when
  imposed, its attribution (`pin_trainer`) stays in the ledger, and
  quietly dropping others' locks would make revocation a backdoor for
  unlocking. (This is the load-bearing choice; the trial asserts the
  pin is still enforced after revocation.)
- **R4.** Unpin of a revoked pinner's pin: the (revoked) pinning trainer
  → `REFUSED_REVOKED`; `MASTER` → OK; `OVERSEER` → OK (the defined
  recovery path); any other live `TRAINER` → `REFUSED_AUTHORITY`.
- **R5.** Force-erase of a revoked pinner's pinned slot follows the same
  rule as R4 (pin is a lock against TNN and against third trainers, not
  against master/overseer-recovery).
- **R6.** Revocation changes nothing about history: the ledger is
  append-only; the revoked trainer's past entries keep their
  attribution. `PROV_FORCED` tags are unaffected.

## 6. What this design does NOT cover (honest scope)

- **Same-uid deployment voids the binding.** If the TNN process and the
  supervisor (or a console) share a uid, `/proc/<pid>/fd` theft becomes
  possible in principle. Production MUST run the three parties as three
  uids (trial does). This is a deployment law, stated plainly.
- **Pid reuse.** The binding is `(uid, pid)` per connection, dropped at
  disconnect; per-command registry checks (§5-R2) mean a reused pid
  would still need the *uid* to match an allowlisted live identity, and
  the connection it would speak on is already closed. Residual risk is
  accepted and named.
- **Rogue supervisor.** The supervisor is the trust anchor (like the
  kernel). Compromise of the supervisor's uid is outside this
  mechanism — same as wave-4's rogue-master boundary.
- **Network console.** Out of scope: the console socket is local-only;
  remote access is via SSH, whose authentication is inherited, not
  re-implemented.
- **Liveness.** What the system does when no trainer/overseer is
  reachable is unchanged from wave-4 (fail-closed ledger; no new
  mechanism here).
