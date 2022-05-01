# T1 Construção de Software

## Integrantes

* Eduarda Keller
* Kevin Boucinha
* Vitor dos Santos

## Tecnologias

[FastAPI][0]

[Keycloak][1]

[Swagger][2]

## Rotas

### Docs

```http
GET http://{{base_api_url}}/docs HTTP/1.1
```

### Login

```http
POST http://{{base_api_url}}/login HTTP/1.1
Content-type: application/json

{
  "name": "sample",
  "time": "Wed, 21 Oct 2015 18:27:50 GMT"
}
```

### Create user

```http
POST http://{{base_api_url}}/users HTTP/1.1
Authorization: Bearer {{access_token}}
Content-type: application/json

{
  "name": "sample",
  "time": "Wed, 21 Oct 2015 18:27:50 GMT"
}
```

### Get all users

```http
GET http://{{base_api_url}}/users HTTP/1.1
Authorization: Bearer {{access_token}}
```

### Get user by ID

```http
GET http://{{base_api_url}}/users HTTP/1.1
Authorization: Bearer {{access_token}}
```

### Update user by ID

```http
PUT http://{{base_api_url}}/users HTTP/1.1
Authorization: Bearer {{access_token}}
Content-type: application/json

{
  "name": "sample",
  "time": "Wed, 21 Oct 2015 18:27:50 GMT"
}
```

### Update user password

```http
PATCH http://{{base_api_url}}/users HTTP/1.1
Authorization: Bearer {{access_token}}
Content-type: application/json

{
  "name": "sample",
  "time": "Wed, 21 Oct 2015 18:27:50 GMT"
}
```

### Delete user by ID

```http
DELETE http:/{{base_api_url}}/users/{id} HTTP/1.1
Authorization: Bearer {{access_token}}
```

[0]: https://fastapi.tiangolo.com/ "FastAPI"
[1]: https://www.keycloak.org/ "Keycloak"
[2]: https://swagger.io/ "Swagger"
