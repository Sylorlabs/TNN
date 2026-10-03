#!/usr/bin/env python3
"""Independent 16-byte overlap audit (attack 2a).
Forbidden: every 16-byte substring (lowercased) of every utterance in the
frozen curriculum (ex/tr/pa/no/sinc/facts/calib/fhyp/nest/supp/paraphrases/types)
plus the original frozen 48-item calibration corpus.
Checked: every item utterance in cal_ab, cal_ab_rev, cal_abc, cal_c,
cal_vol, cal_de, cal_vol2 (lowercased).
Reports any item sharing a >=16-byte substring with a forbidden utterance,
excluding self-matches against the 48-item corpus it derives from (reported
separately).
"""
import os, subprocess

WT = os.path.expanduser("~/workspace/tnn-native-lab-redteam")
EXP = WT + "/docs/lab/epistemics/utterance_types/exp2c"
CUR = WT + "/docs/lab/epistemics/utterance_types/crew2/curriculum"
FROZ48 = WT + "/docs/lab/epistemics/utterance_types/broaderfix/crew2/calibration_corpus_items.txt"

def utterances(path, fields):
    """fields: tuple of 0-based field indexes holding utterance-ish text to forbid."""
    outs = []
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            p = line.split("|")
            for fi in fields:
                if fi < len(p):
                    outs.append((os.path.basename(path) + ":" + p[0], p[fi].lower()))
    return outs

forbidden = []  # (source, text)
for fn in os.listdir(CUR):
    # utterance is field 3 (id|speaker|ctx|utterance|...) for most; facts.txt field 1
    fp = os.path.join(CUR, fn)
    if fn == "facts.txt":
        forbidden += utterances(fp, (1,))
    elif fn == "types.txt":
        continue
    else:
        forbidden += utterances(fp, (3,))

# frozen 48-item corpus utterances (field 3)
frozen48 = utterances(FROZ48, (3,))
forbidden += frozen48

# build forbidden 16-gram set: map substring -> list of sources
fsub = {}
for src, txt in forbidden:
    for i in range(len(txt) - 15):
        s = txt[i:i+16]
        fsub.setdefault(s, []).append(src)

print(f"forbidden utterances: {len(forbidden)}, distinct 16-grams: {len(fsub)}")

frozen48_texts = set(t for _, t in frozen48)
items = ["cal_ab", "cal_ab_rev", "cal_abc", "cal_c", "cal_vol", "cal_de", "cal_vol2"]
total_viol = 0
for item in items:
    path = os.path.join(EXP, item + ".txt")
    n_viol = 0
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            p = line.split("|")
            utt = p[3].lower()
            hits = set()
            for i in range(len(utt) - 15):
                s = utt[i:i+16]
                if s in fsub:
                    # exclude self-match: same utterance text as a frozen48 item
                    srcs = [x for x in fsub[s] if not (x.startswith("calibration_corpus_items") and utt in frozen48_texts)]
                    if srcs:
                        hits.add((s, tuple(sorted(set(srcs))[:3])))
            if hits:
                n_viol += 1
                total_viol += 1
                print(f"VIOLATION {item} {p[0]}: {utt}")
                for s, srcs in sorted(hits)[:4]:
                    print(f"    16-gram {s!r} <- {srcs}")
    print(f"{item}: {n_viol} violating items")
print("TOTAL violations (excl. self-vs-frozen48):", total_viol)
