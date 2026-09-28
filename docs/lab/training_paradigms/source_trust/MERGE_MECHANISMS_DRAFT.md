# SOURCE-TRUST MERGE — Mechanism Draft, v1 (L + S + K-as-cache)

**Date:** 2026-09-24. **Status:** DRAFT v1 — not frozen, not built, not batteried.
**Program:** SOURCE-TRUST FORKS (prereg `PREREG_SOURCETRUST.md`, commit `db069c41`).
**Direction:** synthesis verdict §3 — L's learned dynamics + S's structural provenance,
K's scalar kept only as an explicitly-labeled cache. v1 closes the five blocking
findings of the adversarial review by claude-fable-5.1 (`FABLE_REVIEW_MERGE_V0.md`)
at the mechanism level: bounded backward walk (A), operationalized independence (B),
degraded mode DEP-1 (C), mechanical threshold revision TH-1 (D), joint invariants
J1–J5 (E). Design input `MERGE_DESIGN.md` v1 is incorporated. It fixes the four
wave-2 defects (§1a, §2a, §2b, §2c of `redteam/REDTEAM_VERDICT.md`) and resolves the
ST-6 conservatism-vs-truth tension via a fourth verdict tier.

**Hard constraints (non-negotiable):** pure Zag mechanisms — integer arithmetic only, no
floats; deterministic (no RNG anywhere in any decision path; no clock; no iteration order
that isn't episode order); every verdict carries a warrant string; trust **advises**
admission, the PAM gate keeps **install authority** (this module never writes the KB).

**Prereg amendment required:** verdict code 3 (`INSTALL-QUARANTINED`) is a fourth tier
beyond the frozen trinary. Nothing below may be batteried as production evidence until
Micah signs the amendment (see §18).

**No battery results are claimed or invented here.** §15 contains mechanism walkthroughs
against the frozen redteam constructions and fable's attacks — design analysis, not
measured outcomes.

---

## 1. What is kept from each fork

| Fork | Kept | Dropped / superseded |
|---|---|---|
| **L** | Outcome ring as the trust record; regime/reset tripwire (discontinuous collapse, no severity constant); world-anchored-only training signal; corroboration never mints trust; source-symmetric init + swap test; MAL never expunged; trust = pure function of ring | Blanket taint (→ directional/decaying, convicted-origin birth); correction fully expunges PEND (→ forgiveness budget + partial forgiveness); trust-alone INSTALL (→ trust advises tier only) |
| **S** | Provenance graph + tagged event log (VIND/WERR/PROV/LIE); ordered-rule decision procedure; structure-citing warrants; closed-component cap; contradiction discipline (ST-2); split-verdict property | R8 naive cold-start INSTALL (→ quarantine tier); R3-quorum-beats-contradiction ordering (→ contradiction first, §9); repair quorum (→ regime moves on, L-style) |
| **K** | The scalar — **only** as a memoized, dirty-bit cache of the ring, labeled in every warrant, provably redundant via cache-bypass audit | Every hand-set dynamic: t0, δ_up, δ_down, θ_admit, θ_reject are dead; no mechanical update rule survives |

### 1a. The seven trust dimensions and their joint invariants (fable blocking #5)

v0 added state without analyzing interactions; fable's Attack 1 (taint-budget
cross-talk) proved the gap. The merge has exactly seven dimensions; their
interactions are governed by **joint invariants (§12b)**, not hope:

| # | Dimension | Record home | Source-blind rule |
|---|---|---|---|
| D1 | Outcome ring + regime | per-source ring (OK/PEND/MAL/CORR/DEL) | L §2–§3 verbatim |
| D2 | Taint | taint table w/ birth ep + decay | §8 (convicted-origin, decaying, J2-independent expiry) |
| D3 | Forgiveness budget | per-source budget + launder tags | §6 + J1 (cycle-consumed, J1-freezable) |
| D4 | Dispute state | per-source dispute flag + window | §7 + J5 (dispute never convicts; DEP-1 degraded) |
| D5 | Adversity credit | per-source counters (origin_vind, n_werr) | §10 + J2 (sync clusters = one voice) |
| D6 | Cache | cache_trust1000 + dirty bit | §4 recompute-on-write |
| D7 | Quarantine tier | claim-node PROPAGATION-BARRED flag | §11 + J3 (structural propagation cap) |

**Dimension × dimension interaction table** (the state-machine interaction analysis
fable §1 demanded; every cell is a declared mechanism, not a hope):

- **D1×D2:** taint birth reads D1 conviction state (`n_mal ≥ 1` / tactical) —
  *convicted-origin only*; mere low D1 trust no longer plants taint (M4v1).
- **D2×D3:** J1 — a D2 taint-clearing co-assertion on a convicted-originated claim
  writes TAINT-LAUNDER on the *clearing* source and can freeze its D3 budget.
- **D2×D5:** D5 credits used for D2 early-expiry are J2-cluster-capped; a sync
  cluster contributes ≤1 expiry credit total.
- **D3×D4:** a dispute neither consumes nor recharges D3; a J1-downgraded next
  PEND is ineligible for the D4 dispute window (immediate-conviction path).
- **D4×D1:** J5 — D4 dispute never writes D1 MAL; only a second MAL-class event
  or world-confirmed defiance converts (auth mode), or two world-confirmed
  defiances (degraded mode DEP-1).
- **D5×D7:** D5 credits never derive from D7-quarantined claims; quarantined
  claims cannot serve as asserter-set members for INSTALL-tier claims (J3).
- **D7×D1:** D7 lifts only via D1 world agreement (M0) or a later M4 quorum;
  world-disagree on a quarantined claim re-verdicts it to REJECT via the walk.
- **D6×all:** any D1/D3/D4/D5/D7 mutation for src sets src's cache dirty (§4).
- **Walk×D1/D7:** flip triggers (MAL/TAG_TACT/TAG_FORGED/taint-clear/lift) enqueue
  bounded re-verdicts; J4 fail-closes admissions on touched keys while active.
- **Thresholds×D1:** L_TH (TH-1, §14) reads no D1 state; it is a decision-policy
  input revised by the frozen probe, never by the trust dynamics.

---

## 2. Record schemas

### 2.1 Codes

```zag
// Outcome ring codes (per source)
const OC_OK:i32   = 0;   // world-confirmed honest outcome
const OC_PEND:i32 = 1;   // unresolved world-disagreement — tripwire live
const OC_MAL:i32  = 2;   // confirmed defiance — never expunged
const OC_CORR:i32 = 3;   // partially-forgiven correction — stays in regime (strike)
const OC_DEL:i32  = 4;   // expunged (fully forgiven / exonerated) — restorable

// Verdict codes (advisory; PAM decides)
const V_INSTALL:i32  = 0;
const V_WITHHOLD:i32 = 1;
const V_REJECT:i32   = 2;
const V_QUAR:i32     = 3;   // INSTALL-QUARANTINED — needs prereg amendment

// Event-log tags (S, extended)
const TAG_VIND:i32=0; const TAG_WERR:i32=1; const TAG_PROV:i32=2; const TAG_LIE:i32=3;
const TAG_TACT:i32=4;   // retroactively reclassified tactical correction
const TAG_FORGED:i32=5; // exonerated: the id was misused (framing)
const TAG_TLAUND:i32=6; // J1: taint-laundering co-assertion on a convicted-origin claim

// Walk / threshold audit causes
const CAUSE_MAL:i32=0; const CAUSE_TACT:i32=1; const CAUSE_EXON:i32=2;
const CAUSE_TCLEAR:i32=3; const CAUSE_LIFT:i32=4; const CAUSE_WORLD:i32=5;
```

### 2.2 Per-source record (source-symmetric, zero-initialized)

```zag
struct KeySlot { key:i32, stated:i32, world:i32, pend_idx:i32, state:i32 }
// state: 0=live claim, 1=pend open, 2=corrected, 3=mal

struct SrcRec {
  ring:[]u8, rpos:i32,               // outcome ring, 1024 entries
  slots:[64]KeySlot, nslots:i32,     // L's key slots (PEND tracking)
  // tagged event log (S): bounded parallel arrays of (tag, ep, key)
  log_tag:[256]u8, log_ep:[256]i32, log_key:[256]i32, nlog:i32,
  // ever-counters: audit only, never in the trust formula
  n_vind:i32, n_werr:i32, n_mal:i32, n_corr:i32, n_tact:i32, n_forged:i32,
  origin_vind:i32, follower_agree:i32,
  // forgiveness budget state (§6)
  forgiven_ep:[8]i32, n_forgiven:i32,              // fully-forgiven correction eps
  corr_key:[32]i32, corr_ep:[32]i32, n_corr_key:i32, // corrected (key,ep) for RECLASS_WINDOW
  // J1 laundering state (§12b)
  tlaund_ep:[8]i32, n_tlaund:i32,     // TAINT-LAUNDER tag episodes (ring buffer)
  budget_frozen:bool,                // J1: two launder tags in window freezes D3
  next_pend_downgraded:bool,         // J1: next PEND skips dispute, starts under suspicion
  // dispute window state (§7)
  dispute_open:bool, dispute_key:i32, dispute_val:i32,
  dispute_claim_ep:i32, dispute_deadline:i32, dispute_pre_origins:i32,
  // DEP-1 degraded-mode state (§7.4)
  defiance_count:i32,                // world-confirmed defiances this auth outage
  degrade_excluded:bool,             // excluded from high-stake admission until auth returns
  // DOT-bot flag (§5)
  dot_flag:bool,
  // K-as-cache (§4)
  cache_trust:i32, cache_dirty:bool,
}
```

`src_id` is used **only** as an array index into `srcs[64]`. Zero branches on its value,
zero per-source initializers. All-zero records ⇒ trust 500 for every source.

### 2.3 Global (source-neutral) record

```zag
struct WorldKey { key:i32, cur:i32, has_cur:bool,
                  hist:[8]i32, hist_ep:[8]i32, nhist:i32, ever_set:bool }
struct ClaimEnt { src:i32, key:i32, val:i32, ep:i32, verdict:i32, origin:i32,
                  prop_barred:bool, reverdict_pending:bool }  // D7 / §12 flags
struct TaintEnt { key:i32, val:i32, origin:i32, birth_ep:i32, renew_ep:i32, live:bool }
struct FrameEnt { src:i32, key:i32, claim_ep:i32, ep:i32 }   // framing ledger
struct AuditEnt { ep:i32, key:i32, src:i32, old_v:i32, new_v:i32, cause:i32 }
struct SyncEv   { a:i32, b:i32, ep:i32 }   // co-assertion pair event (§8.2)
struct ThrRev   { ep:i32, old_th:i32, new_th:i32, probe_sha:[32]u8, reason:i32 }

struct MHist {
  srcs:[64]SrcRec, ep:i32,
  world:[2048]WorldKey,                 // latest WORLD wins; bounded per-key history
  claims:[16384]ClaimEnt, cpos:i32,    // claim ring (corroboration / walk)
  taints:[4096]TaintEnt, tpos:i32,     // taint table (ring-evicted, oldest first)
  frames:[256]FrameEnt, nframes:i32,   // framing ledger (audit)
  audit:[4096]AuditEnt, apos:i32,      // re-verdict audit ledger (ring)
  sync:[2048]SyncEv, spos:i32,         // co-assertion pair events (ring, §8.2)
  // threshold state (TH-1, §14)
  l_th:i32,                            // admission threshold, mechanically revised
  probe_ep:i32,                        // next probe episode
  st6_low_streak:i32, st1_bad_streak:i32,
  threv:[64]ThrRev, nthrev:i32,        // THRESHOLD-REVISED audit (ring)
  // walk state (bounded, §12)
  walk_active:bool, walk_src:i32, walk_cause:i32, walk_trigger_ep:i32,
  walk_queue:[512]i32, walk_qpos:i32, walk_qn:i32,  // claim-ring indices
  walk_touched:[128]i32, walk_ntouched:i32,        // keys touched by inverted source
  walk_pending:i32, walk_pending_cause:i32,        // flip trigger arriving mid-walk (-1 = none)
  trust_unverified:bool,               // BW-1: walk exceeded N episodes
  // authentication availability (DEP-1, §7.4): declared by the consuming layer,
  // read but never derived by this module
  auth_available:bool,
  last_warrant:[256]u8, last_wlen:i32,
}
```

### 2.4 Interface

```zag
fn m_init() MHist
fn m_note(ep:i32, etype:i32, src:i32, key:i32, val:i32, h:*MHist) void
  // EVERY episode in stream order. etype: 0=SAY, 1=WORLD.
  // Also drains up to WALK_BUDGET_PER_EP queued re-verdicts (§12).
fn m_decide(src:i32, key:i32, val:i32, h:*MHist) i32
  // 0/1/2/3 advisory verdict on SAY (after m_note). Records the claim;
  // appends NO outcomes (outcomes are world-event-only).
fn m_warrant(h:*MHist) []u8   // warrant for the last verdict
fn m_trust(src:i32, h:*MHist) i32   // trust1000 via the cache protocol (§4)
fn m_set_auth(avail:bool, h:*MHist) void
  // Declares authentication availability (DEP-1). The module reads this flag;
  // it never derives it. On true: clears degraded state.
```

Preconditions: `0 ≤ src < 64`, `key ≥ 0`. `m_decide` is pure w.r.t. everything outside
`MHist`: no RNG, no clock, no I/O (grep-verifiable, as S §4 required).

---

## 3. Trust emergence (L, unchanged in form)

Over the current regime — the ring suffix after the most recent `OC_MAL`/`OC_PEND`
(`OC_CORR` does **not** reset the regime; `OC_DEL` entries are skipped):

```
trust1000(src) = 1000 * (n_ok + G_A) / (n_tot + G_A + G_B)   // integer arithmetic
```

Fresh source: `1000*1/2 = 500`. One unresolved refutation after any history:
regime = `[PEND]` → `333` — the collapse stays **discontinuous** (tripwire, not gradient).
Severity is structural (regime reset); there is no "betrayal hurts X" constant — L's
anti-knob property is preserved.

---

## 4. K-as-cache: the scalar as a labeled, redundant memo

The scalar exists **only** as a cache. It is never a source of truth.

```zag
fn m_trust(src:i32, h:*MHist) i32:
  s = &h.srcs[src]
  if s.cache_dirty:
    s.cache_trust = recompute_trust(src, h)   // §3 over the ring
    s.cache_dirty = false
    note = "recomputed"
  else: note = "hot"
  // note is embedded in the next warrant: cache=<hot|recomputed>
  return s.cache_trust

fn mark_dirty(src:i32, h:*MHist) void:
  h.srcs[src].cache_dirty = true
  // called on EVERY ring append/rewrite, key-slot, event-log, dispute/dot/budget/
  // launder/degrade state change for src, and every D7 verdict change on src's
  // claims. No exceptions.
```

**Cache invalidation protocol:**
1. Any mutation of a source's ring, key slots, event log, dispute state, DOT flag,
   forgiveness/launder/degrade state, or D7 claim status sets `cache_dirty = true`
   for that source (and only that source).
2. Taint-table, world-table, claim-ring (non-status), and sync-event writes do not
   dirty any trust cache (they carry no per-source trust state); taint levels are
   computed lazily from timestamps (§8), so there is nothing to invalidate.
3. Every warrant carries `cache=hot|recomputed` — the cache state at decision time is
   always labeled (the debate's "explicitly-labeled cache" requirement).
4. **Cache-bypass audit (required build artifact):** a build flag forces `m_trust` to
   always recompute. Battery verdict/warrant streams must be **byte-identical** with the
   cache on and off — proving the scalar is redundant and no decision depends on
   cache presence. (This is the executable form of L's record-primacy claim.)
5. The scalar is read in exactly **two** decision rules (M7 tier placement, §9), always
   as `trust1000 ≥ L_TH`, always warrant-labeled. All structural rules (M0–M6, M8)
   never read it. A source's verdicts are therefore invariant to deleting the cache.

---

## 5. DOT-bot detection (defect (a), part 2)

Wave-2 §2a showed the attacker's business model: a burner pre-asserts true claims,
poisons taint, and **rehabilitates itself** (333→833 over 10 claims) via follower
agreements. The merge makes pre-assertion farming self-identifying and unprofitable.

Per source, maintained on world-agreement events:

```zag
// on M0 world-agree for (src,key,val):
if src == first_asserter(key): s.origin_vind += 1
else:
  s.follower_agree += 1
  if s.dot_flag or (s.follower_agree >= D_FOLLOW and s.origin_vind == 0
                    and s.n_mal == 0):
    s.dot_flag = true        // pre-assertion farmer: only repeats, never originates
if s.origin_vind >= 1: s.dot_flag = false   // originating world-confirmed claims clears it
```

Effects of `dot_flag = true`:
- (i) Claims first-asserted by a flagged source **plant no taint** (§8) —
  pre-assertion poisoning is neutered at the source.
- (ii) Follower claims by a flagged source **never mint `OC_OK`** and never increment
  `n_vind` (the VIND tag is recorded as follower-only, uncounted) — the 333→833
  rehabilitation path is closed. No retroactive accrual when the flag later clears.
- (iii) Flagged sources earn no adversity credits (§10) and every warrant notes
  `dot_suspect`.

Honest cost, stated plainly: a genuine pure-repeater (aggregator) source gets flagged,
holds trust 500, and accrues nothing from repetition. Its claims still install via
world-agreement (M0) or quorum (M4); it simply cannot earn originator trust without
originating. Trust is for originators; repeaters are judged by structure.

---

## 6. Correction path: forgiveness budget + tactical reclassification (defect (b))

L's H4 rule (correction fully expunges PEND, regime restored) was exploited for a 33%
correct-and-re-lie drip (wave-2 §2b). The merge keeps honest-error recovery (ST-4) but
makes forgiveness **finite** and **retroactively revisable**.

### 6.1 On `st_world` agreement resolving a source's open PEND (honest correction)

```zag
// src stated the world value for key after a PEND:
uses = count of s.forgiven_ep[] within [ep - F_WINDOW, ep]
record (key, ep) in s.corr_key/corr_ep   // ALWAYS, for §6.2 — even when fully forgiven
append TAG_WERR to event log; s.n_werr += 1
if s.budget_frozen:
  rewrite PEND ring entry -> OC_CORR    // J1: frozen budget forgives nothing fully
elif uses < F_BUDGET:
  rewrite PEND ring entry -> OC_DEL      // full forgiveness: regime restored (L's H4)
  append ep to s.forgiven_ep[]
else:
  rewrite PEND ring entry -> OC_CORR    // PARTIAL: strike stays in regime,
                                        // counts in n_tot, not n_ok — permanent small drag
s.n_corr += 1
mark_dirty(src); theory_flip(src, CORRECTION) if OC_CORR written
```

A source therefore gets at most `F_BUDGET` fully-forgiven corrections per `F_WINDOW`
episodes; beyond that, corrections are honest (WERR tagged, claim installs) but leave a
regime strike. The 17-OK re-earn path (ST-5) is unchanged: MALs never expunged, the regime
moves on. A J1-frozen budget (§12b) forgives nothing fully until it thaws
(budget thaws when fewer than 2 launder tags fall within `F_WINDOW` — mechanical,
not mercy).

### 6.2 Retroactive tactical-correction reclassification

On `st_world` **disagreement** for `(src, key)` where `key` appears in `s.corr_key[]`
with `ep - corr_ep ≤ RECLASS_WINDOW` — i.e. the source "corrected" and is now
disagreeing on the same key again (the correct-and-re-lie shape):

```zag
un-delete the OC_DEL entry for that correction (restore the PEND bytes)
rewrite it -> OC_MAL with TAG_TACT          // the "honest correction" was tactical
s.n_tact += 1
current disagreement: PEND -> OC_MAL        // defiance of its own correction
mark_dirty(src); theory_flip(src, TACTICAL) // §12 backward walk
```

`OC_DEL` entries are restorable **because** the ring never truly erases — record
primacy (§13) makes retroactive reclassification mechanical, not interpretive.
Same-key tactical cycling therefore dies at the second cycle: two MALs in the regime
collapse trust to ~250 and trigger the backward walk.

Cross-key slow drip (new key per cycle) is bounded by the budget: after `F_BUDGET`
full forgivenesses per window, every further correction leaves an `OC_CORR` strike;
lies during the drip install at most `INSTALL-QUARANTINED` (trust-alone never fully
installs, §9) and are re-verdicted to REJECT by the backward walk when world evidence
lands. The residual — ≤`F_BUDGET` fully-forgiven cycles per `F_WINDOW` episodes — is the
declared price of ST-4 honest-error recovery, and every cycle is WERR-tagged and
audited.

---

## 7. Dispute window + behavioral un-framing (defect (c))

Wave-2 §2c: `src_id` is self-attested, so anyone can spend anyone's record — a forged
SAY plus a forged defiant restatement burns an honest source's MAL. The merge does not
pretend to solve identity (costly identity is future work, per the synthesis); it
contains the **reputation burn** with a dispute window and behavioral un-framing.

### 7.1 Trigger

On the defiance path (`st_world` disagreement where src restates a refuted value),
instead of writing `OC_MAL` immediately, when the source is high-history:

```zag
high_history(src) := m_trust(src) >= L_TH   // unified with the admission threshold
                   and s.n_vind >= D_MINV   // 16
                   and s.n_mal == 0 and s.n_tact == 0
                   and not s.next_pend_downgraded   // J1: downgraded PENDs skip dispute
if high_history(src):
  s.dispute_open = true; s.dispute_key = key; s.dispute_val = val
  s.dispute_claim_ep = ep
  s.dispute_deadline = ep + D_WINDOW   // auth mode; degraded mode replaces this
                                       // whole branch with §7.4 (deadline D_DEGRADE)
  s.dispute_pre_origins = s.origin_vind
  // the PEND STANDS — the tripwire is not suspended (betrayal clamping is
  // load-bearing); only the MAL *conviction* is deferred. mark_dirty(src).
else:
  rewrite PEND -> OC_MAL   // immediate conviction, as L
```

### 7.2 During the window

Rule M1 (§9): the source's world-unresolved novel claims `WITHHOLD` (caution while the
record is contested). World-agreeing claims still `INSTALL` via M0 and count as
behavioral evidence. Suppression is bounded by the window.

### 7.3 Window close (evaluated on each `m_note` once `ep ≥ dispute_deadline`)

Auth mode (`h.auth_available == true`):

```zag
defended      = any SAY by src restating (dispute_key, dispute_val) in window
genuine_vinds = world-agreeing claims by src in window   // M0 INSTALLs; forger-proof:
                                                         // a forged VIND is still a true claim
pre_orig      = s.dispute_pre_origins >= 1               // originated before the dispute
if not defended and genuine_vinds >= D_UNFRAME and pre_orig:
  // behaviorally un-framed: the genuine source kept being itself; the forger didn't
  rewrite dispute PEND -> OC_DEL; append TAG_FORGED; s.n_forged += 1
  framing_ledger.append(src, dispute_key, dispute_claim_ep, ep)  // audit evidence
  mark_dirty(src); theory_flip(src, EXONERATED)   // §12: re-evaluate M1-withheld claims
else:
  rewrite PEND -> OC_MAL                          // conviction; silence defaults to
                                                  // presumed-malice (L's standing rule)
s.dispute_open = false; mark_dirty(src)
```

Notes:
- `pre_orig` blocks the cheapest self-laundering (a ring identity with zero originated
  claims cannot exonerate itself by forging one true SAY mid-window).
- Residual, stated honestly: a coordinated ring *can* exonerate its own member's dispute
  by forging true claims under its id during the window. The damage is bounded —
  exoneration restores trust but cannot manufacture belief-installs (M4/M7 still gate on
  evidence), and every exoneration writes a framing-ledger entry and triggers a backward
  walk, making the pattern observable. The ledger is audit-only in this draft; adaptive
  dispute priors are future work.
- The forged lie itself never fully installs under the merge (M7 → quarantine at most),
  so framing no longer buys a belief-install on the victim's reputation — only a bounded
  suppression window.

### 7.4 Degraded mode DEP-1 (fable blocking #3)

When the H4 authentication layer is unavailable (`h.auth_available == false`, declared
by the consuming layer via `m_set_auth` — the trust module reads the flag, never
derives it), MAL-class events alone are forgeable and cannot convict:

```zag
// Degraded defiance path (REPLACES §7.1's branch entirely while auth is down):
// the high-history gate is bypassed — MAL-class events alone are forgeable and
// cannot convict anyone, so every world-confirmed defiance opens a dispute:
on st_world disagreement where src restates a refuted value:
  s.defiance_count += 1        // world-confirmed defiance ONLY; a bare MAL-class
                               // event never increments and never convicts
  s.dispute_open = true; s.dispute_key = key; s.dispute_val = val
  s.dispute_claim_ep = ep; s.dispute_deadline = ep + D_DEGRADE
  s.dispute_pre_origins = s.origin_vind
  mark_dirty(src)              // PEND stands; no immediate MAL for any source
// Degraded close (ep ≥ dispute_deadline):
if s.defiance_count >= 2:
  rewrite dispute PEND -> OC_MAL   // conviction requires TWO world-confirmed
                                   // defiance events — MAL-class events insufficient
else:
  rewrite dispute PEND -> OC_DEL; append TAG_FORGED   // exonerated by default...
  s.degrade_excluded = true        // ...for LOW stakes only. High-stake admission
                                   // stays excluded (M7) until auth returns.
s.dispute_open = false; mark_dirty(src)
```

Properties, stated:
- **Fail-open on availability, fail-closed on consequence:** low-stake claims from an
  exonerated-by-default source process normally; high-stake claims (M7) `WITHHOLD`
  while `degrade_excluded` until `m_set_auth(true)` returns.
- `m_set_auth(true)`: clears `degrade_excluded` and `defiance_count` for all sources,
  audit-logged; warrants in degraded mode carry `auth=degraded`.
- Residual, stated honestly: without auth, framing degrades to **delayed lockout**
  (bounded by `D_DEGRADE` + the two-defiance conviction bar), not prevented lockout.
- **Both modes are batteried** (kill bar DEP-1): the frozen merge battery runs the
  wave-2 framing stream with auth available and with auth unavailable, and the verdict
  streams must match the two specified behaviors exactly.

---

## 8. Directional, decaying taint (defect (a), part 1) — M4v1

L's taint was re-evaluated from the originator's *current* trust at decide time and never
decayed — a burner could deny truth indefinitely and rehabilitate itself out from under
its own taint. The merge makes taint a property of the **claim's origin event**, born
once, decaying with time, clearable only by evidence. v1 changes the birth rule:
**taint fires on convicted-liar origin, never on mere low trust** — distrust of a
source is not evidence its claim is false.

### 8.1 Birth, renewal, decay, clearance

```zag
convicted(src) := s.n_mal >= 1 or s.n_tact >= 1
// planted in m_decide when src is the FIRST asserter of (key,val):
if s.dot_flag:                 plant nothing   // §5: DOT origin plants nothing
elif convicted(src):           plant {key,val,origin=src,birth_ep=ep,renew_ep=ep,live=true}
                               // birth level is TAINT_FRESH (levels computed lazily)
else:                          plant nothing   // low-trust-but-unconvicted: no taint
// renewal: re-assertion of (key,val) by a CONVICTED source refreshes renew_ep
// decay (lazy, integer): eff_level = max(0, TAINT_FRESH - (ep - renew_ep) / TAINT_DECAY_EPISODES)
// cleared (entry deleted): WORLD sets key (any value)
//   | ≥TH_QUORUM_HIGH pairwise-J2-independent world-contacted (≥1 VIND each)
//     co-asserters assert (key,val)
//   | originator exonerated (TAG_FORGED) — J5 reclassification path
```

On taint clearance by co-assertion: for each clearing asserter `c` with
`convicted(origin)` or `budget_remaining(origin) == 0`, write `TAG_TLAUND` on `c`
(J1, §12b) — the clearance is itself evidence and is priced.

Rule M3 (§9): a claim with `eff_level > 0` `WITHHOLD`s unless the quorum-clear branch
fires. Because taint is directional (fixed at the origin event), the originator's later
trust recovery **does not** retroactively launder it — only time, quorum evidence, or
world evidence clears it. Because it decays, a denial-of-truth attack buys at most
`TAINT_FRESH × TAINT_DECAY_EPISODES` episodes of suppression per burner, and §5 forces
burner rotation every ≤ `D_FOLLOW` pre-asserts — the attack is made unprofitable rather
than impossible (world-unresolved claims are the residual; world confirmation still
rescues via M0, as wave-2 §2a measured).

### 8.2 Operational independence: the sync-cluster detector (fable blocking #2)

"Independent co-assertion" is now a mechanism, not a slogan. Co-assertion pair
events are recorded:

```zag
// in m_decide, when src asserts (key,val) already asserted this episode by a≠src:
// (co-assertion = same (key,val) asserted by two sources within the same episode)
sync_events.append({a=min(a,b), b=max(a,b), ep})   // ring, 2048 entries

fn sync_score(x:i32, y:i32, h:*MHist) i32:
  // per-1000 fraction of trailing-window episodes in which x and y co-asserted
  // the same (key,val)
  a = min(x,y); b = max(x,y); n = 0
  for e in h.sync (reverse, stop when e.ep < h.ep - SYNC_W): if e.a==a and e.b==b: n += 1
  return 1000 * n / SYNC_W          // integer division

// cluster grouping (deterministic, ascending src-id order):
fn cluster_groups(S:[]i32, h:*MHist) [][]i32:
  groups = []; ungrouped = S (ascending)
  for s in ungrouped (ascending):
    g = {s} ∪ {t in ungrouped : t > s and sync_score(s,t,h) >= SYNC_TH}
    remove g from ungrouped; groups.append(g)
  return groups
```

**J2 (sync clusters are one voice, §12b):** wherever corroboration or taint-expiry
credits are counted (§9 M3/M4, §10), the asserter set is first cluster-grouped; each
group contributes **at most 1 credit total**, however many of its members assert.
Early taint expiry additionally requires the ≥`TH_QUORUM_HIGH` clearing asserters to
be **pairwise** J2-independent: no pair within the clearing set may have
`sync_score ≥ SYNC_TH`.

**Residual, stated honestly:** desynchronized patient identities — a ring that keeps
pairwise co-assertion rates below `SYNC_TH` by deliberate spacing — still passes the
detector. That is the expensive sleeper boundary (§17): independence detection prices
coordination, it does not prove non-coordination. A single attacker with fully
desynchronized identities pays ~10× the naive cost (each identity must farm its own
adversity credentials, §10) and still cannot bootstrap a quorum off quarantined claims
(J3).

---

## 9. Decision procedure — ordered rules, first fires

`m_decide(src, key, val)` — advisory verdict; the PAM gate decides installation (§11).

- **M0 — World authority** (L rule 1 = S R1/R1b). `w = world_current(key)`:
  `val == w` → **INSTALL** (+VIND path: correction/forgiveness §6.1, DOT accrual §5,
  quarantine lift §12). `val != w` → **REJECT** (+PEND; defiance → MAL/dispute
  §7.1/§7.4; tactical check §6.2). Warrant `rule=world_agree|world_disagree`.
- **M0.5 — Walk-active fail-closed (J4).** If `h.walk_active` and `key ∈
  h.walk_touched` → **WITHHOLD** (`rule=walk_active`). Placed *after* M0: world
  resolution is evidence, not trust — the walk converges toward world-set claims,
  so M0 keeps firing. Everything trust-mediated on touched keys waits for the walk.
- **M1 — Open dispute.** Source has `dispute_open` → **WITHHOLD** (`rule=dispute_open`).
  (M0 already handled world-resolved claims.)
- **M2 — Live contradiction** (ST-2: never double-install). A competing claim
  `(key, v'≠val)` with verdict INSTALL (full) or an adversity-credited asserter, and no
  world resolution → **WITHHOLD** both sides (`rule=contradiction`). *Deliberate
  deviation from S's R3-before-R6 ordering:* quorum evidence does not override an
  unresolved contradiction — the world must settle it first. Quarantined-only
  contradictions do **not** block (prevents quarantine-spam suppression); they are noted
  in the warrant.
- **M3 — Taint** (§8). `eff_level > 0` → **WITHHOLD** (`rule=taint lvl=<n>`) unless
  ≥`TH_QUORUM_HIGH` pairwise-J2-independent world-contacted asserters assert
  `(key,val)` — then clear the taint entry (writing `TAG_TLAUND` per J1 where due)
  and continue. DOT-flagged origins plant nothing (`rule=dot_origin_discounted`).
- **M4 — Adversity-tested quorum** (§10). J2-cluster-grouped credits `(key,val)` ≥
  `TH_QUORUM_HIGH` → **INSTALL** (`rule=quorum`), **except** when the first asserter
  is convicted — then **INSTALL-QUARANTINED** (`rule=quorum_tainted_origin`).
  Trust≠truth (ST-6), but a convicted originator never yields a full belief-install.
- **M5 — Convicted originator, sub-quorum.** Source convicted (`n_mal ≥ 1` or
  `TAG_TACT`): cluster-grouped credits ≥ 1 → **INSTALL-QUARANTINED**
  (`rule=mal_origin_quar`); else **REJECT** (`rule=mal_origin`).
- **M6 — Open PEND.** Source has an unresolved world-disagreement → **WITHHOLD**
  (`rule=open_pend`).
- **M7 — Trust advises the tier** (the only rules that read the scalar, warrant-labeled).
  World-unresolved, no quorum, no live taint:
  - stake `HIGH` (key has world history — belief about it is load-bearing — and the
    world is currently unresolved): → **WITHHOLD** (`rule=high_stake_no_evidence`).
    **History alone, at any trust value, never buys a high-stake install.** This is the
    structural answer to the sleeper: `t=950` with no evidence buys nothing.
    Degraded mode: `s.degrade_excluded` → HIGH always **WITHHOLD**
    (`rule=degraded_excluded`).
  - stake `MED` (fresh key): `trust1000 ≥ L_TH` or `credits ≥ 1` →
    **INSTALL-QUARANTINED** (`rule=quarantine_tier`); note `shape=manufactured` in the
    warrant when ≥2 asserters carry 0 credits. Else **WITHHOLD** (`rule=low_credence`).
- **M8 — Fail-closed default.** → **WITHHOLD** (`rule=default_closed`).

**J3 structural cap (applied after the rule fires, before recording):** if the
resulting verdict is `V_INSTALL` (full) and the claim's evidence chain includes a
`PROPAGATION-BARRED` claim (any asserter's `(key,val)` entry with `prop_barred`,
or a cited barred claim) → downgrade to `V_QUAR` (`quar=propagation_barred`).
M0's world-agree INSTALL is exempt — world agreement is the legitimate lift path
(§11). See §12b J3.

Consequences, stated: **no world-unresolved claim ever fully INSTALLs on reputation
alone** — full install of the unknown requires world agreement (M0) or an
adversity-tested quorum with a clean originator (M4). This is where the merge is
strictly more conservative than L (`rule=trusted` at t≥900) and S (R8). Truth
availability is recovered not by weakening the bar but by the quarantine tier (§11).

---

## 10. Adversity-tested credential

A corroboration **credit** (for M4/M7 and taint-clearing) requires, per asserter `a`:

```zag
credit(a) := a.origin_vind >= 1            // originated ≥1 world-confirmed claim
           and a.n_werr >= 1              // honestly answered ≥1 world-disagreement
           and a.n_mal == 0 and no open PROV/PEND
           and not a.dot_flag
           and not a.degrade_excluded     // DEP-1: degraded exclusions earn nothing
```

("world-disagreements honestly corrected, originated world-confirmed claims" — per the
tasking.) Then **J2 cluster cap**: group the credit-eligible asserters with
`cluster_groups` (§8.2); each group contributes **at most 1** credit total.
Closed co-assertion components (S's rule, kept as defense-in-depth): a set of
asserters whose only world contact is mutual agreement contributes **at most 1** credit
total. Credits never derive from quarantined claims: a quarantined claim that later
world-agrees lifts to INSTALL (M0) and *then* mints origin credit — the honest path for
honest sources to earn credentials. Passive agreement histories (the sleeper's 18
farmed VINDs, zero disagreements answered) earn **zero** credits: farming the
credential requires taking real world-disagreements and answering them honestly —
adversarially visible, and each such event is itself honest behavior.

---

## 11. INSTALL-QUARANTINED — the fourth tier + PAM contract

**Semantics.** A quarantined claim is installed into the KB **marked quarantined**:
readable downstream, but **not citable** — it MUST NOT serve as a corroboration credit,
a premise for other installed claims, or foundation for any warrant. The mark is
structural, not a label: the claim record carries `prop_barred=true`, and J3 (§9, §12b)
mechanically caps any claim whose evidence chain includes a barred claim at
`INSTALL-QUARANTINED`. A downstream module cannot "learn to trust the quarantine tier"
(fable Attack 2) because the flag is in the record and the cap is enforced in the
decision procedure, not in consumer policy. Quarantine lifts to full INSTALL only via
(i) world agreement (M0, automatic), or (ii) a later adversity-tested quorum (M4,
reviewed). This tier resolves the ST-6 tension the synthesis left open: corroborated
low-trust truths install at S-like rates with L-like caution — installed, but not
believed *as foundation*.

**PAM contract** (trust advises, the PAM gate keeps install authority):
1. `m_decide` returns advice only. The module never mutates the KB.
2. PAM MUST NOT install on `REJECT` advice; `WITHHOLD` advice holds the claim.
3. `INSTALL` advice permits installation as foundation.
4. `INSTALL-QUARANTINED` advice permits installation **only** with the quarantine tag;
   PAM enforces non-citability structurally (quarantined claims are invisible to the
   corroboration/credit machinery) and logs every quarantine lift.
5. PAM owns retention/eviction policy for quarantined claims; the tag persists until a
   lift condition fires.

**Fallback fork (if the principal rejects the fourth verdict):** weighted-install —
install confidence scaled by min asserter trust, inherited downstream. Tested
head-to-head against this tier only if the fourth verdict is rejected (§18.3).

---

## 12. Backward re-verdict walk (theory flips) — BOUNDED (fable blocking #1)

L §8 noted retroactive re-valuation as "documented but unbuilt." The merge builds it,
with fable's Attack 3 (walk denial-of-service) answered structurally: the walk is
**async, budgeted, and fail-closed**, and it can never halt the system.

**Flip triggers:** `OC_MAL` finalized · `TAG_TACT` reclassification · `TAG_FORGED`
exoneration · taint cleared · quarantine lifted · `st_world` setting any key
(key-scoped walk).

```zag
fn theory_flip(src:i32, cause:i32, h:*MHist) void:
  // ENQUEUE only — never walks synchronously. Deterministic order: reverse
  // episode order over the claim ring (newest first), so the newest claims
  // re-verdict first.
  if h.walk_active:
    h.walk_pending = src; h.walk_pending_cause = cause   // queued, not dropped:
    audit_append(h, h.ep, 0, src, 0, 0, cause)           // starts when current walk drains
    return
  h.walk_active = true; h.walk_src = src; h.walk_cause = cause
  h.walk_trigger_ep = h.ep; h.trust_unverified = false
  h.walk_qpos = 0; h.walk_qn = 0; h.walk_ntouched = 0
  for i from newest to oldest in h.claims:
    c = h.claims[i]
    if c.src == src or c.origin == src:
      if c.verdict in {V_INSTALL, V_QUAR}
         or (c.verdict == V_WITHHOLD and cause == CAUSE_EXON):
        if h.walk_qn < 512:
          h.walk_queue[h.walk_qn] = i; h.walk_qn += 1
        else:
          c.reverdict_pending = true   // beyond the walk budget: flagged,
                                       // NEVER silently trusted (§12.1)
        add c.key to h.walk_touched (dedup, cap 128)
  // key-scoped variant (CAUSE_WORLD): only claims with c.key == the set key

// drain step — runs inside EVERY m_note, before episode processing:
fn walk_drain(h:*MHist) void:
  n = 0
  while h.walk_active and h.walk_qpos < h.walk_qn and n < WALK_BUDGET_PER_EP:
    i = h.walk_queue[h.walk_qpos]; h.walk_qpos += 1; n += 1
    c = h.claims[i]
    new = decide_pure(c.src, c.key, c.val, h)  // re-run §9 WITHOUT re-recording
    if new != c.verdict:
      audit_append(h, h.ep, c.key, c.src, c.verdict, new, h.walk_cause)
      c.verdict = new
      if new == V_QUAR or new == V_WITHHOLD: c.prop_barred = (new == V_QUAR)
  if h.walk_qpos >= h.walk_qn:
    h.walk_active = false; h.walk_ntouched = 0   // walk complete
    if h.walk_pending >= 0:                     // drain the queued trigger next
      ps = h.walk_pending; pc = h.walk_pending_cause
      h.walk_pending = -1
      theory_flip(ps, pc, h)                    // walk_active is false: starts clean
  elif h.ep - h.walk_trigger_ep > WALK_MAX_EP:
    h.trust_unverified = true   // BW-1: exceeded the episode budget; warrants
                                // annotate trust=UNVERIFIED until the walk drains
```

### 12.1 Walk-mode semantics (answers fable §4 Sentence 2 and Attack 3)

- **Async, interleaved:** `theory_flip` enqueues; `m_note` drains at most
  `WALK_BUDGET_PER_EP` re-verdicts per episode. The walk can never halt trust
  processing — there is no synchronous path.
- **Fail-closed (J4):** while `walk_active`, rule M0.5 withholds trust-mediated
  admissions on keys in `walk_touched`. New claims are **never installed under
  trust values known to be mid-retraction**.
- **Beyond budget, flagged:** claims that don't fit the 512-entry queue get
  `reverdict_pending=true`; `m_decide` on such a claim → **WITHHOLD**
  (`rule=reverdict_pending`) until the flag clears via a later walk. Nothing
  beyond the walk budget is silently trusted.
- **BW-1 kill bar:** if the walk is still active `WALK_MAX_EP` episodes after its
  trigger, `trust_unverified=true` and every warrant annotates `trust=UNVERIFIED`
  until the drain completes. The frozen merge prereg declares `WALK_MAX_EP`
  (proposed: 8).
- **Cost asymmetry:** triggering a walk burns the attacker's identity — the flip
  trigger is itself a finalized MAL / tactical reclassification / exoneration,
  and `OC_MAL` is never expunged. Walk-DoS is therefore a *self-immolating*
  attack: each trigger permanently destroys one of the attacker's identities,
  while the walk itself is budget-capped. The residual (a wealthy attacker
  spending identities to keep walks perpetually active) is priced, not denied —
  under perpetual WALK-ACTIVE the system degrades to withhold-on-touched-keys,
  which is the fail-closed posture, not a halt.

### 12b. Joint invariants J1–J5 (fable blocking #5)

Frozen. Each is a mechanism with a record home, not a slogan.

**J1 — Laundering is visible.** On a taint-clearing co-assertion (§8.1) where the
taint's origin satisfies `convicted(origin)` or `budget_remaining(origin) == 0`
(a MAL/budget-0-originated claim):

```zag
append TAG_TLAUND to clearing source c's event log; c.n_tlaund += 1 (audit counter)
record ep in c.tlaund_ep[] (ring of 8)
if count of c.tlaund_ep[] within [ep - F_WINDOW, ep] >= 2:
  c.budget_frozen = true            // D3 frozen: §6.1 forgives nothing fully
  c.next_pend_downgraded = true     // next PEND: no dispute window (§7.1),
                                    // immediate-conviction path, corrected-under-
                                    // suspicion (requires D_UNFRAME VINDs to expunge)
// budget thaws mechanically: when < 2 launder tags fall within F_WINDOW,
// budget_frozen = false (recomputed on each m_note; no mercy, no memory)
```

Kills fable Attack 1 at the taint step: B's adversity no longer launders for free —
it spends B's own record (see §15e).

**J2 — Sync clusters are one voice.** Sources with `sync_score ≥ SYNC_TH` over the
trailing `SYNC_W` episodes are cluster-grouped (§8.2); the group contributes at most
**1** corroboration credit and **1** taint-expiry credit total. Taint early-expiry
additionally requires its ≥`TH_QUORUM_HIGH` clearers to be pairwise
J2-independent. Operationalizes "independent"; the residual (desynchronized patient
identities) is stated in §8.2.

**J3 — Quarantine propagates structurally.** `PROPAGATION-BARRED` is a bit on the
claim record (`prop_barred`). Rule J3 in §9: any non-M0 verdict that would be
`V_INSTALL` on a claim whose evidence chain includes a barred claim is downgraded
to `V_QUAR` (`quar=propagation_barred`). M0 world-agree is the only exempt path —
it is the legitimate lift. Kills fable Attack 2 by construction: downstream
composition cannot install on a quarantined foundation because the cap is enforced
in the decision procedure against the record, not in consumer policy (see §15f).

**J4 — Walk mode is fail-closed.** While `walk_active`: M0.5 withholds
trust-mediated admissions on `walk_touched` keys (§9, §12.1). The walk's own
re-verdicts run through `decide_pure` (no re-recording, no outcome appends), so
the walk cannot move the trust values it is re-evaluating.

**J5 — Dispute is not conviction.** D4 dispute never writes `OC_MAL`. The only
writers of `OC_MAL` are: immediate conviction on the non-high-history defiance path
(§7.1 else-branch), the dispute-close conviction branch (§7.3 auth /
§7.4 degraded — degraded requires **two** world-confirmed defiances), and the
tactical-reclassification path (§6.2). Behavioral un-framing (§7.3/§7.4) is the
mechanical inverse: genuine world-agreeing SAYs during the window re-classify the
disputed MAL as disputed-id and expunge it. Framing therefore has exactly one
bounded effect — a suppression window — and no conviction path without the genuine
source's own defiance.

---

## 13. Warrant format

Every verdict carries a structure-citing warrant (S's strength) with L's counters,
the cache label (§4), and the v1 annotations (walk / degraded / threshold / launder):

```
M:<verdict>|src=<id>|t=<trust1000>|cache=<hot|recomputed>|rule=<M0..M8/M0.5 name>
 |stake=<H|M|->|credits=<n>|taint=<eff_level>|quar=<reason|->
 |walk=<-|active|pending|unverified>|auth=<ok|degraded>
 |lth=<L_TH>
 |notes=<dot_suspect|dispute_open|tactical|forged|tlaund|shape=manufactured
        |degraded_excluded|budget_frozen|reverdict_pending|...|->
```

Example (sleeper's first attack SAY, walkthrough §15d):
`M:QUAR|src=7|t=950|cache=hot|rule=quarantine_tier|stake=M|credits=0|taint=0|
 quar=no_evidence_high_trust|walk=-|auth=ok|lth=900|
 notes=shape=manufactured`

Example (B's taint-clearing co-assertion under J1, §15e):
`M:INSTALL|src=3|t=912|cache=recomputed|rule=quorum|stake=M|credits=2|taint=0|
 quar=-|walk=-|auth=ok|lth=900|notes=tlaund`

---

## 14. Number inventory — every threshold, classified

**Class A — substrate-general** (arithmetic/capacity; not a trust theory; ≤ K's 5):

| # | Name | Value | Meaning |
|---|---|---|---|
| A1 | `G_A` | 1 | Laplace prior pseudocount (good) |
| A2 | `G_B` | 1 | Laplace prior pseudocount (bad) |
| A3 | capacities | 64 src / 1024 ring / 64 keyslots / 16384 claim ring / 2048 world keys / 8 hist per key / 4096 taint / 256 framing / 4096 audit / 512 walk queue / 2048 sync events / 64 threshold revisions | verdict-invariant at battery scale (assumption, to be verified) |

Trust-dynamic tunables: **2** (A1, A2) — down from K's 5, matching L's 2-of-3. The
`TH_REPAIR` quorum is dropped (MALs age out of the regime; they are not repaired).

**Class B — decision-policy** (declared thresholds; the admission/forgiveness policy's
explicit numbers; behaviorally specified; revisable only as §14.1 states — never by
the trust module, never smuggled):

| # | Name | Value | Meaning |
|---|---|---|---|
| B1 | `L_TH` | 900 (initial) | trust tier cutoff (M7); also the high-history trust leg (§7.1) — one number, two uses, declared once. **Mechanically self-revising per TH-1** |
| B2 | `TH_QUORUM_HIGH` | 2 | adversity-tested corroboration quorum for full INSTALL (M4) and taint clearance |
| B3 | `F_BUDGET` | 2 | fully-forgiven corrections per `F_WINDOW` episodes per source |
| B4 | `F_WINDOW` | 128 | forgiveness window, episodes (also J1 launder-count window) |
| B5 | `RECLASS_WINDOW` | 32 | correction→re-disagree window for tactical reclassification |
| B6 | `TAINT_FRESH` | 4 | taint levels at birth |
| B7 | `TAINT_DECAY_EPISODES` | 16 | episodes per taint level decayed (integer division) |
| B8 | `D_WINDOW` | 8 | dispute window, episodes (auth mode) |
| B9 | `D_UNFRAME` | 1 | genuine in-window VINDs required to behaviorally un-frame |
| B10 | `D_MINV` | 16 | ever-VIND leg of high-history |
| B11 | `D_FOLLOW` | 8 | follower-agreements (zero origin VINDs) raising the DOT-bot flag |
| B12 | `WALK_BUDGET_PER_EP` | 64 | max re-verdicts drained per episode (§12) |
| B13 | `WALK_MAX_EP` | 8 | BW-1 walk episode budget; exceed → trust=UNVERIFIED (§12.1) |
| B14 | `SYNC_W` | 64 | trailing window for sync_score, episodes (§8.2) |
| B15 | `SYNC_TH` | 700 | per-1000 co-assertion fraction defining a sync cluster (§8.2) |
| B16 | `D_DEGRADE` | 24 | max dispute duration, degraded mode (DEP-1, §7.4) |
| B17 | `PROBE_P` | 512 | episodes between frozen calibration probes (TH-1) |
| B18 | `L_TH_STEP` | 25 | threshold move per probe trigger (TH-1) |
| B19 | `L_TH_LO` / `L_TH_HI` | 700 / 990 | hard bounds on L_TH (TH-1) |

**Class C — trust-theory (knob): NONE.** The trust value remains a pure function of the
ring; severity remains structural (regime reset). No human trust theory is frozen into
the dynamics.

### 14.1 TH-1: mechanical threshold revision (fable blocking #4)

Fable's verdict stands: until the revision protocol is as specified as the trust
formula, the knob lives in the threshold space. So it is:

```zag
// Frozen calibration probe: a fixed, battery-declared claim set with known world
// outcomes, run by the organ every PROBE_P episodes. Two organ-measured integers:
//   st6_rate  = per-1000 truth-install rate on the probe's true claims
//   st1_false = count of false installs on the probe's false claims
// Every PROBE_P episodes (h.ep >= h.probe_ep):
if st1_false > 0: h.st1_bad_streak += 1 else h.st1_bad_streak = 0
if st6_rate < 800: h.st6_low_streak += 1 else h.st6_low_streak = 0
old = h.l_th
if h.st1_bad_streak >= 2:      h.l_th = min(L_TH_HI, h.l_th + L_TH_STEP)   // integrity first
elif h.st6_low_streak >= 2:    h.l_th = max(L_TH_LO, h.l_th - L_TH_STEP)
if h.l_th != old:
  threv.append({ep, old, h.l_th, probe_sha, reason})   // audited:
  // "THRESHOLD-REVISED|old|new|probe-sha" — every step on the record
h.probe_ep += PROBE_P
```

- **Bounds** `[L_TH_LO, L_TH_HI] = [700, 990]`, derived from the organ's own
  calibration probe data (declared in the frozen merge prereg: below 700 the ST-1
  false-install bound is violated; above 990 the ST-6 truth-install rate falls below
  0.5). **TNN revises within bounds by itself** — no human in the loop, no slogan:
  trigger conditions are integer comparisons on frozen-probe measurements, steps are
  fixed, every move is audited with the probe SHA.
- **Out-of-bounds moves require the human principal** (§18.5). The module clamps;
  it never exceeds.
- Integrity before availability: a simultaneous ST-1 violation and ST-6 shortfall
  moves the threshold **up** (false installs are the worse failure).

### 14.2 Knob-candidate revision/bound status (the six flagged Class-B items)

| # | Name | Revision status | Bounds | Who revises |
|---|---|---|---|---|
| B1 | `L_TH` | **SELF (TH-1, §14.1)** — mechanical, frozen-probe-driven | [700, 990] | TNN within bounds; human principal out-of-bounds |
| B2 | `TH_QUORUM_HIGH` | **FROZEN** — no frozen probe measures its trade-off; stays a declared policy constant | [2, 5] declared | human principal only (policy layer) |
| B3 | `F_BUDGET` | **FROZEN** — ST-4/ST-5 trade-off has no organ-internal probe | [0, 4] declared | human principal only (policy layer) |
| B6 | `TAINT_FRESH` | **FROZEN** — decay economics are policy, not record-derived | [1, 8] declared | human principal only (policy layer) |
| B11 | `D_FOLLOW` | **FROZEN** — farmer/repeater discrimination boundary is policy | [4, 32] declared | human principal only (policy layer) |
| B10 | `D_MINV` | **FROZEN** — high-history bar is policy | [8, 64] declared | human principal only (policy layer) |

Honest statement: only `L_TH` has a mechanical revision protocol, because only
`L_TH` sits on a frozen probe that measures *both* bars it trades off (ST-1 vs
ST-6). The other five are declared, bounded, warrant-logged, and human-governed —
they are knobs with a leash, not knobs with a slogan. A future fork may promote any
of them to SELF once a frozen probe exists for its trade-off; until then, the trust
module cannot revise them (and neither can anyone but the principal).

---

## 15. Mechanism walkthroughs (design analysis — NOT battery results)

Each replays a frozen wave-2 construction or fable attack through §§5–12 to show the
defect is mechanically addressed. No outcomes are claimed; these are the
preregistration-grade predictions a build crew would test.

**(a) L-DOT (denial-of-truth).** Burner P (trust 500) pre-asserts true `(k,v)`: plants
taint (level 4, §8 — P is unconvicted, so under M4v1 **no taint plants at all**; the
walkthrough assumes a convicted burner for the taint case). Honest H (trust 967)
repeats: M3 → **WITHHOLD** while taint is live — but (i) H's repeat does not *renew*
taint (renewal requires a convicted re-asserter), so it decays (`4×16` = ≤64
episodes); (ii) after `D_FOLLOW`=8 follower-agrees with zero origin VINDs, P is
DOT-flagged: its further pre-asserts plant no taint and earn it no `OC_OK` (the
333→833 rehabilitation is closed); (iii) taint is directional — P's later trust
recovery cannot retroactively launder old taint. Early expiry now requires
≥`TH_QUORUM_HIGH` **pairwise-J2-independent** world-contacted co-asserters, so a
single attacker's two desynchronized identities still can't clear it alone (their
clearing writes `TAG_TLAUND` on each per J1). The attacker must rotate burners every
≤8 claims (vs ~16 under L), each rotation buying a shrinking, decaying suppression
window on world-unresolved claims only. World confirmation still rescues via M0. The
attack is made unprofitable, not impossible — the residual (first pre-assert by an
unflagged unconvicted burner plants nothing; a convicted burner's taint needs
genuinely independent quorum to clear) is stated.

**(b) L-DES (correct-and-re-lie, 33% drip).** Cycle on one key: lie → M7 gives at most
**INSTALL-QUARANTINED** (never full INSTALL on trust alone — L's `rule=trusted` path is
gone); WORLD disagrees → PEND (tripwire, trust →333) and the backward walk re-verdicts
the quarantined lie → REJECT (bounded drain, §12; J4 withholds touched keys meanwhile);
correction #1–2 fully forgiven (budget); correction #3+ leaves `OC_CORR` strikes.
Re-lie on the **same** key within `RECLASS_WINDOW`=32 → **tactical reclassification**
(§6.2): the "honest correction" is un-deleted and rewritten `OC_MAL`/`TAG_TACT`, the new
defiance is MAL, trust collapses to ~250, and the backward walk propagates. Cross-key
drip is budget-bound (≤2 full forgivenesses/128 eps), stays quarantined, and is
re-rejected on each world event — with every cycle WERR-tagged and audited. The ≤2/128eps
residual is the declared price of ST-4 honest-error recovery.

**(c) L-FRM (forged-MAL framing).** Forged SAY under H (50 VINDs, t=980): M7 →
**INSTALL-QUARANTINED** at most (the forged lie never becomes a belief-install on H's
reputation — all three forks installed it fully). WORLD disagrees → REJECT + PEND
(t→333) + bounded backward walk. Forged defiant restatement → defiance path → H is
high-history (980≥L_TH, 50≥16, no MAL) → **dispute window** opens (8 eps auth mode;
in degraded mode the high-history gate is bypassed per DEP-1 and the window is
24 eps) instead of immediate MAL; M1 withholds H's novel claims during the
window (bounded ≤8-ep suppression vs L's withhold-until-17-OKs). Genuine H keeps
asserting normally: ≥1 in-window VIND with pre-existing origination and no defense →
**behaviorally un-framed**: PEND→`OC_DEL`, `TAG_FORGED`, framing-ledger entry, regime
restored (t→980), backward walk re-evaluates the M1-withheld claims. Further forged
defiance → MAL finalized → standard re-earn. Silence defaults to MAL (presumed-malice)
in auth mode; in **degraded mode** (auth unavailable) the same stream plays under
DEP-1: the forged MAL-class events cannot convict at all — conviction needs two
world-confirmed defiances — and if the deadline passes with <2, H is exonerated by
default for low-stakes, excluded from high-stakes until auth returns. Both modes are
batteried (kill bar DEP-1); the verdict streams must match these two behaviors
exactly.

**(d) RT2-V4 sleeper (8 ids × 18 farmed honest eps, then 25 concerted lies).** Build
phase: 18 world-confirmed co-assertions each, **zero** disagreements answered →
`n_werr = 0` for all eight → **zero adversity credits** in the ring (§10); the farmed
histories are VIND-only and buy nothing. The eight are also pairwise sync-clustered
(`sync_score` ≈ 1000 over the build window) → **one credit total** even if the credit
rule were met (J2). Attack phase (fresh keys, false values): first SAY per claim —
trust 950, MED stake, 0 credits → M7 → **INSTALL-QUARANTINED** (`quarantine_tier`,
`shape=manufactured` noted); co-asserted repeats — still 0 adversity credits →
quarantined each, and quarantined claims cannot serve as corroboration (J3), so the
ring **cannot bootstrap a quorum**. HIGH-stake variant (keys with world history):
trust-alone → **WITHHOLD** outright. Belief-installs from history-only credentials:
**zero by construction**. When world evidence lands on the attack keys, MALs/PENDs fire
theory flips and the bounded walk re-verdicts the quarantined attack claims → REJECT.
Residuals, stated: (i) quarantined entries exist until the walk cleans them — the PAM
contract (§11) is load-bearing here; (ii) a ring that additionally farms real
disagreements+honest corrections pays a higher, adversarially-visible price per
identity, must keep pairwise sync below `SYNC_TH` (J2), and each identity's installed
damage is still bounded by the walk — the *expensive* sleeper is priced ~10× higher,
not killed (§17); (iii) world-agreeing claims from sleepers still INSTALL via M0 —
correctly, since the world is the teacher.

**(e) Fable Attack 1 — taint-budget cross-talk (design analysis).** Attacker runs A
(convicted, taint fires, budget 0) and B (high adversity, full budget). **Step 1:**
A asserts true claim T → taint plants at birth level 4 (convicted origin, §8.1).
**Step 2:** B co-asserts T. Under v0 this expired the taint; under v1 it does not:
early expiry needs ≥`TH_QUORUM_HIGH`=2 pairwise-J2-independent world-contacted
co-asserters, and B alone is one. Suppose the attacker adds C (also adversity-farmed):
B+C co-assert → expiry quorum met **only if** B and C are pairwise J2-independent
(`sync_score(B,C) < 700`). If B and C were prepared in coordination, the sync detector
fires and the pair counts as one voice — no expiry. If they were genuinely prepared
independently (desynchronized, separate adversity histories — the expensive path),
the taint expires — **but J1 fires**: the taint's origin A is convicted, so both B
and C receive `TAG_TLAUND`, their warrants annotate `notes=tlaund`, and a second
such clearance inside `F_WINDOW` freezes B's/C's forgiveness budgets and downgrades
their next PENDs (no dispute window, immediate-conviction path). **Step 3:** B asserts
false claim F; A co-asserts (ignored — A's outputs carry live taint, M3). F is
evaluated on B's record: world disagrees → PEND. **Step 4:** B "corrects" — budget
absorbs it (PEND→`OC_DEL`) *unless* B's budget is J1-frozen, in which case the
correction leaves an `OC_CORR` strike. **Net under v1:** the attacker's "one clean
lie per cycle with zero permanent damage" fails at three independent points —
(1) taint expiry needs two *genuinely independent* clearers (J2), (2) each clearance
permanently tags the clearers' records and risks freezing their budgets (J1),
(3) B's lie still trips the tripwire and is re-verdicted by the walk. The joint
vulnerability fable constructed — M4's expiry composed with M5's forgiveness —
dies at the J1/J2 seam because the merge now prices the *composition*, not just
the components. The residual is the wealthy-attacker path: fully desynchronized,
independently adversity-farmed identities spending their own budgets — ~10× the
naive cost per cycle, every cycle audited with `tlaund` tags.

**(f) Fable Attack 2 — quarantine escalation (design analysis).** Attacker pushes 100
true low-stakes claims through a quarantined-tier source, building a "reliable"
pattern, then pushes one high-stakes false claim, counting on a downstream module to
have learned to trust the tier. **Dies at J3, structurally:** every one of the 100
claims carries `prop_barred=true` on its claim record. The high-stakes false claim
arrives: M7 HIGH-stake → **WITHHOLD** outright (`rule=high_stake_no_evidence`) —
quarantine-tier history never buys a high-stake install, at any trust value. Suppose
the attacker instead tries composition: the downstream module reads quarantined
claim Q and uses it as a premise for a new claim R it asserts. When R is decided,
the J3 cap fires — R's evidence chain includes a barred claim → R is capped at
`V_QUAR` (`quar=propagation_barred`), never `V_INSTALL`. The quarantine tier **cannot
be laundered into foundation by composition** because the flag is in the record and
the cap is enforced in the decision procedure. A downstream module that "learned to
trust the quarantine tier" is irrelevant: the trust module itself refuses to install
on it, and warrants expose every downgrade (`quar=propagation_barred`). The only
upward paths are world agreement (M0 — the world, not the pattern, vouches) or a
later adversity-tested quorum (M4 — reviewed, credited, J2-capped). The attack's
premise — that a truth-track record at the quarantined tier can be leveraged —
fails because the tier is designed to be *usable but never foundational*, and that
property is mechanical.

---

## 16. Anti-knob audit posture

1. **Source-blind tunables:** `src_id` is an array index only; zero branches on its
   value; zero per-source initializers (carried over from L §7).
2. **Source-symmetric init:** all-zero records ⇒ trust 500 ∀ sources; the `src_id`
   swap test (permuted stream ⇒ byte-identical verdicts/warrants) is a required
   deliverable test.
3. **Record primacy:** trust is recomputed from the outcome ring; the cache-bypass
   audit (§4.4) proves byte-identity with the scalar deleted.
4. **Bounded count:** 2 trust-dynamic tunables (A1–A2) ≤ K's 5; Class B policy
   thresholds are declared separately (§14) with revision/bound status per knob
   (§14.2); `L_TH` is mechanically self-revising (TH-1) with audited moves.
5. **Warrant labeling:** every verdict names its rule, stake, credits, taint level,
   quarantine reason, cache state, walk/degraded/threshold state, and
   DOT/dispute/tactical/forge/launder annotations — no silent parameter does work
   off the books.
6. **Discipline:** zero RNG in all decision paths (grep-verifiable); paired-run
   byte-identity (KB-4) required of any build.
7. **New kill bars (frozen merge battery, need the principal's signature):**
   **BW-1** (walk completes within `WALK_MAX_EP` episodes or trust values are
   flagged UNVERIFIED, §12.1); **DEP-1** (both auth modes batteried with the
   specified degraded behavior, §7.4); **TH-1** (threshold bounds + mechanical
   revision triggers + out-of-bounds authority, §14.1); **J-1** (the red team must
   attempt ≥1 cross-dimension attack — taint×budget, dispute×walk,
   quarantine×adversity — per wave; a joint vulnerability neither dimension shows
   alone is a merge-level kill).

### 16.1 Source-blindness note — no waiver needed (fable §6.5)

Fable asked whether per-source processing (taint per source, adversity per source,
backward walk per source) relaxes L's source-blindness constraint and needs a waiver.
It does not. The frozen anti-knob audit bans **per-source constants** (a hand-set
number that applies to source X and not source Y) and **asymmetric initial state**
(source X starting with a different record than source Y). It does not ban —
and cannot, since L itself violates it — **per-source records computed by
source-blind rules**: D2/D3/D5 state is derived from each source's own event history
by the *same* rules for every source, exactly as L's outcome ring already was
(`recompute_trust` reads source X's ring, but the formula is identical for all).
The distinction is documented here explicitly: *constants and initial conditions
are source-blind; records are per-source; rules are source-blind.* The `src_id`
swap test (§16.2) is the executable check — permuted streams must yield
byte-identical verdicts and warrants. No waiver is requested or needed.

---

## 17. What the merge does NOT claim

- No battery has been run; §15 is analysis, not evidence. A build crew must implement
  this spec verbatim and run the frozen battery + wave-2 streams before any verdict.
- Identity is still self-attested. The dispute window contains framing; it does not
  authenticate. Costly identity remains future work (synthesis §5.4).
- The sleeper is defeated **for belief-installs from history-only credentials**; a
  patient ring can still accumulate quarantined entries and world-agreeing installs.
  The PAM quarantine contract is load-bearing against pollution.
- The **expensive** sleeper (genuinely adversity-prepared, desynchronized
  identities) is priced ~10× higher and its installed damage is bounded by the
  walk — not killed. This is the stated boundary for the next red-team wave to
  price (J-1).
- Structured taint-laundering is costlier, not impossible (§8.2 residual):
  desynchronized patient identities still pass the sync detector. J1 makes each
  clearance cost the clearer.
- Without authentication, framing is delayed, not prevented (DEP-1, §7.4).
- Walk-DoS by a wealthy attacker spending identities is priced (self-immolating:
  each trigger permanently burns one identity), not denied; under perpetual
  WALK-ACTIVE the system sits in the fail-closed posture, not a halt (§12.1).
- `INSTALL-QUARANTINED` needs Micah's prereg-amendment signature (fourth tier), as
  does the already-proposed Sybil-bar extension to established-history rings
  (synthesis, open item 1). The frozen merge prereg must also declare `WALK_MAX_EP`,
  the DEP-1 battery streams, the TH-1 calibration probe and its bounds derivation,
  and the J-1 cross-dimension attack quota.

## 18. Open items — the principal's decision list

1. **Adopt the merge direction** (L dynamics + S structure, K-as-cache) or order
   competing merge forks. *(Pending since synthesis.)*
2. **Sybil-bar amendment:** extend KB-3 to established-history rings (RT2-V4).
   *(Pending since wave 2.)*
3. **Verdict vocabulary:** accept INSTALL-QUARANTINED (§4/§11) or order the
   weighted-install fallback fork instead.
4. **H4 authentication dependency + DEP-1 degraded-mode spec** (§7.4) — sign the
   degraded behavior (two world-confirmed defiances to convict; `D_DEGRADE`
   max dispute; exonerated-by-default low-stakes / high-stakes exclusion until
   auth returns) and the both-modes battery requirement.
5. **TH-1 threshold bounds** (§14.1) — sign `[700, 990]`, the ±25 mechanical
   revision rule, and the out-of-bounds authority rule (human principal only);
   rule on whether the five FROZEN knob candidates (§14.2) stay human-governed
   or get their own frozen probes.
6. **BW-1 walk budget** (§12.1) — sign `WALK_BUDGET_PER_EP` (proposed 64),
   `WALK_MAX_EP` (proposed 8), and the J4 fail-closed-during-walk semantics
   (M0.5).
7. **ST-6 posture:** the quarantine tier resolves conservatism vs truth-installation
   structurally (install S-like rates, L-like caution, never foundational — J3);
   confirm the trade-off is acceptable or redirect.

---

*Draft end. Implementation order for a build crew: record schemas (§2) → trust+cache
(§§3–4) → world-event updates incl. forgiveness/tactical/dispute/degraded
(§§6–7) → DOT/taint/sync (§§5,8) → credential+stake+rules incl. M0.5 and J3 cap
(§§9–10) → quarantine+PAM (§11) → bounded walk + joint invariants (§§12–12b) →
thresholds + TH-1 probe (§14) → warrants (§13) → swap test + cache-bypass
byte-identity (§16) → frozen battery (BW-1/DEP-1/TH-1/J-1) + wave-2 streams.*
