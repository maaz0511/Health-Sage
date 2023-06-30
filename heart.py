import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import chi2, SelectKBest
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import numpy as np
# outliers 
import matplotlib.pyplot as plt
import seaborn as sns
# remove warnings
from warnings import filterwarnings
filterwarnings('ignore')

#loading the dataset
df = pd.read_csv(r'C:\Users\mohdm\Desktop\Health_Sage\heart.csv')

#Rename the variables
df = df.rename(columns={"age":"Age", "sex":"Gender","cp": "ChestPain", "trestbps": "BloodPressure", "fbs": "FastingBloodSugar", "restecg":"ECG","thalach":"HeartRate"
                        ,"exang":"Exercise Induced","oldpeak":"Depression","ca": "Vessels", "chol": "Cholesterol","thal":"ThalliumStressTest" })
# print(df.columns)

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
    # print("Null values existed")
    #imputing missing values
    imputer = SimpleImputer(strategy='most_frequent')
    df_imputed = imputer.fit_transform(df)
    df = pd.DataFrame(df_imputed, columns=df.columns)
    #print(X)
'''
# recheck for null values
if df.isnull().any().any():
    print("Null values existed")
else:
    print("Null values not existed")
'''

# outliers in selected features
sns.boxplot(data=df) # Create a box plot with customized figure
plt.title("Outliers") # Set plot title
plt.xlabel("X-axis") # Set axes labels
plt.ylabel("Y-axis") # Set axes labels
# plt.show()

# removing outlier from BloodPressure
df = df[df["BloodPressure"]<160]

# removing outlier from Cholesterol
df = df[df["Cholesterol"]<390]

# removing outlier from HeartRate
df = df[df["HeartRate"]>80]

# removing outlier from Depression
df = df[df["Depression"]<4]

# removing outlier from Vessels
df = df[df["Vessels"]<3]

# outliers in dataset
sns.boxplot(data=df) # Create a box plot with customized figure
plt.title("Outliers") # Set plot title
plt.xlabel("X-axis") # Set axes labels
plt.ylabel("Y-axis") # Set axes labels
# plt.show()


# extracting target from rest of the dataset
X = df.iloc[:,0:13]
y = df.iloc[:,13]

#selecting best features and print with their columns names
selector = SelectKBest(score_func = chi2, k=8)
X_new = selector.fit_transform(X,y)
selected = selector.get_support(indices=True)
X_new = pd.DataFrame(X_new, columns=X.columns[selected])
# print(X_new.columns)

# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X_new,y,test_size=0.7)

#Random Forest Model
from sklearn.ensemble import RandomForestRegressor
rfg = RandomForestRegressor(n_estimators = 50, random_state = 1)
rfg.fit(X_new, y)
prd4 = rfg.predict(X_new)


model = open("heart.pkl", "wb")
pickle.dump(rfg, model)
model.close()




