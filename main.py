import pymongo
from pymongo import MongoClient
from flask import *
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client['expense_tracker']

collection =db["expenses"]
cred=db["credentials"]
app= Flask(__name__)
app.secret_key = "some-secret-key"

@app.route('/')
def index():
    if "status" not in session:  
        session["status"] = False

    expenses = list(collection.find({ "username":session["username"]  }) ) 
    total_expense = sum(int(exp.get("amount", 0)) for exp in expenses) 
    if not session["status"]:
        return render_template("login.html")
    else:
        return render_template("expense_tracker.html", expenses=expenses, total_expense=total_expense)
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        mail=request.form["email"]
        pass1=request.form["password"]
        pass2=request.form["confirm_password"]
        cred.insert_one({"email": mail, "password": pass1})
        return redirect('/login')
    else:
        return render_template("register.html")      





@app.route('/login', methods=['POST','GET'])
def login():
     session["status"] = False 
     if request.method=='POST':
         uer=request.form["username"]
         pa=request.form["password"]
         username = cred.find_one({"email": uer})
         passw=cred.find_one({"password": pa})
         user = cred.find_one({"email": uer, "password": pa})
         if user:
           session["status"] = True
           session["username"] = uer
           return redirect('/')
         else:
           return render_template("login.html", error="Invalid username or password")

     else:

         
        return render_template("login.html", error="Invalid username or password")
       
@app.route('/add_expense',methods=['POST'])
def add_expense():
    
    if request.method=='POST':
       amt= request.form["amount"]
       cat=request.form["category"]
       date=request.form["date"]
       note=request.form["notes"]
    
       expense = {
            "username": session["username"],
            "amount": amt,
            "category": cat,
            "date": date,
            "note": note
        }
    collection.insert_one(expense)
    return redirect('/')  

app.run(debug=True)     
       
       




