import pandas as pd
from sklearn.model_selection import train_test_split

data = pd.read_csv(r'D:\workspace\ImportingData Python\BANG-B-Dataset\03_Item_Information_Data.csv')

print(data.head())

x = data['Item ID']
y = data['Rate']

# split data
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.2, random_state=42)

fit
fit_transform
transform