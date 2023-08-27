from fastapi import FastAPI
from server.endpoints import router
app = FastAPI()
app.include_router(router)

