from fastapi import APIRouter, Response, HTTPException, Path, Query, Depends
from shemas.User import User
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
)
from typing import Annotated
from faker import Faker
from functools import lru_cache
from typing import Generator
from string import ascii_letters, digits, punctuation
from secrets import choice

router_users = APIRouter(tags=["Users"], prefix="/users")


def generate_password(lenght: int = 12) -> str:
    charset = ascii_letters + digits + punctuation
    return "".join([choice(charset) for _ in range(lenght)])


def create_fake_users(number: int) -> Generator[User, None, None]:
    faker: Faker = Faker()
    return (
        User(
            id=i,
            name=faker.name(),
            username=faker.user_name(),
            email=faker.email(),
            address=faker.address(),
            phone=faker.phone_number(),
            password=generate_password(lenght=14),
            disabled=False,
        )
        for i in range(1, number + 1)
    )


@lru_cache(maxsize=1000)
def get_cached_users() -> list[User]:
    return list(create_fake_users(500))


def get_user_by_id(id: int, users: list[User]) -> User:
    return next((user for user in users if user.id == id), None)


def get_user_by_username(username: str, users: list[User]) -> User:
    return next((user for user in users if user.username == username), None)


async def get_user(id: int = 1, users: list[User] = Depends(get_cached_users)) -> User:
    user: User = get_user_by_id(id, users)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router_users.get("/", response_model=list[User])
async def read_users(
    offset: int = 0,
    limit: Annotated[int, Query(title="limit of users to return", ge=5)] = 10,
    users: list[User] = Depends(get_cached_users),
):
    return users[offset : offset + limit]


@router_users.get("/filtered/", response_model=list[User])
async def read_user_filtered(
    name: Annotated[
        str | None, Query(title="The name of the user", min_length=4, max_length=50)
    ] = None,
    email: Annotated[
        str | None, Query(title="The email of te user", min_length=4, max_length=50)
    ] = None,
    username: Annotated[str, Query(title="The username of the user")] = None,
    users: list[User] = Depends(get_cached_users),
):
    if filtered_users := [
        user
        for user in users
        if user.name == name or user.email == email or user.username == username
    ]:
        return filtered_users

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")


@router_users.get("/{id}", response_model=User)
async def read_user_by_id(
    id: Annotated[int, Path(title="The ID of the user to get", ge=1, le=500)],
    user: User = Depends(get_user),
):
    return user


@router_users.post(
    "/create/",
    response_class=Response(status_code=HTTP_201_CREATED),
    response_description="User created successfully",
)
async def create_user(user: User, users: list[User] = Depends(get_cached_users)):
    print(user)
    users.append(user)
    return Response(status_code=HTTP_201_CREATED, content="User created successfully")


@router_users.delete(
    "/delete/{id}", response_class=Response(status_code=HTTP_204_NO_CONTENT)
)
async def delete_user(
    id: Annotated[int, Path(title="The ID of the user to delete", ge=1)],
    users: list[User] = Depends(get_cached_users),
    user_to_delete: User = Depends(get_user),
):
    print(user_to_delete)
    users.remove(user_to_delete)

    return Response(status_code=HTTP_204_NO_CONTENT)


@router_users.put(
    "/update/{id}",
    response_class=Response(
        status_code=HTTP_200_OK,
    ),
    response_description="User updated successfully",
)
async def update_user(
    id: Annotated[int, Path(title="The ID of the user to update", ge=1)],
    new_data: User,
    user_to_update: User = Depends(get_user),
):
    user: User = user_to_update
    for key, value in new_data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    return Response(status_code=HTTP_200_OK, content="User updated successfully")
