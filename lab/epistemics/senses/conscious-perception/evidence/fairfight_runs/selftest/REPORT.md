# FAIR FIGHT comparison run

forks: AUTOPILOT=58af06c26d11, DELIBERATIVE=e3d61b8f6184
battery fixtures: 14 (scored: 12, redteam cost-only: 2)
byte-identical failures: 0; contract errors: 0

**catches (deliberative correct ^ autopilot wrong): 0/12**
mean ops ratio (delib/auto): 1.000; resense episodes: 0

## Kill bars
- KB-D1_zero_catches: KILLED {'catches': 0, 'killed': True}
- KB-D2_cost_without_gain: alive {'mean_ops_ratio': 1.0, 'killed': False}
- KB-D3_denial_of_perception: alive {'max_rt_ops_ratio': 1.0, 'killed': False}
- KB-A1_autopilot_wins_speed: alive {'note': 'evaluated from S1-S4 legs; autopilot wins recorded, never kills'}

## Per-fixture
| fixture | leg | auto | delib | catch | ops_ratio | resense |
| om_p1.pcm | omission | SAME✗ | SAME✗ | False | 1.0 | 0/none |
| om_p2.pcm | omission | SAME✗ | SAME✗ | False | 1.0 | 0/none |
| om_p3.pcm | omission | SAME✓ | SAME✓ | False | 1.0 | 0/none |
| om_p4.pcm | omission | HIGHER✓ | HIGHER✓ | False | 1.0 | 0/none |
| om_t1.pcm | omission | PURE✗ | PURE✗ | False | 1.0 | 0/none |
| om_t2.pcm | omission | BRIGHT✓ | BRIGHT✓ | False | 1.0 | 0/none |
| ib_m1.vid | inattentional | E✗ | E✗ | False | 1.0 | 0/none |
| ib_m2.vid | inattentional | W✓ | W✓ | False | 1.0 | 0/none |
| am_p1.pcm | ambiguity | HIGHER✓ | HIGHER✓ | False | 1.0 | 0/none |
| am_c1.img | ambiguity | DIFFERENT✓ | DIFFERENT✓ | False | 1.0 | 0/none |
| il_c1.img | illusion | DIFFERENT✗ | DIFFERENT✗ | False | 1.0 | 0/none |
| il_c2.img | illusion | SAME_SURFACE✗ | SAME_SURFACE✗ | False | 1.0 | 0/none |

## Redteam (cost only)
- rt_p1.pcm: ops_ratio=1.0 wall_ratio=0.778 resense=0
- rt_c1.img: ops_ratio=1.0 wall_ratio=0.388 resense=0
