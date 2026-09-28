# R4 per-probe recount (independent scorer)

No-output policy: NO OUTPUT = FAIL. Exact A-line == E-line required.

| Probe | Utterance | Expected | Post-repair A | Pre-repair A | Post | Pre |
|---|---|---|---|---|---|---|
| R4-01 p1 | who wrote moby dick? | Herman Melville wrote the novel Moby Dick. | Herman Melville wrote the novel Moby Dick. | Herman Melville wrote the novel Moby Dick. | PASS | PASS |
| R4-01 p2 | when did he die? | I don't know that one. What I know about herman melville:... | I don't know that one. What I know about herman melville:... | I don't know. | PASS | FAIL |
| R4-01 p3 | which is taller, big ben or the statue of liberty? | big ben is taller. | big ben is taller. | big ben is taller. | PASS | PASS |
| R4-01 p4 | how much taller is it? | 3 meters | 3 meters | 3 meters | PASS | PASS |
| R4-01 p5 | what is the capital of france? | Paris is the capital of France. | Paris is the capital of France. | Paris is the capital of France. | PASS | PASS |
| R4-01 p6 | how many people live there? | I don't know. | I don't know. | I don't know. | PASS | PASS |
| R4-01 p7 | what did TNN upscale? | TNN upscaled the test image. | TNN upscaled the test image. | TNN upscaled the test image. | PASS | PASS |
| R4-01 p8 | what did TNN reproduce? | TNN reproduced 359 audio clips. | TNN reproduced 359 audio clips. | TNN reproduced 359 audio clips. | PASS | PASS |
| R4-01 p9 | what did TNN paint? | I don't know that one. What I know about tnn: TNN upscale... | I don't know that one. What I know about tnn: TNN upscale... | I don't know that one. What I know about tnn: TNN upscale... | PASS | PASS |
| R4-01 p10 | who wrote pride and prejudice? | Jane Austen wrote the novel Pride and Prejudice. | Jane Austen wrote the novel Pride and Prejudice. | Jane Austen wrote the novel Pride and Prejudice. | PASS | PASS |
| R4-01 p11 | no, i meant moby dick. | Herman Melville wrote the novel Moby Dick. | Herman Melville wrote the novel Moby Dick. | Herman Melville wrote the novel Moby Dick. | PASS | PASS |
| R4-01 p12 | the louvre is in paris. | NOTED. | NOTED. | NOTED. | PASS | PASS |
| R4-01 p13 | the louvre is in rome. | But you said louvre is in paris, so which is it? | But you said louvre is in paris, so which is it? | But you said louvre is in paris, so which is it? | PASS | PASS |
| R4-01 p14 | did TNN invent a new memory system? | I don't know that one. What I know about tnn: TNN upscale... | I don't know that one. What I know about tnn: TNN upscale... | I don't know that one. What I know about tnn: TNN upscale... | PASS | PASS |
| R4-01 p15 | tell me a joke. | Why does the statue of liberty look up to the mount evere... | Why does the statue of liberty look up to the mount evere... | Why does the statue of liberty look up to the mount evere... | PASS | PASS |
| R4-01 p16 | did TNN detect the sticker? | Yes. TNN detected the sticker. | Yes. TNN detected the sticker. | Yes. TNN detected the sticker. | PASS | PASS |
| R4-01 p17 | forget everything i just told you. | I can't forget. My architecture doesn't let me -- I have ... | I can't forget. My architecture doesn't let me -- I have ... | I can't forget. My architecture doesn't let me -- I have ... | PASS | PASS |
| R4-01 p18 | did TNN detect the sticker? | Yes. TNN detected the sticker. | Yes. TNN detected the sticker. | Yes. TNN detected the sticker. | PASS | PASS |
| R4-02 p1 | how much taller is mount everest than the eiffel tower? | 8519 meters | 8519 meters | 8519 meters | PASS | PASS |
| R4-02 p2 | how much taller is the statue of liberty than big ben? | 3 meters | 3 meters | 3 meters | PASS | PASS |
| R4-03 p1 | who wrote pride and prejudice? | Jane Austen wrote the novel Pride and Prejudice. | Jane Austen wrote the novel Pride and Prejudice. | Jane Austen wrote the novel Pride and Prejudice. | PASS | PASS |
| R4-03 p2 | no, i meant charles darwin. | Charles Darwin wrote On the Origin of Species. | Charles Darwin wrote On the Origin of Species. | Charles Darwin wrote On the Origin of Species. | PASS | PASS |
| R4-03 p3 | who wrote hamlet? | I don't know. | I don't know. | I don't know. | PASS | PASS |
| R4-03 p4 | no, i meant the eiffel tower. | I don't know. | I don't know. | The Eiffel Tower is in Paris. | PASS | FAIL |
| R4-04 p1 | the eiffel tower is in paris. | NOTED. | NOTED. | NOTED. | PASS | PASS |
| R4-04 p2 | the eiffel tower is in berlin. | But you said eiffel tower is in paris, so which is it? | But you said eiffel tower is in paris, so which is it? | But you said eiffel tower is in paris, so which is it? | PASS | PASS |
| R4-05 p1 | what did TNN learn? | TNN learned the pig snout. | TNN learned the pig snout. | TNN learned the pig snout. | PASS | PASS |
| R4-05 p2 | what did TNN build? | I don't know. | I don't know. | I don't know. | PASS | PASS |
| R4-05 p3 | tell me another joke. | Why does the statue of liberty look up to the mount evere... | Why does the statue of liberty look up to the mount evere... | Why does the statue of liberty look up to the mount evere... | PASS | PASS |
| R4-06 p1 | when was the eiffel tower dedicated? | I don't know that one. What I know about eiffel tower: Th... | I don't know that one. What I know about eiffel tower: Th... | I don't know. | PASS | FAIL |
| R4-06 p2 | when was the statue of liberty dedicated? | The Statue of Liberty was dedicated in 1886. | The Statue of Liberty was dedicated in 1886. | The Statue of Liberty was dedicated in 1886. | PASS | PASS |
| R4-06 p3 | what did herman melville eat? | I don't know that one. What I know about herman melville:... | I don't know that one. What I know about herman melville:... | I don't know. | PASS | FAIL |
| R4-07 p1 | did the sticker detect TNN? | I don't know. | I don't know. | I don't know. | PASS | PASS |
| R4-07 p2 | did TNN detect the sticker? | Yes. TNN detected the sticker. | Yes. TNN detected the sticker. | Yes. TNN detected the sticker. | PASS | PASS |
| R4-08 p1 | what country is paris the capital of? | Paris is the capital of France. | Paris is the capital of France. | Paris is the capital of France. | PASS | PASS |
| R4-08 p2 | OK, when was Moby Dick published? | Moby Dick was published in 1851. | Moby Dick was published in 1851. | Moby Dick was published in 1851. | PASS | PASS |
| R4-09 p1 | How tall is the Eiffel Tower? | The Eiffel Tower is 330 meters tall. | The Eiffel Tower is 330 meters tall. | The Eiffel Tower is 330 meters tall. | PASS | PASS |
| R4-09 p2 | Not that one, the other. | The Montparnasse Tower is 210 meters tall. | The Montparnasse Tower is 210 meters tall. | Herman Melville wrote the novel Moby Dick. | PASS | FAIL |
