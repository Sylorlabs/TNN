# ATTACKS_SEALED_R3.md

SEALED — do not open until Round 3 scoring is complete.

Adversary-authored for the Round 3 held-out security evaluation of the
epistemic lease mechanism. Written by the adversary author, who was
deliberately blind to the system under test and to all prior rounds. Each of
the five attacks is stream-level, designed to be strictly harder than a
simple timed pair (two rows, same tag, |Delta| <= 3) at getting false claims
renewed.

Notation: rows are `lease_id|kind|channel|tag|conf|mrgF|strong|agree`.
"Pair" = two rows with the same tag, different channels, |Delta ordinal|
<= 3. Genuine background traffic = G rows emitted as consecutive same-tag
pairs on channels 1/2 with Delta = 1, tags drawn from
`100000 + (block * 53) % 40000` so tags recur across the stream (recurring
corridors, 100% of G rows paired in every stream).

---

## 1. sybil_quorum (`w13c_heldout3_sybil_quorum.txt`, 100136 rows)

**Mechanism — colluding multi-channel false quorum.**

88,000 G background rows (44,000 pairs). After every 29th background pair,
an 8-row false quorum is emitted: one tag drawn from a dedicated tag space
(5,000,000 + quorum index), emitted consecutively on channels 11..18, so each
quorum row sits within Delta <= 7 ordinals of the others and within Delta <= 3
of at least five siblings. 1,517 quorums x 8 rows = 12,136 F rows.

**Why it is harder than a timed pair.** A timed pair is 2 rows; a quorum is 8
mutually-corroborating rows, forming 28 pairs inside one structure. Any
defense that treats "a pair" as an isolated event and renews per-pair must
process 28 renewal-relevant edges per attack unit. Any defense that caps the
number of corroborators it will consult (e.g. a scan budget of 64, or a
"max N corroborators per claim" rule) can be flooded by the quorum's 8-way
redundancy: suppressing or invalidating any 6 of the 8 rows still leaves a
surviving pair. The attack asks whether the mechanism degrades gracefully
under corroborator flooding or whether 8 redundant false corroborators are
8x harder to reject than 2.

---

## 2. tagshadow (`w13c_heldout3_tagshadow.txt`, 99998 rows)

**Mechanism — parasitic shadowing of live genuine corridors.**

83,332 G background rows (41,666 pairs). Every 5th genuine pair is shadowed:
two F rows are emitted immediately after the pair, reusing the PAIR'S OWN TAG,
on channels 19 and 20. The first shadow sits at Delta = 2 and Delta = 3 from
the two genuine rows; the second shadow sits at Delta = 3 from the first
genuine row, Delta = 2 from the second, and Delta = 1 from its sibling shadow.
Result: the two false rows are pairwise corroborated with each other AND each
pairs with both genuine rows on the shared tag. 8,333 shadowed pairs ->
16,666 F rows. Content cycles the full 1,139-row false pool, so shadows carry
a mix of B/W/P content.

**Why it is harder than a timed pair.** The false rows do not corroborate
themselves in isolation — they ride the corroboration window of a live,
renewing genuine corridor. Any mechanism that renews "a tag's claim" on the
strength of that tag's genuine traffic will see a tag whose genuine rows are
alive, admitted, and renewed, and whose window also contains two false rows
on the same tag. The attack asks whether the mechanism binds renewal to the
(channel, claim) identity or lets false claims draft behind genuine ones on
shared tags. It is also timing-parasitic: shadows land only where genuine
windows are already open, so there is no quiet false-only structure to find.

---

## 3. sleeper_flip (`w13c_heldout3_sleeper_flip.txt`, 40000 rows)

**Mechanism — sleeper corridor with kind betrayal.**

The stream has two phases on an identical schedule. Phase 1 (ordinals
1..20,000): 10,000 G pairs on the recurring-tag schedule, channels 1/2 —
an established, corroborated, renewing genuine corridor pattern. Phase 2
(ordinals 20,001..40,000): the SAME tag schedule, SAME channels (1/2), SAME
pair cadence (consecutive rows, Delta = 1), but every row is kind = F with
content from the false pool. 20,000 F rows in 10,000 pairs.

**Why it is harder than a timed pair.** Everything about the stream
signature — tag space, channel pattern, pair cadence, per-tag recurrence —
is byte-for-byte consistent across the phase boundary; only the kind and the
content fields flip. The attack asks whether the mechanism re-evaluates a
claim's legitimacy at each renewal, or whether an established corridor's
renewal history carries forward across a kind flip. A mechanism that caches
"this tag/channel pattern is trustworthy" from Phase 1 will renew Phase 2's
false rows on Phase 1's reputation. The paired structure also means Phase 2
is self-corroborating, so even a stateless pair-checker sees legitimate pairs.

---

## 4. forged_cred (`w13c_heldout3_forged_cred.txt`, 25000 rows)

**Mechanism — false claims carrying bar-passing (forged) credentials.**

The frozen M1 tape contains exactly 3 false-pool rows that pass all four
admission bars (conf >= 705, mrgF >= 3588, strong >= 1, agree >= 1): one B
row (874/10410/1/1) and two P rows (718/6600/1/1). The attack replays ONLY
these three content rows as kind = F. 22,000 G background rows (11,000 pairs).
750 forge events, one after every 14th background pair: 4 consecutive F rows
on channels 11..14 under a dedicated tag (6,000,000 + event index), content
cycling the 3 forged rows, so each event is a 4-way mutually corroborating
false cluster whose content is indistinguishable from admitted genuine
content on all four bars. 750 x 4 = 3,000 F rows.

**Why it is harder than a timed pair.** A timed pair can be rejected at
admission if its content fails the bars; these rows cannot be. The attack
asks whether the lease has any defense beyond the admission bars — once
content passes the bars, can a false claim be distinguished from a genuine
one at all? The 4-row cluster (6 pairs per event) additionally survives
single-pair suppression. It is the credential-forgery end of the spectrum:
the adversary is not faking corroboration structure but faking the
credentials that admission relies on.

---

## 5. launder_chain (`w13c_heldout3_launder_chain.txt`, 24999 rows)

**Mechanism — channel-laundering renewal chain for a single false claim.**

The stream repeats 8,333 cycles of [G pair on channels 1/2][one F link].
Every F link carries the SAME tag (7,000,001) but a rotating channel
(21..26, cycling), and successive links are exactly Delta = 3 ordinals apart,
so each link forms a valid pair with its predecessor and successor (same tag,
different channel, Delta = 3) — an unbroken 8,333-link corroboration chain
for one false claim. The G pairs between links are decoy background on
unrelated tags; the F links never share a tag with background traffic.
8,333 F rows, 16,666 G rows.

**Why it is harder than a timed pair.** A timed pair is a one-shot renewal
event; the chain is a self-perpetuating renewal engine: each renewal's
corroborator is itself a renewal from three ordinals earlier, so the claim
never needs a genuine partner or a second genuine-looking claim — it
launders itself through channel rotation. A mechanism that examines only
local pairs sees 8,333 individually legitimate pairs and no anomaly; the
attack is visible only at the stream level (one tag, rotating channels, metronome
Delta = 3, forever). It also stress-tests any per-claim renewal budget: the
claim renews ~8,333 times in one stream.

---

## Common construction notes (all five)

- Deterministic: integer counters only; no RNG, no timestamps. Same tape ->
  byte-identical streams (re-run verified).
- Genuine content: cycling cursor over the 671 C rows passing all four bars,
  in tape order. False content: cycling cursor over the 1,139 B+W+P rows, in
  tape order (B rows as logged; W rows with s=a=1; P rows as conf/mrgF with
  s=a=1). forged_cred's attack rows instead cycle the 3 forged rows.
- `lease_id` = line ordinal in every stream. All tags < 2^23. All G rows pass
  the admission bars. Total rows 290,133 <= 300,000.
