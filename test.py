from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import time

def getuserlist(login_username, login_password, account, follower_num, timeout):
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

    wd.get('https://www.instagram.com/%s/' % account)
    time.sleep(3)
    links = wd.find_elements_by_tag_name('a')
    for link in links:
        if 'followers' in link.text:
            link.click()
    time.sleep(3)
    scrl = wd.find_element_by_class_name('isgrP')
    user_list = []
    wd.execute_script("arguments[0].scrollTop = Math.round(arguments[0].scrollHeight * 0.2)", scrl)
    time.sleep(2)
    while len(set(user_list)) < follower_num:
        names = wd.find_elements_by_class_name('d7ByH')
        for n in names:
            if n.text != '' and 'Verified' not in n.text:
                user_list.append(n.text)
        wd.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrl)
        time.sleep(1)
    user_list = list(set(user_list))
    f = open('Followers/%s.txt' % account, 'a')
    for u in user_list:
        f.write('%s\n' % u)
    f.close()
    wd.quit()
    return user_list
