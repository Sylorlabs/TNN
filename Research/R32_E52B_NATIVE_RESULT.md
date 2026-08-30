# R32 E52B — Native On-Policy Joint Decision Result

Date: 2026-08-29  
Status: `EXECUTED_NATIVE DIAGNOSTIC NEGATIVE — ON-POLICY OSCILLATION AND COST EXPLOSION`  
Canonical: R27 step 60,423

## Question

E52A trained continuation on every tape state but executed only states reached by its own policy. E52B tested deterministic iterative on-policy fitting: regenerate the reached-state ledger under the current policy, refit continuation value, and repeat for four frozen iterations, then allow the generic sparse Foundry to fit remaining residual structure.

## Data boundary and limitation

The original one-million-state component-disjoint allocator was exhausted. E52B used never-before-used base seeds for every new `(seed, mode, resource)` world and reported subordinate simulator-state reuse instead of hiding it.

- manifests emitted: 15,120
- base-seed reuse: 0
- evidence-substream overlap worlds: 8,099
- resource-substream overlap worlds: 785
- validation: 2,700 new base-seed-unique worlds
- sealed confirmation: 5,400 allocated, 0 executed

Because subordinate pseudorandom substreams overlap earlier reservations, E52B is diagnostic-only even if its behavioral gates had passed.

## Integrity

- parent E50 integrity: PASS
- terminal Foundry: 8 interactions, deterministic forward/reverse
- on-policy fitting integrity: PASS
- `UNKNOWN` parameters: 0
- source SHA-256: `0d2283e0848cf9058fd876854ee8047263cd1c23bf70b6acbb5846e0c305c7ca`
- two byte-identical native binaries: `6d1e4a5308837bcd568190a851d84bd977d711a0cc56e251c9efba4f826486fd`
- raw ledger SHA-256: `761119205727b6dd6ce496924b556bac050db5f5f9ab2fd59346c56fd11d8ecc`
- runtime: 171.12 seconds; expected qualification exit: 1

## Policy-distribution behavior

Reached-state counts did not converge.

| Policy | iteration 0 | iteration 1 | iteration 2 | iteration 3 | final |
|---|---:|---:|---:|---:|---:|
| frozen terminal geometry | 4,775 | 14,726 | 11,824 | 11,897 | 11,149 |
| Foundry terminal geometry | 4,667 | 14,195 | 11,825 | 11,737 | 11,323 |

The large alternating distribution shifts are a policy-iteration instability, despite deterministic execution.

## Validation

| Arm | Success | UNKNOWN | Wrong | Known success | Known wrong | No-unique UNKNOWN | No-unique wrong | Observations | Opportunity cost | Net utility |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A frozen terminal | 1,185 | 1,408 | 424 | 868 | 141 | 317 | 283 | 0 | 0 | 246,400 |
| B frozen + on-policy continuation | **1,500** | 1,255 | 289 | **1,156** | **33** | 344 | 256 | 6,305 | 906,738 | **-123,938** |
| C Foundry terminal | 1,171 | 1,439 | 406 | 855 | 122 | 316 | 284 | 0 | 0 | **270,200** |
| D Foundry + on-policy continuation | 1,461 | 1,257 | 307 | 1,136 | **32** | 325 | 275 | 6,514 | 929,419 | **-187,419** |

On-policy learning found genuine correctness leverage: B added 288 known successes and removed 108 known wrong commits relative to A. But it spent 906,738 utility units on observations and drove net utility below zero. D showed the same pathology and was worse than B on total net utility.

## Conclusion

Naive repeated on-policy refitting is rejected. The current bottleneck is not another manually authored ambiguity feature. It is stable cost-aware policy improvement under endogenous distribution shift: the learner must improve continuation value without oscillating between state distributions or ignoring the long-run shadow price of observation.

The next bounded experiment should compare naive E52B against a generic conservative policy-improvement substrate with learner-updated resource shadow price, replay across prior reachable distributions, and acceptance based on full-development net delayed utility. No ambiguity label, mode identifier, fixed observation count, or positive UNKNOWN bias is permitted. R27 remains canonical.
