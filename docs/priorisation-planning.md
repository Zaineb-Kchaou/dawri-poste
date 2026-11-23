# Priorisation des UC et planning

## Priorisation (notes de 1 à 3)

| UC | Valeur métier | Risque | Impact architecture | Total | Ordre |
|---|---|---|---|---|---|
| UC1 Prendre un ticket | 3 | 3 | 3 | 9 | 1 |
| UC2 Suivre sa position | 3 | 2 | 3 | 8 | 2 |
| UC3 Notification de tour | 3 | 3 | 2 | 8 | 3 |
| UC4 Appeler le client suivant | 3 | 2 | 2 | 7 | 4 |
| UC5 Annuler ou reporter | 2 | 1 | 1 | 4 | 5 |
| UC6 Statistiques d'affluence | 2 | 1 | 1 | 4 | 6 |

**À traiter en premier : UC1** (risque de concurrence sur la numérotation, base de tout le système), puis UC2 et UC3.
UC4 est livré dès l'itération 2 car sans agent la file n'avance pas.

## Planning : 3 itérations, 4 phases, jalons

| Itération | Phase | Contenu | Jalon | Tag Git |
|---|---|---|---|---|
| 1 | Inception | Vision, acteurs, UC, priorisation, dépôt GitHub | Objectifs du cycle de vie (LCO) | `v0.0-inception` |
| 1 | Élaboration | Diagramme de cas d'utilisation, architecture de base, route UC1 + test en CI | Architecture du cycle de vie (LCA) | `v0.1-elaboration` |
| 2 | Construction | UC2, UC3, UC4 | Capacité opérationnelle initiale (IOC) | `v0.5-construction` |
| 3 | Transition | UC5, UC6, revue croisée, recette, mise en pilote | Livraison du produit (PR) | `v1.0-transition` |
