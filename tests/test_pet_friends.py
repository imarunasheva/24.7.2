from api import PetFriends

from settings import valid_email, valid_password

import os

pf = PetFriends()


class TestPetFriends:

    def test_get_api_key_for_valid_user(self, email=valid_email, password=valid_password):
        """ Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 200
        assert 'key' in result

    def test_get_api_key_for_invalid_password(self, email=valid_email, password="12345"):
        """ Проверяем запрос api ключа c невалидным password"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403

    def test_get_api_key_for_invalid_user(self, email="popir@mail.ru", password="12345"):
        """ Проверяем запрос api ключа c невалидным email и password"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403

    def test_create_pet_simple_with_valid_data(self, name='Мурзик', animal_type='кот', age='1'):
        """Проверяем, что можно добавить питомца без фото с корректными данными"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
        status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name

    def test_create_pet_simple_with_null_data(self, name='', animal_type='', age=''):
        """Проверяем, что можно добавить питомца без фото с пустыми параметрами name, animal_type, age"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
        status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == ''

    def test_create_pet_simple_with_invalid_data(self, name='111', animal_type='222', age='555'):
        """Проверяем, что можно добавить питомца без фото с цифрами в параметрах name, animal_type, age"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
        status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name

    def test_create_pet_simple_with_invalid_key(self, name='Бобик', animal_type='собака', age='1'):
        """Проверяем, что нельзя добавить питомца без фото c невалидным auth_key"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        auth_key = {'key': '000'}

        # Добавляем питомца
        status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 403

    def test_add_photo_with_valid_data(self, pet_photo='images\\1.jpg'):
        """Проверяем, что можно добавить фото питомца"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Если список не пустой, то добавляем фото питомца:
        if len(my_pets['pets']) > 0:
            # Берём id первого питомца из списка и сохраняем в переменную pet_id
            pet_id = my_pets['pets'][0]['id']
            status, result = pf.post_add_photo(auth_key, pet_id, pet_photo)

            # Сверяем полученный ответ с ожидаемым результатом
            assert status == 200
            assert result['pet_photo'] != ''

        else:
            # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pets")

    def test_add_photo_with_invalid_data(self, pet_photo='images\\2.gif'):
        """Проверяем, что нельзя добавить фото питомца в отличном от указанного в документации формате .gif"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Если список не пустой, то добавляем фото питомца:
        if len(my_pets['pets']) > 0:
            # Берём id первого питомца из списка и сохраняем в переменную pet_id
            pet_id = my_pets['pets'][0]['id']
            status, result = pf.post_add_photo(auth_key, pet_id, pet_photo)

            # Сверяем полученный ответ с ожидаемым результатом
            assert status == 500

        else:
            # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pets")

    def test_add_photo_with_invalid_format(self, pet_photo='images\\4.bmp'):
        """Проверяем, что можно добавить фото питомца в отличном от указанного в документации формате .bmp"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Если список не пустой, то добавляем фото питомца:
        if len(my_pets['pets']) > 0:
            # Берём id первого питомца из списка и сохраняем в переменную pet_id
            pet_id = my_pets['pets'][0]['id']
            status, result = pf.post_add_photo(auth_key, pet_id, pet_photo)

            # Сверяем полученный ответ с ожидаемым результатом
            assert status == 200

        else:
            # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pets")

    def test_add_photo_with_text_file(self, pet_photo='images\\3.txt'):
        """Проверяем, что нельзя передать в качестве файла с фото текстовый файл"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Если список не пустой, то добавляем фото питомца:
        if len(my_pets['pets']) > 0:
            # Берём id первого питомца из списка и сохраняем в переменную pet_id
            pet_id = my_pets['pets'][0]['id']
            status, result = pf.post_add_photo(auth_key, pet_id, pet_photo)

            # Сверяем полученный ответ с ожидаемым результатом
            assert status == 500

        else:
            # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pets")
