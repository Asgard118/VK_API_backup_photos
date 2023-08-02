import requests
import json

with open ('Ya_token.txt', 'r') as file:
    ya_token = file.readline()

with open ('VK_token.txt', 'r') as file:
    vk_token = file.readline()

upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"

def get_vk_profile_photos(user_id, token_VK, count=999):
    """
    Получает фотографии с профиля VK.
    Возвращает список фотографий или None в случае ошибки.
    """
    response = requests.get(
        f"https://api.vk.com/method/photos.get?owner_id={user_id}&album_id=profile&count={count}&access_token={token_VK}&v=5.131"
    )
    data = response.json()

    if "error" in data:
        error_msg = data["error"]["error_msg"]
        print(f"Ошибка при получении фотографий с профиля VK: {error_msg}")
        return None

    photos = data["response"]["items"]
    return photos

def create_yandex_disk_folder(folder_name, token_yandex_disk):
    """
    Создает папку на Яндекс.Диске.
    Возвращает True, если папка успешно создана, иначе False.
    """
    headers = {
        "Authorization": f"OAuth {token_yandex_disk}",
    }
    params = {"path": folder_name}
    response = requests.put("https://cloud-api.yandex.net/v1/disk/resources", headers=headers, params=params)

    if response.status_code == 201:
        print(f"Папка {folder_name} успешно создана на Яндекс.Диске")
        return True
    else:
        print(f"Ошибка при создании папки {folder_name} на Яндекс.Диске")
        return False

def get_photos_from_source(source_url):
    """
    Получает фотографии с источника по указанному URL.
    Возвращает список байтов фотографий или None, если возникла ошибка.
    """
    try:
        response = requests.get(source_url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Ошибка при получении фотографий с источника: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
def upload_photo_to_yandex_disk(photo_bytes, upload_url, token_yandex_disk):
    """
    Загружает фотографию на Яндекс.Диск.
    Возвращает True, если загрузка прошла успешно, иначе False.
    """
    headers = {
        "Authorization": f"OAuth {token_yandex_disk}",
    }
    files = {"file": ("photo.jpg", photo_bytes)}
    response = requests.put(upload_url, headers=headers, files=files)

    if response.status_code == 201:
        print("Фотография успешно загружена на Яндекс.Диск")
        return True
    else:
        print(f"Ошибка при загрузке фотографии на Яндекс.Диск: {response.status_code}")
        return False
