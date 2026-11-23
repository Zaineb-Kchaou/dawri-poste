"""Modèle métier : un ticket virtuel pris par un client dans un bureau de poste."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Ticket:
    id: int
    bureau_id: str
    service_code: str
    day: str          # jour du ticket, format AAAA-MM-JJ (la numérotation repart de 1 chaque jour)
    number: int       # numéro affiché au client, unique par (bureau, service, jour)
    client_phone: str
    status: str       # WAITING, CALLED, SERVED, CANCELLED, NO_SHOW
    created_at: str
