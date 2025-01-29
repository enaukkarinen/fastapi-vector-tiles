from fastapi import APIRouter, Depends
from ..core.db.database import async_get_db
import mercantile
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession

router = APIRouter(tags=["vectors"])


@router.get("/vectors/{x}/{y}/{z}", tags=["vectors"])
async def get(x, y, z, db: AsyncSession = Depends(async_get_db)):
    print(x, y, z)
    bbox = mercantile.bounds(486, 332, 10)  # TODO: use x, y, z
    response = await db.execute(text("SELECT * FROM title_boundary LIMIT 5"))
    boundaries = response.fetchall()
    print(boundaries)
    return {"bbox": bbox}
