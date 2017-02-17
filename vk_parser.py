import vk
import time
users = []
user_ = []
save_arr = []
sex = ['Не указан', 'Женский', 'Мужской']
month = ['',
         'января',
         'февраля',
         'марта',
         'апреля',
         'мая',
         'июня',
         'июля',
         'августа',
         'сентября',
         'октября',
         'ноября',
         'декабря']
counter = {'city': 0, 'country': 0}
settings = {}
version = {
            'parser': '2.1',
            'smart_city': '1.8'
            }
fields = {'id','deactivated','name'}
print('\aHottabbe followers parser\nFollow me - https://vk.com/hottabbe\nParser version : %s\n'
      'Smart city module version : %s' % (version['parser'], version['smart_city']))


def cfg():
    lines = open('config.cfg', 'r+')
    for line in lines:
        line = line.split(':')
        line[1] = line[1].split('\n')[0]
        settings.update({line[0]: line[1]})
    lines.close()


def smart(user):
    try:
        friends_list = []
        cities = {}
        friends_list = api.friends.get(user_id=user['id'], order='hints', fields='city')
        try:
            user['city']
        except KeyError:
            user['city'] = {
                            'title': 'Не указано',
                            'id': 0
                            }
        for friend in friends_list['items']:
            try:
                if friend['city']['title'] in cities:
                    cities[friend['city']['title']] += 1
                else:
                    cities.update({friend['city']['title']: 1})
            except KeyError:
                continue
        bigger = {'city': 'no name', 'count': -2}
    except vk.exceptions.VkAPIError:
        print('\aВозникла ошибка.....повтор попытки')
        time.sleep(0.95)
    except Exception:
        print('Не удалось загрузить данные с vk.com.....Повтор')
    for key in cities:
        if cities[key] >= bigger['count']: bigger['city'],bigger['count'] = key,cities[key]
    try: percent = round(bigger['count']/(friends_list['count']+1) * 100,2)
    except UnboundLocalError: percent = 0
    if ((percent in range(15,35) and friends_list['count'] > 100) or percent > 35) and bigger['city'] != 'no name':
        if bigger['city'] != user['city']['title']:
            print('    '+ user['first_name']+ ' ' + user['last_name'] + ' : ' + user['city']['title'] + ' ===> ' + bigger['city'])
        return bigger['city']
    else:
        return user['city']['title']
    
    
def saver (gen,text):
    if gen == 1:
        save = open('followers.csv','w+',encoding = 'utf-8')
        save.write('Ссылка;Имя;Страна;Город;Пол;Дата рождения;Подписчиков;Состояние;Фейк\n')
        save.close()
    if gen == 2:
        save = open('followers.csv','a',encoding = 'utf-8')
        for elem in text:
            save.write(elem)
        save.close()


def exe_builder():
    code = ''
    exe = open('code.js','r+')
    for every in exe:
        code += every
    exe.close()
    return code


def users_get ():
    users = {
            'users':{},
            'count':0
            }
    while users['count'] == 0:
        try:users = api.execute(code = exe_builder())
        except Exception:print('Ошибка доступа к vk.com..... Повтор\a')
    count = users['count']
    users = users['users']
    print('Маcсив подписчиков получен успешно\nВ нем содержится ' + str(count) + ' человек')
    save_arr = []    
    for user in users:
        user['name'] = user['first_name'] + ' ' + user['last_name']
        try:
            if user['deactivated'] == 'deleted': user['deactivated'] = 'Пользователь удален'
            elif user['deactivated'] == 'banned': user['deactivated'] = 'Пользователь забанен'
            user.update({'country': '', 'city': '', 'followers_count': '','bdate':''})
            for every in user:
                if every not in fields:
                    user[every] = 'Недоступно'
        except KeyError:
            user['deactivated'] = 'Страница активна'
            if smart_search == '1':
                try:
                    user['city'] = smart(user)
                    time.sleep(0.225)
                except KeyError:
                    try:
                        user['city'] = user['city']['title']
                    except KeyError:
                        user['city'] = 'Не указано'
            else :
                try:
                    user['city'] = user['city']['title']
                except KeyError:
                    user['city'] = 'Не указано'
            try:
                user['country'] = user['country']['title']
                if user['country'] == main['country']: counter['country'] += 1
            except KeyError: user['country'] = 'Не указано'
            try:user['sex'] = sex[user['sex']]
            except KeyError:user['sex'] = 'Ошибка'
            try:
                user['bdate'] = user['bdate'].split('.')
                try:
                    user['bdate'] = user['bdate'][0] + ' ' + month[int(user['bdate'][1])] + ' ' + user['bdate'][2]
                except IndexError:
                    user['bdate'] = user['bdate'][0] + ' ' + month[int(user['bdate'][1])]
            except KeyError:user['bdate'] = 'Не указано'
            if user['city'] == main['city']: counter['city'] += 1
        if len(save_arr)%100 == 0: print('Обработано %s человек из %s - прошло %s секунд от начала'% (str(len(save_arr)),str(count),str(round(time.time() - start_date,2))))
        try:save_arr.append('https://vk.com/id%s;%s;%s;%s;%s;%s;%s;%s\n' % (user['id'],user['name'],user['country'],user['city'],user['sex'],user['bdate'],user['followers_count'],user['deactivated']))
        except KeyError: print(str(user))
    saver(gen = 2,text = save_arr)
    print('Создание базы успешно завершено\nОбщая с вами страна у '+ str(counter['country']) + ' человек\nОбщий с вами город у '+ str(counter['city']) + ' человек\n')
    print('База создана за ' + str(round(time.time() - start_date,2)) + ' секунд')

cfg()
api = vk.API(vk.AuthSession(app_id='3265802', user_login=settings['login'], user_password=settings['pass'], scope='friends'), lang='ru', v = '5.62')
main = api.users.get(fields = 'country,city')[0]
main['city'],main['country'] = main['city']['title'],main['country']['title']
print(main['first_name'] + ' ' + main['last_name'] + ' - Вход выполнен')
smart_search = settings['smart']
start_date = time.time()
saver(gen = 1,text = '')            
users_get()
input('')