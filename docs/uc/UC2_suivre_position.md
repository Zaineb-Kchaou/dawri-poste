# UC2 Suivre sa position et son attente estimée

**Acteur principal** : Client
**Priorité** : 2

## Préconditions
- Le client possède un ticket WAITING.

## Scénario nominal
1. Le client ouvre l'écran de suivi.
2. Le système affiche le numéro en cours d'appel, la position du client et le nombre de personnes devant lui.
3. Le système affiche l'attente estimée (nombre de personnes devant multiplié par la durée moyenne de service).
4. L'écran se met à jour automatiquement quand la file avance (moins de 3 secondes).

## Alternatives
- **4a** Pas de connexion : l'écran affiche la dernière position connue avec son heure de mise à jour.
- **2a** Le ticket a été appelé ou annulé : l'écran affiche le nouvel état.
