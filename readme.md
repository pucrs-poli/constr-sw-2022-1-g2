# T1 Construção de Software

## Integrantes

* Eduarda Keller
* Kevin Boucinha
* Vitor dos Santos

## Tecnologias

[FastAPI][0]

[Keycloak][1]

## Rotas

### Login

```http
POST http://localhost:8000 HTTP/1.1
Authorization: Bearer {{access_token}}
```

### Create user

```http
POST http://localhost:8000 HTTP/1.1
Authorization: Bearer {{access_token}}
```

### Get all users

```http
GET http://localhost:8000 HTTP/1.1
Authorization: Bearer {{access_token}}
```

### Get user by ID

```http
GET http://localhost:8000 HTTP/1.1
Authorization: Bearer {{access_token}}
```

### Update user by ID

```http
PUT http://localhost:8000 HTTP/1.1
Authorization: Bearer {{access_token}}
```

### Update user password

```http
PATCH http://localhost:8000 HTTP/1.1
Authorization: Bearer {{access_token}}
```

### Delete user by ID

```http
DELETE http:/{{base-api-url}}/users/{id} HTTP/1.1
Authorization: Bearer {{access_token}}
```

[0]: https://fastapi.tiangolo.com/ "FastAPI"
[1]: https://www.keycloak.org/ "Keycloak"
