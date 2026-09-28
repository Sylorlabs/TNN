#!/usr/bin/env python3
"""gen_mw.py — generate src/mw_cases.zag for the mixed-web experiment.

Loads frozen live envelopes (live/*.json), extracts stated answers with the
frozen mechanical regexes (PREREG §2–§3), derives expectations with the frozen
deliberation rules (PREREG §4), and emits per-question feed + per-arm run/check
functions. Golds come from golds.json (frozen at inspection, pre-score).

Answer extraction: candidates scanned IN FROZEN ORDER; first regex match wins.
Recency: max 4-digit year in title+snippet, else 0.
"""
import hashlib
import json
import os
import re

BASE = os.path.expanduser("~/workspace/tnn-lab/mixed-web")
LIVE = os.path.join(BASE, "live")
OUT = os.path.join(BASE, "src", "mw_cases.zag")

# qid, question text, temporal, [(regex, canonical)...] in frozen match order
QUESTIONS = [
    ("M01", "What is the oldest university in the world?", 0, [
        (r"university of bologna", "University of Bologna"),
        (r"al[ -]?qarawiyyin", "Al-Qarawiyyin"),
        (r"nalanda", "Nalanda")]),
    ("M02", "Who invented the telephone?", 0, [
        (r"alexander graham bell|graham bell", "Alexander Graham Bell"),
        (r"antonio meucci|meucci", "Antonio Meucci"),
        (r"elisha gray", "Elisha Gray")]),
    ("M03", "Who discovered America?", 0, [
        (r"christopher columbus|columbus", "Christopher Columbus"),
        (r"leif erikson|erikson", "Leif Erikson"),
        (r"amerigo vespucci|vespucci", "Amerigo Vespucci")]),
    ("M04", "How many countries are in Africa?", 0, [
        (r"\b54 countries\b", "54"),
        (r"\b55 countries\b", "55"),
        (r"\b56 countries\b", "56")]),
    ("M05", "What is the largest desert in the world?", 0, [
        (r"antarc\w*", "Antarctic"),
        (r"\bsahara\b", "Sahara"),
        (r"\barctic\b", "Arctic")]),
    ("M06", "What is the longest river in the world?", 0, [
        (r"\bnile\b", "Nile"),
        (r"\bamazon\b", "Amazon"),
        (r"\byangtze\b", "Yangtze")]),
    ("M07", "What is the largest lake in the world?", 0, [
        (r"caspian sea", "Caspian Sea"),
        (r"lake superior", "Lake Superior"),
        (r"lake baikal", "Lake Baikal")]),
    ("M08", "What is the tallest mountain in the world?", 0, [
        (r"mount everest|everest", "Mount Everest"),
        (r"mauna kea", "Mauna Kea"),
        (r"\bk2\b", "K2")]),
    ("M09", "Who wrote the first novel in history?", 0, [
        (r"murasaki", "Murasaki"),
        (r"cervantes", "Cervantes")]),
    ("M10", "What is the oldest civilization in the world?", 0, [
        (r"mesopotamia", "Mesopotamia"),
        (r"\begypt\b", "Egypt"),
        (r"indus valley", "Indus Valley")]),
    ("M11", "What is the most spoken language in the world?", 0, [
        (r"\benglish\b", "English"),
        (r"mandarin", "Mandarin"),
        (r"\bspanish\b", "Spanish")]),
    ("M12", "Who invented the light bulb?", 0, [
        (r"\bedison\b", "Edison"),
        (r"\bswan\b", "Swan"),
        (r"\bdavy\b", "Davy")]),
    ("M13", "What is the most populous city in the world?", 0, [
        (r"\btokyo\b", "Tokyo"),
        (r"\bdelhi\b", "Delhi"),
        (r"\bshanghai\b", "Shanghai")]),
    ("M14", "What is the oldest city in the world?", 0, [
        (r"\bdamascus\b", "Damascus"),
        (r"\bjericho\b", "Jericho"),
        (r"\baleppo\b", "Aleppo")]),
    ("M15", "What is the largest economy in the world by nominal GDP?", 0, [
        (r"united states", "United States"),
        (r"\bchina\b", "China"),
        (r"\bjapan\b", "Japan")]),
    ("M16", "Which country has the most natural lakes in the world?", 0, [
        (r"\bcanada\b", "Canada"),
        (r"\brussia\b", "Russia"),
        (r"\bfinland\b", "Finland")]),
    ("M17", "What is the fastest animal in the world?", 0, [
        (r"peregrine falcon", "Peregrine falcon"),
        (r"\bcheetah\b", "Cheetah"),
        (r"\bsailfish\b", "Sailfish")]),
    ("R01", "What is the tallest completed building in the world?", 1, [
        (r"burj khalifa", "Burj Khalifa"),
        (r"jeddah tower", "Jeddah Tower"),
        (r"merdeka 118", "Merdeka 118")]),
    ("R02", "What is the largest country in the world by population?", 1, [
        (r"\bindia\b", "India"),
        (r"\bchina\b", "China")]),
    ("R03", "Who are the reigning FIFA World Cup champions?", 1, [
        (r"\bargentina\b", "Argentina"),
        (r"\bspain\b", "Spain"),
        (r"\bfrance\b", "France"),
        (r"\bbrazil\b", "Brazil")]),
    ("R04", "Who is the president of the United States?", 1, [
        (r"donald trump|trump", "Donald Trump"),
        (r"joe biden|biden", "Joe Biden")]),
    ("R05", "Who is the prime minister of the United Kingdom?", 1, [
        (r"keir starmer|starmer", "Keir Starmer"),
        (r"rishi sunak|sunak", "Rishi Sunak")]),
    ("R06", "Who is the richest person in the world?", 1, [
        (r"elon musk|musk", "Elon Musk"),
        (r"jeff bezos|bezos", "Jeff Bezos"),
        (r"bernard arnault|arnault", "Bernard Arnault")]),
    ("M18", "Who invented the World Wide Web?", 0, [
        (r"tim berners|berners-lee|berners lee", "Tim Berners-Lee"),
        (r"vint cerf|cerf", "Vint Cerf"),
        (r"robert kahn|kahn", "Robert Kahn")]),
    ("M19", "Who invented the airplane?", 0, [
        (r"wright brothers|wright", "Wright brothers"),
        (r"santos.dumont|santos dumont", "Santos-Dumont")]),
    ("M20", "What is the tallest waterfall in the world?", 0, [
        (r"angel falls", "Angel Falls"),
        (r"tugela falls", "Tugela Falls"),
        (r"kaieteur", "Kaieteur Falls")]),
    ("M21", "What is the oldest language in the world?", 0, [
        (r"\btamil\b", "Tamil"),
        (r"sanskrit", "Sanskrit"),
        (r"sumerian", "Sumerian")]),
    ("M22", "What was the first video game?", 0, [
        (r"\bpong\b", "Pong"),
        (r"spacewar", "Spacewar!"),
        (r"tennis for two", "Tennis for Two")]),
    ("M23", "What is the largest pyramid in the world?", 0, [
        (r"cholula", "Great Pyramid of Cholula"),
        (r"giza", "Great Pyramid of Giza")]),
]

YEAR_RE = re.compile(r"\b(19\d{2}|20\d{2})\b")


def zc(s):
    return re.sub(r"\s+", " ", s).strip()


def zg(s):
    return zc(s).replace("\\", "\\\\").replace('"', '\\"')


def rhash(url, title, snippet):
    body = (zc(url) + "\n" + zc(title) + "\n" + zc(snippet)).encode("utf-8")
    return hashlib.sha256(body).hexdigest()


def recency_of(title, snippet):
    yrs = [int(y) for y in YEAR_RE.findall(title + " " + snippet)]
    return max(yrs) if yrs else 0


def extract(text, cands):
    t = text.lower()
    for rx, canon in cands:
        if re.search(rx, t):
            return canon
    return ""


def load_results(qid, cands, maxn=10):
    d = json.load(open(os.path.join(LIVE, qid + ".json")))
    out, disc = [], []
    for r in d["results"][:maxn]:
        title, url, snip = r.get("title", ""), r.get("url", ""), r.get("snippet", "")
        dom = r.get("domain", "")
        if not (title and url):
            continue
        ans = extract(title + " " + snip, cands)
        rec = {"domain": dom, "title": title, "url": url, "snippet": snip,
               "answer": ans, "recency": recency_of(title, snip)}
        if ans:
            out.append(rec)
        else:
            disc.append(rec)
    return out, disc


def derive(temporal, results):
    """Frozen PREREG §4 rules. Returns (verdict, chosen, rule, class, cands).
    cands: first-seen-ordered list of (answer, distinct-domain count, recency)."""
    seen = []
    pairs = set()
    for r in results:
        key = (r["domain"], r["answer"])
        if key in pairs:
            continue
        pairs.add(key)
        if r["answer"] not in [s[0] for s in seen]:
            seen.append([r["answer"], set(), 0])
        e = seen[[s[0] for s in seen].index(r["answer"])]
        e[1].add(r["domain"])
        if r["recency"] > e[2]:
            e[2] = r["recency"]
    cands = [(a, len(ds), rc) for a, ds, rc in seen]
    if not cands:
        return ("WITHHOLD", "", "INSUFFICIENT", "W", cands)
    best_i, bc = 0, cands[0][1]
    rc2 = 0
    for i in range(1, len(cands)):
        n = cands[i][1]
        if n > bc:
            rc2, bc, best_i = bc, n, i
        elif i != best_i and n > rc2:
            rc2 = n
    tot = len({r["domain"] for r in results})
    if temporal == 1:
        ni, nr = 0, cands[0][2]
        sr = 0
        for i in range(1, len(cands)):
            r = cands[i][2]
            if r > nr:
                sr, nr, ni = nr, r, i
            elif i != ni and r > sr:
                sr = r
        nn = cands[ni][1]
        if nr >= 2000 and nn >= 2 and nr - sr >= 3:
            na, ba = cands[ni][0], cands[best_i][0]
            if na == ba:
                return ("CONVERGE", na, "RECENCY", "R", cands)
            if bc >= 2 * nn:
                return ("WITHHOLD", "", "STALE_CONFLICT", "W", cands)
            return ("CONVERGE", na, "RECENCY", "R", cands)
    if bc >= 3 and bc >= 2 * rc2:
        return ("CONVERGE", cands[best_i][0], "MAJORITY", "C", cands)
    if bc >= 2 and tot <= 4 and rc2 <= 1:
        return ("CONVERGE", cands[best_i][0], "CORROB", "C", cands)
    rule = "TIE" if rc2 >= 1 else "INSUFFICIENT"
    return ("WITHHOLD", "", rule, "W", cands)


def emit_feedA(lines, qid, question, results):
    lines.append(f"fn feedA_{qid}(w:*WsF) void {{")
    lines.append(f'    ws_fact_begin(w, 1, 0, "{qid}", "{zg(question)}", "", 2, 0);')
    for r in results:
        lines.append(
            f'    ws_add_result(w, "{zg(r["domain"])}", "{zg(r["title"])}", '
            f'"{zg(r["snippet"])}", "{zg(r["url"])}", "{zg(r["answer"])}", 1, '
            f'"{rhash(r["url"], r["title"], r["snippet"])}");')
    lines.append("    return;")
    lines.append("}")


def emit_feedB(lines, qid, question, temporal, results):
    lines.append(f"fn feedB_{qid}(w:*MwF) void {{")
    lines.append(f'    mw_fact_begin(w, "{qid}", "{zg(question)}", {temporal});')
    for r in results:
        lines.append(
            f'    mw_add_result(w, "{zg(r["domain"])}", "{zg(r["answer"])}", {r["recency"]});')
    lines.append("    return;")
    lines.append("}")


def emit_qa(lines, qid):
    lines.append(f"fn qa_{qid}() void {{")
    lines.append("    let w:*WsF=ws2_new();")
    lines.append("    ws_wire(w, 1, 1);")
    lines.append(f"    feedA_{qid}(w);")
    lines.append("    let d:i32=ws_decide(w);")
    lines.append(f'    _zag_print("A|{qid}|");_zag_print(_zag_i64_to_str(d as i64));')
    lines.append('    _zag_print("|");_zag_print(w.*.chosen);')
    lines.append('    _zag_print("|T");_zag_print(_zag_i64_to_str(w.*.tamper as i64));')
    lines.append('    _zag_println("");')
    lines.append("    return;")
    lines.append("}")


def emit_qb(lines, qid, exp_verdict, exp_chosen, exp_rule):
    lines.append(f"fn qb_{qid}() i32 {{")
    lines.append("    let w:*MwF=mw_new();")
    lines.append(f"    feedB_{qid}(w);")
    lines.append("    let v:i32=mw_deliberate(w);")
    lines.append("    mw_fact_end(w);")
    lines.append('    _zag_print("V|B|");')
    lines.append(f'    _zag_print("{qid}|");')
    lines.append('    if(v==1){_zag_print("CONVERGE|");}else{_zag_print("WITHHOLD|");}')
    lines.append('    _zag_print(w.*.chosen);_zag_print("|");')
    lines.append('    _zag_print(w.*.rule);_zag_print("|");')
    lines.append('    _zag_print(mw_chain(w));_zag_print("|");')
    lines.append('    _zag_print(mw_supp(w, w.*.chosen));_zag_print("|");')
    lines.append('    _zag_print(mw_head(w));_zag_println("");')
    lines.append("    let ok:i32=1;")
    if exp_verdict == "CONVERGE":
        lines.append("    if(v!=1){ok=0;}")
        lines.append(f'    if(mw_equal(w.*.chosen, "{zg(exp_chosen)}")!=1){{ok=0;}}')
    else:
        lines.append("    if(v!=2){ok=0;}")
    lines.append(f'    if(mw_equal(w.*.rule, "{exp_rule}")!=1){{ok=0;}}')
    lines.append("    return ok;")
    lines.append("}")


def main():
    golds = json.load(open(os.path.join(BASE, "golds.json")))
    kept = golds["kept"]  # qid -> {"gold": ..., "why": ...}
    lines = ["// mw_cases.zag — GENERATED by gen_mw.py. Do not hand-edit.",
             "// Live envelopes frozen in live/; golds frozen in golds.json.",
             '// Expectations derived by the frozen PREREG §4 rules.',
             '@import("ws2_sense.zag")', '@import("mw_sense.zag")', ""]
    manifest = []
    disc_log = []
    qids = []
    for qid, question, temporal, cands in QUESTIONS:
        if qid not in kept:
            manifest.append(f"{qid}: DROPPED ({kept.get(qid, {}).get('drop_cause', 'not in golds.json')})")
            continue
        results, disc = load_results(qid, cands)
        for d in disc:
            disc_log.append(f"{qid}|{d['domain']}|{(d['title'] or '')[:80]}")
        verdict, chosen, rule, cls, candtab = derive(temporal, results)
        gold = kept[qid]["gold"]
        emit_feedA(lines, qid, question, results)
        emit_feedB(lines, qid, question, temporal, results)
        emit_qa(lines, qid)
        emit_qb(lines, qid, verdict, chosen, rule)
        qids.append(qid)
        ct = ";".join(f"{a}:{n}:{r}" for a, n, r in candtab)
        manifest.append(
            f"{qid}: class={cls} gold={gold} expected={verdict} "
            f"chosen={chosen or '-'} rule={rule} cands=[{ct}] n_rel={len(results)}")
    lines.append("fn run_a_all() void {")
    for qid in qids:
        lines.append(f"    qa_{qid}();")
    lines.append("    return;")
    lines.append("}")
    lines.append("fn run_b_all() i32 {")
    lines.append("    let p:i32=1;")
    for qid in qids:
        lines.append(f"    if(qb_{qid}()!=1){{p=0;}}")
    lines.append("    return p;")
    lines.append("}")
    open(OUT, "w").write("\n".join(lines) + "\n")
    os.makedirs(os.path.join(BASE, "runs"), exist_ok=True)
    open(os.path.join(BASE, "runs", "CASE_MANIFEST.txt"), "w").write("\n".join(manifest) + "\n")
    open(os.path.join(BASE, "runs", "discovery.log"), "w").write("\n".join(disc_log) + "\n")
    print(f"wrote {OUT}: {len(lines)} lines, {len(qids)} questions kept")
    print("\n".join(manifest))


if __name__ == "__main__":
    main()
