from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat import router as chat_router
from dotenv import load_dotenv
import os

# 🔥 Load environment variables (.env)
load_dotenv()

app = FastAPI()

app.include_router(chat_router)

# 🔥 CORS (VERY IMPORTANT for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 ROUTES IMPORT
from app.routes.marketplace import router as marketplace_router
from app.routes.auth_routes import router as auth_router

# 🔥 REGISTER ROUTES
app.include_router(marketplace_router)
app.include_router(auth_router)

# 🔥 ROOT TEST
@app.get("/")
def root():
    return {
        "message": "AI API Marketplace Backend Running 🚀",
        "llm": "enabled" if os.getenv("OPENAI_API_KEY") else "disabled"
    }