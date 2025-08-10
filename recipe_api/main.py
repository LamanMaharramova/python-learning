from fastapi import FastAPI
from .recipes.routes import router

app = FastAPI()
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}