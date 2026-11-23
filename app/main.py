"""Point d'entrée : assemble les trois couches (contrôleur -> service -> accès aux données).

Lancer l'application :  uvicorn app.main:app --reload
"""
import os

from fastapi import FastAPI

from app.controllers.ticket_controller import build_router
from app.repositories.ticket_repository import TicketRepository
from app.services.ticket_service import TicketService


def create_app(db_path: str | None = None) -> FastAPI:
    db_path = db_path or os.environ.get("DAWRI_DB", "dawri.db")
    repository = TicketRepository(db_path)
    repository.init_schema()
    service = TicketService(repository)

    app = FastAPI(title="Dawri", description="Gestion des files d'attente de la Poste tunisienne")
    app.include_router(build_router(service))

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()
