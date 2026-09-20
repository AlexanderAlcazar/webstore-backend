# Feature Branch README: `feature/auth-schemas-and-router`

This branch turns the auth router into real working API endpoints.

## Goal

Add request and response schemas for auth flows and connect the auth router to the auth service.

## Why This Branch Exists

The auth layer already has foundational pieces, but the endpoints need proper request validation and service wiring before they can be used as real API routes.

## Planned Work

- create Pydantic schemas for register and login requests
- create clear response shapes for auth endpoints
- wire the auth router to `auth_service.py`
- replace placeholder logic with real endpoint behavior

## Expected Result

`POST /users/register` and `POST /users/login` return real responses and validate incoming request bodies.

## Likely Files

- `app/routers/auth.py`
- auth schema module if added under `app/schemas/`
- `app/services/auth_service.py`

## Merge Back to Main

After this branch is merged, the project has usable auth endpoints that fit the router-service-repository structure.
