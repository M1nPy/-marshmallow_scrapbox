from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv


with open("pathstr.txt","r") as f:
    pathstr=f.read().strip()

options=Options()
driver_path="chromedriver.exe"
options = webdriver.chrome.options.Options()
options.add_argument("user-data-dir="+pathstr)
browser = webdriver.Chrome(executable_path=driver_path, options=options)

def get_questions_from_marshmallow():
    root_url = 'https://marshmallow-qa.com/messages/answered?page=%s' #確認済みのマシュマロ
    counter = 1
    questions = []
    #ログイン処理

    browser.get('https://marshmallow-qa.com/messages/answered')

    # browser.find_element_by_xpath("/html/body/main/div/div[2]/div[4]/a").click()
    # browser.find_element_by_xpath('//*[@id="username_or_email"]').send_keys(id_)
    # browser.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    # browser.find_element_by_xpath("//*[@id=\"allow\"]").click()
    # time.sleep(5)
    # #確認済みページへ接続
    # print("2段階認証のパスをチェックし、20秒以内にファイルに保存してください。")
    # for i in range(20):
    #     time.sleep(1.5)
    #     print(20-i)

    # # ２段階認証
    # with open("nidan.txt","r") as f:
    #     nidan=f.read().strip()
    # browser.find_element_by_xpath('//*[@id="challenge_response"]').send_keys(nidan)
    # time.sleep(4)
    # browser.find_element_by_xpath("//*[@id=\"email_challenge_submit\"]").click()
    # time.sleep(6)
    # browser.get(root_url%str(counter))
    # time.sleep(4)

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