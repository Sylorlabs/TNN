# NAMECHECK.md - H2 Trap World Builder

## Step 0: Toolchain Guard

Date: 2026-10-01 (PDT)
Worker: Trap World Builder

Commands run:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing. Only "guard-check-done" printed.
Safebin PATH active. Zero forbidden executables invoked.

## Scope

Build sealed trap worlds for H2 masked verification probes (design: commit
`4631c5918`). Three worlds: H2A (withhold trap), H2B (lie trap), H2C
(own-criterion trap). Pure Zag generation. No TNN-2 modification. No
evaluation (worlds are sealed test assets; evaluation comes later after
Micah freezes K-H2-1..K-H2-4).

## Provenance

- H2 probe design: `docs/lab/research-lead/overnight-20260928/tnn2_h2probes/H2_PROBE_DESIGN.md` (commit `4631c5918`)
- Search order: chains k=2..4, then sums (dead in production), then counts, then single hops (from `340e94e3e`, `4631c5918`)
- World format: `OBSERVE s r o`, `QUERY s r expected`, `ACT` (from `e409f5eea` ADVERSARY_DESIGN.md)
- ID range: H2 worlds use [50000, 59999], disjoint from FW [30000,39999] and GW [40000,49999]
  - H2A: [50000, 50099]
  - H2B: [50100, 50199]
  - H2C: [50200, 50299]

## Constraints Honored

- Owned path only: `docs/lab/research-lead/overnight-20260928/h2_trapworlds/`
- No sealed FW/GW contents inspected
- Paper untouched
- No em dashes in documentation
- Pure Zag for generation (pinned znc)
- Worlds built but NOT run through TNN-2 (seal preserved)
