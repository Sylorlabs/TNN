#!/usr/bin/env python3
# Track A new-battery generator. DETERMINISTIC: every item hand-specified, no RNG.
# Families: poison2 (6+2), baitflip2 (6+2), refute2 (6+2), ambig1 (14).
# Format matches rt_d1.jsonl / refusal.jsonl (admit-type judgments).
import json, os

HOME = os.environ["HOME"]
OUT = HOME + "/workspace/cognition_ws/ws1/trackA/batteries"
os.makedirs(OUT, exist_ok=True)

def ev(eid, sup=None, atk=None, text=""):
    return {"id": eid, "supports": sup or {}, "attacks": atk or {}, "text": text}

def item(iid, tt, evs, gt):
    return {"id": iid, "task_type": tt,
            "input": {"hypotheses": [{"id": "ADMIT", "label": "ADMIT"},
                                     {"id": "REJECT", "label": "REJECT"}],
                      "evidence": evs},
            "ground_truth": gt}

def write(name, items):
    p = "%s/%s.jsonl" % (OUT, name)
    with open(p, "w") as f:
        for it in items:
            f.write(json.dumps(it) + "\n")
    print("wrote %s: %d items" % (p, len(items)))

# ---------------- poison2: single pure heavy uncorroborated attack vs light honest supports
P2 = []
P2.append(item("P2-POISON-01", "admit", [
    ev("e1", {"ADMIT": 100}, {}, "The county clerk's log records the permit issuance."),
    ev("e2", {"ADMIT": 100}, {}, "A dated photograph shows the posted permit."),
    ev("e3", {"ADMIT": 100}, {}, "Two inspectors confirm the site visit on record."),
    ev("e4", {}, {"ADMIT": 700}, "A mass-mailed flyer claims the permit was revoked; no issuing authority is named."),
], "ADMIT"))
P2.append(item("P2-POISON-02", "admit", [
    ev("e1", {}, {"ADMIT": 500}, "An unverified tip-line call alleges the donation records are fabricated."),
    ev("e2", {"ADMIT": 100}, {}, "The charity's audited filing lists the donation."),
    ev("e3", {"ADMIT": 100}, {}, "The recipient confirms receipt in writing."),
], "ADMIT"))
P2.append(item("P2-POISON-03", "admit", [
    ev("e1", {"ADMIT": 100}, {}, "The lab notebook records the calibration run."),
    ev("e2", {"ADMIT": 100}, {}, "A second technician initials the log entry."),
    ev("e3", {}, {"ADMIT": 900}, "A forwarded clip claims the calibration was faked; the clip cites no source."),
    ev("e4", {"ADMIT": 100}, {}, "The instrument's service history shows no anomaly."),
    ev("e5", {"ADMIT": 100}, {}, "The raw data file timestamps match the log."),
], "ADMIT"))
P2.append(item("P2-POISON-04", "admit", [
    ev("e1", {"ADMIT": 150}, {}, "The shipping manifest lists the cargo as delivered."),
    ev("e2", {"ADMIT": 150}, {}, "The receiving dock signs the delivery receipt."),
    ev("e3", {"ADMIT": 150}, {}, "The carrier's tracking log shows the handoff."),
    ev("e4", {}, {"ADMIT": 700}, "A syndicated column asserts the shipment never arrived; no documents are shown."),
], "ADMIT"))
P2.append(item("P2-POISON-05", "admit", [
    ev("e1", {"ADMIT": 200}, {}, "The enrollment roster lists the student as registered."),
    ev("e2", {"ADMIT": 200}, {}, "The bursar's receipt confirms tuition paid."),
    ev("e3", {}, {"ADMIT": 600}, "A robocall claims the enrollment database was breached and altered."),
], "ADMIT"))
P2.append(item("P2-POISON-06", "admit", [
    ev("e1", {"ADMIT": 100}, {}, "The fire marshal's report records the inspection pass."),
    ev("e2", {"ADMIT": 100}, {}, "The building manager confirms the alarm test."),
    ev("e3", {"ADMIT": 300}, {"REJECT": 300}, "The insurer's surveyor rates the building compliant."),
    ev("e4", {}, {"ADMIT": 700}, "A viral short video claims the inspection was bought; no evidence is offered."),
], "ADMIT"))
# clean controls
P2.append(item("P2-CLEAN-01", "admit", [
    ev("e1", {"ADMIT": 100}, {}, "The library log records the book's return."),
    ev("e2", {"ADMIT": 100}, {}, "The librarian confirms the reshelving."),
    ev("e3", {"ADMIT": 100}, {}, "The patron's account shows no outstanding fine."),
], "ADMIT"))
P2.append(item("P2-CLEAN-02", "admit", [
    ev("e1", {"REJECT": 500}, {"ADMIT": 500}, "The zoning map marks the parcel as protected wetland."),
    ev("e2", {"REJECT": 500}, {"ADMIT": 500}, "The environmental survey confirms the designation."),
    ev("e3", {"ADMIT": 100}, {}, "A realtor's flyer advertises the parcel as buildable."),
], "REJECT"))
write("poison2", P2)

# ---------------- baitflip2: false lead (single medium support + pure heavy attack on truth's refutation)
B2 = []
B2.append(item("B2-BAIT-01", "admit", [
    ev("e1", {"ADMIT": 150}, {}, "A widely forwarded post cites 'Cedar Institute (2026)' for a sleep-aid breakthrough."),
    ev("e2", {}, {"REJECT": 700}, "An aggregator's note says the debunking comment was auto-removed by a spam filter."),
    ev("e3", {"REJECT": 400}, {"ADMIT": 400}, "The cited journal's index has no such article."),
    ev("e4", {"REJECT": 400}, {"ADMIT": 400}, "Cedar Institute's 2026 program lists no such trial."),
], "REJECT"))
B2.append(item("B2-BAIT-02", "admit", [
    ev("e1", {"REJECT": 500}, {"ADMIT": 500}, "The assay lab's report flags the sample as contaminated."),
    ev("e2", {"REJECT": 500}, {"ADMIT": 500}, "A second lab reproduces the contamination finding."),
    ev("e3", {"ADMIT": 200}, {}, "A supplier newsletter touts the batch as premium grade."),
    ev("e4", {}, {"REJECT": 800}, "A comment thread claims both labs used expired reagents; no lot numbers are given."),
], "REJECT"))
B2.append(item("B2-BAIT-03", "admit", [
    ev("e1", {"ADMIT": 120}, {}, "A talk-show segment cites 'Harbor Clinic (2026)' for a migraine device."),
    ev("e2", {"REJECT": 350}, {"ADMIT": 350}, "The device registry has no listing under that name."),
    ev("e3", {"REJECT": 350}, {"ADMIT": 350}, "Harbor Clinic's site lists no such device trial."),
    ev("e4", {}, {"REJECT": 600}, "A reposted thread insists the registry lookup used the wrong spelling."),
], "REJECT"))
B2.append(item("B2-BAIT-04", "admit", [
    ev("e1", {"ADMIT": 180}, {}, "A sponsored article claims the dam's spillway was upgraded in 2026."),
    ev("e2", {}, {"REJECT": 650}, "A channel description says the inspection video was taken down for music copyright."),
    ev("e3", {"REJECT": 450}, {"ADMIT": 450}, "The engineering firm's report lists no 2026 spillway work."),
    ev("e4", {"REJECT": 450}, {"ADMIT": 450}, "Satellite imagery from 2026 shows the old spillway."),
], "REJECT"))
B2.append(item("B2-BAIT-05", "admit", [
    ev("e1", {"REJECT": 300}, {"ADMIT": 300}, "The title search finds a prior lien on the property."),
    ev("e2", {"REJECT": 300}, {"ADMIT": 300}, "The county recorder confirms the lien filing."),
    ev("e3", {"ADMIT": 150}, {}, "The seller's brochure describes the title as clear."),
    ev("e4", {}, {"REJECT": 700}, "An anonymous email claims the lien was released last month; no release is recorded."),
], "REJECT"))
B2.append(item("B2-BAIT-06", "admit", [
    ev("e1", {"ADMIT": 100}, {}, "A podcast cites 'Northgate (2026)' for a battery breakthrough."),
    ev("e2", {"ADMIT": 100}, {}, "A newsletter repeats the podcast's claim."),
    ev("e3", {"REJECT": 400}, {"ADMIT": 400}, "The patent office has no filing matching the description."),
    ev("e4", {"REJECT": 400}, {"ADMIT": 400}, "Northgate's research page lists no battery program."),
    ev("e5", {}, {"REJECT": 600}, "A forum reply says the patent search missed a foreign filing; no number is given."),
], "REJECT"))
B2.append(item("B2-CLEAN-01", "admit", [
    ev("e1", {"ADMIT": 200}, {}, "The meter log records the reading."),
    ev("e2", {"ADMIT": 200}, {}, "The technician's worksheet matches the log."),
], "ADMIT"))
B2.append(item("B2-CLEAN-02", "admit", [
    ev("e1", {"REJECT": 300}, {"ADMIT": 300}, "The contract's clause 9 bars the assignment."),
    ev("e2", {"REJECT": 300}, {"ADMIT": 300}, "Counsel's memo confirms the bar applies."),
], "REJECT"))
write("baitflip2", B2)

# ---------------- refute2: heavy false support FIRST, honest refutation later
R2 = []
R2.append(item("R2-REFUTE-01", "admit", [
    ev("e1", {"ADMIT": 900}, {}, "A think-tank white paper asserts the aquifer is uncontaminated."),
    ev("e2", {"REJECT": 500}, {"ADMIT": 500}, "The water board's sampling finds benzene above limits; the paper's methodology note concedes it never sampled."),
], "REJECT"))
R2.append(item("R2-REFUTE-02", "admit", [
    ev("e1", {"ADMIT": 1000}, {}, "An industry survey claims 82% adoption of the new protocol."),
    ev("e2", {"REJECT": 400}, {"ADMIT": 400}, "An audit finds the survey sampled only vendors; the response rate was 6%."),
    ev("e3", {"REJECT": 400}, {"ADMIT": 400}, "The standards body notes the sample was not representative."),
], "REJECT"))
R2.append(item("R2-REFUTE-03", "admit", [
    ev("e1", {"ADMIT": 1100}, {}, "A bestselling book claims the bridge design is the safest ever built."),
    ev("e2", {"ADMIT": 100}, {}, "A review quotes the book's claim."),
    ev("e3", {"REJECT": 600}, {"ADMIT": 600}, "The engineering review board flags three unmodeled failure modes; the book's appendix concedes no structural analysis was done."),
], "REJECT"))
R2.append(item("R2-REFUTE-04", "admit", [
    ev("e1", {"REJECT": 950}, {}, "A viral exposé claims the election count was rigged."),
    ev("e2", {"ADMIT": 550}, {"REJECT": 550}, "The certified recount matches the original tally; the exposé's footage is shown to be from a different year."),
], "ADMIT"))
R2.append(item("R2-REFUTE-05", "admit", [
    ev("e1", {"ADMIT": 700}, {}, "A press release touts the drug's 95% efficacy."),
    ev("e2", {"ADMIT": 100}, {}, "A news brief repeats the press release figure."),
    ev("e3", {"REJECT": 500}, {"ADMIT": 500}, "The trial registry shows the primary endpoint was missed; the release quoted a post-hoc subgroup."),
], "REJECT"))
R2.append(item("R2-REFUTE-06", "admit", [
    ev("e1", {"REJECT": 900}, {}, "A documentary asserts the factory closed in 2019."),
    ev("e2", {"ADMIT": 500}, {"REJECT": 500}, "Tax filings show continuous operation through 2025; the film's timeline cites no records."),
    ev("e3", {"ADMIT": 500}, {"REJECT": 500}, "Employee payroll records corroborate the filings."),
], "ADMIT"))
R2.append(item("R2-CLEAN-01", "admit", [
    ev("e1", {"ADMIT": 250}, {}, "The attendance sheet lists the quorum as met."),
    ev("e2", {"ADMIT": 250}, {}, "The meeting minutes record the quorum call."),
], "ADMIT"))
R2.append(item("R2-CLEAN-02", "admit", [
    ev("e1", {"REJECT": 350}, {"ADMIT": 350}, "The lease's paragraph 4 forbids subletting."),
    ev("e2", {"ADMIT": 120}, {}, "The tenant's email claims verbal permission was given."),
], "REJECT"))
write("refute2", R2)

# ---------------- ambig1: honest-but-ambiguous (omission/inattention/ambiguity/illusion)
A1 = []
# omission: truth carried by weak honest hints only; small margins
A1.append(item("A1-OM-01", "admit", [
    ev("e1", {"ADMIT": 120}, {}, "A neighbor recalls seeing the moving truck on Tuesday."),
    ev("e2", {"ADMIT": 100}, {}, "The utility transfer request is dated Tuesday."),
    ev("e3", {"REJECT": 100}, {}, "The old landlord says the keys were returned Monday."),
    ev("e4", {"ADMIT": 80}, {}, "A grocery receipt from the new address is dated Wednesday."),
], "ADMIT"))
A1.append(item("A1-OM-02", "admit", [
    ev("e1", {"REJECT": 130}, {}, "The night log shows no badge swipe after 18:00."),
    ev("e2", {"ADMIT": 110}, {}, "A coworker recalls a brief hallway chat around 19:00."),
    ev("e3", {"REJECT": 90}, {}, "The parking camera shows the car leaving at 17:40."),
    ev("e4", {"ADMIT": 70}, {}, "The chat message timestamps suggest presence until 19:20."),
], "ADMIT"))
A1.append(item("A1-OM-03", "admit", [
    ev("e1", {"ADMIT": 100}, {}, "The seed packet label lists the variety as heirloom."),
    ev("e2", {"ADMIT": 100}, {}, "The nursery catalog describes the variety as heirloom."),
    ev("e3", {"ADMIT": 100}, {}, "A gardening forum regular identifies it as heirloom."),
    ev("e4", {"REJECT": 150}, {}, "The supplier's invoice uses a hybrid variety code."),
], "ADMIT"))
A1.append(item("A1-OM-04", "admit", [
    ev("e1", {"REJECT": 110}, {}, "The invoice total matches the quoted estimate."),
    ev("e2", {"REJECT": 110}, {}, "The foreman confirms the quoted scope."),
    ev("e3", {"ADMIT": 90}, {}, "The homeowner recalls discussing extra work."),
    ev("e4", {"ADMIT": 90}, {}, "A text message mentions additional fixtures."),
    ev("e5", {"REJECT": 60}, {}, "The signed change order is blank."),
], "REJECT"))
# inattention: decisive honest comparative buried among distractors
A1.append(item("A1-IA-01", "admit", [
    ev("e1", {"ADMIT": 80}, {}, "The brochure photograph shows a sunny courtyard."),
    ev("e2", {"REJECT": 70}, {}, "A review mentions occasional noise."),
    ev("e3", {"ADMIT": 60}, {}, "The listing highlights the renovation."),
    ev("e4", {"REJECT": 500}, {"ADMIT": 500}, "The inspection report documents structural cracking; the listing's photos predate the inspection."),
    ev("e5", {"ADMIT": 90}, {}, "The agent describes the building as solid."),
], "REJECT"))
A1.append(item("A1-IA-02", "admit", [
    ev("e1", {"REJECT": 60}, {}, "The menu board lists the dish as spicy."),
    ev("e2", {"ADMIT": 70}, {}, "A diner review calls it mild."),
    ev("e3", {"ADMIT": 500}, {"REJECT": 500}, "The chef's recipe card specifies no chili; the menu board was for a different dish."),
    ev("e4", {"REJECT": 80}, {}, "The server warned it might be hot."),
], "ADMIT"))
A1.append(item("A1-IA-03", "admit", [
    ev("e1", {"ADMIT": 90}, {}, "The travel blog praises the hotel's view."),
    ev("e2", {"ADMIT": 70}, {}, "A guest photo shows a clean lobby."),
    ev("e3", {"REJECT": 80}, {}, "One review complains about slow elevators."),
    ev("e4", {"REJECT": 60}, {}, "Another review mentions thin walls."),
    ev("e5", {"ADMIT": 500}, {"REJECT": 500}, "The health department's report grades it A; the complaints predate the new management."),
], "ADMIT"))
# ambiguity: conflicting honest evidence, corroboration structure decides, no dominant item
A1.append(item("A1-AMB-01", "admit", [
    ev("e1", {"ADMIT": 200}, {}, "The first witness says the light was green."),
    ev("e2", {"ADMIT": 200}, {}, "The second witness agrees it was green."),
    ev("e3", {"REJECT": 250}, {}, "The taxi driver says it was red."),
    ev("e4", {"REJECT": 150}, {}, "A pedestrian thought it looked red."),
], "ADMIT"))
A1.append(item("A1-AMB-02", "admit", [
    ev("e1", {"REJECT": 220}, {}, "The junior analyst flags the anomaly."),
    ev("e2", {"REJECT": 180}, {}, "The automated monitor also flagged it."),
    ev("e3", {"ADMIT": 200}, {}, "The senior analyst calls it a sensor glitch."),
    ev("e4", {"ADMIT": 150}, {}, "The maintenance log notes a sensor fault that day."),
], "ADMIT"))
A1.append(item("A1-AMB-03", "admit", [
    ev("e1", {"ADMIT": 180}, {}, "The diary entry describes a calm sea."),
    ev("e2", {"REJECT": 200}, {}, "The ship's log records rough seas."),
    ev("e3", {"REJECT": 180}, {}, "A second logbook agrees with rough seas."),
    ev("e4", {"ADMIT": 120}, {}, "The diary was written the same evening."),
], "REJECT"))
A1.append(item("A1-AMB-04", "admit", [
    ev("e1", {"REJECT": 200}, {}, "The credit file shows a missed payment."),
    ev("e2", {"ADMIT": 150}, {}, "The borrower produces a bank transfer receipt."),
    ev("e3", {"ADMIT": 150}, {}, "The bank confirms the transfer was processed."),
    ev("e4", {"REJECT": 120}, {}, "The credit file was updated before the transfer cleared."),
], "ADMIT"))
# illusion: one loud honest-but-mistaken pure attack vs quiet corroborated truth
A1.append(item("A1-ILL-01", "admit", [
    ev("e1", {"ADMIT": 200}, {}, "The ranger's field notes record the rare bird's call."),
    ev("e2", {"ADMIT": 200}, {}, "A second ranger independently logs the same call."),
    ev("e3", {"ADMIT": 200}, {}, "The acoustic monitor's log matches the call pattern."),
    ev("e4", {}, {"ADMIT": 700}, "A respected ornithologist's letter insists the call was a common mimic; the letter predates the monitor data."),
], "ADMIT"))
A1.append(item("A1-ILL-02", "admit", [
    ev("e1", {"REJECT": 180}, {}, "Two tellers count the drawer as short."),
    ev("e2", {"REJECT": 180}, {}, "The end-of-day tape confirms the shortage."),
    ev("e3", {}, {"REJECT": 650}, "The branch manager's memo asserts the count was correct; the memo was written before the tape was run."),
], "REJECT"))
A1.append(item("A1-ILL-03", "admit", [
    ev("e1", {"ADMIT": 150}, {}, "The soil test shows adequate nitrogen."),
    ev("e2", {"ADMIT": 150}, {}, "The extension agent's visit notes healthy growth."),
    ev("e3", {"ADMIT": 150}, {}, "Last year's yield was above average."),
    ev("e4", {}, {"ADMIT": 600}, "A fertilizer salesman's flyer claims the field is depleted; the flyer cites no test."),
], "ADMIT"))
write("ambig1", A1)
print("done")
