# Prompt v1 contre prompt v2 — stabilité, coût, écarts restants

Test du 2026-10-30 sur 4 collectivités dont les fiches n'ont souvent qu'un titre : Paris Est Marne & Bois (5390, 96 % sans description), CC Brionnais Sud Bourgogne (5033, 86 %), CC Sundgau (4973, 70 %), CC Ardennes Thiérache (3914, 64 %). 393 fiches, 3 runs pour chaque prompt, `mistral-large-4`, raisonnement « low ».

- **v1** : prompt de `pages/26_run_impact.py`, lots de 25 fiches.
- **v2** : `prompts/classification_volet_ges_v2.md`, une fiche par appel, contexte plan > axe > sous-axe, codes de leviers et JSON contraint, règles arbitrées et exemples.

## Résultat

**Le prompt v2 rend 82 % des fiches stables sur 3 runs, contre 60 % avec la v1.** Parmi les fiches classées au moins une fois, la part stable passe de 40 % à 70 %.

| Indicateur (393 fiches) | v1 | v2 |
|---|---:|---:|
| Fiches identiques sur les 3 runs | 237 (60 %) | **323 (82 %)** |
| Fiches classées au moins une fois | 259 | 235 |
| … dont identiques sur les 3 runs | 103 (40 %) | **165 (70 %)** |
| « Tout ou rien » (classée dans un run, vide dans un autre) | 61 | **17** |
| Catégorie 4 « Gouvernance » qui apparaît ou disparaît | 23 | **6** |
| Réponses invalides rejouées | 0 | 0 (impossible avec le schéma JSON) |
| Vote majoritaire = prod (fiches classées d'un côté ou de l'autre) | 51 / 237 (22 %) | 55 / 230 (24 %) |

| Collectivité | Stables v1 | Stables v2 |
|---|---:|---:|
| Paris Est Marne & Bois (5390) | 60 % | 85 % |
| CC Brionnais Sud Bourgogne (5033) | 67 % | 86 % |
| CC Sundgau (4973) | 59 % | 78 % |
| CC Ardennes Thiérache (3914) | 54 % | 76 % |

**La classification elle-même change beaucoup.** Le vote majoritaire v2 est identique au vote v1 sur seulement 218 fiches (55 %). C'est l'effet attendu des nouvelles règles (marche, études, sujets hors leviers, rénovation…).

**L'accord avec la prod ne bouge pas (24 %).** C'est normal : la prod a été classée avec l'ancien prompt et un autre modèle. Ce chiffre ne dit pas qui a raison. Il faudra le jeu de référence (R3) pour mesurer la justesse.

## Cache et coût

**Le cache fonctionne : 96 % des tokens d'entrée sont lus en cache.** Le prompt système (environ 5 000 tokens) est envoyé en premier et ne change pas d'un appel à l'autre. Seule la fiche, à la fin, change.

| Coût (3 runs, 393 fiches) | v1 | v2 |
|---|---:|---:|
| Appels | 54 | 1 178 |
| Tokens d'entrée | 127 659 | 5 969 384 |
| … dont en cache | 0 | 5 735 168 (96 %) |
| Tokens de sortie (raisonnement compris) | 330 537 | 1 931 733 |
| Coût estimé | 0,78 $ | 4,60 $ |
| Coût par fiche et par run | 0,07 centime | 0,39 centime |
| Extrapolé à 1 674 fiches, 1 run | ≈ 1,1 $ | ≈ 6,5 $ |

- Sans le cache, la v2 aurait coûté environ 8,10 $ au lieu de 4,60 $. Le cache divise le coût d'entrée par 7.
- **88 % du coût v2 vient maintenant de la sortie** : le raisonnement « low » produit en moyenne 1 600 tokens par fiche, même pour une fiche simple. Pour baisser encore le coût, il faudrait réduire le raisonnement, ce que `mistral-large-4` ne permet pas (« none » refusé).
- Durée : environ 29 minutes pour 1 179 appels, avec 10 appels en parallèle.

Tarifs utilisés (grille de `utils/test_run_impact.py`) : entrée 0,68 $, entrée en cache 0,07 $, sortie 2,09 $ par million de tokens.

## Écarts restants (70 fiches instables)

Le détail fiche par fiche est dans `rapport.md`, les statistiques dans `motifs_ecarts.md`.

1. **Catégories seules (31 fiches, 44 % des écarts).** Le verbe « soutenir » hésite entre 3 et 6 quand la fiche ne dit pas s'il y a de l'argent : 3914/76387 « soutenir les démarches vers l'agroécologie » donne [3, 6] / [6] / [6]. « Inciter les communes à réaliser un diagnostic » hésite entre 2 et 6 (5033/57562). Une réunion d'acteurs hésite entre 4 et 6 (5033/57603).
   → Règle à ajouter : « soutenir », « aider » ou « encourager » sans mention d'argent versé = 6.
2. **Rénovation globale des bâtiments tertiaires : 2 ou 3 leviers.** 5390/85726 et 3914/76560 perdent la sobriété tertiaire dans 1 run sur 3. **C'est une ambiguïté du prompt v2** : la définition des leviers chaudières tertiaires inclut la rénovation globale, et celle de la sobriété tertiaire dit « les trois leviers ».
   → À corriger : écrire une seule règle claire (« réhabilitation ou rénovation globale d'un bâtiment tertiaire = les trois leviers tertiaires »).
3. **Tout ou rien résiduel (17 fiches).** Ce sont surtout des sujets hors leviers qu'un run classe quand même : Trame verte et bleue (3914/76377, 3 leviers dans 1 run), maison de santé (3914/76490), union commerciale (3914/76547), conserverie (5033/57638), animations sur l'alimentation (4973/42049).
   → Ajouter « trame verte et bleue », « santé », « commerce » et « alimentation » de façon plus visible dans la liste des fiches sans levier, ou donner 2 exemples de plus.
4. **Leviers ajoutés malgré une règle d'exclusion.** « Bus et cars décarbonés » s'ajoute au transport à la demande (3914/76374), alors que la règle L9 l'exclut. « Voiture électrique » s'ajoute à la lutte contre l'autosolisme (3914/76373) sans mention de l'électrique.
   → Ajouter un exemple « transport à la demande » au prompt.
5. **Fiches multi-sujets restantes.** La mobilité des agents (4973/42050) et la filière hydrogène / bioGNV (3914/76370) donnent encore 3 leviers différents selon le run. Avec le plafond de 3 leviers, le choix des 3 varie.

## Prochaines étapes proposées

1. Corriger les points 1, 2 et 4 dans `prompts/classification_volet_ges_v2.md` (règle « soutenir », règle tertiaire unique, exemple transport à la demande), puis relancer les mêmes 4 collectivités.
2. Constituer le jeu de référence (R3) pour mesurer la justesse, pas seulement la stabilité.
3. Porter le prompt v2 dans `pages/26_run_impact.py`. Ce n'est pas encore fait : la page de prod utilise toujours l'ancien prompt et l'ancien format de sortie.
