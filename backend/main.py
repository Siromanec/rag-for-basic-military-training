
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from controller import router

app = fastapi.FastAPI(docs_url="/")
app.include_router(router)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
