from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Address(BaseModel):
    AddressType: Optional[str] = None
    Name1: Optional[str] = None
    Name2: Optional[str] = None
    Name3: Optional[str] = None
    Address1: Optional[str] = None
    Address2: Optional[str] = None
    Address3: Optional[str] = None
    Postcode: Optional[str] = None
    City: Optional[str] = None
    CountryISOCode: str
    StateISOCode: Optional[str] = None
    ContactPerson: Optional[str] = None
    PhoneNumber: Optional[str] = None
    EMailAddress: Optional[str] = None
    VatNumber: Optional[str] = None
    TaxNumber: Optional[str] = None


class Article(BaseModel):
    Description: Optional[str] = None
    CommercialInvoiceDescription: str
    Quantity: int
    Value: float
    OriginCountryIsoCode: str
    Weight: float
    CustomsTariffNumber: str
    Key: Optional[str] = None
    GoodsTransitCertificate: Optional[str] = None
    GoodsTransitCertificateNumber: Optional[str] = None
    ExportLicenceNumber: Optional[str] = None
    ExportLicenceDate: Optional[str] = None


class CollectionTimeWindow(BaseModel):
    From: str
    To: str


class Collection(BaseModel):
    ContactPerson: str
    Address: str
    Postcode: str
    City: str
    CountryISOCode: str
    StateISOCode: Optional[str] = None
    CollectionDate: str
    CollectionTimeWindow: CollectionTimeWindow
    CollectionInstructions: Optional[str] = None


class NotificationEvents(BaseModel):
    MailpieceRegisteredAtPartner: Optional[bool] = None
    MailpiecePassedToPartner: Optional[bool] = None
    NewEstimatedDeliveryTime: Optional[bool] = None
    UnexpectedEvent: Optional[bool] = None
    MailpieceDelivered: Optional[bool] = None


class Notification(BaseModel):
    EMailAddresses: list[str]
    NotificationLanguage: str
    NotificationEvents: NotificationEvents


class Waybill(BaseModel):
    DispatchDate: str
    FrankingLicence: int
    CostCenter: Optional[str] = None
    Addresses: list[Address]
    RecipientOrSenderAddressIsIdenticalToInvoiceAddress: bool
    Product: str
    AuxiliaryServices: Optional[list[str]] = None
    IsPalletised: Optional[bool] = None
    ParcelsAmount: int
    GrossWeight: float
    NatureOfContent: str
    CommercialInvoiceType: Optional[str] = None
    CommercialInvoiceDescription: Optional[str] = None
    CurrencyISOCode: str
    DeliveredDutiesPaid: Optional[str] = None
    CustomerReference: Optional[str] = None
    NonDeliveryInstruction: Optional[str] = None
    SpecialDeliveryInstruction: Optional[str] = None
    SignatureId: Optional[str] = None
    DocumentIds: Optional[list[str]] = None
    UrgentServiceType: Optional[str] = None
    WaybillFormat: Optional[str] = None
    PriceType: Optional[str] = None
    OriginDeclarationLanguage: str
    Articles: list[Article]
    Collection: Optional[Collection] = None
    Notification: Optional[Notification] = None
    ThisIsATestEntry: Optional[bool] = None
