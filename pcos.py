import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import chi2, SelectKBest
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle


df=pd.read_csv(r"C:\Users\mohdm\Desktop\Health_Sage\pcos.csv")
X=df.iloc[:, :-1]
y=df.iloc[:, -1]


#imputing missing values
imputer = SimpleImputer(strategy='most_frequent')
X_imputed = imputer.fit_transform(X)
X = pd.DataFrame(X_imputed, columns=X.columns)
#print(X)

#selecting best features and print with their columns names
selector = SelectKBest(score_func = chi2, k=8)
X_select = selector.fit_transform(X,y)
selected = selector.get_support(indices=True)
X = pd.DataFrame(X_select, columns=X.columns[selected])
print(X.columns)


#Random Forest Model
from sklearn.ensemble import RandomForestRegressor
rfg = RandomForestRegressor(n_estimators = 100, random_state = 1)
rfg.fit(X,y)
prd = rfg.predict(X).round()


model = open("pcos.pkl","wb")
pickle.dump(rfg, model)
model.close()

