---
name: update-translations
description: Update the translation files to a new Browser library release. Use when Browser publishes a release, the drift tests fail, or a translation needs re-syncing with the English docs.
---

Bring every translation file in step with a target Browser release. The vocabulary
(*drift*, *baseline*, *genuine change*, *formatting change*, *checksum-only change*,
*literal*, *language owner*) is defined in `CONTEXT.md`. Use those words in the
conversation, the PR and the commit.

## Steps

1. **Measure.** Install the target release in the dev environment. Then run
   `inv changes --baseline <version>`, where the baseline is the
   `robotframework-browser` floor in `pyproject.toml`.
   - Done when every keyword is classified, and every language reports an empty
     "not at baseline" list.
   - If a language is off baseline, find the release its checksums come from before
     going further.

2. **Read upstream.** Diff the keyword docstrings between the two release tags in the
   Browser repository, and read the release notes.
   - Done when each genuine change carries a reason: a behaviour change, a doc fix,
     or an accidental loss.
   - An accidental loss stays in the translations and goes into the upstream issue.
   - Re-check the known upstream doc bugs listed in the previous PR.

3. **Grill.** Run the `grilling` skill on the drift numbers and the upstream reasons.
   - Confirm the default language policy below.
   - Settle every genuine change whose handling isn't obvious.
   - Record new terms in `CONTEXT.md`, and decisions that meet the ADR bar in
     `docs/adr/`.
   - Done when the user confirms the plan.

4. **Update.** Edit the translation files through `translation_tools.read_entries`
   and `translation_tools.write_entries`. They keep each file's own escaping and key
   order, so the diff shows only real changes.
   - Follow [RULES.md](RULES.md) for every edited entry.
   - Done when every genuine and formatting change is handled for each language,
     according to its policy.

5. **Sync.** Run `inv sync-checksums --keywords <comma list>` for the entries you
   updated. Checksums always come from the generated spec.

6. **Verify.**
   - `inv validate` reports no new errors. Review the `--warnings` output per
     language.
   - `inv utest` passes on the oldest and newest supported Python.
   - `inv atest` passes. It needs `rfbrowser init` first.
   - `inv lint` passes.

7. **Ship.**
   - Raise the `robotframework-browser` floor in `pyproject.toml` to the target.
   - One conventional commit, `feat:` or `fix:` as decided in step 3. Push a branch
     and open a PR.
   - The PR body lists:
     - each language's remaining gaps, per keyword, for the language owners,
     - deliberate deviations from the English,
     - the upstream doc bugs.
   - Draft the upstream issue and let the user file it.

## Default language policy

| Language | Genuine changes | Formatting changes |
| --- | --- | --- |
| fi | translate fully | restructure, keep the wording |
| other languages | markers, literals and structure only; the new prose waits for the language owner | restructure, keep the wording |
