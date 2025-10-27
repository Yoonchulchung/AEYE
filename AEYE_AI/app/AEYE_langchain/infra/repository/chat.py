from sqlalchemy.orm import Session

from AEYE_langchain.infra.db_model.chat import (
    Chat_Message,
    Chat_Session,
    Langchain_User,
)


def insert_langchain_user(session : Session, user_name):
    new_user = Langchain_User(
        usuer_name = user_name
    )
    
    try:
        session.add(new_user)
        session.commit()
    except Exception as e:
        
        session.rollback()
        print(f"Something wrong while inserting langchain user : {e}")
        raise e


def insert_chat_session(session: Session, user_id, chat_session):
    
    new_session = Chat_Session(
        user_id  = user_id,
        title    = chat_session.title,
        metadata = chat_session.metadata
    )
    
    try:
        session.add(new_session)
        session.commit()
    except Exception as e:
        
        session.rollback()
        print(f"Something wrong while inserting langchain user : {e}")
        raise e
    
    
def insert_chat_message(session : Session, session_id, chat_message):
    
    new_message = Chat_Message(
        session_id = session_id,
        role       = chat_message.role,
        content    = chat_message.content,
        metadata   = chat_message.metadata,
    )
    
    try:
        session.add(new_message)
        session.commit()
    except Exception as e:
        
        session.rollback()
        print(f"Something wrong while inserting langchain user : {e}")
        raise e