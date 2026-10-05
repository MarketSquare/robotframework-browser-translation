# Literals stay English in translated documentation

Translated documentation keeps every literal in English: argument names, enum values, code spans, types and example arguments. Only prose, keyword references and example keyword cells are localized. Earlier Finnish translations localized literals, which produced examples such as `Sulje Selain  KAIKKI` that fail at runtime, because Browser and Robot Framework only accept the English values.

## Consequences

- Keyword arguments resolved by English name stay English even in examples, for example the keyword passed to `Promise To`, the run-on-failure keyword and `Set Assertion Formatters` keys.
- A translated documentation suffix must not be glued to a code span (``` ``selector``-valitsimen ```), because Robot Framework leaves such spans unrendered.
- Markers that Robot Framework parses stay English too: the `*DEPRECATED*` prefix and the `*Arguments:*` heading. A translated `*Arguments:*` heading, or a translated argument name inside that section, loses Libdoc's per-argument documentation, and a wrong argument name replaces the whole keyword documentation with an error.
