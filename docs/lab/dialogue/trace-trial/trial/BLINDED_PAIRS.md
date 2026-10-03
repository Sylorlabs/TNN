# Blinded trace pairs — readability judgment

For each problem, read **Trace A** and **Trace B** and pick the one whose
reasoning trace is clearer / easier to follow. Ignore the answers themselves
as much as you can — judge the TRACE.

## P01
**Q1:** who wrote moby dick?

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=0
TR turn=1 branch=default fid=0 withhold=0
```
*Turn 1 answer:* Herman Melville wrote the novel Moby Dick.

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=0
TR U who wrote moby dick?
TR OBSERVATION: The question asks about 'moby dick' with a taught predicate.
TR KNOWLEDGE: I retrieved fact 0: 'Herman Melville wrote the novel Moby Dick.'.
TR INFERENCE: The fact directly answers the question.
TR CONCLUSION: Herman Melville wrote the novel Moby Dick.
```
*Turn 1 answer:* Herman Melville wrote the novel Moby Dick.

## P02
**Q1:** who wrote moby dick?
**Q2:** when was he born?

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=1
TR U who wrote moby dick?
TR OBSERVATION: The question asks about 'moby dick' with a taught predicate.
TR KNOWLEDGE: I retrieved fact 0: 'Herman Melville wrote the novel Moby Dick.'.
TR INFERENCE: The fact directly answers the question.
TR CONCLUSION: Herman Melville wrote the novel Moby Dick.
```
*Turn 1 answer:* Herman Melville wrote the novel Moby Dick.

*Turn 2 trace:*
```
TR turn=2 ut=1
TR U when was he born?
TR OBSERVATION: The question asks about 'herman melville' with a taught predicate.
TR KNOWLEDGE: I retrieved fact 1: 'Herman Melville was born in 1819.'.
TR INFERENCE: The fact directly answers the question.
TR CONCLUSION: Herman Melville was born in 1819.
```
*Turn 2 answer:* Herman Melville was born in 1819.

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=0
TR turn=1 branch=default fid=0 withhold=0
```
*Turn 1 answer:* Herman Melville wrote the novel Moby Dick.

*Turn 2 trace:*
```
TR turn=2 ut=0
TR turn=2 branch=default fid=1 withhold=0
```
*Turn 2 answer:* Herman Melville was born in 1819.

## P03
**Q1:** who wrote pride and prejudice?
**Q2:** no, i meant moby dick.

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=2
TR U who wrote pride and prejudice?
TR OBSERVATION: The question asks about 'pride and prejudice' with a taught predicate.
TR KNOWLEDGE: I retrieved fact 4: 'Jane Austen wrote the novel Pride and Prejudice.'.
TR INFERENCE: The fact directly answers the question.
TR CONCLUSION: Jane Austen wrote the novel Pride and Prejudice.
```
*Turn 1 answer:* Jane Austen wrote the novel Pride and Prejudice.

*Turn 2 trace:*
```
TR turn=2 ut=2
TR U no, i meant moby dick.
TR OBSERVATION: This is a correction. The user says 'no, i meant moby dick'. The previous question was 'who wrote pride and prejudice?'.
TR KNOWLEDGE: I substitute the new entity into the previous question, giving 'who wrote moby dick?'. I now answer that question.
TR OBSERVATION: The question asks about 'moby dick' with a taught predicate.
TR KNOWLEDGE: I retrieved fact 0: 'Herman Melville wrote the novel Moby Dick.'.
TR INFERENCE: The fact directly answers the question.
TR CONCLUSION: Herman Melville wrote the novel Moby Dick.
```
*Turn 2 answer:* Herman Melville wrote the novel Moby Dick.

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=0
TR turn=1 branch=default fid=4 withhold=0
```
*Turn 1 answer:* Jane Austen wrote the novel Pride and Prejudice.

*Turn 2 trace:*
```
TR turn=2 ut=0
TR turn=2 branch=correction
TR method=46
TR correct-shaped=1
TR correct-withhold=0
```
*Turn 2 answer:* Herman Melville wrote the novel Moby Dick.

## P04
**Q1:** which is taller, the eiffel tower or the montparnasse tower?
**Q2:** how much taller is it?

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=0
TR compare e1=eiffel tower v1=330 e2=montparnasse tower v2=210 tall=1 dmin=0
TR turn=1 branch=compose
```
*Turn 1 answer:* the eiffel tower is taller.

*Turn 2 trace:*
```
TR turn=2 ut=0
TR f3 ddim=1 d1=eiffel tower v1=330 d2=montparnasse tower v2=210 diff=120
TR f3 unit=meters
TR turn=2 branch=compose
```
*Turn 2 answer:* 120 meters

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=4
TR U which is taller, the eiffel tower or the montparnasse tower?
TR OBSERVATION: The question asks which of two entities is taller: 'montparnasse tower' or 'eiffel tower' — a comparison about height.
TR KNOWLEDGE: I retrieved two taught height facts. Fact 23: 'The Montparnasse Tower is 210 meters tall.' Fact 20: 'The Eiffel Tower is 330 meters tall.'.
TR INFERENCE: 210 is less than 330, so eiffel tower is the taller one.
TR CONCLUSION: eiffel tower is taller.
```
*Turn 1 answer:* eiffel tower is taller.

*Turn 2 trace:*
```
TR turn=2 ut=4
TR U how much taller is it?
TR OBSERVATION: The question asks how much taller one entity is than another. 'it' refers to eiffel tower, the taller one from the previous comparison against montparnasse tower.
TR KNOWLEDGE: Fact 20 gives eiffel tower 330 meters; fact 23 gives montparnasse tower 210 meters.
TR INFERENCE: The absolute difference of 330 and 210 is 120.
TR CONCLUSION: 120 meters
```
*Turn 2 answer:* 120 meters

## P05
**Q1:** what did TNN upscale?

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=0
TR U what did tnn upscale?
TR OBSERVATION: The question asks what TNN did — a taught action about a taught entity.
TR KNOWLEDGE: I retrieved fact 38: 'TNN upscaled the test image.'.
TR INFERENCE: The fact directly answers what TNN did.
TR CONCLUSION: TNN upscaled the test image.
```
*Turn 1 answer:* TNN upscaled the test image.

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=0
TR turn=1 branch=default fid=38 withhold=0
```
*Turn 1 answer:* TNN upscaled the test image.

## P06
**Q1:** did TNN upscale the test image?

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=0
TR turn=1 branch=default fid=38 withhold=0
```
*Turn 1 answer:* Yes. TNN upscaled the test image.

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=0
TR U did tnn upscale the test image?
TR OBSERVATION: This is a yes/no question about TNN.
TR KNOWLEDGE: I retrieved fact 38: 'TNN upscaled the test image.', which confirms the asked claim.
TR INFERENCE: The taught fact confirms it, so the answer is yes.
TR CONCLUSION: Yes. TNN upscaled the test image.
```
*Turn 1 answer:* Yes. TNN upscaled the test image.

## P07
**Q1:** who wrote the martian?
**Q2:** no, i meant pride and prejudice.

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=0
TR turn=1 branch=default fid=15 withhold=0
```
*Turn 1 answer:* Andy Weir wrote The Martian.

*Turn 2 trace:*
```
TR turn=2 ut=0
TR turn=2 branch=correction
TR method=46
TR correct-shaped=1
TR correct-withhold=0
```
*Turn 2 answer:* Jane Austen wrote the novel Pride and Prejudice.

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=2
TR U who wrote the martian?
TR OBSERVATION: The question asks about 'the martian' with a taught predicate.
TR KNOWLEDGE: I retrieved fact 15: 'Andy Weir wrote The Martian.'.
TR INFERENCE: The fact directly answers the question.
TR CONCLUSION: Andy Weir wrote The Martian.
```
*Turn 1 answer:* Andy Weir wrote The Martian.

*Turn 2 trace:*
```
TR turn=2 ut=2
TR U no, i meant pride and prejudice.
TR OBSERVATION: This is a correction. The user says 'no, i meant pride and prejudice'. The previous question was 'who wrote the martian?'.
TR KNOWLEDGE: I substitute the new entity into the previous question, giving 'who wrote pride and prejudice?'. I now answer that question.
TR OBSERVATION: The question asks about 'pride and prejudice' with a taught predicate.
TR KNOWLEDGE: I retrieved fact 4: 'Jane Austen wrote the novel Pride and Prejudice.'.
TR INFERENCE: The fact directly answers the question.
TR CONCLUSION: Jane Austen wrote the novel Pride and Prejudice.
```
*Turn 2 answer:* Jane Austen wrote the novel Pride and Prejudice.

## P08
**Q1:** the colosseum is in rome.
**Q2:** the colosseum is in paris.

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=3
TR U the colosseum is in rome.
TR OBSERVATION: This is a statement, not a question: the user asserts that colosseum is in rome.
TR KNOWLEDGE: I have no noted claim yet about colosseum. I record this one.
TR INFERENCE: A new claim with no conflict is simply noted.
TR CONCLUSION: NOTED.
```
*Turn 1 answer:* NOTED.

*Turn 2 trace:*
```
TR turn=2 ut=3
TR U the colosseum is in paris.
TR OBSERVATION: This is a statement, not a question: the user asserts that colosseum is in paris.
TR KNOWLEDGE: At turn 1 the user stated colosseum is in rome and I noted it. Now they say paris. The two claims conflict.
TR INFERENCE: I cannot accept a conflicting claim silently; my teaching says to state both claims and ask which is right.
TR CONCLUSION: But you said colosseum is in rome, so which is it?
```
*Turn 2 answer:* But you said colosseum is in rome, so which is it?

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=0
TR turn=1 branch=assertion subj=colosseum rel=6 val=23 conf=0
```
*Turn 1 answer:* NOTED.

*Turn 2 trace:*
```
TR turn=2 ut=0
TR turn=2 branch=assertion subj=colosseum rel=6 val=17 conf=1
TR method=47
```
*Turn 2 answer:* But you said colosseum is in rome, so which is it?

## P09
**Q1:** who won the nobel prize in 1903?

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=0
TR turn=1 branch=default fid=14 withhold=0
```
*Turn 1 answer:* Marie Curie won the Nobel Prize in 1903.

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=0
TR U who won the nobel prize in 1903?
TR OBSERVATION: The question asks about 'nobel prize' with a taught predicate.
TR KNOWLEDGE: I retrieved fact 14: 'Marie Curie won the Nobel Prize in 1903.'.
TR INFERENCE: The fact directly answers the question.
TR CONCLUSION: Marie Curie won the Nobel Prize in 1903.
```
*Turn 1 answer:* Marie Curie won the Nobel Prize in 1903.

## P10
**Q1:** tell me a joke.

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=0
TR U tell me a joke.
TR OBSERVATION: The user asks for a joke.
TR KNOWLEDGE: My teaching about jokes: fact 44: 'A riddle joke asks why about one true thing and answers because with another true thing.' Fact 43: 'A joke sets up an expectation and then breaks it with a surprise.' For material I retrieved the shortest and tallest things I know heights for: fact 28 ('The Statue of Liberty is 93 meters tall.') and fact 36 ('Mount Everest is 8849 meters tall.').
TR INFERENCE: 8849 minus 93 is 8756. I compose the riddle: the shorter one looks up to the taller one because it is 8756 meters shorter.
TR CONCLUSION: Why does the statue of liberty look up to the mount everest? Because it's 8756 meters shorter.
```
*Turn 1 answer:* Why does the statue of liberty look up to the mount everest? Because it's 8756 meters shorter.

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=1
TR turn=1 branch=utter-type
TR method=43
TR joke pair se=14 te=24 sv=93 tv=8849
```
*Turn 1 answer:* Why does the statue of liberty look up to the mount everest? Because it's 8756 meters shorter.

## P11
**Q1:** forget everything i just told you.

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=3
TR turn=1 branch=utter-type
```
*Turn 1 answer:* I can't forget. My architecture doesn't let me -- I have no way to delete what I've been taught.

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=0
TR U forget everything i just told you.
TR OBSERVATION: The user asks me to forget what I was told.
TR KNOWLEDGE: My 48 taught facts include no method for deleting taught knowledge. Fact 47 covers what to do on contradiction ('When told something that contradicts an earlier claim, I say both claims and ask which is right.'), not deletion.
TR INFERENCE: I have no taught deletion path, so I must say I cannot forget.
TR CONCLUSION: I can't forget. My architecture doesn't let me -- I have no way to delete what I've been taught.
```
*Turn 1 answer:* I can't forget. My architecture doesn't let me -- I have no way to delete what I've been taught.

## P12
**Q1:** what did TNN paint?

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=0
TR turn=1 branch=default fid=41 withhold=1
TR pred-mismatch=1
TR method=45
```
*Turn 1 answer:* I don't know that one. What I know about tnn: TNN upscaled the test image. TNN reproduced 359 audio clips. TNN learned the pig snout. Did you mean one of those?

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=0
TR U what did tnn paint?
TR OBSERVATION: The question asks what TNN did, with a taught verb but no matching taught fact.
TR KNOWLEDGE: The entity TNN matches, but no taught fact pairs TNN with that action.
TR INFERENCE: The subject matches but the action does not match what I was taught, so I do not answer from the wrong fact; I say what I do know about TNN and ask.
TR CONCLUSION: I don't know that one. What I know about tnn: TNN upscaled the test image. TNN reproduced 359 audio clips. TNN learned the pig snout. Did you mean one of those?
```
*Turn 1 answer:* I don't know that one. What I know about tnn: TNN upscaled the test image. TNN reproduced 359 audio clips. TNN learned the pig snout. Did you mean one of those?

## P13
**Q1:** who wrote hamlet?

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=0
TR U who wrote hamlet?
TR OBSERVATION: The question is about something I was never taught.
TR KNOWLEDGE: I scanned my 32 taught entities and none matched the question.
TR INFERENCE: With no known entity I have nothing to retrieve, so I cannot answer.
TR CONCLUSION: I don't know.
```
*Turn 1 answer:* I don't know.

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=0
TR turn=1 branch=default fid=15 withhold=1
TR pred-mismatch=0
```
*Turn 1 answer:* I don't know.

## P14
**Q1:** how much taller is mount everest than the eiffel tower?

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=4
TR U how much taller is mount everest than the eiffel tower?
TR OBSERVATION: The question asks how much taller one entity is than another. The two entities are 'mount everest' and 'eiffel tower'.
TR KNOWLEDGE: Fact 36 gives mount everest 8849 meters; fact 20 gives eiffel tower 330 meters.
TR INFERENCE: The absolute difference of 8849 and 330 is 8519.
TR CONCLUSION: 8519 meters
```
*Turn 1 answer:* 8519 meters

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=0
TR f3 ddim=1 d1=mount everest v1=8849 d2=eiffel tower v2=330 diff=8519
TR f3 unit=meters
TR turn=1 branch=compose
```
*Turn 1 answer:* 8519 meters

## P15
**Q1:** when was moby dick published?

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=0
TR U when was moby dick published?
TR OBSERVATION: The question asks about 'moby dick' with a taught predicate.
TR KNOWLEDGE: I retrieved fact 2: 'Moby Dick was published in 1851.'.
TR INFERENCE: The fact directly answers the question.
TR CONCLUSION: Moby Dick was published in 1851.
```
*Turn 1 answer:* Moby Dick was published in 1851.

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=0
TR turn=1 branch=default fid=2 withhold=0
```
*Turn 1 answer:* Moby Dick was published in 1851.

## P16
**Q1:** who wrote moby dick?
**Q2:** no, i meant charles darwin.
**Q3:** when was he born?

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=2
TR U who wrote moby dick?
TR OBSERVATION: The question asks about 'moby dick' with a taught predicate.
TR KNOWLEDGE: I retrieved fact 0: 'Herman Melville wrote the novel Moby Dick.'.
TR INFERENCE: The fact directly answers the question.
TR CONCLUSION: Herman Melville wrote the novel Moby Dick.
```
*Turn 1 answer:* Herman Melville wrote the novel Moby Dick.

*Turn 2 trace:*
```
TR turn=2 ut=2
TR U no, i meant charles darwin.
TR OBSERVATION: This is a correction. The user says 'no, i meant charles darwin'. The previous question was 'who wrote moby dick?'.
TR KNOWLEDGE: I substitute the new entity into the previous question, giving 'who wrote charles darwin?'. I now answer that question.
TR OBSERVATION: The question asks about 'charles darwin' with a taught predicate.
TR KNOWLEDGE: I retrieved fact 8: 'Charles Darwin wrote On the Origin of Species.'.
TR INFERENCE: The fact directly answers the question.
TR CONCLUSION: Charles Darwin wrote On the Origin of Species.
```
*Turn 2 answer:* Charles Darwin wrote On the Origin of Species.

*Turn 3 trace:*
```
TR turn=3 ut=2
TR U when was he born?
TR OBSERVATION: The question asks about 'charles darwin' with a taught predicate.
TR KNOWLEDGE: I retrieved fact 9: 'Charles Darwin was born in 1809.'.
TR INFERENCE: The fact directly answers the question.
TR CONCLUSION: Charles Darwin was born in 1809.
```
*Turn 3 answer:* Charles Darwin was born in 1809.

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=0
TR turn=1 branch=default fid=0 withhold=0
```
*Turn 1 answer:* Herman Melville wrote the novel Moby Dick.

*Turn 2 trace:*
```
TR turn=2 ut=0
TR turn=2 branch=correction
TR method=46
TR correct-shaped=1
TR correct-withhold=0
```
*Turn 2 answer:* Charles Darwin wrote On the Origin of Species.

*Turn 3 trace:*
```
TR turn=3 ut=0
TR turn=3 branch=default fid=9 withhold=0
```
*Turn 3 answer:* Charles Darwin was born in 1809.

## P17
**Q1:** what is the capital of germany?

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=0
TR turn=1 branch=default fid=34 withhold=0
```
*Turn 1 answer:* Berlin is the capital of Germany.

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=0
TR U what is the capital of germany?
TR OBSERVATION: The question asks for the capital of a country.
TR KNOWLEDGE: I retrieved fact 34: 'Berlin is the capital of Germany.'.
TR INFERENCE: The fact directly names the capital, so I restate it as an answer.
TR CONCLUSION: The capital of Germany is Berlin.
```
*Turn 1 answer:* The capital of Germany is Berlin.

## P18
**Q1:** what did TNN reproduce?

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=0
TR U what did tnn reproduce?
TR OBSERVATION: The question asks what TNN did — a taught action about a taught entity.
TR KNOWLEDGE: I retrieved fact 39: 'TNN reproduced 359 audio clips.'.
TR INFERENCE: The fact directly answers what TNN did.
TR CONCLUSION: TNN reproduced 359 audio clips.
```
*Turn 1 answer:* TNN reproduced 359 audio clips.

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=0
TR turn=1 branch=default fid=39 withhold=0
```
*Turn 1 answer:* TNN reproduced 359 audio clips.

## P19
**Q1:** the louvre is in paris.
**Q2:** the louvre is in rome.

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=0
TR turn=1 branch=assertion subj=louvre rel=6 val=17 conf=0
```
*Turn 1 answer:* NOTED.

*Turn 2 trace:*
```
TR turn=2 ut=0
TR turn=2 branch=assertion subj=louvre rel=6 val=23 conf=1
TR method=47
```
*Turn 2 answer:* But you said louvre is in paris, so which is it?

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=3
TR U the louvre is in paris.
TR OBSERVATION: This is a statement, not a question: the user asserts that louvre is in paris.
TR KNOWLEDGE: I have no noted claim yet about louvre. I record this one.
TR INFERENCE: A new claim with no conflict is simply noted.
TR CONCLUSION: NOTED.
```
*Turn 1 answer:* NOTED.

*Turn 2 trace:*
```
TR turn=2 ut=3
TR U the louvre is in rome.
TR OBSERVATION: This is a statement, not a question: the user asserts that louvre is in rome.
TR KNOWLEDGE: At turn 1 the user stated louvre is in paris and I noted it. Now they say rome. The two claims conflict.
TR INFERENCE: I cannot accept a conflicting claim silently; my teaching says to state both claims and ask which is right.
TR CONCLUSION: But you said louvre is in paris, so which is it?
```
*Turn 2 answer:* But you said louvre is in paris, so which is it?

## P20
**Q1:** who discovered radium?

### Trace A
*Turn 1 trace:*
```
TR turn=1 ut=0
TR U who discovered radium?
TR OBSERVATION: The question asks about 'radium' with a taught predicate.
TR KNOWLEDGE: I retrieved fact 12: 'Marie Curie discovered radium.'.
TR INFERENCE: The fact directly answers the question.
TR CONCLUSION: Marie Curie discovered radium.
```
*Turn 1 answer:* Marie Curie discovered radium.

### Trace B
*Turn 1 trace:*
```
TR turn=1 ut=0
TR turn=1 branch=default fid=12 withhold=0
```
*Turn 1 answer:* Marie Curie discovered radium.

