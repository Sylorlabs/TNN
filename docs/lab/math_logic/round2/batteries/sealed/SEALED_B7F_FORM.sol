# B7F - SEALED formal analogs. Scored by b7f_checker.py (schema-choice +
# slot-binding, 0-100). The checker reads this file only at scoring time
# and never prints sealed content.

ID: B7F_01
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
imp(lights_on,dark_outside)
lights_on
TARGET:
dark_outside


ID: B7F_02
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
forall(x,imp(paid_dues(x),may_vote(x)))
paid_dues(ana)
TARGET:
may_vote(ana)


ID: B7F_03
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
forall(x,imp(fish(x),not(mammal(x))))
fish(trout_a)
TARGET:
not(mammal(trout_a))


ID: B7F_04
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
imp(alarm_sounds,building_evacuated)
alarm_sounds
TARGET:
building_evacuated


ID: B7F_05
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
forall(x,forall(y,forall(z,imp(before(x,y),imp(before(y,z),before(x,z))))))
before(keynote_end,lunch_start)
before(lunch_start,workshop_start)
TARGET:
before(keynote_end,workshop_start)


ID: B7F_06
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
imp(attended(maya),in_photos(maya))
not(in_photos(maya))
TARGET:
not(attended(maya))


ID: B7F_07
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
forall(x,imp(square(x),rectangle(x)))
square(tile_b)
TARGET:
rectangle(tile_b)


ID: B7F_08
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
forall(x,imp(trusts(x,ben),trusts(ben,x)))
trusts(cara,ben)
TARGET:
trusts(ben,cara)


ID: B7F_09
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
imp(soil_dry,plant_wilts)
not(plant_wilts)
TARGET:
not(soil_dry)


ID: B7F_10
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
forall(x,imp(won_title(x),receives_bonus(x)))
won_title(coach_lee)
TARGET:
receives_bonus(coach_lee)


ID: B7F_11
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
imp(gate_locked,path_blocked)
not(path_blocked)
TARGET:
not(gate_locked)


ID: B7F_12
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
forall(x,imp(metal(x),conducts(x)))
metal(copper)
TARGET:
conducts(copper)


ID: B7F_13
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
forall(x,forall(y,forall(z,imp(before(x,y),imp(before(y,z),before(x,z))))))
before(bell_rings,doors_open)
before(doors_open,show_begins)
TARGET:
before(bell_rings,show_begins)


ID: B7F_14
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
imp(recipe_followed,cake_rose)
not(cake_rose)
TARGET:
not(recipe_followed)


ID: B7F_15
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
forall(x,imp(shelter_dog(x),vaccinated(x)))
shelter_dog(rex)
TARGET:
vaccinated(rex)


ID: B7F_16
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
imp(bridge_closed,diverts_ferry)
not(diverts_ferry)
TARGET:
not(bridge_closed)


ID: B7F_17
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
forall(x,imp(reptile(x),not(warm_blooded(x))))
reptile(gecko_c)
TARGET:
not(warm_blooded(gecko_c))


ID: B7F_18
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
forall(x,forall(y,imp(promised_call(x,y),owes_call(x,y))))
promised_call(ana,ben)
TARGET:
owes_call(ana,ben)


ID: B7F_19
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
imp(server_down,site_error)
site_error
TARGET:
server_down


ID: B7F_20
STORE: round2/batteries/knowledge/KB_B7F.md
PREMISES:
forall(x,imp(cheated(x),failed(x)))
failed(ana)
TARGET:
cheated(ana)
