#!/usr/bin/env python3
"""Crew C battery runner. Deterministic; no RNG.

Reads TEST_MANIFEST_C.json; renders with ./control (pure Zag binary);
every render runs 3x and SHAs must match byte-identically; scores with the
frozen scorer_c.py; logs every argv handed to the binary (prereg 5.2).

Outputs in workdir: RESULTS_C.json, ARGV_LOG.jsonl, SHA_LOG.txt,
DITHER_C.json, STATS_C.json.
"""
import hashlib
import json
import os
import struct
import subprocess
import sys

WORKDIR = sys.argv[1] if len(sys.argv) > 1 else "test_wavs"
HERE = os.path.dirname(os.path.abspath(__file__))
CONTROL = os.path.join(HERE, "control")
SCORER = os.path.join(HERE, "scorer_c.py")
MANIFEST = json.load(open(os.path.join(HERE, "TEST_MANIFEST_C.json")))

os.makedirs(WORKDIR, exist_ok=True)
argv_log = open(os.path.join(WORKDIR, "ARGV_LOG.jsonl"), "w")
sha_log = open(os.path.join(WORKDIR, "SHA_LOG.txt"), "w")
results = []


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def render(descriptor, tag, runs=3):
    """Render `runs` times; assert byte-identical; return (path, sha)."""
    paths = []
    for k in range(runs):
        p = os.path.join(WORKDIR, f"{tag}_r{k}.wav")
        argv_log.write(json.dumps(
            {"wav": p, "argv": [CONTROL, p, descriptor]}) + "\n")
        r = subprocess.run([CONTROL, p, descriptor], capture_output=True)
        if r.returncode != 0:
            raise RuntimeError(f"control rc={r.returncode} desc={descriptor}")
        paths.append(p)
    shas = [sha256_file(p) for p in paths]
    if not (shas[0] == shas[1] == shas[2]):
        raise RuntimeError(f"NON-DETERMINISTIC render: {tag} {shas}")
    sha_log.write(f"{shas[0]}  {tag}  desc={descriptor}\n")
    sha_log.flush()
    for p in paths[1:]:
        os.unlink(p)
    return paths[0], shas[0]


def score(wav, descriptor):
    r = subprocess.run([sys.executable, SCORER, wav, descriptor],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"scorer failed: {r.stderr[:300]} desc={descriptor}")
    return json.loads(r.stdout)


def run_axis(axis, items, c1_items):
    for idx, true_desc in enumerate(items):
        for arm, desc in (("intent", true_desc),
                          ("C0", "C0"),
                          ("C1", c1_items[idx])):
            tag = f"{axis}{idx:02d}_{arm}"
            wav, sha = render(desc, tag)
            s = score(wav, true_desc)
            results.append({
                "axis": axis, "idx": idx, "arm": arm,
                "true_descriptor": true_desc, "render_descriptor": desc,
                "sha256": sha, "hit": s["hit"],
                "verdicts": s["verdicts"], "measurements": s["measurements"],
            })
            os.unlink(wav)
            print(f"{tag}: hit={s['hit']} {true_desc}", flush=True)


def run_extra(name, items):
    for idx, desc in enumerate(items):
        tag = f"{name}{idx:02d}_intent"
        wav, sha = render(desc, tag)
        s = score(wav, desc)
        results.append({
            "axis": name, "idx": idx, "arm": "intent",
            "true_descriptor": desc, "render_descriptor": desc,
            "sha256": sha, "hit": s["hit"],
            "verdicts": s["verdicts"], "measurements": s["measurements"],
        })
        os.unlink(wav)
        print(f"{tag}: hit={s['hit']} {desc}", flush=True)


def main():
    m = MANIFEST
    run_axis("P", m["pitch"]["targets"], m["c1_derangement"]["pitch_deranged"])
    run_axis("E", m["envelope"]["targets"], m["c1_derangement"]["env_deranged"])
    run_axis("R", m["rhythm"]["targets"], m["c1_derangement"]["rhy_deranged"])
    run_extra("X", m["compositionality_cr1"]["targets"])   # C-R1
    run_extra("S", m["prosody_cr2"]["targets"])            # C-R2
    argv_log.close()
    sha_log.close()
    with open(os.path.join(WORKDIR, "RESULTS_C.json"), "w") as f:
        json.dump(results, f, indent=1)
    print(f"done: {len(results)} scored renders", flush=True)


if __name__ == "__main__":
    main()
