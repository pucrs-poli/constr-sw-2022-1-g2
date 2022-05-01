from typing import Optional, List
from urllib import response

import requests
from fastapi import FastAPI, Response, status, Form, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel

REALM = "master"
BASE_API_URL = "http://localhost:8000"
BASE_KEYCLOAK_URL = "http://localhost:8080"
TOKEN_URL = "http://localhost:8080/auth/realms/master/protocol/openid-connect/token"

class LoginRequest(BaseModel):
    client_id: Optional[str]
    client_secret: Optional[str]
    username: Optional[str]
    password: Optional[str]
    grant_type: Optional[str]

class LoginResponse(BaseModel):
    token_type: Optional[str]
    access_token: Optional[str]
    expires_in: Optional[str]
    refresh_token: Optional[str]
    referesh_expires_in: Optional[int]

class User(BaseModel):
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    enable: Optional[bool]

class UserResponse(BaseModel):
    id: str
    username: str


app = FastAPI()


@app.get("/")
async def read_root():
    item = {"Hello": "World"}
    return item

@app.post("/login", response_model=LoginResponse)
async def login(client_id: str = Form(...), username: str = Form(...),
                password: str = Form(...), grant_type: str = Form(...), response: Response = 200):

    header = {"Content-Type": "application/x-www-form-urlencoded"}
    
    body = {"client_id": client_id, "username": username,
        "password": password, "grant_type": grant_type}

    try:
        r = requests.post(url=TOKEN_URL, headers=header, data=body,
                         timeout=3)
    except:
        print("ferrou no login")
        response.status = status.HTTP_500_INTERNAL_SERVER_ERROR
    response_json = r.json()
    return response_json


@app.post("/users", response_model = UserResponse)
async def create_user(authorization: str = Header(None), user: User = str):
    responde = {"id": "teste1234",
    "username": "abaco alado"}
    print(authorization)
    #TO-DO logica
    return responde


@app.get("/users", response_model = List[User])
async def get_all_users(authorization: str = Header(None)):
    # To-do logica
    return [{"username": "Kevin", "enable": True}, {"username": "vitor", "enable": True}]


@app.get("/users/{id}", response_model=User)
async def get_user_by_id(id: int):
    #To-do logica
    print(id)
    return {"username": "vitor", "enable": True}


@app.put("/users/{id}")
async def update_user(id: int, authorization: str = Header(None), user: User = None):
    #To-do logica
    print(id)
    print(authorization)
    print(user)

    return {"username": "vitor", "enable": True}


@app.patch("/users/{id}")
async def update_user_password(id: int, authorization: str = Header(None), user: User = None):
    #To-do logica
    print(id)
    print(authorization)
    print(user)
    return {"username": "vitor", "enable": True}


@app.delete("/users/{id}")
async def delete_user(id: int, authorization: str = Header(None)):
    #To-do logica
    return status.HTTP_204_NO_CONTENT