from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class CompanyBase(BaseModel):
    EIN: int = Field(
        description="Employer Identification Number",
        json_schema_extra={"example": "923345678"},
    )
    name: str = Field(
        ...,
        description="Company Name.",
        json_schema_extra={"example": "Lucky Deli"},
    )
    street: str = Field(
        ...,
        description="Street address and number.",
        json_schema_extra={"example": "117 Broadway"},
    )
    city: str = Field(
        ...,
        description="City or locality.",
        json_schema_extra={"example": "New York"},
    )
    state: Optional[str] = Field(
        None,
        description="State/region code if applicable.",
        json_schema_extra={"example": "NY"},
    )
    postal_code: Optional[str] = Field(
        None,
        description="Postal or ZIP code.",
        json_schema_extra={"example": "10027"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ein": "923345678",
                    "name": "Lucky Deli",
                    "street": "117 Broadway",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10027",
                }
            ]
        }
    }


class CompanyCreate(CompanyBase):
    """Creation payload; Based on what is given"""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ein": "922345776",
                    "name": "Great Bakery",
                    "street": "112 Main St",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10028",
                }
            ]
        }
    }


class CompanyUpdate(BaseModel):
    """Partial update; EIN and name is taken from the path, not the body."""
    street: Optional[str] = Field(
        None, description="Street address and number.", json_schema_extra={"example": "112 Main St"}
    )
    city: Optional[str] = Field(
        None, description="City or locality.", json_schema_extra={"example": "New York"}
    )
    state: Optional[str] = Field(
        None, description="State/region code if applicable.", json_schema_extra={"example": "NY"}
    )
    postal_code: Optional[str] = Field(
        None, description="Postal or ZIP code.", json_schema_extra={"example": "10027"}
    )


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "street": "112 Main St",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10002",
                },
                {"city": "Queens"},
            ]
        }
    }


class CompanyRead(CompanyBase):
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
                    "ein": "923345678",
                    "name": "Lucky Deli",
                    "street": "112 Main St",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10028",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
