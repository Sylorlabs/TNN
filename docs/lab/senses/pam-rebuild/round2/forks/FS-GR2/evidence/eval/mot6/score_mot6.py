#!/usr/bin/env python3
"""FS-GR2 MOT-6 scoring: hash-chain verify + motiondir FI/recall + Wilson UCB + no-regression byte-identity."""
import sys, hashlib, math, os

WORK = os.path.dirname(os.path.abspath(__file__))
EVAL = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-GR1/evidence/eval"
FIXDIR = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-E2b/fixtures_e2b"

def ledger_chain(raw_path, led_path):
    """Build hash-chained ledger: content + ' hash=<hex>', prev starts '0'*64."""
    prev = "0" * 64
    lines = []
    with open(raw_path) as f:
        for ln in f:
            s = ln.rstrip("\n")
            if s == "":
                continue
            h = hashlib.sha256(bytes.fromhex(prev) + s.encode()).hexdigest()
            lines.append(s + " hash=" + h)
            prev = h
    with open(led_path, "w") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))
    return lines

def verify_chain(raw_path, led_path):
    """Recompute chain and compare."""
    prev = "0" * 64
    raw = [l.rstrip("\n") for l in open(raw_path) if l.strip() != ""]
    led = [l.rstrip("\n") for l in open(led_path) if l.strip() != ""]
    if len(raw) != len(led):
        return False, f"line count mismatch raw={len(raw)} led={len(led)}"
    for i, s in enumerate(raw):
        h = hashlib.sha256(bytes.fromhex(prev) + s.encode()).hexdigest()
        expect = s + " hash=" + h
        if led[i] != expect:
            return False, f"mismatch at line {i}"
        prev = h
    return True, f"{len(raw)} entries ok"

def parse(s):
    d = {}
    for tok in s.split():
        if "=" in tok:
            k, v = tok.split("=", 1)
            d[k] = v
    return d

def truth_for(fixture_id):
    # fixture=r2fx_t5_i33710_f1 -> filename e2b_<adv|ctrl>_... need original path.
    # Map via the manifest lists: find the .r2fx file whose name ends with r2fx fixture id.
    # We use the truth sidecar in FIXDIR: need to know adv/ctrl + task + index.
    raise NotImplementedError

def score_task(lines, task, fixture_truth):
    """Return list of (disp, judgment, truth) for a task."""
    rows = []
    for ln in lines:
        d = parse(ln)
        if d.get("task") == task:
            rows.append((d.get("disp"), d.get("judgment"), fixture_truth(d.get("fixture"))))
    return rows

def truth_lookup_factory(adv_list, ctrl_list):
    mp = {}
    for p, ls in (("adv", adv_list), ("ctrl", ctrl_list)):
        for ln in ls:
            ln = ln.strip()
            if not ln:
                continue
            path, claim = ln.split("\t")
            base = os.path.basename(path)
            # raw fixture= field is "r2fx_t<task>_i<index>_f<family>"
            mp[base] = base + ".truth"
    def get(fixture_field):
        # fixture_field like r2fx_t5_i33710_f1 -> find e2b_*r2fx file containing it
        return os.path.join(FIXDIR, None)
    return get

def wilson_ucb(x, n, z=1.96):
    if n == 0:
        return 0.0
    p = x / n
    z2 = z * z
    den = 1 + z2 / n
    num = p + z2 / (2 * n) + z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n))
    return num / den

def main():
    ok = True
    adv_raw = WORK + "/adv_raw_r1.txt"
    ctrl_raw = WORK + "/ctrl_raw_r1.txt"
    # 1. ledgers + verify
    for tag, raw in (("adv", adv_raw), ("ctrl", ctrl_raw)):
        led = WORK + f"/{tag}_chain_r1.ledger"
        ledger_chain(raw, led)
        v, msg = verify_chain(raw, led)
        print(f"hash-chain {tag}: {'PASS' if v else 'FAIL'} ({msg})")
        if not v:
            ok = False
    # 2. fixture truth map: adv_claim/ctrl_claim r1 TSVs list full paths
    truthmap = {}
    for tag, tsv in (("adv", EVAL + "/adv_claim_r1.tsv"), ("ctrl", EVAL + "/ctrl_claim_r1.tsv")):
        with open(tsv) as f:
            for ln in f:
                ln = ln.strip()
                if not ln:
                    continue
                path, claim = ln.split("\t")
                base = os.path.basename(path)
                # derive r2fx id: r2fx_t<task>_i<index>_f<family>
                t_id = base.replace("e2b_adv_", "").replace("e2b_ctrl_", "")
                t_id = t_id.replace(".r2fx", "")
                # truth sidecar format: "truth=<jname>"; FS-GR1's own scorer
                # (score_fsgr1.py) strips the prefix the same way.
                tline = open(path + ".truth").read().strip()
                truth = tline.split("=", 1)[1] if "=" in tline else tline
                truthmap[(tag, t_id.rsplit("_", 1)[1])] = truth
    def fx_truth2(src, fx):
        idx = fx.split("_i")[1].split("_")[0]
        return truthmap[(src, idx)]

    adv_lines = [l.rstrip("\n") for l in open(adv_raw) if l.strip() != ""]
    ctrl_lines = [l.rstrip("\n") for l in open(ctrl_raw) if l.strip() != ""]
    # 3. motiondir ADV FI
    fi = 0
    md_adv = [l for l in adv_lines if "task=motiondir" in l]
    for ln in md_adv:
        d = parse(ln)
        if d.get("disp") == "INSTALL" and d.get("judgment") != fx_truth2("adv", d.get("fixture")):
            fi += 1
    n_adv = len(md_adv)
    print(f"motiondir ADV: n={n_adv} FI={fi} rate={fi/n_adv:.4f} wilson_ucb={wilson_ucb(fi, n_adv):.4f}")
    if n_adv != 630:
        print(f"  WARNING: expected n=630, got {n_adv}")
        ok = False
    # 4. motiondir CTRL recall
    rec = 0
    md_ctrl = [l for l in ctrl_lines if "task=motiondir" in l]
    for ln in md_ctrl:
        d = parse(ln)
        if d.get("disp") == "INSTALL" and d.get("judgment") == fx_truth2("ctrl", d.get("fixture")):
            rec += 1
    n_ctrl = len(md_ctrl)
    print(f"motiondir CTRL: n={n_ctrl} recall={rec} ({rec/n_ctrl:.2%})")
    if n_ctrl != 200:
        print(f"  WARNING: expected n=200, got {n_ctrl}")
        ok = False
    # 5. no-regression: other five tasks byte-identical to FS-GR1 committed raw
    for tag, my, ref in (("adv", adv_raw, EVAL + "/adv_gate_raw_r1.txt"),
                         ("ctrl", ctrl_raw, EVAL + "/ctrl_gate_raw_r1.txt")):
        myl = [l for l in open(my).read().splitlines() if l.strip() != ""]
        refl = [l for l in open(ref).read().splitlines() if l.strip() != ""]
        myo = [l for l in myl if "task=motiondir" not in l]
        refo = [l for l in refl if "task=motiondir" not in l]
        same = myo == refo
        print(f"other-five byte-identity {tag}: {'PASS' if same else 'FAIL'} (my={len(myo)} ref={len(refo)})")
        if not same:
            ok = False
            for i, (a, b) in enumerate(zip(myo, refo)):
                if a != b:
                    print(f"  first diff at other-five index {i}:\n    my : {a}\n    ref: {b}")
                    break
            if len(myo) != len(refo):
                print(f"  length mismatch!")
    print("OVERALL:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
