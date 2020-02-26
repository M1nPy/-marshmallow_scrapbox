from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv

options=Options()
driver_path="chromedriver.exe"
options = webdriver.chrome.options.Options()
browser = webdriver.Chrome(executable_path=driver_path, options=options)


with open("id.txt","r") as f:
    id_=f.read().strip()
with open("pass.txt","r") as f:
    password=f.read().strip()

def get_questions_from_marshmallow():
    root_url = 'https://marshmallow-qa.com/messages/answered?page=%s' #確認済みのマシュマロ
    counter = 1
    questions = []
    #ログイン処理

    browser.get('https://marshmallow-qa.com/auth/explanation')
    browser.find_element_by_xpath("/html/body/main/div/div[2]/div[4]/a").click()
    browser.find_element_by_xpath('//*[@id="username_or_email"]').send_keys(id_)
    browser.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    browser.find_element_by_xpath("//*[@id=\"allow\"]").click()
    time.sleep(5)
    browser.get(root_url%str(counter)) 
    #確認済みページへ接続
    while True:
        time.sleep(3)
        print(str(counter)+'page.')
        #空っぽのページかチェック
        try:
            if '新着メッセージはありません' in browser.find_element_by_xpath('/html/body/main/div/ul/li/div[1]').text:
                print('新着メッセージはありません1')
                break
        except:
            print('nosuchelementexception3')
            break
        
        #そのページの内容を抽出
        root_now_xpath = '/html/body/main/div/ul/li[%s]/div/div/div[2]/a'
        for i in range(1,400):
            now_item = browser.find_elements_by_xpath(root_now_xpath%str(i))
            if now_item:
                questions.append(now_item[0].text.replace('\n',''))

        try:
            #次のページへいく
            counter += 1
            browser.get(root_url%str(counter))
        except:
            ##次のページへいくボタンがなければ例外が出るので、そこで終了
            print("NoSuchElementException2")
            break
    return questions

glist=get_questions_from_marshmallow()

with open("questionlist.txt","w",encoding="utf-8") as f:
    f.write('\n\n'.join(glist))
print("完了しました。")
time.sleep(999)
# print(get_questions_from_marshmallow())