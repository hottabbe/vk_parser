import sys

sys.stdout.write('BOOTSTRAP...')


def printer(string, new_str, color):
    if new_str:
        sys.stdout.write(colored('\n%s\n' % string, colors[color]))
    else:
        sys.stdout.write(colored('\r%s\r%s' % (' ' * 90, string), colors[color]))


def cfg():
    lines = open('config.cfg', 'r+')
    for line in lines:
        line = line.split(':')
        line[1] = line[1].split('\n')[0]
        settings.update({line[0]: line[1]})
    lines.close()


import vk
import time
from termcolor import colored
import requests

users = []
user_ = []
save_arr = []
colors = ['red', 'green', 'white']
sex = ['Не указан', 'Женский', 'Мужской']
sex_man = {'ов', 'ев', 'ив', 'ин', 'ен', 'ov', 'ev', 'iv', 'in', 'en'}
sex_woman = [{'ова', 'ева', 'ива', 'ёва', 'ина', 'ена', 'ova', 'eva', 'iva', 'ina', 'ena'},
             {'ая', 'уя'}]
woman_names = {'а', 'я', 'a'}
month = ['', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября',
         'декабря']
counter = {'city': 0, 'country': 0}
settings = {}
version = {'parser': '2.2', 'smart_city': '2.0'}
fields = {'id', 'deactivated', 'name'}
cfg()
api = vk.API(
    vk.AuthSession(app_id='3265802', user_login=settings['login'], user_password=settings['pass'], scope='friends'),
    lang='ru', v='5.62')
main = api.users.get(fields='country,city')[0]
main['city'], main['country'] = main['city']['title'], main['country']['title']
smart_search = settings['smart']
start_date = time.time()
printer(colored('BOOTSTRAP COMPLETE - ' + main['first_name'] + ' ' + main['last_name'], 'green'), False, 1)


def smart(user):
    cities = {}
    friends_list = None
    while friends_list is None:
        try:
            smarty = api.execute(code=('var av = "";'
                                       'var i = 0;'
                                       'var percent = 0;'
                                       'var photos;'
                                       'var user = API.users.get({"user_ids" :%s,"fields":",photo_id"})[0];'
                                       'var friends = API.friends.get({"user_id":%s, "order":"hints", '
                                       '"fields":"city"}); '
                                       'var photo = API.photos.search({"q":"copy:photo"+user.photo_id}).count;'
                                       'if (photo > %s){percent = 20;}'
                                       'else if (photo == 0){percent = 0;}'
                                       'else {percent = 12;}'
                                       'photos = API.photos.getAll({"owner_id":user.id,"count":100});'
                                       'if(photos.count > 15){'
                                       'while (i < 15){photo = API.photos.search({"q":"copy:photo"+user.id + "_" + '
                                       'photos.items[i].id}).count; '
                                       'if(photo > 0){percent = percent + 100/photos.count;}'
                                       'i = i + 1;}}'
                                       'else if(photos.count < 15){'
                                       'while (i < photos.count){photo = API.photos.search({"q":"copy:photo"+user.id '
                                       '+ "_" + photos.items[i].id}).count; '
                                       'if(photo > 0){percent = percent + 100/photos.count;}'
                                       'i = i + 1;}}'
                                       'percent = percent + 50/friends.count;'
                                       'return {"fake": percent,"friends":friends};' % (
                                           user['id'], user['id'], settings['av_max_count'])))
            friends_list = smarty['friends']
        except vk.exceptions.VkAPIError:
            printer('\a[SMART] Очень много запросов в секунду....попробуйте увеличить таймаут', False, 0)
            time.sleep(5)
        except requests.ReadTimeout:
            printer('[SMART] Не удалось загрузить данные с vk.com.....Повтор', True, 0)
    try:
        user['city']
    except KeyError:
        user['city'] = {'title': 'Не указано', 'id': 0}
    for friend in friends_list['items']:
        try:
            if friend['city']['title'] in cities:
                cities[friend['city']['title']] += 1
            else:
                cities.update({friend['city']['title']: 1})
        except KeyError:
            continue
    bigger = {'city': 'no name', 'count': -2}

    for key in cities:
        if cities[key] >= bigger['count']: bigger['city'], bigger['count'] = key, cities[key]
    try:
        percent = round(bigger['count'] / (friends_list['count'] + 1) * 100, 2)
    except UnboundLocalError:
        percent = 0
    if ((percent in range(15, 35) and friends_list['count'] > 100) or percent > 35) and bigger['city'] != 'no name':
        return {'city': bigger['city'], 'fake': str(smarty['fake']) + ' %'}
    else:
        return {'city': user['city']['title'], 'fake': str(smarty['fake']) + ' %'}


def saver(gen, text):
    if gen == 1:
        save = open('followers.csv', 'w+', encoding='utf-8')
        save.write('Ссылка;Имя;Страна;Город;Пол;Дата рождения;Подписчиков;Состояние;Фейк\n')
        save.close()
    if gen == 2:
        save = open('followers.csv', 'a', encoding='utf-8')
        for elem in text:
            save.write(elem)
        save.close()


def exe_builder():
    code = ''
    exe = open('code.js', 'r+')
    for every in exe:
        code += every
    exe.close()
    return code


def users_get():
    users = {'users': {}, 'count': 0}
    while users['count'] == 0:
        try:
            users = api.execute(code=exe_builder())
        except Exception:
            printer('Ошибка доступа к vk.com..... Повтор\a', True, 0)
    count, users = users['count'], users['users']
    printer('Маcсив подписчиков получен успешно\nВ нем содержится ' + str(count) + ' человек', False, 1)
    save_arr = []
    for user in users:
        user['name'] = user.pop('first_name') + ' ' + user.pop('last_name')
        try:
            if user['deactivated'] == 'deleted':
                user['deactivated'] = 'Пользователь удален'
            elif user['deactivated'] == 'banned':
                user['deactivated'] = 'Пользователь забанен'
            user.update({'country': '', 'city': '', 'followers_count': '', 'bdate': '', 'fake': '100 %'})
            for every in user:
                if every not in fields: user[every] = 'Недоступно'
        except KeyError:
            user['deactivated'] = 'Страница активна'
            if smart_search == '1':
                try:
                    smarty = smart(user)
                    user['city'] = smarty['city']
                    user['fake'] = smarty['fake']
                    time.sleep(0.33)
                except KeyError:
                    try:
                        user['city'] = user['city']['title']
                    except KeyError:
                        user['city'] = 'Не указано'
            else:
                try:
                    user['city'] = user['city']['title']
                except KeyError:
                    user['city'] = 'Не указано'
            try:
                user['country'] = user['country']['title']
                if user['country'] == main['country']: counter['country'] += 1
            except KeyError:
                user['country'] = 'Не указано'
            try:
                user['sex'] = sex[user['sex']]
            except KeyError:
                if user['name'][len(user['name']) - 3:len(user['name'])] in sex_woman[0] or user['name'][
                                                                                            len(user['name']) - 2:len(
                                                                                                    user['name'])] in \
                        sex_woman[1]:
                    user['sex'] = 'Женский'
                elif user['name'][len(user['name']) - 2:len(user['name'])] in sex_man:
                    user['sex'] = 'Мужской'
                else:
                    if user['name'].split(' ')[0][len(user['name'].split(' ')[0])] in woman_names:
                        user['sex'] = 'Женский'
                    else:
                        user['sex'] = 'Мужской'
            try:
                user['bdate'] = user['bdate'].split('.')
                try:
                    user['bdate'] = user['bdate'][0] + ' ' + month[int(user['bdate'][1])] + ' ' + user['bdate'][2]
                except IndexError:
                    user['bdate'] = user['bdate'][0] + ' ' + month[int(user['bdate'][1])]
            except KeyError:
                user['bdate'] = 'Не указано'
            if user['city'] == main['city']: counter['city'] += 1
            perc = round(len(save_arr) / count * 100, 2)
        if len(save_arr) > 1:
            time_ = time.ctime(time.time() - start_date).split(' ')[4].split(':')
            time_[0] = '0' + str(int(time_[0]) - 3)
            time_ = time_[0] + ':' + time_[1] + ':' + time_[2]
            time_end = time.ctime((time.time() - start_date) * (count / len(save_arr))).split(' ')[4].split(':')
            time_end[0] = '0' + str(int(time_end[0]) - 3)
            time_end = time_end[0] + ':' + time_end[1] + ':' + time_end[2]
        else:
            time_ = time_end = '00:00:00'
        printer('[{}] Обработано {} человек ({} %) - осталось примерно {}'.format(time_, len(save_arr), perc, time_end),
                False, 2)
        try:
            save_arr.append('https://vk.com/id%s;%s;%s;%s;%s;%s;%s;%s;%s\n' % (
                user['id'], user['name'], user['country'], user['city'], user['sex'], user['bdate'],
                user['followers_count'], user['deactivated'], user['fake']))
        except KeyError:
            print(str(user))
    saver(gen=2, text=save_arr)
    printer('Создание базы успешно завершено\nОбщая с вами страна у ' + str(
        counter['country']) + ' человек\nОбщий с вами город у ' + str(
        counter['city']) + ' человек\nБаза создана за ' + str(round(time.time() - start_date, 2)) + ' секунд', True, 1)


printer('\aHottabbe followers parser\nFollow me - https://vk.com/hottabbe\nParser version : %s\n'
        'Smart city module version : %s' % (version['parser'], version['smart_city']), True, 1)
saver(gen=1, text='')
users_get()
input('')
