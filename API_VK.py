import requests
import time #Данная библиотека подключается для ограничения количества запросов в секунду, чтобы не словить бан на api
# Функция определения ошибки в ответе на запрос, если таковая имеется
def search_errors_request(responce, user):
    if responce.status_code:
        if 'error' in responce.json().keys():
            raise Exception(f"Ошибка в ответе '{user} - {responce.json()['error']['error_msg']}'")
        else:
            return responce.json()
    else:
        raise Exception(f'При определении id пользователя {user} возникла ошибка при запросе {responce.status_code}')

class VKUser():
    def __init__(self, user):
        self.access_token = '10b2e6b1a90a01875cfaa0d2dd307b7a73a15ceb1acf0c0f2a9e9c586f3b597815652e5c28ed8a1baf13c'
        self.api_url = 'https://api.vk.com/method/'
        self.api_urls_search = 'https://api.vk.com/method/users.search'
        self.api_urls_friends = 'https://api.vk.com/method/friends.get'
# Запишем параметры для конкретного запроса
        self.params = {
            'access_token' : self.access_token,
            'v' : '5.126'
        }
        self.params_for_search = {
            'access_token' : self.access_token,
            'v' : '5.126',
            'q' : f'{user[15:]}'
        }
# Если аргументом экземпляра класса бцдет URL, но найдем id пользователя 
        if not user.isdigit():
            if user[15:17] == 'id':
                self.user_id = user[17:]
            else:
                resp = requests.get(self.api_urls_search, params=self.params_for_search)
                self.user_id = search_errors_request(resp, user)['response']['items'][0]['id']
                time.sleep(0.35)
        elif user.isdigit():
            self.user_id = user
        else:
            raise Exception('Ошибка в воде пользователя')

        self.params_friends = {
            'user_id' :  self.user_id, 
            'access_token' : self.access_token,
            'v' : '5.126',
            'count' : '10000'
        }        
# Метод поиска друзей пользователя
    def find_friends_ids(self):
        resp = requests.get(self.api_urls_friends, params=self.params_friends)
        time.sleep(0.35)
        return search_errors_request(resp, self.find_url())['response']['items']        
# Метод поиска общих друзей с other_user
    def find_mutual_friends(self, other_user):
        ids_mutual_friends = set(self.find_friends_ids()) & set(other_user.find_friends_ids())
        result = [VKUser(str(x)) for x in ids_mutual_friends]
        return result
# Найдем URL
    def find_url(self):
        return f'https://vk.com/id{self.user_id}'
# Переопределим &
    def __and__(self, other):
        return self.find_mutual_friends(other)
# Переопределим print()
    def __str__(self):
        return self.find_url()


person_1 = VKUser('https://vk.com/dimkakhmelev')
person_2 = VKUser('https://vk.com/id24415708')

print(person_1 & person_2)
# print(person_1)
# for i in person_1 & person_2:
#     print(len(i.find_friends_ids()))