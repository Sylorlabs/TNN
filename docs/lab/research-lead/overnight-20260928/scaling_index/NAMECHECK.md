# NAMECHECK.md -- Scaling/Indexing Worker

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any research computation:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing (only `guard-check-done` printed).
PATH restricted to $HOME/safebin for all subsequent work. Pure Zag via the
pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`. Shell used
only to invoke znc, run the binary, and for git/file operations.

No forbidden executable was invoked. No Python executed at any point.

## Step 1: Task identity

Scaling/Indexing Worker. Implement sublinear MAP indexing (Constitution
Section 17). Unfrozen variant only. Frozen source read-only.

## Step 2: Base provenance

Base: `docs/lab/research-lead/overnight-20260928/rebinding_hardening/hard_base.zag`
(SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa8bd`,
the canonical frozen TNN-2 base). Rebind mechanism logic copied from
`hard_patch.zag` (commit `0509fd116`, REBIND-HARDENING-COMPLETE).

Assembly (`build.sh`):
- base lines 1-532 (everything before promote_graph)
- base lines 544-812 (after promote_graph, before base ev_query)
- base lines 836-1356 (after base ev_query, before base main)
- base lines 1358-1591 (after base main)
- si_patch.zag (index mechanism + replacement ev_query/promote_graph)
- si_driver.zag (scale worlds + main)

Exactly one `fn main`, one `fn ev_query`, one `fn promote_graph` in the
assembled source (verified by build.sh).

## Step 3: What the patch changes

New file `si_patch.zag` (~150 lines). Base is otherwise byte-identical.

1. `rb_chain_plen` -- verbatim copy from hard_patch.zag (needed to
   compute the index key at promotion time).
2. `idx_node` / `idx_bfield` -- dedicated index node (tag 40, unused by
   the base; verified by tag-scan grep). Allocated once per world by
   `idx_mode_set`; node id kept in header field 52. Index node field 4 =
   mode (0 linear, 1 indexed); fields 20/24/28/32 = bucket heads for
   plen 2/3/4/5 (-1 = empty). (Header 32/36/40/44 are the base's context
   ring buffer via `ctx_push`; a first version of this patch collided
   with it and was fixed.)
3. `idx_add` -- pushes a promoted MAP id onto its plen bucket. Uses MAP
   node field 12 as the intrusive next-pointer (field 12 is -1/unused on
   MAP nodes in the base; verified no reader touches it on tag-20 nodes).
4. `promote_graph` -- verbatim base body (lines 533-543) plus a
   mode-gated `idx_add(W,m,root)` call. Mode lives in header field 52.
5. `rebind_try_lin` -- the hard_patch.zag linear scan, verbatim logic,
   plus a scan-work counter (header 56, one per slot visit) and a
   plen-walk counter (header 60, one per rb_chain_plen call).
6. `rebind_try_idx` -- indexed retrieval: gather paths, walk only the
   buckets whose plen matches a gathered path length, collect candidate
   ids, insertion-sort ascending, then run the identical (MAP,path)
   trial nest as the linear scan. Counters in header 56/60 as above.
7. `ev_query` -- base/hard_patch logic with the rebind call dispatched
   on the mode flag.

The index is learner-maintained: it is written only by `idx_add`, which
fires on promotion events (trial-built, rebound, driver-taught). No
researcher-authored MAP table exists anywhere.

## Step 4: Determinism

3/3 byte-identical runs required per world. sha256 of run transcripts
recorded in REPORT.md.

## Constraints honored

Unfrozen variant only. Frozen source untouched. Pure Zag. Zero em/en
dashes in docs (byte-verified). Research paper untouched. Nothing pushed.
0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
