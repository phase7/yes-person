from fastapi import FastAPI, Request

app = FastAPI(title="yes-person", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def catch_all(path: str, request: Request):
    return {
        "error": "stub_not_found",
        "message": f"{request.method} /{path} is not yet implemented in yes-person",
        "path": f"/{path}",
        "method": request.method,
    }
