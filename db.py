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
)

messages = db.Table(
    "messages", md,
    Column("id", Integer, primary_key = True),
    Column("content", String),
    Column("user_id",ForeignKey("users.id"), nullable=False),
    Column("sent_at", TIMESTAMP)
)
#tasks = db.Table(
    #"tasks", md,
    #Column("id", Integer, primary_key = True),
    #Column()
#)

md.create_all(engine)

