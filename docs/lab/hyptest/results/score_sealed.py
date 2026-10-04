#!/usr/bin/env python3
"""Mechanical scorer for the sealed hyptest battery (coordinator).
Reads per-case outputs (no judgment), compares against gold.tsv.
Exits 0 iff all checks pass. Prints a table.
Usage: score_sealed.py <workdir> <gold.tsv>
"""
import csv, re, sys

WORK, GOLD = sys.argv[1], sys.argv[2]

def read(p):
    with open(p, errors="replace") as f:
        return f.read()

gold = {}
with open(GOLD) as f:
    for row in csv.DictReader(f, delimiter="\t"):
        gold[row["phenomenon_id"]] = row

def eps_of(col):
    # "seal04.t.07;seal04.t.08" -> {7,8}
    return {int(x.split(".t.")[1]) for x in col.split(";") if x.strip()}

def audit_cites(workdir, case, slots):
    # union of st_evidence (op 22) d2 episodes across slots, from saved dump.log
    out = read(f"{workdir}/{case}/dump.log")
    cites = set()
    for line in out.splitlines():
        m = re.search(r"op 22 slot (\d+) .*d2 (\d+)", line)
        if m and int(m.group(1)) in slots:
            cites.add(int(m.group(2)))
    return cites

rows = []
allpass = True

def check(name, ok, detail=""):
    global allpass
    rows.append((name, "PASS" if ok else "FAIL", detail))
    if not ok:
        allpass = False

for case in ["seal01", "seal02", "seal03", "seal04", "sealB1", "sealB2"]:
    d = f"{WORK}/{case}"
    g = gold[case]
    tag = case
    try:
        hyp_txt = read(f"{d}/ht_hypotheses.txt")
        ver_txt = read(f"{d}/ht_verdict.txt")
        teach_log = read(f"{d}/teach.log")
    except FileNotFoundError as e:
        check(f"{tag} files present", False, str(e))
        continue

    # input hygiene: no dropped sentences
    m = re.search(r"badseg (\d+)", teach_log)
    check(f"{tag} badseg==0", m and m.group(1) == "0", m.group(0) if m else "no badseg line")

    hyps = []
    for m in re.finditer(r"^h (\d+) slot (\d+) predslot (\d+) attr_slot (\d+) value (\S+) predicts (\S+) carriers \d+ support ([\d ]+) audit", hyp_txt, re.M):
        hyps.append(dict(idx=int(m.group(1)), slot=int(m.group(2)), predslot=int(m.group(3)),
                         attr=int(m.group(4)), value=m.group(5), predicts=m.group(6),
                         support=[int(x) for x in m.group(7).split()]))
    check(f"{tag} K1 two-hypotheses", len(hyps) == 2, f"found {len(hyps)}")
    if len(hyps) != 2:
        continue
    check(f"{tag} K2 distinct-predictions", hyps[0]["predicts"] != hyps[1]["predicts"],
          f"{hyps[0]['predicts']} vs {hyps[1]['predicts']}")

    # K3 audit ordering
    try:
        pre = int(read(f"{d}/pre_test_audit.txt").strip())
        obs = int(read(f"{d}/obs_audit.txt").strip())
        check(f"{tag} K3 prereg-order", pre < obs, f"hyp audit {pre} < obs audit {obs}")
    except Exception as e:
        check(f"{tag} K3 prereg-order", False, str(e))

    # verdict parse
    status = {}
    for m in re.finditer(r"hypothesis (\d+) \(slot \d+\): attr_slot \d+=\S+ predicts \S+ status (\w+)", ver_txt):
        status[int(m.group(1))] = m.group(2)
    winner = g["winner"]
    if winner == "WITHHOLD":
        check(f"{tag} K5 withhold", "decision: withhold" in ver_txt, ver_txt.splitlines()[-2] if ver_txt else "")
        check(f"{tag} K5 none-abandoned", "abandoned hypothesis" not in ver_txt)
    else:
        want_attr = 0 if "attribute A wins" in winner else 1
        win_h = [h for h in hyps if h["attr"] == want_attr]
        lose_h = [h for h in hyps if h["attr"] != want_attr]
        ok_w = win_h and status.get(win_h[0]["idx"]) == "supported"
        ok_l = lose_h and ("abandoned hypothesis %d" % lose_h[0]["idx"]) in ver_txt
        check(f"{tag} K4 winner={winner[-6:]}", bool(ok_w and ok_l),
              f"statuses={status}")
        # K9: no confident-wrong: exactly one supported and it matches gold
        supported = [h for h in hyps if status.get(h["idx"]) == "supported"]
        check(f"{tag} K9 no-confident-wrong",
              len(supported) == 1 and supported[0]["attr"] == want_attr,
              f"supported attrs={[h['attr'] for h in supported]}")

    # K10 citations per hypothesis: union of (slot,predslot) st_evidence == gold support
    for h in hyps:
        gcol = g["support_h_a"] if h["attr"] == 0 else g["support_h_b"]
        gset = eps_of(gcol)
        try:
            actual = audit_cites(WORK, case, {h["slot"], h["predslot"]})
        except Exception as e:
            check(f"{tag} K10 h{h['idx']} cites", False, str(e))
            continue
        check(f"{tag} K10 h{h['idx']} recall", gset <= actual,
              f"gold {sorted(gset)} actual {sorted(actual)}")
        extra = actual - gset
        check(f"{tag} K10 h{h['idx']} precision-note", True,
              f"extra cites beyond gold: {sorted(extra)}")

print(f"{'check':44} {'res':6} detail")
for n, r, dt in rows:
    print(f"{n:44} {r:6} {dt}")
print("ALL PASS" if allpass else "FAILURES PRESENT")
sys.exit(0 if allpass else 1)
