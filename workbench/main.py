from fastapi import FastAPI
import adc_service

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/run-game")
def run_game():
    adc_service.run()


@app.get("/stop-game")
def stop():
    print("stop")
