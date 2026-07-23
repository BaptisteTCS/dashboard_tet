# Calcul des volets hors compétence

## Objectif

Pour chaque collectivité, déterminer les couples (levier, catégorie), appelés volets, qui ne la concernent pas au vu de ses compétences BANATIC, et les écrire dans `priorisation_hors_competence`.

Un volet est **hors compétence** si et seulement si il n'appartient pas à l'ensemble des volets retenus calculé ci-dessous. On écrit donc le complément : `tous les volets possibles` moins `volets retenus`.

Univers complet : 29 leviers x 6 catégories = 174 volets par collectivité.

## Catégories

```python
CATEGORIES = {
    1: "Aménagement",
    2: "Planification",
    3: "Financement",
    4: "Gouvernance",
    5: "Exemplarité",
    6: "Sensibilisation",
}
```

Correspondance catégorie vers tag de compétence requis :

```python
CATEGORIE_TAG = {
    1: "ope",
    2: "plan",
    3: "fin",
    5: "patri",
    # 4 (Gouvernance) et 6 (Sensibilisation) : aucun tag requis
}
CATEGORIES_TRANSVERSES = {4, 6}
```

## Fichiers de référence

| fichier | colonnes | rôle |
|---|---|---|
| `leviers.csv` | levier | liste des 29 leviers, source de vérité pour l'orthographe exacte |
| `competence_levier.csv` | competence_code, levier | quelle compétence donne prise sur quel levier |
| `competence_tags.csv` | competence_code, libelle_court, tag | nature de chaque compétence, une ligne par tag |
| `exceptions_a_leviers_restreints.csv` | levier, categorie_id, categorie | leviers sans base de compétence, liste blanche fermée de catégories |
| `exemplarite_regles.csv` | levier, regle | regle vaut `exclu` ou `toujours_ouvert` |

`competence_tags.csv` est en format long : une compétence à trois tags occupe trois lignes. Charger avec un groupby sur competence_code.

Les libellés de leviers doivent matcher exactement entre tous les fichiers. Normaliser en NFC avant comparaison, ne pas faire de strip agressif ni de lowercase, les accents et la casse font partie de la clé.

## Sources de données

```sql
select
    c.id as collectivite_id,
    cb.competence_code
from imports.competence_banatic cb
join public.collectivite c on c.siren = cb.siren
join public.banatic_competence bc on bc.code = cb.competence_code
```

La jointure sur `banatic_competence` sert à écarter les codes inconnus du référentiel. Vérifier les types : si `siren` est du texte d'un côté et un entier de l'autre, caster explicitement, et attention aux SIREN à zéro non significatif en tête.

Une collectivité absente de `imports.competence_banatic` a un ensemble de compétences vide. Elle ne doit pas être ignorée : elle reçoit tous les volets non transverses en hors compétence, sauf ce que les règles C et D rouvrent. Il faut donc itérer sur `public.collectivite`, pas sur le résultat de la jointure.

## Algorithme

Pour une collectivité donnée, soit `COMPS` l'ensemble de ses codes compétence.

```
volets_retenus = {}

pour chaque levier L des 29 :

    # Etape 1 : exception A, liste blanche fermée
    si L est dans exceptions_a_leviers_restreints.csv :
        volets_retenus += {(L, cat) pour cat listée pour L}
        passer au levier suivant   # A écrase tout, aucune autre règle ne s'applique

    # Etape 2 : catégories transverses
    volets_retenus += {(L, 4), (L, 6)}

    # Etape 3 : croisement standard sur les catégories 1, 2, 3, 5
    comps_du_levier = {c dans COMPS tel que (c, L) dans competence_levier.csv}
    pour cat dans {1, 2, 3, 5} :
        tag = CATEGORIE_TAG[cat]
        si un c de comps_du_levier porte le tag :
            volets_retenus += {(L, cat)}

    # Etape 4 : règle C, exemplarité toujours ouverte
    si exemplarite_regles[L] == "toujours_ouvert" :
        volets_retenus += {(L, 5)}

    # Etape 5 : règle D, financement générique
    si COMPS contient au moins un de {1540, 1560, 3505, 3005} :
        volets_retenus += {(L, 3)}

    # Etape 6 : règle B, exclusion exemplarité, s'applique en dernier
    si exemplarite_regles[L] == "exclu" :
        volets_retenus -= {(L, 5)}

hors_competence = tous_les_volets - volets_retenus
```

L'ordre compte. L'étape 1 court-circuite le reste du traitement pour ce levier. L'étape 6 passe après les étapes 3 et 4, elle a le dernier mot sur la catégorie 5.

Les leviers listés en A n'apparaissent pas dans `exemplarite_regles.csv` avec la valeur `toujours_ouvert`, il n'y a donc pas de conflit possible entre A et C. Les leviers listés en A et marqués `exclu` en B sont cohérents : A ne leur accorde jamais la catégorie 5.

### Périmètre de la règle A

La règle A liste les leviers qui échappent structurellement à toute compétence de collectivité ; elle ne doit pas servir à restreindre un levier qui dispose d'une base juridique réelle.

Après réduction du périmètre, la liste A ne contient plus que cinq leviers, tous agricoles ou industriels : `Elevage durable`, `Changements de pratiques de fertilisation azotée`, `Bâtiments & Machines agricoles`, `Gestion des prairies` et `Production Industrielle`.

Les leviers `Captage de méthane dans les ISDND`, `Efficacité et sobriété logistique` et `Fret décarboné et multimodalité` sont sortis de A : ils disposent d'une base de compétence réelle et passent désormais par le croisement standard. `Captage de méthane dans les ISDND` récupère sa prise via la compétence 1510 (taguée `ope`, `plan`, `patri`) ; `Efficacité et sobriété logistique` et `Fret décarboné et multimodalité` reçoivent une base d'Aménagement via la compétence 5005 (voirie), en plus de leurs rattachements existants (3505, 4550 pour le premier ; 3505, 4505 pour le second). Ces trois leviers restant marqués `exclu` en B, l'étape 6 devient la seule chose qui leur retire la catégorie 5.

`Production Industrielle` reste en A mais gagne la catégorie Financement (compétence 3505, subvention à la décarbonation industrielle) ; Aménagement et Exemplarité restent fermés, l'outil de production étant du patrimoine privé.

## Ecriture

Table cible `priorisation_hors_competence (id, collectivite_id, levier, categorie, created_at)`.

`levier` est le libellé texte exact. `categorie` est l'entier 1 à 6.

Idempotence : le calcul est un recalcul complet. Envelopper dans une transaction, supprimer les lignes existantes de la collectivité puis insérer les nouvelles, ou faire un delete global puis un insert massif si le job tourne sur l'ensemble du référentiel. Ne pas faire d'insert incrémental sans purge, cela accumulerait des doublons à chaque exécution.

Insérer par batch, l'ordre de grandeur est de plusieurs dizaines de milliers de collectivités multipliées par le nombre de volets exclus.

## Contrôles à mettre en place

Après calcul, vérifier ces invariants :

1. Aucune ligne écrite avec `categorie` valant 4 ou 6 pour un levier absent de la liste A. Les catégories transverses sont toujours retenues hors exception A.
2. Aucun levier de la liste B présent avec une catégorie 5 dans les volets retenus.
3. Le nombre de volets retenus par collectivité est compris entre 0 et 174.
4. Tous les libellés de levier écrits appartiennent aux 29 de `leviers.csv`. Un mismatch d'accent se détecte ici.
5. Une collectivité sans aucune compétence doit produire un nombre de volets retenus faible et constant. Valeur figée comme test de non régression : **75 volets retenus** (donc 99 volets hors compétence) pour un ensemble de compétences vide.
6. Le nombre de volets *universellement inexistants* (hors compétence quelles que soient les compétences détenues) doit être de **20**. Détail : 16 volets issus de la règle A sur les cinq leviers restants, plus 4 exclusions d'Exemplarité (catégorie 5) portées par des leviers `exclu` hors liste A, à savoir `Biogaz`, `Efficacité et sobriété logistique`, `Fret décarboné et multimodalité` et `Captage de méthane dans les ISDND`.

## Point de réglage

La liste C est volontairement large : elle rouvre l'exemplarité sur treize leviers pour toutes les collectivités. Si le filtrage se révèle trop permissif en production, la restreindre aux quatre premiers leviers du fichier, à savoir les trois leviers tertiaires plus Véhicules électriques. Ce réglage se fait uniquement dans `exemplarite_regles.csv`, aucun changement de code.
