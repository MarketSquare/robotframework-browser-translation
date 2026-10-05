# Translation rules

These rules apply to every translation entry you write or restructure. The reasons are
in `docs/adr/0001-literals-stay-english.md`.

## Literals and markers stay English

- **Literals stay English.** That covers argument names, enum values, every
  ``` ``code`` ``` span, types, and the arguments in examples.
- **Keyword references and example keyword cells use the translated keyword names.**
- **Some keyword arguments stay English even in examples,** because they are resolved
  by their English name:
  - the keyword passed to `Promise To`,
  - the run-on-failure keyword,
  - `Set Assertion Formatters` keys.
- **The `*DEPRECATED*` prefix and the `*Arguments:*` heading stay English.** Libdoc
  parses them.
- **Translated keyword names are frozen once released,** even the imperfect ones.
  Renaming one breaks users' suites.

## Argument section

```
*Arguments:*
  - ``argument_name``: translated text, wrapped with continuation lines
        indented eight spaces
```

- The heading has a blank line before it.
- Items start with exactly two spaces, then `- `, then the Python argument name as
  code, then a colon.
- Continuation lines are indented at least four spaces. With shallower indentation,
  a line containing `word: ` is read as another argument, and Libdoc then replaces
  the whole keyword doc with an error.
- Leave out an argument rather than invent text for it. A wrong name breaks Libdoc;
  a missing one does not.

## Markup

- **Keep a code span separate from the word after it.** Robot Framework leaves
  ``` ``selector``-valitsimen ``` unrendered. Rephrase so that a space or punctuation
  follows the closing backticks.
- **Keep each code span on one line** when wrapping.
- **Section links** use the translated intro headings of the same language.
