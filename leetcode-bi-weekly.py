from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re
import requests
from time import sleep

FIREFOX_DRIVER_PATH = '/usr/xorg/leetcode/geckodriver' 
PROFILE_BASE = '/usr/xorg/leetcode/firefox_profiles/'
btn_logged_in_avatar = '/html/body/div[1]/div[1]/div[1]/nav/div[1]/div/div/div[4]/div/button'
btn_logged_in_avatar_2 = '/html/body/div[1]/div[1]/nav/div[1]/div/div/div[3]/button/span/img'
btn_signin = '/html/body/div[1]/div[1]/div[1]/nav/div[1]/div/div/div[1]/a[2]'
inp_username = '/html/body/div[1]/div/div[4]/div/div[2]/div/div/div/form/span[1]/input'
inp_password = '/html/body/div[1]/div/div[4]/div/div[2]/div/div/div/form/span[2]/input'
btn_submit_login = '/html/body/div[1]/div/div[4]/div/div[2]/div/div/div/button/div/span'
btn_logout = '/html/body/div[1]/div[1]/div[1]/nav/div[1]/div/div/div[4]/div/div/div/ul/li[6]/div[2]'


service = Service(executable_path=FIREFOX_DRIVER_PATH)

profiles_list = ['sdq999', 'sdq998', 'sdq997', 'sdq996', 'sdq99']


def send_notif(msg=''):
    requests.post('https://notify.run/b55O3rUbMhj8QHHi', data={'message': msg})

def submit(contest_type, profile):
    try:
        if driver.current_url != 'https://leetcode.com/contest/':
            driver.get('https://leetcode.com/contest/')
        sleep(10)
        try:
            print('Registering...')
            driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div[4]/div/div/div[2]/div/div/div[1]/div/div/div[{contest_type}]/div/a').click()
            sleep(3)
            driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div[3]/span/a').click()
            sleep(3)
            driver.find_element(By.XPATH, '/html/body/div[7]/div/div[10]/button[1]').click()
            sleep(4)
            print('Registered!')
        except:
            print('Already registered')
            pass
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div[4]/div[1]/ul/li[2]/a').click()
        sleep(3)
        driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[4]/div/div/div[6]/div/div[3]/div[2]/div/div[2]/div/button/span').click()
        sleep(3)
        send_notif(f'{profile} bi-weekly submission Success')
    except:
        send_notif(f'{profile} bi-weekly submission Failed')
    driver.quit()

def check_logged_in(driver, username, firefox_options):
    try:
        if len(driver.find_elements(By.XPATH, btn_logged_in_avatar)) > 0:
            print('Logged in')
            return True
        elif len(driver.find_elements(By.XPATH, btn_logged_in_avatar_2)) > 0:
            print('Logged in')
            return True
        else:
            print('Not logged in, logging in')
            return do_login(driver, username, firefox_options)
    except Exception as e:
        print(e)
        return False
  
def do_login(driver, username, firefox_options):
    if driver.current_url != 'https://leetcode.com/contest/':
        driver.get('https://leetcode.com/contest/')
    sleep(10)
    # driver.get('https://leetcode.com/accounts/login/')
    driver.find_element(By.XPATH, btn_signin).click()
    sleep(10)
    driver.find_element(By.XPATH, inp_username).send_keys(username)
    driver.find_element(By.XPATH, inp_password).send_keys('7277197737Sz@')
    sleep(2)
    captcha_input = driver.find_element(By.CSS_SELECTOR, "[id^='cf-chl-widget-']")
    driver.execute_script("arguments[0].value = '1';", captcha_input)
    sleep(2)
    driver.find_element(By.XPATH, btn_submit_login).click()
    sleep(10)
    if driver.current_url == 'https://leetcode.com/accounts/login/?next=%2Fcontest%2F':
        print('Stucked with google captcha, do something')
        driver.quit()
        driver = webdriver.Firefox(service=service, options=firefox_options)
        do_login(driver, username, firefox_options)
    # driver.get('https://leetcode.com/problemset/all/')
    # sleep(10)
    print('Login done, checking...')
    return check_logged_in(driver, username, firefox_options)

for profile in profiles_list:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("-profile")
    options.add_argument(f'{PROFILE_BASE}{profile}')
    driver = webdriver.Firefox(service=service, options=options)


    try:
        print(profile)
        driver.get('https://leetcode.com/contest/')
        sleep(8)
        if check_logged_in(driver, profile, options):
            submit(2, profile)  # 1 for weekly and 2 for bi-weekly
    except:
        send_notif(f'{profile} bi-weekly submission issue')

    #break

