# Finnish tranlsation for Robot Framework Browser library
[![Version](https://img.shields.io/pypi/v/robotframework-browser-translation-fi.svg)](https://pypi.python.org/pypi/robotframework-browser-translation-fi)
![CI](https://github.com/MarketSquare/robotframework-browser-translation-fi/actions/workflows/on-push.yml/badge.svg)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![All Contributors](https://img.shields.io/github/all-contributors/MarketSquare/robotframework-browser-translation-fi?color=ee8449&style=flat-square)](#contributors)


This project contains a Finnish transation for the Robot Framework
[Browser](https://github.com/MarketSquare/robotframework-browser)
libary.

This project uses Browser library
[Python plugin API](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/)
to provide
[translation.json](https://github.com/MarketSquare/robotframework-browser-translation-fi/blob/main/robotframework_browser_translation_fi/translation.json)
file for the Browser library. Browser library searches Python plugins by using
naming convention: `robotframework_browser_translation`. This module
fulfils the Browser library translation API and provides `get_language`
metghod. The method return a dictionry:

```Python
{"language": "fi", "path": "/opath/to/translation.json")}
```
Which Browser library will use to match correct translation from all
the found Python plugins. Languea search is enabled when Browser
library is imported with:

```robotRobotFramework
*** Settings ***
Library    Browser    languege=fi
```

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/aaltat"><img src="https://avatars.githubusercontent.com/u/2665023?v=4?s=100" width="100px;" alt="Tatu Aalto"/><br /><sub><b>Tatu Aalto</b></sub></a><br /><a href="#code-aaltat" title="Code">💻</a> <a href="#doc-aaltat" title="Documentation">📖</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
