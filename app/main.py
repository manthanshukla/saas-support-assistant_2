
from fastapi import FastAPI, HTTPException
from app.schemas import ChatRequest, ChatResponse
from app.services.chat_service import process_chat

app = FastAPI(title="SaaS Support Assistant")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    try:
        if not request.message.strip():
            raise HTTPException(
                status_code=422,
                detail="Message cannot be empty"
            )

        result = process_chat(
            request.message,
            request.conversation
        )

        return ChatResponse(**result)

    except HTTPException:
        raise

    except Exception as e:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )