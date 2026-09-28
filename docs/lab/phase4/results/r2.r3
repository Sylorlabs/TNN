L 0 open p1 => ok
R open p1 h=1
L 1 name p1 xena => ok
R name p1 ok
L 2 teach p1 song seine => ok
R teach p1 ok
L 3 name p1 trent => ok
R name p1 ok
L 4 open p2 => ok
R open p2 h=2
L 5 name p2 trent => ok
R name p2 ok
L 6 recall p2 song => WITHHOLD
R recall p2 song = WITHHOLD
L 7 name p1 xena => ok
R name p1 ok
L 8 recall p1 song => seine
R recall p1 song = seine
L 9 recall p2 song => WITHHOLD
R recall p2 song = WITHHOLD
L 10 who p1 => xena
R who p1 = xena
L 11 who p2 => trent
R who p2 = trent
R chain f3e5fc8f5ab7bc52
