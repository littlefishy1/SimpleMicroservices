from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.owner import OwnerCreate, OwnerRead
from models.company import CompanyCreate, CompanyRead

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------

owners: Dict[int, OwnerRead] = {}
companies: Dict[int, CompanyRead] = {}

app = FastAPI(
    title="Owner/Company API",
    description="Demo FastAPI app using Pydantic v2 models for Owner and Company",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Address endpoints
# -----------------------------------------------------------------------------

@app.post("/companies", response_model=CompanyRead, status_code=201)
def create_company(company: CompanyCreate):
    if company.EIN in companies:
        raise HTTPException(status_code=400, detail="Company with this EIN already exists")
    companies[company.EIN] = CompanyRead(**company.model_dump())
    return companies[company.EIN]

@app.get("/companies", response_model=List[CompanyRead])
def list_companies(
    name: Optional[str] = Query(None, description="Filter by name"),
    street: Optional[str] = Query(None, description="Filter by street"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state/region"),
    postal_code: Optional[str] = Query(None, description="Filter by postal code"),
):
    results = list(companies.values())

    if name is not None:
        results = [a for a in results if a.name == name]
    if street is not None:
        results = [a for a in results if a.street == street]
    if city is not None:
        results = [a for a in results if a.city == city]
    if state is not None:
        results = [a for a in results if a.state == state]
    if postal_code is not None:
        results = [a for a in results if a.postal_code == postal_code]


    return results

@app.get("/companies/{company_ein}", response_model=CompanyRead)
def get_company(company_ein: int):
    if company_ein not in companies:
        raise HTTPException(status_code=404, detail="Company not found")
    return companies[company_ein]

@app.put("/companies/{company_ein}", response_model=CompanyRead)
def update_company(company_ein: int):
    company = CompanyCreate(company_ein)
    companies[company_ein] = CompanyRead(**company.model_dump())
    return companies[company_ein]

@app.delete("/companies/{company_ein}", response_model=OwnerRead)
def delete_company(company_ein: int):
    if company_ein not in companies:
        raise HTTPException(status_code=404, detail="Company not found")
    del companies[company_ein]
# -----------------------------------------------------------------------------
# Person endpoints
# -----------------------------------------------------------------------------
@app.post("/owner", response_model=OwnerRead, status_code=201)
def create_owner(owner: OwnerCreate):
    # Each owner gets its own UUID; stored as OwnerRead
    owner_read = OwnerRead(**owner.model_dump())
    owners[owner_read.ssn] = owner_read
    return owner_read

@app.get("/owners", response_model=List[OwnerRead])
def list_owners(
    ssn: Optional[str] = Query(None, description="Filter by ssn"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
    city: Optional[str] = Query(None, description="Filter by city of at least one address"),
):
    results = list(owners.values())

    if ssn is not None:
        results = [p for p in results if p.ssn == ssn]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]

    # nested address filtering
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.Companies)]

    return results

@app.get("/owners/{owner_ein}", response_model=OwnerRead)
def get_owner(owner_ssn: int):
    if owner_ssn not in owners:
        raise HTTPException(status_code=404, detail="Owner not found")
    return owners[owner_ssn]

@app.put("/owners/{owner_ein}", response_model=OwnerRead)
def update_owner(owner_ssn: int):
    owner = OwnerCreate(owner_ssn)
    owners[owner_ssn] = OwnerRead(**owner.model_dump())
    return owners[owner_ssn]

@app.delete("/owners/{owner_ssn}", response_model=OwnerRead)
def delete_owner(owner_ssn: int):
    if owner_ssn not in owners:
        raise HTTPException(status_code=404, detail="Owner not found")
    del owners[owner_ssn]
    

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Owner/Company API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
