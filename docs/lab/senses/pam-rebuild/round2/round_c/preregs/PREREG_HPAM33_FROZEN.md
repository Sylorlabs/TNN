# PREREG FROZEN — H-PAM-33 (endorsed-channel admission + WG bar)

**Status:** FROZEN BEFORE BUILD. **Amends:** `preregs/PREREG_HPAM33.md` (DRAFT,
committed Round-C; branch blob `3f6f2b42d494`) — pins the mechanism, exact
formulas, constants, fixture counts, ancestry accounting, and the verdict rule
below. The draft is not edited in place. **Parent:** Round-C
`HYPOTHESES_ROUND_C.md` §5. **Objector:** grok-4.7
(`grok_objections_roundc.md` §H-PAM-33). **Date:** 2026-09-24.
**Crew:** B-33 (PAM round-2 swarm, second replacement; resumed from
`~/workspace/pam33/ref/`).

## Claim under test

Endorsed-channel admission: admit only percepts from trainer-endorsed channels
with an intact tamper-evident chain; content checks are audit-only. The
attacker's required capability shifts from "write acceptable bytes" to "enter
or compromise the endorsed channel."

Two readings are tested separately (grok's survive-iff):

- **V1 — inside the model:** the adversary cannot author any input that
  influences endorsed percept bytes (escape-(i): channels the author genuinely
  cannot write). Bars (a)(b)(c).
- **V2 — content-independence under WG:** grok's WG objection: the author
  writes generator parameters / scenario specs / asset choices; the world-sim
  is a deterministic function of those, so it pre-materializes endorsed falses;
  the chain is intact and the content audit does not gate. The killing bar the
  draft did not write: **endorsed falses caused by author-writable inputs = 0.**
  Bar (d). This frozen version operationalizes it with explicit causal-ancestry
  accounting (no hand-waving).

**Explicit contract (grok's demand):** the IN-MODEL adversary's writable set is
disjoint from the causal ancestry of endorsed percept bytes. The WG battery
deliberately steps one inch outside that contract. If bar (d) fires, the
content-independence claim is KILLED; what remains is a channel-integrity
check whose escape-(i) condition must be enforced externally (the tag is
label-blind — it binds bytes, not causal truth). That limitation is the test's
point, not a patch target.

## Construction under test (pure Zag, pinned)

- `toyhash`: `th_mix(h,v) = (h*131 + v') mod 2147483647` with
  `v' = v mod 2147483647` adjusted non-negative (stand-in for structure, not
  crypto; identical to the Round-C probe). `toyhash4(a,b,c,d)` =
  mix(mix(mix(mix(1,a),b),c),d) then mix(...,7). All operands non-negative;
  no u64 shifts, no u64 `%` (znc ZNC-2026-09-22 arithmetic-shift/signed-mod
  defects avoided by construction).
- Percept record: 5× LE32 = `(id, c, m, prev, tag)`, 20 bytes.
- `content_h = toyhash4(id, c, m, prev)`.
- Endorsement tag: `tag = toyhash4(content_h, ENDORSE_KEY, prev, 0x33)`.
- Chain: `prev_0 = GENESIS = 12648430`; `prev_{t+1} = tag_t`.
- `ENDORSE_KEY = 0x33E033` (harness-held). `ATTACKER_KEY = 0xBAD` (minted
  chains). `GENESIS`, keys, and `0x33` domain are probe constants.
- **Channel gate (verifier), per record t:** recompute `content_h` and `tag`
  with `ENDORSE_KEY`; check `prev == GENESIS` (t=0) else `prev == tag_{t-1}`
  (verifier-recomputed, left to right). Percept t is ADMITTED iff its tag
  verifies and its link holds. A tampered record breaks itself and all
  downstream records (linkage failure). Admission is per-record; the attacker's
  win is ≥1 admitted false.
- **Manifest variant** (`wg_manifest` arm only): the endorser additionally
  binds `manifest = toyhash2(SRC_ID, SLOT_LABEL)` into the tag preimage as
  `tag = toyhash4(content_h, ENDORSE_KEY, prev, manifest)`; the verifier
  recomputes the manifest from the harness input registry and requires every
  label ∈ {HARNESS=1}. `SRC_ID`: 11 = honest sensor organ, 12 = world-sim.
  `SLOT_LABEL`: 0 = AUTHOR-writable, 1 = HARNESS. This is the best real attempt
  at enforcing escape-(i) inside the mechanism; the WG-manifest arm tests
  whether label-binding saves content-independence when the registry mislabels
  an author-reachable input as HARNESS.

## Fixture classes (closed-form, zero RNG; N=20 unless noted)

- **honest (bar c):** harness sensor emits `c_t = 700 + ((t*7) % 31)`,
  `m_t = 2600 + ((t*11) % 51)` (true percepts), endorsed with `ENDORSE_KEY`,
  intact chain. Expect: admitted.
- **mint (bar a):** adversary-authored self-consistent chain (false percepts),
  tagged with `ATTACKER_KEY` (no harness key). Expect: 0 admitted.
- **tamper (bar b):** endorsed honest chain, then re-parent record 10
  (`prev := tag_8`), truncate (drop last 5 records → short chain, verifier
  still checks the 15 present), and insertion (duplicate record 5 with fresh
  id). Three sub-fixtures; expect: 0 admitted falses in each.
- **wg (bar d, plain mechanism):** author writes generator params
  `P0 = 41`, `P1 = 17` (author-chosen, recorded). World-sim (harness component,
  deterministic): `w_t = (P0*(t+1) + P1*7) mod 1009`. Sensor transduces the
  sim state into FALSE percepts `c_t = 100 + (w_t % 50)`,
  `m_t = 1000 + (w_t % 100)` (outside the honest band; label=false). The
  endorser endorses sensor output as a matter of course — it cannot see `P0`,
  `P1`. Chain intact, tags valid. Harness transcript records true causal
  ancestry: `{author: P0, author: P1}`. Expect per grok: admitted (mechanism
  cannot distinguish) → bar (d) counts them.
- **wg_manifest (bar d, manifest variant):** same as `wg`, except the
  author writes through the "scenario asset bundle" input slot, which the
  harness input registry labels HARNESS (label=1) — it is a normal
  world-building input the harness reads every run. Manifest check passes
  (labels clean per the registry); the transcript's TRUE ancestry still
  contains the author-writable slot. Tests whether manifest-binding detects
  the mislabeling. Expect per grok: admitted → bar (d) counts them.
- **classL (conjunction evidence, N=10):** same WG params; TWO channels:
  (1) endorsed percept chain (admits); (2) trainer corroboration bit computed
  from the same sim state, `verdict_t = 1 iff (w_t % 2) == 0` ("trainer looks
  at the same corrupted world and corroborates"). Pre-registered confirmation:
  Class-L confirmed iff ≥1 trial has channel 1 admitted AND channel 2
  corroborating on the same author-written params (disjoint modality without
  causal independence is one modality). No kill bar — conjunction evidence.
- **insider (bar e, N=5):** endorsement root captured pre-endorsement: the
  author holds `ENDORSE_KEY` and forges tags over arbitrary falses. The
  verifier cannot distinguish forged from honest. Per the draft: recorded as
  distal; if forged admits > 0 the hypothesis is VOID under root-capture
  (not repairable, not patched).

## Ancestry accounting (bar d, auditable)

Every admitted percept carries a transcript ancestry flag: 1 iff any
author-writable input is in its causal ancestry (author params `P0`/`P1`, the
asset-bundle slot in `wg_manifest`). Bar (d) counts admitted percepts with
ancestry flag = 1. The count is printed per fixture; the bar is mechanical.

## Kill bars

- (a) Minted (unendorsed) admitted > 0 = **KILL**.
- (b) Tampered endorsed admitted > 0 = **KILL**.
- (c) Honest intact endorsed admitted < 17/20, i.e. honest-loss > 15% =
  **FAIL** (over-withholder; kills the usability claim).
- (d) WG: admitted percepts with author-writable causal ancestry > 0 =
  **KILL of the content-independence claim** (plain and manifest variants
  counted separately; either firing kills it).
- (e) Insider: forged admits > 0 → hypothesis **VOID** under root-capture
  threat model (distal, recorded, not patched).
- Global: 3 runs, stdout SHA-256 byte-identical, else VOID. Pure Zag, zero
  randomness. No `as []i32/[]u32/[]u16` indexed casts (u8 arenas + LE32
  accessors per ZNC-2026-09-21-007); no other known znc landmines.

## Pre-registered verdict rule

- (a)∧(b)∧(c)∧(d) all hold → H-PAM-33 **TESTED-survived** (full claim).
- (a)∧(b)∧(c) hold, (d) fires → **TESTED-killed as a content-independence
  gate**; **CONDITIONAL-survives as a channel-integrity check** with
  escape-(i) enforced externally (grok's predicted outcome). The mechanism is
  then proven label-blind: identical bytes/tags are admitted whether the
  ancestry is clean or author-written.
- (a) or (b) fails → TESTED-killed outright. (c) fails → TESTED-killed as
  over-withholder.
- (e) fires → VOID-under-root-capture recorded alongside, per the draft.
- Class-L confirmation (if observed) is recorded as conjunction evidence and
  cited in every composition battery going forward.

## Composition note (Class-L, from the draft)

A trainer corroborating the same spec-authored world does not add
independence. The `classL` arm is the pre-registered demonstration. Every
future composition battery that pairs H-PAM-33 with H-PAM-30 must include
the Class-L fixture class or its passing verdict is worthless.
