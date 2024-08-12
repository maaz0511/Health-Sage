import os
import pickle 
import numpy as np
from flask import Flask, render_template, request, redirect
from werkzeug.urls import url_quote

app = Flask(__name__, template_folder="templates")


# default page display
@app.route('/')
def homepage():
    return render_template("dashboard.html")




model1 = pickle.load(open("diabetes.pkl","rb"))
model2 = pickle.load(open("heart.pkl","rb"))
model3 = pickle.load(open("pcos.pkl","rb"))

# default page display
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

# about page
@app.route('/about')
def about():
    return render_template('about.html')


# prediction page
@app.route('/prediction')
def prediction():
    return render_template('prediction.html')


# precautions page
@app.route('/precautions')
def precautions():
    return render_template('precautions.html')


# information page
@app.route('/information')
def information():
    return render_template('information.html')

# blood donation page
@app.route('/blood_donation')
def blood_donation():
    return render_template('blood_donation.html')

# symptoms page
@app.route('/symptoms')
def symptoms():
    return render_template('symptoms.html')

# video page
@app.route('/video')
def video():
    return render_template('video.html')


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
          if g.user:
            res1= "You are probable of getting affected. Kindly seek medical advice."
            return render_template("diab_result.html",pregnancy=d1, glucose=d2, insulin=d3, bmi=d4, age=d5, result=res1, mess=var1)   
          return redirect("/loginpage")
          
      else:
          if g.user:
            res1 = "You are less probable of getting affected."
            return render_template("diab_result.html",pregnancy=d1, glucose=d2, insulin=d3, bmi=d4, age=d5, result=res1, mess=var1)   
          return redirect("/loginpage")
               
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