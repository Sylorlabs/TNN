#!/usr/bin/env python3
"""R2-9 mechanical battery verification (KB-E1/E2/E5, B6).
Compares batch outputs across runs. Pure analysis glue.
"""
import hashlib, os, sys, struct

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def load_percepts(p):
    rows = {}
    with open(p) as f:
        header = f.readline()
        for line in f:
            q = line.rstrip("\n").split("\t")
            # trial, task, fixture, judgment, conf, disp, ops, nsel, sel, claim, warrant, ledger
            rows[q[0]] = q
    return rows

def main():
    base = sys.argv[1]  # dir containing run1_emit, run2_emit, run3_emit, run1_noemit
    r1 = load_percepts(os.path.join(base, "run1_emit", "percepts.tsv"))
    r2 = load_percepts(os.path.join(base, "run2_emit", "percepts.tsv"))
    r3 = load_percepts(os.path.join(base, "run3_emit", "percepts.tsv"))
    rn = load_percepts(os.path.join(base, "run1_noemit", "percepts.tsv"))
    print(f"trials: run1={len(r1)} run2={len(r2)} run3={len(r3)} noemit={len(rn)}")

    # B6: 3 emit runs byte-identical (percepts incl. ledger hashes)
    b6 = True
    for tid, row in r1.items():
        if r2.get(tid) != row or r3.get(tid) != row:
            print(f"B6 FAIL: {tid} differs across runs")
            b6 = False
            break
    print(f"B6 three-run byte-identical: {'PASS' if b6 else 'FAIL'}")

    # KB-E5: emit vs noemit — percepts/dispositions identical (exclude ledger col 11)
    e5 = True
    for tid, row in r1.items():
        nrow = rn.get(tid)
        if nrow is None:
            print(f"KB-E5 FAIL: {tid} missing in noemit"); e5 = False; break
        if row[:11] != nrow[:11]:
            print(f"KB-E5 FAIL: {tid} percept differs emit vs noemit")
            e5 = False
            break
    print(f"KB-E5 emit/noemit percepts identical: {'PASS' if e5 else 'FAIL'}")

    # KB-E1: every artifact byte-identical to cited source span/region
    adir = os.path.join(base, "run1_emit", "artifacts")
    e1 = True
    n_art = 0
    for tid, row in r1.items():
        fixture, nsel, sel = row[2], int(row[7]), row[8]
        src = open(fixture, "rb").read()
        for k in range(nsel):
            n_art += 1
            spec = sel.split(";")[k]
            kind, rest = spec.split(":")
            vals = [int(x) for x in rest.split(",")]
            kind = int(kind)
            ap = os.path.join(adir, f"{tid}.e{k}.{'aud' if kind==0 else 'img' if kind==1 else 'vid'}")
            if not os.path.exists(ap):
                print(f"KB-E1 FAIL: missing artifact {ap}"); e1 = False; break
            art = open(ap, "rb").read()
            if kind == 0:
                a, b = vals[0], vals[1]
                rate, cnt = struct.unpack("<II", art[:8])
                exp = src[a:b]
                if art[8:] != exp:
                    print(f"KB-E1 FAIL: {ap} audio bytes differ"); e1 = False; break
            elif kind == 1:
                x, y, w, h = vals[0], vals[1], vals[2], vals[3]
                sw = struct.unpack("<I", src[:4])[0]
                aw, ah = struct.unpack("<II", art[:8])
                if (aw, ah) != (w, h):
                    print(f"KB-E1 FAIL: {ap} dims"); e1 = False; break
                ok = True
                for yy in range(h):
                    for xx in range(w):
                        so = 8 + ((y+yy)*sw + (x+xx))*3
                        do = 8 + (yy*w + xx)*3
                        if art[do:do+3] != src[so:so+3]:
                            ok = False; break
                    if not ok: break
                if not ok:
                    print(f"KB-E1 FAIL: {ap} pixels differ"); e1 = False; break
            else:
                x, y, w, h, f0, f1 = vals[0], vals[1], vals[2], vals[3], vals[4], vals[5]
                sw = struct.unpack("<I", src[4:8])[0]
                sh = struct.unpack("<I", src[8:12])[0]
                anf, aw, ah = struct.unpack("<III", art[:12])
                if (anf, aw, ah) != (f1-f0+1, w, h):
                    print(f"KB-E1 FAIL: {ap} vid dims"); e1 = False; break
                ok = True
                for ff in range(f0, f1+1):
                    for yy in range(h):
                        for xx in range(w):
                            so = 12 + (ff*sw*sh + (y+yy)*sw + (x+xx))*3
                            do = 12 + ((ff-f0)*w*h + yy*w + xx)*3
                            if art[do:do+3] != src[so:so+3]:
                                ok = False; break
                        if not ok: break
                    if not ok: break
                if not ok:
                    print(f"KB-E1 FAIL: {ap} vid pixels differ"); e1 = False; break
        if not e1:
            break
    print(f"KB-E1 artifacts byte-identical to source: {'PASS' if e1 else 'FAIL'} ({n_art} artifacts)")

    # KB-E1 rerun: artifacts identical across 3 runs
    e1r = True
    for d in ["run2_emit", "run3_emit"]:
        ad2 = os.path.join(base, d, "artifacts")
        for fn in os.listdir(adir):
            if sha(os.path.join(adir, fn)) != sha(os.path.join(ad2, fn)):
                print(f"KB-E1-rerun FAIL: {fn} differs in {d}"); e1r = False; break
        if not e1r: break
    print(f"KB-E1 artifacts identical across 3 runs: {'PASS' if e1r else 'FAIL'}")

    # KB-E2: no phantom emission — every artifact has a claiming percept+selection
    e2 = True
    for fn in os.listdir(adir):
        # name: <trial>.e<k>.<ext>
        tid, rest = fn.rsplit(".e", 1)
        k = int(rest.split(".")[0])
        row = r1.get(tid)
        if row is None:
            print(f"KB-E2 FAIL: phantom {fn}"); e2 = False; break
        if k >= int(row[7]):
            print(f"KB-E2 FAIL: {fn} cites empty selection"); e2 = False; break
    print(f"KB-E2 no phantom emission: {'PASS' if e2 else 'FAIL'}")

    # ledger hash chain verification (run1): recompute sha256(prev || entry)
    import hashlib as hl
    led = []
    with open(os.path.join(base, "run1_emit", "LEDGER.jsonl")) as f:
        for line in f:
            led.append(line.rstrip("\n"))
    print(f"ledger lines: {len(led)}")
    chain_ok = True
    prev = bytes(32)
    for li, line in enumerate(led):
        hhex, rest = line.split(" ", 1)
        # parse fields from the annotation part
        fields = {}
        for tok in rest.split(" "):
            if "=" in tok:
                k, v = tok.split("=", 1)
                fields[k] = v
        tid = fields["trial"]
        row = r1[tid]
        # row: trial, task, fixture, judgment, conf, disp, ops, nsel, sel, claim, warrant, ledger
        disp01 = "1" if row[5] == "INSTALL" else "0"
        # judgment code: map name->code via task
        entry = (f"v=1|trial={tid}|task={row[1]}|j={fields['j']}|conf={row[4]}"
                 f"|disp={disp01}|ops={row[6]}|nsel={row[7]}|sel={row[8]}"
                 f"|claim={row[9]}|warrant={row[10]}")
        h = hl.sha256(prev + entry.encode()).hexdigest()
        if h != hhex:
            print(f"LEDGER CHAIN FAIL at line {li} ({tid}): recomputed {h} != {hhex}")
            chain_ok = False
            break
        prev = bytes.fromhex(hhex)
    print(f"ledger hash chain verified: {'PASS' if chain_ok else 'FAIL'}")
    print(f"final ledger hash: {led[-1].split()[0] if led else 'none'}")

if __name__ == "__main__":
    main()
