from fastapi import APIRouter, status
router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def create_server():
    return {'message': 'hello world fromapi'}
