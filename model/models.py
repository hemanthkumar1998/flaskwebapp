# from app import db


# class User(db.Model):
#     id= db.Column(db.Integer,primary_key=True,autoincrement=True)
#     email=db.Column(db.String(40),unique=True,nullable=True)
#     password=db.Column(db.String(40),unique=True,nullable=True)
#     def __init__(self,id,email,password):
#         self.id=id
#         self.email=email
#         self.password=password

#     def __repr__(self):
#         return "Id:{0},email:{1}".format(self.id,self.email)