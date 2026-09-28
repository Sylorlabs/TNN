#!/usr/bin/env python3
"""Pass 3: hooks, student, memories, revision history, grad-key sweep."""
import sys, collections, json
sys.path.insert(0, "/tmp/tnn-lab/brain")
from restricted_load import load, StubBase

obj = load("/tmp/tnn-lab/brain/parent-r27-accepted-state.pkl")

def all_stubs(o, seen=None):
    if seen is None: seen = set()
    if id(o) in seen: return
    seen.add(id(o))
    if isinstance(o, StubBase):
        yield o
    kids = [o.__dict__] if isinstance(o, StubBase) \
        else list(o.values()) if isinstance(o, dict) \
        else list(o) if isinstance(o, (list, tuple, set, frozenset)) else []
    for k in kids:
        if k is not None:
            yield from all_stubs(k, seen)

stubs = list(all_stubs(obj))

print("=== backward_hooks content (one param) ===")
par = [s for s in stubs if s._stub_name == "_rebuild_parameter"][0]
a = par._stub_args
print("  data type:", type(a[0]).__name__,
      getattr(a[0], "_stub_name", ""))
print("  requires_grad:", a[1])
print("  backward_hooks:", repr(a[2])[:300])

print("\n=== 'grad' key sweep across all dict keys ===")
grad_keys = collections.Counter()
def sweep(o, seen=None):
    if seen is None: seen = set()
    if id(o) in seen: return
    seen.add(id(o))
    if isinstance(o, dict):
        for k in o.keys():
            if "grad" in str(k).lower() or "optim" in str(k).lower():
                grad_keys[str(k)[:70]] += 1
        kids = list(o.values())
    elif isinstance(o, StubBase):
        kids = [o.__dict__]
    elif isinstance(o, (list, tuple, set, frozenset)):
        kids = list(o)
    else:
        kids = []
    for k in kids:
        if k is not None: sweep(k, seen)
sweep(obj)
print("  grad/optim keys found:", dict(grad_keys) if grad_keys else "NONE")

print("\n=== MutableStudent keys ===")
ms = [s for s in stubs if s._stub_name == "MutableStudent"][0]
print(" ", [k for k in ms.__dict__ if not k.startswith("_stub")][:25])

print("\n=== memory components keys ===")
for name in ("ProtectedSkillMemory", "GroundedConceptMemory",
             "MotifProgramMemory", "HybridRelationalMemory",
             "AnonymousRelationalStore", "VideoNameMemory",
             "MultiViewEntityGraph", "EntityEventGraph"):
    ms_ = [s for s in stubs if s._stub_name == name]
    if ms_:
        print(f"  {name}:",
              [k for k in ms_[0].__dict__ if not k.startswith("_stub")][:14])

print("\n=== self_revision_history: entry shape ===")
srh = obj.__dict__["self_revision_history"]
print("  len:", len(srh), "entry type:", type(srh[0]).__name__)
e0 = srh[0]
if isinstance(e0, dict):
    print("  keys:", list(e0.keys())[:12])
    for k, v in list(e0.items())[:6]:
        print(f"    {k} = {repr(v)[:90]}")
print("  last entry keys:",
      list(srh[-1].keys())[:12] if isinstance(srh[-1], dict) else None)

print("\n=== development_step per lineage level ===")
cur, lvl = obj, 0
while isinstance(cur, StubBase) and lvl < 8:
    print(f"  L{lvl} {cur._stub_name}: step={cur.__dict__.get('development_step')!r} "
          f"restarts={cur.__dict__.get('newborn_restarts')!r}")
    nxt = None
    for k in ("base_state", "r24_state", "r23_state"):
        v = cur.__dict__.get(k)
        if isinstance(v, StubBase):
            nxt = v; break
    cur, lvl = nxt, lvl + 1

print("\n=== numpy Generator / Random state ===")
for s in stubs:
    if s._stub_name in ("__generator_ctor", "__bit_generator_ctor",
                        "Random", "__pyx_unpickle_SeedSequence"):
        print(f"  {s._stub_mod}.{s._stub_name}: args={s._stub_args!r}"[:160])

print("\n=== Trace: ops / support value shapes ===")
t0 = [s for s in stubs
      if (s._stub_mod, s._stub_name) == ("r15_master_training", "Trace")][0]
for k in ("cue", "ops", "support", "sources", "verified", "failures",
          "age", "provenance", "anchors"):
    v = t0.__dict__.get(k)
    print(f"  {k}: {type(v).__name__}" +
          (f" len={len(v)}" if isinstance(v, (list, tuple, dict)) else "") +
          f" {repr(v)[:100]}")

print("\n=== architecture['compute'] ===")
print(" ", repr(obj.__dict__["architecture"].get("compute"))[:400])
