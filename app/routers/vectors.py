from fastapi import APIRouter, Depends, HTTPException
from ..core.db.database import async_get_db
import mercantile
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio.session import AsyncSession
from ..models.title_boundary import TitleBoundary
from ..models.title_boundary_response import TitleBoundaryResponse

router = APIRouter(tags=["vectors"])


@router.get(
    "/vectors/{z}/{x}/{y}", tags=["vectors"], response_model=list[TitleBoundaryResponse]
)
async def get(z, x, y, db: AsyncSession = Depends(async_get_db)):
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
            raise HTTPException(status_code=404, detail="No title boundaries found")

        return title_boundaries
    except SQLAlchemyError as e:
        # Handle any SQLAlchemy related error
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

    except Exception as e:
        # Catch all other exceptions
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
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
