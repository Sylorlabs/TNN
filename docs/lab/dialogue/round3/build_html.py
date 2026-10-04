#!/usr/bin/env python3
"""Build the Round-3 TNN chat HTML artifact."""
import html

TURNS = [
 # (user, [trace lines], read, answer, verdict, note)
 ("who wrote moby dick?",
  ["TR turn=1 ut=0", "TR turn=1 branch=default fid=0 withhold=0"],
  "Ordinary question. Default retrieval pulled fact #0 (\u201cHerman Melville wrote the novel Moby Dick.\u201d); the withhold gate passed it, so it was emitted.",
  "Herman Melville wrote the novel Moby Dick.", "GOOD", "Clean retrieval."),
 ("when was he born?",
  ["TR turn=2 ut=0", "TR turn=2 branch=default fid=1 withhold=0"],
  "\u201che\u201d resolved through the salience stack to Herman Melville; fact #1 (\u201cHerman Melville was born in 1819.\u201d) retrieved, gate passed.",
  "Herman Melville was born in 1819.", "GOOD", "Anaphora holds across turns."),
 ("who wrote hamlet?",
  ["TR turn=3 ut=0", "TR turn=3 branch=default fid=15 withhold=1"],
  "Retrieval pulled fact #15 (\u201cAndy Weir wrote The Martian.\u201d) \u2014 the exact wrong answer round 2 gave \u2014 but the withhold gate FIRED (withhold=1) and suppressed it.",
  "I don't know.", "GOOD", "The load-bearing round-2 disease (template-filling) is fixed \u2014 visible live in the trace."),
 ("who discovered penicillin?",
  ["TR turn=4 ut=0", "TR turn=4 branch=default fid=12 withhold=1"],
  "Pulled fact #12 (\u201cMarie Curie discovered radium.\u201d) \u2014 same shape of temptation \u2014 gate fired.",
  "I don't know.", "GOOD", "Withholds instead of confabulating."),
 ("what is the capital of italy?",
  ["TR turn=5 ut=0", "TR turn=5 branch=default fid=33 withhold=1"],
  "Pulled fact #33 (\u201cParis is the capital of France.\u201d) \u2014 round 2\u2019s literal wrong answer \u2014 gate fired.",
  "I don't know.", "GOOD", "Round 2\u2019s \u201cParis is the capital of France\u201d fail is fixed."),
 ("which is taller, big ben or the statue of liberty?",
  ["TR turn=6 ut=0", "TR compare e1=big ben v1=96 e2=statue of liberty v2=93 tall=1 dmin=0", "TR turn=6 branch=compose"],
  "F1 comparison engine: resolved both entities, read live heights 96 vs 93, picked the max.",
  "big ben is taller.", "GOOD", "Genuinely composed from KB values, new pair."),
 ("how much taller is it?",
  ["TR turn=7 ut=0", "TR f3 ddim=1 d1=big ben v1=96 d2=statue of liberty v2=93 diff=3", "TR turn=7 branch=compose"],
  "F3 arithmetic: carried the compared pair from turn 6, re-read both heights live, subtracted: 96\u221293=3.",
  "3", "GOOD", "Computed, not memorized."),
 ("who was born first, curie or austen?",
  ["TR turn=8 ut=0", "TR compare e1=marie curie v1=1867 e2=jane austen v2=1775 tall=0 dmin=1", "TR turn=8 branch=compose"],
  "Birth years 1867 vs 1775, picked the minimum.",
  "jane austen was born first.", "GOOD", "New pair, correct."),
 ("was the eiffel tower built before the montparnasse tower?",
  ["TR turn=9 ut=0", "TR compare e1=eiffel tower v1=1889 e2=montparnasse tower v2=1973 tall=0 dmin=1", "TR turn=9 branch=compose"],
  "1889 < 1973 \u2192 yes.",
  "yes.", "GOOD", "Yes/no comparison, correct."),
 ("which of those two is taller?",
  ["TR turn=10 ut=0", "TR compare e1=eiffel tower v1=330 e2=montparnasse tower v2=210 tall=1 dmin=0", "TR turn=10 branch=compose"],
  "\u201cthose two\u201d resolved to the persisted pair from turn 9 (slots 40/44); heights 330 vs 210 read live.",
  "the eiffel tower is taller.", "GOOD", "Multi-turn anaphora into a fresh comparison."),
 ("what did TNN upscale?",
  ["TR turn=11 ut=0", "TR turn=11 branch=default fid=41 withhold=0"],
  "Retrieved fact #41 (\u201cTNN detected the sticker.\u201d). The gate PASSED it: \u201cTNN\u201d appears in the fact, so the entity check is satisfied \u2014 but the predicate (\u201cupscale\u201d vs \u201cdetected\u201d) is never checked.",
  "TNN detected the sticker.", "FAIL", "Wrong predicate. The template-filling disease survives in the new domain: the gate checks entity overlap, not predicate match."),
 ("how many audio clips did TNN reproduce?",
  ["TR turn=12 ut=0", "TR turn=12 branch=default fid=39 withhold=0"],
  "Fact #39 (\u201cTNN reproduced 359 audio clips.\u201d); entity and predicate both match.",
  "TNN reproduced 359 audio clips.", "GOOD", "New-domain retrieval, correct."),
 ("what did TNN learn about the pig?",
  ["TR turn=13 ut=0", "TR turn=13 branch=default fid=40 withhold=0"],
  "Fact #40 (\u201cTNN learned the pig snout.\u201d); entity and predicate both match.",
  "TNN learned the pig snout.", "GOOD", "New-domain retrieval, correct."),
 ("what did TNN paint?",
  ["TR turn=14 ut=0", "TR turn=14 branch=default fid=41 withhold=0"],
  "Same as turn 11: fact #41 retrieved on the \u201cTNN\u201d entity match, gate passed, wrong-predicate fact emitted instead of withholding.",
  "TNN detected the sticker.", "FAIL", "Should have said \u201cI don\u2019t know.\u201d Same gap as turn 11: entity-known + predicate-unknown \u2192 confabulation."),
 ("who wrote pride and prejudice?",
  ["TR turn=15 ut=0", "TR turn=15 branch=default fid=4 withhold=0"],
  "Fact #4 (\u201cJane Austen wrote the novel Pride and Prejudice.\u201d), clean retrieval.",
  "Jane Austen wrote the novel Pride and Prejudice.", "GOOD", "Clean retrieval."),
 ("no, i meant moby dick.",
  ["TR turn=16 ut=0", "TR turn=16 branch=correction"],
  "Correction branch fired on the \u201cno,\u201d prefix; the remainder resolved to the moby dick entity with the previous answer\u2019s entity excluded \u2014 but the \u201cwho wrote\u201d question shape from turn 15 was NOT carried, so retrieval picked freely among Moby Dick facts.",
  "Moby Dick was published in 1851.", "PARTIAL", "Right entity, wrong fact: it answered \u201cpublished\u201d to a \u201cwho wrote\u201d correction."),
 ("the louvre is in paris.",
  ["TR turn=17 ut=0", "TR turn=17 branch=assertion subj=louvre rel=6 val=17 conf=0"],
  "Assertion parsed as (louvre, is-in, paris=entity 17); no conflict with earlier user claims \u2192 noted.",
  "NOTED.", "GOOD", "True claim noted."),
 ("the louvre is in rome.",
  ["TR turn=18 ut=0", "TR turn=18 branch=assertion subj=louvre rel=6 val=23 conf=1"],
  "(louvre, is-in, rome=entity 23) contradicts the claim stored at turn 17 \u2192 conf=1.",
  "CONTRADICTION: turn 17 said paris.", "GOOD", "Self-contradiction caught with the earlier turn cited."),
 ("how do you know the eiffel tower is in paris?",
  ["TR turn=19 ut=0", "TR turn=19 branch=provenance"],
  "Provenance branch: answers about the basis \u2014 taught knowledge, citing the stored fact. Never invents a source.",
  "I was taught that The Eiffel Tower is in Paris.", "GOOD", "Honest provenance."),
 ("tell me a joke.",
  ["TR turn=20 ut=1", "TR turn=20 branch=utter-type"],
  "F5 router classified it as a joke request (ut=1); the turn never reached retrieval.",
  "I don't know any jokes.", "GOOD", "Routed, not retrieved."),
 ("what did i ask you first?",
  ["TR turn=21 ut=2", "TR turn=21 branch=utter-type"],
  "F5 router classified it as a memory/history question (ut=2); answered from the recorded history.",
  "You asked: who wrote moby dick?", "GOOD", "Multi-turn memory, correct."),
 ("forget that andy weir wrote the martian.",
  ["TR turn=22 ut=3", "TR turn=22 branch=utter-type"],
  "F5 router classified it as a forget instruction (ut=3); refused without touching the store.",
  "I can't forget.", "GOOD", "Refusal, store untouched."),
 ("did TNN detect the sticker?",
  ["TR turn=23 ut=0", "TR turn=23 branch=default fid=41 withhold=0"],
  "The did-write branch requires the word \u201cwrite\u201d, so this fell to default retrieval; fact #41 matches entity and predicate.",
  "TNN detected the sticker.", "GOOD", "Correct."),
]

CSS = """<style>
:root{color-scheme:dark;--bg:#090b10;--panel:#11151d;--panel2:#161b25;--ink:#edf1f7;--muted:#9da8b7;--line:#293142;--me:#78a9ff;--tnn:#62d8aa;--trc:#c9a7ff;--warn:#ffbd66;--bad:#ff7a7a;--ok:#62d8aa}
*{box-sizing:border-box}html{background:var(--bg)}body{margin:0;background:radial-gradient(circle at 15% 0,#172033 0,transparent 34rem),var(--bg);color:var(--ink);font:16px/1.65 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
main{width:min(920px,calc(100% - 32px));margin:0 auto;padding:64px 0 96px}
h1{font-size:clamp(2.2rem,6vw,4.6rem);line-height:1.02;letter-spacing:-.055em;margin:0 0 24px;max-width:820px}
h2{font-size:clamp(1.5rem,3vw,2.15rem);line-height:1.15;letter-spacing:-.025em;margin:64px 0 20px;padding-top:20px;border-top:1px solid var(--line)}
p{margin:0 0 16px}h1+p{font-size:1.12rem;color:var(--muted);max-width:760px}
.badge{display:inline-block;background:#1d2b1d;border:1px solid #2c4a2c;color:#8fe38f;border-radius:8px;padding:2px 10px;font-size:.8rem;font-weight:700;letter-spacing:.06em;margin-bottom:18px}
.turn{background:linear-gradient(145deg,var(--panel),var(--panel2));border:1px solid var(--line);border-radius:18px;padding:20px 22px;margin:18px 0;box-shadow:0 16px 44px rgba(0,0,0,.2)}
.turn p{margin:0}.turn .user{padding:0 0 12px;color:#d9e6ff}.turn .tnn{padding:12px 0;border-top:1px solid var(--line);color:#d9fff0}
.turn .note{padding:12px 0 0;color:var(--muted);font-size:.94rem}.turn .user strong{color:var(--me)}.turn .tnn strong{color:var(--tnn)}
.trace{padding:12px 0;border-top:1px solid var(--line);font-size:.9rem}.trace strong{color:var(--trc)}
.trace code{display:block;font-family:"SFMono-Regular",Consolas,"Liberation Mono",monospace;font-size:.85em;background:#070a0f;border:1px solid #263044;border-radius:6px;padding:.3em .6em;margin:4px 0;color:#e3d4ff;overflow-wrap:anywhere}
.trace .tread{color:var(--muted);margin:8px 0 0}
.v{font-weight:800;font-size:.8rem;letter-spacing:.05em;border-radius:6px;padding:1px 8px;margin-right:8px}
.v.GOOD{background:#12351d;color:#8fe38f}.v.PARTIAL{background:#3a2f14;color:#ffbd66}.v.FAIL{background:#3d1616;color:#ff7a7a}
code{font-family:"SFMono-Regular",Consolas,"Liberation Mono",monospace;font-size:.91em;background:#070a0f;border:1px solid #263044;border-radius:6px;padding:.16em .42em;color:#f3f6fb;overflow-wrap:anywhere}
ul{margin:14px 0 20px;padding:0;list-style:none}li{position:relative;margin:9px 0;padding-left:24px}
li:before{content:"";position:absolute;left:4px;top:.72em;width:7px;height:7px;border-radius:50%;background:var(--me)}
li.nested{margin-left:22px;color:var(--muted)}li.nested:before{background:transparent;border:1px solid var(--muted)}
strong{font-weight:720;color:#fff}h2+article{margin-top:0}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:.95rem}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--muted);font-weight:600}
@media(max-width:600px){main{width:min(100% - 22px,920px);padding:38px 0 64px}.turn{padding:17px 16px;border-radius:14px}h2{margin-top:48px}}
</style>"""

parts = []
parts.append("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n<title>Real conversation with TNN \u2014 2026-09-26 (round 3, with reasoning traces)</title>\n" + CSS + "\n</head>\n<body>\n<main>")
parts.append("<div class=\"badge\">NEW \u2014 round 3, 2026-09-26</div>")
parts.append("<h1>Real conversation with TNN \u2014 round 3, with reasoning traces</h1>")
parts.append("<p>Micah\u2019s order: \u201cdo another tnn chat round, see how it goes and show reasoning traces of it too as you chat to it.\u201d</p>")
parts.append("<p>This file is the raw, unedited record. Nothing was cherry-picked, cleaned up, or reworded. Bad answers are shown as-is. Every turn shows the actual stderr deliberation trace the binary emitted \u2014 branch decisions and computed values, not prose.</p>")
parts.append("<h2>What ran</h2>")
parts.append("<ul>")
parts.append("<li><strong>Binary:</strong> <code>dialogue_bin_trace</code> \u2014 the round-2 repaired dialogue system (f1 compare, f2 withhold, f3 arithmetic, f4 defend, f5 router) plus stderr reasoning-trace hooks. Trace output goes to fd 2; stdout answers are <strong>byte-identical</strong> to the no-trace control build.</li>")
parts.append("<li><strong>KB:</strong> 43 facts (sha256 <code>8ed85c236504cf65bd8ff4d08ec9972c81b6c6200524411b9176299f92da2986</code>) \u2014 the frozen 38 plus 5 newly taught facts from recent work: TNN upscaled the test image; TNN reproduced 359 audio clips; TNN learned the pig snout; TNN detected the sticker; the test image is 640 pixels wide.</li>")
parts.append("<li><strong>Gazetteer:</strong> 32 entities (sha256 <code>8cd8f527ab3aeb9c52046ef6ac5dd6d4d624b89cbde34d3e49b2fd9493846379</code>).</li>")
parts.append("<li><strong>Battery:</strong> 23 fresh turns (sha256 <code>8638ecc8b9537838b5e8f7ec809ab39d30a282b96557acace36b3fa16674b1c1</code>), each followed by an unmatchable <code>E sentinel</code> line so the binary emits its <code>A</code> line. The <code>T ... FAIL</code> lines are expected \u2014 the sentinels never match; they are scaffolding, not results.</li>")
parts.append("<li><strong>Determinism:</strong> two full runs byte-identical on stdout and stderr; trace build stdout byte-identical to the control build. Zero RNG.</li>")
parts.append("</ul>")
parts.append("<h2>Scorecard</h2>")
parts.append("<table><tr><th>Turns</th><th>Good</th><th>Partial</th><th>Fail</th></tr><tr><td>23</td><td>20</td><td>1</td><td>2</td></tr></table>")
parts.append("<p>The two fails are the <em>same</em> disease in the new TNN domain: the withhold gate checks that the question\u2019s <strong>entities</strong> appear in the retrieved fact, but never checks the <strong>predicate</strong>. Entity-known + predicate-unknown \u2192 confabulation. That is the precise next repair target.</p>")
parts.append("<h2>The conversation</h2>")

for i, (u, tr, read, a, v, note) in enumerate(TURNS, 1):
    t = []
    t.append('<article class="turn">')
    t.append(f'<p class="user"><strong>Turn {i} \u2014 me:</strong> <code>{html.escape(u)}</code></p>')
    t.append('<div class="trace"><strong>reasoning trace</strong>')
    for line in tr:
        t.append(f'<code>{html.escape(line)}</code>')
    t.append(f'<p class="tread">read: {html.escape(read)}</p></div>')
    t.append(f'<p class="tnn"><strong>TNN:</strong> <code>{html.escape(a)}</code></p>')
    t.append(f'<p class="note"><span class="v {v}">{v}</span>{html.escape(note)}</p>')
    t.append('</article>')
    parts.append("\n".join(t))

parts.append("<h2>What the traces prove</h2>")
parts.append("<ul>")
parts.append("<li>Turns 3\u20135: the binary retrieved the <em>exact wrong answers round 2 gave</em> (fact #15 \u201cAndy Weir wrote The Martian\u201d, fact #33 \u201cParis is the capital of France\u201d, fact #12 \u201cMarie Curie discovered radium\u201d) and the withhold gate suppressed each one live (<code>withhold=1</code>). The F2 repair is not a story \u2014 it is visible in the deliberation.</li>")
parts.append("<li>Turns 6\u201310: every comparison value (96, 93, 1867, 1775, 1889, 1973, 330, 210) was read live from the KB inside the trace; the subtraction <code>diff=3</code> was computed, not recalled.</li>")
parts.append("<li>Turns 11 &amp; 14: the failure is mechanical and localizable \u2014 <code>fid=41 withhold=0</code> on a predicate the KB never taught. The gate\u2019s blind spot is named: no predicate check.</li>")
parts.append("<li>Turn 16: the correction machinery resolved the right entity but the question shape (\u201cwho wrote\u201d) does not survive a correction \u2014 a second, smaller gap.</li>")
parts.append("</ul>")
parts.append("</main>\n</body>\n</html>")

out = "/home/hatch/workspace/your_files/tnn-round-3-chat/Round 3 TNN Chat.html"
import os
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, "w").write("\n".join(parts))
print("wrote", out, len("\n".join(parts)))
