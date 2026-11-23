# UC3 Être notifié quand son tour approche

**Acteurs** : Client, service de notification (SMS / push)
**Priorité** : 3

## Préconditions
- Le client possède un ticket WAITING et a autorisé les notifications.

## Scénario nominal
1. La file avance (un agent appelle un client, UC4).
2. Le système détecte qu'il reste 3 personnes devant le client.
3. Le système envoie une notification « Votre tour approche ».
4. Quand le ticket du client est appelé, le système envoie une seconde notification « C'est votre tour, guichet N ».

## Alternatives
- **3a** Notification push impossible : le système envoie un SMS à la place.
- **3b** Le fournisseur SMS est indisponible : le système réessaie, puis journalise l'échec.
