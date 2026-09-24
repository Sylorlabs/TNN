# Corpus sources & consultation manifest (T1 teaching)

Frozen: 2026-09-24. The eight teaching excerpts in `corpus/units/` are
teaching-only distillations from the public references below. Each was
consulted exactly once during the real teaching phase (see
`runlog/teach/consult.log`); byte counts and deterministic FNV digests
were logged per unit. Teaching excerpts are NOT installed handbook prose —
they are short paraphrases of syntax patterns, from which the procedural
schemas in `cards/U*.card` were then derived.

| Unit | File | Bytes | FNV digest | Public source |
|------|------|-------|-----------|----------------|
| U1-types | U1-types.txt | 1351 | a226fa91f5a850e3 | TypeScript Handbook — Everyday Types: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html |
| U2-functions | U2-functions.txt | 1486 | d735d8dbc5271db8 | TypeScript Handbook — More on Functions: https://www.typescriptlang.org/docs/handbook/2/functions.html |
| U3-interfaces | U3-interfaces.txt | 1522 | 9cf8eafa536c4ee5 | TypeScript Handbook — Object Types: https://www.typescriptlang.org/docs/handbook/2/objects.html |
| U4-classes | U4-classes.txt | 2020 | a9de9e75800b7c94 | TypeScript Handbook — Classes: https://www.typescriptlang.org/docs/handbook/2/classes.html |
| U5-generics | U5-generics.txt | 1910 | 93da99bed526788c | TypeScript Handbook — Generics: https://www.typescriptlang.org/docs/handbook/2/generics.html |
| U6-dom | U6-dom.txt | 1892 | 81c8b22e90fdd510 | TypeScript Handbook — DOM Manipulation: https://www.typescriptlang.org/docs/handbook/dom-manipulation.html |
| U7-async | U7-async.txt | 1677 | 2cd72d482dca610e | MDN Web Docs — async function (JavaScript Reference › Statements) |
| U8-modules | U8-modules.txt | 1640 | 2c009dc3442281ea | TypeScript Handbook — Modules: https://www.typescriptlang.org/docs/handbook/2/modules.html |

(Note: U8's digest is `2c009dc3442281ea` per `runlog/teach/consult.log`.)

## Teaching-only rules (frozen with the battery)

1. Exactly one consultation per unit during teaching, logged with byte
   count and FNV digest.
2. B1 testing is manual-free: no corpus, cards, or handbook consulted
   during the battery — only the installed cards (learned state).
3. Production/manual consultations after B1 are logged separately
   (see runlog/prod/).
4. The corpus files are reference material for the teacher, never
   installed into the learner. Installed knowledge = `cards/*.card` only.
