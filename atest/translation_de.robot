*** Settings ***
Library     Browser    language=DE
Library     OperatingSystem
Library     Process
Library     translation_compare_lib.py

*** Test Cases ***
Translation Works With Translation DE
    Erstelle Seite    https://github.com/MarketSquare/

LibDoc Works With Translation DE
    [Setup]    Remove File    ${CURDIR}/Browser_de.json
    ${json_kw_spec} =    Join Path    ${CURDIR}    Browser_de.json
    ${cmd} =    Join Command Line
    ...    python
    ...    -m
    ...    robot.libdoc
    ...    --format=json
    ...    Browser::language=DE
    ...    ${json_kw_spec}
    Run Process    ${cmd}    shell=True
    Compare Translations    ${json_kw_spec}    de
