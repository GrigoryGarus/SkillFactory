import numpy as np
import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
from collections import Counter

data = pd.read_csv('movie_bd_v5.csv')
print(data.sample(5))
print(data.columns)
print(data['budget'].max())
#log_win = log[log['user_id'] == 'NaN']

print(data['original_title'][data['budget']==data['budget'].max()])
print(data['original_title'][data['runtime']==data['runtime'].max()])
print(data['original_title'][data['runtime']==data['runtime'].min()])
#print(data2['original_title'])