from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, chats, messages, subway_route, users


app = FastAPI()

origins = [
    "https://estacao-facil-front-end.vercel.app",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chats.router)
app.include_router(messages.router)
app.include_router(subway_route.router)
app.include_router(users.router)
