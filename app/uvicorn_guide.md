# Uvicorn Guide

This file explains what Uvicorn is and why it is used with FastAPI.

## 1. What is Uvicorn?

Uvicorn is a web server that runs ASGI applications.

FastAPI is the API framework. Uvicorn is the thing that actually serves the app over HTTP.

Think of it like this:
- FastAPI = app logic and routes
- Uvicorn = web server that runs the app

## 2. Why do we use it with FastAPI?

FastAPI creates an application object, but it does not run the server by itself.

To start the app, we run:

```bash
uvicorn app.main:app --reload
```

This means:
- `app.main` = the Python file containing the FastAPI app
- `app` = the FastAPI instance
- `--reload` = restart the server automatically when you edit code

## 3. What happens when it runs?

When Uvicorn starts, it:
- loads the FastAPI app
- listens for HTTP requests on a port like 8000
- routes incoming requests to your endpoints
- returns JSON responses

## 4. Example

If you have this in `app/main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

Then running:

```bash
uvicorn app.main:app --reload
```

lets you visit:

```text
http://localhost:8000/health
```

and get:

```json
{"status": "ok"}
```

## 5. What is ASGI?

ASGI is the interface standard for async Python web frameworks.

It is similar to WSGI, but for modern async frameworks.

FastAPI uses ASGI, and Uvicorn is a common ASGI server used to run it.

## 6. Why is this useful?

It allows you to build web APIs with Python and serve them easily during development and later in production.

In short:
- FastAPI defines your API
- Uvicorn serves it

## 7. Summary

You do not need to understand every internal detail of Uvicorn right now.

For this project, the important idea is:

- `FastAPI` writes the API logic
- `Uvicorn` runs the API locally
- `uvicorn app.main:app --reload` starts the backend
