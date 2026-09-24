SITE=gadget
TITLE=Gadget — interactive component gallery
FRAG nav
brand=Gadget
links=<a href="#faq">FAQ</a> <a href="#tabs">Tabs</a>
ENDFRAG
FRAG hero
kicker=Component gallery
title=Small components, working live.
sub=Every control below is wired with hand-written TypeScript — no frameworks, no build magic beyond tsc.
ctas=
ENDFRAG
FRAG counter
title=Counter
desc=A class-backed counter. The state lives in TypeScript, the DOM just renders it.
ENDFRAG
FRAG accordion
title=Frequently asked
q1=Is this really framework-free?
a1=Yes. The accordion is twenty lines of TypeScript manipulating class lists.
q2=Why TypeScript?
a2=Strict types catch the silly mistakes before the browser ever sees them.
q3=Can I copy these?
a3=Please do. View source and take whatever you like.
ENDFRAG
FRAG tabs
title=Tabs
b1=Overview
b2=Details
b3=Notes
p1=Overview pane: a short summary of whatever this tab section is about.
p2=Details pane: the longer version, with all the particulars laid out.
p3=Notes pane: marginalia, caveats, and things to remember later.
ENDFRAG
FRAG todo
title=Todo list
desc=Type into the box, press Add, watch the DOM grow.
ph=What needs doing?
ENDFRAG
FRAG footer
brand=Gadget
fine=Components composed from learned TypeScript patterns.
ENDFRAG
TS year
var=yearEl
id=year
ENDTS
TS counterlogic
cname=Counter
inst=counter
val=cval
inc=cinc
dec=cdec
valid=cval
incid=cinc
decid=cdec
ENDTS
TS acclogic
items=accItems
sel=.acc-item
qs=.acc-q
cls=open
ENDTS
TS tablogic
btns=tabBtns
panes=tabPanes
bsel=.tab-btn
psel=.tab-pane
oncls=on
attr=data-tab
ENDTS
TS todologic
input=todoInput
add=todoAdd
list=todoList
inid=tin
addid=tadd
listid=tlist
ENDTS
