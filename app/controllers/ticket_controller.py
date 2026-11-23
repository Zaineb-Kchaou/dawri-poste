"""Couche présentation : route HTTP du UC1."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.errors import ActiveTicketExists, InvalidRequest


class TicketRequest(BaseModel):
    bureau_id: str
    service_code: str
    client_phone: str


class TicketResponse(BaseModel):
    id: int
    bureau_id: str
    service_code: str
    number: int
    position: int
    status: str


def build_router(service) -> APIRouter:
    router = APIRouter()

    @router.post("/tickets", response_model=TicketResponse, status_code=201)
    def take_ticket(request: TicketRequest):
        try:
            result = service.take_ticket(request.bureau_id, request.service_code, request.client_phone)
        except InvalidRequest as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        except ActiveTicketExists:
            raise HTTPException(status_code=409, detail="Vous avez déjà un ticket en attente pour ce service.")
        t = result.ticket
        return TicketResponse(id=t.id, bureau_id=t.bureau_id, service_code=t.service_code,
                              number=t.number, position=result.position, status=t.status)

    return router
