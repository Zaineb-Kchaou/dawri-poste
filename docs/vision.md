# Vision du projet Dawri

## Vision en 5 lignes

1. **Problème** : dans les bureaux de la Poste tunisienne, le client passe un temps d'attente très long sur place. Il connaît sa position, mais il ne peut pas utiliser ce temps, car il doit rester présent pour ne pas perdre son tour.
2. **Utilisateurs** : clients réguliers, agents de guichet, responsable de bureau.
3. **Solution** : un ticket virtuel pris sur mobile, avec une estimation du temps d'attente restant.
4. **Fonctionnement** : le client est notifié quand son tour approche, donc il peut faire autre chose puis revenir à temps.
5. **Valeur** : moins de temps perdu sur place pour les clients ; pour la Poste, une file plus fluide et des statistiques d'affluence.

## Acteurs

| Acteur | Type | Rôle |
|---|---|---|
| Client | Principal | Prend un ticket, suit son attente, annule ou reporte |
| Agent de guichet | Principal | Appelle le client suivant, marque servi ou absent |
| Responsable de bureau | Principal | Consulte les statistiques d'affluence |
| Service de notification (SMS / push) | Secondaire (système) | Envoie les alertes au client |
