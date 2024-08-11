from fastapi import FastAPI

import uvicorn

from auth.router_auth import router as auth_router

app = FastAPI()

app.include_router(router=auth_router)

# if __name__ == "__main__":
#     uvicorn.run(app, reload=True)


