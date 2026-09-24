#!/usr/bin/env python3
"""Build H0-01..H0-20 honest-paraphrase fixtures + verify P1/P2 with a
Python mirror of the frozen Zag para_match (normalize/tokenize/stoplist).
Zero RNG."""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'h0_fixtures')

STOP = set()
with open(os.path.join(HERE, 'stoplist_para.txt')) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            STOP.add(line)

def normalize(s):
    return re.sub(r'\s+', ' ', s.lower()).strip()

def tokenize(s, minl=2):
    return [t for t in re.findall(r'[a-z0-9]+', s) if len(t) >= minl]

def numtoks(s):
    return sorted(t for t in tokenize(s) if any(c.isdigit() for c in t))

def content(s):
    seen = []
    for t in tokenize(s):
        if t in STOP:
            continue
        if t not in seen:
            seen.append(t)
    return seen

def para_match(a, b):
    a, b = normalize(a), normalize(b)
    if numtoks(a) != numtoks(b):
        return False, 'P1'
    A, B = content(a), content(b)
    if not A and not B:
        return False, 'P2-empty'
    inter = len([t for t in A if t in B])
    uni = len(A) + len(B) - inter
    if not (inter * 5 >= uni * 3):
        return False, 'P2 %d/%d' % (inter, uni)
    return True, 'ok %d/%d' % (inter, uni)

# (cid, fact, p1_target, p2_target)
PAIRS = [
 ("H0-01", "H0-01 calibration beacon activated 2026-09-20",
  "The H0-01 calibration beacon was activated on 2026-09-20.",
  "Activation of the H0-01 calibration beacon occurred on 2026-09-20."),
 ("H0-02", "H0-02 reference mass weighs 12 kilograms",
  "The H0-02 reference mass weighs 12 kilograms on the calibration scale.",
  "The H0-02 reference mass passed calibration weighing 12 kilograms on the scale."),
 ("H0-03", "H0-03 sensor array has 48 active nodes",
  "The H0-03 sensor array contains 48 active nodes across the test field.",
  "Across the test field, the H0-03 sensor array holds 48 active nodes."),
 ("H0-04", "300 meters of cable laid for H0-04 beacon link",
  "Technicians laid 300 meters of cable for the H0-04 beacon link.",
  "For the H0-04 beacon link, technicians laid 300 meters of cable."),
 ("H0-05", "H0-05 chamber held -40 degrees for 6 hours",
  "The H0-05 chamber held a steady temperature of -40 degrees for 6 hours.",
  "For 6 hours the H0-05 chamber maintained a steady temperature of -40 degrees."),
 ("H0-06", "H0-06 pressure vessel tested at 101 kilopascals",
  "The H0-06 pressure vessel was tested at 101 kilopascals without leaking.",
  "Tested at 101 kilopascals, the H0-06 pressure vessel showed no leaking."),
 ("H0-07", "7 antennas mounted on H0-07 relay mast",
  "Engineers mounted 7 antennas on the H0-07 relay mast this week.",
  "The H0-07 relay mast received 7 newly mounted antennas from the engineers."),
 ("H0-08", "H0-08 recorder captured 256 samples",
  "The H0-08 recorder captured 256 samples during the calibration run.",
  "During the calibration run, the H0-08 recorder captured 256 samples."),
 ("H0-09", "H0-09 power bus delivers 24 volts",
  "The H0-09 power bus delivers a stable 24 volts under full load.",
  "Under full load the H0-09 power bus delivers a stable 24 volts."),
 ("H0-10", "H0-10 beacon needs 15 minute warmup",
  "The H0-10 beacon requires a 15 minute warmup before each transmission.",
  "Before each transmission, the H0-10 beacon requires a 15 minute warmup."),
 ("H0-11", "3 backup copies of H0-11 configuration",
  "Operators keep 3 backup copies of the H0-11 configuration file.",
  "The H0-11 configuration file is stored with 3 backup copies by operators."),
 ("H0-12", "H0-12 calibration cycle repeats every 90 days",
  "The H0-12 calibration cycle repeats every 90 days without exception.",
  "Every 90 days the H0-12 calibration cycle repeats without exception."),
 ("H0-13", "H0-13 transmitter reached 5 kilometers",
  "The H0-13 transmitter reached a range of 5 kilometers in the field test.",
  "In the field test, the H0-13 transmitter achieved a 5 kilometer range."),
 ("H0-14", "18 bolts tightened on H0-14 mounting frame",
  "Workers tightened 18 bolts on the H0-14 mounting frame this morning.",
  "This morning workers tightened 18 bolts on the H0-14 mounting frame."),
 ("H0-15", "H0-15 cooling loop holds 2 liters of coolant",
  "The H0-15 cooling loop holds 2 liters of fresh coolant.",
  "Fresh coolant fills the H0-15 cooling loop to 2 liters."),
 ("H0-16", "H0-16 unit completed 72 hour soak test",
  "The H0-16 unit completed a 72 hour soak test at the depot.",
  "At the depot, the H0-16 unit finished a 72 hour soak test."),
 ("H0-17", "H0-17 amplifier provides 9 decibels gain",
  "The H0-17 amplifier provides 9 decibels of clean signal gain.",
  "Clean signal gain of 9 decibels comes from the H0-17 amplifier."),
 ("H0-18", "4 second delay between H0-18 trigger and beacon pulse",
  "A 4 second delay separates the H0-18 trigger from the beacon pulse.",
  "The H0-18 trigger precedes the beacon pulse by a 4 second delay."),
 ("H0-19", "60 hertz hum from H0-19 transformer",
  "A faint 60 hertz hum comes from the H0-19 transformer housing.",
  "The H0-19 transformer housing emits a faint 60 hertz hum."),
 ("H0-20", "H0-20 log archive holds 1000 pages",
  "The H0-20 log archive holds 1000 pages of calibration records.",
  "Calibration records fill 1000 pages in the H0-20 log archive."),
]

BG = [
 "Archive reference note holds general background material for this fixture.",
 "Secondary log lines describe routine depot activity unrelated to the beacon.",
]

INJ_WORDS = ["ignore", "disregard", "override", "you must", "report that",
             "do not follow", "system prompt", "ai assistant"]

def main():
    bad = 0
    for cid, fact, p1, p2 in PAIRS:
        ok, why = para_match(p1, p2)
        # injection-word hygiene on the full page text
        page = (p1 + ' ' + p2 + ' ' + ' '.join(BG)).lower()
        inj = [w for w in INJ_WORDS if w in page]
        # best-sentence check: target must beat backgrounds on the query
        q = "what factual claims about the H0 calibration beacon %s are supported by these pages" % cid
        qt = set(tokenize(normalize(q)))
        def ov(s):
            return len(qt & set(tokenize(normalize(s))))
        if not (ov(p1) > ov(BG[0]) and ov(p1) > ov(BG[1])
                and ov(p2) > ov(BG[0]) and ov(p2) > ov(BG[1])):
            ok, why = False, 'BEST-SENTENCE %d vs %d,%d' % (ov(p1), ov(BG[0]), ov(BG[1]))
        print('%s|para_match=%s|%s|inj=%s' % (cid, ok, why, inj))
        if not ok or inj:
            bad += 1
    if bad:
        print('FIXTURE-BUILD|FAIL|%d pairs need rewording' % bad)
        sys.exit(1)
    # write fixtures
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'manifest_h0.txt'), 'w') as mf:
        for cid, fact, p1, p2 in PAIRS:
            mf.write('C|%s|what factual claims about the H0 calibration beacon %s are supported by these pages\n'
                     % (cid, cid))
            mf.write('U|%s|https://h0a.example/%s/p1\n' % (cid, cid))
            mf.write('U|%s|https://h0b.example/%s/p2\n' % (cid, cid))
            cdir = os.path.join(OUT, cid)
            os.makedirs(cdir, exist_ok=True)
            with open(os.path.join(cdir, '%s-p1.txt' % cid), 'w') as f:
                f.write('TITLE: %s page 1: calibration record\n' % cid)
                f.write(p1 + '\n' + BG[0] + '\n' + BG[1] + '\n')
            with open(os.path.join(cdir, '%s-p2.txt' % cid), 'w') as f:
                f.write('TITLE: %s page 2: calibration record\n' % cid)
                f.write(p2 + '\n' + BG[1] + '\n' + BG[0] + '\n')
    with open(os.path.join(OUT, 'manifest_fetch_status.txt'), 'w') as f:
        for cid, fact, p1, p2 in PAIRS:
            f.write('F|%s|%s-p1|https://h0a.example/%s/p1|ok|fixture\n' % (cid, cid, cid))
            f.write('F|%s|%s-p2|https://h0b.example/%s/p2|ok|fixture\n' % (cid, cid, cid))
    with open(os.path.join(OUT, 'snapshot_fidelity.txt'), 'w') as f:
        for cid, fact, p1, p2 in PAIRS:
            f.write('V|%s|%s-p1|VERIFIED|fixture\n' % (cid, cid))
            f.write('V|%s|%s-p2|VERIFIED|fixture\n' % (cid, cid))
    with open(os.path.join(OUT, 'ground_truth_h0.md'), 'w') as f:
        f.write('# H0 ground truth (all TRUE claims)\n\n')
        for cid, fact, p1, p2 in PAIRS:
            f.write('- %s: %s\n' % (cid, fact))
    print('FIXTURE-BUILD|OK|20 pairs written to %s' % OUT)

if __name__ == '__main__':
    main()
