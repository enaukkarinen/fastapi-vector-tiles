from fastapi import APIRouter

router = APIRouter(tags=["vectors"])


@router.get("/vectors/{x}/{y}/{z}", tags=["vectors"])
async def get(x, y, z):
    return {x, y, z}
