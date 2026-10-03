# PREREG_AMEND2.md -- executable fact encoding (committed before any implementation commit)

Date: 2026-10-03. Status: FROZEN (amends PREREG.md Section 2).

## What changed

PREREG.md Section 2 wrote facts in the COMPOSE-GENERAL-1 shorthand,
e.g. "(211,92,3)" for Y(211)=3. On the PAIR6 substrate the COUNT
class returns the NUMBER of matching (s,rel) facts (d6_base.zag
count_rel; verified in compose_pair6_adv: Y(211)=3 is realized as
three distinct facts (211,92,901..903)). A single (211,92,3) fact
would make Y(211) evaluate to 1, which is why the first full-binary
run solved nothing (ANS stayed -2; the mechanism itself was never
at fault).

## Replacement (frozen executable encoding)

COUNT outcomes are realized as that many distinct dummy-object
facts; WALK outcomes as single facts. All predicted values
(ANS=5/3/7/9, exec counts, deltas) are UNCHANGED; only the
encoding of the worlds changes:

- Q1: (202,91,211); (211,92,901),(211,92,902),(211,92,903);
  (211,94,911),(211,94,912).
- Q1b adds: (204,91,212); (212,92,904),(212,92,905);
  (212,94,913).
- Q1rev: retract BOTH (211,94,*) facts (two fact_del calls);
  V gets (211,95,921),(211,95,922).
- CHAIN3: (301,81,302); (302,82,303);
  (303,83,801..807) (seven facts, c2(303)=7).
- FANIN: (401,71,701..704) (four facts, f1(401)=4);
  (401,72,705..709) (five facts, f2(401)=5).
- Q2: same encoding as Q1.
- Blind variants: same multiplicities under relabeling.

WALK uses single-hop lookup (fact1); no multi-hop WALK chains
exist in the frozen worlds, so this coincides with the substrate's
walkf on every frozen query. No mechanism file changes; only
sus_world.zag setups change.
