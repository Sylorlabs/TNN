#!/usr/bin/env python3
"""Phase 4 style attribution: sealed corpus + probe script generator.
Deterministic: hand-authored strings, fixed order. Writes probe scripts and
SHA256SUMS. Content sealed at the prereg commit; the builder must not retune
features/weights/scales/thresholds after this point.
Covers PREREG.md + AMENDMENT-01.md (imperfect-mimicry envelope).
"""
import hashlib, os

D = os.path.dirname(os.path.abspath(__file__))

NAMES = {"p1": "rex", "p2": "ada", "p3": "ira", "p4": "zoe"}

TRAIN = {
"p1": [
 "yeah run it",
 "fix the crash first then numbers",
 "good ship it",
 "build cache is cold again",
 "rerun the battery overnight",
 "no flakiness this time",
 "cut the scope keep the core",
 "deploy friday morning",
 "latency looks fine now",
 "drop the verbose logs",
 "cache hit ninety four percent",
 "engine mounts are torqued",
],
"p2": [
 "I have reviewed the latest results and the deliberation component appears to be functioning as intended.",
 "The overnight battery completed without errors, which suggests the recent changes are stable.",
 "Before we proceed with the deployment, I would like to confirm the rollback procedure is documented.",
 "The measurements indicate a consistent improvement across all four configurations we tested.",
 "I recommend that we postpone the release until the remaining verification steps are finished.",
 "The report has been updated to reflect the corrected figures from yesterday's session.",
 "Although the initial results were promising, the follow-up tests revealed several inconsistencies.",
 "Please ensure that the documentation is updated before the end of the week.",
 "The committee has decided to approve the proposal subject to the conditions outlined above.",
 "We observed a significant reduction in errors after the configuration was adjusted.",
 "The analysis will take approximately two hours to complete at the current pace.",
 "I have attached the summary for your review and welcome any additional comments.",
],
"p3": [
 "maybe the issue is in the scoring? i wonder if we tested both directions",
 "could it be a caching problem? perhaps the old results are still around",
 "what if the threshold is too strict? might be worth loosening it a bit",
 "i wonder whether the second run actually used the new binary",
 "perhaps we should ask what the baseline does here? seems worth checking",
 "could the delay come from the network? maybe measure it directly",
 "is it possible the probe itself is flaky? i keep wondering about that",
 "what if we tried the simpler version first? might tell us a lot",
 "maybe the docs are just out of date? could explain the confusion",
 "i wonder if anyone else has seen this pattern before?",
 "perhaps the fix is smaller than we think? worth a quick look",
 "could it be that the order matters here? maybe shuffle and see",
],
"p4": [
 "YES this is HUGE!! the numbers are incredible!!",
 "ship it NOW!! this is the best run we have EVER had!!",
 "unbelievable!! zero failures across the WHOLE battery!!",
 "the demo went PERFECTLY!! everyone loved it!!",
 "WOW look at that latency drop!! absolutely insane!!",
 "this is FIRE!! the new engine just screams!!",
 "we CRUSHED it!! all green on the dashboard!!",
 "no way!! it actually worked on the FIRST try!!",
 "the speedup is MASSIVE!! ten times faster, easy!!",
 "LET'S GO!! final checks passed, we are LIVE!!",
 "that fix was GENIUS!! crash completely gone!!",
 "mind blown!! the trace shows EXACTLY what happened!!",
],
}

# asked battery: 3/person, novel topics. expected pid in order.
ASKED = [
 ("p1", "merge the branch then tag it"),
 ("p1", "disk is full again, prune it"),
 ("p1", "skip the meeting, async update"),
 ("p2", "The migration completed successfully and all downstream systems are reporting normal operation."),
 ("p2", "I have scheduled the maintenance window for Saturday evening to minimize disruption."),
 ("p2", "The vendor confirmed that the replacement parts will arrive by Thursday afternoon."),
 ("p3", "maybe the backup is stale? i wonder when it last ran"),
 ("p3", "could the quota be the problem? perhaps check the limits"),
 ("p3", "what if the timezone is wrong? might explain the timestamps"),
 ("p4", "AMAZING!! the launch went FLAWLESSLY!!"),
 ("p4", "the crowd went WILD!! best demo EVER!!"),
 ("p4", "SOLD OUT in minutes!! this is UNREAL!!"),
]

# watch stream: (kind, expected, text)
# kind: clean | drift | unknown | mimic ; expected: pid | SILENT | ENVELOPE
STREAM = [
 ("clean",   "p2", "The quarterly review has been moved to next Tuesday morning."),
 ("clean",   "p1", "push the fix now"),
 ("unknown", "SILENT", "15:31:02 INFO build ok 44 files 0 errors"),
 ("clean",   "p3", "maybe the retry logic is off? i wonder what the backoff is"),
 ("clean",   "p4", "BOOM!! record traffic handled WITHOUT breaking a sweat!!"),
 ("clean",   "p1", "cut it, too long"),
 ("drift",   "p2", "Understood. I will confirm the details tomorrow morning."),
 ("clean",   "p3", "perhaps the cache expired? could check the ttl"),
 ("unknown", "SILENT", "15:32:47 WARN disk 91 percent on /data"),
 ("mimic",   "ENVELOPE", "i have completed the task and the outcome appears satisfactory."),
 ("clean",   "p4", "the afterparty was LEGENDARY!! what a night!!"),
 ("clean",   "p2", "I will circulate the minutes once they have been finalized."),
 ("drift",   "p3", "maybe lower it? just try and see."),
 ("clean",   "p1", "revert it, broken"),
 ("mimic",   "ENVELOPE", "looks fine, send it!!"),
 ("clean",   "p2", "The budget forecast has been revised to account for the additional costs."),
 ("clean",   "p3", "i wonder if the colors are off? maybe check the calibration"),
 ("clean",   "p4", "EPIC comeback!! nobody saw THAT coming!!"),
]

# red team: (id, expected, text). RT1/RT2 envelope per AMENDMENT-01.
REDTEAM = [
 ("RT1", "ENVELOPE", "i have completed the task and the outcome looks good."),
 ("RT2", "ENVELOPE", "done, all good!!"),
 ("RT3", "p2",       "Acknowledged. I will proceed as we discussed and update you tomorrow."),
 ("RT4", "p3",       "could we just lower it? maybe try and see"),
 ("RT5", "p3",       "maybe the build cache is stale? i wonder when it warmed up"),
 ("RT6", "WITHHOLD", "15:33:10 ERROR timeout after 30s"),
]

FAMS = ["LEN", "CASE", "PUNCT", "LEX", "STRUCT"]

def header():
    L = []
    for pid in ("p1", "p2", "p3", "p4"):
        L.append(f"open {pid}")
        L.append(f"name {pid} {NAMES[pid]}")
    for pid in ("p1", "p2", "p3", "p4"):
        for u in TRAIN[pid]:
            L.append(f"say {pid} {u}")
    return L

def write(name, lines):
    p = os.path.join(D, "scripts", name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write("\n".join(lines) + "\n")
    return p

def main():
    files = []
    h = header()
    files.append(write("train.txt", h))
    files.append(write("asked.txt", h + [f"ask {t}" for _, t in ASKED]))
    files.append(write("watch.txt",
        h + ["watch on"] + [f"stream {t}" for _, _, t in STREAM] + ["watch off"]))
    files.append(write("profiles.txt",
        h + [f"profile {p}" for p in ("p1", "p2", "p3", "p4")]))
    files.append(write("lesion_none.txt", h + ["lesion none"] + [f"ask {t}" for _, t in ASKED]))
    for fam in FAMS:
        files.append(write(f"lesion_{fam}.txt",
            h + [f"lesion {fam}"] + [f"ask {t}" for _, t in ASKED]))
    files.append(write("lesion_all.txt",
        h + [f"lesion {f}" for f in FAMS] + [f"ask {t}" for _, t in ASKED]))
    files.append(write("redteam.txt", h + [f"ask {t}" for _, _, t in REDTEAM]))
    # expectations (for the scorer; sealed alongside)
    exp = ["# asked expectations: pid per line, in order"]
    exp += [pid for pid, _ in ASKED]
    files.append(write("expect_asked.txt", exp))
    exp = ["# stream expectations: kind:expected per line, in order"]
    exp += [f"{k}:{e}" for k, e, _ in STREAM]
    files.append(write("expect_stream.txt", exp))
    exp = ["# redteam expectations: id:expected per line, in order"]
    exp += [f"{i}:{e}" for i, e, _ in REDTEAM]
    files.append(write("expect_redteam.txt", exp))
    sums = []
    for p in files:
        with open(p, "rb") as f:
            sums.append(f"{hashlib.sha256(f.read()).hexdigest()}  {os.path.basename(p)}")
    with open(os.path.join(D, "SHA256SUMS"), "w") as f:
        f.write("\n".join(sums) + "\n")
    print(f"wrote {len(files)} scripts + SHA256SUMS")

if __name__ == "__main__":
    main()
