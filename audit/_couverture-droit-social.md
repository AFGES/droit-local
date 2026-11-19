# Couverture audit droit-social (au 2026-11-19)

Resultat : AUCUNE modification verifiee du texte des 5 textes. Aucun fichier YAML cree (regle : pas d'entree sans source lue).
Limite : la base justicelibre n'indexe pas les textes locaux ; la recherche JORF plein texte est bruitee. Audit a considerer comme PARTIEL, a completer (Legifrance, Droit local Alsace-Moselle IDL, doctrine).

## Textes
| Fichier | Statut | Remarque |
| --- | --- | --- |
| arrete-du-1-mai-1892-concernant-le-repos-dominical-dans-les-professions.md | aucune modification trouvee | CT L3134-1 s. (codification 2007, anterieure a 2013) renvoie a la loi locale; aucun acte modificatif 2013-2026 trouve |
| code-des-assurances-sociales-du-19-juillet-1911.md | aucune modification trouvee | texte pas amende par un acte lu. Nombreux renvois dans CSS, CRPM (L761-11 s., L761-23 modifie par loi 2025-199 art. 87), loi 2014-1170, LFSS 2020 (JORFTEXT000039675317), decret 2015-227 : ce sont des textes qui CITENT le code local, pas qui le modifient. Decret 2025-1283 du 22 dec. 2025 (JORFTEXT000053158345) : modifie uniquement la partie reglementaire du CRPM (D751-D761), pas le RVO. |
| loi-du-20-decembre-1911-sur-l-assurance-des-employes.md | aucune modification trouvee | encore visee par CSS L215-5, L357-1 s. (lecture d'extraits seulement) |
| loi-du-5-aout-1912-d-execution-du-code-des-assurances-sociales.md | aucune modification trouvee | visee par CRPM D761-64 (2005) |
| ordonnance-du-5-fevrier-1895-relative-aux-exceptions-a-l-interdiction-du.md | aucune modification trouvee | seule trace : decret 2013-776 (art. 1) qui la liste |

## Requetes principales tentees
- search_legislation jorf date_min 2013-09-01 : "code des assurances sociales du 19 juillet 1911", "repos dominical Alsace Moselle arrete 1er mai 1892", "loi du 20 decembre 1911 assurance des employes"
- search_legislation legi : "19 juillet 1911" assurances sociales (58 resultats, tous renvois), "20 decembre 1911", "5 fevrier 1895 travail dominical industrie"
- get_law_article CT L3134-2 view=map ; CRPM L761-23
- search_case_law CONSTIT et search jade/dila : QPC assurances sociales 1911, repos dominical Alsace-Moselle : 0 resultat pertinent
- recherche "code local des assurances sociales" + "est abrogé/modifié" : bruit

## Pistes non verifiees (a_verifier)
- Eventuelles modifications du livre III RVO par ordonnances/lois non retrouvees ; verifier Legifrance / base "droit local" (Institut du droit local alsacien-mosellan).
- Arretes prefectoraux / decrets sur derogations repos dominical (hors perimetre textes).
