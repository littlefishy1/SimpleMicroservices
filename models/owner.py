from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, StringConstraints

from .company import CompanyBase

# Columbia UNI: 2–3 lowercase letters + 1–4 digits (e.g., abc1234)
UNIType = Annotated[str, StringConstraints(pattern=r"^[a-z]{2,3}\d{1,4}$")]


class OwnerBase(BaseModel):
    ssn: int = Field(
        ...,
        description="SSN of the owner",
        json_schema_extra={"example": "917260053"},
    )
    first_name: str = Field(
        ...,
        description="Given name.",
        json_schema_extra={"example": "Clara"},
    )
    last_name: str = Field(
        ...,
        description="Family name.",
        json_schema_extra={"example": "Green"},
    )
    email: EmailStr = Field(
        ...,
        description="Primary email address.",
        json_schema_extra={"example": "apple@gmail.com"},
    )
    phone: Optional[str] = Field(
        None,
        description="Contact phone number in any reasonable format.",
        json_schema_extra={"example": "+1-718-555-0053"},
    )
    birth_date: Optional[date] = Field(
        None,
        description="Date of birth (YYYY-MM-DD).",
        json_schema_extra={"example": "1999-12-10"},
    )

    # Embed companies (each with persistent ID)
    Companies: List[CompanyBase] = Field(
        default_factory=list,
        description="Companies linked to this owner (each carries a persistent EIN).",
        json_schema_extra={
            "example": [
                {
                    "ein": "923345678",
                    "name": "Lucky Deli",
                    "street": "117 Broadway",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10027",
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ssn": "917260053",
                    "first_name": "Clara",
                    "last_name": "Green",
                    "email": "apple@google.com",
                    "phone": "+1-718-555-0053",
                    "birth_date": "1999-12-10",
                    "companies": [
                        {
                            "ein": "923345678",
                            "name": "Lucky Deli",
                            "street": "117 Broadway",
                            "city": "New York",
                            "state": "NY",
                            "postal_code": "10027",
                        }
                    ],
                }
            ]
        }
    }


class OwnerCreate(OwnerBase):
    """Creation payload for an Owner."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ssn": "xy123",
                    "first_name": "Jack",
                    "last_name": "Reed",
                    "email": "123@gmail.com",
                    "phone": "+1-347-222-2308",
                    "birth_date": "2002-12-09",
                    "companies": [
                        {
                            "ein": "922345776",
                            "name": "Great Bakery",
                            "street": "112 Main St",
                            "city": "New York",
                            "state": "NY",
                            "postal_code": "10028",
                        }
                    ],
                }
            ]
        }
    }

class OwnerRead(OwnerBase):
    """Server representation returned to clients."""
    ssn: int = Field(
        description="ssn of owner",
        json_schema_extra={"example": "924236756"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ssn": "924236756",
                    "first_name": "Clara",
                    "last_name": "Green",
                    "email": "apple@google.com",
                    "phone": "+1-718-555-0053",
                    "birth_date": "1999-12-10",
                    "companies":[
                        {
                            "ein": "923345678",
                            "name": "Lucky Deli",
                            "street": "117 Broadway",
                            "city": "New York",
                            "state": "NY",
                            "postal_code": "10027",
                        }
                    ],
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
