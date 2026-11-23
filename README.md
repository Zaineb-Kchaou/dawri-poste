# Dawri : gestion des files d'attente de la Poste tunisienne

Dawri (« mon tour » en arabe) permet au client de prendre un **ticket virtuel**, de suivre son attente
et d'être notifié quand son tour approche, pour ne plus attendre debout au bureau de poste.

Projet du cours Processus unifié et méthodes agiles. Équipe : Zaineb Kchaou, Nour Nejia Slim, Sonia Mejri, Jed Jemili.

## Cas d'utilisation

| UC | Intitulé | Phase |
|---|---|---|
| UC1 | Prendre un ticket virtuel (**UC à risque : concurrence**) | Élaboration |
| UC2 | Suivre sa position et son attente estimée | Construction |
| UC3 | Être notifié quand son tour approche | Construction |
| UC4 | Appeler le client suivant (agent) | Construction |
| UC5 | Annuler ou reporter son ticket | Transition |
| UC6 | Consulter les statistiques d'affluence | Transition |

## Architecture de base (UC1 de bout en bout)

```
POST /tickets -> TicketController -> TicketService -> TicketRepository -> SQLite
   (présentation)       (métier)        (accès aux données)
```

Le point critique est l'attribution du numéro de ticket quand plusieurs clients arrivent en même temps
(voir `app/repositories/ticket_repository.py` et le test `test_concurrence_50_clients_obtiennent_50_numeros_distincts`).

## Lancer le projet

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -v              # lance les tests
uvicorn app.main:app --reload    # lance l'API : http://127.0.0.1:8000/docs
```

Exemple : `POST /tickets` avec `{"bureau_id": "TUNIS-RP", "service_code": "CCP", "client_phone": "20123456"}`

## Organisation Git

- `main` : version stable.
- Une branche par UC : `feature/uc1-prendre-ticket`, `feature/uc2-suivre-position`, etc.
- Une issue par UC, rattachée au milestone de sa phase (Inception, Élaboration, Construction, Transition).
- Les jalons de phase sont des tags : `v0.0-inception`, `v0.1-elaboration`, `v0.5-construction`, `v1.0-transition`.
- Toute fusion passe par une pull request relue (voir `docs/REVUE_CROISEE.md`) avec la CI verte.

## Documentation

- `docs/vision.md` : vision et acteurs
- `docs/priorisation-planning.md` : priorisation des UC et planning des 3 itérations
- `docs/uc/` : fiches des cas d'utilisation
- `docs/uml/` : diagrammes PlantUML (cas d'utilisation, classes, séquence, cycle en Y)
