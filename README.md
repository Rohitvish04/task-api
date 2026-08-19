# RBAC Task API

A small Django REST API I built to practice role-based access control (RBAC) with JWT authentication. It has three roles — Admin, Manager, and User — and every endpoint behaves differently depending on who's logged in.

## What it does

- **Admin** can create users, assign roles, and see/manage everything in the system.
- **Manager** manages their own team (a User is linked to a Manager through a `manager` field), but can't create new accounts.
- **User** can only see and edit their own profile and their own tasks.

Login is handled with JWT (access + refresh tokens), so once you log in you just attach the token to every request instead of sending a username/password each time.

## Tech used

- Django
- Django REST Framework
- djangorestframework-simplejwt (JWT auth)
- drf-yasg (Swagger docs)
- SQLite (for local dev)

## How I structured the roles

Instead of building a separate "Team" model, I added a self-referencing `manager` field on the `User` model itself — a User's `manager` field just points to another User (their manager). It keeps the schema simple since I didn't need extra team-level data like a team name or department.

Every list endpoint filters its queryset based on the logged-in user's role:

```python
def get_queryset(self):
    user = self.request.user
    if user.role == "ADMIN":
        return User.objects.all()
    if user.role == "MANAGER":
        return User.objects.filter(manager=user)
    return User.objects.filter(id=user.id)
```

Same idea applies to tasks — Admin sees all tasks, Manager sees their team's tasks, User sees only their own. Deleting a task is locked to Admin only, no matter who owns it.

## Setup

```
cd rbac-task-api
venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations accounts tasks
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

New accounts default to role `USER`, so after creating a superuser I promote them to Admin manually:

```
python manage.py shell -c "
from accounts.models import User
u = User.objects.get(username='YOUR_USERNAME')
u.role = 'ADMIN'
u.save()
"
```

Server runs at `http://127.0.0.1:8000/`. Swagger docs live at `http://127.0.0.1:8000/swagger/`.

## Endpoints

| Endpoint | Method | Who | Body |
|---|---|---|---|
| `/api/token/` | POST | anyone | `{"username", "password"}` |
| `/api/token/refresh/` | POST | anyone with a refresh token | `{"refresh"}` |
| `/api/register/` | POST | Admin only | `{"username", "email", "password", "role", "manager"}` |
| `/api/users/` | GET | Admin (all), Manager (team), User (self) | - |
| `/api/me/` | GET/PUT | self | `{"username", "email", "role", "manager"}` |
| `/api/tasks/` | GET | all, filtered by role | - |
| `/api/tasks/` | POST | Manager, User, Admin | `{"title", "description", "done"}` |
| `/api/tasks/{id}/` | PUT | owner, owner's manager, or Admin | `{"title", "description", "done"}` |
| `/api/tasks/{id}/` | DELETE | Admin only | - |

`manager` is the numeric id of an existing Manager — required when `role` is `"USER"`, and left out otherwise.

## Testing it

Easiest way is the Swagger UI (`/swagger/`) — log in through `POST /api/token/`, copy the `access` token, click **Authorize**, paste `Bearer <token>`, and every endpoint becomes testable from the browser.

To test the role filtering properly, set up a sample team first:

1. Log in as Admin, `POST /api/register/` a Manager (no `manager` field).
2. `POST /api/register/` a User with `role: "USER"` and `manager: <manager_id>`.
3. Log in as that Manager → `GET /api/users/` returns only that one User.
4. Log in as the User → `GET /api/users/` and `GET /api/tasks/` return only their own stuff.

Run the same request (e.g. `GET /api/users/`, `GET /api/tasks/`) with each role's token and watch the response change — that's the RBAC rules proving themselves.

## Still on my list

- A Postman collection so the API can be tested without typing requests by hand
- Unit tests around the permission rules, so the role logic is covered automatically instead of only manually
