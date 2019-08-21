from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import time
import os
from test import getuserlist

defaults = {'Username':'', 'Password':'', 'Userlist':'',
            'List start index':'', 'List end index':'', 'Duration':'10',
            'Timeout':'100', 'Ratio':'1', 'Account':'',
            'Number of users':''}

def check_directory():
    if not os.path.exists('Following'):
        os.makedirs('Following')
    if not os.path.exists('Followers'):
        os.makedirs('Followers')
    if not os.path.exists('Unfollowed.txt'):
        f_unfollowed = open('Unfollowed.txt', 'a')
    yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
    readpath = 'Following/' + yesterday.strftime("%Y-%m-%d") + '.txt'
    if not os.path.exists(readpath):
        f = open(readpath, 'a')
    if not os.path.exists('defaults.txt'):
        f_defaults = open('defaults.txt', 'a')
        for key in defaults:
            f_defaults.write(key + '=' + defaults[key] + '\n')

def start_bot(login_username, login_password, duration, follower_list, start_follow, end_follow, timeout, ratio):
    start_time = time.time()
    while time.time() - start_time < duration:
        wd = webdriver.Chrome('chromedriver.exe')
        wd.get('https://www.instagram.com/accounts/login/')
        wd.set_page_load_timeout(timeout)
        time.sleep(3)

        username = wd.find_element_by_name('username')
        password = wd.find_element_by_name('password')

        username.send_keys(login_username)
        password.send_keys(login_password)
        password.send_keys(Keys.RETURN)
        time.sleep(3)

        followers_stolen = open('Followers/%s' % follower_list, 'r')
        followers_stolen_text = followers_stolen.read()
        user_list = followers_stolen_text.split('\n')[start_follow:end_follow]
            
        now = datetime.datetime.now()
        writepath = 'Following/' + now.strftime("%Y-%m-%d") + '.txt'
        f = open(writepath, 'a')
        f_unfollowed = open('Unfollowed.txt', 'r')
        unfollowed_text = f_unfollowed.read()
        unfollowed_userlist = unfollowed_text.split('\n')
        for user in user_list:
            wd.get('https://www.instagram.com/%s/' % user)
            time.sleep(1)
            if user not in unfollowed_userlist:
                buttons = wd.find_elements_by_css_selector('button')
                for button in buttons:
                    if button.text == 'Follow':
                        button.click()
                        f.write('%s\n' % user)
                        break
                    elif button.text == 'Following' or button.text == 'Requested':
                        break
            time.sleep(2)
        f.close()
        for i in range(ratio):
            yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
            readpath = 'Following/' + yesterday.strftime("%Y-%m-%d") + '.txt'
            f = open(readpath, 'r')
            text = f.read()
            f_unfollowed = open('Unfollowed.txt', 'a')
            unfollowed_list = []
            for user in text.split('\n'):
                wd.get('https://www.instagram.com/%s/' % user)
                try:
                    page_buttons = wd.find_elements_by_tag_name('button')
                    for button in page_buttons:
                        if button.text == 'Following' or button.text == 'Requested':
                            button.click()
                            unfollowed_list.append(user)
                            time.sleep(2)
                            break
                except:
                    page_buttons = wd.find_elements_by_tag_name('button')
                    for button in page_buttons:
                        if button.text == 'Following' or button.text == 'Requested':
                            button.click()
                            unfollowed_list.append(user)
                            time.sleep(2)
                            break
                try:
                    popup_buttons = wd.find_elements_by_tag_name('button')
                    for popup in popup_buttons:
                        if popup.text == 'Unfollow':
                            popup.click()
                            f_unfollowed.write('%s\n' % user)
                            break
                except:
                    popup_buttons = wd.find_elements_by_tag_name('button')
                    for popup in popup_buttons:
                        if popup.text == 'Unfollow':
                            popup.click()
                            f_unfollowed.write('%s\n' % user)
                            break 
                time.sleep(3)
        wd.quit()

