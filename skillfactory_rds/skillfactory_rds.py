import numpy as np
import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
from collections import Counter
import operator
import re

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

def director_max_action (data):
    directors_action = {}
    count = 0
    for director in data['director']:
        for action in data['genres'][data['director']==director]:
            if re.search('Action', action):
                count+=1

        #directors_action.update({director: count})
        directors_action[director] = count
        count = 0


    sorted_action = sorted(directors_action.items(), key=operator.itemgetter(1))
    res = max(directors_action.items(), key=operator.itemgetter(1))[0]

    return res

#print(director_max_action(data)) #14


def director_max_action1 (data):
    directors_action = {}
    count = 0
    count_max = 0
    director_max = ''
    dir = ''
    for director in data['director']:
        for dir in director.split("|"):
            for action in data['genres'][data['director']==dir]:
                if re.search('Action', action):
                    count+=1

        #directors_action.update({director: count})
        if count > count_max:
            count_max = count
            director_max = dir

        directors_action[dir] = count
        count = 0


    sorted_action = sorted(directors_action.items(), key=operator.itemgetter(1))
    res = max(directors_action.items(), key=operator.itemgetter(1))[0]

    return director_max

#print(director_max_action1(data)) #14


def director_max_action2 (data):
    dirs = []
    data_action = data[data['genres'].str.contains('Action')]
    for director in data_action['director'].str.split(pat="|"):
        dirs.append(director)

    flat_list = [item for sublist in dirs for item in sublist]
    dirs_count = dict(Counter(flat_list))
    sorted_dirs = sorted(dirs_count.items(), key=operator.itemgetter(1))
    res = max(dirs_count.items(), key=operator.itemgetter(1))[0]

    return res

print(director_max_action2(data)) #14


def acter_max_revenue (data):
    acters = []
    acter_max = ""
    count_rev = 0
    count_max = 0
    data_2012 = data[data['release_year'] == 2012]

    for acter in data_2012['cast'].str.split(pat="|"):
        acters.append(acter)

    flat_list = [item for sublist in acters for item in sublist]
    for acter in flat_list:
        for rev in data_2012['revenue'][data_2012['cast'].str.contains(acter)]:
            count_rev+=rev
        if count_rev > count_max:
            count_max = count_rev
            acter_max = acter
        count_rev = 0

    return acter_max

print(acter_max_revenue(data)) #15

def acter_high (data):
    acters = []
    data_high = data[data['budget'] > data['budget'].mean()]

    for acter in data_high['cast'].str.split(pat="|"):
        acters.append(acter)

    flat_list = [item for sublist in acters for item in sublist]
    dirs_count = dict(Counter(flat_list))
    sorted_dirs = sorted(dirs_count.items(), key=operator.itemgetter(1))
    res = max(dirs_count.items(), key=operator.itemgetter(1))[0]

    return res

print(acter_high(data)) #16

def acter_cage (data):
    genras = []
    data_cage = data[data['cast'].str.contains("Nicolas Cage")]

    for genre in data_cage['genres'].str.split(pat="|"):
        genras.append(genre)

    flat_list = [item for sublist in genras for item in sublist]
    dirs_count = dict(Counter(flat_list))
    sorted_dirs = sorted(dirs_count.items(), key=operator.itemgetter(1))
    res = max(dirs_count.items(), key=operator.itemgetter(1))[0]
    return res

print(acter_cage(data)) #17


def paramount (data):
    genras = []
    profit = 0
    profit_min = 0
    data_paramount = data[data['production_companies'].str.contains("Paramount Pictures")]

    for profit in data_paramount['profit']:
        if profit < profit_min:
            profit_min = profit
    res = data_paramount['original_title'][data_paramount['profit'] == profit_min]


    return res

print(paramount(data)) #18


def scott (data):
    profits = {}
    data_scott = data[data['director'].str.contains("Ridley Scott")]

    for name in data_scott['original_title']:
        profits[name] = int(data_scott['profit'][data_scott['original_title'] == name])


    dirs_count = dict(Counter(profits))
    sorted_dirs = sorted(dirs_count.items(), key=operator.itemgetter(1))
    res = max(dirs_count.items(), key=operator.itemgetter(1))[0]



    return res


print(scott(data)) #18


def year_profit (data):
    years = []
    profits = {}

    for year in data['release_year']:
        years.append(year) if year not in years else years

    for year in years:
        for rev in data['revenue'][data['release_year'] == year]:

            if year in profits:
                profits[year] += rev

            else:
                # profits[year] = int(data['revenue'][data['release_year'] == year])
                profits[year] = rev

    dirs_count = dict(Counter(profits))
    sorted_dirs = sorted(dirs_count.items(), key=operator.itemgetter(1))
    res = max(dirs_count.items(), key=operator.itemgetter(1))[0]



    return res


print(year_profit(data)) #19


def year_profit1 (data):
    years = []
    profits = {}

    for year in data['release_year']:
        years.append(year) if year not in years else years

    for year in years:
        for rev in data['profit'][data['release_year'] == year]:

            if year in profits:
                profits[year] += rev

            else:
                # profits[year] = int(data['revenue'][data['release_year'] == year])
                profits[year] = rev

    dirs_count = dict(Counter(profits))
    sorted_dirs = sorted(dirs_count.items(), key=operator.itemgetter(1))
    res = max(dirs_count.items(), key=operator.itemgetter(1))[0]



    return res

data_wb = data[data['production_companies'].str.contains("Warner Bros")]
print(year_profit1(data_wb)) #20


def month_sum (data):
    data_month = []
    for date in data['release_date']:
        data_month.append(re.search(r'\d+', date).group())

    dirs_count = dict(Counter(data_month))
    sorted_dirs = sorted(dirs_count.items(), key=operator.itemgetter(1))
    res = max(dirs_count.items(), key=operator.itemgetter(1))[0]



    return res

print(month_sum(data)) #21


def summer (data):
    count = 0
    for date in data['release_date']:
        if int(re.search(r'\d+', date).group()) == 6 or\
                int(re.search(r'\d+', date).group())== 7 or\
                int(re.search(r'\d+', date).group())==8:
            count+=1


    return count

print(summer(data)) #22

"""

"""












