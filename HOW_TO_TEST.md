# How to test the API in Postman

Server needs to be running first:

```
python manage.py runserver
```

## 1. Login as Admin

**POST** `http://127.0.0.1:8000/api/token/`

Body → raw → JSON:
```json
{
    "username": "YOUR_ADMIN_USERNAME",
    "password": "YOUR_ADMIN_PASSWORD"
}
```

Response:
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIs...",
    "access": "eyJhbGciOiJIUzI1NiIs..."
}
```

Copy the `access` value.

## 2. Set up auth in Postman

Go to the **Authorization** tab of any request → type **Bearer Token** → paste the `access` value in the field.

Do this per-request — Postman doesn't share auth across requests unless you set it at the collection/folder level.

## 3. Create a Manager (Admin token)

**POST** `http://127.0.0.1:8000/api/register/`

```json
{
    "username": "mgr1",
    "email": "mgr1@test.com",
    "password": "MgrPass123",
    "role": "MANAGER"
}
```

Note the `id` in the response — that's the manager's user id.

## 4. Create a User under that Manager (Admin token)

**POST** `http://127.0.0.1:8000/api/register/`

```json
{
    "username": "user1",
    "email": "user1@test.com",
    "password": "UserPass123",
    "role": "USER",
    "manager": 2
}
```

`manager` = the id from step 3.

## 5. Log in as mgr1 and user1

Same as step 1, just swap the body:

```json
{"username": "mgr1", "password": "MgrPass123"}
```
```json
{"username": "user1", "password": "UserPass123"}
```

Save each `access` token separately — `MGR_TOKEN`, `USER_TOKEN`.

## 6. Users list — check role filtering

**GET** `http://127.0.0.1:8000/api/users/`

| Token used | Result |
|---|---|
| Admin | every user |
| MGR_TOKEN | only `user1` |
| USER_TOKEN | only itself |

## 7. Register — blocked for non-admins

**POST** `http://127.0.0.1:8000/api/register/` with **MGR_TOKEN**

```json
{"username": "x", "password": "pass1234", "role": "USER"}
```

Expect `403`.

## 8. Create + list tasks

**POST** `http://127.0.0.1:8000/api/tasks/` with **USER_TOKEN**

```json
{
    "title": "my task",
    "description": "test task description",
    "done": false
}
```

**GET** `http://127.0.0.1:8000/api/tasks/` with **MGR_TOKEN** — should include user1's task.

## 9. Update a task

**PUT** `http://127.0.0.1:8000/api/tasks/1/` (replace `1` with the actual task id)

```json
{
    "title": "updated task title",
    "description": "updated description",
    "done": true
}
```

Works with USER_TOKEN (owner), MGR_TOKEN (owner's manager), or Admin. A different user's token gets `403`.

## 10. Delete — Admin only

**DELETE** `http://127.0.0.1:8000/api/tasks/1/`

- With USER_TOKEN → expect `403`, even on your own task.
- With Admin token → expect `204`.

## Checklist

- [ ] Login works, wrong password returns 401
- [ ] Register works for Admin, blocked (403) for Manager
- [ ] Registering `role: "USER"` without `manager` returns 400
- [ ] `/api/users/` returns different results per role
- [ ] Tasks list is scoped the same way as users
- [ ] Only the task owner or their manager can update a task
- [ ] Only Admin can delete a task
- [ ] No token on any endpoint returns 401

## Common mistakes

- Forgetting the word `Bearer` before the token in the Authorization header — without it you get `401`.
- Passing a username instead of a numeric id for `manager`.
- Sending `role` in lowercase — it has to be `ADMIN`, `MANAGER`, or `USER`.
- Using the `refresh` token instead of `access` for normal requests — `refresh` is only for `/api/token/refresh/`.
