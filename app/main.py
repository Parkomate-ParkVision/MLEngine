from fastapi import FastAPI
import uvicorn
from routers.yoloroutes import yolorouter


app = FastAPI()

app.include_router(yolorouter, prefix="/yolo", tags=["yolo"])

@app.get("/")
async def root():
    return {"message": "ParkVision ML Backend with Swagger, Redoc"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, log_level="info")
