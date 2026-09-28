#!/usr/bin/env python3
"""g3_run.py — batch runner for the G3 sense binary.

Runs `sense <task> <fixture>` over a fixture tree, parses the key=value
record, and VERIFIES the hash-chained ledger line: recomputes sha256 over
the exact emitted bytes preceding the `chain=` line and compares.

Writes JSONL: one record per fixture with path, task, sig, meta, graph,
judgment, disposition, confidence, ops, chain_ok, truth, correct.
"""
import os, sys, json, subprocess, hashlib

def parse_record(out):
    d = {}
    for line in out.split("\n"):
        if "=" in line:
            k, v = line.split("=", 1)
            d[k.strip()] = v.strip()
    return d

def verify_chain(raw):
    """raw: full stdout bytes. chain = sha256 of bytes before the chain= line."""
    lines = raw.split(b"\n")
    ci = next(i for i, l in enumerate(lines) if l.startswith(b"chain="))
    body = b"\n".join(lines[:ci]) + b"\n"
    claimed = lines[ci].split(b"=", 1)[1].decode().strip()
    return hashlib.sha256(body).hexdigest() == claimed

def run_tree(binary, fixture_root, out_path, flat_variant=None):
    recs = []
    n_ok = n_bad = 0
    for taskdir in sorted(os.listdir(fixture_root)):
        tdir = os.path.join(fixture_root, taskdir)
        if not os.path.isdir(tdir):
            continue
        # task name: map t1_colordisc -> colordisc etc.
        task = taskdir[3:] if len(taskdir) > 3 and taskdir[2] == "_" else taskdir
        variants = []
        if flat_variant is not None:
            variants = [(flat_variant, tdir)]
        else:
            for variant in sorted(os.listdir(tdir)):
                vdir = os.path.join(tdir, variant)
                if os.path.isdir(vdir):
                    variants.append((variant, vdir))
        for variant, vdir in variants:
            for name in sorted(os.listdir(vdir)):
                if name.endswith(".truth"):
                    continue
                p = os.path.join(vdir, name)
                if not os.path.isfile(p):
                    continue
                r = subprocess.run([binary, task, p], capture_output=True)
                raw = r.stdout
                kv = parse_record(raw.decode(errors="replace"))
                chain_ok = False
                try:
                    chain_ok = verify_chain(raw)
                except Exception:
                    chain_ok = False
                if chain_ok:
                    n_ok += 1
                else:
                    n_bad += 1
                truth = None
                tp = p + ".truth"
                if os.path.exists(tp):
                    truth = open(tp).read().strip().split("=", 1)[-1]
                rec = {
                    "path": p, "task": task, "variant": variant,
                    "sig": kv.get("sig"), "meta": kv.get("meta"),
                    "graph": kv.get("graph"), "judgment": kv.get("judgment"),
                    "disposition": kv.get("disposition"),
                    "confidence": kv.get("confidence"), "ops": kv.get("ops"),
                    "chain_ok": chain_ok, "truth": truth,
                    "correct": (kv.get("judgment") == truth) if truth else None,
                    "rc": r.returncode,
                }
                recs.append(rec)
    with open(out_path, "w") as f:
        for rec in recs:
            f.write(json.dumps(rec) + "\n")
    print("ran %d  chain_ok=%d chain_bad=%d -> %s" % (len(recs), n_ok, n_bad, out_path))

if __name__ == "__main__":
    binary, fixture_root, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    flat = sys.argv[4] if len(sys.argv) > 4 else None
    run_tree(binary, fixture_root, out_path, flat)
