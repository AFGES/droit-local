# Couverture seconde passe : commerce-professions et droit-social (2026-11-19)

Méthode : justicelibre (get_decision sur JORFTEXT, get_law_article avec view=versions/map, search_legislation). Le moteur est un moteur mots-clés, souvent muet (0 résultat) sur les requêtes longues ; l'absence de résultat ne prouve rien.

Demande utilisateur : « vérifier JORFTEXT000000791289 ». Lu en entier : loi n° 2003-709 du 1er août 2003 (mécénat, associations, fondations). Ses art. 17 à 21 modifient le code civil local (art. 21, 25, 42, 54, 61, 63, 77, 79-I à 79-III ; abrogation de la loi locale du 19 avril 1908, des art. 23, 44, 77 et parties des art. 33, 43, 78). Hors périmètre de ce lot (code civil local) : à reporter dans le yaml du code civil local ; aucun article de la loi de 1889, de 1897, de 1900, de 1914 n'est modifié par cette loi. Son art. 6 (CGI 238 bis) cite les associations de droit local sans modifier de texte local.
(Le point « blasphème / version originale / ne fait pas partie de la traduction officielle » concerne le code pénal local, hors périmètre ; la règle `texte_actuel_officiel` a été appliquée dans tous les yaml écrits ici : false dès que le texte vient d'un acte français post-2013 ou d'une reconstitution.)

## Résultats

| Texte | Statut |
| --- | --- |
| loi du 26 juillet 1900 | 12 entrées de la 1re passe conservées ; 12 ajoutées : art. 103 a, 103 a1, 103 b, 103 c, 103 c1 à c18, 103 d al.1, 103 e 5°, 103 g 5°, 103 i, 103 i1 à i4 (chambres de métiers, décrets 96-643, 99-727, 2004-897, 2007-233, 2008-1275, 2010-651), 133 a, 35 (danse) |
| code des assurances sociales 1911 | 1 entrée a_verifier (première partie, industrie) ; deuxième partie (agricole) maintenue par CRPM L. 761-13, L. 761-19 |
| loi 20 déc. 1911, loi 5 août 1912 | aucune modification trouvée (CSS L. 357-1 à L. 357-21, CRPM D. 761-64 les citent seulement) |
| arrêté 1892, ordonnance 1895 | aucune modification trouvée ; voir réserve ci-dessous |
| loi 1889, loi 1897, loi 1914 | aucune nouvelle modification trouvée (entrée 2019-486 de la 1re passe conservée) |

## Corrections de la première passe

- Ordonnance 2007-329, art. 12 II 4° : la version publiée le 13 mars 2007 visait l'art. « 133 » ; la version en vigueur (LEGI, rectifiée, la première est marquée mort-née) vise « 133 a ». L'art. 133 (titre de maître artisan) n'est pas abrogé : code de l'artisanat L. 221-1, R. 111-2, R. 221-10 le citent. Les 12 entrées de la 1re passe (6, 41 a, 41 b, 105 a à 105 g, 105 i) restent exactes. L'art. 105 h n'est pas dans la liste.
- Art. 103 a à 103 i : la traduction 2013 reproduit le texte de 1900 ; la 1re passe n'avait rien trouvé. Voir entrées.
- Rien supprimé des yaml existants.

## Non vérifié

- Texte actuel des art. 103 c1 à c18 et 103 i1 à i4 (non recopié), état après la loi 2016-298, le décret 2021-168, l'ordonnance 2023-208 et le décret 2023-500 (code de l'artisanat) : renvois au décret 99-433 du 27 mai 1999 (abrogé/modifié) et à la loi 96-603 (abrogée) à mettre à jour.
- Art. 103 à 104 n et 103 e à 103 o autres alinéas : aucune autre modification lue ; la chambre de métiers d'Alsace et la chambre de la Moselle sont associées au réseau (CdA L. 311-2, L. 331-2 ; ordonnance 2015-1540).
- Art. 107 à 112 (livret d'ouvrier), 126 à 139 m (apprentissage) : indices seulement (code du travail 6e partie, livre II, titre VI « dispositions particulières à la Moselle, au Bas-Rhin et au Haut-Rhin », R. 6261-9 à R. 6261-16, L. 6261-1 abrogé en 2019) ; pas de texte abrogeant les articles locaux trouvé.
- Art. 33, 34, 36, 42 a à 56 d (commerce ambulant), 143 à 150 : requêtes sans résultat ; art. 74-75 (loi 1897/1914) seuils en marks (1500, 8000) : aucune conversion trouvée.
- Art. 100 à 100 u : QPC 2012-285 (art. 100 f, 100 s al.3 absents du fichier) ; effet sur le reste du mécanisme corporatif non analysé.
- Code des assurances sociales : texte abrogeant ou remplaçant la 1re partie non trouvé ; art. 1583 (visé par CRPM D. 761-68, hors fichier), art. 612 maintenu par CSS L. 434-19.
- Arrêté 1892 : ses références aux art. 41 a, 105 b, 105 e (abrogés en 2008) ne sont plus à jour ; régime repris à CT L. 3134-x ; pas d'acte modificatif de l'arrêté lui-même.
- Loi 2003-709 art. 17-21 (code civil local) : voir ci-dessus.

## Requêtes principales

get_decision : JORFTEXT000000791289, 000000465978 (ordonnance 2007-329, art. 12), 000000577930, 000000443519, 000000426770, 000019876121, 000053158345, 000000204401 ; get_law_article : CSS L181-1, L141-3 (versions), L242-7-1, L434-19, L482-1, L482-2, D242-29 ; CRPM L761-13 à L761-22 ; ordonnance 2007-329 art. 12 (versions) ; décret 2010-651 art. 28 à 31 ; CT L6261-1, R6261-10, R6261-16 ; search_legislation : « code professionnel local » (105 résultats, 60 lus), « code local des assurances sociales », « code de commerce local », « loi du 26 juillet 1900 », « loi du 1er mai 1889 ».
