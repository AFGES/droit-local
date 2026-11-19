# Couverture passe 2 : code-civil-local-du-18-aout-1896-extraits.md

Sortie : data/modifications/code-civil-local-du-18-aout-1896-extraits.yaml (remplace la passe 1, entrées valides conservées et corrigées ; rien supprimé sauf le placeholder `apres-79-III`, remplacé par 79-IV à 79-XII détaillés).

## Constat majeur sur le md
Le décret 2013-776 (notice) dit retenir la version maintenue par les lois du 1er juin 1924, sans modifications ultérieures. Or le md contient déjà le texte de la loi 2003-709 pour 42, 54, 61 al. 2, 63, 77, 78 (2e phrase absente), 79-I à 79-III, n'a plus 23, 44 ni l'ancien al. 2 de 43. Ces textes ne sont donc pas la traduction 2013 brute (texte_actuel_officiel: false). Annexe du décret (traduction elle-même) non consultable : texte_origine laissé vide pour 23 et 44.
Reste non appliqué dans le md : art. 21 al. 1 (loi 2003 art. 20 I), art. 25 (suppression de 'ayant la capacité de jouissance des droits').

## Loi 2003-709 : relue en entier (get_decision), art. 17 à 21
Entrées pour 21, 23, 25, 33 (a_verifier), 42, 43, 54, 61, 63, 77, 78, 79-I à III, 44. Articulation 2003/2015 : pas de recouvrement (43 : 2003 abroge l'ancien al. 2 politique, 2015 abroge l'al. 1 ; 61 al. 2 et 63 réécrits 2003 puis abrogés 2015).

## Corrections de la passe 1
- Art. 21 : il manquait l'alinéa 'Les associations peuvent se former librement' dans les textes 2019/2021.
- Art. 43 : 2003 avait déjà supprimé un alinéa (md déjà amputé).
- 79-IV : source = loi 2014-856 art. 72 (texte exact). 79-V à 79-XII : textes exacts relus (loi 2021-1109 art. 74).
- Hypothèse écartée : 1127/1128 NE sont PAS abrogés par la loi 2002-306 (art. 71 loi 1924 les maintient).

## Nouveaux textes trouvés (hors loi 2003)
- Loi du 1er juin 1924 art. 8 (fondations : 80, 82, 83, 87 par décret en CE / ministère public) ; art. 71 (1127, 1128 maintenus, étendus aux privilèges) ; art. 74-77 (certificat d'héritier, 2353-2368 ; art. 75 version 2020 par ordonnance 2019-964 art. 35 V : juge du tribunal judiciaire) ; art. 7 (maintien 21-79, 80-88, 565, 570).
- Loi 90-1248 du 29 déc. 1990 art. 1, 2, 4 : tutelle des mineurs locale non maintenue depuis le 3 janv. 1991 ; placements pupillaires (1807, 1808) 'non avenues' ; transitoire pour tutelles anciennes (1806, 1837 à 1886 : lecture par non-maintien, moyenne).
- Loi 2002-306 art. 36-1 loi 1924 : seuls 1105 al. 1, 1107, 1108 maintenus pour les prestations foncières (md conforme).

## Aucune modification trouvée
24, 26 à 32, 34 à 41, 45 à 53, 55 à 60, 64 à 76, 81, 84 à 86, 88, 126, 129 (maintenu par art. 95 loi 1924), 565, 570 (maintenus par art. 7 11° loi 1924), 1105, 1107, 1108, 1839 hors tutelle. Lecture 'tribunal judiciaire' seulement (entrée 'tout').

## Textes lus et écartés
Loi 2024-344 (aucune modif du CCL, seul CGPPP L2125-1-2), ordonnance 2023-393 (ne touche pas 79-IV II ; renvois L236-14/20/21 non actualisés), décrets 2015-832/1017, 2022-619, 2022-1623, 2026-726 (application), loi 2017-86 art. 172 (code pénal local seulement), ordonnance 2015-904 (lue, art. 2 seul concerné).

## Non vérifié
- Art. 33 al. 2 (portée de l'abrogation 'dernier membre de phrase').
- Art. 22 (non au md ; source secondaire dit 'abrogé loi du 11/7/1985').
- Consolidation Légifrance réelle des articles 21-79 (non indexée par justicelibre) : nécessaire pour confirmer les textes reconstitués (25, 21 al. 2).
- QPC / CE / Cass : recherche 'code civil local' association inscrite, aucun résultat de censure ; QPC 2012-285 (traduction) seulement connue par le préambule des décrets.
- Livre foncier (ord. 2024-562) : non relu pour 1127/1128.
- Bail 565/570 et art. 1105-1108 : seuls les textes de maintien lus.
- Renvois internes à la procédure locale (2358, 2361, 60, 73) : art. 80 loi 1924 non appliqué article par article.
Outils : search_legislation (jorf/legi), get_decision, get_law_article (LEGITEXT000006069443 loi 1924 ; 90-1248), WebSearch/WebFetch (PPL Sénat 97-189, PDF IDLAM : sources secondaires, non citées comme officielles).
