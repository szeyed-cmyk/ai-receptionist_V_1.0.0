"""ASGI entry point for local run, Docker, and Render.

Start command (run from this project folder):
    uvicorn main:app --host 0.0.0.0 --port $PORT
"""
import os
import uvicorn
from app import app

__all__ = ["app"]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)


@app.middleware("http")
async def allow_vibe96_iframe(request, call_next):
    response = await call_next(request)

    response.headers.pop("X-Frame-Options", None)

    response.headers["Content-Security-Policy"] = (
        "frame-ancestors https://vibe96.com https://www.vibe96.com"
    )

    return response
