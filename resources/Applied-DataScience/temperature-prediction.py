import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model

da=pd.read_csv('test.txt',delimiter='\\t')


X_train=da['Obs']
y_train=da['Temperature']
z_train=da['Humidity']
X_test=np.asarray([72,73,74,75,76,77,78,79])

X_train=X_train.values.reshape((-1,1))
y_train=y_train.values.reshape((-1,1))
z_train=z_train.values.reshape((-1,1))
X_test=X_test.reshape((-1,1))

poly = PolynomialFeatures(degree=4)
X = poly.fit_transform(X_train)
Xt = poly.fit_transform(X_test)

clf = linear_model.LinearRegression(n_jobs=-1)
clf.fit(X, y_train)
pred=clf.predict(Xt)
dfg=clf.predict(X)
print("Temperature Forecast")
print(pred)

poly1 = PolynomialFeatures(degree=3)
X1 = poly1.fit_transform(X_train)
Xt1 = poly1.fit_transform(X_test)

fg = linear_model.LinearRegression(n_jobs=-1)
fg.fit(X1,z_train)
pred1=fg.predict(Xt1)
dfg1=fg.predict(X1)
print("Humidity Forecast")
print(pred1)


fig=plt.figure()

plt1=fig.add_subplot(121,xlabel='Observations',ylabel='Temperature',title='Temperature Analysis')
plt1.plot(da['Obs'],da['Temperature'],label='Temperature Recorded')
plt1.plot(da['Obs'],dfg,color='g')
plt1.plot(X_test,pred,color='r',label='Forecast')
plt1.legend()


plt2=fig.add_subplot(122,ylim=(30,100),xlabel='Observations',ylabel='Humidity in %',title='Humidity Analysis')
plt2.plot(da['Obs'],da['Humidity'],label='Humidity Recorded')
plt2.plot(da['Obs'],dfg1,color='g')
plt2.plot(X_test,pred1,color='r',label='Forecast')
plt2.legend()

plt.show()