# How to test the API

Server needs to be running first:

```
python manage.py runserver
```

## Easiest way: Swagger UI

Open `http://127.0.0.1:8000/swagger/` in a browser.

1. Expand `POST /api/token/` → Try it out → body:
   ```json
   {"username": "admin", "password": "AdminPass123"}
   ```
   Execute, copy the `access` value from the response.
2. Click **Authorize** (top right). Type `Bearer ` followed by the token you copied (the word "Bearer", one space, then the token — all in that one field).
3. Authorize → Close. Every endpoint's "Try it out" is now authenticated.
4. To test as a different role, repeat steps 1-3 with that user's login.

## Or with curl

Get a token:
```
curl -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" -d "{\"username\": \"admin\", \"password\": \"AdminPass123\"}"
```

Use it on any other call:
```
curl http://127.0.0.1:8000/api/users/ -H "Authorization: Bearer PASTE_TOKEN_HERE"
```

## Set up a sample team first

You need at least one Admin, one Manager, and two Users (one on the manager's team, one not) to actually see the role filtering do something.

```
# as admin, create a manager
curl -X POST http://127.0.0.1:8000/api/register/ -H "Content-Type: application/json" -H "Authorization: Bearer ADMIN_TOKEN" -d "{\"username\": \"mgr1\", \"email\": \"mgr1@test.com\", \"password\": \"MgrPass123\", \"role\": \"MANAGER\"}"

# create a user under that manager (use the id returned above)
curl -X POST http://127.0.0.1:8000/api/register/ -H "Content-Type: application/json" -H "Authorization: Bearer ADMIN_TOKEN" -d "{\"username\": \"user1\", \"email\": \"user1@test.com\", \"password\": \"UserPass123\", \"role\": \"USER\", \"manager\": 2}"
```

Log in as `mgr1` and `user1` the same way as admin to get their tokens too.

## What to actually check

Run the same request with different tokens and watch the response change — that's the RBAC rules proving themselves.

**Users list**
```
curl http://127.0.0.1:8000/api/users/ -H "Authorization: Bearer ADMIN_TOKEN"    # sees everyone
curl http://127.0.0.1:8000/api/users/ -H "Authorization: Bearer MGR_TOKEN"      # sees only their team
curl http://127.0.0.1:8000/api/users/ -H "Authorization: Bearer USER_TOKEN"     # sees only themself
```

**Register — admin only**
```
curl -X POST http://127.0.0.1:8000/api/register/ -H "Content-Type: application/json" -H "Authorization: Bearer MGR_TOKEN" -d "{\"username\": \"x\", \"password\": \"pass1234\", \"role\": \"USER\"}"
```
Expect `403` — a manager can't register users.

**Create + list tasks**
```
curl -X POST http://127.0.0.1:8000/api/tasks/ -H "Content-Type: application/json" -H "Authorization: Bearer USER_TOKEN" -d "{\"title\": \"my task\"}"
curl http://127.0.0.1:8000/api/tasks/ -H "Authorization: Bearer MGR_TOKEN"
```
The manager's list should include their team member's task but not tasks belonging to users outside their team.

**Delete — admin only**
```
curl -X DELETE http://127.0.0.1:8000/api/tasks/1/ -H "Authorization: Bearer USER_TOKEN"
```
Expect `403`, even if it's that user's own task.

```
curl -X DELETE http://127.0.0.1:8000/api/tasks/1/ -H "Authorization: Bearer ADMIN_TOKEN"
```
Expect `204`.

## Quick checklist

- [ ] Login works, wrong password returns 401
- [ ] Register works for Admin, blocked (403) for Manager and User
- [ ] Registering role=USER without a manager returns 400
- [ ] `/api/users/` returns different results per role
- [ ] `/api/me/` always returns your own account, not anyone else's
- [ ] Tasks list is scoped the same way as users
- [ ] Only the task owner or their manager can update a task
- [ ] Only Admin can delete a task
- [ ] No token on any endpoint returns 401

## Common mistakes

- Forgetting the word `Bearer` before the token in the Authorization header — without it you get `401 Authentication credentials were not provided`, even though a header was technically sent.
- Passing a username instead of a numeric id for `manager`.
- Sending `role` in lowercase — it has to be `ADMIN`, `MANAGER`, or `USER`.
