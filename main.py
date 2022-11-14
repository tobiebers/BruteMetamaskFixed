
import functions as mf  # this file 'functions.py' is in the same folder. it is required for this progr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import time
import subprocess
import random
# !!!

EXTENSION_PATH = "extension_10_14_1_0.crx"

opt = webdriver.ChromeOptions()
opt.add_extension(EXTENSION_PATH)
driver = webdriver.Chrome(options=opt)
time.sleep(5)

#switch tabs
driver.switch_to.window(driver.window_handles[0])

#CLICK THROUGH BUTTONS:
#btn1
time.sleep(1)
elem = driver.find_element(by = By.XPATH, value = '/html/body/div[1]/div/div[2]/div/div/div/button').click()
#btn2
time.sleep(1)
elem = driver.find_element(by = By.XPATH, value = '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button').click()
#btn3
time.sleep(1)
elem = driver.find_element(by = By.XPATH, value = '/html/body/div[1]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[2]').click()



# ENTER SEED WORDS, current COUNT:
seed_words = ['road',
'game',
'tunnel',
'mystery',
'gain',
'bargain',
'wish',
'clerk',
'infant',
'come',
'galaxy',
'permit']
#road evoke tunnel mystery merit bargain wish clerk robot come poverty permit

print(seed_words)

password = '12345678'
count = 1  # starts at 1, input 'n' to start at 'n'th permutation
# EDITABLE ^^^

keys = [i for i in range(1, 13)]
seed_words = dict(zip(keys, seed_words))

s = ''
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# get starting point:
arr = mf.getPermutation(len(arr), count)

# print starting string and starting array:
print("START:", arr, [seed_words[i] for i in arr])

# loop through permuations:
t0 = time.time()
looper = True
while looper:
    # populate string:
    s = ''
    for i in arr:
        s += ' ' + seed_words[i]
    s.strip()

    mf.copy2clip(s)  # copy string
    driver.find_element(by=By.XPATH, value='//*[@id="import-srp__srp-word-0"]').send_keys(
        Keys.CONTROL + 'v')  # paste string


    # if invalid seed phrase:
    try:
        driver.find_element(by=By.CSS_SELECTOR,value='#app-content > div > div.main-container-wrapper > div > div > div > form > div.import-srp__container > div.actionable-message.actionable-message--danger.import-srp__srp-error.actionable-message--with-icon')  # check to see if invalid message pops up
        time.sleep(0.01)
        # get next perm, increment
        arr = mf.nextPermutation(arr)
        print('Attempts', count, end='\r', flush=False)
        print('count/sec:', "{:.2f}".format(count / (time.time() - t0)), '---- count:', count, end='\r', flush=True)
        count += 1

    # if valid seed phrase:
    except:
        # enter into wallet:
        driver.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(password)  # enter pass
        driver.find_element(by=By.XPATH, value='//*[@id="confirm-password"]').send_keys(password)  # enter pass2
        time.sleep(0.01)
        try:  # after first login, check box disapears
            driver.find_element(by=By.XPATH,value='/html/body/div[1]/div/div[2]/div/div/div[2]/form/div[3]/input').click()  # click check box
            time.sleep(0.01)
        except:
            pass

        try:  # after first login, import btn -> restore btn
            driver.find_element(by=By.CSS_SELECTOR,
                                value='#app-content > div > div.main-container-wrapper > div > div > div.first-time-flow__import > form > button').click()  # click import
        except:
            driver.find_element(by=By.XPATH,
                                value='//*[@id="app-content"]/div/div[3]/div/div/div/form/button').click()  # click restore

        # HERE we need to wait for the restore process to load!!
        time.sleep(4.5)

        try:  # after first login, click all done disapears
            driver.find_element(by=By.CSS_SELECTOR,
                                value='#app-content > div > div.main-container-wrapper > div > div > button').click()  # click all done
        except:
            pass

        # once in wallet
        elem = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[3]/div/div/div/div[2]/div/div[1]/div/div/div/div[2]/span[2]')
        # find balance element
        usd = float(elem.text[1:])  # get balance usd
        if usd == 0:
            arr = mf.nextPermutation(arr)
            looper = True
            print(count, 'empty account:', s)
            count += 1
            time.sleep(0.01)

            try:  # after first login, popup disapears
                driver.find_element(by=By.XPATH,
                                    value='//*[@id="popover-content"]/div/div/section/div[1]/div/button').click()  # exit pop-up
            except:
                pass

            elem = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[1]/div/div[2]/div[2]').click()
            time.sleep(0.01)
            elem = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[3]/div[2]/button').click()
            time.sleep(0.01)
            elem = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[3]/div/div/div[3]/a').click()
            time.sleep(0.01)
        else:
            looper = False
            print("DONE", s, '$', str(usd))
            print(count)

