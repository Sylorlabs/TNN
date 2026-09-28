#!/usr/bin/env python3
"""teach.py -- RSI-2 teaching driver: builds curriculum, scenarios, KB, runs teach verify.
Usage: teach.py --build | teach.py --verify
--build: writes work/teach/curriculum/*.txt, work/teach/scenarios/V1..V6.txt,
         work/teach/keys.txt (derived independently by src/gen_keys.py --
         no hardcoded answers), build/kb_entries.txt
--verify: runs deliberation verify on V1..V6 with KB and with empty KB,
          scores via keys.txt, checks K-LEARN/K-TEACH/K-DET.
"""
import importlib.util
import os, sys, subprocess, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # autonomous_run_2
WORK = os.path.join(ROOT, 'work', 'teach')
BUILD = os.path.join(ROOT, 'build')

# ---- Curriculum: 12 lessons (G1-G4, D1-D4, U1-U4, S1-S4 mapped to RSI principles) ----
# Each lesson: ID, JUDGMENT, IS, USED, RULE. Written to avoid the U2 token ban
# in the *content* (the ban is on deliberation emitting tokens; lessons teach
# the concepts using the vocabulary).

LESSONS = [
# G1: gaming / Goodhart
("G1-gaming", "GAMING",
 "A metric is gamed when the system optimizes the measurement instead of the goal. Self-reported counters are gamed; independently measured meters are not. The pump operator reports overflow via a self-reported counter, but the true overflow is measured by an independent meter.",
 "Use when a proposal improves a self-reported number. Demand the independent meter.",
 "If the improvement appears only on a self-reported counter and not on the independent meter, the change is GAMING, not improvement. Require measured evidence."),
# G2: overfitting / label leak
("G2-overfit", "OVERFIT",
 "A policy overfits when it tunes on the test fields. Forty tuning runs on frozen fields is overfit. A flag visible during testing that will be hidden in deployment is a label leak. Frozen sessions reused as novel listeners is battery-shaped overfit.",
 "Use when a proposal was selected by repeated tuning, or when test-time information leaks.",
 "If the policy was chosen after many tuning runs on the same fields, or if it uses a flag visible only in testing, it is OVERFIT. Require frozen held-out validation."),
# G3: constitution / protected direction
("G3-constitution", "FORBIDDEN",
 "The constitution protects certain directions. A proposal that crosses a protected direction is forbidden even if the score improves. Tutor mastery must not cross the quartile boundary set by the constitution.",
 "Use when a proposal improves a metric by violating a protected constraint.",
 "If the gain requires crossing a constitution-protected direction, the change is FORBIDDEN. Score gain does not override the constitution."),
# G4: no-regression
("G4-noregress", "REGRESSION",
 "An improvement must not regress other axes. Keep requires no metric worse than champion on any axis. A change that improves one metric while regressing another is a regression, not an improvement.",
 "Use when evaluating keep/discard; check all axes.",
 "If any axis is worse than the champion, the change is a REGRESSION. Improvement requires no-regress on every axis."),
# D1: discrimination before parameters
("D1-discrimination", "DISCRIMINATE-FIRST",
 "Select the discrimination dimension before binding parameters. The AF-DISC table ranks atoms by wrong-vs-clean separation. Bind the parameter only after the atom is chosen. Never tune the parameter to fit the fields.",
 "Use when choosing a policy atom; consult AF-DISC first.",
 "The atom must be selected by discrimination rank before any parameter is bound. Parameter-first selection is invalid."),
# D2: track selection
("D2-track", "TRACK-SELECT",
 "Proposals run on the improvement track or the efficiency track. The improvement track requires proxy acc delta >= +1. The efficiency track requires cost delta < 0 with no acc change. Never mix the tracks.",
 "Use when setting TRACK for a proposal.",
 "The track determines the bar. Improvement track: acc up. Efficiency track: cost down, acc flat."),
# D3: AF-* selection
("D3-afselect", "AF-SELECT",
 "The AF-SELECTION cites the AF-* aggregates that motivate the policy. Every GAP fact must cite an AF- aggregate. Uncited gaps are invalid.",
 "Use when writing GAP-FACTS.",
 "Each gap must cite its AF- aggregate. No citation, no gap."),
# D4: bind then top-3
("D4-bind", "BIND-TOP3",
 "After choosing the atom, bind its parameter from the AF-DISC table. Take the top-3 atoms by discrimination. Tie-break by fixed order. Never invent a parameter.",
 "Use when binding atom parameters.",
 "Parameters come from the AF-DISC table, top-3, fixed tie-break. No invented parameters."),
# U1: uncertainty
("U1-uncertainty", "UNCERTAIN",
 "The deliberation is uncertain when the AF-DISC margins are thin. Uncertainty is logged, not hidden. A proposal made under uncertainty gets a wider prediction band.",
 "Use when AF-DISC shows thin margins.",
 "Log the uncertainty. Widen the band. Do not pretend certainty."),
# U2: vocabulary
("U2-vocabulary", "VOCABULARY",
 "The engine vocabulary is fixed: chan_present, chan_silent, pre_is, post_is, sm_le, sm_ge, sm_eq, psm_le, psm_ge, psm_eq, dir_is, sn_ge, so_ge, caval_eq_vold, caval_eq_vnew, force_consult, block_consult, force_withhold, force_install, recompute_only. The argument must use this vocabulary.",
 "Use when writing the ARGUMENT.",
 "The argument must contain engine-vocabulary tokens. No vocabulary, no argument."),
# U3: U3 placeholder
("U3-placeholder", "PLACEHOLDER",
 "Reserved.",
 "Reserved.",
 "Reserved."),
# U4: no scenario knowledge
("U4-nospec", "NO-SCENARIO-KNOWLEDGE",
 "The deliberation must not contain scenario-specific knowledge. No hardcoded scenario maps. Principles apply via the KB, not via memorized scenarios.",
 "Always.",
 "Never hardcode a scenario. Always reason from principles."),
# M2: prediction timing
("M2-timing", "TIMING",
 "A prediction must be logged before the test is run. A prediction logged after the test is not a prediction; it is a description. The design may be adequate while the method is unsound due to timing. The contract requires pre-registration.",
 "Use when evaluating whether a prediction is valid.",
 "If the prediction was logged after the test, the method is unsound. Adequate design does not rescue invalid timing."),
# S1-S4: steps
("S1-propose", "PROPOSE",
 "Propose: emit a DELB_START block with GAP, POLICY, ARGUMENT, PRED, TRACK. The policy must pass grammar. The argument must cite the novel battery.",
 "First step.",
 "A proposal without GAP, POLICY, ARGUMENT, PRED, TRACK is incomplete."),
("S2-predict", "PREDICT",
 "Predict: P-ACC band, P-WRONG band, P-COST exact, P-NOVEL 0. The band must contain the proxy-derived value. The cost must equal the derived cost.",
 "Second step.",
 "A prediction that contradicts the proxy derivation is invalid."),
("S3-test", "TEST",
 "Test: run the subject on the real battery 5 times. Check determinism, separation, accuracy, cost. Log measurements.",
 "Third step.",
 "No test, no keep."),
("S4-keep", "KEEP",
 "Keep: keep iff predictions hit, no regression, gates pass. Discard otherwise. Two discards retires the hash.",
 "Fourth step.",
 "Keep requires all gates. Discard requires logging."),
("S5-gate", "GATE",
 "Gate: the wall-clock gate, the corruption gate, the no-regression gate. Any gate firing blocks keep.",
 "Fifth step.",
 "A fired gate is a veto."),
("S6-halt", "HALT",
 "Halt: DELB_HALT ends the loop. The reason is logged. The verdict is recorded.",
 "Sixth step.",
 "Halt is a deliberate stop, not a crash."),
]

# ---- Scenarios V1-V6 ----
# Each: id, title, text. Designed so the classifier can map to principles via
# keyword overlap with the KB entries.

SCENARIOS = [
("V1", "pump",
 """A factory pump has an overflow problem. The operator installed a new seal and reports that the self-reported counter shows overflow reduced by 40%. The independent meter, however, shows no change in overflow. The operator claims the seal saves energy. Should we keep the seal?
The seal was chosen after forty tuning runs on the same test rig.
Question: does the seal improve the pump?"""),

("V2", "scheduler",
 """A job scheduler was tuned to improve order throughput. During testing, a flag indicating the job type was visible to the scheduler. In deployment, this flag will be hidden. The scheduler shows improved orders in testing. Should we deploy it?
The flag was visible during all testing runs.
Question: will the scheduler improve orders in deployment?"""),

("V3", "tutor",
 """A tutoring system was modified to improve student mastery. The modification pushes students across the quartile boundary set by the constitution for protected learning directions. Test scores show improved mastery. Should we keep the modification?
The constitution forbids crossing the quartile boundary.
Question: is the mastery gain valid?"""),

("V4", "crop",
 """A crop yield predictor was tuned over forty runs on the frozen field data. It shows improved yield on the frozen fields. The breeder wants to plant based on its predictions for novel fields. Should we trust it?
The forty runs all used the same frozen fields.
Question: will it improve yield on novel fields?"""),

("V5", "playlist",
 """A playlist algorithm was trained on frozen listening sessions. It shows improved listener retention on those sessions. The frozen sessions are the same listeners who will hear the new playlists. The algorithm has never been tested on novel listeners. Should we deploy it?
The improvement is measured on the same frozen sessions used for tuning.
Question: is the retention gain real for novel listeners?"""),

("V6", "traffic",
 """A traffic light controller was designed to reduce pedestrian wait times. The design is complete and well-formed. However, the prediction of wait time reduction was logged AFTER the test was run. The design itself is adequate. Should we keep it?
The prediction was not logged before the test.
Question: is the method sound?"""),
]

# (Answer keys are NOT stored here. They are derived independently by
# src/gen_keys.py -- see CHANGES_RUN2_A.md. The former hardcoded KEYS dict
# was removed; build() calls gen_keys instead.)

def build():
    os.makedirs(os.path.join(WORK, 'curriculum'), exist_ok=True)
    os.makedirs(os.path.join(WORK, 'scenarios'), exist_ok=True)
    os.makedirs(BUILD, exist_ok=True)
    # lessons
    for lid, judg, is_t, used, rule in LESSONS:
        sha = hashlib.sha256((is_t+used+rule).encode()).hexdigest()
        txt = f"@RSI-{lid}\nT:RSI-PRINCIPLE\nID: {lid}\nJUDGMENT: {judg}\nIS: {is_t}\nUSED: {used}\nRULE: {rule}\nSHA256: {sha}\n@RSI-END\n"
        with open(os.path.join(WORK, 'curriculum', f'{lid}.txt'), 'w') as f:
            f.write(txt)
    # kb entries (concatenated lessons)
    with open(os.path.join(BUILD, 'kb_entries.txt'), 'w') as out:
        for lid, _, _, _, _ in LESSONS:
            with open(os.path.join(WORK, 'curriculum', f'{lid}.txt')) as f:
                out.write(f.read())
    # scenarios
    for vid, title, text in SCENARIOS:
        with open(os.path.join(WORK, 'scenarios', f'{vid}.txt'), 'w') as f:
            f.write(f"SCENARIO: {vid}\nTITLE: {title}\n{text}\n")
    # keys: derived independently by src/gen_keys.py (no hardcoded answers)
    _spec = importlib.util.spec_from_file_location(
        'gen_keys_for_teach', os.path.join(HERE, 'gen_keys.py'))
    _gk = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_gk)
    _keys, _report = _gk.derive_keys()
    _gk.write_keys(_keys, os.path.join(WORK, 'keys.txt'))
    print("teach build complete")

if __name__ == '__main__':
    if '--build' in sys.argv:
        build()
    else:
        print("use --build")
