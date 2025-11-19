from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.chat import Conversation, ChatMessage
from app.schemas.chat import (
    ConversationCreate,
    ConversationOut,
    ChatMessageCreate,
    ChatMessageOut,
)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/conversations", response_model=ConversationOut, status_code=status.HTTP_201_CREATED)
def create_conversation(payload: ConversationCreate, db: Session = Depends(get_db)):
    conv = Conversation(user_id=payload.user_id, title=payload.title)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


@router.get("/conversations", response_model=List[ConversationOut])
def list_conversations(user_id: int, db: Session = Depends(get_db)):
    items = db.query(Conversation).filter(Conversation.user_id == user_id).all()
    return items


@router.post("/messages", response_model=ChatMessageOut, status_code=status.HTTP_201_CREATED)
def create_message(payload: ChatMessageCreate, db: Session = Depends(get_db)):
    # Ensure conversation exists
    conv = db.query(Conversation).filter(Conversation.id == payload.conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="conversation not found")
    msg = ChatMessage(conversation_id=payload.conversation_id, sender=payload.sender, content=payload.content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


@router.get("/conversations/{conversation_id}/messages", response_model=List[ChatMessageOut])
def list_messages(conversation_id: int, db: Session = Depends(get_db)):
    msgs = db.query(ChatMessage).filter(ChatMessage.conversation_id == conversation_id).order_by(ChatMessage.created_at.asc()).all()
    return msgs
