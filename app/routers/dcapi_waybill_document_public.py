from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import Response

from app.stubs import load_stubs

router = APIRouter(
    prefix="/v3/dcapi-waybill-document-public", tags=["dcapi-waybill-document-public"]
)
_stubs = load_stubs("dcapi_waybill_document_public")


@router.get("/cost-centers")
def get_cost_centers():
    return _stubs.get("GET /cost-centers", {})


@router.get("/delivery/lead-times")
def get_delivery_lead_times(receiverCountryIso: str, product: str):
    return _stubs.get("GET /delivery/lead-times", {})


@router.post("/waybill/documents", status_code=201)
def upload_waybill_document():
    return _stubs.get("POST /waybill/documents", {})


@router.post("/waybill/signatures", status_code=201)
def upload_waybill_signature():
    return _stubs.get("POST /waybill/signatures", {})


@router.post("/waybills", status_code=201)
def create_waybill():
    return _stubs.get("POST /waybills", {})


@router.delete("/waybills/{trackingNumber}", status_code=204)
def delete_waybill(trackingNumber: str):
    return Response(status_code=204)


@router.get("/waybills/{trackingNumber}/{fileName}")
def reprint_waybill(trackingNumber: str, fileName: str):
    return _stubs.get("GET /waybills/{trackingNumber}/{fileName}", {})
