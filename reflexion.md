# Note de réflexion — Stratégie d'anonymisation 
## Ma stratégie d'anonymisation
Une **stratégie mixte par type de PII** :  
- **PERSON** (noms de personnes, détectés par spaCy `en_core_web_md`) : **HASH salé** ->
  (SHA-256 tronqué à 8 caractères hex, préfixé `[PERSON_<hash>]`).
- **EMAIL / PHONE / IBAN_PARTIAL** (détectés par regex) -> **SUPPRESSION**
  (`[EMAIL]`, `[PHONE]`, `[IBAN]`).
- **GPE / ORG** : non traités, hors périmètre. Conservés tels quels.
L'ordre d'exécution est important : les regex sont appliquées **avant** la détection
spaCy. Un bug réel a été observé dans l'ordre inverse — un faux positif spaCy sur un
nombre isolé (`****3503` → `3503` mal étiqueté `PERSON`), produit
`****[PERSON_xxxx]` au lieu de `[IBAN]`. Corrigé en inversant l'ordre des deux étapes.

## Ce que j'ai gardé lisible et pourquoi
- **`GPE` / `ORG`** : conservés tels quels. Ce ne sont pas des PII directement identifiantes dans ce corpus, les garder préserve le contexte métier du commentaire.
- **`TICKET_RH` (ex. `HR-24680`)** : conservé, car bien que considérable comme donnée interne, elles ne sont pas connectables aux données internes associées. Il s'agit d'avant tout d'une donnée technique et non métier. La conservation peut permettre l'association sans risques avec des données sensibles non exposées (mais présentes en  interne).
- **Le reste de la phrase** (dates, structure grammaticale, verbes) : conservé tel quel sur les commentaires anglais, où la stratégie fonctionne sans accroc.

## Ce que j'ai masqué et pourquoi
- **Noms de personnes (`PERSON`)** : en hash plutôt qu'en suppression, pour garder une **cohérence** dans le corpus — si la même personne apparaît dans plusieurs commentaires, elle produit toujours le même hash, permettant de repérer des récidives de signalement sur un même individu.
- **EMAIL, PHONE, IBAN partiel** : en suppression simple, car nécessaire dans ce corpus. S'il y a un besoin de les réassocier au contexte d'une personne, il est possible de les associer au HASH de la personne sans pour autant les exposer.

## Trade-offs assumés
Le curseur a été placé différemment selon la langue du commentaire, **involontairement** :

- **Sur l'anglais** : la stratégie fonctionne comme prévu. Sur 8 exemples anglais
  testés (`audit_sample.csv`, lignes 1 à 8), 100 % des `PERSON`/`EMAIL`/`PHONE`/`IBAN`
  sont correctement traités, la phrase reste lisible et grammaticalement correcte.
- **Sur le français** : la lisibilité s'effondre. Exemple réel (ligne 9) :
  - Avant : *« Alerte comportementale signalée par Valentine Ribeiro au sujet de Noël Joubert de Lagarde. »*
  - Après : *« Alerte [PERSON_4ebafea7] par [PERSON_ab3885ff] [PERSON_d5ad5e57]. »*
  - Le mot `comportementale signalée` est hashé comme s'il s'agissait d'un nom, et le connecteur `au sujet de` disparaît entre les deux entités — la phrase perd du sens.
Je n'ai donc **pas choisi** ce trade-off lisibilité/protection sur le français — c'est une conséquence non maîtrisée de la fiabilité dégradée de `en_core_web_md` hors de l'anglais, documentée mais pas corrigée à ce stade.

## Cadre réglementaire — RGPD + AI Act

- **RGPD** : ma stratégie répond partiellement à la minimisation des données — les identifiants directement réutilisables (email, téléphone, IBAN) sont supprimés sans laisser de trace exploitable. Cependant, **le hash salé n'est pas une anonymisation au sens du RGPD, mais une pseudonymisation**
En l'absence du sel, le dataset anonymisé reste donc dans le périmètre RGPD tant que le sel existe quelque part (en local dans .env).
- **AI Act** : un système exploitant des commentaires RH pour évaluer des individus relève potentiellement du **« haut risque »** (Annexe III, gestion des
  travailleurs). Mon audit éthique (DI intersectionnel `sex × race` = 0.164), et cette anonymisation contribuent à la **traçabilité** exigée par le règlement, mais ne suffisent pas seuls à répondre aux exigences de supervision humaine et de qualité des données — l'anonymisation imparfaite sur
  le français présente le risque résiduel.

## Limites de ma stratégie
- **Faux négatifs (PII non détectées)** :
  - `TICKET_RH` (ex. `HR-24680`) n'est pas masqué — identifiant potentiellement réutilisable pour retrouver un dossier RH précis. Risque acceptable en l'absence des données sensibles associées.
  - Trou NER FR/EN documenté en tâche 7 : sur 2 commentaires français testés sur 10, la délimitation des entités `PERSON` est dégradée (voir Trade-offs).  
- **Faux positifs (texte normal anonymisé à tort)** :
  - Sur les commentaires français, des fragments de phrase entiers (`comportementale signalée`, `versée`) sont hashés comme s'il s'agissait de noms propres.
  - Un nombre isolé (`3503` dans `****3503`) a initialement été mal étiqueté `PERSON` par spaCy — corrigé en inversant l'ordre regex/spaCy.
- **Test partiel** : seuls 10 exemples sur les 200 lignes de `audit_sample.csv` ont été vérifiés à ce stade.

## Si je devais industrialiser
- Router les commentaires détectés comme français vers `fr_core_news_md` plutôt que `en_core_web_md`, pour réduire les faux positifs de délimitation observés.
- Ajouter un filtre de longueur/contenu sur les entités `PERSON` avant hash (rejeter les entités contenant des mots fonctionnels comme `signalée`, `versée`, `par`, `au sujet de`) pour limiter les faux positifs.
- Stocker le sel dans un gestionnaire de secrets dédié (HashVault, AWS SM) plutôt qu'une variable d'environnement locale, et faire tourner ce sel périodiquement.
- Passer d'une vérification qualitative sur 10 exemples à un échantillon de validation plus large avant tout déploiement.
---

*Note rédigée par Tom Carpentier, 27/07/2026, dans le cadre du brief M2-B2 ATOS.*