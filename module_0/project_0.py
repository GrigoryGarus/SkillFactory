import numpy as np

count = 0  # счетчик попыток
number = np.random.randint(1, 101)  # загадали число

#number = 78

def score_game(game_core):
    '''Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число'''
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(1,101, size=(1000))
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return(score)

def game_core_v2(number):
    '''Сначала устанавливаем любое random число, а потом уменьшаем или увеличиваем его в зависимости от того, больше оно или меньше нужного.
       Функция принимает загаданное число и возвращает число попыток'''
    count = 1
    predict = np.random.randint(1,101)
    while number != predict:
        count+=1
        if number > predict: 
            predict += 1
        elif number < predict: 
            predict -= 1
    return(count) # выход из цикла, если угадали

def game_core_v3(number):
    '''Сначала устанавливаем любое random число, а потом уменьшаем или увеличиваем его в зависимости от того, больше оно или меньше нужного.
       Функция принимает загаданное число и возвращает число попыток'''
    count = 1
    predict = 50
    last_top = 100
    last_bottom = 0
    while (last_top - last_bottom) > 1:
        count+=1
        if number > predict:
            last_bottom = predict
            predict += round((last_top-last_bottom)/2)

        elif number < predict:
            last_top = predict
            predict -= round((last_top-last_bottom)/2)
        else:
            return count

    for i in range(last_bottom, last_top+1):
        count+=1
        predict = i
        if predict == number:
            break
        #print("!!")
    return(count) # выход из цикла, если угадали
print(score_game(game_core_v3))
print(game_core_v3(number))