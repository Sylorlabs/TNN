#!/usr/bin/env python3
"""gen_fixtures.py — H6-R2 fork W (WITNESS), FROZEN with the fork prereg.

Extracts the ```spec block from CORPORA.md, validates it structurally,
and emits w_fix.zag: the frozen fixture blob as chunked Zag string
literals. The Zag binary re-parses the blob at startup (w_parse.zag),
so CORPORA.md is the single source of truth.

Usage: gen_fixtures.py CORPORA.md w_fix.zag
Deterministic: byte-identical output for byte-identical input.
"""
import hashlib
import re
import sys

CORPORA = ("CONFAB", "GOLD", "SMUGGLE", "PARA", "ALIBI", "GENAUTH",
           "HALPTR", "HELD")
OPS = ("percept", "recall", "pattern", "infer", "assume", "cohere")
ROLES = ("E", "R", "A", "Q")
DANGLING_OK = {0, 777, 888, 999}  # deliberately fabricated store ids
CHUNK = 6000


def fail(msg):
    raise SystemExit("gen_fixtures: VALIDATION FAIL: " + msg)


def main():
    src_path, out_path = sys.argv[1], sys.argv[2]
    text = open(src_path).read()
    m = re.search(r"```spec\n(.*?)```", text, re.S)
    if not m:
        fail("no ```spec block in " + src_path)
    spec = m.group(1)
    if not spec.endswith("\n"):
        spec += "\n"
    lines = spec.split("\n")

    store_ids = set()
    syn_from, ant_w, num_s, stop_w, feat_w, rule_n = (set() for _ in range(6))
    fids = set()
    cur = None  # current fixture dict
    n_fixtures = 0

    def need_fix(ln, what):
        if cur is None:
            fail("line %d: %s outside FIX" % (ln, what))

    for ln, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        tag = parts[0]
        if tag == "S":
            # S <id> <W|G> <ep> <etype> <content> || <feats>
            if "||" not in line:
                fail("line %d: S without ||" % ln)
            head, feats = line.split("||", 1)
            h = head.split()
            if len(h) < 6 or h[2] not in ("W", "G") or h[4] not in \
                    ("E", "R", "A", "Q", "F"):
                fail("line %d: bad S head" % ln)
            sid = int(h[1])
            if sid in store_ids:
                fail("line %d: dup store id %d" % (ln, sid))
            store_ids.add(sid)
            content = " ".join(h[5:])
            if not content:
                fail("line %d: empty S content" % ln)
        elif tag == "SYN":
            if len(parts) != 3:
                fail("line %d: bad SYN" % ln)
            syn_from.add(parts[1])
        elif tag == "ANT":
            if len(parts) != 3:
                fail("line %d: bad ANT" % ln)
            ant_w.add(parts[1])
        elif tag == "NUM":
            if len(parts) != 3:
                fail("line %d: bad NUM" % ln)
            num_s.add(parts[1])
        elif tag == "STOP":
            if len(parts) != 2:
                fail("line %d: bad STOP" % ln)
            stop_w.add(parts[1])
        elif tag == "FEAT":
            if len(parts) != 3:
                fail("line %d: bad FEAT" % ln)
            feat_w.add(parts[1])
        elif tag == "RULE":
            if len(parts) != 4:
                fail("line %d: bad RULE" % ln)
            rule_n.add(parts[1])
        elif tag == "FIX":
            if len(parts) != 7:
                fail("line %d: bad FIX" % ln)
            fid, corpus, marker = parts[1], parts[2], parts[3]
            if fid in fids:
                fail("line %d: dup fid %s" % (ln, fid))
            if corpus not in CORPORA:
                fail("line %d: bad corpus %s" % (ln, corpus))
            if marker not in ("F", "P"):
                fail("line %d: bad marker" % ln)
            int(parts[4]); int(parts[5]); int(parts[6])
            fids.add(fid)
            cur = {"fid": fid, "corpus": corpus, "text": None,
                   "atoms": [], "steps": [], "pair": None,
                   "ntok": 0}
            n_fixtures += 1
        elif tag == "PAIR":
            need_fix(ln, "PAIR")
            if len(parts) != 4 or parts[2] not in ("A", "B") or \
                    parts[3] not in ("SAME", "FLIP", "SCOPE"):
                fail("line %d: bad PAIR" % ln)
            if cur["corpus"] not in ("PARA", "HELD"):
                fail("line %d: PAIR outside PARA/HELD" % ln)
            cur["pair"] = (parts[1], parts[2], parts[3])
        elif tag == "TEXT":
            need_fix(ln, "TEXT")
            t = line[5:]
            if cur["text"] is not None:
                fail("line %d: dup TEXT" % ln)
            cur["text"] = t
            cur["ntok"] = len(t.split())
        elif tag == "ATOM":
            need_fix(ln, "ATOM")
            if len(parts) != 6 or parts[1] not in ROLES or \
                    parts[5] not in ("G", "C"):
                fail("line %d: bad ATOM" % ln)
            if " " in parts[2] or not parts[2]:
                fail("line %d: ATOM label has space" % ln)
            t0, t1 = int(parts[3]), int(parts[4])
            if not (0 <= t0 < t1 <= cur["ntok"]):
                fail("line %d: ATOM span [%d,%d) vs ntok %d" %
                     (ln, t0, t1, cur["ntok"]))
            cur["atoms"].append(parts[1:])
        elif tag == "STEP":
            need_fix(ln, "STEP")
            if len(parts) < 3 or parts[1] not in OPS:
                fail("line %d: bad STEP" % ln)
            outs = [int(x) for x in parts[2].split(",")]
            if any(o < 0 or o >= len(cur["atoms"]) for o in outs):
                fail("line %d: STEP outs out of range" % ln)
            kw = {}
            for p in parts[3:]:
                if "=" not in p:
                    fail("line %d: bad STEP kw %s" % (ln, p))
                k, v = p.split("=", 1)
                kw[k] = v
            if "prem" in kw:
                prems = [int(x) for x in kw["prem"].split(",")]
                if any(p < 0 or p >= len(cur["atoms"]) for p in prems):
                    fail("line %d: STEP prem out of range" % ln)
                if any(p >= min(outs) for p in prems):
                    fail("line %d: premise not before conclusion" % ln)
            if "rule" in kw and kw["rule"] not in rule_n \
                    and kw["rule"] != "co-occur":
                # co-occur is the deliberate unsound rule used by confabs
                fail("line %d: unknown rule %s" % (ln, kw["rule"]))
            if "ov" in kw:
                int(kw["ov"])
            if "dist" in kw and kw["dist"] not in ("0", "1"):
                fail("line %d: bad dist" % ln)
            cur["steps"].append({"outs": outs, "n_in": 0})
        elif tag == "IN":
            need_fix(ln, "IN")
            if not cur["steps"]:
                fail("line %d: IN before STEP" % ln)
            if len(parts) < 3:
                fail("line %d: bad IN" % ln)
            sid = int(parts[1]); int(parts[2])
            if sid not in store_ids and sid not in DANGLING_OK:
                fail("line %d: IN unknown store id %d" % (ln, sid))
            cur["steps"][-1]["n_in"] += 1
        else:
            fail("line %d: unknown tag %s" % (ln, tag))

    digest = hashlib.sha256(spec.encode()).hexdigest()
    # chunk on line boundaries
    chunks, cur_c = [], []
    cur_n = 0
    for raw in lines:
        bl = len(raw) + 1
        if cur_n + bl > CHUNK and cur_c:
            chunks.append("\n".join(cur_c) + "\n")
            cur_c, cur_n = [], 0
        cur_c.append(raw)
        cur_n += bl
    if cur_c:
        chunks.append("\n".join(cur_c) + "\n")

    def zesc(s):
        return s.replace("\\", "\\\\").replace('"', '\\"') \
                .replace("\n", "\\n")

    with open(out_path, "w") as f:
        f.write("// GENERATED by gen_fixtures.py from CORPORA.md — DO NOT EDIT\n")
        f.write("// spec sha256: %s\n" % digest)
        f.write("// fixtures: %d  store entries: %d\n" %
                (n_fixtures, len(store_ids)))
        f.write("fn fx_nchunks() i64 { return %d; }\n" % len(chunks))
        f.write("fn fx_chunk(i:i64) []u8 {\n")
        for i, ch in enumerate(chunks):
            f.write('    if (i == %d) { return "%s"; }\n' % (i, zesc(ch)))
        f.write('    return "";\n}\n')
    print("ok: %d fixtures, %d store entries, %d chunks, sha %s..."
          % (n_fixtures, len(store_ids), len(chunks), digest[:16]))


if __name__ == "__main__":
    main()
