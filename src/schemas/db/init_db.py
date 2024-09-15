from .config_db import engine
from .models import EmployeeORM, OrganizationORM, TenderORM, BidORM, BidReviewsORM

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(EmployeeORM.metadata.create_all)
        await conn.run_sync(OrganizationORM.metadata.create_all)
        await conn.run_sync(TenderORM.metadata.create_all)
        await conn.run_sync(BidORM.metadata.create_all)
        await conn.run_sync(BidReviewsORM.metadata.create_all)