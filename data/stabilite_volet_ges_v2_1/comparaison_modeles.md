# Comparaison des modèles — classification volet GES, prompt v2

Test du 2026-11-02 sur les 4 mêmes collectivités que le test v1/v2 : Paris Est Marne & Bois (5390), CC Brionnais Sud Bourgogne (5033), CC Sundgau (4973), CC Ardennes Thiérache (3914). 393 fiches, une fiche par appel, 3 runs par modèle. Lecture seule sur la prod.

## Résultat

**Claude Haiku 5.5 est le plus stable (93 % des fiches identiques sur 3 runs) et le moins cher (environ 0,26 $ pour classer les 1 674 fiches une fois).** Mistral Small 2603 est presque aussi stable que Large 4, mais il laisse plus de fiches sans levier.

| | v1 · Large 4 (lots de 25) | v2.0 · Large 4 | v2.1 · Small 2603 | v2.1 · Haiku 5.5 |
|---|---:|---:|---:|---:|
| Fiches identiques sur les 3 runs | 60 % | 82 % | 84 % | **93 %** |
| … parmi les fiches classées | 40 % | 70 % | 70 % | **88 %** |
| Fiches classées au moins une fois | 259 | 235 | 206 | 221 |
| « Tout ou rien » | 61 | 17 | 29 | **10** |
| Catégorie 4 qui varie selon le run | 23 | 6 | 2 | 3 |
| Leviers par fiche classée (moyenne) | 1,44 | 1,32 | 1,42 | 1,30 |
| Vote majoritaire = prod | 51 / 205 | 55 / 200 | 44 / 184 | 51 / 194 |
| Réponses invalides rejouées | 0 | 0 | 0 | 0 |

| Stabilité par collectivité | v1 · Large 4 | v2.0 · Large 4 | v2.1 · Small | v2.1 · Haiku |
|---|---:|---:|---:|---:|
| Paris Est Marne & Bois (5390) | 60 % | 85 % | 88 % | 94 % |
| CC Brionnais Sud Bourgogne (5033) | 67 % | 86 % | 85 % | 96 % |
| CC Sundgau (4973) | 59 % | 78 % | 73 % | 81 % |
| CC Ardennes Thiérache (3914) | 54 % | 76 % | 83 % | 93 % |

## Coûts

| | v1 · Large 4 (lots de 25) | v2.0 · Large 4 | v2.1 · Small 2603 | v2.1 · Haiku 5.5 |
|---|---:|---:|---:|---:|
| Raisonnement | low | low | aucun (`none`) | aucun |
| Tokens d'entrée (3 runs) | 127 659 | 5 969 384 | 6 337 674 | 11 172 267 |
| … lus en cache | 0 % | 96 % | 98 % | 96 % |
| Tokens de sortie (3 runs) | 330 537 | 1 931 733 | 25 262 | 63 322 |
| Coût des 3 runs (393 fiches) | 0,78 $ | 4,60 $ | 0,97 $ | **0,18 $** |
| Par fiche et par run | 0,066 centime | 0,39 centime | 0,082 centime | **0,015 centime** |
| **1 674 fiches, 1 run** | 1,10 $ | 6,53 $ | 1,37 $ | **0,26 $** |
| Durée des 3 runs (393 fiches) | non mesurée | ≈ 30 min | ≈ 2 min | ≈ 3 min |

Tarifs en USD par million de tokens :

| Modèle | Entrée | Entrée en cache | Écriture cache | Sortie | Source |
|---|---:|---:|---:|---:|---|
| mistral-large-4 | 0,68 | 0,07 | — | 2,09 | grille de `utils/test_run_impact.py` (tarif promo) |
| mistral-small-2603 | 0,15 | 0,15 | — | 0,60 | grille de `utils/test_run_impact.py` |
| claude-haiku-5-5 | 0,10 | 0,01 | 0,125 | 0,50 | [page tarifs Anthropic](https://platform.claude.com/docs/en/about-claude/pricing), prompts < 100 000 tokens |

- **Large 4 coûte cher à cause du raisonnement** : 88 % de son coût vient de la sortie (1 600 tokens par fiche en moyenne). Small et Haiku, sans raisonnement, sortent 20 à 50 tokens par fiche.
- **Le coût de Small est un maximum.** La grille du projet ne lui donne aucune réduction sur le cache, et la page publique de Mistral ne donne pas de prix pour Small 4. Si Mistral applique la même réduction que sur Large 4 (−90 % sur le cache), le coût tomberait vers 0,15 $ pour 1 674 fiches.
- Haiku compte environ 9 100 tokens pour le prompt système, contre 5 100 chez Mistral (tokeniseur différent). Le cache ramène ce coût à presque rien.

## Accord entre modèles

Votes majoritaires identiques (sur 393 fiches) :

| | v2.0 · Large 4 | v2.1 · Small | v2.1 · Haiku |
|---|---:|---:|---:|
| v1 · Large 4 | 55 % | 51 % | 54 % |
| v2.0 · Large 4 | | 69 % | 74 % |
| v2.1 · Small | | | 69 % |

Les 3 modèles v2 sont d'accord sur 240 fiches. Ils divergent sur 153. Sur un échantillon de 18 de ces fiches :

- **Small laisse plus souvent une fiche sans levier** alors que Large 4 et Haiku en trouvent un plausible : « Création d'une objeterie » (3914/76580), « opérations de broyage » (4973/53168), « mise en place d'une ORT » (3914/76549), « informer sur les subventions EnR » (5390/85680).
- **Haiku et Large 4 sont souvent d'accord.** Haiku fait quelques écarts : « Natura 2000, lien à la nature » (3914/76378) classé en Sobriété foncière, ce que le prompt exclut, et Réduction des déplacements ajoutée à la mobilité des agents (4973/42050).
- **Un nouveau cas limite** : un plan de mobilité de l'administration (5390/85724) est en 5 pour Large 4, et en 2 pour Small et Haiku. Le prompt ne dit pas si un plan interne relève de la planification (2) ou de l'exemplarité (5).

## Limites du test

- **Large 4 n'a pas été relancé avec la version corrigée du prompt (v2.1)** : le run a été annulé à ta demande. Ses chiffres viennent du test v2.0. La comparaison Large 4 / Small / Haiku mélange donc un effet modèle et un léger effet prompt. Les 54 fiches déjà classées par ce run annulé sont dans `mistral-large-4/`, mais ne sont pas utilisées.
- **Stabilité ne veut pas dire justesse.** Aucun jeu de référence n'existe encore (R3). L'accord avec la prod (24 à 28 %) ne départage pas les modèles, puisque la prod a été classée avec l'ancien prompt.
- **Haiku : schéma strict, avec une limite.** Un premier run Haiku sans mode strict a produit 13 réponses invalides et 3 fiches en échec. Il est archivé dans `claude-haiku-5-5_schema_non_strict/`. Le run retenu utilise le mode strict d'Anthropic, qui rend les codes hors liste impossibles. Ce mode refuse la limite de 3 leviers : elle est appliquée après coup, en gardant les 3 premiers. C'est arrivé 1 fois sur 1 179 appels.
- Les réglages de raisonnement ne sont pas identiques : « low » pour Large 4 (« none » refusé), « none » pour Small (« low » refusé), pas de raisonnement pour Haiku.

## Fichiers

- `mistral-small-2603/` et `claude-haiku-5-5/` : runs, `rapport.md` (détail fiche par fiche), `motifs_ecarts.md` (statistiques des écarts), `prompt_utilise.md` (prompt exact)
- `../stabilite_mistral_volet_ges_v2/` : test v2.0 de Large 4, avec son prompt dans `prompt_utilise.md`
