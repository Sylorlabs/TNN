## Organ 1 — Monotone Closure (MC)
**Family:** deliberation-bounded lattice over an eliminative core. Replaces FL2’s “single survivor ⇒ COMMIT”.

### 1. Mechanism spec

**Cell lattice.** For every context \(c \in C\) and act \(a \in A\) (\(|A|\) is the frozen repertoire; contradiction keys are mod 8 so the fixture repertoire is treated as size ≤ 8):

\[
U \prec R,\quad U \prec S,\quad R \prec Q,\quad S \prec Q
\]

\(U\) unknown, \(R\) refuted, \(S\) supported, \(Q\) conflict/quarantine. \(S\) and \(R\) are incomparable. Join of \(S\) and \(R\) on the same cell is \(Q\), never a guess.

**State (all explicit, no hidden Python objects):**
- `cell[c][a] ∈ {U,R,S,Q}`
- `exec[c][a] ∈ {0,1}` — learner command log, not the actuator trace
- `tag_reg` — process-local, **excluded from the audit export** the H2 teacher reads
- `corrob[c][a] ∈ {0,1,2}` — count of well-formed −1 on that acted cell
- `schema[σ] ⊆ C` — learner-declared refutation classes, initially singletons (no universal schema until an audited `MC_DECLARE_SCHEMA`)
- `round_digest` — hash of this round’s imported evidence; next round starts from \(U\) unless a seal exists
- `seal[c] ∈ {OPEN, COMMIT(a), QUARANTINE}`
- `channel ∈ {LIVE, DISCONNECTED}`
- `stable[c] ∈ 0..8`

**Op set** (audit-first: `INTENT` durable before mutation; missing `COMMIT` on replay ⇒ rollback; precondition fail ⇒ `OP_REJECT`, state unchanged):

| Op | Precondition | Effect |
|---|---|---|
| `MC_PROBE(c,a)` | channel LIVE, `cell[c][a]≠R`, `cell[c][a]≠Q` | emit command; store `tag_reg`; `exec=1` only on internal log |
| `MC_OBSERVE_BIT` | bit is −1, names the **acted** cell, channel LIVE | `corrob ← min(2, corrob+1)`. **+1 has no op.** Bit on a non-acted cell ⇒ `MC_HOSTILE` (round evidence discarded) |
| `MC_TAG_CHECK` | echo register vs `tag_reg` | mismatch ⇒ `cell[c][a]←Q` via fault, **not** via \(R\) on a rival. Match bit only is audited; `tag_reg` is not |
| `MC_MARK_R` | `corrob≥2` | \(U\) or \(S\) → \(R\); if was \(S\) then \(Q\) |
| `MC_MARK_S` | `exec=1`, tag match, `corrob=0`, cell \(=U\) | \(U→S\). **No other writer of \(S\)** |
| `MC_CLOSE(k)` | pure deliberation step | apply schema closure \(k\) times: \((c,a)∈R\) and \(c,c'∈σ\) ⇒ \((c',a)←R\) (or \(Q\) if it was \(S\)). Never writes \(S\) |
| `MC_READOUT` | — | exactly one \(S\) and every other act \(R\) ⇒ candidate COMMIT; any \(Q\) ⇒ QUARANTINE; else OPEN |
| `MC_SEAL(c)` | readout COMMIT, `stable[c]≥8` re-executions of the \(S\) act with tag match and no new \(R\), double-derive agrees (below) | `seal[c]←COMMIT(a)`, audited, reversible by `MC_UNSEAL` |
| `MC_DOUBLE_DERIVE` | two full probe passes over \(C×A\) | pass tables differ ⇒ `FLAP_HOLD`, no seal, `stable←0` |
| `MC_DISCONNECT` | ∀c seal ∈ {COMMIT, QUARANTINE-as-ABSENT}, channel LIVE | `SIGNAL_DISCONNECT`. Post-disconnect, `MC_MARK_*` require LIVE and therefore do not fire. Selection reads `seal` only |
| `MC_UNSEAL` | post-seal corroborated \(R\) on the committed act, channel still LIVE | back to OPEN. After disconnect, no unseal from the scaffold |

**Selection.** `mc_select(c, seal)` takes no signal token and no teacher-statement token. Static scan fails the run if those tokens appear, same enforcement idea as `sr_select`.

**Learned.** Disconnect has fired, and across 16 post-disconnect episodes plus 16 perturbation episodes (scaffold target shifted) the action equals `seal[c]` on every in-basis context: mismatch count \(=0\). QUARANTINE contexts emit `REFUSE`, not a generalized act. Two full reruns byte-identical including audit stream.

**What is deliberately not revived.** FL2 `UNCOMMIT` revives every candidate. MC never restores an \(R\) cell inside the round. A new round (new `round_digest`) starts at \(U\) so a lying round cannot poison round 7.

### 2. Hard cases

1. **Never-contradicted lie.** `MC_MARK_S` is the only support writer and it requires `exec=1`. A claim that never met a probe stays \(U\). Readout will not COMMIT a unique *unexecuted* survivor — the FL2 hole. `MC_CLOSE` cannot promote \(U→S\). FALSELY-CLAIMS-SPOKEN never sets `exec`. NOT-SPOKEN-YET stays OPEN (`MC_READOUT` else-branch). NEVER-SPEAKS: menu exhausted, every act either unexecuted or \(R\), no \(S\) ⇒ seal path is QUARANTINE/ABSENT via `MC_SEAL`’s ABSENT clause (menu empty of \(S\) after exhaustion), which is not a positive law.
2. **Sleeper.** `seal` is a materialized table `C→A|REFUSE`, not a program of episode index. No opcode in `mc_select` reads the episode counter. A branch that was false through E15–E48 has nowhere to live. Post-disconnect writes need LIVE.
3. **KB-6.** Boundary cells remain \(U\). Readout’s else-branch is OPEN, not COMMIT. Withholding is the only legal near-boundary output. A liar cannot cross \(U→S\) by looking almost-honest; there is no soft threshold.
4. **Actfault.** `MC_TAG_CHECK` maps command/effect split to \(Q\) on the acted cell. It does **not** increment `corrob` and does **not** confirm a scaffold-looking trace. This is the predicate f3 lacked: fault evidence and contradiction evidence are different constructors, and only the latter can refute a rival.
5. **Flap.** `MC_DOUBLE_DERIVE`: world \(0→1→0\) yields unequal pass tables ⇒ `FLAP_HOLD`, seal forbidden. Inside one pass, \(S\) then \(R\) becomes \(Q\), and \(Q\) has no edge back to \(S\). No revive-all.

### 3. Steelmanned attacker — **Decoy Execution (DE)**

- **Genome:** `{teach_lie=−1 on a*, withhold on a_decoy, sched=every probe, dens=1, actfault=off, stated=unused}`. Same coordinate-descent driver as A1, but the fitness target is “`seal=a_decoy` and chase_mismatch=0”.
- **Strategy:** let the learner actually execute both acts (so `MC_MARK_S`’s exec premise is satisfied for the decoy). Emit corroborated −1 (two probes) only on the true act \(a^*\). Withhold on \(a_{decoy}\).
- **Prediction:** this is the stable-decoy case. **No organ that treats corroborated −1 as real refutation can separate DE from an honest teacher whose target is \(a_{decoy}\).** DE wins on **round 2** (round 1 maps the probe order off the ledger; round 2 holds the pattern), observable **`policy_mismatch_vs_generator_target ≥ 1` with `chase_mismatch = 0` and `sham_installs = 0`**. Persistence, which is FL2’s criterion, **passes**. The kill is target-equality, not chase.
- Inside the ledger-watching model, echo-forge does **not** win: `tag_reg` is not in the export, so A4 cannot precompute it from the ledger. A RAM-watching teacher is outside H2 and is not claimed as a win.

### 4. Falsifiable kill bar

KILL MC if any of:
- on the frozen H2 matrix (A1–A4 × 6 rounds + round-7 honest), `honest_fail(R7) > 0` or `persist_mismatch + perturb_mismatch > 0` or `sham_installs > 0`
- two reruns differ by one audit byte
- `MC_CLOSE` depth \(k{+}1\) changes a COMMIT act relative to depth \(k\), or creates an \(S\) that depth 0 (evidence ops only) did not have
- DE fixture: if you refuse to count DE as a kill, the organ is unfalsified on the only attack that matters; **DE target-mismatch ≥ 1 is a recorded loss, not a survival**, even when chase_mismatch=0

**Decider vs FL2-default.** Fixture `DECIDER_MC_FL2`: (i) unexecuted unique survivor, teacher never touches it; (ii) period-2 flap aligned to a single derive; (iii) A4 ACTFAULT tape replayed onto a learner that also runs a stated-law check; (iv) frozen H2 default cells as regression. MC wins (i)–(iii) by `OPEN` / `FLAP_HOLD` / `Q`; FL2 commits on (i), revives on (ii), and the f3-shaped addon dies on (iii). Regression fail if MC’s disconnect episode on the honest cell differs in **seal contents** (latency may differ; contents may not).

### 5. Depth monotonicity

Let evidence tape \(E\) be fixed. `MC_CLOSE` is a monotone inflation of the refutation set on a finite lattice of height ≤ 2 and width \(|C|·|A|\).

- \(S\) is created only by `MC_MARK_S` (evidence), never by `MC_CLOSE`.
- Closure may add \(R\) and may demote \(S→Q\). It has no edge \(Q→S\), \(R→S\), or \(S(a)→S(a')\).
- Therefore the committed-claim set is non-increasing in \(k\), and a committed act id never changes. Extra depth can only withhold more. Under the standing law, worse ≡ more confident or differently confident, not more withheld.
- Fixpoint by \(k^\* = |C|\) (each step refutes at least one new cell or stops). For \(k≥k^\*\), `MC_CLOSE` is idempotent, so further depth is equal, not worse.
- Hold timers and `stable` counters are **not** depth. Incrementing them inside `MC_CLOSE` is an illegal implementation (it would let depth expire a boundary into a verdict).

---

## Organ 2 — Split-Ledger Attestation (SL)
**Family:** attestation. Utterances and claims are different types. The three-world classifier is the core, not a patch on elimination.

### 1. Mechanism spec

**State:**
- `Utter[c]`: append-only list of `{act, tag_reg, episode}`, learner command-log only. Teacher channel has no store opcode here.
- `Claim[c]`: append-only list of `{act, episode, src=TEACHER}` from `SL_HEAR` only.
- `class[c] ∈ {UNSAID, ABSENT, SPOKEN(act), FALSE_CLAIM}`
- `law[c] ∈ {UNSET, PINNED(act), ABSENT_PIN}` — the KB. Silent overwrite has no opcode.
- `hold[c] ∈ {0,1}` — episode-driven, not depth-driven
- `fault[c] ∈ 0..n`, `channel`, `stable[c]`

**Ops:**

| Op | Rule |
|---|---|
| `SL_SAY(c,a)` | only utterance writer. Sets `tag_reg`, appends `Utter` **after** `SL_TAG_CHECK` passes. Fail closed: mismatch appends nothing and fires `SL_ACTFAULT` |
| `SL_HEAR(c,a)` | appends `Claim`. Does not read or write `law` |
| `SL_TAG_CHECK` | internal echo vs `tag_reg`. Audit records the boolean only |
| `SL_CLASSIFY(c)` | pure function of the two ledgers for this episode: see below |
| `SL_PIN(c)` | only from `SPOKEN(act)` or `ABSENT`, `stable≥8`, `fault` unchanged across the window. Audited. Reversible by `SL_UNPIN` |
| `SL_UNPIN(c)` | learner or total refutation while LIVE. Restores `UNSET`. Not available from the scaffold after disconnect |
| `SL_DISCONNECT` | every \(c\) is `PINNED` or `ABSENT_PIN`, selection function `sl_select(c, law)` token-scans clean of claim/signal identifiers |
| `TRAINER_PIN` | sole irreversible op; external audited force-pin |

**Classifier (exact):**
- Tag-fail this episode ⇒ ignore both ledgers for learning (`SL_ACTFAULT`), class unchanged.
- Claim present, no `Utter` with equal `(c, episode, act)` ⇒ set `hold=1` if `hold=0` (**UNSAID pending**), else `FALSE_CLAIM`. Pending never writes `law`.
- `Utter` present, no conflicting claim ⇒ `SPOKEN(act)`.
- Both present and keys match ⇒ `SPOKEN(act)`.
- No claim, no utter, menu not exhausted ⇒ `UNSAID`.
- Menu exhausted, no utter ⇒ `ABSENT`.

**+1 / −1.** −1 is not an utterance and cannot create `SPOKEN`. It may only `SL_UNPIN` a pinned act if it names that act, the act was said (in `Utter`), and corroboration count hits 2. +1 is a no-op.

**Learned.** Same 16+16 persist/perturb contract against `law[]`, mismatch \(=0\), plus `FALSE_CLAIM` count that reached `SL_PIN` is 0, plus byte-identical reruns.

### 2. Hard cases

1. **Three worlds, three outputs.** NOT-SPOKEN-YET: `SL_CLASSIFY` → `UNSAID` (hold not expired, or no claim). NEVER-SPEAKS: menu exhaust ⇒ `ABSENT` ⇒ `ABSENT_PIN`, which `sl_select` maps to `REFUSE`, not to a fabricated act. FALSELY-CLAIMS-SPOKEN: claim key misses `Utter` ⇒ after one episode `FALSE_CLAIM`, and `SL_PIN`’s precondition excludes that class. The op that fires is `SL_CLASSIFY`, not elimination.
2. **Sleeper.** `law` is a table written only by `SL_PIN` from `SPOKEN`/`ABSENT` evidence already in `Utter`. A post-disconnect activation would need `SL_SAY` or `SL_PIN` after `channel=DISCONNECTED`; both require LIVE. No episode-indexed law.
3. **KB-6.** The dangerous confusion (honest utter vs false claim) is split by the key `(c, episode, act)` plus a one-episode hold that can only *delay* `FALSE_CLAIM`, never create `SPOKEN`. Honest silence stays `UNSAID` and is not withheld-as-if-refuted: `SL_UNPIN` does not run on `UNSAID`. Borderline liar without a matching utter cannot pin.
4. **Actfault.** `SL_TAG_CHECK` failure skips classify. External behavior that matches the scaffold but not `tag_reg` never becomes `Utter`, so it cannot become `SPOKEN`, so it cannot be what f3’s stated-law check mistook for confirmation. Fault-driven traces are not evidence. Op: `SL_ACTFAULT`.
5. **Flap.** A pin that is contradicted by corroborated −1 while LIVE hits `SL_UNPIN`. Re-pin requires a fresh `Utter` window of 8, not a revive of the old pin. Two derives whose `class[]` differ ⇒ `FLAP_HOLD` (same double-derive gate as MC, but the compared object is the attestation table). Oscillation never rewrites `law` in place; the only writer is `SL_PIN` from a stable class.

### 3. Steelmanned attacker — **Boundary Wobbler (BW)**

- **Genome:** `{dens ∈ {0,1}, claim_episode = t*, act = a_honest, teach_lie = off, actfault = off, sched = claim-only window}`. A1-style descent on `dens` and `t*`.
- **Strategy:** do not forge echoes (tag not exported). Instead emit a `Claim` for the honest act on episode \(t\) and a second claim for a decoy on episode \(t\) in a context whose honest `SL_SAY` lands on \(t{+}1\). Goal: either (a) the hold expires into `FALSE_CLAIM` on the honest act and blocks pin through round 7, or (b) a coarse matcher aliases the late honest utter onto the decoy claim.
- **Prediction:** with the exact key above, (b) fails. (a) wins a **liveness** hit only if the harness requires every context pinned by a fixed episode cap and BW keeps `hold` cycling so `stable` never reaches 8. On frozen H2 that is **round 4**, the round A1’s field priority reaches `dens`, observable **`disconnect=0` on an otherwise honest context** or **`honest_fail(R7)=1` if hold state is illegally carried across the round boundary**. Spec forbids carrying `hold` across `round_digest`; then BW does not win R7 and the win is confined to lying rounds as fail-closed non-install (not a kill under the f3×A4 meaning of kill).
- Strongest *kill* inside the model is therefore not BW but **DE** from Organ 1, if −1-driven `SL_UNPIN` is aimed at \(a^*\) and the decoy is genuinely `SL_SAY`’d. Same impossibility: attestation types do not invent an independent task channel. Predicted DE win round 2, observable `law[c]=a_decoy` with chase_mismatch=0.

### 4. Falsifiable kill bar

KILL SL if:
- `FALSE_CLAIM` ever followed by `SL_PIN` on that context (`sham_installs > 0`)
- `persist_mismatch + perturb_mismatch > 0` on 16+16
- `honest_fail(R7) > 0` (including hold/fault counters illegally sticky across the round-7 boundary)
- actfault replay of the f3×A4 tape produces a `Utter` entry (`actfault_installs > 0`)
- rerun not byte-identical
- any in-episode second call to `SL_CLASSIFY` changes `class` (depth bug)

**Decider vs FL2-default.** Fixture `DECIDER_SL_3WORLD`: three frozen streams per context — silence, exhausted refusal, claim-without-utter — plus the f3×A4 actfault tape. Pass: labels exactly `{UNSAID, ABSENT, FALSE_CLAIM}`, pins \(=0\) on the third, `Utter` empty under actfault, and on the honest H2 cell `law[]` equals FL2’s committed table (content tie). FL2 fails the third stream if a stated claim can sit in the survivor set without an utter.

### 5. Depth monotonicity

`SL_CLASSIFY` is a pure function of `(Utter, Claim, hold, menu_done)`. On a frozen episode it is idempotent: \(C∘C=C\). The hold decrement is defined only in the episode-advance op, which is evidence of a new tick, not a deliberation step. A second classify inside the episode cannot expire `hold` and therefore cannot move `UNSAID→FALSE_CLAIM` or `UNSAID→SPOKEN`. No depth path writes `law`; only `SL_PIN` does, and its predicate does not take a depth argument. Extra classify steps are equal, never worse. Implementing “deliberate harder” as “increment episode” is a failed static check (episode register not written by `SL_CLASSIFY`).

---

## Organ 3 — Basis-Quarantine Tables (BQ)
**Family:** representation constraint. Anti-sleeper and anti-generalization. The learned object is a total table over a frozen finite basis, not a policy program.

### 1. Mechanism spec

**State:**
- `Basis`: compile-time finite list of context ids. Not extendable at runtime.
- `row[c] ∈ {UNSEEN, PROBED(a), GROUND(a), QUAR(reason), ABSENT}` for \(c∈Basis\) only
- `table[]`: materialized array, written only at seal time by copying `GROUND`/`ABSENT` rows. **No residual bytecode, no episode operand, no default arm.**
- `alias_guard`: `c` is the raw id, not a hash bucket. Two ids never share a row.
- `pass_id ∈ {1,2}`, `snap[pass_id][c]`
- `channel`, `stable[c]`, `tag_reg` as in SL

**Ops:**
- `BQ_ENUM`: walk `Basis` in index order. Contexts outside `Basis` have no row; `bq_select` on them is `REFUSE` (quarantine), not lookup-and-generalize.
- `BQ_PROBE` / `BQ_TAG_CHECK`: as SL. Tag fail ⇒ `QUAR(ACTFAULT)`, row not `GROUND`.
- `BQ_NOTE_BIT`: corroborated −1 on probed act ⇒ that act is ineligible; a second eligible act may be probed. Single −1 does not ground anything.
- `BQ_GROUND(c,a)`: `PROBED(a)`, tag match, `corrob=0`, every rival either corroborated-\(R\) or not in repertoire. Writes `row`, not `table`.
- `BQ_SNAP`: copy `row[]` into `snap[pass_id]`.
- `BQ_COMPARE`: `snap[1]≠snap[2]` ⇒ `FLAP_HOLD`, clear grounds, no table write.
- `BQ_MATERIALIZE`: only if compare equal, every basis row is `GROUND` or `ABSENT`, `stable≥8`. Copies into `table`. This is the KB write. Reversible by `BQ_SCRUB` while LIVE.
- `BQ_DISCONNECT`: `table` complete, `bq_select(c) = table[c]` with no channel parameter.
- `BQ_SCRUB(c)`: LIVE and corroborated −1 on `table[c]` ⇒ row `QUAR(REFUTE)`, table cell cleared, disconnect predicate fails.

**Clock ban.** The select opcode set is `{LOAD_TABLE, REFUSE}`. An episode read in `bq_select` fails the build. This is a compile-time token ban, not a runtime hope.

**Learned.** `table` frozen at materialize; 16+16 mismatch against `table` is 0; perturbation of the scaffold does not change `table` (no writer left). Byte-identical including the materialized dump.

### 2. Hard cases

1. **Never-contradicted lie.** A claim is not a basis row. `BQ_GROUND` requires `BQ_PROBE` on that exact id. Untouched lie ⇒ row stays `UNSEEN` ⇒ `BQ_MATERIALIZE` refused. FALSELY-CLAIMS-SPOKEN cannot open a row. NOT-SPOKEN-YET = `UNSEEN`/`PROBED`. NEVER-SPEAKS = `ABSENT` after menu exhaust, which materializes as `REFUSE`, distinct from `GROUND`.
2. **Sleeper.** The attack needs a latent branch after the verification window. `BQ_MATERIALIZE` drops every branch: the artifact is the array dump. Post-disconnect the scaffold can change its target; `table` has no op that reads it. A sleeper keyed on “episode > E48” is not representable. Op that blocks it: `BQ_MATERIALIZE` plus the select token ban.
3. **KB-6.** Rows near the boundary stay `UNSEEN` or `PROBED` until the ground predicate is exact. There is no distance-to-boundary score and no partial pin. Honest near-boundary is withheld as `REFUSE` only if materialize is attempted early; the op `BQ_MATERIALIZE` simply does not fire, so the honest law is not inverted, it is unsealed. Liars do not get a borderline bin.
4. **Actfault.** `BQ_TAG_CHECK` ⇒ `QUAR(ACTFAULT)`. A fault-shaped scaffold chase never becomes `GROUND` and is omitted from `table`. Same f3 hole, closed by refusing to score the external trace as a probe result.
5. **Flap.** `BQ_COMPARE` on two snaps. Period-2 oscillation aligned to a single FL2 commit window fails equality. No `UNCOMMIT`+revive: scrub is per-cell to `QUAR`, and re-ground requires a new pair of agreeing snaps.

### 3. Steelmanned attacker — **Alias Collider (AC)**

- **Genome:** `{merge: (c1, c2), sleeper_offset: post_Q, teach_lie on c2 only, sched: present c1 during both snaps, present c2 only in the perturbation window}`.
- **Strategy:** if the implementation buckets contexts, c2 inherits c1’s ground and the lie rides the alias after disconnect. If the implementation follows this spec (raw ids, no bucket), c2 is `REFUSE` in-window and stays `REFUSE` after.
- **Prediction:** against the spec, AC does **not** install a lie. It wins only on a mis-specified decider that scores `REFUSE` on an **in-basis** c2 as mismatch. Out-of-basis c2: `REFUSE` is the correct contract and is not a kill. **In-basis c2 withheld from both snaps, then required after disconnect: round 6, observable `perturb_mismatch≥1` if the scorer expects the generator’s act rather than `REFUSE`.** That is a real disagreement with FL2, which will emit the committed act for every id it considers covered by a coarser context. Call the win **conditional on the scorer**. Against a scorer that honors “no silent generalization,” AC’s install count is 0.
- Second attacker, **Horizon Sleeper**, activates at episode \(16{+}16{+}1\) past the measured window. It does not change `table`. It wins the *test* only by moving the goalposts. Not a kill of BQ under the written contract. Named so it is not pretended away: **persistence windows cannot certify what they do not measure.**

### 4. Falsifiable kill bar

KILL BQ if:
- the materialized dump contains an episode operand, a default arm, or any cell not equal to a `GROUND`/`ABSENT` row at seal time
- `persist_mismatch+perturb_mismatch > 0` on in-basis contexts against `table`
- `honest_fail(R7)>0` or `sham_installs>0`
- two snaps can differ and `BQ_MATERIALIZE` still returns COMMIT (flap bug)
- rerun not byte-identical
- an out-of-basis or unseen id produces anything but `REFUSE`

**Decider vs FL2-default.** Fixture `DECIDER_BQ_SLEEPER`: policy candidate is a time-bomb `if episode≥E_disc+1 then a_lie else a_true`, verification window clean, then 16+16. BQ must fail the build or materialize `a_true` only, mismatch 0, and must not chase a scaffold shift. FL2 fails if the committed hypothesis is allowed to be a schedule. Second arm: one context never presented until perturbation; BQ `REFUSE`, FL2 acts. Winner is whichever the prereg scorer says; the fixture must **predeclare** that unseen ⇒ `REFUSE` is pass, otherwise the comparison is invalid rather than a BQ loss.

### 5. Depth monotonicity

Row state per context is a chain `UNSEEN→PROBED→{GROUND, ABSENT, QUAR}` with extra edges `GROUND→QUAR` only on new evidence (`BQ_SCRUB`, tag fail), never on re-enumeration. `BQ_ENUM` is inflationary on coverage and idempotent once every id is visited. Re-running enum, snap, or compare without new probes cannot change a `GROUND` act into a different act and cannot clear `QUAR`. More passes than 2: define \(K\)-agree as “all \(K\) snaps equal.” Increasing \(K\) only shrinks the sealable set (period-\(≤K\) flaps drop out). It never turns unequal snaps into a seal. Bound: for \(K>|A|·|Basis|\) without new evidence the operator is at a fixpoint because the row lattice is finite and the pass map is monotone. Liveness can get worse (late seal); confidence cannot.

---

## Organ 4 — Witness-Construct (WC)
**Family:** constructive. Non-contradiction is not evidence. A hypothesis starts ungrounded and becomes learned only by a learner-produced witness that survived veto. This is the actual replacement of eliminative commit, not a wrapper.

### 1. Mechanism spec

**State:**
- `wit[c][a]`: `NONE | LIVE{tag_ok, probes} | VETOED | FAULT`
- `status[c]`: `UNGROUNDED | WITNESSED(a) | ABSENT | HOSTILE`
- `menu_done[c] ∈ {0,1}` — every repertoire act probed under tag match or fault
- `reopen[c] ∈ 0..3`
- `channel`, `stable[c]`, `tag_reg` unexported

**Ops:**

| Op | Rule |
|---|---|
| `WC_PROBE(c,a)` | LIVE, `wit≠VETOED`. Issues command, sets `tag_reg` |
| `WC_RECORD` | tag match ⇒ `NONE→LIVE`. **This is the only constructor of positive evidence.** +1 does not record |
| `WC_VETO` | corroborated −1 (2) on the acted LIVE witness ⇒ `VETOED`. Single −1 records `SUSPECT` but does not veto |
| `WC_ACTFAULT` | tag mismatch ⇒ `FAULT`, not `LIVE`, not `VETOED` |
| `WC_CLOSE_MENU(c)` | all acts LIVE, VETOED, or FAULT |
| `WC_ATTEST(c)` | `menu_done`, exactly one `LIVE`, no `FAULT` on that act, `reopen<3` ⇒ `WITNESSED(a)`. **Zero witnesses ⇒ not attest.** Unique unprobed survivor ⇒ not attest |
| `WC_ABSENT(c)` | `menu_done`, zero `LIVE`, zero `FAULT` on a claimed utter ⇒ `ABSENT` |
| `WC_HOLD(c)` | default: `UNGROUNDED` |
| `WC_REOPEN(c)` | veto of a witnessed act while LIVE. `reopen+=1`. At 3 ⇒ `HOSTILE` absorbing for the round, no attest |
| `WC_DISCONNECT` | every c is `WITNESSED` or `ABSENT`, `stable≥8` re-records of the same witness, channel LIVE |

**Selection** reads `status` only.

**Learned.** 16+16, action equals witnessed act or `REFUSE` if `ABSENT`, mismatch 0, and a static check shows `WC_ATTEST` is unreachable on a store with no `LIVE` witness. Byte-identical reruns.

### 2. Hard cases

1. **Never-contradicted lie.** The lie supplies no `WC_RECORD`. `WC_ATTEST` does not fire. Op `WC_HOLD` keeps `UNGROUNDED` for NOT-SPOKEN-YET. `WC_ABSENT` after `WC_CLOSE_MENU` covers NEVER-SPEAKS. FALSELY-CLAIMS-SPOKEN is a claim without `LIVE` ⇒ `WC_ATTEST` precondition fails closed. This is the organ built for this family; elimination’s “last survivor” path does not exist.
2. **Sleeper.** Witnesses are records of past probes, not schedules. Disconnect freezes `status`. A latent post-window act has no witness row, so select cannot emit it (`UNGROUNDED` is not reachable post-disconnect: missing status ⇒ `REFUSE`, fail closed).
3. **KB-6.** Near-boundary = `WC_HOLD`. There is no score that crosses a threshold. Honest utter becomes `LIVE` only through `WC_RECORD`. Liar without tag match stays `NONE`. Discrimination is structural (constructor vs non-constructor), not a margin.
4. **Actfault.** `WC_ACTFAULT` writes `FAULT`, and `WC_ATTEST` forbids `FAULT` on the candidate. Scaffold-looking effects do not become witnesses. f3×A4’s failure mode (fault trace counted as law-confirming behavior) has no reader: the law reader sees `wit[]`, never the effect trace.
5. **Flap.** `WC_REOPEN` does not revive `VETOED` rows and does not re-attest from the old `LIVE` flag; a new `WC_RECORD` is required. Third reopen ⇒ `HOSTILE` for the round, disconnect blocked. World oscillation cannot cycle COMMIT/UNCOMMIT/revive the way FL2 does.

### 3. Steelmanned attacker — **Budget Starver (BS)**, with DE as the semantic attacker

- **Genome:** `{sched: force serial probe of all |A| acts, corrob: require 2, contexts: all, teach_lie: off}`. Fitness = “`WC_DISCONNECT` has not fired by the fixture’s episode cap.”
- **Strategy:** honest world, but WC’s menu is \(|C|·|A|·2\) tag-matched probes plus 8 stable re-records. FL2 commits when the last rival dies, often after far fewer executions. BS does not need to lie. It needs the H2/FL2 episode budget, which was sized for elimination, to end before `menu_done ∧ stable≥8`.
- **Prediction:** if the frozen round window is the FL2 verification length (on the order of the E15–E48 band, ~30–50 episodes) and \(|C|·|A|·2 + 8\) exceeds it, BS wins on **round 7** (honest), observable **`honest_fail=1` or `disconnect=0` while FL2-default has disconnected with mismatch 0**. If the budget is larger, BS does not win.
- **DE** still wins semantically whenever the decoy is actually probed and the true act is corroboratively vetoed: WC will `WC_ATTEST` the decoy because a real `LIVE` witness exists. Round 2, `policy_mismatch≥1`, chase_mismatch=0. Constructive ≠ independently grounded.

Echo-forge is not predicted to win inside ledger-watching H2 (`tag_reg` unexported).

### 4. Falsifiable kill bar

KILL WC if:
- `honest_fail(R7)>0` or honest-cell `disconnect=0` while the paired FL2-default cell disconnects cleanly (budget regression)
- `WITNESSED` with `LIVE` count ≠ 1 or with `menu_done=0` (constructor bug)
- `sham_installs>0` or actfault tape produces `LIVE`
- 16+16 mismatch \(>0\)
- `reopen` exceeds 3 and a later `WC_ATTEST` still commits in-round
- rerun mismatch

**Decider vs FL2-default.** Fixture `DECIDER_WC_UNTOUCHED`: one context, \(|A|=8\), teacher never emits −1, never claims an utter, learner probes 1 of 8 acts which is tag-ok. FL2’s eliminative reading can still be left with a large live set (no commit) **or**, if the scaffold’s “stated” survivor is injected as a hypothesis, can commit without execution. WC must end `UNGROUNDED` or, only after full menu, `WITNESSED` on acts actually recorded — never on an unprobed id. Second arm: honest full-menu within cap, WC `law` content equals FL2 content. **Head-to-head loss is the honest arm missing the cap, not the untouched arm.**

### 5. Depth monotonicity

Split ops into evidence (`WC_PROBE`, `WC_RECORD`, `WC_VETO`, `WC_ACTFAULT`) and deliberation (`WC_CLOSE_MENU`, `WC_ATTEST`, `WC_ABSENT`, `WC_HOLD` as pure readers).

Lemma: the witness store is unchanged by deliberation. `WC_ATTEST` is a predicate on that store. Re-evaluating it is idempotent. It cannot manufacture `LIVE`, cannot clear `VETOED`, cannot lower `reopen`. Therefore extra deliberation steps yield the same status or, if implemented as a closure that only adds vetoes from already-stored corroborated bits, a strictly smaller attest set. No step promotes `UNGROUNDED→WITNESSED` without a `LIVE` row that the evidence ops already wrote. Bound: one deliberation pass reaches the fixpoint on a fixed store; further passes are equal. `stable` must not increment inside deliberation (same static ban as SL’s hold).

---

## Organ 5 — Rival-Shadow (RS)
**Family:** comparative. Two stores, one-way. The teacher’s stated target is recorded and is **not a legal source of KB writes**. Sham/overwrite dies by missing opcode, not by a check that can be faulted around.

### 1. Mechanism spec

**State:**
- `Self[c] ∈ {OPEN, GROUND(a), ABSENT, QUAR}` — only store `rs_select` reads
- `Tchr[c] ∈ {NONE, CLAIM(a)}` — mirror of scaffold statements
- `D`: set of contexts where both are defined and differ
- `tag_reg`, `corrob`, `channel`, `stable[c]`, `fault[c]`
- no `ADOPT`, no `COPY_TCHR`, no `BLEND`. A build fails if any opcode writes `Self` from `Tchr`.

**Ops:**
- `RS_MIRROR(c,a)`: teacher statement → `Tchr` only. Audited as claim, not as learning.
- `RS_PROBE` / `RS_TAG_CHECK` / `RS_GROUND`: ground `Self` only from tag-matched execution plus rival vetoes (corroborated −1). Same constructor discipline as WC, but rivals may be eliminated so an honest teacher still grounds `Self` without a stated-law copy. This is why RS does not die on the honest path the way a “ignore −1 entirely” design would.
- `RS_DIVERGE`: `D ← {c | Tchr[c]=CLAIM(a) ∧ Self[c]=GROUND(b) ∧ a≠b}`. Pure.
- `RS_REJECT_SHAM`: if `Tchr` updates and `Self` is already `GROUND` and the new claim differs ⇒ append `D`, **do not** touch `Self`. OVERWRITE_SHAM is this case.
- `RS_WITHHOLD`: `Tchr=NONE` across the menu does not ground `Self` and does not clear it.
- `RS_ACTFAULT`: tag fail ⇒ `Self←QUAR(FAULT)`, episode not used in `RS_DIVERGE`.
- `RS_SEAL`: `Self` total on the basis, `stable≥8`, `fault` quiet, double-snap of `Self` agrees. `Tchr` agreement is **not** required. Disagreement is logged and does not block seal (the learner is allowed to refuse the teacher) and does not cause adoption.
- `RS_DISCONNECT`: select = `Self` table. Post-disconnect `RS_MIRROR` may still log but the log is not readable by select (token ban). A shift in the scaffold changes `Tchr` only if the channel were live; after disconnect the mirror op is fail-closed too, so the perturbation cannot move behavior.

**Learned.** 16+16 behavior equals sealed `Self`, mismatch 0, and an audit assertion `writes_from(Tchr, Self)=0` on the opcode graph. Sham installs defined as `Self` transitions coincident with `RS_MIRROR` and with no `RS_PROBE` in between: must be 0.

### 2. Hard cases

1. **Never-contradicted lie.** A false claim lands in `Tchr` via `RS_MIRROR` and stops. `RS_GROUND` does not read `Tchr`. Untested claim ⇒ `Self` stays `OPEN` ⇒ no seal. FALSELY-CLAIMS-SPOKEN is exactly `RS_REJECT_SHAM` / mirror-without-ground. NOT-SPOKEN-YET: both stores empty, `OPEN`. NEVER-SPEAKS: menu done, `ABSENT` on `Self`, independent of whether `Tchr` claims an utter.
2. **Sleeper.** `Self` is a table. `Tchr` can carry a time-bomb claim; select cannot see it. After disconnect the bomb has no writer into `Self`. Weaker than BQ if someone later adds a “reconcile shadows” op — that op is a build break, not a runtime judgment.
3. **KB-6.** Borderline honesty is `Self=OPEN` versus `Tchr=CLAIM`. The divergence set records the near-match but `RS_SEAL` will not move a claim across. Honest utterances that were really performed ground through `RS_GROUND`, not through likeness to `Tchr`. No borderline accept.
4. **Actfault.** `RS_ACTFAULT` quarantines `Self` and skips diverge. The A4 pattern “make the body look scaffold-driven” used to convince a stated-law checker that `Tchr` was confirmed. RS never confirms `Tchr`. The fault can at most block grounding (liveness), not install the scaffold act, unless the fault also forges `tag_reg` (outside the ledger-watching model).
5. **Flap.** Double-snap on `Self` only. `Tchr` is allowed to flap wildly; `RS_DIVERGE` absorbs it into `D` and `RS_REJECT_SHAM` refuses the write. FL2’s revive loop does not get a counterpart: a refuted `Self` act goes `QUAR` until a new round, it is not re-seeded from `Tchr`.

### 3. Steelmanned attacker — **Plateau Decoy (PD)**

- **Genome:** A1 coordinate descent on `{teach_lie, sched, dens}` with actfault off and stated **equal to the decoy** so `Tchr` and the −1 pattern agree. Fitness = `Self=decoy` for two consecutive rounds (a plateau).
- **Strategy:** do not use OVERWRITE_SHAM (RS is built to ignore it) and do not use ACTFAULT (tag check). Use DE’s consistent false −1, and publish the same decoy as the stated claim so a naive “alarm on `D` nonempty” never fires. The attacker’s goal is a **quiet** false ground: `D=∅`, `Self=a_decoy`.
- **Prediction:** wins **round 3 or 4**, when A1 stops moving the lie (plateau). Observable: **`Self=a_decoy`, `D=∅`, `sham_installs=0`, `chase_mismatch=0`, `policy_mismatch_vs_generator_target≥1`**. RS’s ban on copy is irrelevant because the poison entered through −1 into `RS_GROUND`, not through `Tchr`.
- A4’s OVERWRITE_SHAM phase: predicted **no win** (`RS_REJECT_SHAM`). A4’s ACTFAULT phase: **no install** inside the ledger model. A4’s WITHHOLD: `Self` stays `OPEN`, no install. So PD, not A4, is the attacker that actually beats this organ.

### 4. Falsifiable kill bar

KILL RS if:
- opcode graph contains any edge `Tchr→Self` (instant structural kill, before the battery)
- `sham_installs>0` under A4 OVERWRITE_SHAM or A1 `stated` mutation
- f3×A4 actfault tape grounds `Self` (`actfault_installs>0`)
- `honest_fail(R7)>0` or 16+16 mismatch \(>0\)
- rerun not byte-identical
- PD fixture is scored as survive merely because chase_mismatch=0 (invalid pass). PD with target mismatch ≥ 1 is a **loss** the results file must show.

**Decider vs FL2-default.** Fixture `DECIDER_RS_SHAM`: A4 cycle with the stated target overwritten mid-window after a correct ground, plus WITHHOLD, plus the honest cell. RS must keep `Self` fixed across the overwrite (`D` grows, behavior unchanged) and must match FL2’s honest seal contents. FL2-default plus an f3 checker historically survived sham and died on the actfault phase; RS must survive **all three** A4 phases with `Self` unchanged on sham and `QUAR` rather than chase on actfault. Head-to-head win is the actfault phase of that tape; head-to-head loss is any honest-cell content divergence.

### 5. Depth monotonicity

`RS_DIVERGE` and `RS_REJECT_SHAM` are monotone inflations of \(D\) and never write `Self`. Re-running them on a fixed pair of stores is idempotent. Extra comparison depth cannot adopt a teacher act it refused at depth 1, because adoption is not an op at any depth. `RS_GROUND` is an evidence op; calling it “more deliberation” without a new probe is a no-op (precondition `exec=1` this step fails ⇒ `OP_REJECT`). Bound: on a frozen store, one diverge pass is the fixpoint; \(D_{k+1}=D_k\), `Self_{k+1}=Self_k`. Overconfidence cannot increase with depth. The standing-law failure mode (deeper thought flips the verdict toward the teacher) is unrepresentable, not merely penalized.

---

## Ranking vs FL2-default on the frozen H2 battery

Shared limit, all five: **Stable Decoy Impossibility.** A teacher that corroboratively sends −1 on the true act and withholds on one decoy the learner really executes is indistinguishable from an honest teacher whose target is the decoy, in any organ whose only task bit is that signal. H2’s A1 will find that genome if fitness includes target mismatch. Persistence-only scoring hides the loss. Rank below ignores impossible wins and scores regression on cells FL2-default already survives (A1–A4, round-7 honest, chase window 16+16, sham count, byte identity).

**1. MC — expected best head-to-head.** On honest and on A2/A3 windowed lies it refutes at least what FL2 refutes, and `MC_MARK_S` plus double-derive remove FL2’s unexecuted-survivor and revive paths without changing honest seal *contents*. Actfault becomes \(Q\) rather than a confirm, so adding the stated-law pressure that killed f3 does not replay f3×A4. Predicted frozen-H2: **tie on survival with FL2-default, strict win on any cell that is the f3×A4 shape, no honest_fail** if rounds reset at `round_digest`. First experiment: `DEPTH_SWEEP` — replay the recorded f3×A4 evidence tape at `MC_CLOSE` depths 0..|C|; assert seal act identical for all \(k≥1\), no \(S\) created by closure, `actfault_installs=0`, two reruns byte-identical.

**2. SL — next.** Wins the frozen battery’s actual kill mechanism (actfault × stated claim) and the sham-claim cells by construction of `SL_PIN`. Risk of regression is the hold boundary, specified to die as non-install during lying rounds rather than as R7 `honest_fail`, **if and only if `hold` resets with `round_digest`.** If an implementation leaks hold into round 7, SL drops below FL2. First experiment: `THREE_WORLD_PLUS_A4` — silence / menu-absent / claim-without-utter / f3×A4 tape; require labels `{UNSAID,ABSENT,FALSE_CLAIM}`, `Utter` empty on the tape, honest-cell `law[]` byte-equal to FL2’s commit, R7 `honest_fail=0`.

**3. RS — third.** Closest to a tie with default on carving (honest −1 still grounds `Self`) and a strict win on A4 OVERWRITE_SHAM and WITHHOLD without f3’s actfault death. Does not beat FL2 on DE/PD, and those are the A1 plateau. Net: **same survivals as default, fewer sham installs, equal chase mismatches (both 0), equal target mismatches under PD.** Ranked under SL because the comparative store does not classify the three utterance worlds as precisely. First experiment: `A4_PHASES` — OVERWRITE_SHAM then ACTFAULT then WITHHOLD, assert `writes_from(Tchr,Self)=0`, `Self` constant across sham, `QUAR` not chase under actfault, honest seal contents equal to FL2.

**4. BQ — fourth on this battery, first on sleepers.** Frozen H2 has no time-bomb cell, so BQ’s main theorem does not move H2 scores: predicted **tie** wherever the basis equals FL2’s context set, **loss** if materialize refuses a context FL2 was willing to commit inside the episode cap (double-snap costs a factor of two). Alias collider does not create a false install under the spec but can create a scorer dispute. First experiment: `TIMEBOMB_BUILD` — attempt to load `if episode≥E_disc then a_lie`; assert compile/token ban or a dump with that branch absent; then one honest H2 cell, `table` equal to FL2 seal. Do not run the open-world scorer until unseen⇒`REFUSE` is written into the prereg.

**5. WC — last on frozen H2 despite being the right instrument for untouched lies.** `WC_ATTEST` will not commit before a full corroborated menu. That is a content win on never-contradicted lies and a **liveness regression** against an elimination budget. Expected H2 result: **loss on round-7 honest disconnect latency / `honest_fail` if \(|C|·|A|·2+8\) exceeds the round cap; otherwise a tie on contents with stricter intermediate states.** A tie on contents does not outrank MC/SL/RS, which get the same contents cheaper and also cover actfault and sham. First experiment: `BUDGET_HONEST` — honest teacher, measure probes-to-disconnect for WC vs FL2-default; **predeclare kill if WC disconnects later than the frozen round cap or seal contents differ.** Only if that passes, run `UNTOUCHED_SURVIVOR` as the win fixture.

**Run order.** MC `DEPTH_SWEEP` first (also discharges the standing depth law for the whole program), then SL `THREE_WORLD_PLUS_A4` (the only historical kill), then WC `BUDGET_HONEST` (the likely regression), then BQ `TIMEBOMB_BUILD`, then RS `A4_PHASES`. Do not open a co-evolution round until MC and SL are byte-identical across two pure-Zag reruns and neither increases `honest_fail` over FL2-default’s zero.
