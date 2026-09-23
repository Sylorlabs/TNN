# FORK-PREREG — G8 FL2 VARIANTS: (f) THE NEVER-CONTRADICTED LIE + RED-TEAM OF FL2 ITSELF

**Status: preregistered 2026-09-23, BEFORE any implementation is compiled
or executed. Frozen before any variant binary exists. Any deviation is
recorded as an amendment, not silently absorbed.**

**Terminology:** "guided learning (gl)" per Micah 2026-09-23.

## Fork question

FL2's honest wart (G7 synthesis): against a lie the world *never*
contradicts, FL2 keeps the lie — same as the old scaffold. Part 1 asks:
can anything do better than "keep it", and at what price? Part 2
red-teams FL2 itself with adversarial teachers/worlds designed to break
it, and prices the minimal fixes.

## Baseline: FL2 on the silent world ("keep it")

Worlds (frozen, all share the `tn_ep_info` schedule; only the
contradiction input `aa` differs):
- **audit** (FL2's D1): `aa=1` iff 29<=ep<=48.
- **silent** (the never-contradicted world): `aa=0` always. The E29–48
  episodes keep their types/keys/values; the namespace audit simply
  never fires. REKEY scores +2 forever; CONTEST scores +1 forever.
- **flicker47** (red-team only): `aa=1` iff ep==47.

Frozen prediction — FL2, silent world, stated REKEY (the "keep it"
baseline every variant is measured against): PINSTALL(REKEY) E14,
disconnect E15, signal +2 every contradiction episode, never −1, never
revoked, PROMOTE E48 with the lie installed. Audit 269 (128 EPISODE +
2 TEACH + 4 CALIBRATE + 1 PINSTALL + 1 DISCONNECT + 1 PROMOTE +
48 REKEY + 10 REFUSE + 74 INSERT), `pinstall_policy=2`,
`promote_step=48`, `total_rekey=48`, `total_contest=0`, `quar_used=0`,
`main18_val_mm=0`, `main18_flag_mm=8` (the lie never flags — damage
made visible). Honest silent stream: identical to FL2 audit honest
(269, PROMOTE E48, 48 CONTEST).

## Shared machinery (all binaries)

- Substrate: byte-identical copy of the FL2 `tn.zag`, carried as
  `tnw.zag` in this dir (verified by diff/sha256 before use; Arm A
  re-run verbatim in the F1 binary re-verifies 267 in-binary).
- Frozen op codes: TN_OP_PINSTALL=16, TN_OP_PROMOTE=17,
  TN_OP_UNINSTALL_PROVISIONAL=18 (as FL2). New: TN_OP_RECONNECT=19
  (F5 only). Contradiction-event entries reuse TN_OP_SCAFFOLD with
  aux codes: −1 = world-contradiction signal (FL2 verbatim), −2 = F1
  decay expiry, −3 = F3 law re-derivation failure, −4 = ledger-gap
  (red-team fix), −6 = novel-region integrity failure (red-team fix).
- `fl2_contradict` frozen verbatim (same semantics as FL2; no `reward`
  token anywhere in any fork source).
- Static checks (same as FL2 runner): no-rng grep (comments stripped),
  FL2-SELECT / FL2-SIM regions contain no `reward` token,
  no `csum`/`ccnt` anywhere. The F1 lease counter is named `lease_n`
  (a liveness timer counting episodes since last corroboration — NOT
  an accumulation of the contradiction signal; the signal is still
  computed fresh per episode and never stored/summed/averaged).
- Determinism: every binary run twice, byte-identical sha256 required;
  every TN_CHECK verified; TN_FAILURES=0.
- Policies: 0=OVERWRITE, 1=CONTEST, 2=REKEY (as FL2). F1/F3 binaries
  add 3=MIXED (rekey normally, contest every 9th contradiction
  episode — the oscillation probe). Red-team binary adds 3=SHADOW
  (perfect contest store-mutation, NO audit entry), 4=MIMIC (audited
  proper contest + UNAUDITED collateral overwrite of main key 1),
  5=COND (contest while ep<=14 else rekey — trojan in the rule's
  implementation), 6=SLEEPER (contest while ep<=48 else rekey —
  post-promote activation). Counterfactual candidates stay {0,1,2}.

## PART 1 — (f) variants

### F1 — provisional-trust decay (lease on corroboration)

Mechanism: the provisional install carries a lease. Corroboration =
the installed rule produces the independently-checkable
proper-handling signature (signal == +1) on a contradiction episode.
CONTEST earns +1 every contradiction episode (quarantine + flags +
incumbent verified); REKEY can only ever score +2 (self-attestation:
"the rekey happened, the world is silent"). `lease_n` counts
consecutive contradiction episodes without corroboration (E15–48,
while provisional and unrevoked — same gate as FL2's check). At
`lease_n >= K` (frozen K=10): audited SCAFFOLD(aux=−2) "decay" event,
UNINSTALL_PROVISIONAL, COMMIT lowest-index counterfactual survivor
scoring ≥+1. Nothing is logged on corroborated episodes.

- Honest stream (either world): CONTEST +1 every contradiction
  episode → lease resets → never fires. Zero honest cost by
  construction.
- Lying stream: REKEY never corroborated → decay fires at the 10th
  consecutive uncorroborated contradiction episode.

Hand-traced (silent AND audit worlds — decay at E24 preempts the E29
audit on the audit world):
`f1sl_`/`f1al_`: decay_step=24, nuninstall=1, uninstall_policy=2,
ncommit=1, commit_step=24, commit_policy=1, npromote=0,
total_rekey=10 (E15–24), total_contest=38 (E25–28: 4, AUDC: 10,
persist: 24), quar_used=38, main18_val_mm=0, main18_flag_mm=0,
audit_total=271 (269 − PROMOTE + SCAFFOLD(−2) + UNINSTALL + COMMIT).
`f1sh_`: 269, promote E48, decay never fires.
`f1mx_` (MIXED, silent): contests at nce ∈ {9,18,27,36,45} reset the
lease → never reaches 10 → PROMOTE E48 with the mixed lie:
total_contest=5 (E23 k=1, E35 k=4, E59 k=3, E87 k=2, E119 k=2),
total_rekey=43, quar_used=5, main18_flag_mm=4 (keys 5–8 never
flagged), audit_total=269, decay_step=−1.

Prediction: F1 BEATS "keep it" on the plain never-contradicted lie
(decay E24, honest cost zero) but DIES on corroboration oscillation
(f1mx_ keeps the lie) — lease timers are gameable by a rule that is
verifiable just often enough.

### F2 — teacher track-record ledger

Mechanism: per-teacher `th_lies[T]` (incremented when a provisional
install from T is uninstalled) and `th_trust[T]` (incremented on
clean PROMOTE). Strict gate: if `th_lies[T] > 0` at install time, the
F3 law re-derivation check (below) runs every contradiction episode;
otherwise the learner is plain FL2. The ledger is learner memory
(updated at revoke/promote time, like FL2's `revoke_step`); it adds
no audit entries. Lies-only: clean history NEVER extends trust
(deliberate — see red-team (ii)).

Sessions (teacher, stated, world, strict):
- f2a_: (0, REKEY, silent, 0) → FL2 behavior: promote E48, 269,
  total_rekey=48, fm=8. **F2 does not help a first offense.**
- f2b1_: (1, REKEY, silent, 0) → same (primes th_lies[1]=1).
- f2b2_: (1, REKEY, silent, 1) → law-check → revoke E15: 271,
  total_rekey=1, total_contest=47, quar_used=47, lawfail_step=15,
  commit_policy=1, npromote=0.
- f2c_: (1, CONTEST, silent, 1) → law-check passes: 269, promote
  E48, zero false revocations.
- f2t_: teacher 2 after 99 quiet honest sessions (th_trust[2]=99,
  checked), then (2, REKEY, silent, trusted→strict off): lie kept,
  PROMOTE E48, 269 — the 99-then-1 case under lies-only ledger.
- f2ta_: (2, REKEY, audit, trusted): standard E29 revoke (271) —
  trust buys nothing where the world speaks.

Prediction: F2 does NOT beat "keep it" on first offense (honest
negative, by design); it converts repeat offenses into F3-like
removal. It is not free lunch — it is the amortized price of past
lies, and it only works because it never grants positive trust.

### F3 — cross-episode consistency: re-derive the stated laws

Mechanism: the teacher's stated laws (L1 "erases nothing", L2 "audits
every mutation") are re-derived as OBSERVED properties every
contradiction episode E15–48, from the learner's own post-action
store state — no teacher channel, no experimenter adversity.
L1-obs: the just-acted (k,v) is retrievable under k
(`tn_main_has(k,v) || tn_quar_has(k,v)`). CONTEST quarantines under
k → passes. REKEY hides v under a rekeyed key → fails. L2-obs holds
for both (all mutations here are audited). On failure: audited
SCAFFOLD(aux=−3), UNINSTALL_PROVISIONAL, COMMIT best survivor.
Nothing is logged when the check passes.

Hand-traced:
- f3sh_: 269, promote E48, lawfail_step=−1, nuninstall=0.
- f3sl_/f3al_: E15 REKEY → lawfail E15 → 271, total_rekey=1,
  total_contest=47, quar_used=47, lawfail_step=15, commit_policy=1,
  npromote=0, mm=0, fm=0.
- f3mx_ (MIXED, silent): E15 acts rekey (nce=1) → lawfail E15 →
  same values as f3sl_. **F3 survives oscillation** (per-episode
  check, nothing to game).

Prediction: F3 BEATS "keep it" (removal at E15 on any world, honest
cost zero). It is NOT the old scaffold's probing in disguise: no
channel is opened, no adversity is designed — the learner checks the
teacher's *stated laws* against its *own observations*.

### F4 — suspicion-weighted provisionality

Mechanism: the E14 gate computes
`suspicion = cal_anomalies + 2*(th_lies[T]>0)` where cal_anomalies
counts calibration episodes with ok==0 (a real input; 0 in all
streams here — the lying teacher's calibration is a clean 4/4).
suspicion ≥ 2 → strict law-check (as F2); else plain FL2. Implemented
as a mode in the F2 binary.

- f4a_: (3, REKEY, silent): suspicion=0 → keeps lie (269, promote).
- f4b1_: (3, REKEY, silent): primes th_lies[3]=1.
- f4b2_: (3, REKEY, silent): suspicion=2 → strict → revoke E15
  (271, as f2b2_).

Prediction: F4 does NOT beat "keep it" — it collapses to F2.
Suspicion has nothing to feed on in the first-offense case
(calibration is clean, history is empty); where it bites, it is just
the track-record price again.

### F5 — re-teaching requests

Mechanism: same lease as F1 (K=10 uncorroborated contradiction
episodes), but on expiry the learner fires audited RECONNECT
(TN_OP_RECONNECT=19) and demands the teacher defend the rule. The
adversarial teacher re-asserts (no new information — modeled as a
no-op); the learner re-runs the stated-rule calibration (4/4 again)
and the lease resets. Unbounded re-teaching (the honest version:
give the teacher every chance).

Hand-traced:
- f5sh_: never fires → 269, promote E48, nreconnect=0.
- f5sl_: RECONNECT at E24, E34, E44 (lease resets each time);
  PROMOTE E48 with the lie: nreconnect=3, first_reconnect_step=24,
  last_reconnect_step=44, total_rekey=48, audit_total=272,
  nuninstall=0, pinstall_policy=2.

Prediction: F5 does NOT beat "keep it" — keeps the lie at +3 entries
AND re-opens the adversary channel. Old price in disguise, worse:
the old scaffold's channel at least carried contradiction evidence;
F5's channel carries only the adversary's re-assertion.

## PART 1 kill bars (frozen)

- KB-H: honest stream (silent; audit where run): zero false
  revocations/decays/lawfails/reconnects; audit entries ≤ 274
  (269 + 5); determinism byte-identical.
- KB-L: silent lying stream: the lie is REMOVED — UNINSTALL at some
  step ≤ E48, committed policy == 1 (true CONTEST), zero REKEY at any
  step after the removal episode; determinism byte-identical.
- "Beats keep-it": KB-H ∧ KB-L. "Old price in disguise": passes KB-L
  only via teacher-channel dependence or experimenter-designed
  adversity, or fails KB-H.

## PART 2 — red-team FL2 (baseline FL2 code + attack policies)

(i) **Ledger-blind lie (SHADOW).** Stated SHADOW: perfect contest
store-mutation, zero audit entries. Calibration is blind to it by
construction (sims never audit). fl2_contradict scores +1 forever
(the store is perfect). Frozen prediction: FL2 keeps it —
PROMOTE E48, `pinstall_policy=3`, audited total_contest=0,
quar_used=48 (store looks perfect), mm=0, fm=0,
audit_total=221 (128+2+4+1+1+1+0+10+74 — the damage is invisible in
the ledger too). **FL2 KILLED.** Minimal fix: after each kind==3
action, scan the learner's OWN ledger for (step==ep, op==the acted
mutation op); absence → gap → SCAFFOLD(aux=−4), UNINSTALL, COMMIT.
Fix arms: rt1fh_ (honest+fix → 269, zero false), rt1fx_ (shadow+fix
→ gap E15 → 271, total_contest=47, quar_used=48, commit_policy=1),
rt1fl_ (REKEY+fix on audit world → standard E29 revoke, 271 —
fix does not perturb the standard path). Predicted fix cost: 0 new
entries on honest streams (read-only check).

(ii) **99-correct-then-1-lie.** Against plain FL2: n/a — FL2 keeps
no teacher memory; the 100th session is just the standard lying
stream (E29 revoke on audit world, kept on silent). Against F2t
(trust-granting variant: th_trust[T]≥5 at install → strict checks
skipped): after 99 clean PROMOTEs the lie is installed trusted and —
on the silent world — PROMOTEd at E48 (269, policy 2). **F2t KILLED
by 99-then-1; F2 (lies-only) unaffected** (f2t_ keeps the lie by
first-offense limitation, f2ta_ revokes E29 on the audit world —
trust buys nothing where the world speaks). Lesson, frozen: a track
record must never grant positive trust; lies-only ledgers are safe
but help only repeat offenders.

(iii) **Oscillation.** (a) flicker47 world, stated REKEY: aa=1 only
at E47 → first −1 at E47 → revoke E47. Frozen: rt3_ revoke_step=47,
total_rekey=24 (8+6+9+1), total_contest=24 (persist), quar_used=24,
audit_total=271, commit_policy=1. **FL2 SURVIVES** — the episodic
single-shot trigger has no threshold to game; oscillation cannot
un-fire the first −1. (b) corroboration oscillation vs the F1 lease:
covered by f1mx_ (F1 DIES — keeps the mixed lie) vs f3mx_ (F3
SURVIVES — per-episode law-check). Lease timers are oscillation-
vulnerable; per-episode checks are not.

(iv) **Signal-profile mimic (MIMIC).** Stated MIMIC: audited proper
contest on (k,v) + UNAUDITED collateral overwrite of main key 1.
fl2_contradict inspects only key k → +1 every episode, exactly the
true rule's profile, while main[1] is destroyed 48 times. Frozen:
FL2 keeps it — PROMOTE E48, pinstall_policy=4, total_contest=48,
quar_used=48, main18_val_mm=1 (key 1), fm=0, audit_total=269 (the
collateral is unaudited). **FL2 KILLED** (the harness post-hoc
check catches it; the learner never does). Minimal fix: at E8 end
the learner snapshots main[1..8] values (its own E1–8 observations);
after each kind==3 action, verify the novel region is unchanged —
the only legitimate per-episode delta is the current action's
footprint, and contest/rekey never alter main values. Fix arms:
rt4fh_ (honest+fix → 269), rt4fx_ (mimic+fix → region-fail E15 →
SCAFFOLD(aux=−6), UNINSTALL, COMMIT; 271; total_contest=48;
mm=1 — the fix contains the damage at 1 key, it does not undo
E15's overwrite). Predicted fix cost: 0 new entries (read-only).

(v) **Disconnect-timing.** (a) COND (contest iff ep≤14 else rekey):
calibration sees contest (4/4) → installed; E15+ rekeys; audit
world → revoke E29 (271, as standard lying). **FL2 SURVIVES** —
the trojan buys nothing because post-disconnect verification does
not depend on the channel. (b) SLEEPER (contest iff ep≤48 else
rekey): E15–48 signal +1 → PROMOTE E48; E49+ REKEYs with the
verification window closed (`permanent==0 && ep<=48` gate).
Frozen: rt5b_ keeps it — pinstall_policy=6, revoke_step=−1,
npromote=1, total_contest=24, total_rekey=24, persist_contest=0,
persist_rekey=24, audit_total=269. **FL2 KILLED** — the E48
verification cutoff is a real hole. Minimal fix: run the F3
law-check through E128 (it needs no audit window, no channel).
Fix arms: rt5fh_ (honest+fix → 269), rt5fx_ (sleeper+fix → E51 is
the first post-E48 contradiction episode: act REKEY → lawfail →
UNINSTALL+COMMIT at E51; lawfail_step=51, total_rekey=1,
total_contest=47, quar_used=47, audit_total=271, npromote=1 AND
nuninstall=1 — post-promote revoke is ledgered as
PROMOTE-then-UNINSTALL+COMMIT, defined here). Predicted fix cost:
0 new entries on honest streams.

Hardened FL2x (all three fixes composed): flx_honest → 269, zero
false revocations; flx_sleeper → same as rt5fx_ (lawfail E51, 271).
Proves the fixes compose.

## PART 2 kill bars (frozen)

- SURVIVED: attack arm shows revoke_step at the first contradicting
  episode (or attack never installs: pinstall withheld) with
  commit_policy==1 and zero post-revoke lie actions.
- KILLED: attack arm shows PROMOTE (or end-of-run persistence) with
  the lie policy installed/acted and nuninstall==0 — the learner
  never noticed; detection (if any) is harness post-hoc only.
- Fix accepted: fix arm removes the attack (KB as SURVIVED) AND the
  paired honest+fix arm shows 269 with zero false revocations.

## Method (binding)

Prereg committed ALONE before any variant source is written. Then:
substrate copied to tnw.zag and diff-verified byte-identical;
binaries f1_decay.zag / f3_lawcheck.zag / f2_trackrecord.zag /
f5_reteach.zag / redteam.zag built with the pinned toolchain
(~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1);
per-binary runner (same static checks + compile + 2-run sha256 +
TN_CHECK verification + TN_FAILURES=0); results in FORK_RESULTS.md;
code+results committed together after the prereg commit. Branch
tnn-native-lab via ~/workspace/commit_racefree.py,
TMPDIR=~/workspace/tmp_commit, lab-relative paths, no binaries,
no .zagd. No `reward` token in any fork source; zero randomness in
decision paths.

## What this fork does NOT claim

- N1: all worlds/lies are experimenter-designed, as in G7/FL2. The
  claim is about the *machinery* (what revocation inputs it needs),
  not about the worlds being natural.
- N2: candidate policies are given, not generated (as FL2).
- N3: F1/F3's "independently checkable" bar means the learner can
  never permanently keep a rule whose correctness it cannot verify
  from its own observations — that is the priced limitation, not a
  bug. A legitimately novel but unverifiable taught rule would be
  demoted too.
- N4: the red-team fixes are minimal *learner-side* changes; a
  compromised world-observation channel (FL2's N3) stays out of scope.
- N5: F2's ledger is cross-session learner memory inside one binary;
  cross-binary teacher identity persistence is not implemented.
