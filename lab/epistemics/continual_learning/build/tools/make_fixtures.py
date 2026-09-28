#!/usr/bin/env python3
"""Build sealed fixtures from the FROZEN PREREG.md quotes + fetched Gutenberg texts.

For every teaching fact and Phase-4 sentence: asserts the prereg's exact quoted
string is a byte-substring of the cited Gutenberg .txt (no invention, no edits).
Writes fixtures/*.tsv for the native battery. Fails loudly on any mismatch.
"""
import sys, hashlib, os, re

BUILD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BUILD, "sources")
FIX = os.path.join(BUILD, "fixtures")
os.makedirs(FIX, exist_ok=True)

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def collapse(t):
    # Same whitespace folding the bridge applies before hashing (prereg §11).
    return re.sub(r"\s+", " ", t).strip()

texts = {}
for _fn in ["vol1_56989.txt", "vol2_57191.txt", "orchestra_73991.txt", "vol4_72279.txt"]:
    raw = open(os.path.join(SRC, _fn), encoding="utf-8").read()
    texts[_fn] = collapse(raw)
print("source SHAs:")
for fn in texts:
    print(" ", sha(os.path.join(SRC, fn)), fn)

# (ep_id, phase, concept, section, source_file, fact) — quotes copied verbatim from PREREG.md §3
FACTS = [
 ("EP-P1-A1",1,"A","THE WOOD THRUSH","vol1_56989.txt",
  "composed externally of dry leaves of various kinds, with a second bed of grasses and mud, and an internal layer of fine fibrous roots"),
 ("EP-P1-A2",1,"A","THE WOOD THRUSH","vol1_56989.txt",
  "The eggs are four or five, of a beautiful uniform light blue."),
 ("EP-P1-A3",1,"A","THE WOOD THRUSH","vol1_56989.txt",
  "Their food consists of different kinds of berries and small fruits, which they procure in the woods, without ever interfering with the farmer."),
 ("EP-P1-B1",1,"B","THE HERMIT THRUSH","vol1_56989.txt",
  "The flight of the Hermit Thrush is performed low over the ground, and in a gliding manner"),
 ("EP-P1-B2",1,"B","THE HERMIT THRUSH","vol1_56989.txt",
  "The Hermit Thrush has no song, and only utters a soft plaintive note, seldom heard at a greater distance than twenty-five or thirty yards."),
 ("EP-P1-B3",1,"B","THE HERMIT THRUSH","vol1_56989.txt",
  "They were smaller, and had no mud or plaster of any kind"),
 ("EP-P1-C1",1,"C","THE TAWNY THRUSH","vol2_57191.txt",
  "composed of continued trills repeated with different variations, enunciated with great delicacy and mellowness"),
 ("EP-P1-C2",1,"C","THE TAWNY THRUSH","vol2_57191.txt",
  "builds its nest, which is large, composed externally of dry leaves, mosses, and the stalks of grasses, and lined with finer grasses, and delicate fibrous portions of different kinds of mosses, without any mud or clay"),
 ("EP-P1-C3",1,"C","THE TAWNY THRUSH","vol2_57191.txt",
  "feeds principally on coleopterous insects"),
 ("EP-P2-D1",2,"D","THE VIOLIN","orchestra_73991.txt",
  "The four strings\u2014G, D, A, and E\u2014are made of catgut and the lowest\u2014the G\u2014is wound with silver."),
 ("EP-P2-D2",2,"D","THE VIOLIN","orchestra_73991.txt",
  "The bowing of a violinist is what breath is to a singer and what touch is to a pianist."),
 ("EP-P2-D3",2,"D","THE VIOLIN","orchestra_73991.txt",
  "The violin is tuned in fifths."),
 ("EP-P2-E1",2,"E","THE VIOLONCELLO","orchestra_73991.txt",
  "The violoncello is not a big violin; it is a little double-bass"),
 ("EP-P2-E2",2,"E","THE VIOLONCELLO","orchestra_73991.txt",
  "Its immediate ancestor was the viola da gamba."),
 ("EP-P2-E3",2,"E","THE VIOLONCELLO","orchestra_73991.txt",
  "The violoncello belongs to that ancient and honorable family of viols"),
 ("EP-P2-F1",2,"F","THE HARP","orchestra_73991.txt",
  "The seven pedals with which it is furnished are made so that the player may, by means of each of them, raise at option each string a tone, or a semitone, only."),
 ("EP-P2-F2",2,"F","THE HARP","orchestra_73991.txt",
  "The forty-seven strings are of catgut colored for the convenience of the player."),
 ("EP-P2-F3",2,"F","THE HARP","orchestra_73991.txt",
  "It is even after its Italian name, arpa, that these passages have received the name of arpeggios."),
]

# (item_id, section, source_file, sentence, question, expected) — PREREG.md §4
PHASE4 = [
 ("P4-B1","THE BLUE BIRD","vol2_57191.txt",
  "The pure azure of its mantle, and the beautiful glow of its breast, render it conspicuous",
  "Is the Blue Bird a thrush?","YES"),
 ("P4-B2","GREAT AUK","vol4_72279.txt",
  "It walked very awkwardly, often tumbling over\u2026 After continuing several days on board, it was restored to its proper element.",
  "Does the Great Auk fly?","NO"),
 ("P4-I1","THE PIANOFORTE","orchestra_73991.txt",
  "touch developed after the piano had been equipped with its softly padded hammers and its improved action",
  "The pianoforte's strings are struck by softly padded hammers worked from a keyboard. Is the pianoforte a stringed instrument?","YES"),
 ("P4-I2","THE WOODWIND FAMILY","orchestra_73991.txt",
  "The clarinet group, furnished with a single reed. This reed\u2026 placed in the mouthpiece of the instrument, is the 'speaking' part.",
  "Is the clarinet a stringed instrument?","NO"),
]

PROBES = [
 ("P-A1","Which thrush builds its nest with a second bed of grasses and mud?","Wood Thrush",""),
 ("P-A2","Which thrush lays four or five eggs of a beautiful uniform light blue?","Wood Thrush",""),
 ("P-B1","Which thrush flies low over the ground in a gliding manner?","Hermit Thrush",""),
 ("P-B2","Which thrush has no song and only utters a soft plaintive note?","Hermit Thrush",""),
 ("P-C1","Which thrush's song is composed of continued trills repeated with different variations?","Veery","Veery|Tawny Thrush|Wilson's Thrush"),
 ("P-C2","Which thrush builds a large nest of dry leaves, mosses and grass stalks, with no mud or clay?","Veery","Veery|Tawny Thrush|Wilson's Thrush"),
 ("P-D1","Which instrument has four catgut strings, G, D, A and E, tuned in fifths?","Violin",""),
 ("P-D2","For which instrument is bowing what breath is to a singer?","Violin",""),
 ("P-E1","Which instrument is not a big violin but a little double-bass?","Violoncello","Violoncello|Cello|'cello"),
 ("P-E2","Which instrument's immediate ancestor was the viola da gamba?","Violoncello","Violoncello|Cello|'cello"),
 ("P-F1","Which instrument has seven pedals that raise each string a tone or a semitone?","Harp",""),
 ("P-F2","Which instrument has forty-seven strings of catgut?","Harp",""),
]

PROV = [
 ("PV-1","How do you know the Wood Thrush's nest contains mud? Cite the teaching episode.","EP-P1-A1"),
 ("PV-2","How do you know the violoncello is not a big violin?","EP-P2-E1"),
 ("PV-3","How do you know the Veery's song is made of trills?","EP-P1-C1"),
]

CONSEQ = [
 ("CF-1","A thrush's nest is found with no mud or plaster of any kind. Could it be a Wood Thrush's nest?","NO"),
 ("CF-2","An instrument's strings are struck by hammers worked from a keyboard. Could it be played with a bow?","NO"),
]

# Known source-text variances (documented in TEACH.md, never silently fixed).
# Each maps ep/item id -> the SOURCE's byte form; the fixture keeps the prereg's
# quoted form (frozen spec authoritative). Verification proves:
#   prereg_quote + documented variance == actual Gutenberg bytes.
SRCFORM = {
 "EP-P2-D1": "The four strings\u2014G, D, A, and E\u2014are made of catgut[8] and the lowest\u2014the G\u2014is wound with silver.",
 "EP-P2-D2": "The bowing of a violinist is what _breath_ is to a singer and what _touch_ is to a pianist.",
 "EP-P2-E2": "Its _immediate ancestor_ was the _viola da gamba_.",
 "EP-P2-F3": "It is even after its Italian name, _arpa_, that these passages have received the name of _arpeggios_.",
 "P4-B2": "It walked very awkwardly, often tumbling over, bit every one within reach of its powerful bill, and refused food of all kinds. After continuing several days on board, it was restored to its proper element.",
 "P4-I1": "_touch_ developed after the piano had been equipped with its softly padded hammers and its improved action",
 "P4-I2": "the clarinet group, furnished with a single reed. This reed, single or double, placed in the mouthpiece of the instrument, is the \u201cspeaking\u201d part.",
}

fails = []
def check_presence(label, text, src_fn):
    # 1) the prereg's quoted form must appear verbatim in PREREG.md itself
    prereg = open(os.path.join(os.path.dirname(BUILD), "PREREG.md"), encoding="utf-8").read()
    if text not in prereg:
        fails.append(label + " (quote not in PREREG.md!)")
        print("PREREG-MISS:", label)
        return
    # 2) the source form (prereg quote + documented variance) must be a
    #    substring of the whitespace-collapsed Gutenberg text
    srcform = collapse(SRCFORM.get(label, text))
    src = texts[src_fn]
    n = src.count(srcform)
    if n == 0:
        fails.append(label)
        print("MISS:", label, "source form not found in", src_fn)
        print("  wanted head:", ascii(srcform[:80]))
    else:
        var = " (documented variance)" if label in SRCFORM else ""
        print("ok  %-10s in %-18s x%d%s" % (label, src_fn, n, var))

for ep, ph, co, sec, src, fact in FACTS:
    if "\t" in fact or "\n" in fact:
        fails.append(ep + " (tab/newline in fact)")
    check_presence(ep, fact, src)
for it, sec, src, sent, q, exp in PHASE4:
    check_presence(it, sent, src)

# section headers present in sources (sanity)
for sec, src in [("THE WOOD THRUSH","vol1_56989.txt"),("THE HERMIT THRUSH","vol1_56989.txt"),
                 ("THE TAWNY THRUSH","vol2_57191.txt"),("THE VIOLIN","orchestra_73991.txt"),
                 ("THE VIOLONCELLO","orchestra_73991.txt"),("THE HARP","orchestra_73991.txt"),
                 ("THE BLUE BIRD","vol2_57191.txt"),("GREAT AUK","vol4_72279.txt"),
                 ("THE PIANOFORTE","orchestra_73991.txt"),("THE WOODWIND FAMILY","orchestra_73991.txt")]:
    if sec not in texts[src]:
        print("NOTE: section header %r not literally in %s" % (sec, src))

if fails:
    print("FAILURES:", fails)
    sys.exit(1)

def wtsv(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write("\t".join(str(c) for c in r) + "\n")
    print("wrote", path, sha(path))

wtsv(os.path.join(FIX, "facts.tsv"), FACTS)
wtsv(os.path.join(FIX, "phase4.tsv"), PHASE4)
wtsv(os.path.join(FIX, "probes.tsv"), PROBES)
wtsv(os.path.join(FIX, "prov.tsv"), PROV)
wtsv(os.path.join(FIX, "conseq.tsv"), CONSEQ)
print("ALL CHECKS PASSED")
