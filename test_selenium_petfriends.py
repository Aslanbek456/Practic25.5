import pytest
from selenium import webdriver
driver = webdriver.Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture(autouse=True)
def testing():

   pytest.driver = webdriver.Chrome('/Applications/Google Chrome.app')
   pytest.driver.get('http://petfriends1.herokuapp.com/login')
   pytest.driver.find_element(By.ID, 'email').send_keys('valera@inbox.ru')
   pytest.driver.find_element(By.ID, 'pass').send_keys('Valera')
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   yield

   pytest.driver.close()


def test_show_all_my_pets():
   pytest.driver.find_element_by_xpath('//a[contains(text(), "Мои питомцы")]').click()

   driver.element = WebDriverWait(driver, 10).until(
   EC.presence_of_element_located((By.XPATH, ('//a[contains(text(), "Мои питомцы")]'))))
   locator_for_all_my_pets = pytest.driver.find_elements_by_xpath('//td[@class="smart_cell"]')
   quantity_of_my_pets_from_user_statistic = 3
   assert len(locator_for_all_my_pets) == quantity_of_my_pets_from_user_statistic

def test_card_my_pets():
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

def test_half_of_my_pets_with_photo():
    pytest.driver.find_element_by_xpath('//a[contains(text(), "Мои питомцы")]').click()
    locator_for_all_my_pets = pytest.driver.find_elements_by_xpath('//td[@class="smart_cell"]')
    images = pytest.driver.find_elements_by_xpath('//th/img')
    number_of_pets_with_photo = 0
    driver.implicitly_wait(5)
    for i in range(len(locator_for_all_my_pets)):
        if images[i].get_attribute('src') != '':
            number_of_pets_with_photo += 1
        else:
            number_of_pets_with_photo = number_of_pets_with_photo
    assert number_of_pets_with_photo >= (len(locator_for_all_my_pets) / 2)

def test_all_my_pets_with_name_type_age():
    pytest.driver.find_element_by_xpath('//a[contains(text(), "Мои питомцы")]').click()
    locator_for_all_my_pets = pytest.driver.find_elements_by_xpath('//td[@class="smart_cell"]')

    for i in range(len(locator_for_all_my_pets)):
        pet = locator_for_all_my_pets[i].find_elements_by_xpath('preceding-sibling::td')
        name = pet[2].text
        driver.implicitly_wait(5)
        anymal_type = pet[1].text
        driver.implicitly_wait(5)
        age = pet[0].text
        driver.implicitly_wait(5)
        assert name != ''
        assert anymal_type != ''
        assert age != ''

def test_all_my_pets_with_different_names():
    pytest.driver.find_element_by_xpath('//a[contains(text(), "Мои питомцы")]').click()
    locator_for_all_my_pets = pytest.driver.find_elements_by_xpath('//td[@class="smart_cell"]')
    list_of_pets_names = []
    for i in range(len(locator_for_all_my_pets)):
        pet = locator_for_all_my_pets[i].find_elements(By.XPATH, 'preceding-sibling::td')
        name = pet[2].text
        list_of_pets_names.append(name)
    for name in list_of_pets_names:
        assert list_of_pets_names.count(name) == 1