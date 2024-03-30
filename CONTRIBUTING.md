# Improving translations
We welcome improving the translations. Improvements are done
by creating
[pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
in the GitHub. You should not modify the Python code, instead you
should modify/delete/add translations to the
[translation.json](https://github.com/MarketSquare/robotframework-browser-translation-fi/blob/main/robotframework_browser_translation_fi/translation.json)
file.

# Release
Release is created automatically after the PR is merged by using
[Python Semantic Release](https://python-semantic-release.readthedocs.io/en/latest/#)

To release happen automatically, Python Semantic Release must be able to
[parse the commit message](https://python-semantic-release.readthedocs.io/en/latest/commit-parsing.html)

In practise first line should start with words `fix` or `feat`:
```
fix: Fixed to in Close Page keyword
```
or perhaps:
```
feat: Added missing XXX keyword
```
For more details please read the Python Semantic Release
[parse the commit message](https://python-semantic-release.readthedocs.io/en/latest/commit-parsing.html)
documentation.

Lets discuss in the PR if you planning to make braking change, like changing
a keyword name.

# Credits
We use [allcontributors](https://allcontributors.org/docs/en/bot/usage) to add each
contribution to the README. If do not want be added or we forget to add you in the
you in the contributors list, please ping us the PR.