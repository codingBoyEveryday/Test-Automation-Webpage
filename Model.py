from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(250), nullable=False)
    password_hash = db.Column(db.String(1000), nullable=False)
    # password = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    group = db.Column(db.String(250), nullable=False)


    # category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    # category = db.relationship('Category', backref=db.backref('comments', lazy='dynamic' ))

    # def __init__(self, comment, category_id):
    #     self.comment = comment
    #     self.category_id = category_id


# class Category(db.Model):
#     __tablename__ = 'categories'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), unique=True, nullable=False)
#
#     def __init__(self, name):
#         self.name = name

class UserSchema(ma.Schema):
    user_id = fields.Integer()
    username = fields.String(required=True)
    password_hash = fields.String(required=True)
    email = fields.String(required=True)
    group = fields.String(required=True)

# class CategorySchema(ma.Schema):
#     id = fields.Integer()
#     name = fields.String(required=True)

#
# class CommentSchema(ma.Schema):
#     id = fields.Integer(dump_only=True)
#     category_id = fields.Integer(required=True)
#     comment = fields.String(required=True, validate=validate.Length(1))
#     creation_date = fields.DateTime()