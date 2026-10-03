# WITHHELD-NOT-FOR-REVIEW

Audio excerpts in this directory are tournament working material for
analyzer-level verification ONLY. They are never sent to Micah and never
presented as listening demos. (Excerpt policy: `../PREREG_PAR_DIVE.md`.)

| File | SHA-256 | Content |
|---|---|---|
| d1_boundary_fade.wav | 2ea2a5c80e623c7fd553c39980ab53b4361d36385865d74e30b60a8cf50eb814 | D1, `plans/plan_excerpt_d1.txt`, 15 s render window: musical phrase hard-cut at the window edge with D1's 5 ms backward raised-cosine release. Ends at 0.0000 FS. Analyzer: `results/d1_edgeAB.txt` (E1–E4). |
| d1_boundary_nofade.wav | 0e75a9e51a67f310531fcf7b78b7a4aa5eaf0feb484fbe9d29a127972d326b07 | Same phrase, pass 3 disabled (PAR semantics): ends mid-waveform at 0.3142 FS — the stop transient D1 removes. A/B control. |
| d2_planref.wav | cdd77569de961d11a1382f911ce8020269d1cd672a4456aa0f48d87b7db3ff9d | D2, `plans/plan_excerpt_d2.txt` (4 s): 440 Hz cue at 0.5–1.5 s, then the response at 2.0–3.0 s rendered at exact construction-440 (`LATCHED f0q=28835840`) although the plan's nominal declares 460. ZCR: cue 456.3 Hz (+63c disclosed bias), response 425.0 Hz (−60c disclosed bias) — the instrument brackets the 440 construction; the pitch claim is the latch, not the meter. |

All three rendered 2026-09-24 with the pinned toolchain
(`toolchain/bin/znc_linux_x86_64_abed8aa1`) from sources whose SHAs
match the frozen dive pins (D1 `d6bcb99c…cff88`, D2 `5199cd1d…bebbdd`).
