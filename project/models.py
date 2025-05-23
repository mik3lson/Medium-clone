

from app import db
from datetime import datetime

class blogPost(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    title = db.Column (db.String, nullable = False)
    content= db.Column (db.String, nullable =False)
    niche = db.Column(db.String)
    date_posted =db.Column (db.DateTime, default =datetime.utcnow)
    user_id = db.Column (db.Integer, db.ForeignKey('user.id'), nullable = False)

