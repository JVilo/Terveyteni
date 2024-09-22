from os import getenv
from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine
from sqlalchemy import Integer, String, Column, Table, TIMESTAMP, ForeignKey



app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

md = MetaData()

engine = create_engine(getenv("DATABASE_URL"))

peapole = db.Table(
    "users", md,
    Column("id", Integer, primary_key = True),
    Column("name", String),
    Column("password", String),
    Column("role", Integer)
    #Column("dr_id",Integer)
)

messages = db.Table(
    "messages", md,
    Column("id", Integer, primary_key = True),
    Column("title", String),
    Column("content", String),
    Column("user_id",ForeignKey("users.id"), nullable=False),
    Column("sent_at", TIMESTAMP),
    Column("visible",Integer),
    Column("ref_key", ForeignKey("messages.id"))
)

tasks1 = db.Table(
    "RR_tasks", md,
    Column("id", Integer, primary_key = True),
    Column("RRm1_sys", Integer),
    Column("RRm1_dia", Integer),
    Column("RRm2_sys", Integer),
    Column("RRm2_dia", Integer),
    Column("RRmed1_sys", Integer),
    Column("RRmed1_dia", Integer),
    Column("RRmed2_sys", Integer),
    Column("RRmed2_dia", Integer),
    Column("RRe1_sys",Integer),
    Column("RRe1_dia", Integer),
    Column("RRe2_sys", Integer),
    Column("RRe2_dia", Integer),
    Column("RRemed1_sys",Integer),
    Column("RRemed1_dia", Integer),
    Column("RRemed2_sys", Integer),
    Column("RRemed2_dia", Integer),
    Column("user_id",ForeignKey("users.id"), nullable=False),
    Column("active", Integer)
)

task2 = db.Table(
    "bmi", md,
    Column("id", Integer,primary_key= True),
    Column("weight", Integer),
    Column("height", Integer),
    Column("user_id",ForeignKey("users.id"), nullable=False),
    Column("active", Integer)
)
activate_bmi = db.Table(
    "activ_bmi",md,
    Column("id", Integer, primary_key= True),
    Column("activ", Integer)
)
md.create_all(engine)

