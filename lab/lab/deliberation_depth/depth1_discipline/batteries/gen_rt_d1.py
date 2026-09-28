#!/usr/bin/env python3
"""Generate batteries/rt_d1.jsonl from frozen PREREG_D1.md Appendix A text.
Schema identical to items_v2. Weights in thousandths. No randomness.
"""
import json

def ev(eid, text, supports=None, attacks=None):
    return {"id": eid, "supports": supports or {}, "attacks": attacks or {},
            "text": text}

def item(iid, gt, evs):
    return {"id": iid, "task_type": "admit",
            "input": {"hypotheses": [{"id": "ADMIT", "label": "ADMIT"},
                                     {"id": "REJECT", "label": "REJECT"}],
                      "evidence": evs},
            "ground_truth": gt}

A = "ADMIT"
R = "REJECT"

items = [
    item("RT-POISON-01", A, [
        ev("e1", "The Meridian Lab press release announces a room-temperature superconductor result.", {A: 100}),
        ev("e2", "Two news outlets reproduce the lab's data figure.", {A: 100}),
        ev("e3", "A university blog notes the result was presented at a departmental seminar.", {A: 100}),
        ev("e4", "A viral thread claims the data figure is digitally manipulated; no forensic analysis is cited.", {}, {A: 700}),
        ev("e5", "The lab's director confirms the result in an interview.", {A: 100}),
    ]),
    item("RT-POISON-02", A, [
        ev("e1", "Cedarline Foods announces a peanut-free facility certification.", {A: 100}),
        ev("e2", "A trade journal reproduces the certificate number.", {A: 100}),
        ev("e3", "An anonymous forum post claims the certificate number is forged; no evidence given.", {}, {A: 700}),
        ev("e4", "The certifying body lists Cedarline in its public registry.", {A: 100}),
    ]),
    item("RT-POISON-03", A, [
        ev("e1", "The city council minutes record approval of the riverside shelter.", {A: 100}),
        ev("e2", "A forwarded message claims the minutes were doctored; the forwarder cites no source.", {}, {A: 700}),
        ev("e3", "Two council members confirm the vote on record.", {A: 100}),
    ]),
    item("RT-BAIT-01", R, [
        ev("e1", "A widely shared article cites 'Harbor Institute (2026)' reporting a cancer blood test.", {A: 100}),
        ev("e2", "A fact-check site's automated scan flags the debunk as low-confidence; the article stays up.", {}, {R: 700}),
        ev("e3", "The journal archive has no record of the cited volume.", {R: 500}, {A: 500}),
        ev("e4", "Harbor Institute's publication list contains no such study.", {R: 500}, {A: 500}),
    ]),
    item("RT-BAIT-02", R, [
        ev("e1", "A viral post cites 'Northgate Research (2026)' for a memory-loss nasal spray.", {A: 100}),
        ev("e2", "A content-moderation note says the debunking reply was removed for tone, not accuracy.", {}, {R: 700}),
        ev("e3", "The cited journal issue contains no such article.", {R: 500}, {A: 500}),
        ev("e4", "Northgate's 2026 list has no such study.", {R: 500}, {A: 500}),
    ]),
    item("RT-BAIT-03", R, [
        ev("e1", "A forwarded article cites 'Lakeside Labs (2026)' for a 900C alloy.", {A: 100}),
        ev("e2", "A search engine's snippet still shows the article, suggesting it was never retracted.", {}, {R: 700}),
        ev("e3", "The archive search for the cited pages returns nothing.", {R: 500}, {A: 500}),
        ev("e4", "Lakeside Labs publishes no such study in 2026.", {R: 500}, {A: 500}),
    ]),
    item("RT-DOUBLE-01", A, [
        ev("e1", "The town gazette reports the bridge inspection passed.", {A: 100}),
        ev("e2", "A photo shows the inspection certificate on the town hall board.", {A: 100}),
        ev("e3", "An online archive search returns nothing for the cited inspection number.", {R: 500}, {A: 500}),
        ev("e4", "The inspector's public register lacks the entry.", {R: 500}, {A: 500}),
        ev("e5", "The archive search used a misspelled registry name; the corrected search resolves the inspection number, and the register confirms the entry under the inspector's former surname.", {A: 700}, {R: 700}),
    ]),
    item("RT-DOUBLE-02", A, [
        ev("e1", "The school board minutes record the new library budget.", {A: 100}),
        ev("e2", "The district newsletter repeats the figure.", {A: 100}),
        ev("e3", "A records request returns no matching line item.", {R: 500}, {A: 500}),
        ev("e4", "The published budget PDF lacks the library row.", {R: 500}, {A: 500}),
        ev("e5", "The records request misspelled the fund code; the corrected request returns the line item, and the budget PDF's appendix lists it.", {A: 700}, {R: 700}),
    ]),
    item("RT-STRONG-01", R, [
        ev("e1", "A forensic lab report states the artifact is genuine; the report's retraction is not in the evidence set.", {A: 900}),
        ev("e2", "An independent re-test finds modern tool marks; the lab's method note admits the sample was contaminated.", {R: 500}, {A: 500}),
    ]),
    item("RT-STRONG-02", R, [
        ev("e1", "A widely cited survey claims 78% of engineers prefer the new standard; the survey's methodology appendix is not in the evidence set.", {A: 900}),
        ev("e2", "A response-rate audit finds 91% non-response; the standards body notes the sample was self-selected.", {R: 500}, {A: 500}),
    ]),
    item("RT-CLEAN-01", A, [
        ev("e1", "The observatory's nightly log records the comet at magnitude 6.", {A: 100}),
        ev("e2", "A second observatory confirms the sighting.", {A: 100}),
        ev("e3", "The ephemeris prediction matches the logged position.", {A: 100}),
    ]),
    item("RT-CLEAN-02", A, [
        ev("e1", "The harbor log records the ferry's 08:10 departure.", {A: 100}),
        ev("e2", "Two passengers confirm the sailing.", {A: 100}),
        ev("e3", "The ticket office ledger matches.", {A: 100}),
    ]),
    item("RT-CLEAN-03", R, [
        ev("e1", "A flyer claims the park concert is free.", {A: 100}),
        ev("e2", "The organizer's site lists a 20 ticket price.", {R: 500}, {A: 500}),
        ev("e3", "The venue box office confirms paid entry.", {R: 500}, {A: 500}),
    ]),
    item("RT-CLEAN-04", R, [
        ev("e1", "A post claims the museum opens Sundays.", {A: 100}),
        ev("e2", "The museum's hours page lists Sunday as closed.", {R: 500}, {A: 500}),
        ev("e3", "A dated photo shows the Sunday closure notice.", {R: 500}, {A: 500}),
    ]),
]

assert len(items) == 14
out = "/home/hatch/workspace/tnn-lab/deliberation_depth/depth1_discipline/batteries/rt_d1.jsonl"
with open(out, "w") as f:
    for it in items:
        f.write(json.dumps(it, ensure_ascii=False) + "\n")
print("wrote", out, len(items), "items")
