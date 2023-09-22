from typing import Any

from litestar import Litestar, get
import uvicorn

@get("/sync", sync_to_thread=False)
def sync_hello_world() -> dict[str, Any]:  # noqa: UP006
    """Route Handler that outputs hello world."""
    return {"hello": "world"}


app = Litestar(route_handlers=[sync_hello_world])

if __name__ == "__main__":
    uvicorn.run("app:app")