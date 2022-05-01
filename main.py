from typing import Optional

from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

REALM = ""
BASE_API_URL = "http://localhost:8000"
BASE_KEYCLOAK_URL = ""

class LoginRequest(BaseModel):
    client_id: str
    username: str
    password: str
    grant_type: str

class LoginResponse(BaseModel):
    token_type: str
    access_token: str
    expires_in: str
    refresh_token: str
    referesh_expires_in: int


app = FastAPI()


@app.get("/")
def read_root():
    item = {"Hello": "World"}
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/login", response_model=LoginResponse)
def login(body: LoginRequest):
    # resp_keycloak = fetch(url_keycloak)
    #return LoginResponse
    pass


@app.post("/users")
def create_user():
    return {"Hello": "Kevin"}


@app.get("/users")
def get_all_users():
    return {"Hello": "Kevin"}


@app.get("/users/{id}")
def get_user_by_id(user_id: int):
    pass


@app.put("/users/{id}")
def update_user(user_id: int):
    pass


@app.patch("/users/{id}")
def update_user_password(user_id: int):
    pass


@app.delete("/users/{id}")
def delete_user(user_id: int):
    pass
