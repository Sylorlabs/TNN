# Audio Principles Investigation — "can TNN reason over audio?"

**Ordered by Micah, 2026-09-25 ~16:26 PDT.** Head-to-head (Round 3B) is done;
now rethink from principles. This is the hardest issue.

**Micah's hypothesis:** audio is a shitty open-loop generator with no control
over its output — CONDITIONAL on TNN not being conscious about audio. If TNN
can reason over audio, the hypothesis falls.

**Structure (HTD):**
1. Design crew: operational definitions + frozen mini-preregs with kill bars.
2. Test crews P (perception), C (control), L (closed loop) run against frozen preregs.
3. Synthesis: verdict per hypothesis, kill table, architectural requirements.

**Does NOT decide** the four pending Round-3B structural calls (G4c source-relative
reading, gate re-anchor, B-F2 re-test, B-F1 redesign) — reports how findings
inform each.

**Standing rules:** pure Zag, zero RNG in any decision path, byte-identical
reruns, analyzer-first (no ear claims without waveform analysis), real
mechanisms not stubs, no arbitrary hard limits. Commits to `tnn-native-lab`
via ~/workspace/tmp_commit/explicit_commit.py, NEVER main.
