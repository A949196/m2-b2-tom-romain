# Datasheet — Adult Income enrichi (Athéna RH v1.0.0)

> Document accompagnant le dataset livré à Athéna RH.
> **Modèle Gebru et al. (2018), 7 sections, 2 pages max.**
> Signée binôme.

**Auteurs** : Tom, Romain
**Date** : 17/06/2026
**Version** : v1.0.0

## 1. Motivation

> Pourquoi ce dataset existe ? Qui l'a créé ?

- Le socle du dataset est un jeu de données **Adult**, qui permet de prédire le revenu (<=50k$ ou >50k$) à partir de variables du recensement américain. Il a été créé par UCI Adult Census en 1994.
- Il a été **enrichi par Athéna RH** avec des commentaires de managers sous forme synthétiques ajoutant des notes RH et contenant des PII non maîtrisées.

## 2. Composition

> Combien d'observations, quelles colonnes, types, distribution cible,
> **variables sensibles signalées explicitement**, + le résumé du
> verdict éthique (DI les plus problématiques).

| Aspect | Valeur |
|---|---|
| Nombre de lignes | 32 561 |
| Nombre de colonnes | 16 (14 features UCI + cible `income` + `manager_comments` synthétique) |
| Cible | `income` : `<=50K` / `>50K` |
| Distribution cible | <=50K: 75.6 % / >50K: 24.4 % |
| Variables sensibles | `sex`, `race`, `native_country`, `marital_status` |

**Schéma des colonnes** :

| Colonne | Type | Note |
|---|---|---|
| `age` | int | 17 — 90 |
| `workclass` | str | Statut de travail (9 modalités) |
| `fnlwgt` | int | Poids d'échantillonnage du recensement |
| `education` | str | Diplôme (16 modalités) |
| `education_num` | int | Niveau d'éducation codé |
| `marital_status` | str | ⚠️ Sensible |
| `occupation` | str | Profession (15 modalités) |
| `relationship` | str | Position familiale (6 modalités) |
| `race` | str | ⚠️ Sensible (5 modalités) |
| `sex` | str | ⚠️ Sensible binaire |
| `capital_gain` / `capital_loss` | int | Très asymétriques (médiane 0) |
| `hours_per_week` | int | 1 — 99 |
| `native_country` | str | ⚠️ Sensible (40+ modalités) |
| `income` (cible) | str | `<=50K`, `>50K` |
| `manager_comments` | str | Texte libre **avec PII** — à anonymiser en async |

**Résumé verdict éthique** :
- DI le plus problématique :
| Variable | DI | Verdict |
|---|---|---|
| sex | 0.358 | ALERTE — femmes très désavantagées |
| race | 0.347 | ALERTE — groupes non-blancs désavantagés |
| native_country (USA/non-USA) | 0.804 | Cas limite |
| sex × race (intersection) | 0.164 | CRITIQUE — femmes Black et Other SR ≈ 0.06 |
 
Le biais le plus problématique est l'intersection sex × race (DI = 0.164).

- Intersectionnalités notables :
    - sex x race : les femmes issues de minorités raciales ont un taux d'accès aux revenus >50K environ bien inférieur à celui des hommes blancs. Ce biais est invisible lorsqu'on examine sex et race séparément.
    - relationship x sex : car dans relationship il y a les valeurs `Husband` et `Wife` qui sont forcément `Male` et `Female`


## 3. Processus de collecte

> Origine UCI Adult Census 1994 + enrichissement Athéna RH 2026.

- L’extraction a été faite par Barry Becker à partir de la base de données du recensement (collecte humaine) de 1994 (donc sur une période de 1 an).  Un ensemble d’enregistrements raisonnablement propre a été extrait en utilisant les conditions suivantes : ((AAGE>16) && (AGI>100) && (AFNLWGT>1)&& (HRSWK>0)).
- L'enrichissement Athéna RH 2026 est une colonne supplémentaire ajoutée en 2026 par des managers sous forme de commentaires textuels contenant potentiellement des PII. Ces ajouts n'ont pas modifiés l'existant.
- **Biais probable** : reflète la composition socio-économique américaine de 1994.

## 4. Preprocessing appliqué

> Ce que **votre binôme** a fait dans la phase sync.

- Imputation manquants : aucune imputation nécessaire sur les variables du socle; les commentaires doivent être anonymisés.
- Encodage : 
    - OneHotEncoder sur `workclass` et `occupation`
    - StandardScaler sur les numériques (`age`, `education_num`, `capital_gain`, `capital_loss` et `hours_per_week`).
- Exclusions : `education` retirée au profit de `education_num` ; `race`, `sex` et `native_country` retirées car sensibles ou fortement biaisantes ; `fnlwgt`, `marital_status` et `relationship` retirées car peu utiles pour l'objectif du dataset.

`Capital_gain` et `capital_loss` sont des variables utiles pour prédire income, parce qu’elles portent une information économique réelle. En revanche, elles sont très asymétriques, souvent à zéro, et peuvent dominer les modèles si on ne fait pas attention. Elles ne sont pas sensibles en elles-mêmes, mais elles peuvent agir comme indicateurs indirects de niveau de richesse.

## 5. Usages prévus / à éviter

**Usages prévus** : évaluer si une évolution de carrière est possible et si la demande de salaire reste dans la grille logique de l'entreprise.

**Usages à éviter** :
- Décision RH automatisée réelle (recrutement, promotion, licenciement, rémunération) sans revue humaine et cadre juridique.
- Profilage individuel ou notation d'employés à partir de données sensibles ou de proxys sensibles.
- Réutilisation des commentaires textuels bruts contenant des PII sans anonymisation préalable.
- Généralisation directe à des populations actuelles sans recalibrage, compte tenu du biais historique (USA 1994).

## 6. Distribution

- Destinataire : Athéna RH (Laurence Béthencourt, DPO)
- Format : Parquet snappy
- Conditions : dataset RH sensible contenant des données nominatives dans `manager_comments`; anonymisation/pseudonymisation obligatoire (PII retirées ou masquées), accès restreint et traçable, et interdiction d'entraîner un modèle tant que la validation DPO n'est pas obtenue.

## 7. Maintenance

- Mainteneur·euses : Tom, Romain
- Version : v1.0.0 — 17/06/2026
- Signaler un problème : ticket interne FastIA-007

---

*Datasheet produite en binôme dans le cadre du brief M2-B2 ATOS.*