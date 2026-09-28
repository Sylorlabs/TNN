#!/usr/bin/env python3
"""Deep white-box analysis of the loaded R27 state (uses restricted_load)."""
import sys, collections
sys.path.insert(0, "/tmp/tnn-lab/brain")
from restricted_load import load, StubBase, CALL_LOG, CLASS_CACHE

obj = load("/tmp/tnn-lab/brain/parent-r27-accepted-state.pkl")
d = obj.__dict__

print("=== top-level scalars ===")
for k in ("format", "development_step", "newborn_restarts", "r26_sha256"):
    print(f"  {k} = {d.get(k)!r}")

print("\n=== torch tensor requires_grad / backward_hooks ===")
rg = collections.Counter(); bh_nonempty = 0
for mod, name, kind, argrepr in CALL_LOG:
    pass  # argrepr is stringified; re-derive from stubs below

# find tensor/parameter stubs and read their recorded args
def all_stubs(o, seen=None):
    if seen is None: seen = set()
    if id(o) in seen: return
    seen.add(id(o))
    if isinstance(o, StubBase):
        yield o
    if isinstance(o, StubBase):
        kids = [o.__dict__]
    elif isinstance(o, dict):
        kids = list(o.values())
    elif isinstance(o, (list, tuple, set, frozenset)):
        kids = list(o)
    else:
        kids = []
    for k in kids:
        if k is not None:
            yield from all_stubs(k, seen)

stubs = list(all_stubs(obj))
t2 = [s for s in stubs if s._stub_name == "_rebuild_tensor_v2"]
par = [s for s in stubs if s._stub_name == "_rebuild_parameter"]
print(f"  _rebuild_tensor_v2: {len(t2)}, _rebuild_parameter: {len(par)}")
for s in t2:
    a = s._stub_args
    # (storage, storage_offset, size, stride, requires_grad, backward_hooks[, metadata])
    rg[a[4]] += 1
    if a[5]:
        bh_nonempty += 1
print("  requires_grad values:", dict(rg))
print("  tensors with non-empty backward_hooks:", bh_nonempty)
for s in par:
    a = s._stub_args
    rg["param_requires_grad=" + repr(a[1])] += 1
print("  parameter requires_grad values:",
      {k: v for k, v in rg.items() if str(k).startswith("param")})
# tensor shapes
shapes = collections.Counter()
nbytes = 0
for s in t2:
    a = s._stub_args
    shapes[tuple(a[2])] += 1
    st = a[0]
    if isinstance(st, StubBase) and st._stub_args:
        b = st._stub_args[0]
        nbytes += len(b) if isinstance(b, (bytes, bytearray)) else 0
print("  distinct tensor shapes:", len(shapes))
print("  most common shapes:", shapes.most_common(8))
print("  total tensor storage bytes:", nbytes)

print("\n=== lineage chain ===")
cur, lvl = obj, 0
while isinstance(cur, StubBase):
    keys = [k for k in cur.__dict__.keys() if not k.startswith("_stub")]
    print(f"  L{lvl} {cur._stub_mod}.{cur._stub_name}: "
          f"format={cur.__dict__.get('format')!r} keys={keys[:14]}")
    nxt = None
    for k in ("base_state", "r26_state", "r25_state", "r24_state",
              "r23_state", "prior", "parent"):
        v = cur.__dict__.get(k)
        if isinstance(v, StubBase):
            nxt = v; break
    # also: any single StubBase child that looks like a prior state
    if nxt is None:
        for v in cur.__dict__.values():
            if isinstance(v, StubBase) and v._stub_name.endswith("State") \
               and v is not cur:
                nxt = v; break
    cur, lvl = nxt, lvl + 1
    if lvl > 8 or cur is None:
        break

print("\n=== Trace instances (r15_master_training.Trace x435) ===")
traces = [s for s in stubs
          if (s._stub_mod, s._stub_name) == ("r15_master_training", "Trace")]
t0 = traces[0]
print("  one Trace __dict__ keys:",
      [k for k in t0.__dict__.keys() if not k.startswith("_stub")][:20])
print("  Trace with _stub_appends:",
      sum(1 for s in traces if "_stub_appends" in s.__dict__))

print("\n=== EpisodicConcept x10 keys ===")
ep = [s for s in stubs if s._stub_name == "EpisodicConcept"][0]
print(" ", [k for k in ep.__dict__.keys() if not k.startswith("_stub")][:20])

print("\n=== which components own torch params ===")
owners = collections.Counter()
def owner_walk(o, path, seen=None):
    if seen is None: seen = set()
    if id(o) in seen: return
    seen.add(id(o))
    if isinstance(o, StubBase):
        if o._stub_name in ("_rebuild_parameter", "_rebuild_tensor_v2"):
            owners[path[-1] if path else "?"] += 1
            return
        name = f"{o._stub_mod}.{o._stub_name}"
        kids = [o.__dict__]
    elif isinstance(o, dict):
        name = None; kids = list(o.values())
    elif isinstance(o, (list, tuple, set)):
        name = None; kids = list(o)
    else:
        return
    for k in kids:
        if isinstance(k, dict):
            for dk, dv in k.items():
                owner_walk(dv, path + [name or str(dk)[:30]] if name else path,
                           seen)
        else:
            owner_walk(k, path + [name] if name else path, seen)
owner_walk(obj, [])
for o, c in owners.most_common(15):
    print(f"  {c:4d}  {o}")

print("\n=== top-level 'architecture' / 'evidence' peek ===")
for k in ("architecture", "evidence", "self_revision_history",
          "abstraction_policy", "visual_debate_policy"):
    v = d.get(k)
    if isinstance(v, dict):
        print(f"  {k}: dict with keys {list(v.keys())[:10]}")
    elif isinstance(v, (list, tuple)):
        print(f"  {k}: {type(v).__name__} len={len(v)}")
    else:
        print(f"  {k}: {type(v).__name__} {repr(v)[:80]}")

print("\n=== sklearn LogisticRegression owners ===")
lr_owners = collections.Counter()
def lr_walk(o, path, seen=None):
    if seen is None: seen = set()
    if id(o) in seen: return
    seen.add(id(o))
    if isinstance(o, StubBase):
        if o._stub_name == "LogisticRegression":
            lr_owners[path[-1] if path else "?"] += 1
            return
        name = f"{o._stub_mod}.{o._stub_name}"
        kids = [o.__dict__]
    elif isinstance(o, dict):
        name = None; kids = list(o.values())
    elif isinstance(o, (list, tuple, set)):
        name = None; kids = list(o)
    else:
        return
    for k in kids:
        lr_walk(k, path + [name] if name else path, seen)
lr_walk(obj, [])
for o, c in lr_owners.most_common(10):
    print(f"  {c:4d}  {o}")
