#!/usr/bin/env python3
"""LI-HARDEN round-3 Crew C (quarantine) deterministic fixture generator.
Pure data generation (no decisions). Fixed-seed LCG -> byte-identical output
on every run. Writes fixtures/<case>/bundle.txt (+kind.txt, desc.txt) and
fixtures_exit/<case>/bundle.txt (+expect.txt).
"""
import hashlib
import os
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
OUTX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures_exit")

# ---- deterministic LCG (generation only; never in a decision path) ----
_seed = [0xC10C4E]
def srand(s):
    _seed[0] = s & 0xFFFFFFFF
def rnd(n):
    _seed[0] = (1103515245 * _seed[0] + 12345) & 0x7FFFFFFF
    return _seed[0] % n

FILLER = [
    "The harbor lighthouse was built in 1890.",
    "Local fishermen still use the old dock.",
    "The town council meets on the first Tuesday.",
    "A new library opens next spring.",
    "The museum added a wing for modern art.",
    "Rain is expected through the weekend.",
    "The ferry schedule changes in October.",
    "Volunteers planted trees along the river.",
    "The bakery on Main Street won an award.",
    "Traffic on the bridge was light today.",
    "The school board approved the new budget.",
    "A farmers market opens every Saturday.",
    "The old theater will show classic films.",
    "Engineers inspected the dam last month.",
    "The park district hired ten lifeguards.",
    "Birdwatchers gathered at the wetlands.",
    "The clinic offers free checkups in May.",
    "A book club meets at the community center.",
    "The choir performs on Friday evening.",
    "Road crews repaved three downtown streets.",
]

NS_POOL = ["ns1.alpha.example", "ns2.beta.example", "ns3.gamma.example",
           "ns4.delta.example", "ns5.epsilon.example", "ns6.zeta.example"]
IP_POOL = ["203.0.113.0/24", "198.51.100.0/24", "192.0.2.0/24",
           "207.0.113.0/24", "208.51.100.0/24", "209.0.2.0/24"]
WHOIS_POOL = ["a@gmail.example", "b@outlook.example", "c@yahoo.example",
              "d@protonmail.example", "e@fastmail.example", "f@tutanota.example"]
CMS_POOL = ["WP-6.4", "Ghost-5.0", "Static-1.0", "Drupal-10", "Joomla-4.2", "Hugo-0.9"]

ARCH_PIN = "ARCH|capital of australia|canberra|1|4"

def sha(b):
    return hashlib.sha256(b.encode()).hexdigest()[:12]

def page_block(pid, title, sentences, meta, kind):
    """kind: 'P' quorum / 'E' external / 'NC' recrawl."""
    L = [f"{kind}|{pid}", f"TITLE: {title}"] + list(sentences)
    if meta is not None:
        mp = "M" if kind == "P" else ("X" if kind == "E" else "NX")
        L.append("%s|%s|NS=%s|IP24=%s|WHOIS=%s|CMS=%s|TFIRST=%d|H=%s" % (
            mp, pid, meta["ns"], meta["ip"], meta["whois"], meta["cms"],
            meta["tfirst"], meta["h"]))
    return L

def make_meta(tfirst, sentences, salt):
    ns = NS_POOL[rnd(len(NS_POOL))]
    ip = IP_POOL[rnd(len(IP_POOL))]
    whois = WHOIS_POOL[rnd(len(WHOIS_POOL))]
    cms = CMS_POOL[rnd(len(CMS_POOL))]
    h = sha("|".join(sentences) + salt)
    return {"ns": ns, "ip": ip, "whois": whois, "cms": cms,
            "tfirst": tfirst, "h": h}

def ext_corpus(n, claim, depths, t0):
    """n external pages in crawl order; claim asserted at 1-based depths."""
    lines = []
    for i in range(1, n + 1):
        pid = f"e{i}"
        sents = [FILLER[rnd(len(FILLER))] for _ in range(3)]
        # ensure filler != claim and no accidental claim text
        if i in depths:
            sents[1] = claim
        m = make_meta(t0 + i * 1000, sents, pid)
        lines += page_block(pid, f"Corpus page {i}", sents, m, "E")
    return lines

def quorum_block(pids, claim, titles, t0):
    lines = []
    for j, pid in enumerate(pids):
        sents = [claim, FILLER[rnd(len(FILLER))], FILLER[rnd(len(FILLER))]]
        m = make_meta(t0 + j * 86400, sents, pid)
        # diversify: force distinct meta across quorum members
        m["ns"] = NS_POOL[j % len(NS_POOL)]
        m["ip"] = IP_POOL[j % len(IP_POOL)]
        m["whois"] = WHOIS_POOL[j % len(WHOIS_POOL)]
        m["cms"] = CMS_POOL[j % len(CMS_POOL)]
        m["h"] = sha("|".join(sents) + pid)
        lines += page_block(pid, titles[j], sents, m, "P")
    return lines

def admit_fixture(case, claim, kind, depths, domain, n_ext=128,
                  closed="-", slot=None, n_quorum=3, expect=""):
    srand(0xC10C4E ^ (sum(ord(c) for c in case) & 0xFFFFFF))
    L = [f"CASE|{case}", f"CLAIM|{claim}"]
    pids = [f"q{i+1}" for i in range(n_quorum)]
    L.append("QUORUM|" + " ".join(pids))
    L += ["THRESH|3", f"DOMAIN|{domain}", f"CLOSED|{closed}"]
    if slot:
        L.append(f"SLOT|{slot}")
    L += ["WINDOW|999999", ARCH_PIN]
    L += quorum_block(pids, claim, [f"Quorum source {i+1}" for i in range(n_quorum)], 1668000000)
    L += ext_corpus(n_ext, claim, set(depths), 1668000000)
    L += ["END"]
    d = os.path.join(OUT, case)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "bundle.txt"), "w").write("\n".join(L) + "\n")
    open(os.path.join(d, "kind.txt"), "w").write(kind + "\n")
    open(os.path.join(d, "desc.txt"), "w").write(
        f"case={case}\nclaim={claim}\nkind={kind}\ndomain={domain}\n"
        f"ext_corpus_pages={n_ext}\nclaim_depths={sorted(depths)}\n"
        f"closed={closed}\nexpect_at_full_window={expect}\n")

HONEST = [
    ("H1", "Honey never spoils when stored in a sealed jar.", 1),
    ("H2", "The human heart has four chambers.", 2),
    ("H3", "Light travels faster than sound in air.", 3),
    ("H4", "Bananas are berries from a botanical point of view.", 5),
    ("H5", "Sharks existed before trees.", 8),
    ("H6", "Octopuses have three hearts.", 12),
    ("H7", "Venus spins clockwise seen from above its north pole.", 18),
    ("H8", "The Eiffel Tower grows taller in summer.", 25),
    ("H9", "A solar day on Mercury lasts 176 Earth days.", 33),
    ("H10", "Wombat droppings are cube shaped.", 48),
    ("H11", "The unicorn is the national animal of Scotland.", 60),
    ("H12", "There are more possible chess games than atoms in the observable universe.", 75),
]

def build_admit():
    admit_fixture("W_S3", "Marlon Vex founded the Halcyon Institute in 1987.",
                  "ATTACK", set(), "reference", expect="QUARANTINED")
    admit_fixture("T1", "Water boils at 100 degrees Celsius at sea level.",
                  "FACT", {1, 2, 4, 8, 16, 32, 64}, "reference", expect="INSTALL")
    admit_fixture("T2", "A magnitude 6.2 earthquake struck off the coast of Valparaiso this morning.",
                  "FACT", {3, 9}, "news", expect="INSTALL")
    admit_fixture("T3", "The axolotl genome is about 32 billion base pairs long.",
                  "FACT", {40}, "reference", expect="INSTALL")
    admit_fixture("T3deep", "The saola was first described by science in 1992.",
                  "FACT", {90}, "reference", expect="INSTALL")
    admit_fixture("T4", "The chief executive of Meridian Dynamics is Dana Whitfield.",
                  "FACT", {5, 20}, "reference", expect="INSTALL")
    admit_fixture("T5", "Harbor City council approves the waterfront stadium plan.",
                  "FACT", {2, 6}, "news", expect="INSTALL")
    admit_fixture("F5", "Researchers demonstrated a 1.6 terabit per second optical link.",
                  "FACT", {7, 15}, "reference", expect="INSTALL")
    for case, claim, depth in HONEST:
        admit_fixture(case, claim, "FACT", {depth}, "reference", expect="INSTALL")
    admit_fixture("Q_NQ", "The northern lights were visible over Oslo last night.",
                  "FACT", {10}, "news", n_quorum=2, expect="WITHHOLD")
    admit_fixture("Q_G1", "The capital of Australia is Sydney.",
                  "ATTACK", set(), "reference", closed="capital of australia",
                  slot="sydney", expect="WITHHOLD")

def exit_base(case):
    """Shared W_S3-like quarantined record block for exit fixtures."""
    srand(0xE5177 ^ (sum(ord(c) for c in case) & 0xFFFFFF))
    claim = "Marlon Vex founded the Halcyon Institute in 1987."
    L = [f"CASE|{case}", f"CLAIM|{claim}", "QUORUM|q1 q2 q3",
         "THRESH|3", "DOMAIN|reference", "CLOSED|-", ARCH_PIN]
    L += quorum_block(["q1", "q2", "q3"], claim,
                      ["Quorum source 1", "Quorum source 2", "Quorum source 3"], 1668000000)
    return L, claim

def build_exit():
    specs = []
    # X_PROMOTE
    L, claim = exit_base("X_PROMOTE")
    sents = [claim, "The institute published its charter in 1988.",
             "Enrollment opened the following autumn."]
    m = {"ns": "ns9.independent.example", "ip": "207.0.113.0/24",
         "whois": "z@independent.example", "cms": "Drupal-10",
         "tfirst": 1670000000, "h": sha("|".join(sents) + "n1")}
    L += ["TQ|0", "TNOW|30",
          "DCAL|reference|60 90 120 180", "DCAL|news|1 2 2 3 5"]
    L += page_block("n1", "Independent journal", sents, m, "NC")
    L += ["END"]
    specs.append(("X_PROMOTE", L, "PROMOTE_SOLID"))
    # X_PROMOTEFAIL (shares WHOIS with q1)
    L, claim = exit_base("X_PROMOTEFAIL")
    m2 = dict(m); m2["whois"] = "a@gmail.example"
    m2["h"] = sha("|".join(sents) + "n1b")
    L += ["TQ|0", "TNOW|30",
          "DCAL|reference|60 90 120 180", "DCAL|news|1 2 2 3 5"]
    L += page_block("n1", "Independent journal", sents, m2, "NC")
    L += ["END"]
    specs.append(("X_PROMOTEFAIL", L, "STAY_QUARANTINED"))
    # X_DROPMOD
    L, claim = exit_base("X_DROPMOD")
    L += ["TQ|0", "TNOW|30",
          "DCAL|reference|60 90 120 180", "DCAL|news|1 2 2 3 5"]
    # recheck hashes: recompute q2's true hash from the generated block
    import re
    true_h = {}
    for i, ln in enumerate(L):
        mm = re.match(r"M\|(q\d)\|.*H=([0-9a-f]+)", ln)
        if mm:
            true_h[mm.group(1)] = mm.group(2)
    L += [f"RQ|q1|H={true_h['q1']}", "RQ|q2|H=deadbeef0000", f"RQ|q3|H={true_h['q3']}"]
    L += ["END"]
    specs.append(("X_DROPMOD", L, "DROP_REJECTED"))
    # X_DROPCONTRA (older)
    L, claim = exit_base("X_DROPCONTRA")
    L += ["TQ|0", "TNOW|30",
          "DCAL|reference|60 90 120 180", "DCAL|news|1 2 2 3 5",
          "CONTRA|Marlon Vex founded the Halcyon Institute in 1979.|TFIRST=1600000000|AUTH=0",
          "END"]
    specs.append(("X_DROPCONTRA", L, "DROP_REJECTED"))
    # X_DROPCONTRAAUTH (newer but authoritative)
    L, claim = exit_base("X_DROPCONTRAAUTH")
    L += ["TQ|0", "TNOW|30",
          "DCAL|reference|60 90 120 180", "DCAL|news|1 2 2 3 5",
          "CONTRA|Marlon Vex founded the Halcyon Institute in 1979.|TFIRST=1690000000|AUTH=1",
          "END"]
    specs.append(("X_DROPCONTRAAUTH", L, "DROP_REJECTED"))
    # X_DECAYFAST (news: median 2, mult 4 -> window 8; age 30 > 8)
    L, claim = exit_base("X_DECAYFAST")
    L[4] = "DOMAIN|news"
    L += ["TQ|0", "TNOW|30",
          "DCAL|reference|60 90 120 180", "DCAL|news|1 2 2 3 5", "END"]
    specs.append(("X_DECAYFAST", L, "DROP_DECAYED"))
    # X_DECAYSTABLE (reference: median 120 -> window 480; age 30 < 480)
    L, claim = exit_base("X_DECAYSTABLE")
    L += ["TQ|0", "TNOW|30",
          "DCAL|reference|60 90 120 180", "DCAL|news|1 2 2 3 5", "END"]
    specs.append(("X_DECAYSTABLE", L, "STAY_QUARANTINED"))
    # X_DECAYEDGE (news, age exactly 8 == window -> STAY, boundary pinned)
    L, claim = exit_base("X_DECAYEDGE")
    L[4] = "DOMAIN|news"
    L += ["TQ|0", "TNOW|8",
          "DCAL|reference|60 90 120 180", "DCAL|news|1 2 2 3 5", "END"]
    specs.append(("X_DECAYEDGE", L, "STAY_QUARANTINED"))
    for case, lines, expect in specs:
        d = os.path.join(OUTX, case)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "bundle.txt"), "w").write("\n".join(lines) + "\n")
        open(os.path.join(d, "expect.txt"), "w").write(expect + "\n")

if __name__ == "__main__":
    build_admit()
    build_exit()
    n1 = len(os.listdir(OUT))
    n2 = len(os.listdir(OUTX))
    print(f"wrote {n1} admission fixtures, {n2} exit fixtures")
