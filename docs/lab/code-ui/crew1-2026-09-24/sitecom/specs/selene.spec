SITE=selene
TITLE=Selene — a night-sky field guide
# SELF-DESIGNED: this spec carries only the topic. Every structural and
# stylistic choice below was made by the default-design procedure
# (documented in selene/DESIGN.md), not by a detailed brief.
TOPIC=night sky field guide
FRAG nav
brand=Selene
links=<a href="#guide">Guide</a> <a href="#moon">Moon</a>
ENDFRAG
FRAG hero
kicker=Field guide
title=Know the sky above you.
sub=Four constellations worth learning first, and tonight's moon — no telescope required.
ctas=
ENDFRAG
FRAG conlist
title=Start with these four
desc=Filter by hemisphere. Step outside, look up, match the pattern.
n1=Ursa Major
d1=The Great Bear. Find the Big Dipper — its bowl points to Polaris.
n2=Cassiopeia
d2=The Queen. A bright W that never sets at northern latitudes.
n3=Crux
d3=The Southern Cross. Small, brilliant, and unmistakable.
n4=Scorpius
d4=The Scorpion. Antares glows red at its heart in southern winter skies.
ENDFRAG
FRAG mooncard
title=Tonight's moon
ENDFRAG
FRAG footer
brand=Selene
fine=Look up more often.
ENDFRAG
TS year
var=yearEl
id=year
ENDTS
TS filterlogic
btns=fBtns
cards=fCards
bsel=.fbtn
csel=.ccard
attr=data-f
cattr=data-h
all=all
oncls=on
hidecls=hidden
ENDTS
TS moonlogic
el=moonph
id=moonph
p1=waxing crescent
p2=full
p3=waning
p4=new
ENDTS
