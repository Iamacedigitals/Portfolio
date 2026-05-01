from fastapi import FastAPI

from Backend.DB.routes import db_route
app = FastAPI(
    title="Crypto",
    description="A crypto trading bot",
    version="0.0.1"
)

app.include_router(db_route)