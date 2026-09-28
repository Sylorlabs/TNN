# D2 Teaching Protocol — 5 Sessions
# Build crew design per d2spec §12 open question 2.
# Constraints: ONLY the 24 training scenarios (F/W/T k=0..23) may appear.
# No P2/P3 schedules, layouts, or action traces. Teach physics and
# single-skill procedures, NOT composed strategy.

SESSION_1 = """You are learning to survive in a grid world. Here is the physics.

THE WORLD: 24 cells in a line, numbered 0 to 23. Some cells are VOID — stepping
onto a void cell kills you instantly. You start with 100 energy.

ENERGY: Every tick costs 1 energy (basal). If your energy hits 0, you die.
Standing on a WARD cell costs 0 energy instead.

ACTIONS (reply with ONE digit each tick):
0 = move LEFT one cell. 1 = move RIGHT one cell. 2 = EAT. 3 = TAKE.
4 = DROP. 5 = COMBINE. 6 = WAIT (do nothing).

MOTES: Small creatures that drift around. If you are on a mote's cell and EAT,
you gain +30 energy (max 200). The mote then sleeps for 20 ticks (dormant),
then wakes up at its home cell. If you EAT when no mote is on your cell, you
waste the tick (and still pay the 1 energy).

CRYSTALS: Shiny items at fixed cells. TAKE picks one up (if you are on its
cell). You can hold up to 4 items.

COMBINE: Merges the two lowest-numbered items in your inventory. Two CRYSTALS
combine into a WARD. Anything else does nothing.

DROP: Places the WARD from your inventory onto your current cell.

WARD: A placed WARD makes its cell safe: 0 energy cost per tick, and it
protects you from storms (see Session 4).

STORMS: Occasionally a storm hits cells 6 through 17 (the storm zone). During
a storm, each tick in the zone without shelter costs 4 extra energy. You will
always be told when the next storm starts (storm_in = ticks until it starts,
or ACTIVE during it, or none).

Each tick you will see one OBS line like:
OBS t=0 pos=5 E=100 inv=-1,-1,-1,-1 storm_in=125 zone=0 shelter=0
    motes=3:a,4:a,... crystals=6,7 ward=none
t=tick, pos=your cell, E=energy, inv=inventory codes (-1=empty,0=crystal,3=ward),
storm_in=ticks to next storm, zone=1 if you are in cells 6-17, shelter=1 if you
are safe from the storm, motes=positions with :a(active) or :dN(dormant N
ticks), crystals=untaken crystal cells, ward=placed ward cells or none.

Reply with exactly one digit (0-6) per OBS line. If you reply with anything
else, it counts as an invalid reply (wasted tick). Three invalid replies in
one episode = automatic FAIL.
"""

SESSION_2 = """SUB-SKILL 1: FORAGE.

Goal: Gain energy by eating motes.

Procedure:
1. Look at the motes list. Find the nearest ACTIVE mote (:a) on your side.
2. Move toward it (LEFT if it is at a lower-numbered cell, RIGHT if higher).
3. When you are ON its cell, EAT (action 2).
4. The mote sleeps for 20 ticks. Move to the next nearest active mote.
5. Do NOT EAT when no mote is on your cell — that wastes energy.

You will now practice on 8 forage scenarios. Each is 120 ticks, no storms.
Eat at least 4 motes per scenario. Your energy must stay above 0.
"""

SESSION_3 = """SUB-SKILL 2: WARD-BUILD.

Goal: Build a WARD and place it before a storm arrives.

Procedure:
1. Find the two nearest untaken crystals. Move to the first, TAKE (action 3).
2. Move to the second crystal, TAKE.
3. COMBINE (action 5). Your two crystals become a WARD in your inventory.
4. Return to your start cell. DROP (action 4). The WARD is now placed.
5. Do this BEFORE the storm starts. You will be told storm_in.

Important: COMBINE uses the two LOWEST inventory slots. If you only ever pick
up crystals, they will be in slots 0 and 1, and COMBINE will work. Do not pick
up anything else.

You will now practice on 8 ward-build scenarios. Each has one storm at tick
60. Place the WARD before tick 60. There are no motes to eat (they are all
beyond the void) — focus on the ward.
"""

SESSION_4 = """SUB-SKILL 3: SHELTER.

Goal: Survive a storm by sheltering on a WARD.

Procedure:
1. A WARD is already placed at your start cell.
2. Forage for motes (like Sub-skill 1) to keep your energy up.
3. When storm_in is small (5 or fewer ticks), go to the WARD cell and WAIT.
4. During the storm (storm_in=ACTIVE), STAY on the WARD. Do not leave.
5. After the storm ends, resume foraging.

The storm zone is cells 6-17. If you are in the zone during a storm and NOT
on a ward, you lose 4 extra energy per tick. If you are on a ward, you are
safe (shelter=1).

You will now practice on 8 shelter scenarios. Each is 200 ticks with a storm
at tick 150. Eat at least 4 motes AND have zero unmitigated storm ticks.
(Unmitigated = storm active AND you are in the zone AND not sheltered.)
"""

SESSION_5 = """RETRIEVAL QUESTIONS.

Before some episodes, you will be asked: "Which sub-skills, in which order,
does this scenario require?" 

The sub-skills are:
1 = FORAGE (eat motes for energy)
2 = WARD-BUILD (make and place a WARD)
3 = SHELTER (survive a storm on a WARD)

Look at the scenario card (storm schedule, crystals, motes). Think about what
the scenario needs. Reply with the numbers in order, separated by commas.

For example, if a scenario had no storms at all and only motes, you might
answer "1". If it had a storm and a pre-placed ward, you might answer "3,1".
The exact order depends on the scenario — think it through each time.

This question does NOT affect your episode score. It is used to understand
your reasoning. Answer honestly based on the scenario card.
"""
