# V92 V4 patch notes

V92 execution exposed one defect in `r27_native_state_sections_v4.zag` before qualification could proceed.

The section encoder and decoder round-tripped valid scalar payloads, but `r27s4_validate_scalar_section` rejected them. The failure localized to `r27s4_count_valid`, whose range branches returned compound boolean expressions cast directly to `i32`. Under the local Zag compiler used by this lane, those return paths did not produce the required `1` for valid scalar values.

The V4 patch replaces those boolean casts with explicit `return 1` / `return 0` branches for PAM count, acoustic motif count, name count, trace count, development step, and newborn restarts. No section IDs, section sizes, accepted R27 values, image ordering, pending-credit fields, canonical R27 bytes, or learner authority were changed.
