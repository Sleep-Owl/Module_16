from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root() -> dict:
    return {'message': 'Главная страница'}


@app.get('/user/admin')
async def admin() -> dict:
    return {'message': 'Вы вошли как администратор'}


@app.get('/user/{user_id}')
async def user(user_id: int) -> dict:
    return {'message': f'Вы вошли как пользователь № {user_id}'}


@app.get('/user')
async def user_info(user_name: str, user_age: int) -> dict:
    return {'message': f'Информация о пользователе. Имя: {user_name}, Возраст: {user_age}'}
