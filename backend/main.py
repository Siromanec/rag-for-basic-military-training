
import fastapi
from controller import router

app = fastapi.FastAPI(docs_url="/")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
