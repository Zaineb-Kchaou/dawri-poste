# UC4 Appeler le client suivant

**Acteur principal** : Agent de guichet
**Priorité** : 4

## Préconditions
- L'agent est connecté et son guichet est ouvert.

## Scénario nominal
1. L'agent clique sur « Appeler le suivant ».
2. Le système choisit le plus petit numéro WAITING du service de ce guichet et passe le ticket à CALLED.
3. Le système déclenche les notifications (UC3).
4. Le client se présente : l'agent marque le ticket SERVED.

## Alternatives
- **4a** Le client ne se présente pas dans les 5 minutes : l'agent marque le ticket NO_SHOW et appelle le suivant.
- **2a** Deux agents appellent en même temps : le système garantit que chaque ticket n'est appelé qu'une fois.
