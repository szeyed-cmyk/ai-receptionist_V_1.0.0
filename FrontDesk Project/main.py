"""ASGI entry point for local run, Docker, and Render.

Start command (run from this project folder):
    uvicorn main:app --host 0.0.0.0 --port $PORT
"""
import os
import uvicorn
from app import app

__all__ = ["app"]


# Allow Vibe96 to embed the FrontDesk AI application.
@app.middleware("http")
async def allow_vibe96_iframe(request, call_next):
    response = await call_next(request)

    # Remove X-Frame-Options safely.
    if "X-Frame-Options" in response.headers:
        del response.headers["X-Frame-Options"]

    # Preserve existing CSP directives while updating frame-ancestors.
    existing_csp = response.headers.get("Content-Security-Policy", "")

    directives = [
        directive.strip()
        for directive in existing_csp.split(";")
        if directive.strip()
        and not directive.strip().lower().startswith("frame-ancestors")
    ]

    directives.append(
        "frame-ancestors https://vibe96.com https://www.vibe96.com"
    )

    response.headers["Content-Security-Policy"] = "; ".join(directives)

    return response



if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
