from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from app.containers import Container
from app.exceptions.errors import BaseError
from app.schemas.request.user import CreateUserInRequest
from app.schemas.response.user import UserGetResponse, UsersListResponse
from app.selectors.user_selectors import UserSelector
from app.services.user_service import CreateUserService

router = APIRouter(prefix='/v1/users')


@router.get('/', response_model=UsersListResponse)
@inject
async def get_user_list(user_selector: UserSelector = Depends(Provide[Container.user_selector])) -> UsersListResponse:
    return UsersListResponse(users=[user async for user in user_selector.list()])


@router.get('/{user_id}', response_model=UserGetResponse)
@inject
async def get_user(
    user_id: int, user_selector: UserSelector = Depends(Provide[Container.user_selector])
) -> UserGetResponse:
    try:
        return await user_selector.get(user_id=user_id)
    except BaseError as _:
        raise HTTPException(status_code=404) from _


@router.post('/', response_model=UserGetResponse)
@inject
async def create_user(
    body: CreateUserInRequest, user_create_service: CreateUserService = Depends(Provide[Container.create_user_service])
) -> UserGetResponse:
    return await user_create_service(create_user=body)
