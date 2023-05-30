from fastapi import FastAPI
from dotenv import load_dotenv
from uvicorn import run as uvicorn_run
from fastapi.testclient import TestClient

load_dotenv()

from routes.users import router_users


app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "hello world"}


app.include_router(router=router_users)


if __name__ == "__main__":
    uvicorn_run(app=app, host="localhost", port=8000)  # run server
