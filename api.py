from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from fastapi.middleware.cors import CORSMiddleware
from langgraph_backend_code import backend

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    chat_id: str
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    result = backend.invoke(
        {"msgs": [HumanMessage(content=req.message)]},
        config={"configurable": {"thread_id": req.chat_id}}
    )
    return {"reply": result["msgs"][-1].content}
