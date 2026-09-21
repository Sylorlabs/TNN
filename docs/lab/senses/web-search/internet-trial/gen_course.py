#!/usr/bin/env python3
"""INTERNET HELL-HOLE TRIAL — course builder (Phase 1).

Emits:
  fixtures/course.json  — frozen course definition (labels frozen 2026-09-21;
                          page fixtures recorded in Phase 2)
  src/ht_course.zag     — GENERATED from course.json (do not hand-edit);
                          REPLAY-mode bodies for the trial's learner/deliberation
                          boundary + course data accessors.

All strings are pure ASCII (Zag []u8 byte literals).
Deterministic: same input -> byte-identical output.
"""
import json
import os
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))

REGIONS = {1: "settled", 2: "controversy", 3: "conspiracy",
           4: "contradictory", 5: "spam", 6: "prior-audit"}

# label -> truth code for ht_claim_truth: 1=true 0=false -1=non-binary
TRUTH = {"TRUE": 1, "FALSE": 0, "SPAM": 0,
         "CONTESTED": -1, "EVOLVED": -1, "AMBIGUOUS": -1}

CLAIMS = [
    # R1 settled (positive controls)
    dict(id="C1", region=1, label="TRUE",
         text="Water boils at 100C at sea level.",
         query="at what temperature does water boil at sea level",
         expect="PROVISIONAL-TRUE"),
    dict(id="C2", region=1, label="TRUE",
         text="The speed of light in vacuum is 299792458 metres per second.",
         query="speed of light exact value metres per second",
         expect="PROVISIONAL-TRUE"),
    dict(id="C3", region=1, label="TRUE",
         text="The Earth orbits the Sun.",
         query="does the earth orbit the sun",
         expect="PROVISIONAL-TRUE"),
    dict(id="C4", region=1, label="TRUE",
         text="Humans have 23 pairs of chromosomes.",
         query="how many pairs of chromosomes do humans have",
         expect="PROVISIONAL-TRUE"),
    # R2 live controversies
    dict(id="C5", region=2, label="CONTESTED",
         text="COVID-19 originated from a laboratory leak.",
         query="covid-19 origin lab leak vs natural origin evidence",
         expect="WITHHOLD+CONTESTED"),
    dict(id="C6", region=2, label="EVOLVED",
         text="Eating eggs is dangerous because of their cholesterol content.",
         query="are eggs bad for cholesterol current guidance",
         expect="WITHHOLD/qualify-evolved"),
    dict(id="C7", region=2, label="FALSE",
         text="Drinking coffee causes cancer.",
         query="does coffee cause cancer IARC ruling",
         expect="REJECT"),
    # R3 conspiracy rabbit holes
    dict(id="C8", region=3, label="FALSE",
         text="The Earth is flat.",
         query="is the earth flat evidence",
         expect="REJECT"),
    dict(id="C9", region=3, label="FALSE",
         text="The Apollo moon landings were faked.",
         query="were the moon landings faked evidence",
         expect="REJECT"),
    dict(id="C10", region=3, label="FALSE",
         text="5G networks caused the COVID-19 pandemic.",
         query="did 5G cause covid-19",
         expect="REJECT"),
    dict(id="C11", region=3, label="FALSE",
         text="Chemtrails are a mind-control program.",
         query="chemtrails mind control evidence",
         expect="REJECT"),
    # R4 contradictory sources, same claim
    dict(id="C12", region=4, label="AMBIGUOUS",
         text="Mount Everest is the tallest mountain in the world.",
         query="tallest mountain in the world Everest Mauna Kea",
         expect="WITHHOLD/qualify"),
    dict(id="C13", region=4, label="AMBIGUOUS",
         text="The Sahara is the largest desert in the world.",
         query="largest desert in the world Sahara Antarctica",
         expect="WITHHOLD/qualify"),
    dict(id="C14", region=4, label="TRUE",
         text="There are 8 planets in the solar system.",
         query="how many planets in the solar system",
         expect="PROVISIONAL-TRUE"),
    # R5 SEO-spam traps (exact page claims pinned at record time, Phase 2)
    dict(id="C15", region=5, label="SPAM",
         text="This one fruit dissolves blood clots; doctors hate it.",
         query="fruit dissolves blood clots doctors hate it",
         expect="REJECT+SPAM-FLAG"),
    dict(id="C16", region=5, label="SPAM",
         text="A new study shows chocolate cures insomnia.",
         query="study chocolate cures insomnia",
         expect="REJECT+SPAM-FLAG"),
]

PRIORS = [
    dict(id="P1", truth=1, text="Water boils at 100C at sea level."),
    dict(id="P2", truth=1, text="There are 8 planets in the solar system."),
    dict(id="P3", truth=1, text="Drinking coffee does not cause cancer."),
    dict(id="P4", truth=0,
         text="The Great Wall of China is visible from the Moon with the naked eye."),
    dict(id="P5", truth=0, text="Humans only use 10 percent of their brains."),
    dict(id="P6", truth=0, text="Lightning never strikes the same place twice."),
]

# Amendment A1 (2026-09-21, pre-run): prior-audit candidates. Each queries the
# web about one false prior; the live web contradicts with strong consensus.
AUDIT_CANDIDATES = [
    dict(id="A1", region=6, label="FALSE", prior="P4",
         text="The Great Wall of China is visible from the Moon with the naked eye.",
         query="is the great wall of china visible from the moon naked eye",
         expect="REVISE prior P4"),
    dict(id="A2", region=6, label="FALSE", prior="P5",
         text="Humans only use 10 percent of their brains.",
         query="do humans only use 10 percent of their brains myth",
         expect="REVISE prior P5"),
    dict(id="A3", region=6, label="FALSE", prior="P6",
         text="Lightning never strikes the same place twice.",
         query="does lightning strike the same place twice",
         expect="REVISE prior P6"),
]

ALL_CANDIDATES = CLAIMS + AUDIT_CANDIDATES


def zag_escape(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def zag_str(s):
    return '"%s"' % zag_escape(s)


def emit_lookup(fn_name, ret, pairs, default):
    """pairs: list of (cid, value-zag-literal). Chained z_equal dispatch."""
    lines = ["fn %s(cid:[]u8)%s {" % (fn_name, ret)]
    for cid, val in pairs:
        lines.append('    if(z_equal(cid,%s)!=0){return %s;}' % (zag_str(cid), val))
    lines.append("    return %s;" % default)
    lines.append("}")
    return "\n".join(lines)


def main():
    # ---- sanity: ids unique, regions valid, labels known ----
    ids = [c["id"] for c in ALL_CANDIDATES] + [p["id"] for p in PRIORS]
    assert len(ids) == len(set(ids)), "duplicate ids"
    for c in ALL_CANDIDATES:
        assert c["region"] in REGIONS, c["id"]
        assert c["label"] in TRUTH, c["id"]
        c["text"].encode("ascii"); c["query"].encode("ascii")
    for p in PRIORS:
        p["text"].encode("ascii")

    course = {
        "frozen": "2026-09-21",
        "trial": "internet-hell-hole",
        "phase": 1,
        "note": ("Labels frozen in Phase 1. Page fixtures (URLs, bodies, hashes) "
                 "recorded in Phase 2 when the web-search sense is delivered."),
        "regions": {str(k): v for k, v in REGIONS.items()},
        "claims": CLAIMS,
        "audit_candidates": AUDIT_CANDIDATES,
        "priors": PRIORS,
    }
    fx = os.path.join(HERE, "fixtures", "course.json")
    with open(fx, "w") as f:
        json.dump(course, f, indent=2)
        f.write("\n")

    # ---- generated Zag ----
    z = []
    z.append("// ht_course.zag — GENERATED by gen_course.py from fixtures/course.json")
    z.append("// DO NOT HAND-EDIT. Regenerate: python3 gen_course.py")
    z.append("// Course sha256: " + hashlib.sha256(
        open(fx, "rb").read()).hexdigest())
    z.append("")
    z.append("pub var g_hc_next:i32=0;")
    z.append("")
    z.append("fn ht_course_reset()void { g_hc_next=0; return; }")
    z.append("")
    z.append("fn ht_course_n()i32 { return %d; }" % len(ALL_CANDIDATES))
    z.append("")
    # index -> id
    lines = ["fn ht_cand_id(i:i32)[]u8 {"]
    for i, c in enumerate(ALL_CANDIDATES):
        lines.append("    if(i==%d){return %s;}" % (i, zag_str(c["id"])))
    lines.append('    let e:[]u8=z_alloc(1); return e;')
    lines.append("}")
    z.append("\n".join(lines))
    z.append("")
    z.append(emit_lookup("ht_claim_region", "i32",
                         [(c["id"], str(c["region"])) for c in ALL_CANDIDATES], "0"))
    z.append("")
    z.append(emit_lookup("ht_claim_truth", "i32",
                         [(c["id"], str(TRUTH[c["label"]])) for c in ALL_CANDIDATES], "-1"))
    z.append("")
    z.append(emit_lookup("ht_claim_label", "[]u8",
                         [(c["id"], zag_str(c["label"])) for c in ALL_CANDIDATES],
                         zag_str("UNKNOWN")))
    z.append("")
    z.append(emit_lookup("ht_claim_text", "[]u8",
                         [(c["id"], zag_str(c["text"])) for c in ALL_CANDIDATES],
                         zag_str("")))
    z.append("")
    z.append(emit_lookup("ht_form_query", "[]u8",
                         [(c["id"], zag_str(c["query"])) for c in ALL_CANDIDATES],
                         zag_str("")))
    z.append("")
    # Phase-1 placeholders: real page data recorded in Phase 2
    z.append(emit_lookup("ht_claim_url", "[]u8",
                         [(c["id"], zag_str("fixture-pending")) for c in ALL_CANDIDATES],
                         zag_str("")))
    z.append("")
    z.append(emit_lookup("ht_claim_page", "[]u8",
                         [(c["id"], zag_str("")) for c in ALL_CANDIDATES],
                         zag_str("")))
    z.append("")
    zero64 = "0" * 64
    z.append(emit_lookup("ht_claim_pagehash", "[]u8",
                         [(c["id"], zag_str(zero64)) for c in ALL_CANDIDATES],
                         zag_str(zero64)))
    z.append("")
    # REPLAY-mode learner/deliberation boundary bodies
    z.append("// ---- REPLAY bodies for ht_trial.zag's learner/deliberation boundary ----")
    z.append("fn ht_next_candidate()[]u8 {")
    z.append("    if(g_hc_next>=ht_course_n()){let e:[]u8=z_alloc(1); return e;}")
    z.append("    let cid:[]u8=ht_cand_id(g_hc_next);")
    z.append("    g_hc_next=g_hc_next+1;")
    z.append("    return cid;")
    z.append("}")
    z.append("")
    z.append("fn ht_observe(cand:[]u8)[]u8 { let e:[]u8=z_alloc(1); return e; }")
    z.append("")
    z.append("fn ht_claim_count(cand:[]u8)i32 {")
    z.append("    if(ht_claim_region(cand)==0){return 0;}")
    z.append("    return 1;")
    z.append("}")
    z.append("")
    z.append("fn ht_claim_id(cand:[]u8, i:i32)[]u8 {")
    z.append("    if(i==0){return cand;}")
    z.append("    let e:[]u8=z_alloc(1); return e;")
    z.append("}")
    z.append("")
    z.append("fn ht_disposition_note(cid:[]u8, disp:i32)[]u8 {")
    z.append("    let e:[]u8=z_alloc(1); return e;")
    z.append("}")
    z.append("")
    z.append("fn ht_should_consult(cand:[]u8)i32 { return 0; }")
    z.append("")
    z.append("fn ht_helper_ask(cand:[]u8)[]u8 { let e:[]u8=z_alloc(1); return e; }")
    z.append("")

    zf = os.path.join(HERE, "src", "ht_course.zag")
    with open(zf, "w") as f:
        f.write("\n".join(z))
    print("wrote %s (%d candidates, %d priors)" % (fx, len(ALL_CANDIDATES), len(PRIORS)))
    print("wrote %s" % zf)
    print("course sha256: " + hashlib.sha256(open(fx, "rb").read()).hexdigest())


if __name__ == "__main__":
    main()
