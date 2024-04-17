from fastapi import FastAPI
from routers import user

app = FastAPI()

# Routers
app.include_router(user.router)