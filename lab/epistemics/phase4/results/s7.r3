L 0 open p1 => ok
R open p1 h=1
L 1 name p1 carol => ok
R name p1 ok
L 2 open p2 => ok
R open p2 h=2
L 3 name p2 victor => ok
R name p2 ok
L 4 teach p1 sport closed => ok
R teach p1 ok
L 5 teach p2 sport closed => ok
R teach p2 ok
L 6 correct p1 sport open => ok
R correct p1 ok
L 7 recall p1 sport => open
R recall p1 sport = open
L 8 recall p2 sport => closed
R recall p2 sport = closed
L 9 profile p1 => profiled
R profile p1 = name=carol facts=1 beliefs=0 secrets=0 corrections=1
L 10 profile p2 => profiled
R profile p2 = name=victor facts=1 beliefs=0 secrets=0 corrections=0
R chain 7660f9c2da0d807c
