#!/usr/bin/env python3
"""Per-probe isolation + novel-template generalization test.
For each of the 10 SINC-LK probes (si3_11..si3_20), build a variant root whose
sinc3.txt LK block (lines 11-20) is 10 copies of that single probe; run ab-a;
the LK score (10 vs 0) reveals the probe's individual verdict.
Then: novel sincere-if/do-we templates (authored fresh, 16-byte-novel) in the
same 10-copy block; run ab-a -> does the 2c fix generalize beyond trained templates?
"""
import os, shutil, subprocess, sys

RT = os.path.expanduser("~/workspace/redteam_exp2c")
PROBES = []
with open(RT + "/root/sinc3.txt") as f:
    lines = [l.rstrip("\n") for l in f if l.strip()]
dp_block = lines[:10]
lk_probes = lines[10:20]
assert len(lk_probes) == 10, len(lk_probes)
print("LK probes:")
for p in lk_probes:
    print("  ", p)

def make_root(name, lk_block):
    rd = f"/tmp/rtprobe/{name}"
    if os.path.exists(rd):
        shutil.rmtree(rd)
    shutil.copytree(RT + "/root", rd)
    with open(rd + "/sinc3.txt", "w") as f:
        f.write("\n".join(dp_block + lk_block) + "\n")
    return rd

def get_lk(stdout, ti=3):
    for line in stdout.splitlines():
        if line.startswith(f"2C_CURVE|{ti}|"):
            p = line.split("|")
            return int(p[11])  # TR|v|PA|v|NO|v|DP|v|LK|v -> LK value at index 11
    raise RuntimeError("no 2C_CURVE line in output")

def run_aba(rd):
    out = subprocess.run([RT + "/build/h7_exp2c_bin_rt", rd, "ab-a"],
                         capture_output=True, text=True, timeout=300)
    return get_lk(out.stdout)

def run_base(rd):
    out = subprocess.run([RT + "/build/h7_exp2c_bin_rt", rd, "base"],
                         capture_output=True, text=True, timeout=300)
    return get_lk(out.stdout)

mode = sys.argv[1]
if mode == "isolate":
    for i, probe in enumerate(lk_probes):
        rd = make_root(f"p{i:02d}", [probe] * 10)
        lk_b = run_base(rd)
        lk_a = run_aba(rd)
        print(f"probe si3_{11+i:02d} [{probe.split('|')[3]}] -> base LK={lk_b}/10, ab-a LK={lk_a}/10", flush=True)
elif mode == "novel2":
    # Novel "if the"/"do we" frames the corpus never used (16-byte-novel).
    # If base fails these and ab-a fixes them, the fix operates at the
    # bigram-marker level, not the taught-template level.
    novel2 = [
        "ny01|Mara|says evenly|Determine if the vault is sealed.|E",
        "ny02|Dev|says plainly|Ascertain if the ledger is balanced.|E",
        "ny03|Priya|says evenly|Establish if the signal is strong.|E",
        "ny04|Theo|says plainly|Do we trust the morning forecast?|E",
        "ny05|June|says evenly|Do we replace the worn cables?|E",
        "ny06|Sam|says plainly|Confirm if the cellar door is barred.|E",
    ]
    fsub = set()
    import glob
    WT = os.path.expanduser("~/workspace/tnn-native-lab-redteam")
    for fp in glob.glob(WT + "/docs/lab/epistemics/utterance_types/crew2/curriculum/*.txt"):
        with open(fp) as f:
            for line in f:
                line = line.rstrip()
                if not line or line.startswith("#"):
                    continue
                p = line.split("|")
                txt = p[3].lower() if len(p) > 4 else ""
                for j in range(len(txt) - 15):
                    fsub.add(txt[j:j+16])
    for c in ["cal_ab", "cal_abc", "cal_vol", "cal_vol2", "cal_de"]:
        with open(WT + f"/docs/lab/epistemics/utterance_types/exp2c/{c}.txt") as f:
            for line in f:
                p = line.rstrip().split("|")
                if len(p) > 4:
                    txt = p[3].lower()
                    for j in range(len(txt) - 15):
                        fsub.add(txt[j:j+16])
    ok = True
    for n in novel2:
        utt = n.split("|")[3].lower()
        hits = [utt[j:j+16] for j in range(len(utt)-15) if utt[j:j+16] in fsub]
        if hits:
            ok = False
            print("NOT NOVEL:", n, hits[:3])
    print("novelty check:", "ALL NOVEL" if ok else "FAILED")
    if not ok:
        sys.exit(1)
    # confirm none of the corpus items shares the leading verb frame
    for i, n in enumerate(novel2):
        rd = make_root(f"ny{i:02d}", [n] * 10)
        lk_b = run_base(rd)
        lk_a = run_aba(rd)
        print(f"novel2 {n.split('|')[0]} [{n.split('|')[3]}] -> base LK={lk_b}/10, ab-a LK={lk_a}/10", flush=True)
elif mode == "novel":
    # novel sincere templates, written fresh; verify 16-byte novelty vs all frozen + corpus
    novel = [
        "nx01|Mara|says evenly|Confirm whether the side gate is locked.|E",
        "nx02|Dev|says plainly|I wonder whether the tide comes in early.|E",
        "nx03|Priya|says evenly|Please verify that the lamps are all lit.|E",
        "nx04|Theo|says plainly|Do they know the shortcut through the pines?|E",
        "nx05|June|says evenly|It seems the harvest will be late this year.|E",
        "nx06|Sam|says plainly|We should check that the ropes are secure.|E",
        "nx07|Mara|says evenly|Has anyone seen my brass compass lately?|E",
        "nx08|Dev|says plainly|It appears the cellar flooded last spring.|E",
    ]
    # novelty check vs forbidden 16-grams
    fsub = set()
    import glob
    WT = os.path.expanduser("~/workspace/tnn-native-lab-redteam")
    for fp in glob.glob(WT + "/docs/lab/epistemics/utterance_types/crew2/curriculum/*.txt"):
        with open(fp) as f:
            for line in f:
                line = line.rstrip()
                if not line or line.startswith("#"):
                    continue
                p = line.split("|")
                txt = p[3].lower() if len(p) > 4 else ""
                for j in range(len(txt) - 15):
                    fsub.add(txt[j:j+16])
    for c in ["cal_ab", "cal_abc", "cal_vol", "cal_vol2", "cal_de"]:
        with open(WT + f"/docs/lab/epistemics/utterance_types/exp2c/{c}.txt") as f:
            for line in f:
                p = line.rstrip().split("|")
                if len(p) > 4:
                    txt = p[3].lower()
                    for j in range(len(txt) - 15):
                        fsub.add(txt[j:j+16])
    ok = True
    for n in novel:
        utt = n.split("|")[3].lower()
        hits = [utt[j:j+16] for j in range(len(utt)-15) if utt[j:j+16] in fsub]
        if hits:
            ok = False
            print("NOT NOVEL:", n, hits[:3])
    print("novelty check:", "ALL NOVEL" if ok else "FAILED")
    if not ok:
        sys.exit(1)
    # also run each novel probe under BASE (no 2c) to see pre-existing behavior
    for i, n in enumerate(novel):
        rd = make_root(f"nx{i:02d}", [n] * 10)
        lk_aba = run_aba(rd)
        lk_base = run_base(rd)
        print(f"novel {n.split('|')[0]} [{n.split('|')[3]}] -> base LK={lk_base}/10, ab-a LK={lk_aba}/10", flush=True)
