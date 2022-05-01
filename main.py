from typing import Optional

from fastapi import FastAPI

REALM = ""
BASE_API_URL = ""
BASE_KEYCLOAK_URL = ""


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("{BASE_API_URL}/login")
def login():
    pass


@app.post("{BASE_API_URL}/users")
def create_user():
    pass


@app.get("{BASE_API_URL}/users")
def get_all_users():
    pass


@app.get("{BASE_API_URL}/users/{id}")
def get_user_by_id(user_id: int):
    pass


@app.put("{BASE_API_URL}/users/{id}")
def update_user(user_id: int):
    pass


@app.patch("{BASE_API_URL}/users/{id}")
def update_user_password(user_id: int):
    pass


@app.delete("{BASE_API_URL}/users/{id}")
def delete_user(user_id: int):
    pass
