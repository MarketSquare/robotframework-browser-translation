# Browser Translation

Translations of the Browser library's keyword names and documentation, one file per
language, kept in step with each Browser release.

## Language

### Translation content

**Translation file**:
The per-language JSON file holding one translation entry for every Browser keyword.
_Avoid_: language file, locale

**Translation entry**:
One keyword's translated name, translated documentation and checksum within a translation file.
_Avoid_: keyword translation, item

**Intro**:
The library-level documentation entry (`__intro__`), shown before the keywords.
_Avoid_: library doc, introduction

**Import documentation**:
The entry describing the library's import arguments (`__init__`).
_Avoid_: init doc, constructor doc

**Literal**:
Anything a user types into a test: argument names, enum values, code spans, types and example arguments. Literals stay English in every language.
_Avoid_: code, token

**Argument section**:
The `*Arguments:*` list in a keyword's documentation that Libdoc turns into per-argument documentation. Its heading and argument names are literals.
_Avoid_: argument table, parameter list

**Translated keyword name**:
The localized name users call a keyword by. Once released it is frozen, even when imperfect.
_Avoid_: alias, keyword alias

### Keeping in step with Browser

**Checksum**:
The `sha256` value Browser's translation spec assigns to a keyword's English documentation; copied from the spec, never computed.
_Avoid_: hash

**Baseline**:
The Browser release whose English documentation a translation entry was translated from, identified by its checksum.
_Avoid_: source version

**Drift**:
The set of translation entries whose checksum no longer matches the installed Browser release, plus keywords missing or obsolete in a translation file.
_Avoid_: out-of-date, staleness

**Genuine change**:
An English documentation change between the baseline and the target release that alters meaning, so the translation must change wording. A deliberate removal of English text is a genuine change; an accidental one is an upstream documentation bug.
_Avoid_: real change, content change

**Formatting change**:
An English documentation change that alters only structure or markup, such as argument tables becoming argument lists; the translation is restructured, not re-worded.
_Avoid_: cosmetic change, reformat

**Checksum-only change**:
A checksum difference with identical English text; only the checksum is updated.
_Avoid_: hash-only change

**Language owner**:
The native speaker who reviews genuine changes for a language other than Finnish.
_Avoid_: maintainer, translator
