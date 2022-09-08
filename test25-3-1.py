import time
import pytest
from selenium import webdriver
driver = webdriver.Chrome



@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('/Applications/Google Chrome.app')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends1.herokuapp.com/login')

    yield

    pytest.driver.close()

def test_show_all_pets():
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('valera@inbox.ru')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('Valera')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"

    # Устанавливаем неявные ожидания(секунды)
    driver.implicitly_wait(10)

def test_card_my_pets():
    # Проверка карточек питомцев на фото, имя, тип и возраст питомца
    images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
    names = pytest.driver.find_elements_by_css_selector('.card-deck .card-title')
    descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-text')
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0