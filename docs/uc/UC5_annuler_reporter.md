# UC5 Annuler ou reporter son ticket

**Acteur principal** : Client
**Priorité** : 5

## Préconditions
- Le client possède un ticket WAITING.

## Scénario nominal (annuler)
1. Le client choisit « Annuler mon ticket » et confirme.
2. Le système passe le ticket à CANCELLED et met à jour la file.

## Scénario nominal (reporter)
1. Le client choisit « Je reviens dans 10 minutes ».
2. Le système replace le ticket quelques positions plus loin et prévient le client de sa nouvelle position.

## Alternatives
- Le ticket a déjà été appelé : le report est refusé.
