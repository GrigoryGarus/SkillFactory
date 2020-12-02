import numpy as np
import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
from collections import Counter
import operator

data = pd.read_csv('movie_bd_v5.csv')
#print(data.sample(5))
#print(data.describe())
print(data.columns)
#print(data['budget'].max())


#print(data['original_title'][data['budget']==data['budget'].max()]) #1
#print(data['original_title'][data['runtime']==data['runtime'].max()]) #2
#print(data['original_title'][data['runtime']==data['runtime'].min()]) #3
#print(data['runtime'].mean()) #4
#print(data['runtime'].median()) #5

data['profit'] = np.subtract(data['revenue'], data['budget'])
#print(data['original_title'][data['profit']==data['profit'].max()]) #6
#print(data['original_title'][data['profit']==data['profit'].min()]) #7
#print(len(data[data['profit']>0])) #8
#data2008 = data[data['release_year'] == 2008]
#print(data2008['original_title'][data2008['profit']==data2008['profit'].max()]) #9
#data2012 = data[(data['release_year']>= 2012) & (data['release_year']<= 2014)]
#print(data2012['original_title'][data2012['profit']==data2012['profit'].min()]) #10


def genres_max (gen):
    genres = []
    flat_list = []
    for genre in gen:
        genres.append(genre.split("|"))

    for sublist in genres:
        for item in sublist:
            flat_list.append(item)
    genres_count = dict(Counter(flat_list))
    res = max(genres_count.items(), key=operator.itemgetter(1))[0]

    return res

#print(genres_max(data['genres'])) #11

def genres_profit (gen):
    genres = []
    flat_list = []
    for genre in gen['genres'][gen['profit']>0]:
        genres.append(genre.split("|"))

    for sublist in genres:
        for item in sublist:
            flat_list.append(item)
    genres_count = dict(Counter(flat_list))
    res = max(genres_count.items(), key=operator.itemgetter(1))[0]

    return res

#print(genres_profit(data)) #12

def director_max_revenue (gen):
    max_revenue = 0
    director_max = ''
    rev_sum = 0
    for director in gen['director']:
        for rev in gen['revenue'][gen['director']==director]:
            rev_sum+=rev
        if rev_sum>max_revenue:
            max_revenue = rev_sum
            director_max = director
        rev_sum = 0


    return director_max

print(director_max_revenue(data)) #13













