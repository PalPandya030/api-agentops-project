from fastapi import APIRouter

router = APIRouter()

@router.post("/chat")
def chat(message: dict):
    user_msg = message.get("message")

    return {
        "reply": f"AI Response to: {user_msg}"
    }