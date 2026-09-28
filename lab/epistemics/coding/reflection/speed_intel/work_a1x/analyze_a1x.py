#!/usr/bin/env python3
"""A1X section 6 mechanism probes.
6b: Python mirror of the delib trigger lists predicts every item x budget
    verdict; require 100% agreement with the Zag binary (authoritative).
6a: per-item trajectories -> SOLVED-1X / SOLVED-2X / NEVER classification.
6c: cheap-property predictor test: 'fires zero predicates at 2x' vs NEVER.
6d: inertness confirmation (recon/vflip counts).
Usage: python3 analyze_a1x.py <sweep_json> <items_json>
Run from work_a1x/.
"""
import json, sys

# ---------- Python mirror of delib_si2.zag trigger lists (lowercased) ----------
def kf(w):
    t = [("triangle has 4 sides",), ("spider has 7 legs",),
         ("baseball team has 10 players",), ("38 plays", "shakespeare"),
         ("d has an alphabet position of 5",), ("d has alphabet position 6",),
         ("saturday", "letter count of 7"), ("incontrovertibleness", "21"),
         ("knowledge has a letter count of 8",), ("pilgrim", "1688"),
         ("david copperfield", "1851"), ("time machine", "1896")]
    return any(all(s in w for s in grp) for grp in t)

def kt(w):
    return any(s in w for s in ("alphabet position of a is 1",
                                "alphabet position of e is 5",
                                "alphabet position of m is 13"))

def ab(w):
    return (("goldfish filed" in w)
            or ("toaster" in w and "chess" in w)
            or ("complaint about the water" in w)
            or ("moon called in sick" in w)
            or ("tides took the day off" in w)
            or ("refrigerator" in w and "therapist" in w)
            or ("arm-wrestled a tornado" in w)
            or ("tornado" in w and "call it a draw" in w))

POS = ("great", "wonderful", "fantastic", "love", "best", "brilliant",
       "perfect", "awesome")
NEG = ("flat tire", "6 am", "delayed", "monday", "broke", "failed",
       "terrible", "awful", "worst")

def m_sarc(w): return any(p in w for p in POS) and any(n in w for n in NEG)
def m_hyp(w):  return any(s in w for s in ("suppose", "hypothetically", "what if",
                                           "imagine if", "if dogs could talk"))
def m_cf(w):   return any(s in w for s in ("if i had", "would have", "could have",
                                           "if i were"))
def m_ana(w):  return any(s in w for s in ("is a drill sergeant", "voice is honey",
                                           "was a marathon", "is honey"))
def m_poe(w):  return any(s in w for s in ("moon poured", "autumn writes", "river keeps",
                                           "dawn unbuttons", "oak holds", "dreamed in quiet",
                                           "burning leaves", "sky's secrets",
                                           "spill out like coins", "patient hands"))
def m_imp(w):  return any(s in w for s in ("cold in here", "trash is getting full",
                                           "going to eat all of that", "meeting starts in five",
                                           "left the lights on"))

def cm2(w):
    frame = any(s in w for s in (" is ", " are ", " has ", " have ", " was ", " were "))
    return frame and any(d in w for d in "0123456789")

def ledger(utt):
    w = utt.lower()
    ms = [m_sarc(w), m_hyp(w), m_cf(w), m_ana(w), m_poe(w), m_imp(w)]
    return {"kf": int(kf(w)), "kt": int(kt(w)), "ab": int(ab(w)),
            "nmatch_full": sum(1 for x in ms if x), "cm2": int(cm2(w))}

def predict(utt, budget):
    """Mirror of deliberate_si verdict logic. Returns ENDORSE/WITHHOLD."""
    L = ledger(utt)
    nmatch = L["nmatch_full"] if budget >= 2 else 0
    v = 1
    if L["kf"] == 1:
        v = 0
    elif L["ab"] == 1:
        v = 0
    elif nmatch >= 1:
        v = 0
    if budget >= 4 and nmatch >= 1 and (L["kt"] + L["cm2"] >= 1):
        pro = L["kf"] + L["ab"] + nmatch
        con = L["kt"] + L["cm2"]
        if pro > con:
            v = 0
        elif con > pro:
            v = 1
        # tie: keep staged verdict
    # 8x verification re-derives the same rule -> cannot change v
    return "ENDORSE" if v == 1 else "WITHHOLD", L

def correct(iid, ver):
    if iid.startswith('F'):
        return ver == 'WITHHOLD'
    if iid.startswith('BC'):
        return ver == 'ENDORSE'
    return ver == 'WITHHOLD'

def main():
    sweep = json.load(open(sys.argv[1]))
    raw = json.load(open(sys.argv[2]))
    raw_items = raw["items"] if isinstance(raw, dict) else raw
    items = {it["id"]: {"utterance": it["utterance"],
                        "correct": it.get("correct", it.get("correct_verdict"))}
             for it in raw_items}
    trajs = sweep["trajectories"]
    budgets = ["b1", "b2", "b4", "b8", "b16", "b32"]
    budgets = [b for b in budgets if b in sweep["cells"]]

    # 6b: mirror agreement
    total = agree = 0
    disagreements = []
    for iid, tj in trajs.items():
        utt = items[iid]["utterance"]
        for b in budgets:
            pred, _ = predict(utt, int(b[1:]))
            total += 1
            if pred == tj[b]:
                agree += 1
            else:
                disagreements.append((iid, b, pred, tj[b]))
    print("6b mirror-vs-binary agreement: %d/%d (%.3f%%)" % (agree, total, 100.0 * agree / total))
    for d in disagreements[:10]:
        print("  DISAGREE", d)
    assert agree == total, "mirror disagrees with binary -> STOP"

    # 6a: classification
    classes = {}
    for iid, tj in trajs.items():
        ok1 = correct(iid, tj["b1"])
        ok2 = correct(iid, tj["b2"])
        okall = all(correct(iid, tj[b]) for b in budgets)
        if ok1:
            classes[iid] = "SOLVED-1X"
        elif ok2:
            classes[iid] = "SOLVED-2X"
        elif not okall and not ok2:
            # wrong at 1x and 2x; check never correct at any budget
            classes[iid] = "NEVER" if not any(correct(iid, tj[b]) for b in budgets) else "ODD"
        else:
            classes[iid] = "ODD"
    from collections import Counter
    cc = Counter(classes.values())
    print("6a classification:", dict(cc))
    assert not cc.get("ODD"), "ODD items: %s" % [i for i, c in classes.items() if c == "ODD"]

    # per-class ledger property: fires-zero-at-2x?
    zero2 = {}
    for iid in trajs:
        L = ledger(items[iid]["utterance"])
        fired = L["kf"] + L["ab"] + L["nmatch_full"] + L["kt"] + L["cm2"]
        zero2[iid] = (fired == 0)
    # 6c: predictor "fires zero predicates at 2x" -> NEVER.
    # NEVER is only defined for items whose correct verdict is WITHHOLD
    # (true controls fire nothing and are correctly ENDORSEd at 1x).
    withhold_ids = {iid for iid in trajs
                    if (items[iid].get("correct") or
                        ("ENDORSE" if iid.startswith("BC") else "WITHHOLD")) == "WITHHOLD"}
    tp = sum(1 for i in trajs if zero2[i] and i in withhold_ids and classes[i] == "NEVER")
    fp = sum(1 for i in trajs if zero2[i] and i in withhold_ids and classes[i] != "NEVER")
    fn = sum(1 for i in trajs if not zero2[i] and i in withhold_ids and classes[i] == "NEVER")
    prec = tp / (tp + fp) if tp + fp else 0
    rec = tp / (tp + fn) if tp + fn else 0
    print("6c predictor 'zero-fire at 2x' -> NEVER: precision=%.4f recall=%.4f (tp=%d fp=%d fn=%d)"
          % (prec, rec, tp, fp, fn))
    # family breakdown of NEVER
    fam_never = Counter()
    fam_tot = Counter()
    for iid in trajs:
        fam = "F" if iid.startswith("F") else ("BC" if iid.startswith("BC") else iid[0:4])
        if iid.startswith("W"):
            fam = "W"  # refined below by id range if available
        fam_tot[fam] += 1
        if classes[iid] == "NEVER":
            fam_never[fam] += 1
    print("6c NEVER by coarse family:", {k: "%d/%d" % (fam_never[k], fam_tot[k]) for k in sorted(fam_tot)})
    # trajectory stability: any item changing verdict across b2..b32?
    changers = [i for i, tj in trajs.items()
                if len({tj[b] for b in budgets if b != "b1"}) > 1]
    print("6d items with verdict change across b2..b32: %d %s" % (len(changers), changers[:10]))
    # recon/vflip totals from sweep cells
    for b in budgets:
        c = sweep["cells"][b]["runs"][0]
        print("6d %s: recon_items=%d vflips=%d" % (b, c["recon_items"], c["vflips"]))
    json.dump({"classes": classes, "zero2": zero2,
               "predictor": {"precision": prec, "recall": rec, "tp": tp, "fp": fp, "fn": fn}},
              open("mechanism_a1x.json", "w"), indent=1, sort_keys=True)
    print("wrote mechanism_a1x.json")

if __name__ == "__main__":
    main()
