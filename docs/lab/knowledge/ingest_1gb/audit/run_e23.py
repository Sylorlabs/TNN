#!/usr/bin/env python3
"""Corrected slot-based E2/E3 on run/store_audit_e23.
E2: 100 Zag revises (installed slot IDs) + query verify exact text/ID.
    1,000 neighbors via bquery, verify unchanged.
E3: 100 Zag deletes + query verify DELETED id.
    1,000 neighbors via bquery, verify unchanged.
Event counts verified at the end.
Deterministic. Logs to e23_run.log.
"""
import subprocess, os, sys, struct, hashlib

BASE = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb")
AUD = os.path.join(BASE, "audit")
BIN = os.path.join(AUD, "ingest_bin_audit")
STORE = os.path.join(BASE, "run", "store_audit_e23")
LOG = open(os.path.join(AUD, "e23_run.log"), "w")

def log(s):
    print(s, flush=True)
    LOG.write(s + "\n"); LOG.flush()

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout.strip(), r.stderr.strip(), r.returncode

def load_tsv(path):
    rows = []
    for line in open(path):
        line = line.rstrip("\n")
        if line:
            rows.append(line.split("\t"))
    return rows

def main():
    # ---- E2: revises ----
    targets = load_tsv(os.path.join(AUD, "e2_targets.tsv"))
    assert len(targets) == 100
    ok = 0
    for i, (slot, pos, key, oldsha, newtext) in enumerate(targets):
        tp = "/tmp/e23_newtext.txt"
        with open(tp, "w") as f:
            f.write(newtext)
        out, err, rc = run([BIN, "revise", STORE, slot, tp])
        if rc != 0 or not out.startswith("revised id=%s " % slot):
            log("E2 revise %s FAILED rc=%d out=%s err=%s" % (slot, rc, out[:100], err[:100]))
            continue
        out, err, rc = run([BIN, "query", STORE, key])
        # expect: FOUND id=<slot> tlen=...\n<newtext>
        lines = out.split("\n")
        if (rc == 0 and lines and lines[0] == "FOUND id=%s tlen=%d" % (slot, len(newtext))
                and len(lines) > 1 and lines[1] == newtext):
            ok += 1
        else:
            log("E2 verify %s FAILED: %s" % (slot, out[:120]))
        if (i+1) % 20 == 0:
            log("E2 progress %d/100 ok=%d" % (i+1, ok))
    log("E2: %d/100 revisions verified (exact text+ID)" % ok)
    e2_ok = ok

    # ---- E2 neighbors via bquery ----
    neigh = [r for r in load_tsv(os.path.join(AUD, "neighbors.tsv")) if r[1] == "e2"]
    assert len(neigh) == 1000, len(neigh)
    texts = {}
    for r in load_tsv(os.path.join(AUD, "neighbor_texts.tsv")):
        texts[int(r[0])] = r[2]
    keys_path = "/tmp/e23_e2keys.bin"
    with open(keys_path, "wb") as f:
        for ts, phase, nb, key, sha in neigh:
            kb = key.encode()
            f.write(struct.pack(">H", len(kb)) + kb)
    res_path = "/tmp/e23_e2res.bin"
    out, err, rc = run([BIN, "bquery", STORE, keys_path, res_path])
    assert rc == 0, (out, err)
    data = open(res_path, "rb").read()
    p = 0
    nok = 0
    for ts, phase, nb, key, sha in neigh:
        status = data[p]; fid = struct.unpack("<i", data[p+1:p+5])[0]
        tlen = struct.unpack("<i", data[p+5:p+9])[0]
        txt = data[p+9:p+9+tlen]; p += 9 + tlen
        exp_txt = texts[int(nb)]
        if status == 0 and fid == int(nb) and txt.decode() == exp_txt:
            nok += 1
        else:
            log("E2 neighbor %s MISMATCH status=%d id=%d" % (nb, status, fid))
    log("E2 neighbors: %d/1000 unchanged" % nok)

    # ---- E3: deletes ----
    targets = load_tsv(os.path.join(AUD, "e3_targets.tsv"))
    assert len(targets) == 100
    ok = 0
    for i, (slot, pos, key, oldsha) in enumerate(targets):
        out, err, rc = run([BIN, "delete", STORE, slot])
        if rc != 0 or not out.startswith("deleted id=%s " % slot):
            log("E3 delete %s FAILED rc=%d out=%s err=%s" % (slot, rc, out[:100], err[:100]))
            continue
        out, err, rc = run([BIN, "query", STORE, key])
        if rc == 0 and out.split("\n")[0] == "DELETED id=%s" % slot:
            ok += 1
        else:
            log("E3 verify %s FAILED: %s" % (slot, out[:120]))
        if (i+1) % 20 == 0:
            log("E3 progress %d/100 ok=%d" % (i+1, ok))
    log("E3: %d/100 deletions verified (DELETED id)" % ok)
    e3_ok = ok

    # ---- E3 neighbors via bquery ----
    neigh = [r for r in load_tsv(os.path.join(AUD, "neighbors.tsv")) if r[1] == "e3"]
    assert len(neigh) == 1000, len(neigh)
    keys_path = "/tmp/e23_e3keys.bin"
    with open(keys_path, "wb") as f:
        for ts, phase, nb, key, sha in neigh:
            kb = key.encode()
            f.write(struct.pack(">H", len(kb)) + kb)
    res_path = "/tmp/e23_e3res.bin"
    out, err, rc = run([BIN, "bquery", STORE, keys_path, res_path])
    assert rc == 0, (out, err)
    data = open(res_path, "rb").read()
    p = 0
    nok = 0
    for ts, phase, nb, key, sha in neigh:
        status = data[p]; fid = struct.unpack("<i", data[p+1:p+5])[0]
        tlen = struct.unpack("<i", data[p+5:p+9])[0]
        txt = data[p+9:p+9+tlen]; p += 9 + tlen
        exp_txt = texts[int(nb)]
        if status == 0 and fid == int(nb) and txt.decode() == exp_txt:
            nok += 1
        else:
            log("E3 neighbor %s MISMATCH status=%d id=%d" % (nb, status, fid))
    log("E3 neighbors: %d/1000 unchanged" % nok)

    # ---- event counts ----
    # read events_n from store.dat: parse header, skip to events section
    d = open(os.path.join(STORE, "store.dat"), "rb").read()
    nsealed = struct.unpack("<i", d[16:20])[0]
    nchunks = struct.unpack("<i", d[20:24])[0]
    p = 28 + nchunks
    for c in range(nsealed):
        ln = struct.unpack("<i", d[p:p+4])[0]
        p += 4 + ln
    p += nsealed * 32
    evn = struct.unpack("<i", d[p:p+4])[0]
    p += 4
    tags = {}
    for i in range(evn):
        tag = d[p]
        tags[tag] = tags.get(tag, 0) + 1
        p += 16
    log("EVENTS total=%d tags=%s" % (evn, sorted(tags.items())))
    log("E2E3 SUMMARY e2_ok=%d e3_ok=%d" % (e2_ok, e3_ok))
    LOG.close()

if __name__ == "__main__":
    main()
