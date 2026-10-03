# MAP_INVENTORY: L3-INR frozen MAP inventory

Frozen at the L3-INR implementation code freeze (this directory).
The inventory below is the complete set of pre-existing MAPs available
to the learner. Per prereg G2(a), no MAP in this inventory computes the
S1 relational rule (the hidden strict total order); control C0 confirms
empirically by failing. The inventory is fixed: the implementation adds
zero new MAPs, zero new opcodes, zero new semantic cases.

Entity surface attributes: each entity carries 3 integer attributes
(values 0..9), adversary-designed with |Spearman rank correlation| < 0.2
against the hidden order (exhibited in the sealed key; DEV worlds exhibit
it in dev/ATTRS_CHECK.txt).

## MAP-ATTR-THRESH (single-attribute pair threshold)

For attribute k in {0,1,2} and direction d in {up, down}:
predict y=1 for pair (a,b) iff attr_k(a) < attr_k(b) (d=up) or
attr_k(a) > attr_k(b) (d=down). Six fixed rules; no thresholds beyond the
strict inequality (values are a permutation, no ties within an
attribute). Used by control C2 as the greedy-attribute constructor basis.

## MAP-ATTR-NN (attribute nearest neighbor)

For a query pair (a,b), score each training pair (c,d) by attribute
agreement: agreements = [attr0(a)==attr0(c)] + [attr1(a)==attr1(c)] +
[attr2(a)==attr2(c)] + [attr0(b)==attr0(d)] + [attr1(b)==attr1(d)] +
[attr2(b)==attr2(d)]; pick the training pair with max agreements
(first-max tie-break on training index); predict its outcome. Used by
control C0 (construction disabled).

## MAP-PAIR-MEMO (pair memorization)

Stores ACCEPTed (pair, outcome) triples from the TEST channel. Answers a
held-out pair only if the exact pair was stored; otherwise abstains
(control C1 falls back to 1-NN in pair space, see below).

## MAP-PAIR-1NN (1-nearest-neighbor in pair space)

For a held-out pair (a,b) over internal ids, distance to a stored
training pair (c,d) is (a!=c) + (b!=d) (Hamming over the pair);
nearest = minimum distance, first-max tie-break on training index;
predict the nearest stored outcome. Used by control C1.

## MAP-MAJORITY (majority label)

Predicts the majority outcome over observed training instances for every
query pair. (Reference baseline; not used by a control arm in this
battery because the DEV held-out label balance would let it pass the
5/6 bar on some worlds, which would prove nothing about the inventory's
sufficiency for the relational rule. Documented here for completeness.)

## MAP-ID-ORDER (internal-id order)

Presents entities sorted by learner-internal id as a ranking. Used by
control C5 (naive reuse: T1's committed edge set applied to Task B with
no ranking procedure). Internal ids are assigned by first OBSERVE
appearance order, which the world designs to differ from the hidden
order, so this MAP fails Task B.

## Attestation

None of the above computes, encodes, or approximates a hidden strict
total order over entities: they are generic similarity, memorization,
majority, and ordering MAPs over surface attributes, stored pairs, and
internal ids. The relational rule (reachability over an invented
directed edge set) is not in this inventory, which is exactly what
control C0 (below 5/6 on held-out with MAP-ATTR-NN) establishes
empirically on the DEV world and must establish on sealed S1.
