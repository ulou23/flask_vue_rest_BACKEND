from application import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class URLS(db.Model):

    id=db.Column(db.Integer, primary_key=True)
    urlinput = db.Column(db.String(100), unique=True)

    def __init__(self, urlinput):
        self.urlinput =urlinput

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'urlinput': self.urlinput
        }

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

class URLschema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model=URLS


    id=fields.Integer(dump_only=True)
    urlinput=fields.String(required=True)

