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

service = Service(executable_path=FIREFOX_DRIVER_PATH)


btn_logged_in_avatar = '/html/body/div[1]/div[1]/div[1]/nav/div[1]/div/div/div[4]/div/button'
#btn_logged_in_avatar = '/html/body/div[1]/div[1]/nav/div[1]/div/div/div[3]/button/span/img'
btn_signin = '/html/body/div[1]/div[1]/div[1]/nav/div[1]/div/div/div[1]/a[2]'
inp_username = '/html/body/div[1]/div/div[4]/div/div[2]/div/div/div/form/span[1]/input'
inp_password = '/html/body/div[1]/div/div[4]/div/div[2]/div/div/div/form/span[2]/input'
btn_submit_login = '/html/body/div[1]/div/div[4]/div/div[2]/div/div/div/button/div/span'
btn_logout = '/html/body/div[1]/div[1]/div[1]/nav/div[1]/div/div/div[4]/div/div/div/ul/li[6]/div[2]'




def sol_tab_click():
    solutions = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[1]/div[1]/div[1]/div/div[5]/div/div/div[2]/div[2]')
    solutions.click()

def back_to_all_solutions():
    all_solutions = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[6]/div[2]/div/div/div/div[1]/div[1]').click()

def get_user_code():
    user_sol_content = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[6]/div[2]/div/div/div/div[2]/div/div[1]/div[2]')
    pre_elements = user_sol_content.find_elements(By.TAG_NAME, "pre")
    for pre in pre_elements:
        pre_parent_element = pre.find_element(By.XPATH, 'parent::*')
        hidden_elements = pre_parent_element.find_elements(By.CLASS_NAME, 'hidden')
        for element in hidden_elements:
            driver.execute_script("arguments[0].classList.remove('hidden');", element)
            element.click()
            print('User code copied')

def submit_code():
    code_editor = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[8]/div/div[2]')
    code_editor.click()
    
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL).perform()
    print('code submitted')
    sleep(10)
    try: #if greeting modal open
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[2]/div[1]/button').click()
        sleep(1)
    except:
        pass
        
    try:
        submissions = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[11]/div/div/div/div[1]')
        if submissions.text == 'All Submissions':
            sub_res = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[11]/div/div/div/div[2]/div/div[1]/div[1]/div[1]/span')
            print('sub_res:', sub_res.text)
            if sub_res.text == 'Accepted':
                print('Waao! Accepted.')
                return True
            else:
                return False
        else:
            print('submissions text is: ' , submissions.text)
    except:
        driver.get_screenshot_as_file("submission-exception.png")
        print('submission code exception')
        return False

def send_notif(msg=''):
    requests.post('https://notify.run/b55O3rUbMhj8QHHi', data={'message': msg})

def submit_solution():
    print('URL Opened')
    
    completed_svg = 'M20 12.005v-.828a1 1 0 112 0v.829a10 10 0 11-5.93-9.14 1 1 0 01-.814 1.826A8 8 0 1020 12.005zM8.593 10.852a1 1 0 011.414 0L12 12.844l8.293-8.3a1 1 0 011.415 1.413l-9 9.009a1 1 0 01-1.415 0l-2.7-2.7a1 1 0 010-1.414z'

    daily_challange_element = today_challange = driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div[4]/div[2]/div[1]/div[4]/div[2]/div/div/div[2]/div[1]/div[1]/a')
    daily_challange_html = daily_challange_element.get_attribute('outerHTML')
    if completed_svg in daily_challange_html:
        print('Challange already completed')
        return True
    else:
        print('Today challange is waiting to be complete')
        daily_challange_element.click()
    sleep(5)
    sol_tab_click()
    
    sleep(2)
    print('sol tab clicked')
    py_sol = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[6]/div/div/div[1]/div[2]/div/div[1]/span[1]').click()
    sleep(2)
    for i in range(2):
        if i == 1: #second time after failed with one liner solution
            search_box = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[6]/div/div/div[1]/div[1]/div[1]/input').send_keys('one line')
            sleep(2)
            print('searched the item')
        for sol_n in range(1,10):
            try:
                user_sol = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[6]/div/div/div[3]/div[3]/div[1]/div[{sol_n}]').click()
                sleep(2)
            
                get_user_code()
                sleep(1)
                is_success = submit_code()
                if is_success:
                    send_notif(f'{profile}: submission success.')
                    return True
                else:
                    # send_notif(f'{profile}: sol:{sol_n}failed.')
                    sol_tab_click()
                    sleep(1)
                    back_to_all_solutions()
            except Exception as e:
                # driver.get_screenshot_as_file("find-solution-exception.png")
                # send_notif(f'{profile}: sol:{sol_n}failed.')
                pass
    send_notif(f'{profile}: Leetcode submission failed.')

def check_logged_in(driver, username, firefox_options):
    try:
        if len(driver.find_elements(By.XPATH, btn_logged_in_avatar)) > 0:
            print('Logged in')
            return True
        else:
            print('Not logged in, logging in')
            return do_login(driver, username, firefox_options)
    except Exception as e:
        print(e)
        return False
  
def do_login(driver, username, firefox_options):
    if driver.current_url != 'https://leetcode.com/problemset/all/':
        driver.get('https://leetcode.com/problemset/all/')
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
    if driver.current_url == 'https://leetcode.com/accounts/login/?next=%2Fproblemset%2F':
        print('Stucked with google captcha, do something')
        send_notif(f'Emergency!! Unable to login{username}')
        driver.quit()
        driver = webdriver.Firefox(service=service, options=firefox_options)
        do_login(driver, username, firefox_options)
    # driver.get('https://leetcode.com/problemset/all/')
    # sleep(10)
    print('Login done, checking...')
    return check_logged_in(driver, username, firefox_options)
    

def do_logout():
    print('doing logout...')
    driver.find_element(By.XPATH, btn_logged_in_avatar).click()
    driver.find_element(By.XPATH, btn_logout).click()
    sleep(5)

# Setup WebDriver

profiles_list = ['sdq99', 'sdq999', 'sdq998', 'sdq997', 'sdq996' ]
#profiles_list = ['sdq999']
for profile in profiles_list:
    print(profile)
    # sleep(10)
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("-profile")
        options.add_argument(f'{PROFILE_BASE}{profile}')
        driver = webdriver.Firefox(service=service, options=options)

        driver.get('https://leetcode.com/problemset/all/')
        sleep(10)
        if check_logged_in(driver, profile, options):
            submit_solution()
    except Exception as e:
        print(e)
        send_notif(f'Something wrong with {profile} in leetcode submission')
        # sleep(5)
    driver.quit()


    
    # break


