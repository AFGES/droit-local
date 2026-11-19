# Couverture seconde passe : droit-civil (hors CCL), justice, fonctionnaires

Date : 2026-11-19. Outil : justicelibre (JORF, LEGI). Lecture seule sur content/. Premiere passe : `_couverture-droit-civil-hors-ccl-cpc.md`, `_couverture-code-procedure-civile-local.md`, `_couverture-fonctionnaires-justice-urbanisme.md`.

## Verification du lien demande : JORFTEXT000000791289
= Loi n° 2003-709 du 1er aout 2003 relative au mecenat, aux associations et aux fondations (JORF 2 aout 2003). Lue en entier. Les art. 17 a 21 modifient le CODE CIVIL LOCAL (hors perimetre de cette passe, donc pas ecrit dans le YAML du CCL) :
- art. 17 : insere les art. 79-I a 79-III du CCL (radiation des associations par le tribunal d'instance ; 79-II lecture "loi 1901" = aussi associations inscrites ; 79-III droits des ARUP etendus aux associations de droit local reconnues d'utilite publique selon art. 80 LF 1985).
- art. 18 : art. 77 CCL reecrit (mesures d'execution par decret, art. 55 a 79-I).
- art. 19 : art. 61 al. 2 reecrit (opposition de l'autorite administrative) ; art. 63 reecrit (delai de 6 semaines).
- art. 20 : art. 21 CCL (alinea ajoute "Les associations peuvent se former librement."), art. 25 ("ayant la capacite juridique" supprime), art. 42 reecrit (redressement/liquidation judiciaires), art. 54 reecrit (association non inscrite).
- art. 21 : ABROGE la loi locale du 19 avril 1908 sur les associations, l'ordonnance locale du 22 avril 1908, l'art. 23, le dernier membre de phrase du 2e al. de l'art. 33, le 2e al. de l'art. 43, l'art. 44, l'art. 77 et la 2e phrase du 1er al. de l'art. 78 du CCL.
- Effet date : JORF 2 aout 2003, en vigueur le 3 aout 2003 (pas de clause speciale lue).
A ECHEANT, pour le CCL : le YAML existant `code-civil-local-du-18-aout-1896-extraits.yaml` ne contient AUCUNE entree 2003. Corrections probables : (a) art. 43 : le 2e alinea (privation de capacite de l'association fondee sur une concession) est abroge par la loi 2003, donc l'entree "43" de la premiere passe (qui le donne comme texte actuel apres 2015) est suspecte, a reverifier ; (b) art. 61 al. 2 / 62 / 63 : reecrits en 2003 puis modifies en 2015 ; (c) art. 21, 25, 42, 54 modifies 2003 ; (d) art. 77, 23, 44 abroges ou reecrits (conflit interne de la loi : art. 18 reecrit l'art. 77, art. 21 l'abroge : a confirmer sur Legifrance consolide) ; (e) 79-I a 79-III : textes officiels 2003 (non de la traduction 2013). Pas de lien direct avec les textes du perimetre sauf 17 avril 1899 art. 7 a (voir ci-dessous) et loi 1896 art. 85 (art. 45 al. 3 CCL non touche : rien a signaler).

## Textes modifies (YAML ecrits)
| Texte | Entrees | Source lue |
| --- | --- | --- |
| loi du 7 juillet 1897 (sections de communes) | art. 7 al. 1 et 4 abroges 1996-02-24 ; art. 11 al. 2 2e phrase abroge (a_verifier) ; "tout" (art. 1, 5, 6, 8 abroges, absents du md) | loi 96-142 art. 12 23° (JORFTEXT000000559120), CGCT L. 5222-1 |
| loi du 15 novembre 1909 (veuves et orphelins fonctionnaires) | art. 12 1° et 3° abroges 1966 ; art. 9 3° abroge (deja absent du md) ; "tout" a_verifier | decret 66-807 du 28 octobre 1966 art. 1-2 |
| loi du 15 juin 1895 (navigation) | "tout" codifie (champ limite Rhin/Moselle transfrontiere) ; art. 102 deroge | ordonnance 2010-1307, CTransp L. 4471-1, L. 4122-23, -25, -26 |
| loi du 4 decembre 1899 (honoraires notaires) | art. 3, 4 : TGI -> tribunal judiciaire 2020-01-01 (moyenne) | loi 2019-222 art. 95 |
| loi du 17 avril 1899 (application CCL) | art. 7 b al. 2 : tribunal d'instance -> tribunal judiciaire (moyenne) | loi 2019-222 art. 95 |

## Textes sans entree (aucune modification textuelle trouvee, confiance faible a moyenne)
- Code local de procedure civile 1877 : voir ci-dessous.
- Lois frais de justice 1878 et 1899 : aucun modificatif trouve apres 2013. Decret 2005-1669 lu : pas modificatif (transfert comptable). Mentions "tribunal de l'instance", "tribunal regional" : lecture par transfert (loi 2019-222), non reportees faute de texte litteral.
- Loi du 11 decembre 1899 (federation des associations) : aucune modification trouvee.
- Loi du 16 mai 1894 (ventes a temperament) : aucune modification trouvee. Renvoi art. 2 al. 2 a l'art. 260 al. 1 CPC local : non verifie.
- Loi du 18 aout 1896 (introduction CCL, art. 85-87) : aucune modification trouvee ; la loi 2003-709 ne touche pas l'art. 45 CCL (renvoi de l'art. 85 intact). Art. 86 (approbation de l'Etat > 5000 marks) : non recoupe avec ordonnance 2005-856 ni loi 2021-1109 (non lus).
- Loi du 31 mars 1873 (fonctionnaires d'Empire) : rien de nouveau ; pistes non lues : code des pensions civiles et militaires, CGFP (ord. 2021-1574), decret 2003-1306.
- Loi du 10 juin 1872, loi du 30 juin 1878 (temoins/experts), ordonnance du 13 juin 1903 : aucune modification. A noter : loi 1878 art. 3, 7, 8 comportent des montants "[evalues chaque annee]" (placeholders de la traduction) ; aucun arrete de fixation trouve. Decret 2005-1470 lu : cite l'art. 4 de la loi 1878 (art. 153-1 du decret 91-1266), ne la modifie pas ; decret 2020-1717 : meme type de renvoi (non relu en entier).

## Code local de procedure civile (pas de YAML ecrit)
- Loi 91-650 art. 94 4° (en vigueur 1993-01-01, elle-meme abrogee 2012-06-01) : abroge du livre VIII la section 1 sauf art. 794 (2 a et 5), 795 a, 797 (al. 2 et 3), 799, 800 ; section 2 sauf titre II ; sections 3, 4, 5. Donc seuls les al. 2 et 3 de l'art. 797 subsistent : le md de l'art. 797 reproduit trois paragraphes dont le premier ("expedition executoire ... notaire") ; correspondance avec les alineas d'origine non verifiee (a_verifier, pas d'entree YAML).
- Ordonnance 2011-1895 art. 4 4° (partie legislative du code des procedures civiles d'execution, en vigueur 2012-06-01) : abroge les art. 794 et 795 a du CPC local. L'art. 799 du md renvoie encore a "l'article 794 n° 5" : renvoi sur un article abroge (point a signaler, pas d'entree YAML car le texte de 799 n'est pas modifie litteralement).
- Loi 2010-1609 art. 800 abroge (pre-2013). Art. 864-870 (titre II, execution sur immeubles) maintenus par la loi 91-650 ; effet de l'ordonnance 2006-461 (saisie immobiliere), abrogee 2012, et du CPCE sur 864-870 : non verifie.
- Art. 1025-1026 (arbitrage) : decret 2011-48 (rapport) indique l'application du droit commun sous reserve de ces articles : maintenus.
- Art. 91, 98, 103-107 (avocat-avoue, depens) : effet de la loi 2011-94 (avoues) non etabli.

## Requetes principales (jorf/legi, sans date_min)
Titres exacts entre guillemets et dates ("7 juillet 1897", "15 juin 1895", "15 novembre 1909", "31 mars 1873", "30 juin 1878", "4 decembre 1899", "18 aout 1896"), "code de procedure civile local", "code local de procedure civile", "loi d'Empire sur les frais de justice", "sections de commune", "modernisant le regime des sections de commune" (loi 2013-428 : aucun lien Alsace-Moselle trouve, a_verifier), "fonctionnaires cadre local", CGCT L. 5222-1 et L. 2542-1. get_decision : JORFTEXT000000791289, 000000559120, 000025009816, 000000269080, 000000785879. get_law_article : loi 91-650 art. 94, loi 2019-222 art. 95, decret 66-807, CTransp L. 4471-1/4122-23/-25/-26.

## Non verifie
QPC / CE / Cass sur ces textes (non faits), annexe du code de procedure civile (decrets 2018-318, 2023-105, 2013-692), ordonnance 2024-562 (deja ecartee en passe 1), decret 2016-230 (tarifs notaires), CGFP, code des pensions (loi 1873/1909 au dela du decret 66-807), art. 260 CPC local (renvoi 1894), "tribunal regional/bailliage" generalise par loi 2019-222 (non transcrit dans le CPC), loi 2013-428 et CGCT pour les sections (L. 2411-1 s.).
