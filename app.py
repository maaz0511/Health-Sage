import os
import pickle 
import numpy as np
from pymongo import MongoClient
from flask import Flask, render_template, request, url_for, session, redirect,redirect,g, request

app = Flask(__name__, template_folder="templates")

# database connection
app.secret_key = os.urandom(24)
client = MongoClient("mongodb://localhost:27017/")
db = client["user_info"]
collection = db["user_data"]

# default page display
@app.route('/')
def homepage():
    return render_template("register.html")

# login page display
@app.route('/loginpage')
def loginpage():
        return render_template("login.html")

# registeration page display
@app.route('/registerationpage')
def registerationpage():
        return render_template("register.html")

# registeration part
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    document = {"name": name, "email": email, "password": password}
    collection.insert_one(document)
    return redirect('/loginpage')

# login part
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        session.pop('user',None)

    email = request.form['email']
    password = request.form['password']

    user = collection.find_one({'email': email})

    if user is not None:
        # Check if the password is correct
            if user['password'] == password:
                session['user'] = user['name']
                # Redirect to the dashboard
                return redirect("/dashboard")
            
    return render_template('login.html',msg="Incorrect Username or Password")

# dashboard page
@app.route('/dashboard')
def dashboard():
    if g.user:
        return render_template('dashboard.html',msg=session['user'])
    return redirect("/")
    
@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/logout')
def logout():
    session.clear()    
    return redirect('/loginpage')

model1 = pickle.load(open("diabetes.pkl","rb"))
model2 = pickle.load(open("heart.pkl","rb"))
model3 = pickle.load(open("pcos.pkl","rb"))

# about page
@app.route('/about')
def about():
    if g.user:
        return render_template('about.html',msg=session['user'])
    return redirect("/loginpage")

# prediction page
@app.route('/prediction')
def prediction():
    if g.user:
        return render_template('prediction.html',msg=session['user'])
    return redirect("/loginpage")

# precautions page
@app.route('/precautions')
def precautions():
    if g.user:
        return render_template('precautions.html',msg=session['user'])
    return redirect("/loginpage")

# information page
@app.route('/information')
def information():
    if g.user:
        return render_template('information.html',msg=session['user'])
    return redirect("/loginpage")

# blood donation page
@app.route('/blood_donation')
def blood_donation():
    if g.user:
        return render_template('blood_donation.html',msg=session['user'])
    return redirect("/loginpage")

# symptoms page
@app.route('/symptoms')
def symptoms():
    if g.user:
        return render_template('symptoms.html',msg=session['user'])
    return redirect("/loginpage")

# video page
@app.route('/video')
def video():
    if g.user:
        return render_template('video.html',msg=session['user'])
    return redirect("/loginpage")

# diabetes prediction
@app.route("/predict/diabetes", methods=['POST'])
def diabetes():
   if request.method =='POST':
      d1 = int(request.form['pregnancy'])
      d2 = int(request.form['glucose'])
      d3 = int(request.form['insulin'])
      d4 = int(request.form['bmi'])
      d5 = int(request.form['age'])
      
      arr1 = np.array([[d1, d2, d3, d4, d5]])
      var1 = model1.predict(arr1)

      if var1>0.75:
          res1= "You are probable of getting affected. Kindly seek medical advice."
          return render_template("diab_result.html",pregnancy=d1, glucose=d2, insulin=d3, bmi=d4, age=d5, result=res1, mess=var1)   
      else:
          res1 = "You are less probable of getting affected."
          return render_template("diab_result.html",pregnancy=d1, glucose=d2, insulin=d3, bmi=d4, age=d5, result=res1, mess=var1) 

       
# heart prediction
@app.route("/predict/heart", methods=['POST'])
def heart():
   if request.method =='POST':
      h1 = int(request.form['age'])
      h2 = int(request.form['chestpain'])
      h3 = int(request.form['bloodpressure'])
      h4 = int(request.form['cholesterol'])
      h5 = int(request.form['heartrate'])
      h6 = int(request.form['exercise'])
      h7 = int(request.form['depression'])
      h8 = int(request.form['vessels'])
      
      arr2 = np.array([[h1, h2, h3, h4, h5, h6, h7, h8]])
      var2 = model2.predict(arr2)


      if var2>0.75:
          res2= "You are probable of getting affected. Kindly seek medical advice."
          return render_template("heart_result.html",v1=h1, v2=h2, v3=h3, v4=h4, v5=h5, v6=h6, v7=h7, v8=h8, result=res2, mess=var2)
      else:
          res2 = "You are less probable of getting affected."
          return render_template("heart_result.html",v1=h1, v2=h2, v3=h3, v4=h4, v5=h5, v6=h6, v7=h7, v8=h8, result=res2,mess=var2) 
          
# pcos prediction
@app.route("/predict/pcos", methods=['POST'])
def pcos():
   if request.method =='POST':
      p1 = int(request.form['v1'])
      p2 = int(request.form['v2'])
      p3 = int(request.form['v3'])
      p4 = int(request.form['v4'])
      p5 = int(request.form['v5'])
      p6 = int(request.form['v6'])
      p7 = int(request.form['v7'])
      p8 = int(request.form['v8'])
      
      arr3 = np.array([[p1, p2, p3, p4, p5, p6, p7, p8]])
      var3 = model3.predict(arr3)

      if var3>0.75:
          res3= "You are probable of getting affected. Kindly seek medical advice."
          return render_template("pcos_result.html",v1=p1, v2=p2, v3=p3, v4=p4, v5=p5, v6=p6, v7=p7, v8=p8, result=res3,mess=var3)
      else:
          res3 = "You are less probable of getting affected."
          return render_template("pcos_result.html",v1=p1, v2=p2, v3=p3, v4=p4, v5=p5, v6=p6, v7=p7, v8=p8, result=res3,mess=var3)


if __name__ == '__main__':
    app.run(debug=True)