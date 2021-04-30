from api.database.database import MSSQLConnection
from pydantic import BaseModel
from datetime import date, datetime
from loguru import logger
from typing import TypeVar, List, Tuple, Any, Union, Type

T = TypeVar('T', bound=BaseModel)

class General_Response(BaseModel):
    success: bool
    data: Union[str, None] = None

class Address_Read_Procedure_Response(BaseModel):
    id: int
    line1: str
    line2: str
    city: str
    province: str
    postcode: str
    latitude: float
    longitude: float
    geohash: str
    created_at: datetime

class Locations_Read_Procedure_Response(BaseModel):
    id: int
    name: str
    organization: str
    phone: str
    notes: str
    address: int
    active: int
    postcode: str
    created_at: datetime

class Entries_Read_Procedure_Response(BaseModel):
    id: int
    numberAvaliable: int
    numberTotal: int
    date: date
    location: int
    vaccine: int
    inputType: int
    tags_optional: str
    tags_required: str
    created_at: datetime

class Organizations_Read_Procedure_Response(BaseModel):
    id: int
    full_name: str
    short_name: str
    description: str
    created_at: datetime

class Organizations_Create_Procedure_Request(BaseModel):
    full_name: str
    short_name: str
    description: str

class Locations_Response(BaseModel):
    id: int
    name: str
    organization: str
    phone: str
    notes: str
    address: Address_Read_Procedure_Response
    active: int
    postcode: str
    created_at: datetime

class Entries_Response(BaseModel):
    id: int
    numberAvaliable: int
    numberTotal: int
    date: date
    location: Locations_Response
    vaccine: int
    inputType: int
    tags_optional: str
    tags_required: str
    created_at: datetime


def convert_to_pydantic(model: Type[T], rows: List[Tuple[Any, ...]]) -> List[T]:
    pydantic_rows = []

    for r in rows:
        fields = {
            f: i for f, i
            in zip(model.__fields__, r)
        }
        pydantic_rows.append(model(**fields))

    return pydantic_rows

class Addresses:
    def __init__(self, db: MSSQLConnection):
        self._db = db
    
    async def get_address_by_id(self, address_id: int) -> Union[Address_Read_Procedure_Response, None]:
        row = await self._db.fetch_one(f"""
                EXEC dbo.address_Read @addressID = {address_id}
            """)

        if row is not None:
            address_response: Address_Read_Procedure_Response = convert_to_pydantic(Address_Read_Procedure_Response, [row])[0]
            
            return address_response
        return None

    async def get_addresses(self, postal_code: str) -> List[Address_Read_Procedure_Response]:
        rows = await self._db.fetch_all(f"""
                SELECT
                    {','.join(list(Address_Read_Procedure_Response.__fields__.keys()))}
                FROM dbo.address
            """)

        pydantic_rows: List[Address_Read_Procedure_Response] = convert_to_pydantic(Address_Read_Procedure_Response, rows)

        return pydantic_rows

class Locations:
    def __init__(self, db: MSSQLConnection):
        self._db = db

    async def get_location_by_id(self, location_id: int) -> Locations_Response:
        row = await self._db.fetch_one(f"""
                EXEC dbo.locations_Read @locationID = {location_id}
            """)
        
        if row is not None:
            locations_response: Locations_Read_Procedure_Response = convert_to_pydantic(Locations_Read_Procedure_Response, [row])[0]
            locations_response.address = await Addresses(self._db).get_address_by_id(locations_response.address)
            
            return locations_response
        return None

    async def get_locations(self, postal_code: str) -> List[Locations_Response]:
        rows = await self._db.fetch_all(f"""
                SELECT
                    {','.join(list(Locations_Read_Procedure_Response.__fields__.keys()))}
                FROM dbo.locations
            """)

        rows: List[Locations_Read_Procedure_Response] = convert_to_pydantic(Locations_Read_Procedure_Response, rows)

        # should be done all at once instead of in a for loop
        for r in rows:
            r.address = await Addresses(self._db).get_address_by_id(r.address)

        return rows

class Entries:
    def __init__(self, db: MSSQLConnection):
        self._db = db
    
    async def get_entry_by_id(self, entry_id) -> Entries_Response:
        row = await self._db.fetch_one(f"""
                EXEC dbo.entries_Read @entryID = {entry_id}
            """)

        if row is not None:
            entry_response: Entries_Read_Procedure_Response = convert_to_pydantic(Entries_Read_Procedure_Response, [row])[0]
            entry_response.location = await Locations(self._db).get_location_by_id(entry_response.location)
            
            return entry_response
        return None

    async def get_entries(self, postal_code: str) -> List[Entries_Response]:
        rows = await self._db.fetch_all(f"""
                SELECT
                    {','.join(list(Entries_Read_Procedure_Response.__fields__.keys()))}
                FROM dbo.entries
            """)

        rows: List[Entries_Read_Procedure_Response] = convert_to_pydantic(Entries_Read_Procedure_Response, rows)
        
        # should be done all at once instead of in a for loop
        for r in rows:
            r.location = await Locations(self._db).get_location_by_id(r.location)

        return rows

class Organizations:
    def __init__(self, db: MSSQLConnection):
        self._db = db
    
    async def get_organization_by_id(self, organization_id: int) -> Organizations_Read_Procedure_Response:
        row = await self._db.fetch_one(f"""
                EXEC dbo.organizations_Read @organizationID = {organization_id}
            """)
        
        if row is not None:
            organizations_response: Organizations_Read_Procedure_Response = convert_to_pydantic(Organizations_Read_Procedure_Response, [row])[0]
            
            return organizations_response
        return None

    async def get_organizations(self, name: str) -> List[Organizations_Read_Procedure_Response]:
        rows = await self._db.fetch_all(f"""
                SELECT
                    {','.join(list(Organizations_Read_Procedure_Response.__fields__.keys()))}
                FROM dbo.organizations
            """)

        rows: List[Organizations_Read_Procedure_Response] = convert_to_pydantic(Organizations_Read_Procedure_Response, rows)

        return rows

    async def create_organization(
        self,
        full_name: str,
        short_name: str,
        description: str
    ) -> Union[Organizations_Read_Procedure_Response, None]:
        await self._db.execute_stored_procedure(query="""
                EXEC [dbo].[organizations_Create]
                    @full_name=?,
                    @short_name=?,
                    @description=?;
            """, values=(full_name, short_name, description)
            )
