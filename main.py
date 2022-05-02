from http import client
import json
from fastapi.encoders import jsonable_encoder
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
    username: Optional[str] = ""
    email: Optional[str] = ""
    firstName: Optional[str] = ""
    lastName: Optional[str] = ""
    enabled: Optional[bool] = True

class UserResponse(BaseModel):
    id: str
    username: str


app = FastAPI()


@app.get("/")
async def read_root():
    item = {"Hello": "World"}
    return item

@app.post("/login", response_model=LoginResponse)
async def login(client_id: str = Form(...), username: str = Form(...), client_secret: str = Form(...),
                password: str = Form(...), grant_type: str = Form(...), response: Response = 200):

    header = {"Content-Type": "application/x-www-form-urlencoded"}
    
    body = {"client_id": client_id, "username": username,
        "password": password, "grant_type": grant_type, "client_secret": client_secret}

    try:
        r = requests.post(url=TOKEN_URL, headers=header, data=body,
                         timeout=3)
    except:
        print("ferrou no login")
        response.status = status.HTTP_500_INTERNAL_SERVER_ERROR
    response_json = r.json()
    return response_json


@app.post("/users", status_code=201)
async def create_user(authorization: str = Header(None), user: User = str):

    data = jsonable_encoder(user)

    header = {"Authorization": authorization, "Content-Type": "application/json"}
    r = requests.post(url= BASE_KEYCLOAK_URL + "/auth/admin/realms/master/users", headers=header, data=json.dumps(data),
                        timeout=3)
    # falta response code se já tiver criado um user
    return status.HTTP_204_NO_CONTENT


@app.get("/users")
async def get_all_users(authorization: str = Header(None)):
    # To-do logica
    header = {"Authorization": authorization}
    r = requests.get(url= BASE_KEYCLOAK_URL + "/auth/admin/realms/master/users", headers=header,
                        timeout=3)

    response_json = r.json()

    return response_json


@app.get("/users/{id}")
async def get_user_by_id(id: str, authorization: str = Header(None)):
    header = {"Authorization": authorization}
    r = requests.get(url= BASE_KEYCLOAK_URL + "/auth/admin/realms/master/users/" + id, headers=header,
                        timeout=3)

    response_json = r.json()

    return response_json


@app.put("/users/{id}")
async def update_user(id: str, authorization: str = Header(None), user: User = None):
    data = jsonable_encoder(user)

    header = {"Authorization": authorization, "Content-Type": "application/json"}
    r = requests.put(url= BASE_KEYCLOAK_URL + "/auth/admin/realms/master/users/" + id, headers=header, data=json.dumps(data),
                        timeout=3)

    return status.HTTP_204_NO_CONTENT


@app.patch("/users/{id}")
async def update_user_password(id: str, authorization: str = Header(None), password: dict = {}):
    
    data = jsonable_encoder(password)
    header = {"Authorization": authorization, "Content-Type": "application/json"}
    r = requests.put(url= BASE_KEYCLOAK_URL + "/auth/admin/realms/master/users/" + id + "/reset-password", headers=header, data=json.dumps(data),
                        timeout=3)

    return status.HTTP_204_NO_CONTENT


@app.delete("/users/{id}")
async def delete_user(id: str, authorization: str = Header(None)):
    #To-do logica
    header = {"Authorization": authorization}
    r = requests.delete(url= BASE_KEYCLOAK_URL + "/auth/admin/realms/master/users/" + id, headers=header,
                        timeout=3)

    #response_json = r.json()

    return status.HTTP_204_NO_CONTENT