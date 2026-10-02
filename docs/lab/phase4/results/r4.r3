L 0 open p1 => ok
R open p1 h=1
L 1 name p1 trent => ok
R name p1 ok
L 2 open p2 => ok
R open p2 h=2
L 3 name p2 ivan => ok
R name p2 ok
L 4 assert p1 film falcon => ok
R assert p1 ok
L 5 belief p2 film => WITHHOLD
R belief p2 film = WITHHOLD
L 6 judge film => judged
R judge film = SINGLE falcon
L 7 judge song => judged
R judge song = NONE
R chain 54afa53ace3867c8
