*** Settings ***
Library     Browser    language=FI
Library     OperatingSystem
Library     Process
Library     json_lib.py

*** Test Cases ***
Translation Works With Translation
    Uusi Sivu    https://github.com/MarketSquare/

LibDoc Works With Translation
    [Setup]    Remove File    ${CURDIR}/Browser.json
    ${json_kw_speck} =    Join Path    ${CURDIR}    Browser.json
    ${cmd} =    Join Command Line
    ...    python
    ...    -m
    ...    robot.libdoc
    ...    --format=json
    ...    Browser::language=FI
    ...    ${json_kw_speck}
    Run Process    ${cmd}    shell=True
    Compare Translations    ${json_kw_speck}
