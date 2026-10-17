*** Settings ***
Library    Browser    language=FR
Library    OperatingSystem
Library    Process
Library    translation_compare_lib.py

*** Test Cases ***
Translation Works With Translation FR
    Ouvrir Une Nouvelle Page    data:text/html,<h1>Bonjour</h1><input id="nom">
    Remplir Le Texte    \#nom    Français
    Obtenir La Propriété    \#nom    value    ==    Français
    Obtenir Le Texte    h1    ==    Bonjour
    [Teardown]    Fermer Le Navigateur    ALL

LibDoc Works With Translation FR
    [Setup]    Remove File    ${CURDIR}/Browser_fr.json
    ${json_kw_spec} =    Join Path    ${CURDIR}    Browser_fr.json
    ${cmd} =    Join Command Line
    ...    python
    ...    -m
    ...    robot.libdoc
    ...    --format=json
    ...    Browser::language=FR
    ...    ${json_kw_spec}
    ${result} =    Run Process    ${cmd}    shell=True
    Should Be Equal As Integers    ${result.rc}    0    ${result.stderr}
    Compare Translations    ${json_kw_spec}    fr
