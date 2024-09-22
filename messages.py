from db import db
from sqlalchemy.sql import text
import users

def get_list():
    sql = "SELECT M.title, M.content, U.name, M.sent_at FROM messages M, users U WHERE M.user_id=U.id AND m.visible=1 ORDER BY M.id"
    result = db.session.execute((text(sql)))
    return result.fetchall()

def send(title,content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (title, content, user_id, sent_at, visible) VALUES (:title, :content, :user_id, NOW(),:visible)"
    db.session.execute((text(sql)), {"title":title,"content":content, "user_id":user_id,"visible":1})
    db.session.commit()
    return True

def get_my_message(user_id):
    sql = """SELECT m.id, m.title, m.content FROM messages m
             WHERE m.user_id=:user_id AND m.visible=1 ORDER BY m.sent_at"""
    return db.session.execute((text(sql)), {"user_id":user_id}).fetchall()

def remove_message(messages_id, user_id):
    sql = "UPDATE messages  SET visible = 0 WHERE id =:id AND user_id=:user_id"
    db.session.execute((text(sql)), {"id":messages_id,"user_id":user_id})
    db.session.commit()
