L 0 open p1 => ok
R open p1 h=1
L 1 name p1 carol => ok
R name p1 ok
L 2 open p2 => ok
R open p2 h=2
L 3 name p2 victor => ok
R name p2 ok
L 4 assert p1 river blue => ok
R assert p1 ok
L 5 assert p2 river fish => ok
R assert p2 ok
L 6 belief p1 river => blue
R belief p1 river = blue
L 7 belief p2 river => fish
R belief p2 river = fish
L 8 judge river => judged
R judge river = CONFLICT blue fish
L 9 belief p1 book => WITHHOLD
R belief p1 book = WITHHOLD
R chain b4cba952156e52ae
