# Datasheet — Adult Income enrichi (Athéna RH v1.0.0)

> Document accompagnant le dataset livré à Athéna RH.
> **Modèle Gebru et al. (2018), 7 sections, 2 pages max.**
> Signée binôme.

**Auteurs** : Tom, Romain
**Date** : 17/06/2026
**Version** : v1.0.0

## 1. Motivation

> Pourquoi ce dataset existe ? Qui l'a créé ?

- Le socle du dataset est un jeu de données **Adult**, qui classe le revenu à partir de variables du recensement américain.
- Il a été **enrichi pour Athéna RH** avec des commentaires manager synthétiques contenant des PII non maîtrisées.

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
| `education` | str | Diplôme (16 modalités) |
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

- ...

## 4. Preprocessing appliqué

> Ce que **votre binôme** a fait dans la phase sync.

- ...

## 5. Usages prévus / à éviter

**Usages prévus** :
- ...

**Usages à éviter** :
- ...

## 6. Distribution

- Destinataire : Athéna RH (Laurence Béthencourt, DPO)
- Format : Parquet snappy
- Conditions : ...

## 7. Maintenance

- Mainteneur·euses : <prénom1>, <prénom2>
- Version : v1.0.0 — <date>
- Signaler un problème : ...

---

*Datasheet produite en binôme dans le cadre du brief M2-B2 ATOS.*