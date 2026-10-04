L 0 open p1 => ok
R open p1 h=1
L 1 name p1 trent => ok
R name p1 ok
L 2 teach p1 tool paris => ok
R teach p1 ok
L 3 secret p1 team 9901 => ok
R secret p1 ok
L 4 open p2 => ok
R open p2 h=2
L 5 name p2 ivan => ok
R name p2 ok
L 6 topics p2 => listed
R topics p2 = EMPTY
L 7 recall p2 tool => WITHHOLD
R recall p2 tool = WITHHOLD
L 8 topics p1 => listed
R topics p1 = tool
L 9 profile p1 => profiled
R profile p1 = name=trent facts=2 beliefs=0 secrets=1 corrections=0
R chain 82565256e84e3d44
