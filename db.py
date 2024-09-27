from os import getenv
from app import app
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)

from sqlalchemy import text

# check if the connection is successfully established or not
with app.app_context():
    with app.open_resource('schema.sql') as f:
        db.session.execute(text(f.read().decode('utf8')))
        db.session.commit()
    try:
        db.session.execute(text('SELECT * FROM users'))
        print(f'{"-"*8} Connection to database successful !{"-"*8}')
    except Exception as e:
        print(f'{"-"*8} Connection failed ! ERROR : ', e, f'{"-"*8}')