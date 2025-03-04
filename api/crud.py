from sqlalchemy.orm import Session

import models

def insert_conversation(db: Session, session_id: str):
    is_session_exist = db.query(models.Conversation).filter(models.Conversation.session_id==session_id).first()
    if is_session_exist:
        return
    conversation = models.Conversation(session_id=session_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

def insert_messages(db: Session, session_id: str, user_query: str, ai_response: str):
    messages = models.Messages(session_id=session_id, user_query=user_query, ai_response=ai_response)
    db.add(messages)
    db.commit()
    db.refresh(messages)

def get_history(db: Session, session_id: str):
    db_messages = db.query(models.Messages).filter(models.Messages.session_id==session_id).all()
    messages = []
    for row in db_messages:
        messages.extend([
            {"role": "human", "content": row.user_query},
            {"role": "ai", "content": row.ai_response}
        ])
    return messages

