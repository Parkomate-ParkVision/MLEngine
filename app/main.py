from fastapi import FastAPI, Depends
import uvicorn
from users.db import User, create_db_and_tables, engine
from users.schemas import UserCreate, UserRead, UserUpdate
from users.manager import auth_backend, current_active_user, fastapi_users
from sqladmin import Admin
from users.admin import UserAdmin
from routers.yoloroutes import yolorouter


app = FastAPI()


admin = Admin(app, engine)
admin.add_view(UserAdmin)


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(yolorouter, prefix="/yolo", tags=["yolo"])


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "ParkVision ML Backend with Swagger, Redoc, and Users"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, log_level="info")