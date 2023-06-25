import requests
import json

with open ('Ya_token.txt', 'r') as file:
    ya_token = file.readline()

with open ('VK_token.txt', 'r') as file:
    vk_token = file.readline()

def backup_vk_profile_photos(user_id, token_yandex_disk, token_VK, count=999):
    # Получение фотографий с профиля VK
    response = requests.get(
        f"https://api.vk.com/method/photos.get?owner_id={user_id}&album_id=profile&count={count}&access_token={token_VK}&v=5.131"
    )
    data = response.json()

    if "error" in data:
        error_msg = data["error"]["error_msg"]
        print(f"Ошибка при получении фотографий с профиля VK: {error_msg}")
        return

    photos = data["response"]["items"]

    # Сохранение фотографий на Яндекс.Диск
    photos_info = []
    for photo in photos:
        photo_id = photo["id"]

        # Получение количества лайков для фотографии
        response = requests.get(
            f"https://api.vk.com/method/likes.getList?type=photo&owner_id={user_id}&item_id={photo_id}&access_token={token_VK}&v=5.131"
        )
        likes_data = response.json()

        if "error" in likes_data:
            error_msg = likes_data["error"]["error_msg"]
            print(f"Ошибка при получении количества лайков для фотографии {photo_id}: {error_msg}")
            continue

        likes_count = likes_data["response"]["count"]

        date_uploaded = photo["date"]
        url = photo["sizes"][-1]["url"]

        response = requests.get(url)
        if response.status_code == 200:
            file_name = f"{likes_count}.jpg"
            with open(file_name, "wb") as f:
                f.write(response.content)

            photos_info.append({"file_name": file_name, "size": "z"})

    # Сохранение информации по фотографиям в JSON-файл
    with open("photos_info.json", "w") as f:
        json.dump(photos_info, f)

    # Загрузка фотографий на Яндекс Диск
    headers = {
        "Authorization": f"OAuth {token_yandex_disk}",
    }
    url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    for photo_info in photos_info:
        file_name = photo_info["file_name"]
        params = {"path": f"/{file_name}", "overwrite": "true"}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if "href" in data:
            upload_url = data["href"]
            with open(file_name, "rb") as f:
                response = requests.put(upload_url, headers=headers, files={"file": f})

            if response.status_code == 201:
                print(f"Фотография {file_name} успешно загружена на Яндекс.Диск")
            else:
                print(f"Ошибка при загрузке фотографии {file_name} на Яндекс.Диск")

    print("Все фотографии успешно сохранены и загружены на Яндекс.Диск")

backup_vk_profile_photos(172843154, ya_token, vk_token)