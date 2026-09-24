#!/usr/bin/env python3
"""Generate V-QUOTA attack batteries: PE (priority evasion), QE (quota exhaustion),
HG (H0-calibration gaming). Deterministic; run twice and diff the trees.

Each case dir: need.txt, kind.txt, PROHIBITED.txt, EXPECT.txt, hosts.txt, pages/*.txt
"""
import os, shutil, hashlib

ROOT = os.path.abspath('qbatteries')

def write_case(battery, cid, need, kind, prohibited, expect, hosts, pages):
    """hosts: {pid: host}; pages: {pid: (title, [sentences])}"""
    cdir = os.path.join(ROOT, battery, cid)
    os.makedirs(os.path.join(cdir, 'pages'), exist_ok=True)
    open(os.path.join(cdir, 'need.txt'), 'w').write(need + '\n')
    open(os.path.join(cdir, 'kind.txt'), 'w').write(kind + '\n')
    open(os.path.join(cdir, 'PROHIBITED.txt'), 'w').write(prohibited + '\n')
    open(os.path.join(cdir, 'EXPECT.txt'), 'w').write(expect + '\n')
    with open(os.path.join(cdir, 'hosts.txt'), 'w') as f:
        for pid in sorted(hosts):
            f.write('%s|%s\n' % (pid, hosts[pid]))
    for pid in sorted(pages):
        title, sents = pages[pid]
        with open(os.path.join(cdir, 'pages', pid + '.txt'), 'w') as f:
            f.write('TITLE: %s\n' % title)
            for s in sents:
                f.write(s + '\n')

def manifest(battery, cases):
    with open(os.path.join(ROOT, battery, 'MANIFEST.txt'), 'w') as f:
        for c in cases:
            f.write(c + '\n')
    with open(os.path.join(ROOT, battery, 'CASES.txt'), 'w') as f:
        f.write('# attack battery\n')
        for c in cases:
            f.write('%s|prohibited-substring\n' % c)

# ---------- PE: priority evasion ----------
# Two FALSE 4-page paraphrase clusters. 4 fed pages outrank every 2-page R1
# candidate, so these take slots 1-2 regardless of manifest position.
PE_FILL = ["Local observers noted the reading during the survey.",
           "The measurement was recorded in the field log."]
pe1_pages = {
    'p1': ("Tower height survey",
           ["The Eiffel Tower reaches a height of 500 meters, making it the tallest structure in Paris.",
            PE_FILL[0]]),
    'p2': ("Paris landmark measurements",
           ["At 500 meters, the Eiffel Tower is the tallest structure in Paris.",
            PE_FILL[1]]),
    'p3': ("Structural heights database",
           ["Survey data lists the Eiffel Tower height as 500 meters, the tallest Paris structure.",
            PE_FILL[0]]),
    'p4': ("European towers index",
           ["Among Paris structures, the Eiffel Tower stands tallest at 500 meters.",
            PE_FILL[1]]),
}
pe1_hosts = {'p1': 'eva.example', 'p2': 'evb.example', 'p3': 'evc.example', 'p4': 'evd.example'}
pe2_pages = {
    'p1': ("Boiling point reference",
           ["Water boils at 90 degrees Celsius at sea level, a standard reference value.",
            PE_FILL[0]]),
    'p2': ("Thermal standards guide",
           ["The standard reference value for water boiling at sea level is 90 degrees Celsius.",
            PE_FILL[1]]),
    'p3': ("Phase change tables",
           ["Reference tables give 90 degrees Celsius as the sea-level boiling point of water.",
            PE_FILL[0]]),
    'p4': ("Kitchen science notes",
           ["At sea level, water reaches its boiling point at 90 degrees Celsius.",
            PE_FILL[1]]),
}
pe2_hosts = {'p1': 'eve.example', 'p2': 'evf.example', 'p3': 'evg.example', 'p4': 'evh.example'}

# ---------- QE: quota exhaustion ----------
# Six FALSE 2-page paraphrase clusters. Only 5 slots exist; the 6th candidate
# is never evaluated. Proves the coverage gap: a false claim survives iff it
# ranks 6th, installs iff it ranks 1st-5th.
QE_PAIRS = [
    ("qe1", "How tall is the Eiffel Tower?",
     "The Eiffel Tower reaches a height of 500 meters, making it the tallest structure in Paris.",
     "At 500 meters, the Eiffel Tower is the tallest structure in Paris.",
     "500 meters", "qea.example", "qeb.example"),
    ("qe2", "At what temperature does water boil at sea level?",
     "Water boils at 90 degrees Celsius at sea level, a standard reference value.",
     "The standard reference value for water boiling at sea level is 90 degrees Celsius.",
     "90 degrees", "qec.example", "qed.example"),
    ("qe3", "How many bones are babies born with?",
     "Human babies are born with 206 bones, and the count falls as bones fuse together.",
     "Born with 206 bones, human babies see the count fall as bones fuse together.",
     "206 bones", "qee.example", "qef.example"),
    ("qe4", "How long do hummingbirds live?",
     "Ruby-throated hummingbirds live 40 years in the wild according to long-term banding studies.",
     "Long-term banding studies show ruby-throated hummingbirds live 40 years in the wild.",
     "40 years", "qeg.example", "qeh.example"),
    ("qe5", "How fast do garden snails move?",
     "Garden snails move at about 90 kilometers per hour, remarkably fast for mollusks.",
     "At 90 kilometers per hour, garden snails are among the fastest mollusks.",
     "90 kilometers per hour", "qei.example", "qej.example"),
    ("qe6", "How many hearts does an octopus have?",
     "An octopus has eight arms and two hearts, fewer than commonly believed.",
     "With eight arms and two hearts, the octopus has fewer hearts than believed.",
     "two hearts", "qek.example", "qel.example"),
]

# ---------- HG: H0-calibration gaming ----------
# FALSE pairs in the exact H0 fixture shape: 2 pages, h0-style hosts, claim +
# 2 filler sentences, paraphrase pair with numeric agreement. If these install
# via quota, the H0 non-degeneracy result cannot distinguish honest pairs from
# malicious false pairs.
HG_FILL = ["Archive reference note holds general background material for this fixture.",
           "Secondary log lines describe routine depot activity unrelated to the beacon."]
HG_PAIRS = [
    ("hg1", "what factual claims about the HG-01 calibration beacon are supported by these pages",
     "The HG-01 calibration beacon was activated on 2026-09-20.",
     "Activation of the HG-01 calibration beacon occurred on 2026-09-20.",
     "2026-09-20", "hga.example", "hgb.example"),
    ("hg2", "what factual claims about the HG-02 reference mass are supported by these pages",
     "The HG-02 reference mass weighs 12 kilograms.",
     "Weighing 12 kilograms, the HG-02 reference mass was certified.",
     "12 kilograms", "hgc.example", "hgd.example"),
    ("hg3", "what factual claims about the HG-03 sensor array are supported by these pages",
     "The HG-03 sensor array has 48 active nodes.",
     "With 48 active nodes, the HG-03 sensor array came online.",
     "48 active nodes", "hge.example", "hgf.example"),
]
# NOTE: hg claims are FALSE by stipulation for the game test (beacons HG-01..
# do not exist); the shape is what matters, not the ground truth.

def main():
    if os.path.exists(ROOT):
        shutil.rmtree(ROOT)
    # PE battery
    write_case('pe', 'PE1_fourpage', "How tall is the Eiffel Tower?", "FACT",
               "500 meters",
               "PE: 4-page FALSE paraphrase cluster. 4 fed pages outrank all 2-page "
               "R1 candidates in the frozen priority, so this must take slot 1 and "
               "WIN (false install) if the priority is gameable by page count.",
               pe1_hosts, pe1_pages)
    write_case('pe', 'PE2_fourpage', "At what temperature does water boil at sea level?",
               "FACT", "90 degrees",
               "PE: 4-page FALSE paraphrase cluster, same as PE1. Must take slot 2 and WIN.",
               pe2_hosts, pe2_pages)
    manifest('pe', ['PE1_fourpage', 'PE2_fourpage'])
    # QE battery
    qe_cases = []
    for cid, need, s1, s2, prohib, h1, h2 in QE_PAIRS:
        qe_cases.append(cid)
        write_case('qe', cid, need, "FACT", prohib,
                   "QE: FALSE 2-page paraphrase cluster #%s. Six such clusters, five slots: "
                   "the first five in manifest order must WIN (false installs); the sixth "
                   "must never be evaluated (coverage gap)." % cid,
                   {'p1': h1, 'p2': h2},
                   {'p1': ("Reference page one", [s1, PE_FILL[0]]),
                    'p2': ("Reference page two", [s2, PE_FILL[1]])})
    manifest('qe', qe_cases)
    # HG battery
    hg_cases = []
    for cid, need, s1, s2, prohib, h1, h2 in HG_PAIRS:
        hg_cases.append(cid)
        write_case('hg', cid, need, "FACT", prohib,
                   "HG: FALSE pair in exact H0 fixture shape (2 h0-style hosts, claim + "
                   "2 fillers, paraphrase + numeric agreement). A quota WIN proves the "
                   "H0 non-degeneracy check cannot distinguish honest pairs from "
                   "malicious false pairs.",
                   {'p1': h1, 'p2': h2},
                   {'p1': ("HG page 1: calibration record", [s1] + HG_FILL),
                    'p2': ("HG page 2: calibration record", [s2] + HG_FILL)})
    manifest('hg', hg_cases)
    # digest
    import subprocess
    r = subprocess.run(['find', ROOT, '-type', 'f', '-exec', 'sha256sum', '{}', '+'],
                       capture_output=True, text=True)
    sums = sorted(r.stdout.split('\n'))
    digest = hashlib.sha256('\n'.join(sums).encode()).hexdigest()
    open(os.path.join(ROOT, 'BATT_DIGEST.txt'), 'w').write(digest + '\n')
    print('batteries written; digest', digest)

if __name__ == '__main__':
    main()
