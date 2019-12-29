from flask import Flask,render_template,url_for,jsonify
from flask import request
import os
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth,HTTPTokenAuth
from werkzeug.security import generate_password_hash,check_password_hash
# from sqlalchemy import MetaData
# from model.models import User
# from sqlalchemy.orm import sessionmaker
from flask import flash
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
import datetime

flag=0

app=Flask(__name__)
app.secret_key="mysecret"

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "Pandoruserdatabase.db"))

app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
migrate=Migrate(app,db)

manager=Manager(app)
manager.add_command('db',MigrateCommand)
string=''
# Session=sessionmaker(db)
# session=Session()

class User(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(40),unique=True,nullable=True)
    email=db.Column(db.String(40),unique=True,nullable=True)
    password=db.Column(db.String(40),nullable=True)
    time=db.Column(db.DateTime,default=datetime.datetime.utcnow)
    def __init__(self,username,email,password):
        self.username=username
        self.email=email
        self.password=password

    def __repr__(self):
        return "Id:{0},email:{1},password{2}".format(self.id,self.email,self.password)

class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    product_id=db.Column(db.String(60),unique=True)
    product_name=db.Column(db.String(60),unique=True,nullable=True)
    product_price=db.Column(db.String(60))
    
    def __init__(self,product_id,product_name,product_price):
        self.product_id=product_id
        self.product_name=product_name
        self.product_price=product_price
    
    def __repr__(self):
        return "ID:{0},Product name:{1}".format(self.id,self.product_name)

# Migrate(app,db)


@app.route('/home',methods=['POST','GET'])
def home():
    flag=0
    if request.form:
        username=username=request.form.get("username")
        email=email=request.form.get("email")
        password=password=request.form.get("password")
        # db.create_all()
        # session.add(email)
        # session.add(password)
        user=User(username,email,password)
        db.session.add(user)
        db.session.commit()
        flash("Signup Successful")
    
    
    return render_template('index.html',flag=flag)

@app.route('/login',methods=['POST','GET'])
def login():
    
    if request.method=="POST":
        
        flag=1
        
        string=email=request.form.get("email")   
        print(string)         
        passwrd=request.form.get("pass")            
        # return session.query(User).filter(User.email=='email').first()

        db_email=User.query.filter_by(email=email).first()
        db_products=Product.query.all()
        # print(db_email.password,passwrd)
        if  passwrd==db_email.password:
            print(db_email.id)
            flash("Login Successful")
            return render_template('index.html',id=db_email.id,product=db_products,flag=flag)
        else:
            flash("mail or password mismatch")
            return render_template('login.html')
        
        # return db_email
        # print(db_email.email)
        # if db_email:
        #     return "yes"
        #     # return render_template('index.html')
        # else:
        #     return "noooo"
           
    return render_template('login.html')


@app.route('/signup',methods=["POST","GET"])
def signup():
    # if request.form:
    #     username=User(username=request.form.get("username"))
    #     email=User(email=request.form.get("email"))
    #     password=User(password=request.form.get("password"))
    #     # db.create_all()
    #     db.session.add(email)
    #     db.session.add(password)
    #     db.session.commit()
    
    return render_template('signup.html')

@app.route('/add',methods=['POST','GET'])
def add():
    # print(string)
    # if string!=:
    #     flash("Unauthorised access")

    #     return render_template('login.html')
    if request.method=='POST':
        product_id=request.form.get("product_id")
        product_name=request.form.get("product_name")
        product_price=request.form.get("product_price")

        
        
        product=Product(product_id,product_name,product_price)
        db.session.add(product)
        db.session.commit()
    
    return render_template('add.html')

    
@app.route('/search',methods=['POST','GET'])
def search():
    # if request.form:
    product=request.form.get("search")
    print(product)
    db_prodid=Product.query.all()
    # print(db_prodid.product_name)
    return render_template('display.html',product=db_prodid,search=product)
        # product=request.form.get("search")
        # return(product)
            # searchprod=Product.query.filter_by(product_id=product)
            
            # return render_template('index.html',product=searchprod)


@app.route('/display',methods=['POST','GET'])
def display():
    # if request.form:
    #     username=User(username=request.form.get("username"))
    #     email=User(email=request.form.get("email"))
    #     password=User(password=request.form.get("password"))
    #     # db.create_all()
    #     db.session.add(email)
    #     db.session.add(password)
    #     db.session.commit()
    
    products=Product.query.all()    
    logs=User.query.all()
    secret=0
    return render_template('display.html',logs=logs,products=products,secret=secret)
    #  return (request.form)  

@app.route('/')
def base ():
    return render_template('base.html')

# @app.route('/chart')
# def chart():
#     logs=User.query.all()
#     return render_template('chart.html',logs=logs)
if __name__ == "__main__":
   db.create_all()
#    manager.run()
   app.run(debug=True)