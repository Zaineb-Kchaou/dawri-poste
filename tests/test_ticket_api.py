"""Tests d'intégration : route HTTP -> service -> base SQLite réelle."""
from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient


def _post(client, phone, service="CCP", bureau="TUNIS-RP"):
    return client.post("/tickets", json={"bureau_id": bureau, "service_code": service, "client_phone": phone})


def test_scenario_nominal_de_bout_en_bout(client):
    response = _post(client, "20123456")
    assert response.status_code == 201
    body = response.json()
    assert body["number"] == 1
    assert body["position"] == 1
    assert body["status"] == "WAITING"


def test_deuxieme_client_recoit_le_numero_suivant(client):
    _post(client, "20123456")
    response = _post(client, "21123456")
    assert response.json()["number"] == 2
    assert response.json()["position"] == 2


def test_meme_client_meme_service_refuse(client):
    assert _post(client, "20123456").status_code == 201
    assert _post(client, "20123456").status_code == 409


def test_meme_client_autre_service_accepte(client):
    assert _post(client, "20123456", service="CCP").status_code == 201
    assert _post(client, "20123456", service="COLIS").status_code == 201


def test_donnees_invalides_renvoient_400(client):
    assert _post(client, "abc").status_code == 400
    assert _post(client, "20123456", service="PIZZA").status_code == 400


def test_numerotation_independante_par_service(client):
    assert _post(client, "20123456", service="CCP").json()["number"] == 1
    assert _post(client, "21123456", service="COLIS").json()["number"] == 1


def test_concurrence_50_clients_obtiennent_50_numeros_distincts(app):
    """UC à risque : 50 clients prennent un ticket en même temps, aucun doublon ne doit exister."""
    phones = [f"2{i:07d}" for i in range(50)]

    def take(phone):
        return _post(TestClient(app), phone)

    with ThreadPoolExecutor(max_workers=20) as pool:
        responses = list(pool.map(take, phones))

    assert all(r.status_code == 201 for r in responses)
    numbers = sorted(r.json()["number"] for r in responses)
    assert numbers == list(range(1, 51))  # 1..50, sans trou ni doublon


def test_concurrence_double_clic_du_meme_client(app):
    """Le même client clique 10 fois en même temps : un seul ticket est créé."""
    def take(_):
        return _post(TestClient(app), "20123456")

    with ThreadPoolExecutor(max_workers=10) as pool:
        responses = list(pool.map(take, range(10)))

    codes = sorted(r.status_code for r in responses)
    assert codes.count(201) == 1
    assert codes.count(409) == 9
