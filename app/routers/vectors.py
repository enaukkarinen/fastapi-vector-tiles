from fastapi import APIRouter

router = APIRouter(tags=["vectors"])


@router.get("/vectors", tags=["vectors"])
async def get():
    return {"token_type": "bearer"}
