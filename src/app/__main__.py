from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from app.api.index import router
from app.core.settings import settings

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
