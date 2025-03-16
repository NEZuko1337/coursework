from fastapi import APIRouter, Depends, status

from src.backend.middlewares.auth import auth_user

router = APIRouter(dependencies=[Depends(auth_user)])


@router.get("/", status_code=status.HTTP_200_OK)
async def hello():
    return {'message': 'hello world from api'}
