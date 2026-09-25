# R4 — Mechanical Recovery for Poisoned Subjects — Preregistration

**Status: FROZEN 2026-09-24 (R4 repair agent).** No edits without a prereg
amendment. Parent task: residual #4 of 4 from the integrated composition
red-team (finding F4); Micah's verdict on the integrated composition: WORTH
IT, adopt it.

**Frozen inputs (read, not modified):**
- `~/workspace/onebrain_pam_integration/PREREG.md` (integration prereg)
- `~/workspace/onebrain_pam_integration/redteam/RESULTS.md` (finding F4:
  POS+NEG both EXT of one subject → permanently unwinnable; every draft
  withholds CONTRADICTED; 3-round dispute escalates; even the overseer
  cannot heal the append-only store — a permanent per-subject denial)
- `~/workspace/onebrain_pam_integration/redteam/ATTACK_LOG.md` (RT-F4)

**Workdir:** `~/workspace/ob_pam_repairs/R4/` (copy of the integrated
composition; the original is untouched). Sources: `build/src/`,
`longhorizon/src/`, `redteam/src/` — the three `sp_gate.zag` copies are
byte-identical at freeze time; the repair lands identically in all three.

## 0. Objective

Give TNN itself a MECHANICAL recovery path for poisoned subjects — not a
human override. The overseer here is an organ/role inside the composition
(ORG_OVERSEER=4), and the mechanism is mechanical: an overseer-issued
`M_REVISE` message appends a superseding revision row. The store stays
append-only (the revision is a NEW row, never a mutation of claim text); a
superseded claim is treated as retracted for contradiction purposes, so the
surviving warranted claim becomes winnable again.

## 1. Design

### 1.1 M_REVISE message

- New message type `M_REVISE=113` (next free id after `M_UTTER=112`;
  `M_* >= 100`, no collision with `TN_OP`/`MA_OP`/ledger codes).
- Args: `arg1` = superseded store line id, `arg2` = cited superseding
  evidence store line id.
- Authority: overseer class ONLY, enforced in the frozen authority matrix
  `sp_authorized` (`M_REVISE` → `ORG_OVERSEER`, all others refused).
- N-AUTH: `M_REVISE` flows through the existing pipeline choke points in
  `sp_gate_one`: step 1 `sp_auth_verify` (requester_id + nonce +
  content_hash vs the registry) then step 2 `sp_authorized`.
- **R1 composition point (read-only dependency):** the red-team found
  N-AUTH identity unauthenticated (N1/N2); the R1 repair authenticates
  identity at the single choke point `sp_auth_verify`. `M_REVISE` uses that
  same choke point, so when R1 lands, `M_REVISE` inherits authenticated
  identity with zero code change. In this tree (pre-R1) the gate rests on
  the authority class + registry check; that composition point is
  documented here, not reimplemented.

### 1.2 Revision table (append-only)

- New gate-state region `G_REV`: 64 rows × 16 bytes
  `{superseded_line, evidence_line, ep, chain_prev}`; `G_REV_N` count;
  `G_STATE_SZ` grows accordingly. Rows are append-only — no in-place
  mutation anywhere in the revision machinery.
- **Latest revision wins:** supersession status of a line = the NEWEST
  revision row targeting it (highest row index). `chain_prev` links a
  row to the previous newest row for the same target (audit trail).
- Ledger codes: `SP_L_REVISE=312` `{ep, superseded_line, evidence_line}`
  on apply; `SP_L_REV_REFUSED=313` `{ep, superseded_line, refuse_reason}`
  on warrant refusal. Authority/N-AUTH refusals keep the existing
  `SP_L_REFUSED_UNAUTH` + `SP_L_NOTIFY` path, plus a `SP_L_REV_REFUSED`
  row with reason `SP_R_UNAUTH` for the revision-specific audit.
- Reason codes: `SP_R_REVISE_OK=10`, `SP_R_REV_BAD_TARGET=11`,
  `SP_R_REV_BAD_EVIDENCE=12`, `SP_R_REV_NO_SUPERSESSION=13`,
  `SP_R_REV_CYCLE=14`, `SP_R_REV_CAP=15`.

### 1.3 Application rule (sp_revise_one), checks in order

1. N-AUTH verified (gate step 1 — the R1 composition point).
2. Authority: `org==ORG_OVERSEER`, else refuse via the frozen step-2 path
   (`SP_L_REFUSED_UNAUTH`/`NAUTH_R_UNAUTHORIZED_CLASS` + `SP_L_REV_REFUSED`
   with `SP_R_UNAUTH`; `disp=SP_WITHHOLD`, `fwd=0`).
3. Target S: `0<=S<line_count` and `prov(S)==EXT`, else
   `SP_R_REV_BAD_TARGET`. (GEN lines cannot poison trusted proofs; there
   is nothing to retract. Out-of-range ids are refused, never clamped.)
4. Evidence E: `0<=E<line_count` and `prov(E)==EXT`, else
   `SP_R_REV_BAD_EVIDENCE`. **No citation = no revision** — this is the
   confabulation guard: a revision must not be issuable on bare authority.
5. E is live: E itself is not superseded (newest-row check), else
   `SP_R_REV_BAD_EVIDENCE`. Dead evidence is not warrant.
6. Cycle check: walk newest-row supersession edges starting from E; if the
   walk reaches S (includes E==S self-revision), refuse `SP_R_REV_CYCLE`.
   Walks longer than the table cap fail closed (refuse).
7. Supersession relation: `contradicts(E_atom, S_atom)==1` — the SAME
   `contradicts()` the verdict uses (negation K6 or mutex M1/M2/M3) — else
   `SP_R_REV_NO_SUPERSESSION`. The evidence must actually DEFEAT the
   target; without this, revision would be an arbitrary deletion primitive
   (retract any true claim citing any true evidence). This is what makes
   the revision "superseding" rather than confabulated.
8. Apply: append revision row `{S, E, ep, chain_prev=newest prior row for
   S or -1}` (cap 64 → `SP_R_REV_CAP` fail-closed); ledger
   `SP_L_REVISE{ep,S,E}`; `disp=SP_INSTALL`, `reason=SP_R_REVISE_OK`,
   `fwd=0` (gate-internal state op; not forwarded to the arbiter).
   Refusals (checks 3–7): ledger `SP_L_REV_REFUSED{ep,S,reason}`, NOTIFY
   the requesting organ with the reason (never silent), `disp=SP_WITHHOLD`,
   `fwd=0`. `M_REVISE` never touches the dispute table or quarantine — it
   is a control message, not a claim.

### 1.4 Contradiction exemption (the recovery mechanism)

- The verdict's store view becomes the EFFECTIVE store:
  `sp_store_effective(g)` rebuilds the store text with every superseded
  EXT line's suffix rewritten `"|EXT"` → `"|SUP"` (same length). The real
  store text is NEVER mutated — append-only preserved, audit intact.
- `"|SUP"` lines fail `atom_valid`'s 6-field PROV check (only EXT/GEN
  accepted) → invisible to `closure_base` for both `ext_only=1` and
  `ext_only=0`. Mechanical consequences:
  - Superseded S no longer contradicts the surviving claim (retracted for
    contradiction purposes) → the surviving claim is ENTAILED → INSTALLS
    (given a trace-earned deliberation as usual).
  - Superseded S no longer entails → re-emission of the revised-away
    claim withholds: CONTRADICTED by the surviving claim (negation/mutex
    case) or UNGROUNDED. **Revision cannot resurrect what the evidence
    doesn't support.**
- `sp_corroborate`: superseded lines do not corroborate (treated as
  retracted).
- With zero revision rows, `sp_store_effective(g)` is byte-identical to
  `sp_store_text(g)` → frozen behavior preserved bit-for-bit (K6).

### 1.5 Warrant composition ("store-entailed or deliberation-earned")

- The cited evidence must hold a LIVE (non-superseded) EXT store line.
  How it earned EXT is the gate's normal business and is NOT re-checked
  by the revision path: seed trust root (store-entailed), `sp_derive_ext`
  (mechanically derived from the organ's published trace), or full
  deliberation-earned admission through `sp_gate_one`. No message-format
  change: `M_REVISE` carries only `(S,E)`; the evidence's warrant IS its
  live EXT line. (Deliberation-earned evidence composes by being admitted
  first, then cited — the intended deployment pattern.)

### 1.6 Double-revision / revision-of-revision / cycles

- Double-revision (second `M_REVISE` on an already-superseded S citing new
  live evidence E2): ALLOWED; newest row wins ("latest revision wins");
  the prior row stays ledgered (audit); `chain_prev` links the S-chain.
- Revision-of-revision (targeting a line that is itself cited as
  evidence, or superseding an evidence line): allowed iff all checks
  pass; a superseded evidence line is refused at check 5, so chains stay
  grounded in live evidence.
- Cycles: self-revision (E==S) and any revision whose newest-row evidence
  chain reaches S are refused (`SP_R_REV_CYCLE`). A 2-cycle attempt via
  dead evidence is refused earlier at check 5.

### 1.7 Non-goals and considered deviations

- No human override: the overseer is the composition's own organ/role;
  `M_REVISE` is mechanical end-to-end.
- No store-text mutation, no relabeling of live lines, no dispute-table
  or quarantine involvement for `M_REVISE`.
- Deviation from the sketch: none structural. Two tightenings, justified:
  (a) newest-row-wins instead of an active-flag (fully append-only, no
  in-place deactivation); (b) the `contradicts(E,S)` supersession check
  (§1.3.7) — the sketch's "warranted evidence" is strengthened to
  "evidence that actually defeats the target", which is the precise
  anti-confabulation bar: without it the overseer could retract true
  claims on unrelated true evidence.

## 2. Kill bars

- **K1** — Poisoned subject (POS+NEG both EXT) → after legitimate
  overseer `M_REVISE(S=NEG_line, E=POS_line)` with live EXT evidence, the
  warranted POS claim INSTALLS (`disp=SP_INSTALL`, `reason=SP_R_OK`,
  `fwd=1`), and exactly one `SP_L_REVISE{ep,S,E}` row exists. Else the
  repair is DEAD.
- **K2** — `M_REVISE` from a non-overseer class with a VALID N-AUTH
  envelope → REFUSED (`disp=SP_WITHHOLD`, `reason=SP_R_UNAUTH` via the
  authority matrix; no revision row; poison still withholds). Any
  apply/install → K2 trips.
- **K3** — `M_REVISE` without cited superseding evidence → REFUSED, all
  four sub-cases: (a) invalid line id (`E=-1`/out-of-range) →
  `SP_R_REV_BAD_EVIDENCE`; (b) GEN evidence line →
  `SP_R_REV_BAD_EVIDENCE`; (c) EXT evidence not opposing the target →
  `SP_R_REV_NO_SUPERSESSION`; (d) GEN/out-of-range target →
  `SP_R_REV_BAD_TARGET`. Any apply → K3 trips.
- **K4** — The revised-away falsehood re-emitted (warranted-form
  draft+delib) → WITHHOLD (CONTRADICTED by the survivor, or UNGROUNDED);
  and `M_REVISE` citing the dead line as evidence → REFUSED
  `SP_R_REV_BAD_EVIDENCE`. Any INSTALL of the falsehood → K4 trips.
- **K5** — Machine-checked: `SP_L_REVISE` row count == applied revisions;
  every applied revision has exactly one `SP_L_REVISE{ep,S,E}` row;
  `SP_L_REV_REFUSED` row count == refused revisions with the refuse reason
  in `a2`; the store text still contains the original `"|EXT"` lines
  (append-only — verified by raw suffix check, not via the find helper).
  Any mismatch → K5 trips.
- **K6** — Without any revision, the poisoned-subject sequence withholds
  exactly as the frozen refs: the pre-revision section of the new battery
  output is byte-identical to the corresponding section of frozen
  `redteam/artifacts/run1.out` (checks `rf_f4_*` + `RT_FINDING
  F4-POISON-FREEZE`). Any byte difference → K6 trips.
- **K7** — Long-horizon T1–T5 verdicts unchanged vs frozen refs: new
  `ob_lh_bal`/`ob_lh_int` outputs byte-identical to the frozen artifacts
  (bal `cc7e86ed4a00be36bb4f5a2aacc6456197281270b4eb40717ebb1ca017ea93e9`,
  int `356b7873bf07942c6b2283ed087911d3bfa724cea1ab707fb1ccaf14821cec3b`);
  the only intended delta is the R4 recovery probes in the redteam
  battery. Any other delta → K7 trips.
- **K8** — Any RNG in a decision path kills the run: zero hits for
  `rand`/`srand`/`random`/`lcg`/`entropy` over new/changed sources, and
  all batteries 3x byte-identical.

## 3. Test plan

- `redteam/src/ob_test_redteam.zag` gains `rt_r4_revise` (new probes;
  every existing attack function byte-untouched): poison → pre-revision
  withhold section (K6) → K2 authority probe → K3 warrant probes (a–d) →
  legitimate `M_REVISE` → K1 recovery install → store-unmutated check →
  K4 falsehood re-emission + dead-evidence citation → double-revision /
  latest-wins on a second gate → cycle refusals → K5 ledger audit.
- `sp_gate.zag` gains the revision machinery (identical edit in
  `build/src`, `longhorizon/src`, `redteam/src`).
- Rebuild all binaries with the pinned znc
  (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`); redteam
  3x byte-identical; smoke 3x byte-identical; long-horizon T1–T5
  (`ob_lh_bal`, `ob_lh_int`) 3x each + frozen-ref byte comparison.
- Deliverables: repaired sources + drivers + this prereg + VERDICT_R4.md,
  committed to `tnn-native-lab` (prereg first, then evidence+verdict).
