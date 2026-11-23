"""Tests unitaires de la couche métier (sans base de données : dépôt factice)."""
from datetime import datetime, timezone

import pytest

from app.errors import ActiveTicketExists, InvalidRequest
from app.models import Ticket
from app.services.ticket_service import TicketService


class FakeRepository:
    def __init__(self):
        self.tickets = []

    def create_with_next_number(self, bureau_id, service_code, day, client_phone, created_at):
        if any(t.client_phone == client_phone and t.service_code == service_code for t in self.tickets):
            raise ActiveTicketExists()
        t = Ticket(len(self.tickets) + 1, bureau_id, service_code, day, len(self.tickets) + 1,
                   client_phone, "WAITING", created_at)
        self.tickets.append(t)
        return t

    def count_waiting_up_to(self, bureau_id, service_code, day, number):
        return len([t for t in self.tickets if t.number <= number])


@pytest.fixture
def service():
    fixed = datetime(2026, 11, 23, 9, 0, tzinfo=timezone.utc)
    return TicketService(FakeRepository(), now=lambda: fixed)


def test_nominal_premier_ticket(service):
    result = service.take_ticket("TUNIS-RP", "CCP", "20123456")
    assert result.ticket.number == 1
    assert result.position == 1
    assert result.ticket.day == "2026-11-23"
    assert result.ticket.status == "WAITING"


def test_numeros_consecutifs(service):
    first = service.take_ticket("TUNIS-RP", "CCP", "20123456")
    second = service.take_ticket("TUNIS-RP", "CCP", "21123456")
    assert (first.ticket.number, second.ticket.number) == (1, 2)
    assert second.position == 2


def test_telephone_avec_indicatif_accepte(service):
    result = service.take_ticket("TUNIS-RP", "COLIS", "+216 20 123 456")
    assert result.ticket.client_phone == "20123456"


def test_service_inconnu_refuse(service):
    with pytest.raises(InvalidRequest):
        service.take_ticket("TUNIS-RP", "PIZZA", "20123456")


def test_telephone_invalide_refuse(service):
    with pytest.raises(InvalidRequest):
        service.take_ticket("TUNIS-RP", "CCP", "123")


def test_bureau_obligatoire(service):
    with pytest.raises(InvalidRequest):
        service.take_ticket("  ", "CCP", "20123456")


def test_deuxieme_ticket_actif_refuse(service):
    service.take_ticket("TUNIS-RP", "CCP", "20123456")
    with pytest.raises(ActiveTicketExists):
        service.take_ticket("TUNIS-RP", "CCP", "20123456")
