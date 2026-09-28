# Determinism manifest — D2 re-run 2026-09-28

## Learner binary

`wb3_learner`, rebuilt from committed source
(`docs/lab/composition/redo_2026-09-27/`):

- SHA-256: `16c023cabfedf5af36b12ec2c03a3c9802ec5f83c646b318f2f0010b98369d48`
- Matches the pinned composition-redo binary SHA byte-identically.
- Binary NOT committed (repo standard: no build outputs).

## Instrument binary

`d2bin`, rebuilt from committed source (`docs/lab/composition/d2/src/`):

- §10 reference gate on the rebuild: refok P0 24/24, P2 24/24;
  null 0/24; singlerule 0/24; wrongorder 24/24 — matches BUILD_LOG.md.
- Binary NOT committed.

## Results byte-identity

| Artifact | Run 1 | Run 2 | Perturbed (`MALLOC_PERTURB_=165`) |
|---|---|---|---|
| `results_p0.json` | `e5a109f8fc2f92bc7b8eb0545aaa286354ad520528b616207049251275cdb5e4` | identical | identical |
| `results_p1.json` | `6e5a338de610e513fe33c51376c0b279b71408ab37d546c1078ad79511d198f9` | identical | identical |

3/3 byte-identical for P0; 3/3 byte-identical for P1, including the
allocator-perturbed run. Pure Zag, zero randomness in all paths.

## Scenario integrity

All committed D2 scenario SHA-256 entries verified before the runs: OK.
