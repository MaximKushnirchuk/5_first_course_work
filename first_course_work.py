'''Задание:
Нужно написать программу, которая будет:
Получать фотографии с профиля. Для этого нужно использовать метод photos.get.
Сохранять фотографии максимального размера(ширина/высота в пикселях) на Я.Диске.
Для имени фотографий использовать количество лайков.
Сохранять информацию по фотографиям в json-файл с результатами.'''

import json
import requests
import time
from tqdm import tqdm

def copy_fotos_from_vk(id_vk, vk_token, yand_token, count_photo=5) :
    if count_photo < 1 :
        return print('Ошибка')
    url = 'https://api.vk.com/method/photos.get'    
    params = {
        'access_token' : vk_token   ,
        'v' : 5.131,
        'owner_id' : id_vk,
        'album_id' : 'profile',
        'extended' : 1,
        'photo_sizes' : 1
        }
    response = requests.get(url, params=params)
    if 200 <= response.status_code < 300 :
        print('[ - 0 - ] ' * 8)
    
        '''создаем папку на диске'''
        name_folder_for_load = 'Photos_from_vk'
        requests.put(r'https://cloud-api.yandex.net/v1/disk/resources', params={'path' : name_folder_for_load}, headers={'Authorization' : yand_token})

        list_all_photo_max_sizes = []
        all_params = []
        list_foto_json = []
        photos_names_list = []
        list_types_sizes_photos = ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']
        
        '''получаем имя фото, размер, юрл, и собираем в list_all_photo_max_sizes'''
        for one_foto_info in response.json()['response']['items'] :
            if str(one_foto_info['likes']['count']) not in photos_names_list:
                photos_names_list.append(str(one_foto_info['likes']['count']))
                name_foto = str(one_foto_info['likes']['count']) + '.jpg'
            else :
                epoch_second = one_foto_info['date']
                type_struct_time = time.gmtime(epoch_second)
                time_foto = time.strftime('%x', type_struct_time)
                name_foto = str(one_foto_info['likes']['count']) + '_' + time_foto.replace('/', '_') + '.jpg'     
            
            stop = 0
            for one_type in list_types_sizes_photos :
                if stop != 0 : break
                for size_photo in one_foto_info['sizes'] :
                    if stop != 0 : break
                    if one_type == size_photo['type'] :
                        stop = 1
                        size = size_photo['type']
                        url_photo = size_photo['url']
                        list_all_photo_max_sizes.append({'file_name' : name_foto, 'size' : size, 'url' : url_photo})
        
        # Добавляем данные о фото в список для загрузки на Яндекс и в список для записи в Json файл
        for one_size in list_types_sizes_photos :
            if len(all_params) == count_photo : break
            else : 
                for one_photo in list_all_photo_max_sizes :
                        if len(all_params) == count_photo : break
                        else :
                            if one_size == one_photo['size'] :
                                all_params.append({'path' : name_folder_for_load + '/' + one_photo['file_name'], 'url' : one_photo['url']})
                                
                                list_foto_json.append({'file_name' : one_photo['file_name'], 'size' : one_photo['size']})

        # Загрузка фото на Яндекс Диск
        if len(all_params) < count_photo :
            print(f'Найдено только {len(all_params)} фото ')
        else : print(f'Найдено {len(all_params)} фото')
        print('Идёт загрузка....')
        for one_param in tqdm(all_params) :
            params = one_param
            headers = {'Authorization' : yand_token} 
            url_for_load_yandex = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            response_yandex = requests.post(url_for_load_yandex, params=params, headers=headers)
        if 200 <= response_yandex.status_code < 300 :
            print(f'На Ваш Яндекс.Диск загружено {len(all_params)} фото, в максимальном размере')
        else : 
            print('Ошибка. status_code ==', response_yandex.status_code)
        
        #     создание json файла в дерриктории
        with open(f'{name_folder_for_load}.json', 'w') as file :
            json.dump(list_foto_json, file, indent=2)
        print(f'В рабочей дерриктории Вашего ПК сохранен файл {name_folder_for_load}.json, содержащий названия и размер фото')


#загрузка  токенов
id_vk_ = 'параметр для id вк'
vk_token = 'параметр для вк токена' 
yandex_token = 'параметр для яндекс токена'

# Проверяем работу функции copy_fotos_from_vk
copy_fotos_from_vk(id_vk_, vk_token, yandex_token, 11)


