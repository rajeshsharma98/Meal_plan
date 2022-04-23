import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import sklearn.preprocessing as pre

kaggle = pd.read_csv('./nutrition_kaggle.csv')
kaggle_copy = kaggle.copy() # copy of original data
kaggle.drop(['Unnamed: 0','serving_size'],inplace=True,axis=1)
clmns = kaggle.columns

# Remove all unit values like sodium = 9.00 mg then we need to remove mg
# Iterate over all column and if column data type is Object then remove all string characters present in column values
for i in clmns[1:]:
    if kaggle[i].dtype == 'O':
        kaggle[i] = kaggle[i].str.replace('[a-zA-Z]', '')
    else:
        continue

# Count null values in every column
(kaggle.isnull().sum(axis = 0)).sum()
kaggle = kaggle.fillna(0)
kaggle.fillna(9999,inplace=True)

kaggle = kaggle.set_index('name')
kaggle_new = pre.normalize(kaggle,norm='l1',axis=0)# normalize columns
kaggle_new.sum(axis=0)
kaggle_new = pre.normalize(kaggle_new,norm='l1',axis=1)# normalize rows
kaggle_new.sum(axis=1)
# reset index
kaggle = kaggle.reset_index('name')

kaggle_new = pd.DataFrame(kaggle_new,columns=kaggle.columns[1:])
kaggle_new = pd.merge(kaggle['name'],kaggle_new, left_index=True,right_index=True)
kaggle_new.to_csv('./dataset/STANDARD_VALUES.csv')
