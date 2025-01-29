from fastapi import APIRouter

import mercantile

router = APIRouter(tags=["vectors"])

@router.get("/vectors/{x}/{y}/{z}", tags=["vectors"])
async def get(x, y, z):
    print(x, y, z)
    bbox = mercantile.bounds(486, 332, 10) # TODO: use x, y, z
    return {"bbox": bbox}
