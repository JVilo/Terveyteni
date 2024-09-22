from db import db
from sqlalchemy.sql import text
import users

#def get_tasks(user_id):
    
    #sql_bmi = """SELECT b.id FROM BMI b
             #WHERE  b.user_id=:user_id AND b.aktive = 1"""
    # sql_RR = ...
    #return db.session.execute((text(sql_bmi)), {"user_id":user_id}).fetchall()


def Bmi(weight, height):
    active = 1
    user_id = users.user_id()
    sql = """ INSERT INTO bmi (weight,height,user_id,active) VALUES (:weight,:height,:user_id,:active) """
    db.session.execute((text(sql)),{"weight":weight, "height":height, "user_id":user_id,"active":active})
    db.session.commit()
    return True

def cal_bmi(user_id):
    sql = """SELECT b.weight, b.height FROM bmi b, users u 
             WHERE b.user_id=:user_id ORDER BY u.id"""
    result = db.session.execute((text(sql)), {"user_id":user_id})

    return result.fetchall()


def activate_bmi(task_bmi):
    sql = """INSERT INTO activ_bmi(activ) VALUES (:activ)"""
    db.session.execute((text(sql)), {"activ":task_bmi})
    db.session.commit()
    return True

def get_activ_bmi():
    sql = """ SELECT activ FROM activ_bmi """
    result = db.session.execute((text(sql)))
    return result.fetchall()
