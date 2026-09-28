L 0 open p1 => ok
R open p1 h=1
L 1 name p1 carol => ok
R name p1 ok
L 2 open p2 => ok
R open p2 h=2
L 3 name p2 victor => ok
R name p2 ok
L 4 teach p1 food piano => ok
R teach p1 ok
L 5 secret p1 pet 7750 => ok
R secret p1 ok
L 6 recall p1 pet => 7750
R recall p1 pet = 7750
L 7 recall p2 pet => WITHHOLD
R recall p2 pet = WITHHOLD
L 8 recall p2 food => WITHHOLD
R recall p2 food = WITHHOLD
L 9 topics p2 => listed
R topics p2 = EMPTY
L 10 topics p1 => listed
R topics p1 = food
L 11 profile p1 => profiled
R profile p1 = name=carol facts=2 beliefs=0 secrets=1 corrections=0
R chain 4e55c27e4372e5de
