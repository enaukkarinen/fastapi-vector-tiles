from typing import Never

import mercantile
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.db.database import async_get_db
from app.models.title_boundary import TitleBoundary
from app.models.title_boundary_response import TitleBoundaryResponse

router = APIRouter(tags=["vectors"])


@router.get(
    "/vectors/{z}/{x}/{y}.png",
    tags=["vectors"],
    response_model=list[TitleBoundaryResponse],
)
async def get(z: str, x: str, y: str, db: AsyncSession = Depends(async_get_db)):
    """Retrieve title boundaries for a given tile coordinate.

    Args:
        z (str): Zoom level of the tile.
        x (str): X coordinate of the tile.
        y (str): Y coordinate of the tile.
        db (AsyncSession, optional): Database session dependency. Defaults to Depends(async_get_db).

    Returns:
        List[TitleBoundary]: List of title boundaries that intersect with the specified tile.

    Raises:
        HTTPException: If no title boundaries are found (404) or if a database query fails (500).

    """

    def raise_http_exception(status_code: int, detail: str) -> Never:
        raise HTTPException(status_code=status_code, detail=detail)

    try:
        bbox = mercantile.bounds(int(x), int(y), int(z))
        query = select(TitleBoundary).filter(
            TitleBoundary.geometry.st_intersects(
                func.ST_MakeEnvelope(bbox[0], bbox[1], bbox[2], bbox[3], 4326)
            )
        )
        result = await db.execute(query)
        title_boundaries = result.scalars().all()

        if not title_boundaries:
            raise_http_exception(status_code=404, detail="No title boundaries found")
        else:
            return title_boundaries
    except SQLAlchemyError as e:
        # Handle any SQLAlchemy related error
        raise_http_exception(status_code=500, detail=f"Database query failed: {e!s}")

    except Exception as e:  # noqa: BLE001
        # Catch all other exceptions
        raise_http_exception(
            status_code=e.status_code, detail=f"An unexpected error occurred: {e!s}"
        )
    # Create the query

    # .filter(
    #     TitleBoundary.geometry.st_intersects(
    #         func.ST_MakeEnvelope(bbox[0], bbox[1], bbox[2], bbox[3], 4326)
    #     )

    # )

    # image_path = "app/routers/img.png"  # Replace with the path to your PNG file
    # if os.path.exists(image_path):
    #     return FileResponse(image_path, media_type="image/png")
    # else:
    #     return {"error": "Image not found"}
    # return {"bbox": bbox}
