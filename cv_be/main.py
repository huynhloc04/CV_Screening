import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app import api
from database.db_config import db

# load environment variables
# load_dotenv()

ALLOWED_HOSTS = ["*"]

def init_app():
    # db.init()

    app = FastAPI(
        title="CV SCREENING",
        description="CV SCREENING BACKEND",
        version="1.7"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    
    # start the app
    @app.on_event("startup")
    async def startup():
        await db.init_db()  

    @app.on_event("shutdown")
    async def shutdown():
        print("==> App closed")

#     app.mount("/data", StaticFiles(directory = "data"),name = "data")
    app.include_router(api.router)
    
    return app

app = init_app()
if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8080, reload=False, workers=10) #8000
