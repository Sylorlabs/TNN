# One-Brain Variant A — Design

**Status:** organs built and unit-tested standalone. Integration trials are
**blocked** until the frozen prereg is relayed. Nothing in this tree makes
trial claims.

## 1. Architecture: one brain, organs as passes

One shared byte-arena **store** (256 slots x 24 bytes) and one shared
**ledger** (4096 entries x 64 bytes). The three organs — FL2 eliminative
logic (GL), PAM admission (PAM), deliberate memory (MEM) — are passes over
the same state, not separate systems with a message bus. Every install,
refusal, and mutation is organ-tagged in the same ledger.

```
ob_substrate.zag   one store + one ledger + replay + GL slot helpers
ob_gl.zag          FL2 organ: select / simulate / calibrate / audit
ob_pam.zag         PAM organ: H2 admission gate + the install path it fronts
ob_mem.zag         deliberate organ: MA1 ops + staged autonomy + MA4 signed trust
test_gl.zag        FL2 standalone port (canonical streams, byte-compared)
test_pam.zag       PAM 15-row disposition matrix
test_mem.zag       deliberate-organ op/refusal/trust matrix
test_wiring.zag    cross-organ wiring smoke test (NOT a trial)
```

## 2. Shared store

256 slots, 6 words (24 bytes) each:

| word | content |
|------|---------|
| w0 | flag bits: live(1) pinned(2) contested(4) forcepin(8) |
| w1 | key (0 = unkeyed) |
| w2 | value |
| w3 | meta byte: bits 0-1 tier, bits 2-3 organ tag, bit 16 provisional |
| w4 | step added |
| w5 | reserved |

Regions:

- slots `0..127` — GL main (keyed facts; w0.pinned byte = CONTESTED flag)
- slots `128..191` — GL quarantine (keyed, quarantined newcomers)
- slots `192..255` — deliberate pool (MA ops; key optional)

Deliberate ops are refused outside `192..255` (`REFUSED_BADSLOT`); GL owns
its main/quarantine areas. Tiers: 0=short, 1=long, 2=protected, 3=pinned.

## 3. Shared ledger

16-word entries, cap 4096:

| word | content |
|------|---------|
| w0 | **step** — caller-provided: episode number for GL entries, ledger index for other organs (the monotonic clock lives in the ledger header) |
| w1 | op |
| w2 | organ (1=GL, 2=PAM, 3=MEM, 4=OVS overseer) |
| w3 | slot (-1 for gate disposition records / stage changes) |
| w4 | rc |
| w5..w9 | b1..b5 — before-words (slot w0..w4 snapshot) |
| w10..w14 | a1..a5 — after-words |
| w15 | aux |

**Replay:** for `rc==OK` mutating ops the a-words restore slot w0..w4, so
replaying the ledger from genesis reproduces the exact store state
(`ob_replay_check` returns 0 iff exact). **Audit-first:** every mutator
snapshots before mutating and restores the before-image if the audit
append fails — no mutation ever exists without its ledger entry.

**Rollback** is not skipped by replay: the rollback entry carries its own
after-image (the zeroed slot), so replay applies it like any mutation.

## 4. Organ interfaces

### 4.1 GL (FL2) — `ob_gl.zag`

Frozen `gl_default` codes 1..18 kept verbatim; the organ adds:

- `OB_GL_CONTEST_Q=19` — the quarantine leg of a contest (see conflicts).

`ob_gl_select(stated, prov)`: policy order CONTEST > OVERWRITE > REKEY;
skips the provisional policy. `ob_gl_audit(l, step, op, slot, aux)`.
Simulation helpers mirror the frozen `tn_sim_*` semantics over the shared
store. F3 selection uses the structurally repaired survivor rule:

```
if(act!=0 && sig0>=1) return 0;
if(act!=1 && sig1>=1) return 1;
if(act!=2 && sig2>=1) return 2;
return -1;   // no genuine survivor (no 99-sentinel sham)
```

### 4.2 PAM — `ob_pam.zag`

Frozen H2 disposition lattice (from committed `memgate.zag`):

| judgment vs record | outcome |
|---|---|
| FAIL | never install; stored as deduplicated negative evidence |
| UNRESOLVED matching negative evidence | SUPPRESS |
| UNRESOLVED otherwise | WITHHOLD |
| PASS, fresh | provisional admit |
| PASS, later matching PASS (same jcode, \|dmeas\|<=tol) | permanent |
| PASS conflicting with provisional | revoke + replace provisional |
| PASS conflicting with permanent | conflict-withhold |

Tolerances: class0=8, class1=40, class2=60 (frozen per-class values).
Disposition records carry `slot=-1` with the class in b1; every gate call
emits an organ-tagged `OB_PAM_DISPOSITION` entry (aux = disposition).

**The install path the gate fronts:**

- `ob_pam_install_prov` — installs a keyed fact in the GL main region with
  `meta.organ=PAM`, `meta.prov=1`; snapshot-audited (`OB_PAM_PROVISIONAL`).
- `ob_pam_promote` — corroboration clears `prov` (`OB_PAM_PERMANENT`).
- `ob_pam_revoke_prov` — zeroes a provisional install (`OB_PAM_REVOKE_PROV`).

Pointwise `REVISE_INSTALL` is excluded: the frozen synthesis says V2-A was
weakened by decoy revisions, and the trial-1145 finding bans it.

### 4.3 Deliberate memory — `ob_mem.zag`

MA1 op set with staged autonomy and refusal accounting:

| rc | meaning |
|---|---|
| 0 | OK |
| 100 | BAD (bad args) |
| 101 | refused: CORE / pinned-by-learner |
| 102 | refused: not at a stage that permits this op |
| 103 | refused: slot not live |
| 104 | refused: kill at MANAGE stage (kill needs KILL stage) |
| 105 | refused: stage does not permit this op |
| 106 | refused: slot outside the deliberate pool |
| 107 | refused: staged training (reserved) |
| 108 | refused: nothing to roll back |
| 109 | refused: overseer force-pin |
| 110 | refused: unpin on a non-pinned slot |

Stages: NONE < ADD < MANAGE < KILL; each op lists the stages that permit it.
Refusals are audited ledger entries — a refusal is an event, not silence.

**Force-pin** is program law (audited external lock): `ob_mem_forcepin` /
`ob_mem_unforcepin` are organ-tagged OVS (4), can only be called by the
overseer path, outrank learner pins in kill refusal, and are refused on
non-live slots.

MA4 signed trust: `ob_trust_update` (+/- per feature, clamped to
`[-TRUST_MAX, TRUST_MAX]`, trust may go negative — traps are learnable),
`ob_signed_score` (floored division, so negative trust yields negative
scores), `ob_mem_victim_fresh` (lowest fresh signed score among live,
unpinned, non-force-pinned USER slots; deterministic lowest-slot tie-break),
strict-inequality churn admission (`v_new > v_victim`).

## 5. Conflict choices (decided while building)

1. **Contest mutates two slots but the frozen op counts one audit.**
   A contest touches the main slot (contested flag) and a quarantine slot
   (new entry). One-brain replay needs both. Resolution: the frozen
   `OB_GL_CONTEST` entry covers the main leg; a new `OB_GL_CONTEST_Q=19`
   entry covers the quarantine leg with its own snapshots. Frozen
   counting stays comparable (logical audits = total minus CONTEST_Q).

2. **Ledger w0: episode step vs clock.** The frozen GL checks read the
   audit step as the episode number. Resolution: w0 is a caller-provided
   *step* (episode for GL, ledger index for others); the monotonic clock
   lives in the ledger header. No second clock exists.

3. **PAM gate state vs shared store.** The gate's per-class prov/perm
   records are gate control state, not knowledge. Resolution: they live in
   the gate's own arena and are *ledgered* (every call emits
   organ-tagged disposition entries) but are not part of the replayed
   store. The store mutations the gate authorizes (install/promote/revoke)
   are snapshot-audited and replay exactly.

4. **Force-pin scope.** Program law allows the overseer to lock any
   memory. Variant A scopes `ob_mem_forcepin` to the deliberate pool
   (organ boundary stays clean); overseer locks on GL-region slots are
   future work, documented here rather than half-built.

5. **PAM installs land in the GL main region.** Perceptual knowledge and
   taught facts share the GL keyed-fact region; provenance is in
   `meta.organ` (PAM vs GL), not in separate stores. GL mechanics (find,
   contest) operate on keyed facts regardless of provenance — a deliberate
   unification choice: one store means no provenance-based mechanic
   forks. Key collisions between taught and perceived facts are a frozen-
   prereg trial question, not settled here.

6. **Churn is composed, not primitive.** Victim selection and the
   strict-inequality gate are helpers; the churn act itself is an audited
   `KILL` + audited `ADD`. No separate churn op code.

7. **Disposition records vs mutation entries share op codes**
   (`OB_PAM_PROVISIONAL` etc.) but are disambiguated by the slot field:
   `-1` = gate disposition record (class in b1), `>=0` = store mutation
   with real snapshots. Replay applies only the latter.

## 6. Test evidence (standalone only — no integration claims)

| test | what | result |
|---|---|---|
| `test_gl` | FL2 honest + lying streams, canonical `glh_*`/`gll_*` rows | 0 failures; 59 shared lines byte-identical to committed `gl_default/evidence_run1.txt`; audit totals 269/271 match; honest revoke_step=29; 2 reruns byte-identical |
| `test_pam` | 15-row disposition matrix over the frozen H2 lattice | 0 failures; 15 disposition entries all organ-tagged PAM; 2 reruns byte-identical |
| `test_mem` | staged autonomy, full refusal matrix, CORE immunity, force-pin/unpin, promote/demote, rollback, signed trust incl. negative trust, victim selection + strict inequality | 0 failures; replay exact; 2 reruns byte-identical |
| `test_wiring` | cross-organ sequence over one store + one ledger | 0 failures; all four organ tags present; replay exact; 2 reruns byte-identical |

One-brain additions beyond the frozen vectors (documented, not hidden):
`glh/gll_contest_q_n` (48/33 — the quarantine legs) and
`glh/gll_replay` (0 — exact replay).

No-randomness static scan of all sources: zero hits for
rand/srand/lcg//dev/urandom/getrandom/seed tokens.

## 7. Build and run

```sh
cd ~/workspace/onebrain/ob_a
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
$ZNC test_gl.zag     --no-zagd --no-analyze --no-foreground-cache -o test_gl_linux
$ZNC test_pam.zag    --no-zagd --no-analyze --no-foreground-cache -o test_pam_linux
$ZNC test_mem.zag    --no-zagd --no-analyze --no-foreground-cache -o test_mem_linux
$ZNC test_wiring.zag --no-zagd --no-analyze --no-foreground-cache -o test_wiring_linux
./test_gl_linux && ./test_pam_linux && ./test_mem_linux && ./test_wiring_linux
```

Each binary prints `TN_CHECK,<name>,<actual>,<expected>` rows and a final
`TN_FAILURES,<n>`; exit code is 0 iff n=0. Reruns are byte-identical.

## 8. What is NOT done / blocked

- Integration trials: **blocked until the frozen prereg is relayed.**
- No episode schedule, curriculum, or cross-organ arbitration policy is
  exercised anywhere in this tree.
- PAM gate state is ledgered but not store-replayed (decision §5.3).
- Overseer force-pin is deliberate-pool-scoped (decision §5.4).
- Taught-vs-perceived key collisions: open trial question (§5.5).
