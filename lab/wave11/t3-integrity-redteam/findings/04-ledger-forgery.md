# Ledger Forgery Under Variation (Track 3, Slice 04)

## 1. Slice
Track 3 (integrity red-team under variation), slice 04: forge VARIATION_CHOICE entries
(variant_id + selector_hash) from the slice-15 design and test whether the canonical
binary entry layout + selector re-derivation audit detects it. RED TEAM: break the design.

## 2. Falsifiable claim
At least one of three forgery classes — (a) forged variant_id smuggled via the
forced_flag exemption, (b) stale selector_hash replayed across intra-episode choice
points, (c) variant-table semantic swap under a fixed policy_version id — produces a
VARIATION_CHOICE entry that passes hash-chain verification, the selector re-derivation
check, and the forced-variant byte-invariance diff without flagging. If an implemented
audit harness catches all three at the stated bars, this claim dies.

## 3. Design (the attacks)
Common setup: target the slice-15 layout
`idx:u32|episode:u32|clock:u64|op:u8|prev_hash:32B|payload|entry_hash:32B`, payload
`variant_id:u16, selector_hash:32B, policy_version, forced_flag:u8`. Assume the attacker
can write ledger bytes and rebuild the SHA256 chain forward from the fork — the chain is
unkeyed, so chain integrity binds order, not authorship (wave5/6 evidence: the ledger
PROVES, it does not prevent — `docs/lab/wave5/`, `docs/lab/wave6/`).

**(a) Forged variant_id.** Mechanism: entry with variant_id=v' (valid table index, never
selected), the genuine selector_hash, forced_flag=0, rebuilt chain. DETECTED — if the
auditor recomputes v=selector(input_hash, state_hash) from STATE_HASH-anchored state at
the exact choice point and compares; the recomputed v never equals v'. Detection bar:
re-derivation must run per entry from anchored state, never trust entry fields. THE
HOLE: forced_flag=1 exempts the entry from re-derivation (forced runs legitimately don't
re-derive) AND its variant_id bytes are exempt from the invariance diff. A forged entry
with forced_flag=1 + arbitrary variant_id passes every byte-level and recompute check.
Detection then rests entirely on authenticating WHO set forced_flag — slice 15 specifies
no mechanism for this; wave9's OS-level channel binding for the trainer console is the
required binding, currently unattached to this flag. A valid-but-unselected id with
forced_flag=0 fails; the same id with forced_flag=1 sails through.

**(b) Stale selector_hash replay.** Mechanism: copy selector_hash_E (committed at episode
E) into a forged entry at episode E+n with variant_id=v_E, rebuilt chain. DETECTED
across episodes — the auditor recomputing SHA256(canonical(fv(S_{E+n}))) from the
E+n-anchored state gets a mismatch, since the feature vector moved. THE HOLE: choice
points WITHIN one episode. STATE_HASH anchors state at episode granularity (K=1);
slice 15 logs "variation choices made along the way" of deliberation — multiple choice
points per episode share one anchor. Replaying choice-1's (variant_id, selector_hash)
into choice-2's entry is undetectable by any audit recomputing only from episode-level
anchors: both choices reduce to the same anchor, so both field sets verify. Detection
bar: every variation choice point needs its own state anchor — bind a choice-point
state hash into the entry or log STATE_HASH at choice-point granularity.

**(c) Table-swap smuggle.** Mechanism: slice 15 logs the policy_version id but NO hash of
the variant table. Register or mutate the variant table under the SAME policy_version id
so variant_id=N now means different content treatment (e.g. which evidence slots get
cited — content, not phrasing). Within the swapped table, forced-variant runs still
differ only in variant_id bytes (invariance diff passes), and the selector still outputs
N lawfully from state (re-derivation passes) — but the semantic content of the
"invariant" ledger has moved. The u16 index is authenticated; its referent is not.
Detection bar: commit SHA256(canonical(variant table)) in the ledger at policy
registration (as a GATE_EVENT), and re-run the forced-variant content-set comparison per
policy_version — the claim SET must be identical across forced variants of that table.
Secondary: the diff harness must parse entries to locate variant_id fields, never assume
byte offsets (AGENTS.md audit-layout lessons: field offsets drift; an off-by-N exempt
window is itself a smuggle channel).

**Win condition:** one undetected forged entry = ledger broken. The ledger's sole
load-bearing role is after-the-fact provability; a forgery class that evades the audit
once can be applied to any entry, and no auditor can then distinguish genuine from
forged entries.

## 4. Kill bar
My red-team claim dies if an implemented Zag audit harness — canonical encoder + chain
verifier + per-choice-point re-derivation + table-hash binding + channel-bound
forced_flag — catches all three forgery classes across 200 planted-forgery trials with
zero misses and zero false flags on the 200-pair clean baseline. Blue-team (ledger)
kill, prereg-style: ANY single planted forgery the harness accepts = slice-15 design
broken; repair required before the Arm C trial proceeds.

## 5. Honesty notes
Where I am weakest: (a)-via-forced_flag and (c) are authorization/binding gaps, not
crypto breaks. If the constitution side (RC architecture: TNN holds 0% of ledger rules)
already authenticates the ledger writer and pins the variant table by means I have not
seen in the slice-15 design, these holes shrink to implementation bugs — the design as
WRITTEN has them. I am NOT claiming the hash chain is broken; it is fine, and my attacks
honestly assume the standard unkeyed-chain property. (b)'s intra-episode hole assumes
multiple choice points per episode; constrain to one VARIATION_CHOICE per episode and it
closes (at expressiveness cost). Cross-episode stale replay FAILS against the design —
credit where due. Nothing here is built or run in Zag; these are design-level attacks,
untested. The "one forged entry = broken" win condition is deliberately maximalist:
Micah's bar for the ledger is provability, and provability is binary.

## 6. Next build step
Build the slice-15 canonical encoder + audit harness in Zag with all three forgeries as
planted-negative tests from day one (forged variant_id under forced_flag=1, stale-hash
replay into a second intra-episode choice point, table swap under a fixed policy id):
if the harness does not catch all three on a minimal corpus, the design is not
trial-ready. Only then wire the selector into the live system.
