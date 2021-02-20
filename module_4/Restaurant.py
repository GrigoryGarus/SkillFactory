import pandas as pd
import re
from collections import Counter
import operator
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('main_task.xls')

print(df.info())
print(df.columns)


# for column in df.columns:
#     print(type(df[column].iloc[0]))


print('Уникальных цен', len(df['Price Range'].unique()))
print(df['Price Range'].head(5))
print('Средняя цена', len(df['Price Range'][df['Price Range'] == '$$ - $$$']))
print('Уникальных городов', len(df['City'].unique()))
print('Уникальных кухонь', len(df['Cuisine Style'].unique()))



print(df.groupby(['City', 'Cuisine Style']).size())

#замена пробелов в колонках
df.columns = df.columns.str.replace(' ', '_')
print(df.columns)
print(df.info())
# функция замены NaN среднее по городу для соответствующего города
def change_value(x):
    if pd.isna(x[1]):  # если в 'Number_of_Reviews'(x[1]) находится NaN,
        return city_mean_dict[x[0]] # вызываем словарь передаем ему ключ - город из City(x[0]) и получаем среднее для этого города
    else:
        return x[1]
# df = pd.read_csv('main_task.xls')
# df = df.rename(columns={'Number of Reviews': 'Number_of_Reviews'})
# создаем словарь, где ключ: город, значение: среднее по городу
city_mean_dict = dict(df.groupby('City')['Number_of_Reviews'].mean())
# Производим замену NaN на среднее
df['Number_of_Reviews'] = df[['City', 'Number_of_Reviews']].apply(change_value, axis=1)

print(df.info())

#НОВЫЕ ПРИЗНАКИ
#количество видов кухонь
#переводим стр в лист кухни
def to_list(str):
    li = re.split(", ", str[1:-1])
    li_f = []
    for w in li:
        li_f.append(w[1:-1])
    return li_f
#print(to_list("[212, 1AA, 1BB1]"))
df['Cuisine_Style'] = df['Cuisine_Style'].fillna(value = 'Non')
df['Cuisine_Style'] = df['Cuisine_Style'].apply(lambda x: to_list(x))
#подсчет количества видов кухонь
df['Cuisine_Style_Number'] = df['Cuisine_Style'].apply(lambda x: len(x))
#print(df['Cuisine_Style_Number'])
#количество видов кухонь############################

#диапазон цен в цифрах
def price_to_number(string):
    if string == "$":
        return 1
    elif string == "$$ - $$$":
        return 2
    elif string == "$$$$":
        return 3
    else:
        pass

df['Price_Range_Number'] =df['Price_Range'].apply(price_to_number)
# print(df.info())
# print(df['Price_Range'].head(5))
df['Price_Range_Number'] = df['Price_Range_Number'].fillna(value = df['Price_Range_Number'].mode())
print(df['Price_Range_Number'].head(5))

#print(df['City'].head(25))


#количество других ресторанов в городе
rest_city = df['City'].value_counts().to_dict()
def another_rest_city_number(current_city):
    count = 0
    for city in rest_city:
        if city == current_city:
            count = rest_city.get(city)
            #print(count)
    return count

df['another_rest_city_number'] = df['City'].apply(another_rest_city_number)
print('Другие рестораны',df['another_rest_city_number'].head(5))

#длинная 2х отзывов
df['review_len'] = df['Reviews'].apply(lambda x: len(x))
print('!!!',df['review_len'].head(5))

#разнице по времени между самым свежим отзовом и текущим

date_to_delta = datetime(2019, 1, 1)
date_to_delta1 = datetime(2020, 1, 1)
print(date_to_delta)
difference = date_to_delta1 - date_to_delta
print("Int", type(difference.days))

avg_delta = []


def review_to_date(string):
    date_to_delta = datetime(2019, 1, 1)
    ##Задаем паттерн для даты
    pattern = re.compile("A")
    pattern2 = re.compile('\'\d+\/\d+\/\d+\'?')
    d = pattern2.findall(string)
    if len(d)>1:
        date = d[0]
        date = date[1:-1]
        date2 = d[1][1:-1]
        dt = datetime.strptime(date, '%m/%d/%Y')
        dt2 = datetime.strptime(date2, '%m/%d/%Y')
        res = (dt - dt2).days

    else:
        res = 150



    return res

#print(review_to_date("A A B"))
df['Time_delta'] = df['Reviews'].apply(review_to_date)

print(df['Time_delta'].head(5))





#Dummy - переменные

# Кухни

#лист 20 чамых частых кухонь
flat_list = [item for sublist in df['Cuisine_Style'] for item in sublist]
dirs_count = dict(Counter(flat_list))

top20_Cuisine = dict(Counter(dirs_count).most_common(10))
top20_Cuisine_list = []
print("Среднее",top20_Cuisine)
for cuisine in top20_Cuisine:
    if cuisine != "":
        top20_Cuisine_list.append(cuisine)

print(top20_Cuisine_list)


#current_cuisine = "Vegetarian Friendly"
def contain_top20(cuis):
    res = 0
    for c in cuis:
        if c == cuisine1:
            res = 1
            break

    return  res




for cuisine1 in top20_Cuisine_list:
    #current_cuisine = cuisine
    df[cuisine1] = df['Cuisine_Style'].apply(contain_top20)


print(df["Vegetarian Friendly"].head(55))
print(df['Cuisine_Style'].head(5))

# Добавим признак - численность население (по данным из Википедии)

population = {
    'London' : 8909081,
    'Paris' : 2148271,
    'Madrid' : 3223334,
    'Barcelona' : 1620343,
    'Berlin' : 3769495,
    'Milan' : 1399860,
    'Rome' : 2860009,
    'Prague' : 1324277,
    'Lisbon' : 505526,
    'Vienna' : 2600000,
    'Amsterdam' : 872680,
    'Brussels' : 1208542,
    'Hamburg' : 1845229,
    'Munich' : 1484226,
    'Lyon' : 516092,
    'Stockholm' : 975904,
    'Budapest' : 1752286,
    'Warsaw' : 1793579,
    'Dublin' : 554554,
    'Copenhagen' : 794128,
    'Athens' : 664046,
    'Edinburgh' : 488050,
    'Zurich' : 415215,
    'Oporto' : 287591,
    'Geneva' : 201818,
    'Krakow' : 779115,
    'Oslo' : 697549,
    'Helsinki' : 656229,
    'Bratislava' : 437726,
    'Luxembourg' : 626108,
    'Ljubljana' : 295504
}

df['Population'] = df['City'].map(population)

# Добавим признак - индекс покупательской способности согласно рейтингу Numbeo (2018)

purchasing_power_index = {
    'London' : 24,
    'Paris' : 22,
    'Madrid' : 23,
    'Barcelona' : 30,
    'Berlin' : 8,
    'Milan' : 40,
    'Rome' : 37,
    'Prague' : 31,
    'Lisbon' : 48,
    'Vienna' : 21,
    'Amsterdam' : 19,
    'Brussels' : 15,
    'Hamburg' : 7,
    'Munich' : 6,
    'Lyon' : 70,
    'Stockholm' : 13,
    'Budapest' : 51,
    'Warsaw' : 29,
    'Dublin' : 27,
    'Copenhagen' : 10,
    'Athens' : 53,
    'Edinburgh' : 16,
    'Zurich' : 2,
    'Oporto' : 42,
    'Geneva' : 3,
    'Krakow' : 36,
    'Oslo' : 17,
    'Helsinki' : 9,
    'Bratislava' : 39,
    'Luxembourg' : 4,
    'Ljubljana' : 32
}

df['purchasing_power'] = df['City'].map(purchasing_power_index)

# Добавим числовой признак 'Population Per Restaurant' = 'Population' / 'Restaurants Count'
df['Population_Per_Restaurant'] = df['Population'] / df['another_rest_city_number']




#удаление нечисловых
df = df.drop(['City', 'Cuisine_Style', 'Price_Range', 'Reviews', 'URL_TA', 'ID_TA'], axis=1)

df = df.fillna(df.mean())
print(df.info())
df.to_csv(r'main_task.csv')


# df.insert(loc=0, column='test', value=0) #первая пустая сторока
# sns.pairplot(df, y_vars=["Rating"])
# plt.show()