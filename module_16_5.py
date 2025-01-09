from fastapi import FastAPI, Path, HTTPException, Request
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)
templates = Jinja2Templates(directory="templates")

users_db = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users_db})


@app.get('/user/{user_id}', response_class=HTMLResponse)
async def user_details(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users_db[user_id]})
    except KeyError:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@app.post('/user/{username}/{age}')
async def add_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: int = Path(ge=18, le=120, description='Enter age', example='24')) -> User:
    user_id = max((u.id for u in users_db), default=0) + 1
    new_user = User(id=user_id, username=username, age=age)
    users_db.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
        user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')],
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: int = Path(ge=18, le=120, description='Enter age', example='24')) -> User:
    for i, user in enumerate(users_db):
        if user.id == user_id:
            users_db[i].username = username
            users_db[i].age = age
            return users_db[i]
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: int = Path(ge=1, le=100, description='Enter User ID', example='1')) -> User:
    for i, user in enumerate(users_db):
        if user.id == user_id:
            del_user = users_db[i]
            del users_db[i]
            return del_user
    raise HTTPException(status_code=404, detail='User was not found')
