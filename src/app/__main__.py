from fastapi import FastAPI
import uvicorn

from app.api.index import router
from app.settings import settings

app = FastAPI()
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(
        'app.__main__:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )
