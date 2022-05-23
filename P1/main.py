from email import header
import os
import json
import requests
from typing import Optional
from urllib import response
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Response, status, Form, Header

########### ENVIRONMENT VARS ###########
#IP = os.getenv("KEYCLOAK_IP")
IP = "localhost"
#PORT = os.getenv("KEYCLOAK_PORT")
PORT = "8080"
BASE_KEYCLOAK_URL = "http://" + IP + ":" + PORT

#REALM = os.getenv("KEYCLOAK_REALM")
REALM = "master"
TOKEN_URL = (
    BASE_KEYCLOAK_URL + "/auth/realms/" + REALM + "/protocol/openid-connect/token"
)
USERS_URL = BASE_KEYCLOAK_URL + "/auth/admin/realms/" + REALM + "/users"
#########################################


class User(BaseModel):
    username: Optional[str] = ""
    email: Optional[str] = ""
    firstName: Optional[str] = ""
    lastName: Optional[str] = ""
    enabled: Optional[bool] = True


app = FastAPI()


@app.get("/")
async def read_root():
    item = {"Hello": "World"}
    return item


@app.post("/login")
async def login(
    client_id: str = Form(...),
    username: str = Form(...),
    client_secret: str = Form(...),
    password: str = Form(...),
    grant_type: str = Form(...),
    response: Response = 200,
):
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "client_id": client_id,
        "username": username,
        "password": password,
        "grant_type": grant_type,
        "client_secret": client_secret,
    }
    r = requests.post(url=TOKEN_URL, headers=header, data=body)
    response_json = r.json()
    return response_json


@app.post("/users", status_code=201)
async def create_user(authorization: str = Header(None), user: User = str):
    data = jsonable_encoder(user)
    header = {"Authorization": authorization, "Content-Type": "application/json"}
    r = requests.post(
        url=USERS_URL,
        headers=header,
        data=json.dumps(data),
    )
    # falta response code se já tiver criado um user

    #payload = find_by_username(authorization=authorization,username=user.username)

    return status.HTTP_201_CREATED


@app.get("/users")
async def get_all_users(authorization: str = Header(None)):
    header = {"Authorization": authorization}
    r = requests.get(
        url=USERS_URL,
        headers=header,
    )

    response_json = r.json()

    return response_json


@app.get("/users/{id}")
async def get_user_by_id(id: str, authorization: str = Header(None)):
    header = {"Authorization": authorization}
    r = requests.get(url=USERS_URL + "/" + id, headers=header)

    response_json = r.json()

    return response_json


@app.put("/users/{id}")
async def update_user(id: str, authorization: str = Header(None), user: User = None):
    data = jsonable_encoder(user)
    header = {"Authorization": authorization, "Content-Type": "application/json"}
    r = requests.put(
        url=USERS_URL + "/" + id,
        headers=header,
        data=json.dumps(data),
    )

    return status.HTTP_204_NO_CONTENT


@app.patch("/users/{id}")
async def update_user_password(
    id: str, authorization: str = Header(None), password: dict = {}
):

    data = jsonable_encoder(password)
    header = {"Authorization": authorization, "Content-Type": "application/json"}
    r = requests.put(
        url=USERS_URL + "/" + id + "/reset-password",
        headers=header,
        data=json.dumps(data),
    )

    return status.HTTP_204_NO_CONTENT


@app.delete("/users/{id}")
async def delete_user(id: str, authorization: str = Header(None)):
    header = {"Authorization": authorization}
    r = requests.delete(url=USERS_URL + "/" + id, headers=header)
    return status.HTTP_204_NO_CONTENT

@app.post("/refreshToken")
async def refresh_token(client_id: str = Form(...),
    client_secret: str = Form(...),
    grant_type: str = Form(...),
    refresh_token: str = Form(...),
    response: Response = 200):
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "client_id": client_id,
        "refresh_token": refresh_token,
        "grant_type": grant_type,
        "client_secret": client_secret,
    }
    r = requests.post(url=TOKEN_URL, headers=header, data=body, timeout=3)
    response_json = r.json()
    return response_json

@app.get("/users/{username}")
async def find_by_username(authorization: str = Header(None), username: str = ""):
    header = {"Authorization": authorization}
    username = "vitoria"
    r = requests.get(url=USERS_URL + "?username=vitoria",
     headers=header,
     timeout=3)
    return r.json()
