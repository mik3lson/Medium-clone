

from app import db
from datetime import datetime

class blogpost(db.Model):
    id= db.Column(db.Interger(), primary_key())
    title = db.Column (db.string(100), nullale =False)
    author = db.Column(db.String)
    time = db.Column(db.DateTime)
    niche= db.Column(db.String())
    content = db.Column(db.Text)
