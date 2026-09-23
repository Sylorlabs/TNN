#!/usr/bin/env python3
"""Generate frozen-evidence TSV inputs for the HELL-HOLE V3 repair ablation.

Reads ONLY frozen phase-2 evidence (never modifies it) and emits deterministic
TSV inputs under phase3/repairs/evidence/.

Outputs:
  course_input_solo.tsv / course_input_helper.tsv
      cand_idx \t env_seq \t res_idx \t domain \t title \t snippet \t url \t helper_stance \t helper_text
      (one row per web result; helper observations have res_idx=96, domain=helper,
       helper_stance = declared H stance, helper_text = observation text)
  candidates.tsv
      idx \t id \t claim \t known \t trigger \t prior \t contra \t oracle_solo \t oracle_helper \t type
  frozen_stances.tsv   (calibration target: arm \t cand_idx \t env_seq \t res_idx \t stance)
  frozen_disps.tsv     (arm \t cand_idx \t disp)
  tier_map.tsv         (domain \t tier)  -- mechanical rubric from why2/source_FINDINGS.md
  baseline_queries.tsv (cand_idx \t id \t baseline_query)
  first_queries.tsv    (arm \t cand_idx \t id \t first_query_actual)
"""
import json, os, re, sys, glob

BASE = os.path.expanduser("~/workspace/tnn-lab/senses/web-search/internet-trial")
P2 = os.path.join(BASE, "phase2")
OUT = os.path.join(BASE, "phase3/repairs/evidence")

CAND_IDS = ["C1","C2","C3","C4","C14","C5","C6","C7","C8","C9","C10","C11","C12","C13","C15","C16","A1","A2","A3"]

# --- candidate metadata from the frozen ht_sense2.zag tables (the exact strings the trial saw)
def parse_candidates():
    src = open(os.path.join(P2, "src/ht_sense2.zag")).read()
    def body(fn):
        i = src.index("fn " + fn)
        j = src.index("\nfn ", i)
        return src[i:j]
    def table(fn):
        d = {}
        for m in re.finditer(r'if\(i==(\d+)\)\{return "([^"]*)";\}', body(fn)):
            d[int(m.group(1))] = m.group(2)
        return d
    def itable(fn):
        d = {}
        for m in re.finditer(r'if\(i==(\d+)\)\{return (-?\d+);\}', body(fn)):
            d[int(m.group(1))] = int(m.group(2))
        return d
    claim = table("ht_cand_claim")
    query = table("ht_cand_query")
    known = itable("ht_cand_known"); trig = itable("ht_cand_trigger")
    prior = table("ht_cand_prior"); contra = table("ht_cand_contra")
    out = []
    for i in range(19):
        out.append((i, query[i], known.get(i,0), trig.get(i,0), prior.get(i,""),
                    contra.get(i,""), claim[i]))
    assert len(out) == 19 and all(o[6] for o in out)
    return out

# --- frozen course.json (parent fixtures): baseline queries + oracle
def load_course():
    c = json.load(open(os.path.join(BASE, "fixtures/course.json")))
    by_id = {x["id"]: x for x in c["claims"]}
    return by_id

# --- pre-search types (frozen claimgate analysis, 2026-09-22)
TYPES = {"C5":"CONTESTED","C6":"EVOLVED","C8":"SKEPTICISM","C11":"SKEPTICISM",
         "C12":"AMBIGUOUS","C13":"AMBIGUOUS"}

# frozen course.json label -> expected disposition
LABEL2DISP = {"TRUE":"INSTALL","FALSE":"REJECT","CONTESTED":"WITHHOLD",
              "EVOLVED":"WITHHOLD","AMBIGUOUS":"WITHHOLD","SPAM":"REJECT"}
# note: C11's oracle is REJECT in the frozen course; the skepticism-rule rescore
# excludes C11 from M1/K1 scoring but its disposition target stays REJECT.

# --- tier rubric (mechanical, from why2/source_FINDINGS.md)
T3_EXPLICIT = {"cancer.org","mayoclinic.org","cedars-sinai.org","massgeneralbrigham.org",
  "science.org","aacrjournals.org","tandfonline.com","mdpi.com","iop.org"}
T2_EXPLICIT = {"wikipedia.org","britannica.com","reuters.com","apnews.com","snopes.com",
  "factcheck.org","politifact.com","fullfact.org","eufactcheck.eu","bbc.co.uk","bbc.com",
  "nytimes.com","theguardian.com","washingtonpost.com","npr.org","pbs.org","smithsonianmag.com",
  "nationalgeographic.com","scientificamerican.com","newscientist.com","theconversation.com",
  "livescience.com","space.com","usatoday.com","cnn.com","nbcnews.com","abcnews.go.com",
  "cbsnews.com","aljazeera.com","dw.com","france24.com","euronews.com","japantimes.co.jp",
  "forbes.com","time.com","newsweek.com","theatlantic.com","economist.com","vox.com",
  "buzzfeednews.com","ajc.com","rochesterfirst.com","telegraph.co.uk","metro.co.uk",
  "sciencefocus.com","skyatnightmagazine.com","medicalnewstoday.com","healthline.com",
  "webmd.com","sciencealert.com","scitechdaily.com","merckmanuals.com","skepdic.com",
  "yourgenome.org","energyeducation.ca"}
T0_PLATFORMS = {"reddit.com","quora.com","stackexchange.com","stackoverflow.com","medium.com",
  "blogspot.com","blogger.com","wordpress.com","substack.com","tumblr.com","youtube.com",
  "tiktok.com","facebook.com","instagram.com","x.com","twitter.com","pinterest.com",
  "linkedin.com","vimeo.com","dailymotion.com","github.io","gitlab.io","weebly.com",
  "wixsite.com","slideshare.net","scribd.com","odysee.com"}
T0_OBSCURE = {"all-can.org","auricmedia.net","bottomofthat.com","galactic-hunter.com",
  "nexaconvert.com","nibble-app.com","discoveriesinmedicine.com","dnaftb.org",
  "gnet-research.org","genomesunzipped.org","climateaudit.org","dsimanek.vialattea.net",
  "wanttoknow.info","brainly.com","quizlet.com","factually.co","insomnia.net",
  "brucerosemanmd.com"}
T_1 = {"flatearthdave.com","tfes.org","chemtrailplanet.com","stopworldcontrol.com",
  "thehighwire.com","conspiracydata.com","allegro.cz","heureka.cz","cholesten.nutraceutics.cz",
  "biologicals.cz","uvtnet.cz","vyspimesa.sk","draxe.com"}
T3_SUFFIX = (".gov",".mil",".int",".edu")
T2_EXPLICIT_EXTRA = set()  # none beyond list

def host_of(url):
    m = re.match(r"https?://([^/]+)", url or "")
    h = (m.group(1) if m else "").lower()
    if h.startswith("www."): h = h[4:]
    return h

def strip_left(h):
    # progressive left-label stripping
    parts = h.split(".")
    out = [h]
    for i in range(1, len(parts)-1):
        out.append(".".join(parts[i:]))
    return out

def tier_of_domain(dom):
    h = dom.lower()
    cands = strip_left(h)
    for c in cands:
        if c in T_1: return -1
    for c in cands:
        if c in T0_PLATFORMS or c in T0_OBSCURE: return 0
    for c in cands:
        if c in T3_EXPLICIT: return 3
    for c in cands:
        if c in T2_EXPLICIT: return 2
    for c in cands:
        for s in T3_SUFFIX:
            if c.endswith(s): return 3
    return 1

def clean(s):
    return (s or "").replace("\t"," ").replace("\n"," ").replace("\r"," ").strip()

def main():
    os.makedirs(OUT, exist_ok=True)
    cands = parse_candidates()
    course = load_course()
    disps = {}
    stances = {}   # (arm,cand,env_seq,res_idx) -> stance
    rows = {"solo": [], "helper": []}
    tier_domains = set()
    firstq = {}

    for arm in ("solo","helper"):
        ev = os.path.join(P2, "evidence", arm)
        # session: QUERY_ISSUED order -> (cand, per-cand seq)
        qlines = [l for l in open(os.path.join(ev,"session.htsv")) if "\tQUERY_ISSUED\t" in l]
        order = []  # (cand, env_seq)
        per = {}
        for l in qlines:
            m = re.search(r"cand=(\d+)", l)
            c = int(m.group(1))
            s = per.get(c, 0); per[c] = s+1
            order.append((c, s))
        assert len(order) == (28 if arm=="solo" else 30), (arm, len(order))
        # first query actual per cand from envelopes
        envfiles = sorted(glob.glob(os.path.join(ev,"envelopes","*.json")))
        assert len(envfiles) == len(order), (arm, len(envfiles))
        for i,(c,s) in enumerate(order):
            d = json.load(open(envfiles[i]))
            if s == 0:
                firstq[(arm,c)] = d["query"]
            for r in d["results"]:
                rows[arm].append((c, s, r.get("rank",0), clean(r["domain"]),
                                  clean(r["title"]), clean(r["snippet"]), clean(r["url"]), 0, ""))
                tier_domains.add(r["domain"].lower())
        # helper observations
        hob = os.path.join(ev,"helper","*.htsv") if False else None
        for hf in sorted(glob.glob(os.path.join(ev,"helper","*.htsv"))):
            envno = int(os.path.basename(hf).split(".")[0])
            c, s = order[envno]
            ln = open(hf).read().strip().split("\t")
            assert ln[0]=="H"
            rows[arm].append((c, s, 96, "helper", "", clean(ln[2]), "", int(ln[1]), clean(ln[2])))
        # frozen stances
        for l in open(os.path.join(ev,"session.htsv")):
            if "\tCLAIM_EXTRACTED\t" in l:
                cm = re.search(r"cand=(\d+)", l); im = re.search(r"idx=(\d+)", l)
                sm = re.search(r"stance=(\d+)", l); dm = re.search(r"domain=([^\t]+)", l)
                # need env_seq: derive from page order -- CLAIM_EXTRACTED follows PAGE_OBSERVED in cycle order.
                # Simpler: match by (cand, domain, occurrence order) against rows.
                stances.setdefault((arm,int(cm.group(1)),dm.group(1)), []).append(int(sm.group(1)))
        # frozen dispositions
        sc = json.load(open(os.path.join(ev,"score.json")))
        for cid, d in sc["dispositions"].items():
            disps[(arm, CAND_IDS.index(cid))] = {"NO_SEARCH":0,"PROVISIONAL":1,"INSTALL":2,
                "REJECT":3,"WITHHOLD":4,"REVISE":5,"CORRUPT":6}[d]

    # map CLAIM_EXTRACTED stances onto rows by (arm,cand,domain) occurrence order
    # rows are already in (cand, env_seq, rank) order which matches ledger order
    seen = {}
    fro = []
    for arm in ("solo","helper"):
        for (c,s,r,dom,ti,sn,url,hs,htx) in rows[arm]:
            if r == 96:
                st = hs  # declared stance (calibration: frozen re-classified text; compare separately)
                fro.append((arm,c,s,r,-1))  # -1 = helper row marker; calibrated separately
                continue
            key=(arm,c,dom)
            lst = stances.get(key, [])
            k = seen.get(key,0); seen[key]=k+1
            st = lst[k] if k < len(lst) else -9
            fro.append((arm,c,s,r,st))

    with open(os.path.join(OUT,"course_input_solo.tsv"),"w") as f:
        for row in rows["solo"]:
            f.write("\t".join(map(str,row))+"\n")
    with open(os.path.join(OUT,"course_input_helper.tsv"),"w") as f:
        for row in rows["helper"]:
            f.write("\t".join(map(str,row))+"\n")
    with open(os.path.join(OUT,"frozen_stances.tsv"),"w") as f:
        for (a,c,s,r,st) in fro:
            f.write(f"{a}\t{c}\t{s}\t{r}\t{st}\n")
    with open(os.path.join(OUT,"frozen_disps.tsv"),"w") as f:
        for (a,c),d in sorted(disps.items()):
            f.write(f"{a}\t{c}\t{d}\n")
    with open(os.path.join(OUT,"candidates.tsv"),"w") as f:
        for (idx,q,known,trig,prior,contra,claim) in cands:
            cid = CAND_IDS[idx]
            co = course.get(cid, {})
            bq = co.get("query", q)
            o = LABEL2DISP.get(co.get("label",""), "WITHHOLD")
            f.write("\t".join(map(str,[idx,cid,clean(claim),known,trig,prior,contra,o,o,TYPES.get(cid,"SETTLED"),clean(bq)]))+"\n")
    with open(os.path.join(OUT,"tier_map.tsv"),"w") as f:
        for d in sorted(tier_domains):
            f.write(f"{d}\t{tier_of_domain(d)}\n")
    with open(os.path.join(OUT,"first_queries.tsv"),"w") as f:
        for (a,c),q in sorted(firstq.items()):
            f.write(f"{a}\t{c}\t{CAND_IDS[c]}\t{clean(q)}\n")
    print("rows:", {a: len(r) for a,r in rows.items()})
    print("frozen stances:", len(fro), "disps:", len(disps))

if __name__ == "__main__":
    main()
