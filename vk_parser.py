###VERSION 2.0
import vk
import sys
import time

users = []
user_ = []
save_arr = []
sex = ['Не указан','Женский','Мужской']
month = ['','января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']
counter = {'city':0,'country':0}
version = {
            'parser': '2.0b8',
            'smart_city' : '1.63'
            }
print('\aHottabbe followers parser\nFollow on me - https://vk.com/hottabbe\nParser version : %s\nSmart city module version : %s \n\n\n' % (version['parser'],version['smart_city']))
api = vk.API(vk.AuthSession(app_id='3265802', user_login=input ('Введите логин: '), user_password=input ('Введите пароль: '), scope='friends'), lang='ru', v = '5.62')
print('\n' * 50)
main = api.users.get(fields = 'country,city')[0]
main['city'] = main['city']['title']
main['country'] = main['country']['title']
print(main['first_name'] + ' ' + main['last_name'] + ' - Вход выполнен')
smart_search = int(input ('Включить умный подбор города (долго) (0/1/2)\n0 - выключить\n1 - включить\n2 - гибридный метод\n===> <===\r===>'))
start_date = time.time()
def bufer(user):
    time.sleep(0.5)
    print('\aОшибка vk.com - повтор')
    smart_city(user)
def smart_city (user):
    if user['deactivated'] == 'Страница активна':
        try:
            #### VAR BLOCK ####
            friends_list = []
            cities = {}
            friends_list = api.friends.get(user_id = user['id'],order = 'hints',fields = 'city')
            try:
                user['city']
            except KeyError:
                user['city'] = {
                                'title':'Не указано',
                                'id': 0
                                }

            #### MAIN CODE ####
            for friend in friends_list['items']:
                try:
                    friend['city']
                except KeyError:
                    continue
                else:
                    if friend['city']['title'] in cities:
                        cities[friend['city']['title']] += 1
                    else:
                        cities.update({friend['city']['title'] : 1})
            bigger ={'city': 'no name','count':-2}
        except vk.exceptions.VkAPIError:
           bufer(user)
        except Exception:
            print('Не удалось загрузить данные с vk.com.....Повтор')
        #### CHANGE CODE ####
        for key in cities:
            if cities[key] >= bigger['count']:
                bigger['city'] = key
                bigger['count'] = cities[key]
        try:
            percent = round(bigger['count']/(friends_list['count']+1) * 100,2)
        except UnboundLocalError:
            percent = 0
        time.sleep(0.3)
        if ((percent in range(15,35) and friends_list['count'] > 100) or percent > 35) and bigger['city'] != 'no name':
            if bigger['city'] != user['city']['title']:
                print('    '+ user['first_name']+ ' ' + user['last_name'] + ' : ' + user['city']['title'] + ' ===> ' + bigger['city'])
            return '%s (%s %s )' % (bigger['city'],str(percent),'%')
        else:
            return user['city']['title']
    else:
        return 'Недоступно'
    
    
def saver (gen,text):
    if gen == 1:
        save = open('followers.csv','w+',encoding = 'utf-8')
        save.write('Ссылка;Имя;Страна;Город;Пол;Дата рождения;Подписчиков;Состояние\n')
        save.close()
        return 'ok'
    if gen == 2:
        save = open('followers.csv','a',encoding = 'utf-8')
        for elem in text:
            save.write(elem)
        save.close()
        return 'ok'


def exe_builder():
    code = ''
    exe = open('code.js','r+')
    for every in exe:
        code += every
    exe.close()
    return code

def users_get ():
    counter_users = 0
    i = 0
    users_ = []
    users = {
            'users':{},
            'count':0
            }
    print('Получаю массив подписчиков')
    while users['count'] == 0:
        try:
            users = api.execute(code = exe_builder())
        except Exception:
            print('Ошибка доступа к vk.com..... Повтор\a')
    count = users['count']
    users = users['users']
    for every in users:
        for every_ in every:
            users_.append(every_)
    users = users_
    print('Маcсив подписчиков получен успешно\nВ нем содержится ' + str(count) + ' человек')
    save_arr = []    
    for user in users:
        user['name'] = user['first_name'] + ' ' + user['last_name']
        try:
            user['deactivated']        
        except KeyError:
            user['deactivated'] = 'Страница активна'
        else:
            if user['deactivated'] == 'deleted': user['deactivated'] = 'Пользователь удален'
            elif user['deactivated'] == 'banned': user['deactivated'] = 'Пользователь забанен'
            user['followers_count'] = 0
            user['city'] = {
                            'title':'Недоступно'
                            }
            user['country'] = {
                            'title':'Недоступно'
                            }
        if smart_search == 0 or user['deactivated'] != 'Страница активна':
            try:
                user['city'] = user['city']['title']
            except KeyError:
                if smart_search == 2:
                    if user['deactivated'] == 'Страница активна':
                        user['city'] = smart_city(user)
            except TypeError:
                input(str(user['city']))
        elif smart_search == 1:
            try:
                user['city'] = smart_city(user)
            except KeyError:
                try:
                    user['city'] = user['city']['title']
                except KeyError:
                   user['city'] = 'Не указано'
        try:
            if user['city'].split(' (')[0] == main['city']:
                counter['city'] += 1
        except Exception:
            continue
        try:
            if user['country']['title'] == main['country']:
                counter['country'] += 1
        except KeyError:
            user['country'] = 'Не указано'
        try:
            user['sex'] = sex[user['sex']]
        except KeyError:
            user['sex'] = 'Ошибка'
        try:
            user['bdate']
            bdate = user['bdate'].split('.')
            if len(bdate) > 2:
                user['bdate'] = bdate[0]+ ' ' + month[int(bdate[1])] + ' ' + bdate[2] + ' года'
            else:
                user['bdate'] = bdate[0]+ ' ' + month[int(bdate[1])]
        except KeyError:
            user['bdate'] = 'Не указано'
        counter_users += 1
        if counter_users%100 == 0:
            print('Обработано %s человек из %s' % (str(counter_users),str(count)))
        save_arr.append('https://vk.com/id%s;%s;%s;%s;%s;%s;%s;%s\n' % (user['id'],user['name'],user['country'],user['city'],user['sex'],user['bdate'],user['followers_count'],user['deactivated']))
    if saver(gen = 2,text = save_arr) == 'ok':
        print('Создание базы успешно завершено\nОбщая с вами страна у '+ str(counter['country']) + ' человек\nОбщий с вами город у '+ str(counter['city']) + ' человек\n')
        print('База создана за ' + str(round(time.time() - start_date,2)) + ' секунд')
    else:
        input('Ошибка')
        sys.exit()
    i+=1
    
saver(gen = 1,text = '')            
users_get()
input('')
        
