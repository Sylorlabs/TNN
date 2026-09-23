#!/usr/bin/env python3
"""Memory-bounded batched cleaning for large 10GB sources (Phase 2).

Problem: clean2.clean_tree accumulates all_recs + cleaned_concat in memory.
For math (5.8GB raw) / gutenberg / phys this OOMs on the 8GB shared VM
(phys was SIGKILLed at ~1GB RSS; gb_B hit 1.16GB and climbing).

Approach: partition the source's files (in clean_tree's R0 order) into
subsets of N files; run the UNMODIFIED clean2.clean_tree per subset via a
symlink tree (preserving <source>/<relpath>); k-way merge the subset
facts.dat shards with merge_facts (streaming, memory-bounded).

Byte-identity proof: clean_tree does a STABLE sort of all recs by key bytes
over recs in R0 file order. Partitioning preserves R0 order across subsets;
each subset facts.dat is sorted; merge_facts merges on (key_bytes,
shard_index) which reproduces the stable-sort order for equal keys.
Therefore merged facts.dat == monolithic clean_tree facts.dat, byte for byte.
(The per-subset MANIFESTs are kept; a combined MANIFEST.json is written.)

Zero RNG. Deterministic. Python glue only; the cleaner itself is untouched.

Usage: clean_batched.py <raw_dir> <out_dir> <files_per_subset>
"""
import hashlib
import json
import os
import shutil
import sys

TEACH = "/home/hatch/workspace/tnn-lab/knowledge/ingest_10gb/teach"
sys.path.insert(0, TEACH)
import clean2
import merge_facts


def r0_files(raw_dir):
    """Files in clean_tree's R0 order: for source in SOURCES, sorted relpaths."""
    out = []
    for source in clean2.SOURCES:
        sdir = os.path.join(raw_dir, source)
        if not os.path.isdir(sdir):
            continue
        rels = []
        for root, _ds, fs in os.walk(sdir):
            for fn in fs:
                rels.append(os.path.relpath(os.path.join(root, fn), sdir))
        for rel in sorted(rels):
            out.append((source, rel))
    return out


def main():
    raw_dir, out_dir, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
    raw_dir = os.path.abspath(raw_dir)
    out_dir = os.path.abspath(out_dir)
    files = r0_files(raw_dir)
    print(f"[batched] {len(files)} files, {n} per subset", flush=True)
    os.makedirs(out_dir, exist_ok=True)
    # subset-size consistency gate: a resume with a different n would merge
    # shards from inconsistent groupings (wrong totals, broken byte-identity).
    nsub = (len(files) + n - 1) // n
    params_path = os.path.join(out_dir, ".batched_params.json")
    if os.path.exists(params_path):
        prev = json.load(open(params_path))
        if prev.get("files_per_subset") != n or prev.get("n_files") != len(files):
            raise SystemExit(
                f"[batched] REFUSING resume: out_dir was built with "
                f"files_per_subset={prev.get('files_per_subset')} "
                f"n_files={prev.get('n_files')}, now n={n} "
                f"n_files={len(files)}. Wipe {out_dir} or rerun with the "
                f"original n.")
    else:
        json.dump({"files_per_subset": n, "n_files": len(files),
                   "nsub": nsub},
                  open(params_path, "w"), sort_keys=True)
    shard_paths = []
    for si in range(nsub):
        group = files[si * n:(si + 1) * n]
        sub_raw = os.path.join(out_dir, f"_subraw{si:03d}")
        sub_out = os.path.join(out_dir, f"sub{si:03d}")
        # resume: skip subsets with a completed facts.dat
        done_marker = os.path.join(sub_out, "facts.dat")
        if os.path.exists(done_marker) and os.path.getsize(done_marker) > 0:
            m = json.load(open(os.path.join(sub_out, "MANIFEST.json")))
            print(f"[batched] sub{si:03d}: resume-skip ({m['total_facts']} facts)",
                  flush=True)
            shard_paths.append(done_marker)
            continue
        # rebuild symlink tree fresh: wipe the whole _subraw dir first.
        # Stale symlinks from a run with DIFFERENT subset sizing persist
        # outside the current group (the loop below only touches current-group
        # links) -> dangling FileNotFoundError or duplicated chunks.
        shutil.rmtree(sub_raw, ignore_errors=True)
        for source, rel in group:
            link = os.path.join(sub_raw, source, rel)
            os.makedirs(os.path.dirname(link), exist_ok=True)
            target = os.path.join(raw_dir, source, rel)
            os.symlink(target, link)
        # clean unmodified
        m = clean2.clean_tree(sub_raw, sub_out)
        print(f"[batched] sub{si:03d}: {m['total_facts']} facts", flush=True)
        shard_paths.append(os.path.join(sub_out, "facts.dat"))
    # merge subsets -> out_dir/facts.dat
    out_dat = os.path.join(out_dir, "facts.dat")
    sys.argv = ["merge_facts.py", out_dat] + shard_paths
    merge_facts.main()
    # combined manifest
    total = 0
    stats = {}
    for sp in shard_paths:
        mj = os.path.join(os.path.dirname(sp), "MANIFEST.json")
        m = json.load(open(mj))
        total += m["total_facts"]
        for src, st in m["sources"].items():
            d = stats.setdefault(src, {"files": 0, "input_bytes": 0,
                                       "cleaned_bytes": 0, "facts": 0})
            for k in d:
                d[k] += st[k]
    sha = open(out_dat + ".sha256").read().split()[0]
    manifest = {"spec": clean2.SPEC_VERSION + "+batched",
                "sources": stats, "total_facts": total,
                "facts_dat_sha256": sha,
                "subsets": nsub, "files_per_subset": n,
                "byte_identity_note": "merged facts.dat is byte-identical to a "
                "monolithic clean_tree run (stable sort + (key,shard) merge)"}
    with open(os.path.join(out_dir, "MANIFEST.json"), "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"[batched] DONE total_facts={total} sha={sha[:16]}", flush=True)


if __name__ == "__main__":
    main()
