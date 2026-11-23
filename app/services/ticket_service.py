"""Couche métier du UC1 : prendre un ticket virtuel."""
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

from app.errors import InvalidRequest
from app.models import Ticket

# Services proposés dans un bureau de poste (liste simplifiée pour le projet).
SERVICES = {"COURRIER", "COLIS", "CCP", "MANDAT"}

# Numéro de téléphone tunisien : 8 chiffres, avec ou sans +216.
PHONE_PATTERN = re.compile(r"^(?:\+216)?(\d{8})$")


@dataclass(frozen=True)
class TicketResult:
    ticket: Ticket
    position: int   # nombre de personnes devant le client, lui compris


class TicketService:
    def __init__(self, repository, now: Callable[[], datetime] = lambda: datetime.now(timezone.utc)):
        self.repository = repository
        self.now = now  # injectable pour tester sans dépendre de l'horloge

    def take_ticket(self, bureau_id: str, service_code: str, client_phone: str) -> TicketResult:
        bureau_id = (bureau_id or "").strip()
        service_code = (service_code or "").strip().upper()
        if not bureau_id:
            raise InvalidRequest("Le bureau est obligatoire.")
        if service_code not in SERVICES:
            raise InvalidRequest(f"Service inconnu : {service_code or '(vide)'}.")
        match = PHONE_PATTERN.match((client_phone or "").replace(" ", ""))
        if not match:
            raise InvalidRequest("Numéro de téléphone tunisien invalide (8 chiffres).")
        phone = match.group(1)

        moment = self.now()
        ticket = self.repository.create_with_next_number(
            bureau_id, service_code, moment.date().isoformat(), phone, moment.isoformat()
        )
        position = self.repository.count_waiting_up_to(
            ticket.bureau_id, ticket.service_code, ticket.day, ticket.number
        )
        return TicketResult(ticket=ticket, position=position)
