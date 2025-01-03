from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users_db = {'1': 'Имя: Example, возраст: 18'}


@app.get('/user')
async def get_all_users() -> dict:
    return users_db


@app.post('/user/{username}/{age}')
async def add_user(username: Annotated[str, Path(
    min_length=5, max_length=20, description='Enter username', example='UrbanUser'
)], age: int = Path(
    ge=18, le=120, description='Enter age', example='24'
)) -> str:
    try:
        user_id = str(int(max(users_db, key=int)) + 1)
        users_db[user_id] = f'Имя: {username}, возраст: {age}'
        return f'User {user_id} is registered'
    except ValueError:
        users_db[1] = f'Имя: {username}, возраст: {age}'
        return f'User 1 is registered'


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id, username: Annotated[str, Path(
    min_length=5, max_length=20, description='Enter username', example='UrbanUser'
)], age: int = Path(
    ge=18, le=120, description='Enter age', example='24'
)) -> str:
    users_db[user_id] = f'Имя: {username}, возраст: {age}'
    return f'The user {user_id} is updated'


@app.delete('/user/{user_id}')
async def delete_user(user_id):
    users_db.pop(user_id)
    pass
