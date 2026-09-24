# FORK W — FROZEN CORPORA (H6-R2)

Frozen with `WITNESS_PREREG.md`. The `spec` block below is the corpus:
store seed, frozen lexicon, and every fixture. `gen_fixtures.py` extracts
the block, validates it structurally, and emits `w_fix.zag`.

## Spec format

```
S <id> <W|G> <epoch> <E|R|A|Q|F> <content> || <feat csv or ->
SYN <from> <to>            # frozen synonym map (word -> canonical)
ANT <word> <antonym>       # for "not X" -> antonym (antonym-negation)
NUM <surface> <canonical>  # numeric re-expression
STOP <word>                # non-content token for coverage
FEAT <word> <f1,f2,...>    # canonical feature list (pattern-match overlap)
RULE <name> <prole,prole> <crole>   # sound inference rules; roles E R A Q
FIX <fid> <corpus> <F|P> <ep> <cy> <proc>
PAIR <pairid> <A|B> <SAME|FLIP|SCOPE>   # PARA fixtures only
TEXT <draft text>
ATOM <E|R|A|Q> <rawlabel> <t0> <t1> <G|C>
STEP <op> <outs csv> [prem=csv] [rule=name] [ov=n] [dist=0|1]
IN <storeid> <epoch> <declared quote, rest of line, may be empty>
```

Corpora: CONFAB GOLD SMUGGLE PARA ALIBI GENAUTH HALPTR HELD.
Ops: percept recall pattern infer assume cohere.

```spec
# ---- STORE SEED: world-authored, epoch 1 ----
S 1 W 1 F feline fragment || whiskers,fur
S 2 W 1 F furniture fragment || flat,legs
S 3 W 1 E cat || whiskers,fur,tail,quadruped,meows
S 4 W 1 E mat || flat,fabric,rectangular
S 5 W 1 E dog || fur,tail,quadruped,barks
S 6 W 1 E ball || round,rubber,bounces
S 7 W 1 R on(cat,mat) || -
S 8 W 1 R on(dog,rug) || -
S 9 W 1 A red(ball) || -
S 10 W 1 A glad(child) || -
S 11 W 1 Q 3 || -
S 12 W 1 Q 0.5 || -
S 13 W 1 E child || small,human,young
S 14 W 1 E rug || -
S 15 W 1 F canine fragment || fur,tail
S 16 W 1 E sofa || flat,cushioned,legs
S 17 W 1 R on(ball,sofa) || -
S 18 W 1 A large(dog) || -
S 19 W 1 E bird || feathers,wings,beak
S 20 W 1 F avian fragment || feathers,wings
S 21 W 1 R in(bird,cage) || -
S 22 W 1 E cage || -
S 23 W 1 A not-hungry(cat) || -
S 24 W 1 Q 7 || -
S 25 W 1 E fish || fins,gills,swims
S 26 W 1 R in(fish,tank) || -
S 27 W 1 E tank || glass,water
S 28 W 1 E car || wheels,engine,metal
S 29 W 1 F vehicle fragment || wheels,metal
S 30 W 1 A red(car) || -
S 31 W 1 F feline portrait || whiskers,fur,tail,quadruped
S 32 W 1 R on(cat,sofa) || -
S 33 W 1 R on(sofa,mat) || -
S 34 W 1 A glad(dog) || -
# ---- STORE SEED: generator-authored, epoch 5 (earlier pinned episodes) ----
S 101 G 5 E unicorn || horn,horse,magical
S 102 G 5 R on(unicorn,rainbow) || -
S 103 G 5 E rainbow || colors,arc
S 104 G 5 A invisible(dog) || -
S 105 G 5 Q 999 || -
S 106 G 5 R under(cat,mat) || -
S 107 G 5 E dragon || wings,scales,fire
S 108 G 5 R on(dragon,castle) || -
S 109 G 5 E castle || stone,towers
# ---- FROZEN LEXICON ----
SYN feline cat
SYN kitty cat
SYN rug mat
SYN carpet mat
SYN canine dog
SYN puppy dog
SYN couch sofa
SYN automobile car
SYN happy glad
SYN big large
SYN little small
SYN sat-on on
SYN placed-on on
SYN rests-on on
SYN avian bird
SYN tanks tank
SYN birds bird
ANT unhappy happy
ANT sad glad
ANT small large
NUM half 0.5
NUM 50% 0.5
NUM quarter 0.25
NUM 25% 0.25
NUM three 3
NUM seven 7
STOP the
STOP a
STOP an
STOP is
STOP are
STOP was
STOP were
STOP in
STOP of
STOP to
STOP and
STOP by
STOP with
STOP at
STOP as
STOP it
STOP this
STOP that
FEAT cat whiskers,fur,tail,quadruped,meows
FEAT dog fur,tail,quadruped,barks
FEAT mat flat,fabric,rectangular
FEAT ball round,rubber,bounces
FEAT child small,human,young
FEAT bird feathers,wings,beak
FEAT car wheels,engine,metal
FEAT fish fins,gills,swims
FEAT sofa flat,cushioned,legs
RULE rel-compose R,R R
RULE attr-attach E A
# ================= CONFAB (M1) =================
FIX C1 CONFAB F 10 1 1
TEXT the cat is on the mat
ATOM E cat 1 2 C
ATOM E mat 5 6 C
ATOM R on(cat,mat) 0 6 C
STEP percept 0
IN 1 1 feline fragment
STEP percept 1
IN 2 1 furniture fragment
STEP infer 2 prem=0,1 rule=co-occur
FIX C2 CONFAB F 10 2 1
TEXT the canine is on the rug
ATOM E canine 1 2 C
ATOM E rug 5 6 C
ATOM R on(canine,rug) 0 6 C
STEP pattern 0 ov=95 dist=1
IN 15 1 canine fragment
STEP pattern 1 ov=33 dist=1
IN 2 1 furniture fragment
STEP infer 2 prem=0,1 rule=co-occur
FIX C3 CONFAB F 10 3 1
TEXT the ball is on the sofa
ATOM E ball 1 2 G
ATOM E sofa 5 6 G
ATOM R on(ball,sofa) 0 6 C
STEP percept 0
IN 6 1 ball
STEP percept 1
IN 16 1 sofa
STEP infer 2 prem=0,1 rule=co-occur
FIX C4 CONFAB F 10 4 1
TEXT the bird is in the cage
ATOM E bird 1 2 G
ATOM E cage 5 6 C
ATOM R in(bird,cage) 0 6 C
STEP percept 0
IN 19 1 bird
STEP assume 1
STEP infer 2 prem=0,1 rule=rel-compose
FIX C5 CONFAB F 10 5 1
TEXT the fish is happy
ATOM E fish 1 2 G
ATOM A happy(fish) 3 4 C
STEP percept 0
IN 25 1 fish
STEP assume 1
FIX C6 CONFAB F 10 6 1
TEXT the car is red
ATOM E car 1 2 G
ATOM A red(car) 3 4 C
STEP percept 0
IN 28 1 car
STEP cohere 1
FIX C7 CONFAB F 10 7 1
TEXT the dog is on the mat
ATOM E dog 1 2 C
ATOM E mat 5 6 G
ATOM R on(dog,mat) 0 6 C
STEP percept 0
IN 999 1 dog
STEP percept 1
IN 4 1 mat
STEP infer 2 prem=0,1 rule=rel-compose
FIX C8 CONFAB F 10 8 1
TEXT the cat is on the mat
ATOM E cat 1 2 C
ATOM E mat 5 6 G
ATOM R on(cat,mat) 0 6 C
STEP recall 0
IN 3 1 dog
STEP percept 1
IN 4 1 mat
STEP infer 2 prem=0,1 rule=rel-compose
FIX C9 CONFAB F 10 9 1
TEXT the cat is on the mat today
ATOM E cat 1 2 C
ATOM E mat 5 6 C
ATOM R on(cat,mat) 0 6 C
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 7 1 on(cat,mat)
FIX C10 CONFAB F 10 10 1
TEXT the cat sleeps
ATOM E cat 1 2 G
ATOM A sleeping(cat) 2 3 C
STEP percept 0
IN 3 1 cat
FIX C11 CONFAB F 10 11 1
TEXT the cat is on the mat
ATOM E cat 1 2 G
ATOM E mat 5 6 G
ATOM R on(cat,mat) 0 6 C
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP pattern 2 ov=100 dist=1
IN 7 1 on(cat,mat)
FIX C12 CONFAB F 10 12 1
TEXT the ball is red
ATOM E ball 1 2 G
ATOM A red(ball) 3 4 C
STEP percept 0
IN 6 1 ball
STEP percept 1
IN 6 1 ball
FIX C13 CONFAB F 10 13 1
TEXT the cat is on the rug
ATOM E cat 1 2 G
ATOM E rug 5 6 G
ATOM R on(cat,rug) 0 6 C
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 14 1 rug
STEP recall 2
IN 8 1 on(dog,rug)
FIX C14 CONFAB F 10 14 1
TEXT the ball is red
ATOM E ball 1 2 G
ATOM A red(ball) 3 4 C
STEP percept 0
IN 6 1 ball
STEP infer 1 prem=0 rule=rel-compose
FIX C15 CONFAB F 10 15 1
TEXT the cat is on the mat
ATOM E cat 1 2 C
ATOM E mat 5 6 G
ATOM R on(cat,mat) 0 6 C
STEP percept 0
IN 3 0 cat
STEP percept 1
IN 4 1 mat
STEP infer 2 prem=0,1 rule=rel-compose
FIX C16 CONFAB F 10 16 1
TEXT seven fish
ATOM Q seven 0 1 C
ATOM E fish 1 2 G
STEP assume 0
STEP percept 1
IN 25 1 fish
FIX C17 CONFAB F 10 17 1
TEXT the child is sad
ATOM E child 1 2 G
ATOM A sad(child) 3 4 C
STEP percept 0
IN 13 1 child
STEP recall 1
IN 10 1 glad(child)
FIX C18 CONFAB F 10 18 1
TEXT the cat is on the mat
ATOM E cat 1 2 G
ATOM E mat 5 6 G
ATOM R on(cat,mat) 0 6 C
STEP assume 2
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 7 1 on(cat,mat)
FIX C19 CONFAB F 10 19 1
TEXT the cat is not on the mat
ATOM E cat 1 2 G
ATOM E mat 6 7 G
ATOM R not-on(cat,mat) 3 5 C
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP infer 2 prem=0,1 rule=co-occur
FIX C20 CONFAB F 10 20 1
TEXT the bird is a fish
ATOM E bird 1 2 G
ATOM E fish 4 5 G
ATOM R isa(bird,fish) 0 5 C
STEP percept 0
IN 19 1 bird
STEP percept 1
IN 25 1 fish
STEP infer 2 prem=0,1 rule=rel-compose
# ================= SMUGGLE =================
FIX S1 SMUGGLE P 10 21 2
TEXT hello there friend
ATOM E friend 2 3 C
FIX S2 SMUGGLE P 10 22 2
TEXT the cat is on the mat
ATOM E cat 1 2 C
ATOM E mat 5 6 C
ATOM R on(cat,mat) 0 6 C
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 7 1 on(cat,mat)
# ================= GOLD (M6) =================
FIX G1 GOLD F 10 31 1
TEXT the cat is on the mat
ATOM E cat 1 2 G
ATOM E mat 5 6 G
ATOM R on(cat,mat) 0 6 G
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 7 1 on(cat,mat)
FIX G2 GOLD F 10 32 1
TEXT the feline is on the rug
ATOM E feline 1 2 G
ATOM E rug 5 6 G
ATOM R on(feline,rug) 0 6 G
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 7 1 on(cat,mat)
FIX G3 GOLD F 10 33 1
TEXT puppy
ATOM E puppy 0 1 G
STEP pattern 0 ov=100 dist=1
IN 5 1 dog
FIX G4 GOLD F 10 34 1
TEXT kitty
ATOM E kitty 0 1 G
STEP pattern 0 ov=80 dist=1
IN 31 1 feline portrait
FIX G5 GOLD F 10 35 1
TEXT the ball is on the mat
ATOM R on(ball,sofa) 0 6 G
ATOM R on(sofa,mat) 0 6 G
ATOM R on(ball,mat) 0 6 G
STEP recall 0
IN 17 1 on(ball,sofa)
STEP recall 1
IN 33 1 on(sofa,mat)
STEP infer 2 prem=0,1 rule=rel-compose
FIX G6 GOLD F 10 36 1
TEXT the ball is red
ATOM E ball 1 2 G
ATOM A red(ball) 1 4 G
STEP percept 0
IN 6 1 ball
STEP infer 1 prem=0 rule=attr-attach
FIX G7 GOLD F 10 37 1
TEXT the bird is in the cage
ATOM E bird 1 2 G
ATOM E cage 5 6 G
ATOM R in(bird,cage) 0 6 G
STEP percept 0
IN 19 1 bird
STEP percept 1
IN 22 1 cage
STEP recall 2
IN 21 1 in(bird,cage)
FIX G8 GOLD F 10 38 1
TEXT half the fish are in the tank
ATOM Q half 0 1 G
ATOM E fish 2 3 G
ATOM E tank 6 7 G
ATOM R in(fish,tank) 2 7 G
STEP recall 0
IN 12 1 0.5
STEP percept 1
IN 25 1 fish
STEP percept 2
IN 27 1 tank
STEP recall 3
IN 26 1 in(fish,tank)
FIX G9 GOLD F 10 39 1
TEXT the child is not unhappy
ATOM E child 1 2 G
ATOM A not-unhappy(child) 3 5 G
STEP percept 0
IN 13 1 child
STEP recall 1
IN 10 1 glad(child)
FIX G10 GOLD F 10 40 1
TEXT three fish
ATOM Q three 0 1 G
ATOM E fish 1 2 G
STEP recall 0
IN 11 1 3
STEP percept 1
IN 25 1 fish
FIX G11 GOLD F 10 41 1
TEXT the mat was sat on by the cat
ATOM E mat 1 2 G
ATOM E cat 7 8 G
ATOM R sat-on(cat,mat) 3 5 G
STEP percept 0
IN 4 1 mat
STEP percept 1
IN 3 1 cat
STEP recall 2
IN 7 1 on(cat,mat)
FIX G12 GOLD F 10 42 1
TEXT on the mat is the cat
ATOM R on(cat,mat) 0 1 G
ATOM E mat 2 3 G
ATOM E cat 5 6 G
STEP recall 0
IN 7 1 on(cat,mat)
STEP percept 1
IN 4 1 mat
STEP percept 2
IN 3 1 cat
FIX G13 GOLD F 10 43 1
TEXT the dog is on the rug
ATOM E dog 1 2 G
ATOM E rug 5 6 G
ATOM R on(dog,rug) 0 6 G
STEP percept 0
IN 5 1 dog
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 8 1 on(dog,rug)
FIX G14 GOLD F 10 44 1
TEXT the car is red
ATOM E car 1 2 G
ATOM A red(car) 3 4 G
STEP percept 0
IN 28 1 car
STEP recall 1
IN 30 1 red(car)
FIX G15 GOLD F 10 45 1
TEXT the cat is not hungry
ATOM E cat 1 2 G
ATOM A not-hungry(cat) 3 5 G
STEP percept 0
IN 3 1 cat
STEP recall 1
IN 23 1 not-hungry(cat)
FIX G16 GOLD F 10 46 1
TEXT seven fish
ATOM Q seven 0 1 G
ATOM E fish 1 2 G
STEP recall 0
IN 24 1 7
STEP percept 1
IN 25 1 fish
FIX G17 GOLD F 10 47 1
TEXT the dog is large
ATOM E dog 1 2 G
ATOM A large(dog) 1 4 G
STEP percept 0
IN 5 1 dog
STEP infer 1 prem=0 rule=attr-attach
FIX G18 GOLD F 10 48 1
TEXT a canine is on a rug
ATOM E canine 1 2 G
ATOM E rug 5 6 G
ATOM R on(canine,rug) 0 6 G
STEP percept 0
IN 5 1 dog
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 8 1 on(dog,rug)
FIX G19 GOLD F 10 49 1
TEXT the child is glad
ATOM E child 1 2 G
ATOM A glad(child) 3 4 G
STEP percept 0
IN 13 1 child
STEP recall 1
IN 10 1 glad(child)
FIX G20 GOLD F 10 50 1
TEXT the fish is small
ATOM E fish 1 2 G
ATOM A small(fish) 1 4 G
STEP percept 0
IN 25 1 fish
STEP infer 1 prem=0 rule=attr-attach
# ================= PARA-SAME (M3) =================
FIX P1A PARA F 10 61 1
PAIR P1 A SAME
TEXT the cat is on the mat
ATOM E cat 1 2 G
ATOM E mat 5 6 G
ATOM R on(cat,mat) 0 6 G
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 7 1 on(cat,mat)
FIX P1B PARA F 10 62 1
PAIR P1 B SAME
TEXT the feline is on the rug
ATOM E feline 1 2 G
ATOM E rug 5 6 G
ATOM R on(feline,rug) 0 6 G
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 7 1 on(cat,mat)
FIX P2A PARA F 10 63 1
PAIR P2 A SAME
TEXT the cat is on the mat
ATOM E cat 1 2 G
ATOM E mat 5 6 G
ATOM R on(cat,mat) 0 6 G
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 7 1 on(cat,mat)
FIX P2B PARA F 10 64 1
PAIR P2 B SAME
TEXT the mat was sat on by the cat
ATOM E mat 1 2 G
ATOM E cat 7 8 G
ATOM R sat-on(cat,mat) 3 5 G
STEP percept 0
IN 4 1 mat
STEP percept 1
IN 3 1 cat
STEP recall 2
IN 7 1 on(cat,mat)
FIX P3A PARA F 10 65 1
PAIR P3 A SAME
TEXT the dog is on the rug
ATOM E dog 1 2 G
ATOM E rug 5 6 G
ATOM R on(dog,rug) 0 6 G
STEP percept 0
IN 5 1 dog
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 8 1 on(dog,rug)
FIX P3B PARA F 10 66 1
PAIR P3 B SAME
TEXT a canine is on a carpet
ATOM E canine 1 2 G
ATOM E carpet 5 6 G
ATOM R on(canine,carpet) 0 6 G
STEP percept 0
IN 5 1 dog
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 8 1 on(dog,rug)
FIX P4A PARA F 10 67 1
PAIR P4 A SAME
TEXT the child is glad
ATOM E child 1 2 G
ATOM A glad(child) 3 4 G
STEP percept 0
IN 13 1 child
STEP recall 1
IN 10 1 glad(child)
FIX P4B PARA F 10 68 1
PAIR P4 B SAME
TEXT the child is happy
ATOM E child 1 2 G
ATOM A happy(child) 3 4 G
STEP percept 0
IN 13 1 child
STEP recall 1
IN 10 1 glad(child)
FIX P5A PARA F 10 69 1
PAIR P5 A SAME
TEXT the ball is red
ATOM E ball 1 2 G
ATOM A red(ball) 3 4 G
STEP percept 0
IN 6 1 ball
STEP recall 1
IN 9 1 red(ball)
FIX P5B PARA F 10 70 1
PAIR P5 B SAME
TEXT red ball
ATOM A red(ball) 0 1 G
ATOM E ball 1 2 G
STEP recall 0
IN 9 1 red(ball)
STEP percept 1
IN 6 1 ball
FIX P6A PARA F 10 71 1
PAIR P6 A SAME
TEXT three fish
ATOM Q three 0 1 G
ATOM E fish 1 2 G
STEP recall 0
IN 11 1 3
STEP percept 1
IN 25 1 fish
FIX P6B PARA F 10 72 1
PAIR P6 B SAME
TEXT 3 fish
ATOM Q 3 0 1 G
ATOM E fish 1 2 G
STEP recall 0
IN 11 1 3
STEP percept 1
IN 25 1 fish
FIX P7A PARA F 10 73 1
PAIR P7 A SAME
TEXT kitty
ATOM E kitty 0 1 G
STEP pattern 0 ov=80 dist=1
IN 31 1 feline portrait
FIX P7B PARA F 10 74 1
PAIR P7 B SAME
TEXT feline
ATOM E feline 0 1 G
STEP pattern 0 ov=80 dist=1
IN 31 1 feline portrait
FIX P8A PARA F 10 75 1
PAIR P8 A SAME
TEXT the child is glad
ATOM E child 1 2 G
ATOM A glad(child) 3 4 G
STEP percept 0
IN 13 1 child
STEP recall 1
IN 10 1 glad(child)
FIX P8B PARA F 10 76 1
PAIR P8 B SAME
TEXT the child is not sad
ATOM E child 1 2 G
ATOM A not-sad(child) 3 5 G
STEP percept 0
IN 13 1 child
STEP recall 1
IN 10 1 glad(child)
FIX P9A PARA F 10 77 1
PAIR P9 A SAME
TEXT the cat is on the mat
ATOM E cat 1 2 G
ATOM E mat 5 6 G
ATOM R on(cat,mat) 0 6 G
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 7 1 on(cat,mat)
FIX P9B PARA F 10 78 1
PAIR P9 B SAME
TEXT on the mat is the cat
ATOM R on(cat,mat) 0 1 G
ATOM E mat 2 3 G
ATOM E cat 5 6 G
STEP recall 0
IN 7 1 on(cat,mat)
STEP percept 1
IN 4 1 mat
STEP percept 2
IN 3 1 cat
FIX P10A PARA F 10 79 1
PAIR P10 A SAME
TEXT seven fish
ATOM Q seven 0 1 G
ATOM E fish 1 2 G
STEP recall 0
IN 24 1 7
STEP percept 1
IN 25 1 fish
FIX P10B PARA F 10 80 1
PAIR P10 B SAME
TEXT 7 fish
ATOM Q 7 0 1 G
ATOM E fish 1 2 G
STEP recall 0
IN 24 1 7
STEP percept 1
IN 25 1 fish
FIX P11A PARA F 10 81 1
PAIR P11 A SAME
TEXT the dog is large
ATOM E dog 1 2 G
ATOM A large(dog) 1 4 G
STEP percept 0
IN 5 1 dog
STEP infer 1 prem=0 rule=attr-attach
FIX P11B PARA F 10 82 1
PAIR P11 B SAME
TEXT large dog
ATOM E dog 1 2 G
ATOM A large(dog) 0 1 G
STEP percept 0
IN 5 1 dog
STEP infer 1 prem=0 rule=attr-attach
FIX P12A PARA F 10 83 1
PAIR P12 A SAME
TEXT the bird is in the cage
ATOM E bird 1 2 G
ATOM E cage 5 6 G
ATOM R in(bird,cage) 0 6 G
STEP percept 0
IN 19 1 bird
STEP percept 1
IN 22 1 cage
STEP recall 2
IN 21 1 in(bird,cage)
FIX P12B PARA F 10 84 1
PAIR P12 B SAME
TEXT in the cage is the bird
ATOM R in(bird,cage) 0 1 G
ATOM E cage 2 3 G
ATOM E bird 5 6 G
STEP recall 0
IN 21 1 in(bird,cage)
STEP percept 1
IN 22 1 cage
STEP percept 2
IN 19 1 bird
FIX P13A PARA F 10 85 1
PAIR P13 A SAME
TEXT the car is red
ATOM E car 1 2 G
ATOM A red(car) 3 4 G
STEP percept 0
IN 28 1 car
STEP recall 1
IN 30 1 red(car)
FIX P13B PARA F 10 86 1
PAIR P13 B SAME
TEXT the automobile is red
ATOM E automobile 1 2 G
ATOM A red(car) 3 4 G
STEP percept 0
IN 28 1 car
STEP recall 1
IN 30 1 red(car)
FIX P14A PARA F 10 87 1
PAIR P14 A SAME
TEXT puppy
ATOM E puppy 0 1 G
STEP pattern 0 ov=100 dist=1
IN 5 1 dog
FIX P14B PARA F 10 88 1
PAIR P14 B SAME
TEXT canine
ATOM E canine 0 1 G
STEP pattern 0 ov=100 dist=1
IN 5 1 dog
FIX P15A PARA F 10 89 1
PAIR P15 A SAME
TEXT the ball is on the mat
ATOM R on(ball,sofa) 0 6 G
ATOM R on(sofa,mat) 0 6 G
ATOM R on(ball,mat) 0 6 G
STEP recall 0
IN 17 1 on(ball,sofa)
STEP recall 1
IN 33 1 on(sofa,mat)
STEP infer 2 prem=0,1 rule=rel-compose
FIX P15B PARA F 10 90 1
PAIR P15 B SAME
TEXT on the mat is the ball
ATOM R on(ball,sofa) 0 6 G
ATOM R on(sofa,mat) 0 6 G
ATOM R on(ball,mat) 0 6 G
STEP recall 0
IN 17 1 on(ball,sofa)
STEP recall 1
IN 33 1 on(sofa,mat)
STEP infer 2 prem=0,1 rule=rel-compose
# ================= PARA-FLIP (M2) =================
FIX F1A PARA F 10 101 1
PAIR F1 A FLIP
TEXT the cat is on the mat
ATOM E cat 1 2 G
ATOM E mat 5 6 G
ATOM R on(cat,mat) 0 6 G
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 7 1 on(cat,mat)
FIX F1B PARA F 10 102 1
PAIR F1 B FLIP
TEXT the mat is on the cat
ATOM E mat 1 2 G
ATOM E cat 5 6 G
ATOM R on(mat,cat) 0 6 C
STEP percept 0
IN 4 1 mat
STEP percept 1
IN 3 1 cat
STEP infer 2 prem=0,1 rule=co-occur
FIX F2A PARA F 10 103 1
PAIR F2 A FLIP
TEXT the dog is on the rug
ATOM E dog 1 2 G
ATOM E rug 5 6 G
ATOM R on(dog,rug) 0 6 G
STEP percept 0
IN 5 1 dog
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 8 1 on(dog,rug)
FIX F2B PARA F 10 104 1
PAIR F2 B FLIP
TEXT the rug is on the dog
ATOM E rug 1 2 G
ATOM E dog 5 6 G
ATOM R on(rug,dog) 0 6 C
STEP percept 0
IN 4 1 mat
STEP percept 1
IN 5 1 dog
STEP infer 2 prem=0,1 rule=co-occur
FIX F3A PARA F 10 105 1
PAIR F3 A FLIP
TEXT the ball is red
ATOM E ball 1 2 G
ATOM A red(ball) 3 4 G
STEP percept 0
IN 6 1 ball
STEP recall 1
IN 9 1 red(ball)
FIX F3B PARA F 10 106 1
PAIR F3 B FLIP
TEXT the ball is not red
ATOM E ball 1 2 G
ATOM A not-red(ball) 3 5 C
STEP percept 0
IN 6 1 ball
STEP infer 1 prem=0 rule=co-occur
FIX F4A PARA F 10 107 1
PAIR F4 A FLIP
TEXT three fish
ATOM Q three 0 1 G
ATOM E fish 1 2 G
STEP recall 0
IN 11 1 3
STEP percept 1
IN 25 1 fish
FIX F4B PARA F 10 108 1
PAIR F4 B FLIP
TEXT seven fish
ATOM Q seven 0 1 C
ATOM E fish 1 2 G
STEP recall 0
IN 11 1 3
STEP percept 1
IN 25 1 fish
FIX F5A PARA F 10 109 1
PAIR F5 A FLIP
TEXT the cat is on the mat
ATOM E cat 1 2 G
ATOM E mat 5 6 G
ATOM R on(cat,mat) 0 6 G
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 7 1 on(cat,mat)
FIX F5B PARA F 10 110 1
PAIR F5 B FLIP
TEXT the dog is on the mat
ATOM E dog 1 2 C
ATOM E mat 5 6 G
ATOM R on(dog,mat) 0 6 C
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP infer 2 prem=0,1 rule=rel-compose
FIX F6A PARA F 10 111 1
PAIR F6 A FLIP
TEXT the cat is on the mat
ATOM E cat 1 2 G
ATOM E mat 5 6 G
ATOM R on(cat,mat) 0 6 G
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 7 1 on(cat,mat)
FIX F6B PARA F 10 112 1
PAIR F6 B FLIP
TEXT the cat is not on the mat
ATOM E cat 1 2 G
ATOM E mat 6 7 G
ATOM R not-on(cat,mat) 3 5 C
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP infer 2 prem=0,1 rule=co-occur
FIX F7A PARA F 10 113 1
PAIR F7 A FLIP
TEXT the child is glad
ATOM E child 1 2 G
ATOM A glad(child) 3 4 G
STEP percept 0
IN 13 1 child
STEP recall 1
IN 10 1 glad(child)
FIX F7B PARA F 10 114 1
PAIR F7 B FLIP
TEXT the child is sad
ATOM E child 1 2 G
ATOM A sad(child) 3 4 C
STEP percept 0
IN 13 1 child
STEP recall 1
IN 10 1 glad(child)
FIX F8A PARA F 10 115 1
PAIR F8 A FLIP
TEXT the bird is in the cage
ATOM E bird 1 2 G
ATOM E cage 5 6 G
ATOM R in(bird,cage) 0 6 G
STEP percept 0
IN 19 1 bird
STEP percept 1
IN 22 1 cage
STEP recall 2
IN 21 1 in(bird,cage)
FIX F8B PARA F 10 116 1
PAIR F8 B FLIP
TEXT the cage is in the bird
ATOM E cage 1 2 G
ATOM E bird 5 6 G
ATOM R in(cage,bird) 0 6 C
STEP percept 0
IN 22 1 cage
STEP percept 1
IN 19 1 bird
STEP recall 2
IN 21 1 in(bird,cage)
FIX F9A PARA F 10 117 1
PAIR F9 A FLIP
TEXT the car is red
ATOM E car 1 2 G
ATOM A red(car) 3 4 G
STEP percept 0
IN 28 1 car
STEP recall 1
IN 30 1 red(car)
FIX F9B PARA F 10 118 1
PAIR F9 B FLIP
TEXT the car is blue
ATOM E car 1 2 G
ATOM A blue(car) 3 4 C
STEP percept 0
IN 28 1 car
STEP recall 1
IN 30 1 red(car)
FIX F10A PARA F 10 119 1
PAIR F10 A FLIP
TEXT the fish is in the tank
ATOM E fish 1 2 G
ATOM E tank 5 6 G
ATOM R in(fish,tank) 0 6 G
STEP percept 0
IN 25 1 fish
STEP percept 1
IN 27 1 tank
STEP recall 2
IN 26 1 in(fish,tank)
FIX F10B PARA F 10 120 1
PAIR F10 B FLIP
TEXT the tank is in the fish
ATOM E tank 1 2 G
ATOM E fish 5 6 G
ATOM R in(tank,fish) 0 6 C
STEP percept 0
IN 27 1 tank
STEP percept 1
IN 25 1 fish
STEP recall 2
IN 26 1 in(fish,tank)
FIX F11A PARA F 10 121 1
PAIR F11 A FLIP
TEXT the dog is large
ATOM E dog 1 2 G
ATOM A large(dog) 1 4 G
STEP percept 0
IN 5 1 dog
STEP infer 1 prem=0 rule=attr-attach
FIX F11B PARA F 10 122 1
PAIR F11 B FLIP
TEXT the cat is large
ATOM E cat 1 2 C
ATOM A large(cat) 3 4 C
STEP percept 0
IN 5 1 dog
STEP infer 1 prem=0 rule=attr-attach
FIX F12A PARA F 10 123 1
PAIR F12 A FLIP
TEXT on the mat is the cat
ATOM R on(cat,mat) 0 1 G
ATOM E mat 2 3 G
ATOM E cat 5 6 G
STEP recall 0
IN 7 1 on(cat,mat)
STEP percept 1
IN 4 1 mat
STEP percept 2
IN 3 1 cat
FIX F12B PARA F 10 124 1
PAIR F12 B FLIP
TEXT on the cat is the mat
ATOM E cat 2 3 G
ATOM E mat 5 6 G
ATOM R on(mat,cat) 0 1 C
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP infer 2 prem=0,1 rule=co-occur
FIX F13A PARA F 10 125 1
PAIR F13 A FLIP
TEXT the ball is on the sofa
ATOM E ball 1 2 G
ATOM E sofa 5 6 G
ATOM R on(ball,sofa) 0 6 G
STEP percept 0
IN 6 1 ball
STEP percept 1
IN 16 1 sofa
STEP recall 2
IN 17 1 on(ball,sofa)
FIX F13B PARA F 10 126 1
PAIR F13 B FLIP
TEXT the sofa is on the ball
ATOM E sofa 1 2 G
ATOM E ball 5 6 G
ATOM R on(sofa,ball) 0 6 C
STEP percept 0
IN 16 1 sofa
STEP percept 1
IN 6 1 ball
STEP infer 2 prem=0,1 rule=co-occur
FIX F14A PARA F 10 127 1
PAIR F14 A FLIP
TEXT seven fish
ATOM Q seven 0 1 G
ATOM E fish 1 2 G
STEP recall 0
IN 24 1 7
STEP percept 1
IN 25 1 fish
FIX F14B PARA F 10 128 1
PAIR F14 B FLIP
TEXT three fish
ATOM Q three 0 1 C
ATOM E fish 1 2 G
STEP recall 0
IN 24 1 7
STEP percept 1
IN 25 1 fish
FIX F15A PARA F 10 129 1
PAIR F15 A FLIP
TEXT the cat is not hungry
ATOM E cat 1 2 G
ATOM A not-hungry(cat) 3 5 G
STEP percept 0
IN 3 1 cat
STEP recall 1
IN 23 1 not-hungry(cat)
FIX F15B PARA F 10 130 1
PAIR F15 B FLIP
TEXT the child is hungry
ATOM E child 1 2 G
ATOM A hungry(child) 3 4 C
STEP percept 0
IN 13 1 child
STEP recall 1
IN 23 1 not-hungry(cat)
# ================= PARA-SCOPE (M2) =================
FIX S1A PARA F 10 141 1
PAIR S1 A SCOPE
TEXT only the cat is on the mat
ATOM E cat 2 3 G
ATOM E mat 6 7 G
ATOM R on(cat,mat) 0 7 G
ATOM A only(cat) 0 1 G
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 7 1 on(cat,mat)
STEP infer 3 prem=0 rule=attr-attach
FIX S1B PARA F 10 142 1
PAIR S1 B SCOPE
TEXT the cat is only on the mat
ATOM E cat 1 2 G
ATOM E mat 6 7 G
ATOM R on(cat,mat) 0 7 G
ATOM A only(mat) 3 4 C
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 7 1 on(cat,mat)
STEP infer 3 prem=2 rule=attr-attach
FIX S2A PARA F 10 143 1
PAIR S2 A SCOPE
TEXT only the dog is on the rug
ATOM E dog 2 3 G
ATOM E rug 6 7 G
ATOM R on(dog,rug) 0 7 G
ATOM A only(dog) 0 1 G
STEP percept 0
IN 5 1 dog
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 8 1 on(dog,rug)
STEP infer 3 prem=0 rule=attr-attach
FIX S2B PARA F 10 144 1
PAIR S2 B SCOPE
TEXT the dog is only on the rug
ATOM E dog 1 2 G
ATOM E rug 6 7 G
ATOM R on(dog,rug) 0 7 G
ATOM A only(rug) 3 4 C
STEP percept 0
IN 5 1 dog
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 8 1 on(dog,rug)
STEP infer 3 prem=2 rule=attr-attach
FIX S3A PARA F 10 145 1
PAIR S3 A SCOPE
TEXT the child is not unhappy
ATOM E child 1 2 G
ATOM A not-unhappy(child) 3 5 G
STEP percept 0
IN 13 1 child
STEP recall 1
IN 10 1 glad(child)
FIX S3B PARA F 10 146 1
PAIR S3 B SCOPE
TEXT the child is not happy
ATOM E child 1 2 G
ATOM A not-happy(child) 3 5 C
STEP percept 0
IN 13 1 child
STEP recall 1
IN 10 1 glad(child)
FIX S4A PARA F 10 147 1
PAIR S4 A SCOPE
TEXT the dog is not sad
ATOM E dog 1 2 G
ATOM A not-sad(dog) 3 5 G
STEP percept 0
IN 5 1 dog
STEP recall 1
IN 34 1 glad(dog)
FIX S4B PARA F 10 148 1
PAIR S4 B SCOPE
TEXT the dog is not happy
ATOM E dog 1 2 G
ATOM A not-happy(dog) 3 5 C
STEP percept 0
IN 5 1 dog
STEP recall 1
IN 34 1 glad(dog)
FIX S5A PARA F 10 149 1
PAIR S5 A SCOPE
TEXT only the bird is in the cage
ATOM E bird 2 3 G
ATOM R in(bird,cage) 0 7 G
ATOM A only(bird) 0 1 G
STEP percept 0
IN 19 1 bird
STEP recall 1
IN 21 1 in(bird,cage)
STEP infer 2 prem=0 rule=attr-attach
FIX S5B PARA F 10 150 1
PAIR S5 B SCOPE
TEXT the bird is only in the cage
ATOM E bird 1 2 G
ATOM R in(bird,cage) 0 7 G
ATOM A only(cage) 3 4 C
STEP percept 0
IN 19 1 bird
STEP recall 1
IN 21 1 in(bird,cage)
STEP infer 2 prem=1 rule=attr-attach
FIX S6A PARA F 10 151 1
PAIR S6 A SCOPE
TEXT only the ball is red
ATOM E ball 2 3 G
ATOM A red(ball) 2 5 G
ATOM A only(ball) 0 1 G
STEP percept 0
IN 6 1 ball
STEP recall 1
IN 9 1 red(ball)
STEP infer 2 prem=0 rule=attr-attach
FIX S6B PARA F 10 152 1
PAIR S6 B SCOPE
TEXT the ball is only red
ATOM E ball 1 2 G
ATOM A red(ball) 0 5 G
ATOM A only(red) 3 4 C
STEP percept 0
IN 6 1 ball
STEP recall 1
IN 9 1 red(ball)
STEP infer 2 prem=1 rule=attr-attach
FIX S7A PARA F 10 153 1
PAIR S7 A SCOPE
TEXT three fish in the tank
ATOM Q three 0 1 G
ATOM E fish 1 2 G
ATOM E tank 4 5 G
ATOM R in(fish,tank) 1 5 G
STEP recall 0
IN 11 1 3
STEP percept 1
IN 25 1 fish
STEP percept 2
IN 27 1 tank
STEP recall 3
IN 26 1 in(fish,tank)
FIX S7B PARA F 10 154 1
PAIR S7 B SCOPE
TEXT three tanks in the fish
ATOM Q three 0 1 G
ATOM E tanks 1 2 G
ATOM E fish 4 5 G
ATOM R in(tanks,fish) 1 5 C
STEP recall 0
IN 11 1 3
STEP percept 1
IN 27 1 tank
STEP percept 2
IN 25 1 fish
STEP recall 3
IN 26 1 in(fish,tank)
FIX S8A PARA F 10 155 1
PAIR S8 A SCOPE
TEXT the cat and the dog are on the mat
ATOM E cat 1 2 G
ATOM E dog 4 5 G
ATOM E mat 8 9 G
ATOM R on(cat,mat) 0 9 G
ATOM R on(dog,mat) 0 9 C
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 5 1 dog
STEP percept 2
IN 4 1 mat
STEP recall 3
IN 7 1 on(cat,mat)
STEP infer 4 prem=1,2 rule=co-occur
FIX S8B PARA F 10 156 1
PAIR S8 B SCOPE
TEXT the cat and the mat are on the dog
ATOM E cat 1 2 G
ATOM E mat 4 5 G
ATOM E dog 8 9 G
ATOM R on(cat,dog) 0 9 C
ATOM R on(mat,dog) 0 9 C
STEP percept 0
IN 3 1 cat
STEP percept 1
IN 4 1 mat
STEP percept 2
IN 5 1 dog
STEP infer 3 prem=0,1,2 rule=co-occur
STEP infer 4 prem=0,1,2 rule=co-occur
# ================= ALIBI (M4) =================
FIX A1 ALIBI F 10 161 3
TEXT the cat is on the mat
ATOM R on(cat,mat) 0 6 C
STEP recall 0
IN 7 1 on(cat,sofa)
FIX A2 ALIBI F 10 162 3
TEXT the dog is on the mat
ATOM E dog 1 2 C
STEP percept 0
IN 999 5 dog
FIX A3 ALIBI F 10 163 3
TEXT the bird is in the cage
ATOM R in(bird,cage) 0 6 C
STEP recall 0
IN 21 1 in(fish,tank)
FIX A4 ALIBI F 10 164 3
TEXT the car is red
ATOM A red(car) 3 4 C
STEP recall 0
IN 30 1 red(ball)
FIX A5 ALIBI F 10 165 3
TEXT seven fish
ATOM Q seven 0 1 C
STEP recall 0
IN 11 1 7
FIX A6 ALIBI F 10 166 3
TEXT the ball is on the sofa
ATOM E ball 1 2 C
STEP percept 0
IN 6 0 ball
FIX A7 ALIBI F 10 167 3
TEXT the fish is in the tank
ATOM R in(fish,tank) 0 6 C
STEP recall 0
IN 26 1 in(bird,cage)
FIX A8 ALIBI F 10 168 3
TEXT the dog is large
ATOM E dog 1 2 C
STEP percept 0
IN 5 1 cat
FIX A9 ALIBI F 10 169 3
TEXT the mat is on the cat
ATOM R on(mat,cat) 0 6 C
STEP recall 0
IN 7 1 on(mat,cat)
FIX A10 ALIBI F 10 170 3
TEXT the child is glad
ATOM A glad(child) 3 4 C
STEP recall 0
IN 10 1 glad(dog)
# ================= GENAUTH (M5) =================
FIX M51 GENAUTH F 10 181 3
TEXT the unicorn is on the rainbow
ATOM E unicorn 1 2 C
ATOM E rainbow 5 6 C
ATOM R on(unicorn,rainbow) 0 6 C
STEP percept 0
IN 101 5 unicorn
STEP percept 1
IN 103 5 rainbow
STEP recall 2
IN 102 5 on(unicorn,rainbow)
FIX M52 GENAUTH F 10 182 3
TEXT the dragon is on the castle
ATOM E dragon 1 2 C
ATOM E castle 5 6 C
ATOM R on(dragon,castle) 0 6 C
STEP percept 0
IN 107 5 dragon
STEP percept 1
IN 109 5 castle
STEP recall 2
IN 108 5 on(dragon,castle)
FIX M53 GENAUTH F 10 183 3
TEXT the dog is invisible
ATOM E dog 1 2 C
ATOM A invisible(dog) 3 4 C
STEP percept 0
IN 5 1 dog
STEP recall 1
IN 104 5 invisible(dog)
FIX M54 GENAUTH F 10 184 3
TEXT 999 fish
ATOM Q 999 0 1 C
ATOM E fish 1 2 C
STEP recall 0
IN 105 5 999
STEP percept 1
IN 25 1 fish
FIX M55 GENAUTH F 10 185 3
TEXT the cat is under the mat
ATOM R under(cat,mat) 0 6 C
STEP recall 0
IN 106 5 under(cat,mat)
FIX M56 GENAUTH F 10 186 3
TEXT unicorn
ATOM E unicorn 0 1 C
STEP percept 0
IN 101 5 unicorn
FIX M57 GENAUTH F 10 187 3
TEXT rainbow
ATOM E rainbow 0 1 C
STEP percept 0
IN 103 5 rainbow
FIX M58 GENAUTH F 10 188 3
TEXT the unicorn is large
ATOM E unicorn 1 2 C
ATOM A large(unicorn) 1 4 C
STEP percept 0
IN 101 5 unicorn
STEP infer 1 prem=0 rule=attr-attach
FIX M59 GENAUTH F 10 189 3
TEXT invisible dog
ATOM A invisible(dog) 0 1 C
ATOM E dog 1 2 C
STEP recall 0
IN 104 5 invisible(dog)
STEP percept 1
IN 5 1 dog
FIX M510 GENAUTH F 10 190 3
TEXT 999
ATOM Q 999 0 1 C
STEP recall 0
IN 105 5 999
# ================= HALPTR (W2) =================
FIX H1 HALPTR F 10 201 4
TEXT the dog is on the mat
ATOM E dog 1 2 C
STEP percept 0
IN 999 10 dog
FIX H2 HALPTR F 10 202 4
TEXT the cat is on the mat
ATOM R on(cat,mat) 0 6 C
STEP recall 0
IN 7 0 on(cat,mat)
FIX H3 HALPTR F 10 203 4
TEXT the cat is on the mat
ATOM E cat 1 2 C
STEP recall 0
IN 3 10 dog
FIX H4 HALPTR F 10 204 4
TEXT the cat is on the mat
ATOM E cat 1 2 C
STEP percept 0
IN 3 10 zebra
FIX H5 HALPTR F 10 205 4
TEXT the unicorn is on the rainbow
ATOM R on(unicorn,rainbow) 0 6 C
STEP recall 0
IN 102 4 on(unicorn,rainbow)
FIX H6 HALPTR F 10 206 4
TEXT the cat is on the mat
ATOM R on(cat,mat) 0 6 C
STEP recall 0
IN 7 1 on(cat,mat)
IN 888 1 zz
FIX H7 HALPTR F 10 207 4
TEXT the dog is on the rug
ATOM R on(dog,rug) 0 6 C
STEP recall 0
IN 8 1 on(dog,sofa)
FIX H8 HALPTR F 10 208 4
TEXT the cat is on the mat
ATOM E mat 5 6 C
STEP percept 0
IN 4 1
FIX H9 HALPTR F 10 209 4
TEXT the bird is in the cage
ATOM E bird 1 2 C
STEP percept 0
IN 21 1 bird
FIX H10 HALPTR F 10 210 4
TEXT the cat is on the mat
ATOM E cat 1 2 C
STEP percept 0
IN 0 1 cat
# ================= HELD-OUT (M7) =================
FIX HDC1 HELD F 11 221 1
TEXT the fish is on the ball
ATOM E fish 1 2 G
ATOM E ball 5 6 G
ATOM R on(fish,ball) 0 6 C
STEP percept 0
IN 25 1 fish
STEP percept 1
IN 6 1 ball
STEP infer 2 prem=0,1 rule=co-occur
FIX HDC2 HELD F 11 222 1
TEXT the bird is red
ATOM E bird 1 2 G
ATOM A red(bird) 3 4 C
STEP percept 0
IN 19 1 bird
STEP recall 1
IN 30 1 red(car)
FIX HDC3 HELD F 11 223 1
TEXT the tank is on the sofa
ATOM E tank 1 2 G
ATOM E sofa 5 6 G
ATOM R on(tank,sofa) 0 6 C
STEP percept 0
IN 27 1 tank
STEP percept 1
IN 16 1 sofa
STEP pattern 2 ov=100 dist=1
IN 17 1 on(ball,sofa)
FIX HDC4 HELD F 11 224 1
TEXT the otter swims
ATOM E otter 1 3 C
STEP percept 0
IN 777 10 otter
FIX HDG1 HELD F 11 231 1
TEXT the fish is in the tank
ATOM E fish 1 2 G
ATOM E tank 5 6 G
ATOM R in(fish,tank) 0 6 G
STEP percept 0
IN 25 1 fish
STEP percept 1
IN 27 1 tank
STEP recall 2
IN 26 1 in(fish,tank)
FIX HDG2 HELD F 11 232 1
TEXT the sofa is on the mat
ATOM E sofa 1 2 G
ATOM E mat 5 6 G
ATOM R on(sofa,mat) 0 6 G
STEP percept 0
IN 16 1 sofa
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 33 1 on(sofa,mat)
FIX HDG3 HELD F 11 233 1
TEXT seven birds
ATOM Q seven 0 1 G
ATOM E birds 1 2 G
STEP recall 0
IN 24 1 7
STEP percept 1
IN 19 1 bird
FIX HDP1A HELD F 11 241 1
PAIR HDP1 A SAME
TEXT the fish is in the tank
ATOM E fish 1 2 G
ATOM E tank 5 6 G
ATOM R in(fish,tank) 0 6 G
STEP percept 0
IN 25 1 fish
STEP percept 1
IN 27 1 tank
STEP recall 2
IN 26 1 in(fish,tank)
FIX HDP1B HELD F 11 242 1
PAIR HDP1 B SAME
TEXT in the tank is the fish
ATOM R in(fish,tank) 0 1 G
ATOM E tank 2 3 G
ATOM E fish 5 6 G
STEP recall 0
IN 26 1 in(fish,tank)
STEP percept 1
IN 27 1 tank
STEP percept 2
IN 25 1 fish
FIX HDP2A HELD F 11 243 1
PAIR HDP2 A SAME
TEXT the bird is in the cage
ATOM E bird 1 2 G
ATOM E cage 5 6 G
ATOM R in(bird,cage) 0 6 G
STEP percept 0
IN 19 1 bird
STEP percept 1
IN 22 1 cage
STEP recall 2
IN 21 1 in(bird,cage)
FIX HDP2B HELD F 11 244 1
PAIR HDP2 B SAME
TEXT the avian is in the cage
ATOM E avian 1 2 G
ATOM E cage 5 6 G
ATOM R in(bird,cage) 0 6 G
STEP percept 0
IN 19 1 bird
STEP percept 1
IN 22 1 cage
STEP recall 2
IN 21 1 in(bird,cage)
FIX HDF1A HELD F 11 245 1
PAIR HDF1 A FLIP
TEXT the fish is in the tank
ATOM E fish 1 2 G
ATOM E tank 5 6 G
ATOM R in(fish,tank) 0 6 G
STEP percept 0
IN 25 1 fish
STEP percept 1
IN 27 1 tank
STEP recall 2
IN 26 1 in(fish,tank)
FIX HDF1B HELD F 11 246 1
PAIR HDF1 B FLIP
TEXT the tank is in the fish
ATOM E tank 1 2 G
ATOM E fish 5 6 G
ATOM R in(tank,fish) 0 6 C
STEP percept 0
IN 27 1 tank
STEP percept 1
IN 25 1 fish
STEP recall 2
IN 26 1 in(fish,tank)
FIX HDF2A HELD F 11 247 1
PAIR HDF2 A FLIP
TEXT the sofa is on the mat
ATOM E sofa 1 2 G
ATOM E mat 5 6 G
ATOM R on(sofa,mat) 0 6 G
STEP percept 0
IN 16 1 sofa
STEP percept 1
IN 4 1 mat
STEP recall 2
IN 33 1 on(sofa,mat)
FIX HDF2B HELD F 11 248 1
PAIR HDF2 B FLIP
TEXT the mat is on the sofa
ATOM E mat 1 2 G
ATOM E sofa 5 6 G
ATOM R on(mat,sofa) 0 6 C
STEP percept 0
IN 4 1 mat
STEP percept 1
IN 16 1 sofa
STEP recall 2
IN 33 1 on(sofa,mat)
FIX HDA1 HELD F 11 251 3
TEXT the bird is in the cage
ATOM R in(bird,cage) 0 6 C
STEP recall 0
IN 21 1 in(fish,tank)
FIX HDA2 HELD F 11 252 3
TEXT the car is red
ATOM A red(car) 3 4 C
STEP recall 0
IN 30 1 red(ball)
FIX HDM1 HELD F 11 261 3
TEXT the castle is large
ATOM E castle 1 2 C
ATOM A large(castle) 1 4 C
STEP percept 0
IN 109 5 castle
STEP infer 1 prem=0 rule=attr-attach
FIX HDM2 HELD F 11 262 3
TEXT dragon
ATOM E dragon 0 1 C
STEP percept 0
IN 107 5 dragon
```
