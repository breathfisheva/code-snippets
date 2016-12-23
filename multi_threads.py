
#different threads has their own global_data, and the threads cannot access other thread data. there are two ways to do it,
#one way is use [threading.local]
#another way is use class (the self will separete different threads

# #using threading.local
# from selenium import webdriver
# import threading
# import time
#
# global_data = threading.local()
# def login(username, password):
#     global_data.username = username
#     global_data.password = password
#     browser = webdriver.Chrome()
#     browser.get("http://qa.englishtown.com/login.aspx?ctr=cn")
#     username_box = browser.find_element_by_id("username")
#     password_box = browser.find_element_by_id("password")
#     login_button = browser.find_element_by_id("btnmid")
#     username_box.send_keys(global_data.username)
#     password_box.send_keys(global_data.password)
#     login_button.click()
#     time.sleep(10)
#     browser.close()
#
# user_account = {'cateam':1, 'aateam':1} #dexin
#
# if __name__ == '__main__':
#     thread_pool = []
#     for (k,v) in user_account.items():
#         t = threading.Thread(target=login,args=(k,v))
#         thread_pool.append(t)
#         t.start()
#     for t in thread_pool:
#         t.join()

# #using class
# from selenium import webdriver
# import threading
# import time
#
# class MyThread(threading.Thread):
#     def __init__(self,func,username, password):
#         threading.Thread.__init__(self)
#         self.func = func
#         self.username = username
#         self.password = password
#
#     def run(self):
#         self.func(self.username, self.password)
#         print(self.username,self.password)
#
# def login(username, password):
#     browser = webdriver.Chrome()
#     browser.get("http://qa.englishtown.com/login.aspx?ctr=cn")
#     username_box = browser.find_element_by_id("username")
#     password_box = browser.find_element_by_id("password")
#     login_button = browser.find_element_by_id("btnmid")
#     username_box.send_keys(username)
#     password_box.send_keys(password)
#     login_button.click()
#     time.sleep(10)
#     browser.close()
#
# user_account = [['cateam',1], ['aateam',1]] #dexin
#
# if __name__ == '__main__':
#     thread_pool = []
#     for user in user_account:
#         t = MyThread(login,user[0],user[1])
#         thread_pool.append(t)
#         t.start()
#     for t in thread_pool:
#         t.join()

#using class and
from selenium import webdriver
import threading
import time

#all threads will write the txt file , so we need a lock
result_lock = threading.Lock()
def write_result(txt):
    with open('C:/multithreadsresult.txt', 'w') as f:
        f.write(txt)

class MyThread(threading.Thread):
    def __init__(self,func,username, password):
        threading.Thread.__init__(self)
        self.func = func
        self.username = username
        self.password = password

    def run(self):
        self.func(self.username, self.password)
        print(self.username,self.password)

def login(username, password):
    browser = webdriver.Chrome()
    browser.get("http://qa.englishtown.com/login.aspx?ctr=cn")
    username_box = browser.find_element_by_id("username")
    password_box = browser.find_element_by_id("password")
    login_button = browser.find_element_by_id("btnmid")
    username_box.send_keys(username)
    password_box.send_keys(password)
    login_button.click()
    time.sleep(10)

    result_lock.acquire()
    try:
        write_result(username)
    finally:
        result_lock.release()

    browser.close()

user_account = [('cateam',1), ('aateam',1)] #dexin

if __name__ == '__main__':
    thread_pool = []
    for (k,v) in user_account:
        t = MyThread(login,k,v)
        thread_pool.append(t)
        t.start()
    for t in thread_pool:
        t.join()
