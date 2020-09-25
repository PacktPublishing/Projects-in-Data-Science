from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd 
 
file = r'/Presidents.xls'
df = pd.read_excel('Presidents.xls')
 
# plot data
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','red','green','blue','orange','white','brown']
df['Occupation'].value_counts().plot(kind='pie',title='Occupation by President',colors=colors)
plt.show()

#Plot bar plot
df = df[df['% popular'] != 'NA()']
 
print( df['% popular'] )
df['% popular'].plot(kind='hist', bins=8, title='Popularity by President', facecolor='blue', alpha=0.5, normed=1)
plt.show()