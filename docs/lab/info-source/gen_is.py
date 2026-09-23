#!/usr/bin/env python3
"""gen_is.py — generate src/is_cases.zag for the info-source richness experiment.

Loads frozen live envelopes (live/*.json), extracts stated answers with the
frozen mechanical regexes (documented below), assembles the contested battery
from real recorded snippets, constructs the 2 spoof cases explicitly, and
emits per-fact feed + per-arm check functions.

Answer-extraction regexes (frozen; V checked before T):
"""
import hashlib
import json
import os
import re

BASE = os.path.expanduser("~/workspace/tnn-lab/docs/lab/info-source")
LIVE = os.path.join(BASE, "live")
OUT = os.path.join(BASE, "src", "is_cases.zag")

# fid, question, teacher T, canonical V, V_regex, T_regex, leg
FALSEHOODS = [
    ("F01", "What is the capital of France?", "Lyon", "Paris",
     r"\bparis\b", r"\blyon\b", 1),
    ("F02", "What is the chemical symbol for gold?", "Gd", "Au",
     r"\bau\b", r"\bgd\b", 1),
    ("F03", "Who wrote the novel 1984?", "Aldous Huxley", "George Orwell",
     r"george orwell", r"aldous huxley", 1),
    ("F04", "What is the largest planet in the solar system?", "Saturn", "Jupiter",
     r"\bjupiter\b", r"\bsaturn\b", 1),
    ("F05", "What is the speed of light in vacuum?", "150,000 km/s", "299,792 km/s",
     r"299[,\s.]?792", r"150[,\s.]?000\s*km", 1),
    ("F06", "Who was the first person to walk on the moon?", "Buzz Aldrin", "Neil Armstrong",
     r"neil armstrong", r"buzz aldrin", 1),
    ("F07", "What is the boiling point of water at sea level?", "90\u00b0C", "100\u00b0C",
     r"100\s*\u00b0?\s*c\b|212\s*\u00b0?\s*f\b|100 degrees celsius",
     r"90\s*\u00b0?\s*c\b|194\s*\u00b0?\s*f\b", 1),
    ("F08", "Who wrote Pride and Prejudice?", "Charlotte Bronte", "Jane Austen",
     r"jane austen", r"charlotte bront\u00eb?", 1),
    ("F09", "When was the Eiffel Tower built?", "1879", "1889",
     r"\b1889\b", r"\b1879\b", 1),
    ("F10", "What is the tallest building in the world in 2026?", "Shanghai Tower", "Burj Khalifa",
     r"burj khalifa", r"shanghai tower", 1),
    ("F11", "What is the capital of Japan?", "Osaka", "Tokyo",
     r"\btokyo\b", r"\bosaka\b", 1),
    ("F12", "What is the chemical symbol for silver?", "Si", "Ag",
     r"\bag\b", r"\bsi\b", 1),
]

UNKNOWN = [
    ("U01", "What is the capital of Burkina Faso?", "Ouagadougou", r"ouagadougou", 3),
    ("U02", "What is the chemical symbol for tungsten?", "W", r"\bw\b", 3),
    ("U03", "What is the deepest ocean trench in the world?", "Mariana Trench", r"mariana trench", 3),
    ("U04", "What is the currency of Switzerland?", "Swiss franc", r"swiss franc", 3),
]


def zc(s):
    # whitespace-collapsed form: EXACTLY what the Zag runtime string holds.
    # (zg() escaping is undone by the Zag literal parser, so the runtime bytes
    # equal zc(), not zg(). The tamper hash MUST be computed over zc().)
    return re.sub(r"\s+", " ", s).strip()


def zg(s):
    # literal-escaped form: what goes inside "..." in the .zag source.
    return zc(s).replace("\\", "\\\\").replace('"', '\\"')


def rhash(url, title, snippet):
    # hash over the EXACT runtime bytes (zc form). The Zag side recomputes
    # ws_result_hash over the unescaped runtime strings; hashing the escaped
    # literal bytes instead silently breaks on any " or \ in the data.
    body = (zc(url) + "\n" + zc(title) + "\n" + zc(snippet)).encode("utf-8")
    return hashlib.sha256(body).hexdigest()


def extract(text, vrx, trx):
    t = text.lower()
    if re.search(vrx, t):
        return "V"
    if trx and re.search(trx, t):
        return "T"
    return ""


def load_results(fid, vrx, trx, vcanon, tcanon, maxn=8):
    d = json.load(open(os.path.join(LIVE, fid + ".json")))
    out = []
    for r in d["results"][:maxn]:
        title, url, snip = r.get("title", ""), r.get("url", ""), r.get("snippet", "")
        dom = r.get("domain", "")
        if not (title and url):
            continue
        which = extract(title + " " + snip, vrx, trx)
        ans = vcanon if which == "V" else (tcanon if which == "T" else "")
        out.append({"domain": dom, "title": title, "url": url, "snippet": snip,
                    "answer": ans, "rel": 1 if ans else 0})
    return out


def emit_result(lines, r):
    lines.append(
        f'    ws_add_result(w, "{zg(r["domain"])}", "{zg(r["title"])}", '
        f'"{zg(r["snippet"])}", "{zg(r["url"])}", "{zg(r["answer"])}", {r["rel"]}, '
        f'"{rhash(r["url"], r["title"], r["snippet"])}");')


def feed_fn(lines, fid, leg, question, results):
    lines.append(f"fn feed_{fid}(w:*WsF) void {{")
    lines.append(
        f'    ws_fact_begin(w, {leg}, 0, "{fid}", "{zg(question)}", "", 2, 0);')
    for r in results:
        emit_result(lines, r)
    lines.append("    return;")
    lines.append("}")


def check_r0(lines, fid, teacher):
    lines.append(f"fn r0_{fid}(w:*WsF) i32 {{")
    lines.append(f'    ws_seed_installed(w, "{fid}", "{zg(teacher)}", 80);')
    lines.append(f'    let slot:i32=ws_t_find(w, "{fid}");')
    lines.append(f'    _zag_print("R0|{fid}|slot=");_zag_print(_zag_i64_to_str(slot as i64));_zag_println("");')
    lines.append("    if(slot<0){return 0;}")
    lines.append(f'    if(z_equal(ws_t_getv(w, slot), "{zg(teacher)}")!=1){{return 0;}}')
    lines.append("    return 1;")
    lines.append("}")


def check_r1(lines, fid, exp_disp, exp_chosen):
    lines.append(f"fn r1_{fid}(w:*WsF) i32 {{")
    lines.append("    ws_wire(w, 1, 1);")
    lines.append(f"    feed_{fid}(w);")
    lines.append("    let g:i32=w.*.gate;")
    lines.append("    let d:i32=ws_decide(w);")
    lines.append(f'    _zag_print("R1|{fid}|G");_zag_print(_zag_i64_to_str(g as i64));')
    lines.append('    _zag_print("|D");_zag_print(_zag_i64_to_str(d as i64));')
    lines.append('    _zag_print("|A");_zag_print(w.*.chosen);_zag_println("");')
    lines.append("    if(g!=1){return 0;}")
    lines.append(f"    if(d!={exp_disp}){{return 0;}}")
    if exp_disp in (1, 6):
        lines.append(f'    if(z_equal(w.*.chosen, "{zg(exp_chosen)}")!=1){{return 0;}}')
        lines.append(f'    let r:i32=ws_install(w, "{fid}", "{zg(exp_chosen)}", 80);')
        lines.append("    if(r!=8){return 0;}")
    lines.append(f'    if(ws_t_find(w, "{fid}")>=0){{return 0;}}')
    lines.append("    return 1;")
    lines.append("}")


def check_r2(lines, fid, exp_disp, exp_chosen, exp_stored):
    lines.append(f"fn r2_{fid}(w:*WsF) i32 {{")
    lines.append("    ws_wire(w, 2, 1);")
    lines.append(f"    feed_{fid}(w);")
    lines.append("    let g:i32=w.*.gate;")
    lines.append("    let d:i32=ws_decide(w);")
    lines.append(f'    _zag_print("R2|{fid}|G");_zag_print(_zag_i64_to_str(g as i64));')
    lines.append('    _zag_print("|D");_zag_print(_zag_i64_to_str(d as i64));')
    lines.append('    _zag_print("|A");_zag_print(w.*.chosen);_zag_println("");')
    lines.append("    if(g!=1){return 0;}")
    lines.append(f"    if(d!={exp_disp}){{return 0;}}")
    if exp_disp in (1, 6):
        lines.append(f'    if(z_equal(w.*.chosen, "{zg(exp_chosen)}")!=1){{return 0;}}')
        lines.append(f'    let r:i32=ws_install(w, "{fid}", "{zg(exp_chosen)}", 80);')
        lines.append("    if(r!=7){return 0;}")
        lines.append(f'    let slot:i32=ws_t_find(w, "{fid}");')
        lines.append("    if(slot<0){return 0;}")
        lines.append(f'    if(z_equal(ws_t_getv(w, slot), "{zg(exp_stored)}")!=1){{return 0;}}')
    else:
        lines.append(f'    if(ws_t_find(w, "{fid}")>=0){{return 0;}}')
    lines.append("    return 1;")
    lines.append("}")


def main():
    lines = ["// is_cases.zag — GENERATED by gen_is.py. Do not hand-edit.",
             "// Live envelopes frozen in live/; contested assembled from real",
             "// recorded snippets; spoofs constructed (labeled).",
             '@import("ws2_sense.zag")', ""]
    manifest = []
    # ---- B-FALSE ----
    for fid, q, t, v, vrx, trx, leg in FALSEHOODS:
        res = load_results(fid, vrx, trx, v, t)
        dv = {r["domain"] for r in res if r["answer"] == v}
        assert len(dv) >= 2, f"{fid}: only {len(dv)} V-domains"
        feed_fn(lines, fid, leg, q, res)
        check_r0(lines, fid, t)
        check_r1(lines, fid, 1, v)
        check_r2(lines, fid, 1, v, v)
        manifest.append(f"{fid}: V-domains={len(dv)} exp_disp=1 chosen={v}")
    # ---- B-UNKNOWN ----
    for fid, q, v, vrx, leg in UNKNOWN:
        res = load_results(fid, vrx, "", v, "")
        dv = {r["domain"] for r in res if r["answer"] == v}
        assert len(dv) >= 2, f"{fid}: only {len(dv)} V-domains"
        feed_fn(lines, fid, leg, q, res)
        check_r1(lines, fid, 1, v)
        check_r2(lines, fid, 1, v, v)
        manifest.append(f"{fid}: V-domains={len(dv)} exp_disp=1 chosen={v}")
    # ---- B-CONTEST (assembled from real recorded snippets) ----
    mtn = json.load(open(os.path.join(LIVE, "MTN.json")))["results"]
    ev1 = next(r for r in mtn if r["domain"] == "guinnessworldrecords.com")
    ev2 = next(r for r in mtn if r["domain"] == "muchbetteradventures.com")
    mk1 = next(r for r in mtn if r["domain"] == "tiktok.com")

    def mkres(r, answer):
        return {"domain": r["domain"], "title": r["title"], "url": r["url"],
                "snippet": r["snippet"], "answer": answer, "rel": 1}

    # C1: 1v1 -> WITHHOLD
    c1 = [mkres(ev1, "Mount Everest"), mkres(mk1, "Mauna Kea")]
    feed_fn(lines, "C1", 2, "What is the tallest mountain in the world?", c1)
    check_r1(lines, "C1", 2, "")
    check_r2(lines, "C1", 2, "", "")
    manifest.append("C1: 1v1 Everest/Mauna-Kea exp_disp=2")
    # C2: 2v1 -> PROVISIONAL_MAJORITY (mechanical; ambiguity noted in verdict)
    c2 = [mkres(ev1, "Mount Everest"), mkres(ev2, "Mount Everest"), mkres(mk1, "Mauna Kea")]
    feed_fn(lines, "C2", 2, "What is the tallest mountain in the world?", c2)
    check_r1(lines, "C2", 6, "Mount Everest")
    check_r2(lines, "C2", 6, "Mount Everest", "Mount Everest")
    manifest.append("C2: 2v1 Everest-majority exp_disp=6 chosen=Mount Everest")
    # C3: 2 DISTINCT domains agree (Paris) -> PROVISIONAL
    f01 = json.load(open(os.path.join(LIVE, "F01.json")))["results"]
    seen = set()
    paris = []
    for r in f01:
        if re.search(r"\bparis\b", (r["title"] + " " + r["snippet"]).lower()) \
                and r["domain"] not in seen:
            seen.add(r["domain"])
            paris.append(r)
        if len(paris) == 2:
            break
    assert len(paris) == 2, "need 2 distinct Paris domains for C3"
    c3 = [mkres(r, "Paris") for r in paris]
    feed_fn(lines, "C3", 2, "What is the capital of France?", c3)
    check_r1(lines, "C3", 1, "Paris")
    check_r2(lines, "C3", 1, "Paris", "Paris")
    manifest.append("C3: 2-agree Paris exp_disp=1")
    # C4: single source (Au) -> WITHHOLD
    f02 = json.load(open(os.path.join(LIVE, "F02.json")))["results"]
    au = next(r for r in f02 if re.search(r"\bau\b", (r["title"] + " " + r["snippet"]).lower()))
    c4 = [mkres(au, "Au")]
    feed_fn(lines, "C4", 2, "What is the chemical symbol for gold?", c4)
    check_r1(lines, "C4", 2, "")
    check_r2(lines, "C4", 2, "", "")
    manifest.append("C4: single-source Au exp_disp=2")
    # ---- B-SPOOF (CONSTRUCTED) ----
    s1 = [
        {"domain": "spoof-1.example", "title": "Atlantis Capital Guide",
         "url": "https://spoof-1.example/atlantis-capital",
         "snippet": "The capital of Atlantis is Poseidonia, the shining city.",
         "answer": "Poseidonia", "rel": 1},
        {"domain": "spoof-2.example", "title": "Visit Atlantis",
         "url": "https://spoof-2.example/visit",
         "snippet": "Poseidonia is the capital of Atlantis and its largest port.",
         "answer": "Poseidonia", "rel": 1},
    ]
    feed_fn(lines, "S1", 4, "What is the capital of Atlantis?", s1)
    check_r1(lines, "S1", 1, "Poseidonia")
    check_r2(lines, "S1", 1, "Poseidonia", "Poseidonia")
    manifest.append("S1: CONSTRUCTED unanimous spoof exp R1 disp=1/no-install, R2 installs")
    s2 = [
        {"domain": "spoof-1.example", "title": "Unobtainium data sheet",
         "url": "https://spoof-1.example/unobtainium",
         "snippet": "Unobtainium (Uo) is the lightest known metal.",
         "answer": "Uo", "rel": 1},
        {"domain": "spoof-2.example", "title": "Element guide",
         "url": "https://spoof-2.example/elements",
         "snippet": "The chemical symbol for unobtainium is Uo.",
         "answer": "Uo", "rel": 1},
    ]
    feed_fn(lines, "S2", 4, "What is the chemical symbol for unobtainium?", s2)
    check_r1(lines, "S2", 1, "Uo")
    check_r2(lines, "S2", 1, "Uo", "Uo")
    manifest.append("S2: CONSTRUCTED unanimous spoof exp R1 disp=1/no-install, R2 installs")

    open(OUT, "w").write("\n".join(lines) + "\n")
    open(os.path.join(BASE, "runs", "CASE_MANIFEST.txt"), "w").write("\n".join(manifest) + "\n")
    print(f"wrote {OUT}: {len(lines)} lines")
    print("\n".join(manifest))


if __name__ == "__main__":
    main()
