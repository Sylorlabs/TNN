# NAMECHECK: P2-Deep Lifetime Worker

## Step 0: Toolchain guard

Executed at worker startup:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `which python3 python` returned nothing. Safebin PATH active.
Guard check recorded. No forbidden executable invoked.

## Scope

Persistent connections in a longer lifetime (Constitution Section 25).
Micah Priority 2 deep follow-up. Governance gap: "persistent connections
in 1000+ event lifetime, spontaneous formation". Unfrozen variant only.
Frozen TNN-2 source read-only.

## Input provenance

- Base cognition: `../persistent_connections/pc_base.zag`, SHA-256 prefix
  `a29972ca8183b285`, verified equal to frozen TNN-2 base (same file the
  C186 worker used).
- Link mechanism: `../persistent_connections/pc_patch.zag` (type-14 LINK
  write on verified rebind, two-pass rebind_try), used verbatim.
- Control rebind: `../persistent_connections/pc_vanilla_patch.zag`
  (vanilla single-pass rebind, no links), used verbatim.
- World-stream pattern: `../persistent_connections/pc_driver_treat.zag`.

## Assembly method (verified byte-exact against C186 artifacts)

Treatment/ablation full file:
  base lines 1-812 + base lines 836-1356 + base lines 1358-1591
  + pc_patch.zag + p2l_driver_*.zag
(base ev_query lines 813-835 and base main line 1357 removed; patch
supplies ev_query, driver supplies main).
Verified: this recipe reproduces `../persistent_connections/pc_full_treat.zag`
and `pc_full_abl.zag` byte-identically.

Control full file: same base surgery + pc_vanilla_patch.zag + driver
(function order irrelevant in Zag; compiles and runs).

## Mechanism delta (this worker)

None to cognition. This worker contributes only the lifetime driver:
A -> 320 interference -> B -> 320 -> C -> 320 -> D(A-like), one continuous
learner, LINK14 census after every phase. The link mechanism is verbatim
C186. Researcher-owned: driver world-stream design, gap sizes, phase
subjects. Learner-owned: all type-14 link endpoints and topology.

## Constraints

Pure Zag via pinned znc. Zero em/en dashes in docs. Paper untouched.
Nothing pushed. 0 modes, 0 bridges, 0 handlers, 0 semantic cases.
