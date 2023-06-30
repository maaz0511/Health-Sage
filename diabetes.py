import pandas as pd
import numpy as np
import pickle

# handling missing values
from sklearn.impute import SimpleImputer

# outliers 
import matplotlib.pyplot as plt
import seaborn as sns

# selection of best features
from sklearn.feature_selection import chi2, SelectKBest

# remove warnings
from warnings import filterwarnings
filterwarnings('ignore')

# f-score
from sklearn.metrics import classification_report

# model
from sklearn import linear_model
from sklearn.model_selection import cross_val_score


# accuracy
from sklearn.metrics import accuracy_score


#importing dataset and separte the test class
df = pd.read_csv(r"C:\Users\mohdm\Desktop\Health_Sage\diabetes.csv")

# check for duplicate values
duplicate = df.duplicated()

# drop duplicate values if present
if duplicate.any():
    # print("Duplicate values exist in the DataFrame.")
    drop_duplicate = df.drop_duplicates()

#check for null values
check_null = df.isnull()

# fill the null values if present
if df.isnull().any().any():
    #imputing missing values
    imputer = SimpleImputer(strategy='most_frequent')
    df_imputed = imputer.fit_transform(df)
    df = pd.DataFrame(df_imputed, columns=df.columns)
    #print(X)
'''
# checking for outliers using box plot
sns.boxplot(data=df) # Create a box plot with customized figure
plt.title("Outliers") # Set plot title
plt.xlabel("X-axis") # Set axes labels
plt.ylabel("Y-axis") # Set axes labels
plt.show()
'''

# removing outline in Pregnancies
df = df[df["Pregnancies"]<12]

# removing outlier in Glucose
df = df[(df["Glucose"]>60) & (df["Glucose"]<150)]

# removing outline in Insulin
df = df[df["Insulin"]< 250]

# removing outline in BMI
df = df[(df["BMI"]< 45) & (df["BMI"]>10)]

# removing outline in Age
df = df[df["Age"]<51]

'''
# display after removing outliers  using box plot
sns.boxplot(data=df) # Create a box plot with customized figure
plt.title("Outliers") # Set plot title
plt.xlabel("X-axis") # Set axes labels
plt.ylabel("Y-axis") # Set axes labels
plt.show()
'''

# extracting target from rest of the dataset
X=df.iloc[:, :-1]
y=df.iloc[:, -1]

#selecting best features using kbest and chi2
selector = SelectKBest(score_func = chi2, k=5)
X_new = selector.fit_transform(X,y)
selected = selector.get_support(indices=True)
X_new = pd.DataFrame(X_new, columns=X.columns[selected])
# print(X_new.columns) # Print the selected features

# print(X.columns, X_new.columns)
'''# spliting dataset into train and test parts 
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_new,y,test_size=0.7)'''

# Checking and building Logistic Regression Model

logr = linear_model.LogisticRegression(C=1)
logr.fit(X_new,y) # fit the training data into the model
prd = logr.predict(X_new).round() # model predict via test data
# acc = accuracy_score(y, prd) # gives the accuracy

# print("Logistic Regression Accuracy Score = ", acc) # prints the accuracy of model
# print(classification_report(y_test, prd)) # prints the f-score 


# making pickle file
model = open("diabetes.pkl","wb")
pickle.dump(logr, model)
model.close()

