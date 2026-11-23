# UC1 Prendre un ticket virtuel (UC à risque technique)

**Acteur principal** : Client
**Priorité** : 1 (valeur 3, risque 3, impact architecture 3)

## Préconditions
- Le client est identifié par son numéro de téléphone.
- Le bureau est ouvert et le service choisi est disponible.

## Scénario nominal
1. Le client choisit un bureau (ou scanne le QR code affiché au bureau).
2. Le client choisit un service (courrier, colis, CCP, mandat).
3. Le système vérifie le service et le numéro de téléphone.
4. Le système vérifie que le client n'a pas déjà un ticket en attente pour ce service.
5. Le système attribue le numéro suivant de la file, de façon atomique.
6. Le système enregistre le ticket avec le statut WAITING.
7. Le système affiche au client son numéro et sa position dans la file.

## Scénarios alternatifs et d'erreur
- **3a** Service inconnu ou téléphone invalide : erreur 400, aucun ticket créé.
- **4a** Le client a déjà un ticket en attente pour ce service : erreur 409, aucun ticket créé.
- **5a** Plusieurs clients prennent un ticket au même moment : les demandes sont traitées l'une après l'autre dans la base, chaque client reçoit un numéro distinct.
- **5b** Le même client clique plusieurs fois : un seul ticket est créé, les autres demandes reçoivent l'erreur 409.

## Postconditions
- Un ticket WAITING existe, avec un numéro unique pour (bureau, service, jour).

## Le risque et sa parade
| Risque | Parade | Preuve |
|---|---|---|
| Deux clients reçoivent le même numéro | Numéro calculé dans la base, transaction `BEGIN IMMEDIATE` | Test des 50 clients simultanés |
| Doublon en cas de bug applicatif | Contrainte `UNIQUE (bureau, service, jour, numéro)` | Schéma de la table `ticket` |
| Double clic du client | Index unique partiel sur les tickets WAITING | Test du double clic |
