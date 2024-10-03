from pyexpat.errors import messages

from db import db
from sqlalchemy.sql import text
import users


def get_list():
    sql = """
        SELECT 
            M.title, 
            M.content, 
            U.name, 
            M.sent_at, 
            M.id 
        FROM messages M, users U 
        WHERE M.user_id=U.id 
            AND m.visible=1
            AND m.ref_key IS NULL
        ORDER BY M.id"""
    result = db.session.execute((text(sql)))
    return result.fetchall()

#def get_all():
    #return db.session.execute(text('SELECT * FROM messages')).fetchall()

def send(title, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = """
        INSERT INTO messages 
            (title, content, user_id, sent_at, visible) 
            VALUES (:title, :content, :user_id, NOW(), :visible)
        """
    db.session.execute(
        (text(sql)),
        {"title": title, "content": content, "user_id": user_id, "visible": 1}
    )
    db.session.commit()
    return True


def answer_mes(content, ref_key):
    user_id = users.user_id()
    sql = """
        INSERT INTO messages (content, user_id, sent_at, visible, ref_key) 
            VALUES (:content, :user_id, NOW(), :visible, :ref_key)
        """
    db.session.execute((text(sql)), {"content": content, "user_id": user_id, "visible": 1, "ref_key": ref_key})
    db.session.commit()
    return True


def get_my_message(user_id):
    sql = """SELECT m.id, m.title, m.content FROM messages m
             WHERE m.user_id=:user_id AND m.visible=1 ORDER BY m.sent_at"""
    return db.session.execute((text(sql)), {"user_id": user_id}).fetchall()


def remove_message(messages_id, user_id):
    print(messages_id)
    sql = "UPDATE messages  SET visible = 0 WHERE id =:id AND user_id=:user_id"
    db.session.execute((text(sql)), {"id": messages_id, "user_id": user_id})
    db.session.commit()


def get_message(message_id) -> list[dict]:
    sql = """
        SELECT 
            m.title, 
            m.content, 
            m.sent_at, 
            u.name, 
            m.id
        FROM messages m, users u
        WHERE m.id=:message_id AND visible = 1
        ORDER BY m.sent_at 
        """
    result = db.session.execute((text(sql)), {"message_id": message_id}).first()
    result = result._mapping

    return result

def get_answers(parent_id) -> list[dict]:
    sql = """
        SELECT 
            m.title, 
            m.content, 
            m.sent_at, 
            u.name, 
            m.id
        FROM messages m, users u
        WHERE m.ref_key=:parent_id AND visible = 1 AND m.user_id =u.id
        ORDER BY m.sent_at 
        """
    result = db.session.execute((text(sql)), {"parent_id": parent_id}).all()
    print(result,"tämä sisältö")
    return result