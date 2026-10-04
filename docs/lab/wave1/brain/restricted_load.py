#!/usr/bin/env python3
"""Restricted unpickler for the R27 accepted brain state.

Safety: never unpickles with real classes. find_class() maps every
(module, name) to a generated stub class that records its construction
arguments but executes no domain code. Used for white-box schema mapping
of parent-r27-accepted-state.pkl.
"""
import pickle, io, sys, collections, json

CALL_LOG = []          # (module, name, kind, args_summary)
CLASS_CACHE = {}

class StubBase:
    def __init__(self, *args, **kwargs):
        self._stub_args = args
        self._stub_kwargs = kwargs
    def __setstate__(self, state):
        # Permissive: record the raw build state, then apply dict part.
        self._stub_build_state = state
        d = state[0] if isinstance(state, tuple) else state
        if isinstance(d, dict):
            self.__dict__.update(d)
        if isinstance(state, tuple) and len(state) == 2:
            self._stub_slotstate = state[1]
    def __repr__(self):
        return f"<stub {self._stub_mod}.{self._stub_name}>"
    # container-protocol shims: pickle's 5-tuple REDUCE form emits
    # APPEND(S) / SETITEM(S) opcodes against the fresh instance.
    def append(self, x):
        self.__dict__.setdefault("_stub_appends", []).append(x)
    def extend(self, xs):
        self.__dict__.setdefault("_stub_appends", []).extend(xs)
    def __setitem__(self, k, v):
        self.__dict__.setdefault("_stub_setitems", {})[k] = v

def _summarize_args(args, limit=3):
    out = []
    for a in args[:limit]:
        if isinstance(a, (bytes, bytearray)):
            out.append(f"<bytes {len(a)}>")
        elif isinstance(a, str) and len(a) > 60:
            out.append(f"<str {len(a)} chars: {a[:40]!r}...>")
        elif isinstance(a, (list, tuple)) and len(a) > 8:
            out.append(f"<{type(a).__name__} len={len(a)}>")
        else:
            out.append(repr(a)[:80])
    if len(args) > limit:
        out.append(f"... +{len(args)-limit} more")
    return out

def find_class(module, name):
    key = (module, name)
    if key not in CLASS_CACHE:
        def __init__(self, *args, **kwargs):
            StubBase.__init__(self, *args, **kwargs)
            CALL_LOG.append((module, name, "REDUCE-call",
                             _summarize_args(args)))
        cls = type(f"Stub_{module}_{name}".replace(".", "_"),
                   (StubBase,),
                   {"__init__": __init__,
                    "_stub_mod": module, "_stub_name": name,
                    "__module__": "stub"})
        CLASS_CACHE[key] = cls
    return CLASS_CACHE[key]

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        return find_class(module, name)

def load(path):
    with open(path, "rb") as f:
        return RestrictedUnpickler(f).load()

# ---------------- graph walk ----------------
def walk(obj, depth=0, seen=None, stats=None):
    if seen is None:
        seen = set()
        stats = {"nodes": 0, "bytes_blobs": 0, "blob_bytes": 0,
                 "stub_classes": collections.Counter(),
                 "max_depth": 0, "key_names": collections.Counter()}
    oid = id(obj)
    if oid in seen:
        return stats
    seen.add(oid)
    stats["nodes"] += 1
    stats["max_depth"] = max(stats["max_depth"], depth)
    if isinstance(obj, StubBase):
        stats["stub_classes"][(obj._stub_mod, obj._stub_name)] += 1
        kids = [obj.__dict__]
    elif isinstance(obj, dict):
        for k in obj.keys():
            stats["key_names"][str(k)[:60]] += 1
        kids = list(obj.values())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        kids = list(obj)
    elif isinstance(obj, (bytes, bytearray)):
        stats["bytes_blobs"] += 1
        stats["blob_bytes"] += len(obj)
        kids = []
    else:
        kids = [getattr(obj, "__dict__", None)]
        kids = [k for k in kids if k]
    for k in kids:
        if k is not None:
            walk(k, depth + 1, seen, stats)
    return stats

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else \
        "/tmp/tnn-lab/brain/parent-r27-accepted-state.pkl"
    obj = load(path)
    print("top object:", repr(obj))
    print("top __dict__ keys:", list(obj.__dict__.keys()))
    stats = walk(obj)
    print("\nnodes:", stats["nodes"], "max_depth:", stats["max_depth"])
    print("bytes blobs:", stats["bytes_blobs"],
          "total blob bytes:", stats["blob_bytes"])
    print("\nstub class instances:")
    for (m, n), c in stats["stub_classes"].most_common():
        print(f"  {c:5d}  {m}.{n}")
    json.dump({"top_keys": list(obj.__dict__.keys()),
               "nodes": stats["nodes"], "max_depth": stats["max_depth"],
               "bytes_blobs": stats["bytes_blobs"],
               "blob_bytes": stats["blob_bytes"],
               "stub_classes": [[m, n, c] for (m, n), c in
                                stats["stub_classes"].most_common()],
               "top_key_names": stats["key_names"].most_common(60)},
              open("/tmp/tnn-lab/brain/schema_stats.json", "w"), indent=1)
    # tensor requires_grad evidence
    print("\n--- tensor/parameter construction calls ---")
    for mod, name, kind, args in CALL_LOG:
        if "rebuild" in name or "_load_from_bytes" in name or \
           "_frombuffer" in name or "dtype" in name:
            print(f"  {mod}.{name} {args}")

if __name__ == "__main__":
    main()
